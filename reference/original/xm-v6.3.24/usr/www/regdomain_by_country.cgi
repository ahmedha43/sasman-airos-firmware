#!/sbin/cgi
<?
    header("Content-Type: application/json");
	include("lib/settings.inc");
	$cfg = @cfg_load($cfg_file);
	include("lib/link.inc");

    if (strlen($chanbw) == 0 || !ereg("^[[:digit:]]+$", $chanbw)) {
        $chanbw = cfg_get_def($cfg, "radio.1.chanbw", "0");
    }

    generate_json_regdomain($country, "full_regdomain", $radio["devdomain"], $radio["regdomain_flags"], $chanbw);
    echo $full_regdomain;
    exit;
>