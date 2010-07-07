<?
$Data = GetReport ($Post['ID']);
$Stacktrace = GetStacktrace ($Post['ID']);
$Extensions = GetExtensionMapping ();
?>
<TABLE>
<TR><TH COLSPAN="2">Crash report details</TH></TR>
<TR><TD>File</TD><TD><A HREF="?DownloadFile&NoHTML=1&File=<? echo $Data['filename']; ?>">Download</A></TD></TR>
<TR><TD>Buildserv command:</TD><TD>!translate file=http://<? echo $Global['BaseURL'] . (substr ($Global['BaseURL'], -1) != "/" ? "/" : ""); ?>?Infolog&NoHTML=1&ID=<? echo $Post['ID']; ?></TD></TR>
<?
if (is_array ($Stacktrace))	{	?>
<TR><TH CLASS="Sub" COLSPAN="2">Stacktrace</TH></TR>
<TR><TD CLASS="NoPad" COLSPAN="2"><TABLE CELLSPACING="0" CELLPADDING="0" WIDTH="100%">
<TR>
<TH CLASS="SubSub">Order</TH>
<TH CLASS="SubSub">File</TH>
<TH CLASS="SubSub">Function</TH>
<TH CLASS="SubSub">File</TH>
</TR>
<?	foreach ($Stacktrace as $Row)	{
		?>
<TR>
<TD><? echo $Row['orderid']; ?></TD>
<TD><? echo $Row['file']; ?> [<? echo $Row['address']; ?>]</TD>
<TD><? echo $Row['functionname'] . ($Row['functionaddress'] ? " (" . $Row['functionaddress'] . ")" : "&nbsp;"); ?></TD>
<TD><? echo $Row['cppfile'] . ($Row['cppline'] ? " (" . $Row['cppline'] . ")" : "&nbsp;"); ?></TD>
</TR>
<?	}	?>
</TABLE></TD></TR>
<?
}
?>
<TR><TH CLASS="Sub" COLSPAN="2">Data</TH></TR>
<?
foreach (array ("player", "spring", "platform", "map", "gamemod", "gameid", "sdl_version", "glew_version", "al_vendor", "al_version", "al_renderer", "al_extensions", "alc_extensions", "al_device", "al_available_devices", "gl_version", "gl_vendor", "gl_renderer", "lobby_client_version", "first_crash_line") as $Field)	{	?>
<TR><TD><? echo $Field; ?></TD><TD><? echo $Data[$Field]; ?></TD></TR>
<?
}
?>

<TR><TH CLASS="Sub" COLSPAN="2">Extensions</TH></TR>
<?
if ($Data['extensions'])
	foreach (explode ("\n", str_replace ("\r", "", $Data['extensions'])) as $Extension)	{	?>
<TR><TD><? echo ($Extensions[$Extension] ? "<A HREF=\"" . $Extensions[$Extension] . "\">" : "") . $Extension . ($Extensions[$Extension] ? "</A>" : ""); ?></TD></TR>
<?	}
?>
</TABLE>