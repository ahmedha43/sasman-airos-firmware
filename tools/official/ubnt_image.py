#!/usr/bin/env python3
"""Unpack, repack and verify legacy UBNT XM/XW firmware containers.

This preserves the official kernel/u-boot/EXEC payloads and replaces only rootfs.
It does not create or claim a Ubiquiti RSA signature.
"""
from __future__ import annotations
import argparse
import json
import struct
import zlib
from pathlib import Path

HEADER_SIZE = 268
PART_SIZE = 56
CRC_SIZE = 8
END_MAGICS = (b"END.", b"ENDS")


def parse_parts(data: bytes):
    if len(data) < HEADER_SIZE:
        raise ValueError("image is shorter than UBNT header")
    parts = []
    off = HEADER_SIZE
    while off + 4 <= len(data):
        magic = data[off:off + 4]
        if magic in END_MAGICS:
            if off + 12 > len(data):
                raise ValueError("truncated END record")
            return parts, off
        if magic not in (b"PART", b"EXEC"):
            raise ValueError(f"unexpected record magic {magic!r} at offset {off}")
        if off + PART_SIZE > len(data):
            raise ValueError("truncated part header")
        header = data[off:off + PART_SIZE]
        name = header[4:20].split(b"\0", 1)[0].decode("latin1")
        data_size = struct.unpack_from(">I", header, 48)[0]
        allocated = struct.unpack_from(">I", header, 52)[0]
        data_start = off + PART_SIZE
        data_end = data_start + data_size
        crc_end = data_end + CRC_SIZE
        if crc_end > len(data):
            raise ValueError(f"truncated data for {name}")
        stored_crc = struct.unpack_from(">I", data, data_end)[0]
        calc_crc = zlib.crc32(header + data[data_start:data_end]) & 0xffffffff
        parts.append({
            "offset": off,
            "magic": magic.decode("latin1"),
            "name": name,
            "header": header,
            "data_start": data_start,
            "data_end": data_end,
            "data_size": data_size,
            "allocated": allocated,
            "stored_crc": stored_crc,
            "calc_crc": calc_crc,
            "crc_ok": stored_crc == calc_crc,
        })
        off = crc_end
    raise ValueError("END record not found")


def unpack(args):
    data = Path(args.image).read_bytes()
    parts, end_offset = parse_parts(data)
    root = next((p for p in parts if p["name"] == "rootfs"), None)
    if root is None:
        raise SystemExit("rootfs partition not found")
    marker = data[:40].split(b"\0", 1)[0].decode("latin1")
    if args.board and not marker.startswith(args.board):
        raise SystemExit(f"board marker mismatch: got {marker!r}, expected prefix {args.board!r}")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rootfs_path = out / "rootfs.squashfs"
    rootfs_path.write_bytes(data[root["data_start"]:root["data_end"]])
    meta = {
        "source": str(args.image),
        "header_marker": marker,
        "header_version": data[4:260].split(b"\0", 1)[0].decode("latin1"),
        "file_size": len(data),
        "end_offset": end_offset,
        "parts": [{k: p[k] for k in ("name", "magic", "data_size", "allocated", "crc_ok")} for p in parts],
        "rootfs_section": {k: root[k] for k in ("data_start", "data_end", "data_size", "allocated")},
    }
    (out / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(meta, indent=2))


def repack(args):
    source = Path(args.image).read_bytes()
    replacement = Path(args.rootfs).read_bytes()
    parts, end_offset = parse_parts(source)
    root = next((p for p in parts if p["name"] == "rootfs"), None)
    if root is None:
        raise SystemExit("rootfs partition not found")
    if len(replacement) > root["allocated"]:
        raise SystemExit(f"rootfs is {len(replacement)} bytes, partition allows {root['allocated']}")
    header = bytearray(source[:HEADER_SIZE])
    struct.pack_into(">II", header, 260, zlib.crc32(header[:260]) & 0xffffffff, 0)
    output = bytearray(header)
    for p in parts:
        part_header = bytearray(p["header"])
        payload = source[p["data_start"]:p["data_end"]]
        if p["name"] == "rootfs":
            payload = replacement
        struct.pack_into(">I", part_header, 48, len(payload))
        crc = zlib.crc32(part_header + payload) & 0xffffffff
        output.extend(part_header)
        output.extend(payload)
        output.extend(struct.pack(">II", crc, 0))
    end_record = bytearray(source[end_offset:end_offset + 12])
    struct.pack_into(">II", end_record, 4, zlib.crc32(output) & 0xffffffff, 0)
    output.extend(end_record)
    Path(args.out).write_bytes(output)
    print(f"wrote {args.out} ({len(output)} bytes)")
    print("WARNING: output has updated structural CRCs but is not RSA-signed by Ubiquiti")


def verify(args):
    data = Path(args.image).read_bytes()
    parts, end_offset = parse_parts(data)
    header_crc = struct.unpack_from(">I", data, 260)[0]
    header_ok = header_crc == (zlib.crc32(data[:260]) & 0xffffffff)
    end_crc = struct.unpack_from(">I", data, end_offset + 4)[0]
    outer_ok = end_crc == (zlib.crc32(data[:end_offset]) & 0xffffffff)
    print(f"header_crc_ok={header_ok}")
    for p in parts:
        print(f"part={p['name']} data={p['data_size']} allocated={p['allocated']} fit={p['data_size'] <= p['allocated']} crc_ok={p['crc_ok']}")
    print(f"outer_crc_ok={outer_ok}")
    if not header_ok or not outer_ok or any(not p["crc_ok"] or p["data_size"] > p["allocated"] for p in parts):
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p_unpack = sub.add_parser("unpack")
    p_unpack.add_argument("image")
    p_unpack.add_argument("out")
    p_unpack.add_argument("--board", default="")
    p_unpack.set_defaults(func=unpack)
    p_repack = sub.add_parser("repack")
    p_repack.add_argument("image")
    p_repack.add_argument("rootfs")
    p_repack.add_argument("out")
    p_repack.set_defaults(func=repack)
    p_verify = sub.add_parser("verify")
    p_verify.add_argument("image")
    p_verify.set_defaults(func=verify)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
