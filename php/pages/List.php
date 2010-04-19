<?
$MySQL_Result = DB_Query ("SELECT id, date, `mod` FROM records");
?>
<TABLE>
<?
while ($Data = mysql_fetch_assoc ($MySQL_Result))	{
	?>
<TR><TD><A HREF="?Details&ID=<? echo $Data['id']; ?>"><? echo $Data['id']; ?></A></TD><TD><? echo $Data['date']; ?></TD><TD><? echo $Data['mod']; ?></TD></TR>
<?
}
?>
</TABLE>