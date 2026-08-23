#!/sbin/cgi
<?
include("lib/settings.inc");
include("lib/l10n.inc");
include("lib/misc.inc");
include("lib/link.inc");
>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title><? echo dict_translate("DFS"); ></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Pragma" content="no-cache">
<link rel="shortcut icon" href="/251204.1815/favicon.ico" >
<link href="/251204.1815/style.css" rel="stylesheet" type="text/css">
</head>

<body class="popup">
<script type="text/javascript" src="/251204.1815/js/jquery.js"></script>
<script type="text/javascript" src="/251204.1815/js/jquery.utils.js"></script>
<script type="text/javascript" src="/251204.1815/js/jquery.dataTables.js"></script>
<script type="text/javascript" src="/251204.1815/js/jquery.ui.js"></script>
<script type="text/javascript" src="/251204.1815/util.js"></script>
<script type="text/javascript" src="/251204.1815/common.js"></script>
<script type="text/javascript" language="javascript" src="jsl10n.cgi?l=<? echo htmlspecialchars($ui_language); >&v=/251204.1815"></script>
<script type="text/javascript" language="javascript">

</script>
<script type="text/javascript" src="/251204.1815/nolinfo.js"></script>

<br>
<form action="<?echo htmlspecialchars($PHP_SELF);>" method="GET">
<table cellspacing="0" cellpadding="0" align="center">
	<tr>
		<td>
			<table id="dfs_nolinfo" class="listhead dataTables_head" cellspacing="0" cellpadding="0">
				<thead>
					<tr>
						<th><? echo dict_translate("Frequency"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("Channel Width"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("Frequency Band"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("Time Remaining"); >&nbsp;&nbsp;&nbsp;</th>
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
