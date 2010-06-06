<?
$MySQL_Result = DB_Query ("SELECT COUNT(records.id) AS Reports, records.crashed, records.contains_demo, recordsdata.data as lobby_client_version FROM records LEFT JOIN recordsdata ON records.lobby_client_versionid=recordsdata.id AND recordsdata.field='lobby_client_version' GROUP BY records.crashed, records.lobby_client_versionid, records.contains_demo");
while ($Data = mysql_fetch_assoc ($MySQL_Result))	{
	$Return['Reports']['Total'] += $Data['Reports'];
	$Return['Reports']['Crashed'][$Data['crashed']] += $Data['Reports'];
	$Return['Reports']['Clients'][($Data['lobby_client_version'] ? $Data['lobby_client_version'] : "(unknown)")] += $Data['Reports'];
	$Return['Reports']['Demo'][$Data['contains_demo']] += $Data['Reports'];
}
ksort ($Return['Reports']['Clients']);
?>
<TABLE>
<TR><TH COLSPAN="2">Statistics</TH></TR>
<TR><TD>No. reports</TD><TD><? echo $Return['Reports']['Total']; ?></TD></TR>
<TR><TD>No. crashed reports</TD><TD><? echo ($Return['Reports']['Crashed'][1] ? $Return['Reports']['Crashed'][1] : "0"), " (", number_format ($Return['Reports']['Crashed'][1] / $Return['Reports']['Total'] * 100, 1); ?>%)</TD></TR>
<TR><TD>No. demo reports</TD><TD><? echo ($Return['Reports']['Demo'][1] ? $Return['Reports']['Demo'][1] : "0"), " (", number_format ($Return['Reports']['Demo'][1] / $Return['Reports']['Total'] * 100, 1); ?>%)</TD></TR>
<TR><TH COLSPAN="2" CLASS="Sub">Clients</TH></TR>
<?
foreach (array_keys ($Return['Reports']['Clients']) as $Client)	{	?>
<TR><TD><? echo ($Client ? $Client : "N/A"); ?></TD><TD><? echo $Return['Reports']['Clients'][$Client]; ?> (<? echo number_format ($Return['Reports']['Clients'][$Client] / $Return['Reports']['Total'] * 100, 1); ?>%)</TD></TR>
<?
}
?>
</TABLE>