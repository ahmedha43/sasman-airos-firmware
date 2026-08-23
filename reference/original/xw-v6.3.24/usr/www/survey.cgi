#!/sbin/cgi
<?
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file);
$running_cfg = @cfg_load($cfg_file_bak);
include("lib/l10n.inc");
include("lib/link.inc");
include("lib/misc.inc");

if (!IsSet($iface) || strlen($iface) == 0 || !ereg("^[[:alnum:]]+$", $iface)) {
	$iface = $wlan_iface;
}

init_board_inc($iface);

$wmode = w_get_mode($iface);

if ($feature_ap_scan != 1) {
	if ($wmode == 3) {
		include("lib/err_scan.tmpl");
		exit;
	}
}

$chanlist_active = file("/proc/sys/net/"+$iface+"/chanlist");
$chans =  $chanlist_active[0];

$chanbw = cfg_get_def($running_cfg, "radio.1.chanbw", "40");

$radio1_airmax_only = htmlspecialchars($radio1_airmax_only);
$mode = htmlspecialchars($mode);
$iface = htmlspecialchars($iface);

include("lib/survey.tmpl");
>
