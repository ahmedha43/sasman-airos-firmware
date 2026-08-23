#!/sbin/cgi
<?
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file);
include("lib/l10n.inc");
include("lib/link.inc");
include("lib/misc.inc");
include("lib/help.inc");
include("lib/utils.inc");
include("lib/password.inc");

$idx = get_wlan_index($wlan_iface);
init_board_inc($wlan_iface);

if (IsSet($uri) && !ereg("^\/(\.|[[:alnum:]]|-|_)*$", $uri)) {
	$uri = "/index.cgi";
}

$first_login = "false";
if (is_first_login($cfg, $idx, $uri) != 0) {
	$first_login = "true";
	if ($radio["ccode_fixed"] != 0 || $radio["ccode_locked"] == 1) {
		$country = $radio["ccode"];
	}
}

$is_password_change = is_default_password($cfg);
if ($is_password_change) {
	$is_username_change = is_default_username($cfg);
} else {
	$is_username_change = 0;
}
$error_msg = "";

function get_redirect_uri $postback (
	global $uri;
	if ($postback == "true") {
		return $uri;
	}

	if (strlen($QUERY_STRING) > 4) {
		if (substr($QUERY_STRING, 0, 4) == "uri=") {
			return check_uri(substr($QUERY_STRING, 4, strlen($QUERY_STRING) - 4));
		}
	}
	return "/index.cgi";
);

if (IsSet($country)) {
    if (!ereg("^[[:digit:]]+$", $country)) {
        UnSet($country);
    }
}

if ($REQUEST_METHOD=="POST") {
	$postback = "true";
	if ($lang_changed != "yes") {
		if ($is_username_change) {
			$auth_user = "ubnt";
		} else {
			$auth_user = $username;
		}
		if ($is_password_change) {
			$auth_pass = "ubnt";
		} else {
			$auth_pass = $password;
		}

		$rc = 0;
		if ($is_password_change && ((strlen($password) == 0) || ($password == 'ubnt') || ($password != $password2))) {
			$rc = -1;
		}
		if ($is_username_change && strlen($username) == 0) {
			$rc = -1;
		}
		if ($rc == 0) {
			$rc = PasswdAuth($auth_user, $auth_pass);
		}
		if ($rc == 0) {
			$session = get_session_id($$session_id, $AIROS_SESSIONID, $HTTP_USER_AGENT);
			$cmd = "/bin/ma-auth $db_sessions $session $auth_user";
			exec(EscapeShellCmd($cmd));

            if ($username != $auth_user) {
				cfg_set($cfg, "users.1.name", $username);
            }

			if ($is_password_change) {
				setCryptedPassword($cfg, crypt($password));
				$password_has_changed = 1;
			} else {
				$password_has_changed = 0;
			}
			if ($first_login == "true" || $password_has_changed) {
				change_country($cfg, $idx, $country, $radio["subsystemid"]);
			}
			if ($password_has_changed) {
				# to regenerate /etc/passwd
				exec($cmd_ubntconf);
			}

			# no more use for password change, just to clear cookies if still stored in browser
			check_default_passwd($cfg);

			if (isset($uri) && strlen($uri) > 0) {
				$uri = check_uri($uri);
				Header("Location: " + $uri);
			} else {
				Header("Location: /index.cgi");
			}
			exit;
		} else {
			sleep(3);
			if ($rc > 3) {
				$rc = $rc - 2;
				$error_msg = dict_translate("Too many authentication failures, please try again in $rc seconds.");
			} elseif ($rc > 0) {
				$error_msg = dict_translate("Too many authentication failures, please try again.");
			} else {
				$error_msg = dict_translate("Invalid credentials.");
			}
		}
	}
}
else {
	$postback = "false";
}
>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/DTD/loose.dtd">
<html>
<head>
<title><? echo dict_translate("Login"); ></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta http-equiv="Cache-Control" content="no-cache">
<link rel="shortcut icon" href="/251204.1815/favicon.ico" >
<link href="/251204.1815/login.css" rel="stylesheet" type="text/css">
<link href="/251204.1815/style.css" rel="stylesheet" type="text/css">
<link href="/251204.1815/help.css" rel="stylesheet" type="text/css">
<script type="text/javascript" language="javascript" src="jsl10n.cgi?l=<? echo $lng; >&v=/251204.1815"></script>
<script type="text/javascript" src="/251204.1815/js/jquery.js"></script>
<script type="text/javascript" src="/251204.1815/util.js"></script>
<script type="text/javascript" src="/251204.1815/index.js"></script>
<script type="text/javascript" src="/251204.1815/js/jquery.ui.js"></script>
<? if ($is_password_change) { >
<script type="text/javascript" src="/251204.1815/js/pstrength.js"></script>
<? } >
<script type="text/javascript" language="javascript">
//<!--
var globals = {
	first_login : <? echo $first_login; >,
	postback : <? echo $postback; >,
	fixed : <? if ($radio["ccode_fixed"] == 0) { echo "false"; } else { echo "true"; } >,
	country : "<? echo HtmlSpecialChars($country); >"
};

