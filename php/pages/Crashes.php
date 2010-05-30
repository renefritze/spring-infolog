<?
$Data = ($Post['Version'] == 1 ? GetCrashes2 () : GetCrashes ());
echo "<!---";
//print_r ($Data);
echo "--->";

?>
<TABLE>
<TR><TH COLSPAN="4">Crashes</TH></TR>
<TR><TH CLASS="Sub">Setting</TH><TH CLASS="Sub">Value</TH><TH CLASS="Sub">Crash reports</TH><TH CLASS="Sub">Percentage</TH></TR>
<?
$iSettings = -1;
foreach (array_keys ($Data['Settings']) as $Setting)	{
	++$iSettings;
	$iSettings2 = -1;
	foreach (array_keys ($Data['Settings'][$Setting]) as $Value)	{
		++$iSettings2;
		?>
<TR>
<?		if (++$i[$Setting] == 1)	{
			unset ($SettingIDs);
			foreach ($Data['Settings'][$Setting] as $ValueData)
				$SettingIDs[$ValueData['ID']] = $ValueData['ID'];
			?>
<TD CLASS="LineM<? echo ($iSettings % 2); ?>" ROWSPAN="<? echo count ($Data['Settings'][$Setting]); ?>"><A HREF="?List&Filter[]=crashed@1&Filter[]=settingid@<? echo join ("&Filter[]=settingid@", $SettingIDs); ?>"><? echo $Setting; ?></A></TD>
<?		}	?>
<TD CLASS="LineM<? echo ($iSettings % 2); ?>S<? echo ($iSettings2 % 2); ?>"><A HREF="?List&Filter[]=crashed@1&Filter[]=settingid@<? echo $Data['Settings'][$Setting][$Value]['ID']; ?>"><? echo $Value; ?></A></TD>
<TD CLASS="LineM<? echo ($iSettings % 2); ?>S<? echo ($iSettings2 % 2); ?>"><? echo $Data['Settings'][$Setting][$Value]['Reports']; ?></TD>
<TD CLASS="LineM<? echo ($iSettings % 2); ?>S<? echo ($iSettings2 % 2); ?>"><? echo $Data['Settings'][$Setting][$Value]['Percentage']; ?>%</TD>
</TR>
<?	}
}
?>
</TABLE>