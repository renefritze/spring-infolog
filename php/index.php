<?
require ("site.config.php");
require ("logical/common.php");
$ScriptStartTime = DoxTime ();
$Post = array_merge ($_POST, $_GET);
if (!$Post['Page'])	{
	$Post['Page'] = str_replace (array ("/", ".", ",", "\\"), "", (key ($Post) ? key ($Post) : "Index"));
	require ("header.php");
	require ("pages/" . $Post['Page'] . ".php");
	require ("footer.php");
}
?>

<!-- RunTime: <? echo number_format (DoxTime () - $ScriptStartTime, 5, ".", ""); ?> sec -->