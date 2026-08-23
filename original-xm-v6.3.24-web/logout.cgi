#!/sbin/cgi
<?
include("lib/settings.inc");
include("lib/utils.inc");

$session = get_session_id($$session_id, $AIROS_SESSIONID, $HTTP_USER_AGENT);
if (isset($session) && strlen($session) == 32) {
	Exec(EscapeShellCmd("/bin/ma-deauth $db_sessions $session"));
	SetCookie($session_id, "-", time() - 36000);
	if (!isset($redirect) || $redirect != "false") {
		Header("Location: /login.cgi");
	}
}
>
