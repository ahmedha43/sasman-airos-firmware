#!/sbin/cgi
<?
include("lib/settings.inc");
include("lib/system.inc");
include("lib/misc.inc");

$filename = $fname + ".sh";
$file = $fname + $status;

if (ereg("\.\.\/", $file)) {
	exit;
}

header("Content-Type: application/force-download");
header("Content-Disposition: attachment; filename=" + $filename);
passthru("/bin/cat " + EscapeShellArg("/tmp/persistent/$file"));
exit;
>
