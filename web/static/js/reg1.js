var isyx=0;


$(document).ready(function(){
	$.formValidator.initConfig({theme:"baidu",submitOnce:true,formID:"form1",
		onError:function(msg){alert(msg);},mode:'AutoTip',
		submitAfterAjaxPrompt : '�����������첽��֤�����Ե�...'
	});

$("#username").formValidator({onShow:"����������Ҫע����û�����",onFocus:"��ʹ��Ӣ����ĸ������,����5-16�ַ�.",onShowText:"�������û���",onCorrect:"���û�������ע��"}).inputValidator({min:5,max:16,onError:"��������û����Ȳ���ȷ,��ȷ��"}).regexValidator({regExp:"username",dataType:"enum",onError:"�û�����ʽ����ȷ"}).ajaxValidator({		dataType : "html",
		async : true,
		url : "ajax.asp?c=user",
		success : function(data){
           if( data == "�벻Ҫ�ύ�Ƿ���������GETע�룡" ) {return "�벻Ҫ�ύ�Ƿ�����,������û���!";}else{
if( data == "0" ){return "���û����Ѵ���,����д�����û���!";}else{return true;}}
		},
		buttons: $("#button"),
		error: function(jqXHR, textStatus, errorThrown){alert("������û�з������ݣ����ܷ�����æ��������"+errorThrown);},
		onError : "���û��������ã�������û���",
		onWait : "���ڶ��û������кϷ���У�飬���Ժ�..."
	});
	
	$("#password1").formValidator({onShowFixText:"6~16���ַ���������ĸ�����֡�������ţ����ִ�Сд",onShow:"����������",onFocus:"����1������",onCorrect:"����Ϸ�"}).inputValidator({min:6,max:16,empty:{leftEmpty:false,rightEmpty:false,emptyError:"�������߲����пշ���"},onError:"���볤�ȴ���,��ȷ��"}).passwordValidator({compareID:"us"});


	$("#password2").formValidator({onShow:"�����ٴ������¼���룡",onFocus:"����ֻ��ʹ��Ӣ����ĸ�����֣�����6-16�ַ�",onCorrect:"����һ��"}).inputValidator({min:6,max:16,empty:{leftEmpty:false,rightEmpty:false,emptyError:"�ظ��������߲����пշ���"},onError:"����������볤�Ȳ���ȷ,�����˶ԣ�"}).compareValidator({desID:"password1",operateor:"=",onError:"2�����벻һ��,�����˶ԣ�"});	



	  $("#email").formValidator({onShowFixText:"������ȷ��д�������䣬�����һ�����",onShow:"����������ȷ��Email��",onFocus:"Email�����һ�����,����������д",onCorrect:"��ȷ",defaultValue:"@"}).inputValidator({min:6,max:100,onError:"����������䳤�ȷǷ�,�����˶ԣ�"}).regexValidator({regExp:"^([\\w-.]+)@(([[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.)|(([\\w-]+.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(]?)$",onError:"������������ʽ����ȷ"}).ajaxValidator({
		dataType : "html",
		async : true,
		url : "ajax.asp?c=mail",
		success : function(data){
           if( data == "�벻Ҫ�ύ�Ƿ���������GETע�룡" ) {return "�벻Ҫ�ύ�Ƿ�����,�����!";}else{
if( data == "0" ){return "�����䱻ע��,�����";}else{return true;}}
		},
		buttons: $("#button"),
		error: function(jqXHR, textStatus, errorThrown){alert("������û�з������ݣ����ܷ�����æ��������"+errorThrown);},
		onError : "Email���䲻���ã������",
		onWait : "���ڶ�������кϷ���У�飬���Ժ�..."
	});
	
	
	$("#qq").formValidator({onShow:"����������ȷ��QQ���룡",onCorrect:"��ȷ"}).regexValidator({regExp:"qq",dataType:"enum",onError:"QQ�����ʽ����ȷ"}).ajaxValidator({
		dataType : "html",
		async : true,
		url : "ajax.asp?c=qq",
		success : function(data){
           if( data == "�벻Ҫ�ύ�Ƿ���������GETע�룡" ) {return "�벻Ҫ�ύ�Ƿ�����,�����!";}else{
if( data == "0" ){return "QQ���뱻ע��,�����";}else{return true;}}
		},
		buttons: $("#button"),
		error: function(jqXHR, textStatus, errorThrown){alert("������û�з������ݣ����ܷ�����æ��������"+errorThrown);},
		onError : "��QQ�����ã������",
		onWait : "���ڶ�QQ���кϷ���У�飬���Ժ�..."
	});
	
	$("#sj").formValidator({onShow:"�����������ֻ����룡",onfocus:"",onCorrect:"��ȷ"}).inputValidator({min:11,max:11,onError:"�ֻ��������Ϊ11λ,����������."}).regexValidator({regExp:"mobile",dataType:"enum",onError:"�ֻ������ʽ����ȷ"}).ajaxValidator({
		dataType : "html",
		async : true,
		url : "ajax.asp?c=sj",
		success : function(data){
           if( data == "�벻Ҫ�ύ�Ƿ���������GETע�룡" ) {return "�벻Ҫ�ύ�Ƿ�����,�����!";}else{
if( data == "0" ){return "�ֻ����뱻ע�ᣬ�����";}else{return true;}}
		},
		buttons: $("#button"),
		error: function(jqXHR, textStatus, errorThrown){alert("������û�з������ݣ����ܷ�����æ��������"+errorThrown);},
		onError : "���ֻ����벻���ã������",
		onWait : "���ڶ��ֻ�������кϷ���У�飬���Ժ�..."
	});
		
	

    

       	$("#tuiguang").formValidator({empty:true,onShow:"�������ƹ�����վ�û�����",onFocus:"�������ƹ�����վ�û�����",onCorrect:"��ȷ",onEmpty:"û�о����գ�"})
             .ajaxValidator({
		dataType : "html",
		async : true,
		url : "ajax.asp?c=tguang",
		success : function(data){
           if( data == "�벻Ҫ�ύ�Ƿ���������GETע�룡" ) {return "�벻Ҫ�ύ�Ƿ�����,�����!";}else{
if( data == "0" ){return "�ƹ��˲�����,������ϸ�˶ԣ�";}else{return true;}}
		},
		buttons: $("#button"),
		error: function(jqXHR, textStatus, errorThrown){alert("������û�з������ݣ����ܷ�����æ��������"+errorThrown);},
		onError : "�ƹ��˲�����,������ϸ�˶ԣ�",
		onWait : "���ڶ��ƹ��˽��кϷ���У�飬���Ժ�..."
	});
	
});

function reloadAutoTip()
{
	$.formValidator.reloadAutoTip();
}



