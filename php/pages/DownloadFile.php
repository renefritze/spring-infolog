<?
if (file_exists ("../" . $Post['File']))	{
	$MySQL_Result = DB_Query ("SELECT id FROM records WHERE filename='" . mysql_escape_string ($Post['File']) . "'");
	if (mysql_num_rows ($MySQL_Result))	{
		$File = "../" . $Post['File'];
	    header("Content-Type: application/octet-stream");
    	header("Content-Length: " . filesize ($File));
	    header("Content-Disposition: attachment; filename=" . $Post['File']);
    	header("Content-Transfer-Encoding: binary");
		$FP = fopen ($File, "r");
		fpassthru ($FP);
		fclose ($FP);
	}
}
?>