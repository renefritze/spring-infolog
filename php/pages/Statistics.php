<?
$MySQL_Result = DB_Query ("SELECT COUNT(id) AS Reports, crashed FROM records GROUP BY crashed");
while ($Data = mysql_fetch_assoc ($MySQL_Result))
	$Return['Reports'][$Data['crashed']] = $Data['Reports'];

?>
<TABLE>
<TR><TH COLSPAN="2">Statistics</TH></TR>
<TR><TD>No. reports</TD><TD><? echo array_sum ($Return['Reports']); ?></TD></TR>
<TR><TD>No. crashed reports</TD><TD><? echo ($Return['Reports'][1] ? $Return['Reports'][1] : "0"), " (", number_format ($Return['Reports'][1] / array_sum ($Return['Reports']) * 100, 1); ?>%)</TD></TR>
</TABLE>