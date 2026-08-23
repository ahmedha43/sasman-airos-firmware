#!/sbin/cgi
<?
include("lib/settings.inc");
$l10n_no_cookies = 1;
include("lib/l10n.inc");

$error_msg = "";

if (isset($ticketid) && (strlen($ticketid) > 0)) {
	$redir_url = "/";

	if (!ereg("^[[:xdigit:]]{32}$", $ticketid)) {
		Header("Location: $redir_url");
		exit;
	}

	/* check ticket existence */
	$cmd = "/bin/ma-show " + $db_tickets + " " + $ticketid;
	unset($lines); unset($rc);
	exec(EscapeShellCmd($cmd),$lines,$rc);

	if ($rc == 0) {
		$user_regexp = "[[:space:]]+user:[[:space:]]+\\'([[:print:]]+)\\'$";
		$username = "mcuser";
		$i = 0; $size = count($lines);
		while ($i < $size) {
			if (ereg($user_regexp, $lines[$i], $res)) {
				$username = $res[1];
				$i = $size;
			}
			$i++;
		}
		/* authorize the session, that brought this ticket */
		$cmd = "/bin/ma-auth " + $db_sessions + " " +
			$$session_id + "  " + $username;
		unset($lines); unset($rc);
		exec(EscapeShellCmd($cmd), $lines, $rc);
		if ($rc == 0) {
			/* remove the ticket! */
			$cmd = "/bin/ma-rm " + $db_tickets + " " + $ticketid;
			exec(EscapeShellCmd($cmd));

			/* if we have uri preference - redirect */
			if (isset($uri) && strlen($uri) > 0) {
				$redir_url = urldecode($uri);
			} else {
				$redir_url = "/index.cgi";
			}
		} elseif (strlen($r) == 0) {
			$redir_url = $PHP_SELF + "?r=1&ticketid=" + $ticketid;
			if (isset($uri) && strlen($uri) > 0) {
				$redir_url = $redir_url + "&uri=" + urlencode($uri);
			}
		}
	}

	if (strlen($redir_url) == 0) {
		$redir_url = "/";
	}
	Header("Location: " + $redir_url);
	exit;
}
>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title><? echo dict_translate("Login"); ></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta http-equiv="Cache-Control" content="no-cache">
<link rel="shortcut icon" href="/251204.1902/favicon.ico" >
<link href="/251204.1902/login.css" rel="stylesheet" type="text/css">
<link href="/251204.1902/style.css" rel="stylesheet" type="text/css">
<script type="text/javascript" language="javascript" src="jsl10n.cgi?l=<? echo $lng; >&v=/251204.1902"></script>
<script type="text/javascript" language="javascript" src="/251204.1902/util.js"></script>
<script type="text/javascript" src="/251204.1902/js/jquery.js"></script>
<script type="text/javascript" language="javascript">
//<!--
$(document).ready(function(){
 $("#ticketid").focus();
});
//-->
</script>
</head>
<body>
<table border="0" cellpadding="0" cellspacing="0" align="center" class="loginsubtable">
<tr>
<td valign="top"><a href="/index.cgi"><img src="/251204.1902/images/airos_logo.png" title="airOS" alt="airOS"></a></td>
<td class="loginsep">
<form enctype="multipart/form-data" id="loginform" method="post" action="<?echo htmlspecialchars($PHP_SELF);>">
<input type="hidden" name="uri" id="uri" value="<? echo HtmlSpecialChars($uri); >" />
<table border="0" cellpadding="0" cellspacing="0" class="logintable" align="center">
	<tr><td colspan="2" align="center"> &nbsp;
	<? if (isset($error_msg) && (strlen($error_msg) > 0)) { >
		<span class="error">
		<? echo $error_msg; >
		</span>
	<? } >
	</td></tr>
	<tr>
		<td><label for="ticketid"><? echo dict_translate("Ticket"); >:</label></td>
		<td><input type="text" name="ticketid" id="ticketid" /></td>
	</tr>
	<tr>
		<td></td>
		<td class="submit"><input name="submit" type="submit" id="submit" value="<? echo dict_translate("Login"); >" /></td>
	</tr>
</table>
</form>
</td>
</tr>
</table>
</body>
</html>
