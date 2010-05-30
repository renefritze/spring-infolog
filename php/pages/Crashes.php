<?
$Data = ($Post['Version'] == 1 ? GetCrashes2 () : GetCrashes ());
$FilterType = ($Post['Version'] == 1 ? "stacktraceid" : "settingid");
echo "<!---";
//print_r ($Data);
echo "--->";

?>
<TABLE>
<TR><TH COLSPAN="4">Crashes</TH></TR>
<TR><TH CLASS="Sub">Setting</TH><TH CLASS="Sub">Value</TH><TH CLASS="Sub">Crash reports</TH><TH CLASS="Sub">Percentage</TH></TR>
<?
$iSettings = -1;
foreach (array_keys ($Data['Data']) as $Setting)	{
	++$iSettings;
	$iSettings2 = -1;
	foreach (array_keys ($Data['Data'][$Setting]) as $Value)	{
		++$iSettings2;
		?>
<TR>
<?		if (++$i[$Setting] == 1)	{
			unset ($SettingIDs);
			foreach ($Data['Data'][$Setting] as $ValueData)
				$SettingIDs[$ValueData['ID']] = $ValueData['ID'];
			?>
<TD CLASS="LineM<? echo ($iSettings % 2); ?>" ROWSPAN="<? echo count ($Data['Data'][$Setting]); ?>"><A HREF="?List&Filter[]=crashed@1&Filter[]=<? echo $FilterType; ?>@<? echo join ("&Filter[]=" . $FilterType . "@", $SettingIDs); ?>"><? echo $Setting; ?></A></TD>
<?		}	?>
<TD CLASS="LineM<? echo ($iSettings % 2); ?>S<? echo ($iSettings2 % 2); ?>"><A HREF="?List&Filter[]=crashed@1&Filter[]=<? echo $FilterType; ?>@<? echo $Data['Data'][$Setting][$Value]['ID']; ?>"><? echo $Value; ?></A></TD>
<TD CLASS="LineM<? echo ($iSettings % 2); ?>S<? echo ($iSettings2 % 2); ?>"><? echo $Data['Data'][$Setting][$Value]['Reports']; ?></TD>
<TD CLASS="LineM<? echo ($iSettings % 2); ?>S<? echo ($iSettings2 % 2); ?>"><? echo $Data['Data'][$Setting][$Value]['Percentage']; ?>%</TD>
</TR>
<?	}
}
?>
</TABLE>