<?
require ("site.config.php");
require ("logical/common.php");
$Post = array_merge ($_POST, $_GET);
if (!$Post['Page'])
	$Post['Page'] = str_replace (array ("/", ".", ",", "\\"), "", (key ($Post) ? key ($Post) : "Index"));

require ("pages/" . $Post['Page'] . ".php");
?>