<?
$Data = GetReport ($Post['ID']);
?>
<TABLE>
<TR><TD><? echo $Data['id'], ": ", $Data['mod']; ?></TD></TR>
<TR><TH CLASS="Sub">Extensions</TH></TR>
<?
if ($Data['extensions'])
	foreach (explode ("\n", $Data['extensions']) as $Extension)	{	?>
<TR><TD><? echo $Extension; ?></TD></TR>
<?	}
?>
</TABLE>