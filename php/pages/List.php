<?
function ZydHash ($Value, $Type)	{
	global $ZydHashCache;
	if ($Type == "Table")
		$Return = "T_";
	elseif ($Type == "SubTable")
		$Return = "S_";
	elseif ($Type == "Value")
		$Return = "V_";
	
	if (!$ZydHashCache[md5 ($Value)])
		$ZydHashCache[md5 ($Value)] = count ($ZydHashCache) + 1;
	$Return .= $ZydHashCache[md5 ($Value)];
	return ($Return);
}

unset ($Filter, $Where, $Join, $Select);
if ($Post['Filter'])	{
	foreach ($Post['Filter'] as $Data)	{
		if ($Data)	{
			$Data = explode ("@", $Data);
			if (count ($Data) == 2)
				$Filter[$Data[0]][$Data[1]] = $Data[1];
			elseif (count ($Data) >= 3)	{
				$Temp = $Data;
				unset ($Temp[0], $Temp[1]);
				$Filter[$Data[0]][$Data[1]][join ("@", $Temp)] = join ("@", $Temp);
			}
		}
	}
	if (is_array ($Filter['settingid']))	{
		unset ($NewWhere);
		foreach (array_keys ($Filter['settingid']) as $Setting)	{
			foreach ($Filter['settingid'][$Setting] as $ID)
				$NewWhere[$Setting][] = ZydHash ($Setting, "Table") . ".settingid='" . mysql_escape_string ($ID) . "'";
			$NewWhere[$Setting] = "(" . join (" OR ", $NewWhere[$Setting]) . ")";
			$Join["LEFT JOIN settings AS " . ZydHash ($Setting, "Table") . " ON records.id=" . ZydHash ($Setting, "Table") . ".reportid"] = "LEFT JOIN settings AS " . ZydHash ($Setting, "Table") . " ON records.id=" . ZydHash ($Setting, "Table") . ".reportid LEFT JOIN settingsdata AS " . ZydHash ($Setting, "SubTable") . " ON " . ZydHash ($Setting, "Table") . ".settingid=" . ZydHash ($Setting, "SubTable") . ".id";
			$Select[$Setting] = ZydHash ($Setting, "SubTable") . ".value AS " . ZydHash ($Setting, "Value");
		}
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
			foreach ($Filter['index'][$Setting] as $ID)
				$NewWhere[$Setting][] = "records." . $Setting . "='" . mysql_escape_string ($ID) . "'";
			$NewWhere[$Setting] = "(" . join (" OR ", $NewWhere[$Setting]) . ")";
			$Select[$Setting] = "records." . $Setting . " AS " . ZydHash ($Setting, "Value");
		}
		$Where[] = "(" . join (" AND ", $NewWhere) . ")";
	}
}
//echo "SELECT records.id, date, gamemod" . ($Select ? ", " . join (", ", $Select) : "") . " FROM records" . ($Join ? " " . join (" ", $Join) : NULL) . ($Where ? " WHERE (" . join (") AND (", $Where) . ")" : NULL), "<BR>";
$MySQL_Result = DB_Query ("SELECT records.id, date, gamemod" . ($Select ? ", " . join (", ", $Select) : "") . " FROM records" . ($Join ? " " . join (" ", $Join) : NULL) . ($Where ? " WHERE (" . join (") AND (", $Where) . ")" : NULL));
?>
<TABLE>
<FORM METHOD="POST" NAME="Filter">
<INPUT TYPE="HIDDEN" NAME="Page" VALUE="List">
<TR><TH COLSPAN="100">Filters</TH></TR>
<TR>
<?
if (is_array ($Filter))	{
	foreach (array_keys ($Filter) as $Type)
		echo Filter ($Type, $Filter[$Type]);
}
?></TR>
<TR><TD><INPUT TYPE="SUBMIT" VALUE="Refresh"></TD><TD><SELECT NAME="Filter[]" ONCHANGE="document.Filter.submit ();"><OPTION VALUE="">==[ New filter ]==</OPTION><? echo FilterOptions (); ?></SELECT></TD></TR>
</FORM>
</TABLE><BR>


