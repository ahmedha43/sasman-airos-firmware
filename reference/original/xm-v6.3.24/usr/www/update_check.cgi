#!/sbin/cgi
<?
include("lib/settings.inc");
include("lib/l10n.inc");

function need_to_check
(
	global $update_info, $check_interval;
	$do_check = 1;

	$last_checked = fileMtime($update_info);
	if ($last_checked != -1) {
		$diff = Time() - $last_checked;
		if ($diff < $check_interval) {
			$do_check = 0;
		}
	}
	return $do_check;
);

function check_for_update
(
	global $board_id, $check_url, $cmd_trigger, $update_info, $board_hwaddr, $active_language;
	
        @unlink($update_info);
	$temp_file = "/tmp/.update.tmp";
	
	$version = @file("/usr/lib/version");
	$md5 = md5($board_hwaddr);
	$params = "sysid=$board_id&fwver=$version&md5=$md5&lang=$active_language";

	$res = 0;
	exec("$cmd_trigger '$check_url?$params' >$temp_file 2>&1", $lines, $res);
	if ($res == 0) {
		rename($temp_file, $update_info);
	}
	else {
		@unlink($temp_file);
	}
);

if (IsSet($force) || need_to_check()) {
	check_for_update();
}

header("Content-Type: application/json");
if (fileInode($update_info) != -1) {
	PassThru("cat $update_info");
}
else {
	echo "{ \"connect\": \"false\" }";
}

>
