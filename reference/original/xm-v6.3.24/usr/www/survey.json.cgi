#!/sbin/cgi
<?
include("lib/settings.inc");

if (strlen($iface) == 0) {
	$iface = $wlan_iface;
}
PassThru(EscapeShellCmd("iwlist $iface scan $update") + " | " + $cmd_scanparser);
>
