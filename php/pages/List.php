<?
unset ($Filter, $Where, $Join);
if ($Post['Filter'])	{
	foreach ($Post['Filter'] as $Data)	{
		if ($Data)	{
			$Data = explode ("@", $Data);
			$Filter[$Data[0]][$Data[1]] = $Data[1];
		}
	}
	if (is_array ($Filter['settingid']))	{
		unset ($NewWhere);
		foreach ($Filter['settingid'] as $ID)
			$NewWhere[] = "settings.settingid='" . mysql_escape_string ($ID) . "'";
		$Join['LEFT JOIN settings ON records.id=settings.reportid'] = "LEFT JOIN settings ON records.id=settings.reportid";
		$Where[] = "(" . join (" OR ", $NewWhere) . ")";
	}
	if (is_array ($Filter['stacktraceid']))	{
		unset ($NewWhere);
		foreach ($Filter['stacktraceid'] as $ID)
			$NewWhere[] = "stacktrace.stacktraceid='" . mysql_escape_string ($ID) . "'";
		$Join['LEFT JOIN stacktrace ON records.id=stacktrace.reportid'] = "LEFT JOIN stacktrace ON records.id=stacktrace.reportid";
		$Where[] = "(" . join (" OR ", $NewWhere) . ")";
	}
	if (is_array ($Filter['crashed']))	{
		unset ($NewWhere);
		$NewWhere[] = "records.crashed='" . mysql_escape_string (key ($Filter['crashed'])) . "'";
		$Where[] = "(" . join (" OR ", $NewWhere) . ")";
	}
}
$MySQL_Result = DB_Query ("SELECT id, date, gamemod FROM records" . ($Join ? " " . join (" ", $Join) : NULL) . ($Where ? " WHERE (" . join (") AND (", $Where) . ")" : NULL));
?>
<TABLE>
<?
while ($Data = mysql_fetch_assoc ($MySQL_Result))	{
	?>
<TR><TD><A HREF="?Details&ID=<? echo $Data['id']; ?>"><? echo $Data['id']; ?></A></TD><TD><? echo $Data['date']; ?></TD><TD><? echo $Data['gamemod']; ?></TD></TR>
<?
}
?>
</TABLE>