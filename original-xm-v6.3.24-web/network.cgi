#!/sbin/cgi
<?
include("lib/settings.inc");
include("lib/l10n.inc");
include("lib/link.inc");
include("lib/misc.inc");
include("lib/system.inc");
  
UnSet($error_msg);
if ($REQUEST_METHOD == "POST" && $X_ACCESS_TOKEN == $token) {
	if (isset($network_data) && strlen($network_data) > 100) {
		if (cfg_put($cfg_file, $network_data) != 0) {
        		$error_msg = dict_translate("msg_cfg_save_failed|Failed to save changes. Try again.");
		}
        } else {
        	$error_msg = dict_translate("msg_cfg_invalid|Failed to save changes. Invalid configuration data received. Try again.");
	}
}

$cfg = @cfg_load($cfg_file);
if ($cfg == -1) {
         include("lib/busy.tmpl");
         exit;
}
$netmode = cfg_get_def($cfg, "netmode", "bridge");
$wmode = strtolower(cfg_get_def($cfg, "radio.1.mode", "managed"));

include("lib/network.tmpl");
>
