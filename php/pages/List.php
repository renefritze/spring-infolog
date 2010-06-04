<?
//print_r ($Post);
if (!$Post['Selected'])
	$Post['Selected'] = array ("index@crashed@");

$HitsPerPage = 100;
function ZydHash ($Value, $Type, $DispValue = NULL)	{
	global $ZydHashCache;
	if ($Type == "Table")
		$Return = "T_";
	elseif ($Type == "SubTable")
		$Return = "S_";
	elseif ($Type == "Value")
		$Return = "V_";
	elseif ($Type == "Source")
		return ($ZydHashCache[1][substr ($Value, 2)]);
	
	if (!$ZydHashCache[0][md5 ($Value)])	{
		$ZydHashCache[0][md5 ($Value)] = count ($ZydHashCache[0]) + 1;
		$ZydHashCache[1][count ($ZydHashCache[0])] = ($DispValue ? $DispValue : $Value);
	}
	$Return .= $ZydHashCache[0][md5 ($Value)];
	return ($Return);
}

unset ($Filter, $Where, $Join, $Select, $PageURL);
if ($Post['Filter'])	{
	foreach ($Post['Filter'] as $Data)	{
		if ($Data)	{
			$Data = explode ("@", $Data);
			$Temp = $Data;
			unset ($Temp[0], $Temp[1]);
			$Filter[$Data[0]][$Data[1]][join ("@", $Temp)] = join ("@", $Temp);
		}
	}
//	print_r ($Filter);
	if (is_array ($Filter['settingid']))	{
		unset ($NewWhere);
		foreach (array_keys ($Filter['settingid']) as $Setting)	{
			if (is_array ($Filter['settingid'][$Setting]))	{
				foreach ($Filter['settingid'][$Setting] as $ID)
					if ($ID || is_numeric ($ID))
						$NewWhere[$Setting][] = ZydHash ($Setting, "Table", GetSettingsList ($Setting)) . ".valueid='" . mysql_escape_string ($ID) . "'";
				if (is_array ($NewWhere[$Setting]))	{
					$NewWhere[$Setting] = "(" . join (" OR ", $NewWhere[$Setting]) . ")";
					$Join[ZydHash ($Setting, "Table")] = "LEFT JOIN settings AS " . ZydHash ($Setting, "Table") . " ON records.id=" . ZydHash ($Setting, "Table") . ".reportid AND " . ZydHash ($Setting, "Table") . ".settingid='" . mysql_escape_string ($Setting) . "'";
					$Join[ZydHash ($Setting, "SubTable")] = "LEFT JOIN settingsdata AS " . ZydHash ($Setting, "SubTable") . " ON " . ZydHash ($Setting, "Table") . ".valueid=" . ZydHash ($Setting, "SubTable") . ".id";
				}
			}
		}
		if (is_array ($NewWhere))
			$Where[] = "(" . join (" AND ", $NewWhere) . ")";
	}
	if (is_array ($Filter['stacktraceid']))	{
		unset ($NewWhere);
		foreach ($Filter['stacktraceid'] as $ID)
			$NewWhere[] = "stacktrace.stacktraceid='" . mysql_escape_string ($ID) . "'";
		$Join['LEFT JOIN stacktrace ON records.id=stacktrace.reportid'] = "LEFT JOIN stacktrace ON records.id=stacktrace.reportid";
		$Where[] = "(" . join (" OR ", $NewWhere) . ")";
	}
	if (is_array ($Filter['index']))	{
		unset ($NewWhere);
		foreach (array_keys ($Filter['index']) as $Setting)	{
			if (is_array ($Filter['index'][$Setting]))	{
				foreach ($Filter['index'][$Setting] as $ID)
					if ($ID || is_numeric ($ID))
						$NewWhere[$Setting][] = "records." . mysql_escape_string ($Setting) . "='" . mysql_escape_string ($ID) . "'";
				if (is_array ($NewWhere[$Setting]))
					$NewWhere[$Setting] = "(" . join (" OR ", $NewWhere[$Setting]) . ")";
			}
		}
		if (is_array ($NewWhere))
			$Where[] = "(" . join (" AND ", $NewWhere) . ")";
	}
	if (is_array ($Filter['indexid']))	{
		unset ($NewWhere);
		foreach (array_keys ($Filter['indexid']) as $Setting)	{
			if (is_array ($Filter['indexid'][$Setting]))	{
				foreach ($Filter['indexid'][$Setting] as $ID)
					if ($ID || is_numeric ($ID))
						$NewWhere[$Setting][] = "records." . mysql_escape_string ($Setting) . "id='" . mysql_escape_string ($ID) . "'";
				if (is_array ($NewWhere[$Setting]))	{
					$NewWhere[$Setting] = "(" . join (" OR ", $NewWhere[$Setting]) . ")";
					$Join[ZydHash ($Setting, "Table")] = "LEFT JOIN recordsdata AS " . ZydHash ($Setting, "Table") . " ON records." . $Setting . "id=" . ZydHash ($Setting, "Table") . ".id AND " . ZydHash ($Setting, "Table") . ".field='" . mysql_escape_string ($Setting) . "'";
				}
			}
		}
		if (is_array ($NewWhere))
			$Where[] = "(" . join (" AND ", $NewWhere) . ")";
	}
	if (is_array ($Filter))
		foreach (array_keys ($Filter) as $Key)
			foreach (array_keys ($Filter[$Key]) as $Key2)
				foreach ($Filter[$Key][$Key2] as $ID)
					$PageURL .= "&Filter[]=" . $Key . "@" . $Key2 . "@" . $ID;
//	print_r ($Filter);
}

