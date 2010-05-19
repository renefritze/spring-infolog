<?
function DoxTime ()	{
	$Time = microtime ();
	return (strstr ($Time, " ") + str_replace (strstr ($Time, " "), " ", $Time));
}


function DB_Query ($Query)	{
	global $Config;
	global $MySQL_Connection;
	if (!$MySQL_Connection)	{
		$MySQL_Connection = mysql_connect ($Config['MySQL']['host'], $Config['MySQL']['user'], $Config['MySQL']['passwd']);
		mysql_select_db ($Config['MySQL']['db'], $MySQL_Connection);
	}
	$Return = mysql_query ($Query, $MySQL_Connection);
	return ($Return);
}


function GetReport ($ID)	{
	$MySQL_Result = DB_Query ("SELECT * FROM records WHERE id='" . mysql_escape_string ($ID) . "'");
	$Return = mysql_fetch_assoc ($MySQL_Result);
	return ($Return);
}


function GetCrashes ()	{
	$MySQL_Result = DB_Query ("SELECT COUNT(id) FROM records WHERE crashed='1'");
	$Crashed = join ("", mysql_fetch_assoc ($MySQL_Result));
	$MySQL_Result = DB_Query ("SELECT settings.setting, settings.value, COUNT(records.id) AS Crashes FROM records LEFT JOIN settings ON records.id=settings.id WHERE crashed='1' GROUP BY settings.setting, settings.value");
	while ($Data = mysql_fetch_assoc ($MySQL_Result))
		$Return['Settings'][$Data['setting']][$Data['value']] = array ("Reports" => $Data['Crashes'], "Percentage" => number_format ($Data['Crashes'] / $Crashed * 100, 1, ".", ""));
	ksort ($Return['Settings']);
	foreach (array_keys ($Return['Settings']) as $Setting)
		ksort ($Return['Settings'][$Setting]);
	return ($Return);
//	print_r ($Return);
}
?>