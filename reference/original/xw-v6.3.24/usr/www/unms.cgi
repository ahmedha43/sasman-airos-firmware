#!/sbin/cgi
<?
include("lib/settings.inc");
include("lib/l10n.inc");
include("lib/help.inc");
$cfg = @cfg_load($cfg_file);
$success = 0;
UnSet($error_msg);

if ($REQUEST_METHOD=="POST" && $X_ACCESS_TOKEN == $token)
{
	cfg_set($cfg, "unms.uri", $unmsKey);
	cfg_save($cfg, $cfg_file);
	cfg_set_modified($cfg_file);
	$success = 1;
}

><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"
 "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title><? echo dict_translate("Ubiquiti Network Management System"); ></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Pragma" content="no-cache">
<link rel="shortcut icon" href="/251204.1815/favicon.ico" >
<link href="/251204.1815/jquery-ui.css" rel="stylesheet" type="text/css">
<link href="/251204.1815/style.css" rel="stylesheet" type="text/css">
<script type="text/javascript" language="javascript" src="jsl10n.cgi?l=<? echo $lng; >&v=/251204.1815"></script>
<script type="text/javascript" language="javascript" src="/251204.1815/system.js"></script>
<script type="text/javascript" language="javascript" src="/251204.1815/jsval.js"></script>
<script type="text/javascript" language="javascript" src="/251204.1815/util.js"></script>
<script type="text/javascript" src="/251204.1815/js/jquery.js"></script>
<script type="text/javascript" src="/251204.1815/js/jquery.ui.js"></script>
<script type="text/javascript" src="/251204.1815/js/jquery.cookie.js"></script>
<script type="text/javascript" src="/251204.1815/js/jquery.utils.js"></script>
<script type="text/javascript" src="/251204.1815/js/jquery.blockUI.js"></script>
<script type="text/javascript">

<?
if ($success == 1) { ?>
$(document).ready(function() {
	window.opener.doSubmit();
	window.close();
});
<? } ?>

</script>
</head>
<body class="popup">
	<tr><td colspan="2"><?include("lib/error.tmpl");></td></tr>
	<form id="unms" name="unms" enctype="multipart/form-data" action="<? echo htmlspecialchars($PHP_SELF);>" method="POST" onSubmit="return validateStandard(this, 'error');">
	<input type="hidden" name="token" value="<? echo $X_ACCESS_TOKEN; ?>" />
	<table cellspacing="0" cellpadding="0" align="center" class="popup">
	<tr><th colspan="2"> <? echo dict_translate("Please enter a valid UNMS Key"); ></th></tr>
	<tr><td colspan="2" class="sep">&nbsp;</td></tr>
	<tr class="unms_entry">
		<td class="f"><? echo dict_translate("Key"); >:</td>
		<td class="f" colspan="2"><input type="text" style="width: 500px;" name="unmsKey" id="unmsKey" realname="<? echo dict_translate("msg_unms_key|UNMS Key"); >" req="1" callback="validateUnmsKey" value=""></td>
	</tr>
	<tr class="unms_entry">
		<td align="center" colspan="2">
		<input type="submit" id="btn_save" value="<? echo dict_translate("Save"); >">
        <input type="button" id="btn_close" value="<? echo dict_translate("Close"); >" onClick="window.close();"></td>
	</tr>
</table>

</form>
</body>
</html>