unset ($Select);
foreach ($Post['Selected'] as $Selected)	{
	$Selected = explode ("@", $Selected);
	if ($Selected[0] == "settingid")	{
		$Join[ZydHash ($Selected[1], "Table", GetSettingsList ($Selected[1]))] = "LEFT JOIN settings AS " . ZydHash ($Selected[1], "Table") . " ON records.id=" . ZydHash ($Selected[1], "Table") . ".reportid AND " . ZydHash ($Selected[1], "Table") . ".settingid='" . mysql_escape_string ($Selected[1]) . "'";
		$Join[ZydHash ($Selected[1], "SubTable")] = "LEFT JOIN settingsdata AS " . ZydHash ($Selected[1], "SubTable") . " ON " . ZydHash ($Selected[1], "Table") . ".valueid=" . ZydHash ($Selected[1], "SubTable") . ".id";
		$Select[ZydHash ($Selected[1], "Value")] = ZydHash ($Selected[1], "SubTable") . ".data AS " . ZydHash ($Selected[1], "Value");
	}	elseif ($Selected[0] == "index")	{
		$Select[ZydHash ($Selected[1], "Value")] = "records." . mysql_escape_string ($Selected[1]) . " AS " . ZydHash ($Selected[1], "Value");
	}	elseif ($Selected[0] == "indexid")	{
		$Join[ZydHash ($Selected[1], "Table")] = "LEFT JOIN recordsdata AS " . ZydHash ($Selected[1], "Table") . " ON records." . mysql_escape_string ($Selected[1]) . "id=" . ZydHash ($Selected[1], "Table") . ".id";
		$Select[ZydHash ($Selected[1], "Value")] = ZydHash ($Selected[1], "Table") . ".data AS " . ZydHash ($Selected[1], "Value");
	}
	$PageURL .= "&Selected[]=" . join ("@", $Selected);
}

