#!/sbin/cgi
<?
if (($REQUEST_METHOD != "POST" || $X_ACCESS_TOKEN != $token) && strlen($do_update) == 0) {
      Header("Location: /index.cgi");
}
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file);
include("lib/l10n.inc");
include("lib/system.inc");
include("lib/password.inc");
$newfwversion = fw_extract_version($firmware_file);
if (is_downgrade_to_pre_sha512_passwd($newfwversion) && !isOldCryptedPassword($cfg)) {
      $crypted = cfg_get($cfg, "users.1.password");
      $CurrentPassword = getStoredCurrentPassword();
      if ($crypted != crypt($CurrentPassword, $crypted)) {
            Header("Location: /system.cgi");
      }
      $crypted = crypt($CurrentPassword, generateOldSalt());
      setCryptedPassword($cfg, $crypted);
      cfg_save($cfg, $cfg_file);
      exec($cmd_cfgsave);
}

include("lib/link.inc");

$pagetitle=dict_translate("Firmware Update");
$message = dict_translate("msg_firmware_upgrading|Firmware is being updated.<br> This operation takes several minutes to complete - <br>meanwhile <span style=\"color: red\">DO NOT POWEROFF</span> the device!");
$duration=$upgrade_time;
include("lib/ipcheck.inc");
$f=@fopen($fwup_lock, "w");
@fclose($f);
include("lib/reboot.tmpl");
bgexec(4, "/sbin/fwupdate -m");
>
