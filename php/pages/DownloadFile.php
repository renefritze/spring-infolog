<?
if (file_exists ("../" . $Post['File']))	{
	$MySQL_Result = DB_Query ("SELECT id FROM records WHERE filename='" . mysql_escape_string ($Post['File']) . "'");
	if (mysql_num_rows ($MySQL_Result))	{
		$FP = fopen ("../" . $Post['File'], "r");
		fpassthru ($FP);
		fclose ($FP);
	}
}
?>