# Official firmware inputs

The GitHub Actions official-firmware workflow downloads these Ubiquiti firmware inputs directly from the user-provided official URLs:

| Platform | URL | Expected board marker | SHA256 observed |
|---|---|---|---|
| XM | https://dl.ui.com/firmwares/XN-fw/v6.3.24/XM.v6.3.24.33508.251204.1904.bin | `UBNTXM.ar7240` | `3c4cbf7928954fb27d4d85747a70b5af73232175ffa2225ddba5531a0474f1da` |
| XW | https://dl.ui.com/firmwares/XW-fw/v6.3.24/XW.v6.3.24.33508.251204.1816.bin | `UBNTXW.ar934x` | `90457c55c3daae3ebf1fb034dcfd56151316d6d6f464fc21c8fef48ed063fa53` |

The official download page is https://www.ui.com/download/airmax-m. The input files were downloaded and identified as Ubiquiti HIT archive data; the XM file size was 7,599,916 bytes and the XW file size was 7424986 bytes at the time of inspection. The workflow must verify the SHA256 and board marker before processing and must fail closed on mismatch.

These are official firmware inputs, but any modified output is not an official Ubiquiti-signed image. The workflow should label generated assets as structurally repacked / unsigned unless a supported signing mechanism is available.
