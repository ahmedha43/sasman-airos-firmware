#!/sbin/cgi
<?
include("lib/settings.inc");
Function getReturnCode $cmd_code
(
	$res = (($cmd_code & 65280) / 256);
	if ($res > 127) {
		$res -= 256;
	}
	return $res;
);

$ping_size = IntVal($ping_size);
if ($ping_size < 28 || $ping_size > 65507) {
	$ping_size = 56;
}

$ip_addr_rg = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";
$ip6_addr_rg = "^([A-f0-9:]+:+)+[A-f0-9]+$";
$hostname_rg = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$";

if (!IsSet($ip_addr) ||
	(!ereg($ip_addr_rg, $ip_addr) && !ereg($ip6_addr_rg, $ip_addr) && !ereg($hostname_rg, $ip_addr))) {
	$ip_addr = "127.0.0.1";
}

$command = EscapeShellCmd("$cmd_webping -s $ping_size $ip_addr");

UnSet($lines); UnSet($res);
exec($command, $lines, $res);
$res = getReturnCode($res);
$i = 0;
echo $res;
while ($i < count($lines))
{
	echo "|"+$lines[$i];    	
	$i++;
}
>
