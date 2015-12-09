var isyx=0;


$(document).ready(function(){
	$.formValidator.initConfig({theme:"baidu",submitOnce:true,formID:"form1",
		onError:function(msg){alert(msg);},mode:'AutoTip',
		submitAfterAjaxPrompt : '有数据正在异步验证，请稍等...'
	});

$("#username").formValidator({onShow:"请您输入需要注册的用户名！",onFocus:"请使用英文字母或数字,长度5-16字符.",onShowText:"请输入用户名",onCorrect:"该用户名可以注册"}).inputValidator({min:5,max:16,onError:"你输入的用户长度不正确,请确认"}).regexValidator({regExp:"username",dataType:"enum",onError:"用户名格式不正确"}).ajaxValidator({		dataType : "html",
		async : true,
		url : "ajax.asp?c=user",
		success : function(data){
           if( data == "请不要提交非法参数尝试GET注入！" ) {return "请不要提交非法参数,请更换用户名!";}else{
if( data == "0" ){return "此用户名已存在,请填写其它用户名!";}else{return true;}}
		},
		buttons: $("#button"),
		error: function(jqXHR, textStatus, errorThrown){alert("服务器没有返回数据，可能服务器忙，请重试"+errorThrown);},
		onError : "该用户名不可用，请更换用户名",
		onWait : "正在对用户名进行合法性校验，请稍候..."
	});
	
	$("#password1").formValidator({onShowFixText:"6~16个字符，包括字母、数字、特殊符号，区分大小写",onShow:"请输入密码",onFocus:"至少1个长度",onCorrect:"密码合法"}).inputValidator({min:6,max:16,empty:{leftEmpty:false,rightEmpty:false,emptyError:"密码两边不能有空符号"},onError:"密码长度错误,请确认"}).passwordValidator({compareID:"us"});


	$("#password2").formValidator({onShow:"请您再次输入登录密码！",onFocus:"密码只能使用英文字母或数字，长度6-16字符",onCorrect:"密码一致"}).inputValidator({min:6,max:16,empty:{leftEmpty:false,rightEmpty:false,emptyError:"重复密码两边不能有空符号"},onError:"您输入的密码长度不正确,请您核对！"}).compareValidator({desID:"password1",operateor:"=",onError:"2次密码不一致,请您核对！"});	



	  $("#email").formValidator({onShowFixText:"必须正确填写您的邮箱，用于找回密码",onShow:"请您输入正确的Email！",onFocus:"Email用于找回密码,请您认真填写",onCorrect:"正确",defaultValue:"@"}).inputValidator({min:6,max:100,onError:"您输入的邮箱长度非法,请您核对！"}).regexValidator({regExp:"^([\\w-.]+)@(([[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.)|(([\\w-]+.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(]?)$",onError:"您输入的邮箱格式不正确"}).ajaxValidator({
		dataType : "html",
		async : true,
		url : "ajax.asp?c=mail",
		success : function(data){
           if( data == "请不要提交非法参数尝试GET注入！" ) {return "请不要提交非法参数,请更换!";}else{
if( data == "0" ){return "该邮箱被注册,请更换";}else{return true;}}
		},
		buttons: $("#button"),
		error: function(jqXHR, textStatus, errorThrown){alert("服务器没有返回数据，可能服务器忙，请重试"+errorThrown);},
		onError : "Email邮箱不可用，请更换",
		onWait : "正在对邮箱进行合法性校验，请稍候..."
	});
	
	
	$("#qq").formValidator({onShow:"请您输入正确的QQ号码！",onCorrect:"正确"}).regexValidator({regExp:"qq",dataType:"enum",onError:"QQ号码格式不正确"}).ajaxValidator({
		dataType : "html",
		async : true,
		url : "ajax.asp?c=qq",
		success : function(data){
           if( data == "请不要提交非法参数尝试GET注入！" ) {return "请不要提交非法参数,请更换!";}else{
if( data == "0" ){return "QQ号码被注册,请更换";}else{return true;}}
		},
		buttons: $("#button"),
		error: function(jqXHR, textStatus, errorThrown){alert("服务器没有返回数据，可能服务器忙，请重试"+errorThrown);},
		onError : "该QQ不可用，请更换",
		onWait : "正在对QQ进行合法性校验，请稍候..."
	});
	
	$("#sj").formValidator({onShow:"请输入您的手机号码！",onfocus:"",onCorrect:"正确"}).inputValidator({min:11,max:11,onError:"手机号码必须为11位,请重新输入."}).regexValidator({regExp:"mobile",dataType:"enum",onError:"手机号码格式不正确"}).ajaxValidator({
		dataType : "html",
		async : true,
		url : "ajax.asp?c=sj",
		success : function(data){
           if( data == "请不要提交非法参数尝试GET注入！" ) {return "请不要提交非法参数,请更换!";}else{
if( data == "0" ){return "手机号码被注册，请更换";}else{return true;}}
		},
		buttons: $("#button"),
		error: function(jqXHR, textStatus, errorThrown){alert("服务器没有返回数据，可能服务器忙，请重试"+errorThrown);},
		onError : "该手机号码不可用，请更换",
		onWait : "正在对手机号码进行合法性校验，请稍候..."
	});
		
	

    

       	$("#tuiguang").formValidator({empty:true,onShow:"请输入推广人网站用户名！",onFocus:"请输入推广人网站用户名！",onCorrect:"正确",onEmpty:"没有就留空！"})
             .ajaxValidator({
		dataType : "html",
		async : true,
		url : "ajax.asp?c=tguang",
		success : function(data){
           if( data == "请不要提交非法参数尝试GET注入！" ) {return "请不要提交非法参数,请更换!";}else{
if( data == "0" ){return "推广人不存在,请您仔细核对！";}else{return true;}}
		},
		buttons: $("#button"),
		error: function(jqXHR, textStatus, errorThrown){alert("服务器没有返回数据，可能服务器忙，请重试"+errorThrown);},
		onError : "推广人不存在,请您仔细核对！",
		onWait : "正在对推广人进行合法性校验，请稍候..."
	});
	
});

function reloadAutoTip()
{
	$.formValidator.reloadAutoTip();
}



