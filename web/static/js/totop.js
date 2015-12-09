toTop = {
	init:function(){
		document.getElementById("toTop").onclick=function(e){
			toTop.set();
			return false;
		}		
	},
	waitTimer:null,
	set:function(){
		var d_st=document.documentElement.scrollTop;
		if(window.navigator.userAgent.indexOf("MSIE")>=1){
			for (var i=d_st; i>10; i-=Math.floor(i/6)){
			window.scrollTo(0,i);
			}
			window.scrollTo(0,10);
		}
		else{
		window.scrollTo(0,Math.floor(d_st / 2));
		
		 if(d_st>10){
				 waitTimer=setTimeout("toTop.set()",40);
		  }
			else{
				  clearTimeout(waitTimer);
			}
		}
	}
}

//window.onload = function(){toTop.init();};

//window.onerror = function(){return true;};