//echo "\n\nSELECT records.id, date" . ($Select ? ", " . join (", ", $Select) : "") . " FROM records" . ($Join ? " " . join (" ", $Join) : NULL) . ($Where ? " WHERE (" . join (") AND (", $Where) . ")" : NULL), "\n\n\n<BR>";
$MySQL_Result = DB_Query ("SELECT COUNT(records.id) AS Rows FROM records" . ($Join ? " " . join (" ", $Join) : NULL) . ($Where ? " WHERE (" . join (") AND (", $Where) . ")" : NULL));
$Rows = join ("", mysql_fetch_assoc ($MySQL_Result));
$MySQL_Result = DB_Query ("SELECT records.id, date" . ($Select ? ", " . join (", ", $Select) : "") . " FROM records" . ($Join ? " " . join (" ", $Join) : NULL) . ($Where ? " WHERE (" . join (") AND (", $Where) . ")" : NULL) . " LIMIT " . mysql_escape_string ($Post['Limit'] ? $Post['Limit'] : 0) . ", " . $HitsPerPage);
?>
<TABLE>
<FORM METHOD="POST" NAME="Filter">
<INPUT TYPE="HIDDEN" NAME="Page" VALUE="List">
<INPUT TYPE="HIDDEN" NAME="Limit" VALUE="0">
<TR><TH>Filters</TH><TH>Selection</TH></TR>
<TR><TD><TABLE>
<TR>
<?
if (is_array ($Filter))	{
	foreach (array_keys ($Filter) as $Type)
		echo Filter ($Type, $Filter[$Type]);
}
?>
</TR>
</TABLE></TD>
<TD>
<SELECT NAME="Selected[]" SIZE="10" MULTIPLE><? echo FilterOptions ($Post['Selected']); ?></SELECT>
</TD></TR>
<TR><TD><INPUT TYPE="SUBMIT" VALUE="Refresh"></TD><TD><SELECT NAME="Filter[]" ONCHANGE="document.Filter.submit ();"><OPTION VALUE="">==[ New filter ]==</OPTION><? echo FilterOptions (); ?></SELECT></TD></TR>
</FORM>
</TABLE><BR>


<TABLE>
<TR><TD COLSPAN="<? echo 2 + count ($Select); ?>">Pages <?
for ($iPage = 1; $iPage <= ceil ($Rows / $HitsPerPage); $iPage++)	{
?>
<A HREF="?List<? echo $PageURL; ?>&Limit=<? echo ($iPage - 1) * $HitsPerPage; ?>"><? echo $iPage; ?></A>
<?
}
?></TD></TR>
<TR><TH COLSPAN="<? echo 2 + count ($Select); ?>">Results (<? echo ($Post['Limit'] + 1) . "-", min ($Post['Limit'] + $HitsPerPage, $Rows), " of " . $Rows; ?>)</TH></TR>
<TR>
<TH CLASS="Sub">ID</TH>
<TH CLASS="Sub">Date</TH>
<?	if (is_array ($Select))	foreach (array_keys ($Select) as $Field)	{	?>
<TH CLASS="Sub"><? echo ZydHash ($Field, "Source"); ?></TH>
<?	}	?>
</TR>
<?
while ($Data = mysql_fetch_assoc ($MySQL_Result))	{
	?>
<TR><TD><A HREF="?Details&ID=<? echo $Data['id']; ?>"><? echo $Data['id']; ?></A></TD><TD><? echo $Data['date']; ?></TD><?	if (is_array ($Select))	{	foreach (array_keys ($Select) as $Field)	{	?><TD><? echo $Data[$Field]; ?></TD><?	}	}	?></TR>
<?
}
?>
</TABLE>
<?

global $ZydHashCache;
echo "\n<!--\n";
print_r ($ZydHashCache);
echo "-->";

function FilterOptions ($Selected = NULL)	{
	$Options['index@crashed'] = "index - crashed";
	$Options['indexid@platform'] = "index - platform";
	$Options['indexid@spring'] = "index - spring";
	$Options['indexid@gamemod'] = "index - gamemod";
	$Options['indexid@sdl_version'] = "index - sdl_version";
	$Options['indexid@glew_version'] = "index - glew_version";
	$Options['indexid@al_vendor'] = "index - al_vendor";
	$Options['indexid@al_version'] = "index - al_version";
	$Options['indexid@al_renderer'] = "index - al_renderer";
	$Options['indexid@al_extensions'] = "index - al_extensions";
	$Options['indexid@alc_extensions'] = "index - alc_extensions";
	$Options['indexid@al_device'] = "index - al_device";
	$Options['indexid@gl_version'] = "index - gl_version";
	$Options['indexid@gl_vendor'] = "index - gl_vendor";
	$Options['indexid@gl_renderer'] = "index - gl_renderer";
	$Options['indexid@lobby_client_version'] = "index - lobby_client_version";
	$Options['index@contains_demo'] = "index - contains_demo";
	$Data = GetSettingsList ();
	foreach (array_keys ($Data) as $ID)
		$Options["settingid@" . $ID] = "setting - " . $Data[$ID];

	foreach (array_keys ($Options) as $Key)
		$Options[$Key] = "<OPTION VALUE=\"" . $Key . "\"" . (is_array ($Selected) && is_numeric (array_search ($Key, $Selected)) ? " SELECTED" : "") . ">" . $Options[$Key] . "</OPTION>";
	return (join ("\n", $Options));
}

