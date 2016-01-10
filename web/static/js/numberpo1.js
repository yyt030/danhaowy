/***************************/
//Code By:<a href="http://wper.so">Wper.So</a>
//转载请保留此信息。	
/***************************/

// 定义弹窗初始状态和淡入淡出特效
var popupStatus = 0;

function loadPopup(){
	if(popupStatus==0){
		$("#backgroundPopup").css({
			"opacity": "0.7"
		});
		$("#backgroundPopup").fadeIn("slow");
		$("#Popup").fadeIn("slow");
		popupStatus = 1;
	}
}

function disablePopup(){
	if(popupStatus==1){
		$("#backgroundPopup").fadeOut("slow");
		$("#Popup").fadeOut("slow");
		popupStatus = 0;
	}
}

//弹窗居中显示
function centerPopup(){

	// 浏览器窗口的宽度和高度
	var windowWidth = document.documentElement.clientWidth;
	var windowHeight = document.documentElement.clientHeight;
	
	// 弹窗的宽度和高度,这里的值我们在CSS中定义。
	var popupHeight = $("#Popup").height();
	var popupWidth = $("#Popup").width();
	
	// 弹窗定位
	$("#Popup").css({
		"position": "absolute",
		"top": windowHeight/2-popupHeight/2,
		"left": windowWidth/2-popupWidth/2
	});
	
	$("#backgroundPopup").css({
		"height": windowHeight
	});
}


$(document).ready(function(){
	
		centerPopup();
		loadPopup();
	
	// 弹窗的关闭按钮激活时，加载淡出特效
	$("#popupClose").click(function(){
		disablePopup();
		window.location.href='ornumber';
	});
	$("#backgroundPopup").click(function(){
		disablePopup();
		window.location.href='ornumber';
	});
	// 响应键盘的ESCape键，加载淡出特效，关闭弹窗
	$(document).keypress(function(e){
		if(e.keyCode==27 && popupStatus==1){
			disablePopup();
			window.location.href='ornumber';
		}
	});

});