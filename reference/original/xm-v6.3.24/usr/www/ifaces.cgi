#!/sbin/cgi
<?
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file_bak);
include("lib/l10n.inc");
include("lib/misc.inc");
include("lib/link.inc");
>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title><? echo dict_translate("Interfaces"); ></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Pragma" content="no-cache">
<link rel="shortcut icon" href="/251204.1902/favicon.ico" >
<link href="/251204.1902/style.css" rel="stylesheet" type="text/css">
</head>

<body class="popup">
<script type="text/javascript" src="/251204.1902/js/jquery.js"></script>
<script type="text/javascript" src="/251204.1902/js/jquery.utils.js"></script>
<script type="text/javascript" src="/251204.1902/js/jquery.dataTables.js"></script>
<script type="text/javascript" src="/251204.1902/js/jquery.ui.js"></script>
<script type="text/javascript" src="/251204.1902/util.js"></script>
<script type="text/javascript" src="/251204.1902/common.js"></script>
<script type="text/javascript" language="javascript" src="jsl10n.cgi?l=<? echo $lng; >&v=/251204.1902"></script>
<script type="text/javascript" language="javascript">

var if_global = {
	'_': '_'
};

</script>
<script type="text/javascript" src="/251204.1902/ifaces.js"></script>

<br>
<form action="<?echo htmlspecialchars($PHP_SELF);>" method="GET">
<table cellspacing="0" cellpadding="0" align="center">
	<tr>
		<td>
			<table id="if_list" class="listhead dataTables_head" cellspacing="0" cellpadding="0">
				<thead>
					<tr>
						<th><? echo dict_translate("Interface"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("MAC Address"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("MTU"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("IP Address"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("RX Bytes"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("RX Errors"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("TX Bytes"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("TX Errors"); >&nbsp;&nbsp;&nbsp;</th>
					</tr>
				</thead>
				<tbody>
				</tbody>
			</table>
		</td>
	</tr>
	<tr>
		<td class="change">
			<input type="button" id="_refresh" value="<? echo dict_translate("Refresh"); >">
		</td>
	</tr>
</table>
</form>
</body>
</html>