function Filter ($Type, $Selected)	{
//<TR><TD>RegEx<INPUT NAME=\"Filter[]\" VALUE=\"\"></TD></TR>
	$Template = "<TD><TABLE>
<TR><TH>%TYPE%</TH></TR>
<TR><TD><SELECT NAME=\"Filter[]\" SIZE=\"10\" MULTIPLE>%LIST%</SELECT></TD></TR>
</TABLE></TD>";
//	if (is_array ($Selected[key ($Selected)]))	{	// Multi-part setting
		foreach (array_keys ($Selected) as $SubType)	{
//			echo "\n\n\n[[[", $SubType, "]]]\n\n\n";
			unset ($Options);
			if ($Type == "settingid")	{
				$MySQL_Result = DB_Query ("SELECT settings.valueid, settingsdata.data FROM settings LEFT JOIN settingsdata ON settings.valueid=settingsdata.id WHERE settings.settingid='" . mysql_escape_string ($SubType) . "' GROUP BY settings.valueid ORDER BY settingsdata.data");
				while ($Data = mysql_fetch_assoc ($MySQL_Result))
					$Options[] = array ($Data['valueid'], $Data['data']);
				$DisplayType = GetSettingsList ($SubType);
			}	elseif ($Type == "index")	{
				$MySQL_Result = DB_Query ("SELECT " . mysql_escape_string ($SubType) . " FROM records GROUP BY " . mysql_escape_string ($SubType) . " ORDER BY " . mysql_escape_string ($SubType));
				while ($Data = mysql_fetch_assoc ($MySQL_Result))
					$Options[] = array ($Data[$SubType], $Data[$SubType]);
			}	elseif ($Type == "indexid")	{
				$MySQL_Result = DB_Query ("SELECT id, data FROM recordsdata WHERE field='" . mysql_escape_string ($SubType) . "' ORDER BY data");
				while ($Data = mysql_fetch_assoc ($MySQL_Result))
					$Options[] = array ($Data['id'], $Data['data']);
			}
			foreach (array_keys ($Options) as $Option)
				$Options[$Option] = "<OPTION VALUE=\"" . $Type . "@" . $SubType . "@" . $Options[$Option][0] . "\"" . (is_numeric ($Selected[$SubType][$Options[$Option][0]]) || $Selected[$SubType][$Options[$Option][0]] ? " SELECTED" : "") . ">" . $Options[$Option][1] . "</OPTION>";
			$Return[] = str_replace (array ("%TYPE%", "%LIST%"), array ($Type . " - " . ($DisplayType ? $DisplayType : $SubType), join ("\n", $Options)), $Template);
		}
//	}	else	{	// Singe setting
//		if ($Type == "crashed")	{
//			$Option[0] = "No";
//			$Option[1] = "Yes";
//		}
//		foreach (array_keys ($Option) as $Key)
//			$Option[$Key] = "<OPTION VALUE=\"" . $Type . "@" . $Key . "\"" . (is_numeric ($Selected[$Key]) ? " SELECTED" : "") . ">" . $Option[$Key] . "</OPTION>";
//		$Return[] = str_replace (array ("%TYPE%", "%LIST%"), array ($Type, join ("\n", $Option)), $Template);
//	}
	return (join ("\n\n\n", $Return));
}
?>