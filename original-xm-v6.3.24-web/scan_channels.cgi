#!/sbin/cgi
<?
	include("lib/settings.inc");
	$cfg = @cfg_load($cfg_file);
	include("lib/l10n.inc");
	include("lib/link.inc");
	include("lib/misc.inc");

	init_board_inc($wlan_iface);
	$wmode_type = get_wmode_type(cfg_get_wmode($cfg, $wlan_iface));
        if (strlen($chanbw) == 0 || !ereg("^[[:digit:]]+$", $chanbw)) {
		$chanbw = cfg_get_def($cfg, "radio.1.chanbw", "0");
        }
>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title><? echo get_title($cfg, dict_translate("Frequency List")); ></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Pragma" content="no-cache">
<link rel="shortcut icon" href="/251204.1902/favicon.ico" >
<link href="/251204.1902/style.css" rel="stylesheet" type="text/css">
<script type="text/javascript" language="javascript1.2" src="/251204.1902/slink.js"></script>
<script type="text/javascript" language="javascript" src="/251204.1902/js/jquery.js"></script>
<script type="text/javascript" language="javascript">
//<!--
<?
if ($radio1_ieee_mode_a == 1 && $radio1_ieee_mode_bg == 0) {
	$ieee_mode = "a";
} elseif ($radio1_ieee_mode_bg == 1 && $radio1_ieee_mode_a == 0) {
	$ieee_mode = "g";
}

generate_js_regdomain($country, "full_regdomain", $radio["devdomain"], $radio["regdomain_flags"], $chanbw);
>

var ieee_mode = '<?echo validate_str("[A-Za-z0-9]+", $ieee_mode)>'.toLowerCase();
var chanbw = "<?echo intval($chanbw)>";
var airmax="<?echo intval($airmax)>";
var obey = '<? echo validate_str("[a-z]+", $obey); >' == "true";
var is_ap = "<? echo intval($wmode_type); >" == "2";
var rg_data = parse_full_regdomain(full_regdomain);
var regdomain = rg_data.regdomain;
var country = "<?echo intval($country)>";
var isIndoorHidden = '<?echo validate_str("[a-z]+", $isIndoorHidden)>';
var hide_dfs = '<?echo validate_str("[a-z]+", $hide_dfs)>';
var channels = get_scan_channels(regdomain, ieee_mode, chanbw, airmax, obey, is_ap);
var selected_channels = '<?echo validate_str("[0-9, ]+", $scan_channels) >'.split(",");

function selectChannels() {
	var chans = $('.frq:checked').map(function(i, n) { return $(n).val(); }).get();
	window.opener.setScanChannels("<?echo htmlspecialchars($elemId)>", chans.join(","));
	window.opener.updateSliderOnChanlist();
	window.close();
	return false;
}

function addRow(tbody, cols) {
	tbody.push('<tr>');
	tbody.push(cols.join(''));
	tbody.push('</tr>');
}