<TABLE>
<TR><TH COLSPAN="<? echo 3 + count ($Select); ?>">Results (<? echo mysql_num_rows ($MySQL_Result); ?>)</TH></TR>
<TR>
<TH CLASS="Sub">ID</TH>
<TH CLASS="Sub">Date</TH>
<TH CLASS="Sub">Mod</TH>
<?	if (is_array ($Select))	foreach (array_keys ($Select) as $Field)	{	?>
<TH CLASS="Sub"><? echo $Field; ?></TH>
<?	}	?>
</TR>
<?
while ($Data = mysql_fetch_assoc ($MySQL_Result))	{
	?>
<TR><TD><A HREF="?Details&ID=<? echo $Data['id']; ?>"><? echo $Data['id']; ?></A></TD><TD><? echo $Data['date']; ?></TD><TD><? echo $Data['gamemod']; ?></TD><?	if (is_array ($Select))	{	foreach (array_keys ($Select) as $Field)	{	?><TD><? echo $Data[ZydHash ($Field, "Value")]; ?></TD><?	}	}	?></TR>
<?
}
?>
</TABLE>
<?

function FilterOptions ()	{
	$Options['index@crashed@'] = "index - crashed";
	$Options['index@platform@'] = "index - platform";
	$Options['index@spring@'] = "index - spring";
	$Options['index@gamemod@'] = "index - gamemod";
	$Options['index@sdl_version@'] = "index - sdl_version";
	$Options['index@glew_version@'] = "index - glew_version";
	$Options['index@al_vendor@'] = "index - al_vendor";
	$Options['index@al_version@'] = "index - al_version";
	$Options['index@al_renderer@'] = "index - al_renderer";
	$Options['index@al_extensions@'] = "index - al_extensions";
	$Options['index@alc_extensions@'] = "index - alc_extensions";
	$Options['index@al_device@'] = "index - al_device";
	$Options['index@gl_version@'] = "index - gl_version";
	$Options['index@gl_vendor@'] = "index - gl_vendor";
	$Options['index@gl_renderer@'] = "index - gl_renderer";
	$Options['index@lobby_client_version@'] = "index - lobby_client_version";
	$Options['index@contains_demo@'] = "index - contains_demo";
	$MySQL_Result = DB_Query ("SELECT setting FROM settingsdata GROUP BY setting ORDER BY setting");
	while ($Data = mysql_fetch_assoc ($MySQL_Result))
		$Options["settingid@" . $Data['setting'] . "@"] = "setting - " . $Data['setting'];

	foreach (array_keys ($Options) as $Key)
		$Options[$Key] = "<OPTION VALUE=\"" . $Key . "\">" . $Options[$Key] . "</OPTION>";
	return (join ("\n", $Options));
}

function Filter ($Type, $Selected)	{
	$Template = "<TD><TABLE>
<TR><TH>%TYPE%</TH></TR>
<TR><TD><SELECT NAME=\"Filter[]\" SIZE=\"10\" MULTIPLE>%LIST%</SELECT></TD></TR>
</TABLE></TD>";
	if (is_array ($Selected[key ($Selected)]))	{	// Multi-part setting
		foreach (array_keys ($Selected) as $SubType)	{
			unset ($Options);
			if ($Type == "settingid")	{
				$MySQL_Result = DB_Query ("SELECT id, value FROM settingsdata WHERE setting='" . mysql_escape_string ($SubType) . "' ORDER BY value");
				while ($Data = mysql_fetch_assoc ($MySQL_Result))
					$Options[] = array ($Data['id'], $Data['value']);
			}	elseif ($Type == "index")	{
				$MySQL_Result = DB_Query ("SELECT " . mysql_escape_string ($SubType) . " FROM records GROUP BY " . mysql_escape_string ($SubType) . " ORDER BY " . mysql_escape_string ($SubType));
				while ($Data = mysql_fetch_assoc ($MySQL_Result))
					$Options[] = array ($Data[$SubType], $Data[$SubType]);
			}
			foreach (array_keys ($Options) as $Option)
				$Options[$Option] = "<OPTION VALUE=\"" . $Type . "@" . $SubType . "@" . $Options[$Option][0] . "\"" . (is_numeric ($Selected[$SubType][$Options[$Option][0]]) || $Selected[$SubType][$Options[$Option][0]] ? " SELECTED" : "") . ">" . $Options[$Option][1] . "</OPTION>";
			$Return[] = str_replace (array ("%TYPE%", "%LIST%"), array ($Type . " - " . $SubType, join ("\n", $Options)), $Template);
		}
	}	else	{	// Singe setting
		if ($Type == "crashed")	{
			$Option[0] = "No";
			$Option[1] = "Yes";
		}
		foreach (array_keys ($Option) as $Key)
			$Option[$Key] = "<OPTION VALUE=\"" . $Type . "@" . $Key . "\"" . (is_numeric ($Selected[$Key]) ? " SELECTED" : "") . ">" . $Option[$Key] . "</OPTION>";
		$Return[] = str_replace (array ("%TYPE%", "%LIST%"), array ($Type, join ("\n", $Option)), $Template);
	}
	return (join ("\n\n\n", $Return));
}
?>