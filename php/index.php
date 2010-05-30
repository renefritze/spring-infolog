<?
require ("logical/common.php");
$ScriptStartTime = DoxTime ();
$Post = array_merge ($_POST, $_GET);
if (!$Post['Page'])	{
	$Post['Page'] = str_replace (array ("/", ".", ",", "\\"), "", (key ($Post) ? key ($Post) : "Index"));
	if (!$Post['NoHTML'])
		require ("header.php");
	require ("pages/" . $Post['Page'] . ".php");
	if (!$Post['NoHTML'])
		require ("footer.php");
}
if (!$Post['NoHTML'])	{	?>
<!-- RunTime: <? echo number_format (DoxTime () - $ScriptStartTime, 5, ".", ""); ?> sec -->
<?
}	?>