function fillTable(channels, selected_channels) {
	var col_count = 5;
	var tbody = [], cols = [];
	$('#channels > tbody').empty();

    if (country == 511) {
        var $select_container =  $('<div />');
        var $highlight_country_select = $('<select id="highlight_country_select" />');
        $select_container.append($highlight_country_select);

        <?
		global $cmd_regdomain;
		$def_cntry_output = "<option value=\"840\">United States</option>";

		$modestring = " -j -L";
		$modestring += " -D " + $radio["devdomain"];
		if ($radio["ccode_locked"] != 0) {
			$modestring += " -u";
		}
		if ($radio["ccode_fixed"] == 1 || $radio["ccode_locked"] != 0) {
			$modestring += " "+$radio["ccode"];
		} else {
			$modestring += " "+$country;
		}

        UnSet($lines); UnSet($res);
        $cmd = $cmd_regdomain + $modestring;
        Exec($cmd, $lines, $res);
        $result = "";
        if ($res == 0) {
            $i = 0;
            while ($i < count($lines)) {
                $result += $lines[$i];
                $i++;
            }
        }
        >

        $highlight_country_select.append('<? echo $result; >');

	    cols.push('<td><input type="checkbox" id="allfreq" /><? echo dict_translate("Select All");></td>');
	    cols.push('<td colspan="' + (col_count - 1)
	        + '" style="padding-bottom: 10px; padding-top: 10px;"><? echo dict_translate("Highlight by country");>&nbsp;'
	        + $select_container.html()
	        + '</td>');
	}
	else {
	    cols.push('<td colspan="' + col_count + '"><input type="checkbox" id="allfreq" /><? echo dict_translate("Select All");></td>');
	}

	addRow(tbody, cols); cols = [];

	var showHideIndoor = false;
		if (requiresCE(country) || country == 756) {
			showHideIndoor = true;
	}

	var i, c = 0, count = 0;
	for (i in channels) {
		var chan = channels[i];
		var label_freq = chan + ' MHz';
		if (country == 902) {
			if (chan == "905") {
				label_freq = "905 (904.75 MHz)";
			} else if (chan == "918") {
				label_freq = "918 (918.25 MHz)";
			} else if (chan == "925") {
				label_freq = "924 (924.75 MHz)";
			} else if (chan == "922") {
				label_freq = "921 (921.75 MHz)";
			}
		}
		count++;

		var freqDfs = isFreqDfs(regdomain, ieee_mode, chanbw, chan);
		var freqIndoor = isFreqIndoor(chan);
		if (!freqDfs) {
			if (freqIndoor && showHideIndoor) {
				label_freq = label_freq + ' (Indoor)';
			}
		} else {
			label_freq = label_freq + ' (DFS';
			if (freqIndoor && showHideIndoor) {
				label_freq = label_freq + ' + Indoor)';
			} else {
				label_freq = label_freq + ')';
			}
		}

		if (isIndoorHidden != "true" || !freqIndoor) {
			cols.push('<td class="frq_col">');
			cols.push('<input type="checkbox" class="frq" id="chan_'+chan+'" value="' + chan + '"');
			if (hide_dfs == "true" && freqDfs) {
				cols.push(' disabled="disabled"');
			} else {
				if ($.inArray(chan, selected_channels) > -1)
					cols.push(' checked');
			}
			cols.push('/><label for="chan_'+ chan +'" class="frq_label">' + label_freq + '<span class="dfs_label dfs_hidden">&nbsp;*</span></label>');
			cols.push('</td>');

			if ((++c % col_count) == 0) {
				addRow(tbody, cols); cols = [];
			}
		}
	}

	if (cols.length > 0) {
		for (i = cols.length; i < col_count; ++i)
			cols.push('<td>&nbsp;</td>');
		addRow(tbody, cols);
	}

	$('#channels > tbody').append(tbody.join(''));

	$('#allfreq').change(function() {
		$('.frq').not(":disabled").attr('checked', $(this).is(':checked'));
	});

	$('.frq').change(function() {
		var len = $('.frq:checked').length;
		$('#allfreq').attr('checked', len == count);
	});
	$('.frq').change();

    if (country == 511) {
        $('#highlight_country_select').change(function() {
            var country_code = $("#highlight_country_select option:selected").val();
            var url = "regdomain_by_country.cgi";
            url += "?country="+country_code;
            url += "&chanbw="+chanbw;

            var successHandler = function(response, textStatus) {
                var rg_data = parse_full_regdomain(response);
                var regdomain = rg_data.regdomain;

                var country_channels = [];
                var country_dfs_channels = [];
                for (curr_ieee in regdomain) {
                    for (curr_chanbw in regdomain[curr_ieee]) {
                        for (curr_channel in regdomain[curr_ieee][curr_chanbw]) {
                            var data = regdomain[curr_ieee][curr_chanbw][curr_channel];
                            country_channels.push(curr_channel);
                            if (rg_data.has_dfs) {
                                var dfs_chan = data[5];
                                if (dfs_chan) {
                                    country_dfs_channels.push(curr_channel);
                                }
                            }
                        }
                    }
                }

                $('#channels td.frq_col').each(function (i, col) {
                    var $col = $(col);
                    var $checkbox = $col.find('.frq');
                    var $label = $col.find('.frq_label');
                    if (country_channels.indexOf($checkbox.val()) != -1) {
                        $label.toggleClass('highlight', true);
                    }
                    else {
                        $label.toggleClass('highlight', false);
                    }

                    var $dfs_label = $col.find('.dfs_label');
                    if (rg_data.has_dfs) {
                        if (country_dfs_channels.indexOf($checkbox.val()) != -1) {
                            $dfs_label.toggleClass('dfs_hidden', false);
                        }
                        else {
                            $dfs_label.toggleClass('dfs_hidden', true);
                        }
                    }
                    else {
                        $dfs_label.toggleClass('dfs_hidden', true);
                    }
                });

                if (rg_data.has_dfs) {
                    $('#dfs_marking_info').show();
                }
                else {
                    $('#dfs_marking_info').hide();
                }
            };

            if (country_code == 511) {
                $('#channels td.frq_col').each(function (i, col) {
                    var $col = $(col);
                    var $label = $col.find('.frq_label');
                    $label.toggleClass('highlight', false);
                    var $dfs_label = $col.find('.dfs_label');
                    $dfs_label.toggleClass('dfs_hidden', true);
                });
                $('#dfs_marking_info').hide();
            }
            else {
                $.ajax({
                    cache: false,
                    url: url,
                    success: successHandler,
                    error: function() {
                    },
                    complete: function(xhr, status) {
                    }
                });
            }
        });
    }
}

$(document).ready(function() {
	fillTable(channels, selected_channels);
});

//-->
</script>
</head>

<body class="popup">
<br>
<form enctype="multipart/form-data" action="#" method="POST" onSubmit="return selectChannels();">
	<input type="hidden" name="token" value="<? echo $X_ACCESS_TOKEN; ?>" />
	<table id="channels" class="popup" align="center" cellspacing="0" cellpadding="0">
		<thead>
			<tr><th colspan="5"><? echo dict_translate("Frequency List, MHz"); ><th><tr>
		</thead>
		<tbody>
		</tbody>
	</table>
	<br/>
	<div id="dfs_marking_info">* indicates DFS channels for selected country</div>
	<br />
	<table align="center" cellspacing="0" cellpadding="0">
		<tr>
			<td><input class="fixwidth" type="submit" value="<? echo dict_translate("OK");>"></td>
			<td><input class="fixwidth" type="button" value="<? echo dict_translate("Close"); >"
				onClick="window.close()"></td>
		</tr>
	</table>
</form>
</body>
</html>
