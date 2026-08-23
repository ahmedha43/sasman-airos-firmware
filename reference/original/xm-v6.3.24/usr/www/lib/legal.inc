<?

Function legal_terms_of_use (
	$tos1 = dict_translate("license_agreement|This Ubiquiti Inc. radio device must be professionally installed. Properly installed shielded Ethernet cable and earth grounding must be used as conditions of product warranty. It is the installer's responsibility to follow local country regulations including operation within legal frequency channels, output power, and Dynamic Frequency Selection (DFS) requirements. You are responsible for keeping the unit working according to these rules.");

	$tos1l = dict_translate("license_agreement_lf|You have selected a \"licensed\" country option in the airOS firmware. Please note that your use of the licensed firmware is subject to your compliance at all times with the terms and restrictions of {link_lf}the Licensed Firmware User Agreement (LFUA)</a>, including having received valid authorization from applicable governmental authorities to configure and use Ubiquiti products beyond their standard radio frequency settings. Ubiquiti reserves the right to request such information and records as may be reasonably necessary to confirm your compliance with the LFUA.");
	$tos1l = legal_replace_links($tos1l);

	$tos2 = dict_translate("license_agreement_chk|I have read and agree to the TERMS OF USE, {link_eula}EULA</a> and {link_pp}PRIVACY POLICY</a>");
	$tos2 = legal_replace_links($tos2);

	$tos3 = dict_translate("license_agreement_lf_chk|I have read and agree to the TERMS OF USE, {link_eula}EULA</a>, {link_lf}LFUA</a> and {link_pp}PRIVACY POLICY</a>");
	$tos3 = legal_replace_links($tos3);

	return "<div class='legal_container'>" +
		"<strong>" + dict_translate("TERMS OF USE") + "</strong>" +
		"<p>$tos1<br>" +
		"<span class='lfua' style='display: none'><br>$tos1l</span>" +
		"</p>" +
		"<input type='checkbox' id='agreed'></input>" +
		"<label for='agreed'>" +
		"<span class='n_lfua'>$tos2</span>" +
		"<span class='lfua' style='display: none'>$tos3</span>" +
		"</label>" +
		"</div>";
);

Function legal_replace_links $txt (
	$eula_url = localize_help("legal_eula.html");
	$pp_url = localize_help("legal_privacy_policy.html");
	$lf_url = localize_help("legal_licensed_firmware.html");
	$close_btn = dict_translate("Close");
	$txt = ereg_replace("\{link_eula}", "<a href='$eula_url' onclick='return showLegalText(\"$eula_url\", \"$close_btn\")'>", $txt);
	$txt = ereg_replace("\{link_pp}", "<a href='$pp_url' onclick='return showLegalText(\"$pp_url\", \"$close_btn\")'>", $txt);
	$txt = ereg_replace("\{link_lf}", "<a href='$lf_url' onclick='return showLegalText(\"$lf_url\", \"$close_btn\")'>", $txt);

	return $txt;
);

Function legal_footer (
	return legal_replace_links(dict_translate("Ubiquiti {link_eula}EULA</a> and {link_pp}PRIVACY POLICY</a>"));
);

>
<script type="text/javascript" language="javascript">
function handle_licensed(country)
{
	if (country == "511" || country == "2124")
	{
		$(".n_lfua").hide();
		$(".lfua").css("display", "inline");
	}
	else
	{
		$(".lfua").hide();
		$(".n_lfua").css("display", "inline");
	}

}

$(document).ready(
	function()
	{
		$("#country_select").change(function() { handle_licensed($(this).val()); } ).change();
		$("#country").change(function() { handle_licensed($(this).val()); } ).change();
	}
);

</script>
