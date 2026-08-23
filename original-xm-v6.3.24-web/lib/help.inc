<?
Function localize_help $help_page (
      	global $active_language;
       	$h = "/251204.1902/help/"+$active_language+"/"+$help_page;
       	if (fileSize("."+$h) <= 0) {
       		$h = "/251204.1902/help/en_US/"+$help_page;
       	}
       	return $h;
);
>