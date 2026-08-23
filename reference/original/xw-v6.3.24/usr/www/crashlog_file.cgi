#!/sbin/cgi
<?
include("lib/settings.inc");
PassThru("cat $crashlog_file");
>
