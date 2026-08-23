#!/sbin/cgi
<?
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file);
include("lib/l10n.inc");
include("lib/log_head.tmpl");

$syslog_file = "/var/log/messages";

flush();

$syslog_status = cfg_get_def($cfg, "syslog.status", "enabled");
if ($syslog_status == "enabled") {
	if (($clr == "yes") && (fileinode($syslog_file) != -1) && !$is_ro) {
		$fh = fopen($syslog_file, "w");
		fclose($fh);
                @unlink($syslog_file+".0");
                @unlink($syslog_file+".1");
		system("logger 'Messages cleared.'");
	}
	echo "<pre>";
	$fp = @fopen($syslog_file, "r");
	if ($fp > -1) {
		while(!feof($fp)) {
			$line=fgets($fp,512);
			echo HtmlSpecialChars($line);
		}
	}
	fclose($fp);
	echo "</pre>";
} else {
	include("lib/err_syslog.tmpl");
}

include("lib/log_tail.tmpl");
>