function onLangChange() {
	$("#lang_changed").val("yes");
	$("#loginform").submit();
}

<? if ($is_password_change) { >
function toggleLoginButton() {
	var u1 = $('#username').val();
	
	if (u1)
	{
		u1 = u1.trim();
	}

	var p1 = $('#password').val();
	var p2 = $('#password2').val();		
	var verdict = $('#PasswordVerdict > span').attr('acceptable');

	var valid = (u1 !== '' && p1 == p2 && p1 != 'ubnt' && verdict == '1');

	var submit_btn = $('#loginform_submit');
	submit_btn.prop('disabled', !valid);
	if (valid)
		submit_btn.removeClass("ui-state-disabled");
	else
		submit_btn.addClass("ui-state-disabled");
}
<? } >

function validateForm() {
	if ($("#lang_changed").val() == "yes")
		return true;

	if ($("#country").val() == "0") {
		$("#errmsg").text("<? echo dict_translate("Please select your country."); >");
		return false;
	}

	if (!$("#agreed").is(":checked")) {
		$("#errmsg").html("<? echo dict_translate("msg_agree_with_terms|To use this product, you must agree to<br>terms of use."); >");
		return false;
	}

	return true;
}

function isMobile() {
	return  navigator.userAgent.match(/Android/i) ||
			navigator.userAgent.match(/BlackBerry/i) ||
			navigator.userAgent.match(/iPhone|iPad|iPod/i) ||
			navigator.userAgent.match(/Opera Mini/i) ||
			navigator.userAgent.match(/IEMobile/i);
}

