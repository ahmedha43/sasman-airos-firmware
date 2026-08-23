<?
include("lib/settings.inc");
@unlink($emerg_file);
@unlink($emerg_supp_file);
@unlink($emerg_crashlog_file);
@unlink($wd_reset_file);
exec("cfgmtd -w -p /etc/ &>/dev/null&");
>
