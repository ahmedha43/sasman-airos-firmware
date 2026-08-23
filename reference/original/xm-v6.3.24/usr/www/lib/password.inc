<?
Function passChangeErr $err
(
	switch($err) {
		case -1;
			$msg = dict_translate("msg_passwords_dont_match|New passwords do not match!");
			break;
		case -2;
			$msg = dict_translate("msg_password_empty|New password cannot be empty!");
			break;
		case -3;
			$msg = dict_translate("msg_curr_passwd_wrong|Current password is wrong.");
			break;
		case -4;
			$msg = dict_translate("msg_all_passw_empty|Please enter current and new passwords.");
			break;
		default;
			$msg = dict_translate("Undefined error.");
			break;
	}

	return $msg;
);

Function validatePassword $OldPassword, $NewPassword, $NewPassword2
(
	global $cfg;

	if ((strlen($OldPassword) != 0) || (strlen($NewPassword) != 0) ||
		(strlen($NewPassword2) != 0))
	{
		if ($NewPassword != $NewPassword2)
		{
			return -1;
		}
		elseif ((strlen($NewPassword) == 0) || (strlen($NewPassword2) == 0)) {
			return -2;
		}
		else
		{
			$passwd = cfg_get($cfg, "users.1.password");
			if ($passwd == "")
			{
				$passwd = "\$1\$CCtKtXoV\$t3YJh1/OXd0qiuIDLsxKT0";
			}

			$crypted = crypt($OldPassword, $passwd);
			if ($passwd != $crypted)
			{
				return -3;
			}
			else
			{
				return 0;
			}
		}
	}
	return -4;
);

Function generateOldSalt
(
	$seedchars = "vWXnopjk./0123YZabcdefghiIJKLMNOPQRSTUlm456789ABCDEFGHqrstuVwxyz";
	$salt = "\$1\$";
	srand(time() * getmypid());
	$i = 0;
	while ($i < 8) {
		$salt = $salt + substr($seedchars, rand() % 32, 1);
		$i++;
	}
	return $salt;
);

Function setCryptedPassword $cfg, $crypted
(
	global $cfg_file;

	cfg_set($cfg, "users.1.password", $crypted);
	cfg_set($cfg, "users.1.status", "enabled");
	cfg_save($cfg, $cfg_file);
);


Function changePassword $NewPassword
(
	global $cfg;

	$crypted_new = crypt($NewPassword);

	cfg_set($cfg, "users.1.password", $crypted_new);
	cfg_set($cfg, "users.1.status", "enabled");

	check_default_passwd($cfg);	

	return $crypted_new;

);

Function isOldCryptedPassword $cfg
(
	$passwd = cfg_get($cfg, "users.1.password");
	if (substr($passwd, 0, 5) != "\$6\$") {
		return 1;
	}
	return 0;
);

$stored_current_password_file = "/tmp/.web_current_password";

Function getStoredCurrentPassword
(
	global $stored_current_password_file;
	$fp = @fopen($stored_current_password_file, "r");
	if ($fp > -1) {
		$line=fgets($fp,255);
		fclose($fp);
		return $line;
	}
	return "";
);

Function storeCurrentPassword $CurrentPassword
(
	global $stored_current_password_file;
	$fp = @fopen($stored_current_password_file, "w");
	if ($fp > -1) {
		@fputs($fp, $CurrentPassword);
		fclose($fp);
	}
);

>
