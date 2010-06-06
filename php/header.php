<HTML>
<HEAD>
<STYLE>@import url(Style.css);</STYLE>
<TITLE>Spring crash statistics</TITLE>

</HEAD>
<BODY ONMOUSEMOVE="CaptureMousePos (event);">
<SCRIPT>
function CaptureMousePos (e)	{
	try	{
		if (e.clientX)	{
			window.MousePosX = e.clientX + (document.documentElement.scrollLeft ? document.documentElement.scrollLeft : document.body.scrollLeft);
			window.MousePosY = e.clientY + (document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop);
			return false;
		}
	}
	catch (e)	{
		if (event.clientX)	{
			window.MousePosX = event.clientX + (document.documentElement.scrollLeft ? document.documentElement.scrollLeft : document.body.scrollLeft);
			window.MousePosY = event.clientY + (document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop);
			return false;
		}
	}
}
</SCRIPT>