#!/sbin/cgi
<?
include("lib/settings.inc");
include("lib/system.inc");
include("lib/link.inc");
$cfg = @cfg_load($cfg_file);
include("lib/l10n.inc");
>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"
 "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title><? echo dict_translate("Crash Log Report"); ></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Pragma" content="no-cache">
<link rel="shortcut icon" href="/251204.1815/favicon.ico" >
<link href="/251204.1815/jquery-ui.css" rel="stylesheet" type="text/css">
<link href="/251204.1815/style.css" rel="stylesheet" type="text/css">
<script type="text/javascript" language="javascript" src="jsl10n.cgi?l=<? echo $lng; >&v=/251204.1815"></script>
<script type="text/javascript" language="javascript" src="/251204.1815/jsval.js"></script>
<script type="text/javascript" language="javascript" src="/251204.1815/util.js"></script>
<script type="text/javascript" src="/251204.1815/crashlog.js"></script>
<script type="text/javascript" src="/251204.1815/js/jquery.js"></script>
<script type="text/javascript" src="/251204.1815/js/jquery.utils.js"></script>

<script type="text/javascript">

var wd_reset = <? echo wd_reset(); >;
var label = <? echo get_ubntbox_label(); >;
var autoack = '<? $autoack = ""; echo cfg_get_autoack($cfg, $wlan_iface, $autoack); >' == 'enabled';

$(document).ready(function(){
	getData();
	getCrashLog();
	$('#crash_log_email').bind('change', checkEmailAddress);
	$('#crash_log_content_label').bind('click', toggle_crashlog);
	$('#crash_log_send_button').bind('click', send_crashlog);
	$('#crash_log_dismiss_button').bind('click', remove_warning);
});

</script>
</head>
<body class="popup">
<form id="chrashlog" name="chrashlog" enctype="multipart/form-data" action="<? echo htmlspecialchars($PHP_SELF);>" method="POST">
	<input type="hidden" name="token" value="<? echo $X_ACCESS_TOKEN; ?>" />
	<table cellspacing="0" cellpadding="0" class="popup">
		<tr><th colspan="2"><div id="clErrDiv" class="ui-state-error ui-corner-all initial_hide errors"></div></th></tr>
		<tr><caption colspan="2">
			<b><? echo dict_translate("Unexpected reboot detected. The following information will be reported to Ubiquiti."); ></b>
			<p><? echo dict_translate("Device crashes can be caused by unstable power. Please check PoE adapter, ethernet cable and connectors."); ></p>
		</caption></tr>
			<tr>
				<td valign="top" style="width: 50%">
					<div class="fieldset">
						<div class="row">
							<span class="label"><? echo dict_translate("Device Model"); >:</span>
							<span class="value" id="crash_log_device_model">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("Label"); >:</span>
							<span class="value" id="crash_log_label">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("Country Code"); >:</span>
							<span class="value" id="crash_log_ccode">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("Channel Width"); >:</span>
							<span class="value" id="crash_log_chan_bw">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("Connections Count"); >:</span>
							<span class="value" id="crash_log_sta_count">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("Firmware Version"); >:</span>
							<span class="value" id="crash_log_fw_version">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("TDD Framing Status"); >:</span>
							<span class="value" id="crash_log_ff_mode">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("TDD Framing Duration"); >:</span>
							<span class="value" id="crash_log_ff_duration">&nbsp;</span>
						</div>
					</div>
				</td>
				<td valign="top" style="width: 50%">
					<div class="fieldset">
						<div class="row">
							<span class="label"><? echo dict_translate("MAC"); >:</span>
							<span class="value" id="crash_log_mac">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("Frequency"); >:</span>
							<span class="value" id="crash_log_frequency">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("Wireless Mode"); >:</span>
							<span class="value" id="crash_log_wmode">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("Wireless Security"); >:</span>
							<span class="value" id="crash_log_security">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("Reset By Watchdog"); >:</span>
							<span class="value" id="crash_log_reset_wd">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("Distance"); >:</span>
							<span class="value" id="crash_log_distance">&nbsp;</span>
						</div>
						<div class="row">
							<span class="label"><? echo dict_translate("DL/UL Ratio"); >:</span>
							<span class="value" id="crash_log_ff_dlulratio">&nbsp;</span>
						</div>
					</div>
				</td>
			</tr>
		<tr>
			<td>
				<div class="row">
					<span class="label"><? echo dict_translate("Comments"); >:</span>
					<input type="text" style="width: 157%" class="value input--full" id="crash_log_comment" placeholder="Please provide any information that can help us reproduce the issue.">&nbsp;</span>
				</div>
				<div class="row">
					<span class="label"><? echo dict_translate("E-mail"); >:</span>
					<input type="text" style="width: 157%" class="value" id="crash_log_email" placeholder="Please enter your e-mail if you're willing to help us troubleshooting.">&nbsp;</span>
				</div>
			</td>
		</tr>
		<tr>
			<td>
				<div class="row">
					<span class="label" style="font-weight: bold;">
						<a href="" id="crash_log_content_label"><? echo dict_translate("Crashlog"); >&nbsp;<span id="crash_log_arrow">&gt;&gt;</span></a>
					</span>
				</div>
			</td>
			<td style="text-align: right; vertical-align: middle;">
				<input type="button" style="margin: 5px;" id="crash_log_send_button" value="<? echo dict_translate("Send");>" >
				<input type="button" style="margin: 5px;" onclick="location.href='/support.cgi';" value="<? echo dict_translate("Download Support Info");>" >
				<input type="button" style="margin: 5px;" id="crash_log_dismiss_button" value="<? echo dict_translate("Dismiss");>" >
			</td>
		</tr>
		<tr>
			<td colspan="2">
				<div style="max-width: 708px;">
					<pre id="crash_log_content" style="display:none;"></pre>
				</div>
			</td>
		</tr>
	</table>
</form>
</body>
</html>
