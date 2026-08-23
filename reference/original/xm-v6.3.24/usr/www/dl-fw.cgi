#!/sbin/cgi
<?
include("lib/settings.inc");
include("lib/misc.inc");
#----------
# DEBUG
#----------

#$action = "progress";#download;#eula;
#$fw_url = "http://www.ubnt.com/downloads/XM-v5.5.6.build17762.bin";
#$fw_checksum = "3f93e831a2640df16f47767086d95ff3";

#----------

Function getRetVal $cmd_code
(
	$res = (($cmd_code & 65280) / 256);
	if ($res > 127) {
		$res -= 256;
	}
	return $res;
);

Function exitResult $status, $message
(
	header("Content-Type: application/json");
	echo "{ \"status\" : $status, \"message\" : \"$message\" }";
	exit;
);

Function calcMd5Sum $fpath
(
	global $cmd_md5sum;
	$md5 = "";

	if (fileInode($fpath) != -1) {
		$cmd = "$cmd_md5sum $fpath | cut -d ' ' -f 1";
		exec($cmd, $lines, $res);
		$res = getRetVal($res);
		if ($res == 0) {
			$md5 = $lines[0];
		}
	}

	return $md5;
);

Function getEula
(
	global $cmd_trigger, $eula_html, $eula_url;
	$cmd = "$cmd_trigger $eula_url >$eula_html 2>&1";
	exec($cmd, $lines, $res);
	$res = getRetVal($res);
	if ($res != 0) {
		exitResult(-2, "Failed to downlad EULA.");
	}
	return $res;
);

Function getFirmware $fw_url
(
	global $cmd_trigger, $firmware_file, $eula_html, $eula_url, $progress_file, $fw_checksum;

	@unlink($firmware_file);
	$f_url = EscapeShellArg($fw_url);
	$cmd = "$cmd_trigger -d 'Referer: $eula_url' -s $f_url > $firmware_file 2>$progress_file";
	exec($cmd, $lines, $res);
	Unlink($progress_file);
	if ($res != 0) {
        	Unlink($eula_html);
		exitResult(-3, "Firmware download failed.");
	}

	$md5 = calcMd5Sum($firmware_file);
	if ($md5 != $fw_checksum) {
        	Unlink($eula_html);
		exitResult(-3, "Firmware download failed - checksum is invalid.");
	}

	return $res;
);

Function doDownload $fw_url
(
	$fw_url = getParams($fw_url);
	$tab = "\t";
	if ((IsSet($fw_url) != 1) || strlen($fw_url) < 10 || 
		strchr($fw_url, ' ') || strchr($fw_url, $tab)) { # TODO: rest of required parameters
		exitResult(-1, "Invalid URL");
	}

	getEula();
	getFirmware($fw_url);
	exitResult(0, "OK");

	return 0;
);

Function doProgress
(
	global $progress_file;

	header("Content-Type: application/json");
	if (fileInode($progress_file) != -1) {
		$str = "sed 's/^M$//' $progress_file | tail -n 1 | ";
		$str += "sed 's/^.\([0-9]\+\).%$/";
		$str += "{\"status\" : 0, \"percent\" : \1, \"bytes\" : \"\2\"}\n/'";
		PassThru($str);
	}
	else {
		echo "{ \"status\" : -1 }";
	}
	return 0;
);

Function getParams $url
(
	global $update_info, $fw_url, $fw_checksum;
        
        if (fileInode($update_info) != -1 &&
                (IsSet($url) != 1 || strlen($url) < 10)
        ) {
                $str = "sed 's/.*\"url\"[]*:[]*\"\\([^\"]*\\)\"";
                $str += ".*\"checksum\"[]*:[]*\"\\([^\"]*\\)\".*/";
                $str += "global \\\$fw_url, \\\$fw_checksum; \\\$fw_url=\"\\1\";\\\$fw_checksum=\"\\2\";/' ";
                $str += " $update_info";
                $str = StripSlashes($str);
                exec($str, $ret);
                if (strstr($ret[0], "fw_url") && strstr($ret[0], "fw_checksum")) {
	                eval($ret[0]);
        	        $url = $fw_url;
                }
        }
        return $url;
);

Function doEula
(
	global $eula_html;
        
	$eula_ready = 0;
	if (fileInode($eula_html) != 1) {
        	$eula_ready = 1;
        } else {
        	if (getEula() == 0) {
                	$eula_ready = 1;
                }
        }
        if ($eula_ready == 1) {
	        PassThru("cat " + $eula_html);
        }
        return 0;
);

if ($action == "download" && $REQUEST_METHOD == "POST" && $X_ACCESS_TOKEN == $token) {
	doDownload($fw_url);
} elseif ($action == "progress") {
	doProgress();
} elseif ($action == "eula") {
	doEula();
} else {
	exitResult(-1, "What to do?");
}
>