$(document).ready(function() {
	$("#username").focus();
	cache_images([
		'main_top.png', 'main.png', 'link.png',
		'net.png', '4dv.png', 'srv.png',
		'system.png', 'border.gif', 'spectr.gif']);

	if (globals.first_login) {
		$("#ui_language").change(onLangChange);
		$("#loginform").submit(validateForm);
		if (!globals.postback && !globals.fixed)
			$("#country").val(0);
		else
			$("#country").val(globals.country);
	}

	if (isMobile() || $('.first_login').length) {
		$('.desktopView').addClass("initial_hide");
		$('.mobileView').removeClass("initial_hide");
	} else {
		$('.mobileView').addClass("initial_hide");
		$('.desktopView').removeClass("initial_hide");
	}

<? if ($is_password_change) { >
	$('#password').pStrength($('#username'), $('#PasswordVerdict'), ui_password_strength_opts);
	$('#username').on('input', toggleLoginButton);
	$('#password').on('input', toggleLoginButton);
	$('#password2').on('input', toggleLoginButton);
	toggleLoginButton();
<? } >
});
//-->
</script>
</head>
<? flush(); >
<body class="<? if ($first_login == "true") { echo "first_login"; } ?>">
<table border="0" cellpadding="0" cellspacing="0" align="center" class="loginsubtable">
<form enctype="multipart/form-data" id="loginform" method="post" action="<?echo htmlspecialchars($PHP_SELF);>">
	<tr>
		<td valign="top"><img src="/251204.1815/images/airos_logo.png"></td>
		<td class="loginsep">
				<input type="hidden" name="uri" id="uri" value="<? echo get_redirect_uri($postback); >" />
				<table border="0" cellpadding="0" cellspacing="0" class="logintable" align="center">
					<tr>
						<td colspan="2" align="center">
							<div id="errmsg" class="error">
								<? if (isset($error_msg) && (strlen($error_msg) > 0)) { echo $error_msg; } >
							</div>
						</td>
					</tr>
					<tr>
						<td colspan="2">&nbsp;</td>
					</tr>
					<tr>
						<? if ($is_username_change) { >
						<td><label for="username"><? echo dict_translate("Administrator User Name"); >:</label></td>
						<? } else { >
						<td><label for="username"><? echo dict_translate("User Name"); >:</label></td>
						<? } >
						<td><input class="config" type="text" name="username" id="username" autocomplete="username" maxlength="31" realname="<? echo dict_translate("User Name"); >"/></td>
					</tr>
					<tr>
						<? if ($is_password_change) { >
						<td><label for="password"><? echo dict_translate("New Password"); >:</label></td>
						<? } else { >
						<td><label for="password"><? echo dict_translate("Password"); >:</label></td>
						<? } >
						<td><input class="config" type="password" name="password" id="password"
						<? if ($is_password_change) { >
							autocomplete="new-password"
						<? } else { >
							autocomplete="current-password"
						<? } >
						maxlength="63" realname="<? echo dict_translate("New Password"); >"/></td>
						<? if ($is_password_change) { >
						<td>&nbsp;<span id="PasswordVerdict" name="PasswordVerdict" style="width: 100px; display: inline-block;"><span>&nbsp;</span></span></td>
						<? } >
					</tr>
					<? if ($is_password_change) { >
					<tr>
						<td><label for="password2"><? echo dict_translate("Verify New Password"); >:</label></td>
						<td><input class="config" type="password" name="password2" id="password2" autocomplete="new-password" maxlength="63" equals="password" realname="<? echo dict_translate("msg_passwd_verify|New password for verification"); >"/></td>
					</tr>
					<? } >
					<? if ($first_login == "true") { >					
					<tr <? if ($radio["ccode_fixed"] != 0) { echo " style=\"display:none;\"";} >>
						<td><label for="country"><? echo dict_translate("Country"); >:</label></td>
						<td>
							<? if ($radio["ccode_fixed"] == 0 && $radio["ccode_locked"] != 1) { >
								<select name="country" id="country"/>
								<option value="0"><? echo dict_translate("Select Your Country");></option>
								<? include("lib/ccode.inc"); >
								</select>
							<? } else { >
								<select name="country_locked" id="country_locked" disabled="disabled"/>
								<? include("lib/ccode.inc"); >
								</select>
							<? } >
						</td>
					</tr>
					<tr>
						<td><label for="ui_language"><? echo dict_translate("Language"); >:</label></td>
						<td>
							<select name="ui_language" id="ui_language">
								<? echo get_language_options($languages, $active_language);>
							</select>
							<input type="hidden" id="lang_changed" name="lang_changed" value="no" />
						</td>
					</tr>
					<? } >
					<tr>
						<td colspan="2">&nbsp;</td>
					</tr>
				</table>
		</td>
	</tr>

	<? if ($first_login == "true") { >
	<tr>
		<td colspan="2" class="license">
			<? include("lib/legal.inc"); echo legal_terms_of_use(); ?>
		</td>
	</tr>
	<? } >

        <tr>
		<td colspan="2" class="submit" align="right">
			<input type="submit" value="<? echo dict_translate("Login"); >" id="loginform_submit"/>
		</td>
	</tr>
</form>
</table>
<footer class="footer">
	<div class="umobileSection">
		<div class="mobileView">
			<img class="umobile" src="/251204.1815/images/unms.svg">&nbsp;
			<div class="umobileApp">
				<div class="umobileAppText"><? echo dict_translate("Have a SmartPhone? Try our new UNMS to install this device"); ></div>
			</div>
			<a href="https://play.google.com/store/apps/details?id=com.ubnt.umobile">
			<img class="badge gplay" src="/251204.1815/images/gplay.svg" alt="GooglePlay"></a>&nbsp;
			<a href="https://itunes.apple.com/us/app/umobile-ubnt/id1183022489?mt=8">
			<img class="badge" src="/251204.1815/images/astore.svg" alt="AppleStore"></a>
		</div>
		<div class="desktopView">
			<a target="_blank" href="https://www.ubnt.com/software/">
				<img class="logos" src="/images/login-logos.svg">
			</a>
		</div>
	</div>
</footer>
</body>
</html>
