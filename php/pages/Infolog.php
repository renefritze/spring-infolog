<?
$Data = GetReport ($Post['ID']);
echo "[0] " . $Data['spring'], " has crashed.\n";
$Data = GetStacktrace ($Post['ID']);
foreach ($Data as $Row)
	echo $Row['raw'], "\n";
?>