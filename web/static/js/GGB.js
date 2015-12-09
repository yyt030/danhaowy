function myfun(){
	$.get("GG.asp",{"name":"john","location":"Boston","rnd":new Date().getTime()},function(msg){$("#mydiv").html(msg);},"html");
}
$(function(){myfun();});