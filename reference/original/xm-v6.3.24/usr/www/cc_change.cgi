#!/sbin/cgi
<?
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file);
include("lib/l10n.inc");
include("lib/link.inc");
include("lib/misc.inc");
include("lib/help.inc");
>

<html>
<head>
<link href="/251204.1902/style.css" rel="stylesheet" type="text/css">
<script type="text/javascript" language="javascript">

$(document).ready(function() {
	<? if ($radio1_ccode_fixed == 0 && $radio1_ccode_locked != 1) {>
	       	$("#country_select").val(0);
        <?}>
        $('#errmsg').hide();
});
</script>
</head>
<body>
<table border="0" cellpadding="0" cellspacing="0" align="center">
	<tr>
		<td colspan="2" align="center">
		    <div id="errmsg" class="error" style="display:none;">
		       &nbsp;
		    </div>
		</td>
	</tr>
	<tr>
		<td><label for="country_select"><? echo dict_translate("Country"); >:</label></td>
		<td>
		     <select name="country_select" id="country_select" <? if ($radio1_ccode_locked == 1) { echo "disabled";} >>
								<? if ($radio1_ccode_fixed == 0 && $radio1_ccode_locked != 1) { >
									<option value="0"><? echo dict_translate("Select New Country");></option>
								<? } 
								   include("lib/ccode.inc");
                                                                >
		     </select>
		</td>
	</tr>
	<tr>
		<td colspan="2">
			<? include("lib/legal.inc"); echo legal_terms_of_use(); ?>
		</td>
	</tr>
</table>
</body>
</html>

