var xmlHttp;
var addNew;
var uu = "";
var jc = "";
function GetXmlHttpObject(handler) {
	var objXmlHttp = null
	if (navigator.userAgent.indexOf("MSIE") >= 0) {
		var strName = "Msxml2.XMLHTTP"
		if (navigator.appVersion.indexOf("MSIE 5.5") >= 0) {
			strName = "Microsoft.XMLHTTP"
		}
		try {
			objXmlHttp = new ActiveXObject(strName)
			objXmlHttp.onreadystatechange = handler
			return objXmlHttp
		} catch (e) {
			alert("Error. Scripting for ActiveX might be disabled")
			return
		}
	} else {
		objXmlHttp = new XMLHttpRequest()
		objXmlHttp.onload = handler
		objXmlHttp.onerror = handler
		return objXmlHttp
	}
}
function showre(p,x) {
	var p = p || 0;
	var x = x || 0;
	var code = get("code");
	var sja = get("sja");
	var s1 = get("Select1");
	var s2 = get("Select2");
	var s3 = get("Select3");
	var s4 = get("Select4");
	var s5 = get("Select5");
	var s6 = get("Select6");
	var com = get("com");
	var sm = get("sm");
	var shdz = get("shdz");
	var fhdz = get("fhdz");
	var isordz = $('input:radio[name="sertype"]:checked').val()
	var sa = s1 + " " + s2 + " " + s3;
	var sb = s4 + " " + s5 + " " + s6;
	if (s1 == "") {
		var sa = "";
	}
	if (s4 == "") {
		var sb = "";
	}
	if (isordz == "2") {
		var sa = shdz;
		var sb = fhdz;
	 var radios = 2
	}else{
	var radios = 1
	}
	 // if(p==0 && x==0 ){if(code==""){alert("����д��֤��,��֤�벻��Ϊ�գ�");return false;}}
	if (sa == "" && sb == "") {
		alert("������ַ �� �ջ���ַ ����ͬʱΪ�գ�\n\n ����������ѡ��һ���շ�����ַ��");
		return false;
	}
	if (x==0){timer(3);}
	var token = topip(true, 3, 32)
	writeCookie("s1", s1, "30");
	writeCookie("s2", s2, "30");
	writeCookie("s3", s3, "30");
	writeCookie("sja", sja, "30");
	writeCookie("s4", s4, "30");
	writeCookie("s5", s5, "30");
	writeCookie("s6", s6, "30");
	writeCookie("sja", sja, "30");
	writeCookie("com", com, "30");
	writeCookie("shdz", shdz, "30");
	writeCookie("fhdz", fhdz, "30");
	writeCookie("p", p, "30");
	gethtml("imglist", "<div style='color:red;text-align:center;'><img src='images/wait.gif'/>���ڲ�ѯ�С�����</div>");
	var url = "Qiso.asp?sja=" + sja + "&sa=" + escape(sa) + "&sb=" + escape(sb) + "&kd=" + com + "&sm=" + sm + "&x=" + x + "&p=" + p + "&token=" + token + "&radios=" + radios + "&code=" + code;
	var lx = showhtml;
	xmlHttp = GetXmlHttpObject(lx)
	xmlHttp.open("GET", url, true)
	xmlHttp.send(null)
}

function showhtml() {
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == "complete") {
		
	
		var Nums = xmlHttp.responseXML.getElementsByTagName("data")[0].getAttribute('Nums');
		xmltitle = xmlHttp.responseXML.getElementsByTagName("title")
		xmlfh = xmlHttp.responseXML.getElementsByTagName("fh")
		xmlsh = xmlHttp.responseXML.getElementsByTagName("sh")
		var imglist = "<TABLE class='table table-bordered table-condensed table-striped' style='font-size: 12px;'><THEAD><TR><TH align='center' style='text-align: center; width:7%;'>���</TH><TH align='center' style='text-align: center; width:12%;'>��ݵ���</TH><TH align='center' style='text-align: center; width:10%;'>�������</TH><TH align='center' style='text-align: center; width:41%;'>������ַ/�ջ���ַ</TH><TH align='center' style='text-align: center; width:19%;'>ɨ��ʱ��</TH><TH style='text-align: center; width:8%;'>��ȡ����</TH><TH align='center' style='text-align: center; width:3%;'><input type='checkbox' id='chkAll'  value='checkbox' style='border:0' onClick=checkAll()><input id='qindex' type='hidden' value='0'/></TH></TR></THEAD><TBODY>";
		for (i = 0; i < xmltitle.length; i++) {
			var title = xmltitle[i].firstChild.data;
			var jh = xmltitle[i].getAttribute("jh");
			if (title == "loginerror") {
				gethtml("imglist", "<div style='color:red;text-align:center;'><img src='images/error_01.png'/>��¼�Ѿ�ʧЧ,�����µ�¼��</div>");
			}
			if (title == "tokenerror") {
				gethtml("imglist", "<div style='color:red;text-align:center;'><img src='images/error_01.png'/>�ύʧ��,�������ύ��ѯ��</div>");
			}
			if (jh == 0) {
				gethtml("jhs", "<div style='color:red;text-align:center;margin-top: 10px;margin-bottom: 15px;'>���ã�����ǰ�ʺ�û�м���,��ѯֻ��ʾ10�����š��ʺż����,��ѯ��ʾ���е��š�<a href='wybjihuo.asp'><img src='images/jihuo.gif'  border='0' align='top' title='����˰�ť�����ʺ�' /></a></div>");
			}
			if (title == "û��") {
				imglist = "<div style='color:red;text-align:center;margin-top: 10px;margin-bottom: 15px;'><img src='images/error_01.png'/>δ���ҵ�,��������ҷ�Χ! <a href='/News.asp?id=48' target='_blank'>>>����鿴����<</a> <br /><br />δ���ҵ�? ���������Է��հ���<a href='buykongbao.asp' target='_blank' class='btn'>��Ҫ���հ�</a></div>";
				gethtml("imglist");
			} else if (title == "timererror") {
				imglist = "<div style='color:red;text-align:center;'><img src='face/018.gif'/>ѹ��ɽ����������ѯ����Ƶ��,��ЪЪ,Ԥ��3���ڿ��ٴβ�ѯ��</div>";
				gethtml("imglist");
			} else if (title == "codeerror") {
				imglist = "<div style='color:red;text-align:center;'><img src='images/error_01.png'/>���������֤�����,��������������ύ��ѯ!</div>";
				$("#code").val("");getcode();
				gethtml("imglist");
			} else {
				var fh = xmlfh[i].firstChild.data;
				var sh = xmlsh[i].firstChild.data;
				var Time = xmltitle[i].getAttribute("Time");
				var htmlid = xmltitle[i].getAttribute("id");
				var Qoi = xmltitle[i].getAttribute("Qoi");
				var Qid = xmltitle[i].getAttribute("Qid");
				var sm = xmltitle[i].getAttribute("sm");
				var kda = xmltitle[i].getAttribute("kda");
				var PerPage = xmltitle[i].getAttribute("PerPage");
				var P_Nums = xmltitle[i].getAttribute("P_Nums");
				var page = xmltitle[i].getAttribute("page");
				var kda = xmltitle[i].getAttribute("kda");
				var saomiaotxt = xmltitle[i].getAttribute("saomiaotxt");
				var cc = xmltitle[i].getAttribute("cc");
									
				imglist += "<tr>";
				imglist += "<td style='line-height: 40px;text-align:center;'>" + Qoi + "</td>";
				if (cc==0){
				imglist += "<td style='line-height: 40px;'>" + htmlid + " </td>";
					}else{
				imglist += "<td style='line-height: 40px;'>" + htmlid + " <input name=\"COSS\" type=\"button\" onclick=\"Coss("+Qid+",'"+cc+"',0);\" value=\"���\" class=\"zdybutton\"></td>";
						}				
				imglist += "<td style='line-height: 40px;text-align:center;'>" + title + "</td>";
				imglist += "<td style='text-align: center;'>������ַ��" + fh + "<br/><font color=#EE5C42>�ջ���ַ��" + sh + "</font></td>";
				if (sm == 0 || sm == 2) {
					imglist += "<td style='color: #1E90FF;line-height: 40px;text-align:center;' id='qs" + Qid + "'>�����ѯ<a href='javascript:' title='�����ѯ״̬' onClick=Qikd('" + kda + "',1,'" + Qid + "','0')><img src='images/so.jpg'></a></td>"
					imglist += "<td style='text-align: center;'><input type='button' id='fs" + Qid + "' class='btnumey' value='��  ȡ' onClick=Qik('" + Qid + "','"+sm+"') style='cursor:hand;margin-top: 9px'></td>";
				} else {
					imglist += "<td style='line-height: 40px;'><font color='red'>" + sm + "</font><a href='javascript:' title='�����ѯ״̬' onClick=sncx('" + escape(sm)+"&nbsp;"+ escape(saomiaotxt) + "')><img src='images/so.jpg'></a></td>";
					imglist += "<td style='text-align: center;'><input type='button' class='btnumey' value='��  ȡ' onClick=Qik('" + Qid + "','"+ escape(sm) +"') style='cursor:hand;margin-top: 9px'></td>";
				}
				imglist += "<TD style='text-align:center;'><span class='qiall'><input id='Qidd' type='checkbox' name='Qidd' value='" + Qid + "' style='margin-top: 12px'></span></TD>";
				imglist += "</tr>";
			}
		}
		if (P_Nums > 1) {
			var Plist = "<tr><td colspan='9'><div id='page'><ul>";
			if (page < 2) {
				Plist += "<li><span>�ס�ҳ</span></li><li><span>��һҳ</span></li>"
			} else {
				Plist += "<li><a href='javascript:' onclick=showre(1,1) title='�ס�ҳ'>�ס�ҳ</a></li><li><a href='javascript:' onclick=showre(" + (page - 1) + ",1) title='��һҳ'>��һҳ</a></li>"
			}
			if (P_Nums > page * 1 + 9) {
				var endpage = page * 1 + 9;
			} else {
				var endpage = P_Nums;
			}
			for (var i = page - 1; i <= endpage; i++) {
				if (i > 0) {
					Plist += (i == page) ? "<li><span>" + i + "</span></li>" : "<li><a href='javascript:' onclick=showre(" + i + ",1)>" + i + "</a></li>"
				}
			}
			if (page == P_Nums) {
				Plist += "<li><span>��һҳ</span></li><li><span>ĩ��ҳ</span></li>"
			} else {
				Plist += "<li><a href='javascript:' onclick=showre(" + (page * 1 + 1) + ",1) title='��һҳ'>��һҳ</a></li><li><a href='javascript:' onclick=showre(" + P_Nums + ",1) title='ĩ��ҳ'>ĩ��ҳ</a></li>"
			}
			Plist += "</ul></div></td></tr></TBODY></TABLE>"
		} else {
			var Plist = "</TBODY></TABLE>";
		}
		gethtml("imglist", imglist + Plist)

		//if (imglist.indexOf("��ѯ") > 0 ){$("#code").val("");getcode();}
	}
}






function shopshowre(p,x) {
	var p = p || 0;
	var x = x || 0;
	var code = get("code");
	var sja = get("sja");
	var s1 = get("Select1");
	var s2 = get("Select2");
	var s3 = get("Select3");
	var s4 = get("Select4");
	var s5 = get("Select5");
	var s6 = get("Select6");
	var com = get("com");
	var sm = get("sm");
	var seller = get("seller");
	var shdz = get("shdz");
	var fhdz = get("fhdz");
	var isordz = $('input:radio[name="sertype"]:checked').val()
	var sa = s1 + " " + s2 + " " + s3;
	var sb = s4 + " " + s5 + " " + s6;
	if (s1 == "") {
		var sa = "";
	}
	if (s4 == "") {
		var sb = "";
	}
	if (isordz == "2") {
		var sa = shdz;
		var sb = fhdz;
	 var radios = 2
	}else{
	var radios = 1
	}
	//if(p==0 && x==0 ){if(code==""){alert("����д��֤��,��֤�벻��Ϊ�գ�");return false;}}
	if (sa == "" && sb == "") {
		alert("������ַ �� �ջ���ַ ����ͬʱΪ�գ�\n\n ����������ѡ��һ���շ�����ַ��");
		return false;
	}
	if (x==0){timer(3);}
	var token = topip(true, 3, 32)
	writeCookie("s1", s1, "30");
	writeCookie("s2", s2, "30");
	writeCookie("s3", s3, "30");
	writeCookie("sja", sja, "30");
	writeCookie("s4", s4, "30");
	writeCookie("s5", s5, "30");
	writeCookie("s6", s6, "30");
	writeCookie("sja", sja, "30");
	writeCookie("com", com, "30");
	writeCookie("shdz", shdz, "30");
	writeCookie("fhdz", fhdz, "30");
	writeCookie("seller", seller, "30");
	writeCookie("p", p, "30");
	gethtml("imglist", "<div style='color:red;text-align:center;'><img src='images/wait.gif'/>���ڲ�ѯ�С�����</div>");
	var url = "ShopQiso.asp?sja=" + sja + "&sa=" + escape(sa) + "&sb=" + escape(sb) + "&kd=" + com + "&sm=" + sm + "&p=" + p + "&seller=" + seller + "&token=" + token + "&radios=" + radios + "&code=" + code;
	var lx = shopshowhtml;
	xmlHttp = GetXmlHttpObject(lx)
	xmlHttp.open("GET", url, true)
	xmlHttp.send(null)
}

function shopshowhtml() {
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == "complete") {
		var Nums = xmlHttp.responseXML.getElementsByTagName("data")[0].getAttribute('Nums');
		xmltitle = xmlHttp.responseXML.getElementsByTagName("title")
		xmlfh = xmlHttp.responseXML.getElementsByTagName("fh")
		xmlsh = xmlHttp.responseXML.getElementsByTagName("sh")
		var imglist = "<TABLE class='table table-bordered table-condensed table-striped'style='font-size: 12px;'><THEAD><TR><TH align='center'style='text-align:center;'width='7%'>���</TH><TH align='center'style='text-align:center;'width='12%'>��ݵ���</TH><TH align='center'style='text-align:center;'width='9%'>�������</TH><TH align='center'style='text-align:center;'width='29%'>������ַ/�ջ���ַ</TH><TH align='center'style='text-align:center;'width='8%'>����</TH><TH align='center'style='text-align:center;'width='17%'>ɨ��ʱ��</TH><TH align='center'style='text-align:center;'width='7%'>������</TH><TH align='center'style='text-align:center;'width='12%'>ȫѡ/��ѡ<input type='checkbox'id='chkAll'value='checkbox'style='border:0'onClick='shopcheckAll()'><input id='qindex'type='hidden'value='0'/></TH></TR></THEAD><TBODY>";
		for (i = 0; i < xmltitle.length; i++) {
			var title = xmltitle[i].firstChild.data;
			var jh = xmltitle[i].getAttribute("jh");
			if (title == "loginerror") {
				gethtml("imglist", "<div style='color:red;text-align:center;'><img src='images/error_01.png'/>��¼�Ѿ�ʧЧ,�����µ�¼��</div>");
			}
			if (title == "tokenerror") {
				gethtml("imglist", "<div style='color:red;text-align:center;'><img src='images/error_01.png'/>�ύʧ��,�������ύ��ѯ��</div>");
			}
			if (title == "û��") {
				imglist = "<div style='color:red;text-align:center;margin-top: 10px;margin-bottom: 15px;'><img src='images/error_01.png'/>δ���ҵ�,��������ҷ�Χ! <a href='/News.asp?id=48' target='_blank'>>>����鿴����<</a> <br /><br />δ���ҵ�? ���������Է��հ���<a href='buykongbao.asp' target='_blank' class='btn'>��Ҫ���հ�</a></div>";
				gethtml("imglist");
			} else if (title == "timererror") {
				imglist = "<div style='color:red;text-align:center;'><img src='face/018.gif'/>ѹ��ɽ����������ѯ����Ƶ��,��ЪЪ,Ԥ��3���ڿ��ٴβ�ѯ��</div>";
				gethtml("imglist");
			} else if (title == "codeerror") {
				imglist = "<div style='color:red;text-align:center;'><img src='images/error_01.png'/>���������֤�����,��������������ύ��ѯ!</div>";
				gethtml("imglist");
			} else {
				var fh = xmlfh[i].firstChild.data;
				var sh = xmlsh[i].firstChild.data;
				var Time = xmltitle[i].getAttribute("Time");
				var htmlid = xmltitle[i].getAttribute("id");
				var Qoi = xmltitle[i].getAttribute("Qoi");
				var Qid = xmltitle[i].getAttribute("Qid");
				var sm = xmltitle[i].getAttribute("sm");
				var kda = xmltitle[i].getAttribute("kda");
				var PerPage = xmltitle[i].getAttribute("PerPage");
				var P_Nums = xmltitle[i].getAttribute("P_Nums");
				var page = xmltitle[i].getAttribute("page");
				var kda = xmltitle[i].getAttribute("kda");
				var shopmoney = xmltitle[i].getAttribute("Shopmoney");
				var shopuser = xmltitle[i].getAttribute("shopuser");
				var saomiaotxt = xmltitle[i].getAttribute("saomiaotxt");
				var cc = xmltitle[i].getAttribute("cc");			
										
				imglist += "<tr id='yc"+Qid+"'>";
				imglist += "<td style='line-height: 40px;text-align:center;'>" + Qoi + "</td>";
				if (cc==0){
				imglist += "<td style='line-height: 40px;'>" + htmlid + " </td>";
					}else{
				imglist += "<td style='line-height: 40px;'>" + htmlid + " <input name=\"COSS\" type=\"button\" onclick=\"Coss("+Qid+",'"+cc+"',1);\" value=\"���\" class=\"zdybutton\"></td>";
						}	
				imglist += "<td style='line-height: 40px;text-align:center;'>" + title + "</td>";
				imglist += "<td style='text-align: center;'>������ַ��" + fh + "<br/><font color=#EE5C42>�ջ���ַ��" + sh + "</font></td>";
				imglist += "<td style='color:#2E2EFE;line-height: 40px;text-align:center;' id='nn"+Qid+"'>" + shopmoney + "/Ԫ</td>";
				if (sm == 0 || sm == 2 ) {	
					imglist += "<td style='color: #1E90FF;line-height: 40px;text-align:center;' id='qs" + Qid + "'>�����ѯ<a href='javascript:' title='¼��ʱ�䣺"+Time+"' onClick=Qikd('" + kda + "',1,'" + Qid + "','1')><img src='images/so.jpg'></a></td>"
				} else {
					imglist += "<td style='line-height: 40px;text-align:center;'><font color='red'>" + sm + "</font><a href='javascript:' title='�����ѯ״̬' onClick=sncx('" + escape(sm)+"&nbsp;"+ escape(saomiaotxt) + "')><img src='images/so.jpg'></a></td>";
				}
				if (shopuser == 0){
					imglist += "<td style='color:#603;line-height: 40px;text-align:center;'>����Ա</td>";	
					}else {
					imglist += "<td style='color:#ea00ff;line-height: 40px;text-align:center;'>"+shopuser+"</td>";	
				
				}
		if (sm == 2 ) {
				imglist += "<td style='line-height: 40px;text-align:center;'><a href='javascript:' id='gm"+Qid+"' onclick='shopQik("+Qid+","+shopmoney+",2)' style='cursor:hand;'>��������</a> <span class='qiall'><input id='id' type='checkbox' name='id' value='"+Qid+"'></span></td>";
				} else {
				imglist += "<td style='line-height: 40px;text-align:center;'><a href='javascript:' id='gm"+Qid+"' onclick='shopQik("+Qid+","+shopmoney+")' style='cursor:hand;'>��������</a> <span class='qiall'><input id='id' type='checkbox' name='id' value='"+Qid+"'></span></td>";					
					}
				
				imglist += "</tr>";
			}
		}
		if (P_Nums > 1) {
			var Plist = "<tr><td colspan='9'><div id='page'><ul>";
			if (page < 2) {
				Plist += "<li><span>�ס�ҳ</span></li><li><span>��һҳ</span></li>"
			} else {
				Plist += "<li><a href='javascript:' onclick=shopshowre(1,1) title='�ס�ҳ'>�ס�ҳ</a></li><li><a href='javascript:' onclick=shopshowre(" + (page - 1) + ",1) title='��һҳ'>��һҳ</a></li>"
			}
			if (P_Nums > page * 1 + 9) {
				var endpage = page * 1 + 9;
			} else {
				var endpage = P_Nums;
			}
			for (var i = page - 1; i <= endpage; i++) {
				if (i > 0) {
					Plist += (i == page) ? "<li><span>" + i + "</span></li>" : "<li><a href='javascript:' onclick=shopshowre(" + i + ",1)>" + i + "</a></li>"
				}
			}
			if (page == P_Nums) {
				Plist += "<li><span>��һҳ</span></li><li><span>ĩ��ҳ</span></li>"
			} else {
				Plist += "<li><a href='javascript:' onclick=shopshowre(" + (page * 1 + 1) + ",1) title='��һҳ'>��һҳ</a></li><li><a href='javascript:' onclick=shopshowre(" + P_Nums + ",1) title='ĩ��ҳ'>ĩ��ҳ</a></li>"
			}
			Plist += "</ul></div></td></tr></TBODY></TABLE>"
		} else {
			var Plist = "</TBODY></TABLE>";
		}
		gethtml("imglist", imglist + Plist)
		
		//if (imglist.indexOf("��ѯ") > 0 ){$("#code").val("");getcode();}

	}
}

function topip(randomFlag, min, max){
    var str = "",
        range = min,
        arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
 
    // �������
    if(randomFlag){
        range = Math.round(Math.random() * (max-min)) + min;
    }
    for(var i=0; i<range; i++){
        pos = Math.round(Math.random() * (arr.length-1));
        str += arr[pos];
    } 
	  var date=new Date();
          date.setTime(date.getTime()+10000);
          document.cookie = "Tokenkey" + "=" + escape(str)  + "; expires=" + date.toGMTString() + "; path=/";
    return str;

}



function Qiall() {
	var idx = document.getElementsByName("Qidd");
	var idlen = 0;
	var Qiids = "";
	for (var i = 0; i < idx.length; i++) {
		if (idx[i].checked) {
			idlen = idlen + 1
		}
	}
	if (idlen < 2) {
		alert('������ȡ����ѡ��2��,���㻹û�в�ѯ,���Ȳ�ѯ��');
		return;
	}
	if (idlen > 20) {
		alert('ÿ�������ȡ20��,��ȡ������¹�ѡ��ȡ��');
		return;
	}
	for (var i = 0; i < idx.length; i++) {
		if (idx[i].checked) {
			Qiids += "uid=" + idx[i].value + "&"
		}
	}
	if (Qiids.charAt(Qiids.length - 1) == "&") {
		Qiids = Qiids.substring(Qiids.length - 1, Qiids);
	}
	location = "BatchGetNumber.asp?" + Qiids + "";
}

function Qik(uid,sm) {
	if (sm == 2 ){
var d = dialog({
    title: '�Ե�����,��ʾ��',
    content: '�õ�����ɨ��,��δ��ѯ������,������Ȳ�ѯ������<br/>��ȷ��Ҫ��ȡ��,��ȡ�󲻿��˵�Ŷ��',
    okValue: 'ȷ��',
    ok: function () {
	var url = "GetNumber.asp?uid=" + uid;
	location = url;
        return false;
    },
    cancelValue: 'ȡ��',
    cancel: function () {}
});
d.show();
		}else{
		if (sm != 0){
var sm = unescape(sm)	
var d = dialog({
    title: '�Ե�����,��ʾ��',
    content: '�õ�����ɨ��,��ȡǰ���ȱȶ�ɨ��ʱ�䣡<br/>ɨ��ʱ�䣺'+ sm +'<br/>��ȷ��Ҫ��ȡ��,��ȡ�󲻿��˵�Ŷ��',
    okValue: 'ȷ��',
    ok: function () {
	var url = "GetNumber.asp?uid=" + uid;
	location = url;
        return false;
    },
    cancelValue: 'ȡ��',
    cancel: function () {}
});
d.show();
			}
		else{			
	var url = "GetNumber.asp?uid=" + uid;
	location = url;	
	
		}
	}
}

function getcode() {
	var randomnum = Math.random();
	var img = document.getElementById("icode");
	img.src = "inc/node.asp?r=" + randomnum;
}

function changesertype(val) {
	$("#diz1").hide()
	$("#diz2").hide()
	$("#diz" + val).show()
}

function checkAll() {
	if ($("#chkAll").is(":checked")) {
		var ids = $("input[name='Qidd']");����
		for (var i = 0; i < ids.length; i++) {
			if (ids[i].checked == true) {
				ids[i].checked = "";
			} else {
				ids[i].checked = "checked";
			}��
		}
	} else {
		$(".qiall input").attr("checked", false);
	}
}


function shopcheckAll(){
if($("#chkAll").is(":checked"))
	{var ids=$("input[name='id']");
���� for(var i=0;i<ids.length;i++){  
if(ids[i].checked==true){ids[i].checked="";   }else{   ids[i].checked="checked";  }  ��}
	}else{
		$(".qiall input").attr("checked",false);
	}
}



function gethtml(name, lx) {
	document.getElementById(name).innerHTML = lx;
}

function get(name) {
	return document.getElementById(name).value;
}

function Qikd(com, id, qid,i) {
	if (id == "0") {
		var q = 1;
	} else {
		var q = 0;
	}
	  if (i == "0"){
		$.ajax({
		type: 'post',
		url: 'Qikd.asp',
		dataType: 'text',
		data: {
			com: com,
			id: id,
			qid: qid,
			q: q
		},
		timeout: 0,
		cache: false,
		error: err,
		success: suc
		
	})
  }else{
		$.ajax({
		type: 'post',
		url: 'Qikd.asp',
		dataType: 'text',
		data: {
			com: com,
			id: id,
			qid: qid,
			q: q
		},
		timeout: 0,
		cache: false,
		error: err,
		success: suv
		
	})	  
	  
	  
	  
	  }
 dialog({
		id: 'ccx',
		content: '����Ŭ����ѯ��........'
	}).showModal();
      uu = dialog.get('ccx').title('�Ե�����,��ʾ��');
	setInterval(function() {
		if (DQCookie("qi" + qid)!= -1) {
			uu.close().remove();
			delCookie("qi" + qid,"1")
			
		}
		
	}, 100);	


	function err() {
		writeCookie("qi" + qid, "1", "1");
		var s = dialog({
			title: '�Ե�����,��ʾ��',
			content: '��ѯ����'
		});
		s.show();
	}

	function suc(str) {
		writeCookie("qi" + qid, "1", "1");
		uu.close().remove();
		if (q == "1") {
			dialog({
				title: '������Ϣ',
				content: str
			}).show();
		} else {
			if (str == 0) {
				uu.close().remove();
				var d = dialog({
					title: '�Ե�����,��ʾ��',
					content: '<font color=\"#006600\">Y(^_^)Y �õ��Ű�ȫ��δɨ��,�����ʹ�á�</font>',
					ok: function() {}
				});
				d.showModal();
			} else {
				
				if (str == 2){
				uu.close().remove();
				var d = dialog({
					title: '�Ե�����,��ʾ��',
					content: '<font color=\"#FF0000\">�õ���δ�ڹ涨��32Сʱ��ɨ��,����������ȡ��</font>',
					ok: function() {}
					
				});
				d.showModal();		
					}else{
				uu.close().remove();
				var str = str.split(",")	
				var d = dialog({	
					title: '�Ե�����,��ʾ��',
					content: '<font color=\"#FF0000\">-_-��sorry�� �õ�����ɨ��,����ϸ�ȶ�ʱ�䡣<br/>�ռ�ʱ�䣺<br/>'+str[0]+ ' '+str[1]+'</font>',
					ok: function() {
						$("#fs"+ qid ).attr("onclick","Qik('"+qid+"','"+escape(str[0])+"')");
						$("#qs" + qid).html("<font color=\"#FF0000\">" + str[0] + "</font><a href=\"javascript:\" title=\"�����ѯ״̬\" onclick=\"sncx('"+str[0]+" "+str[1]+"')\"><img src=\"images/so.jpg\"></a>");


					}
				});
				d.showModal();
				}
			}
		}
	}
	
	
	
		function suv(str) {
		writeCookie("qi" + qid, "1", "1");
		uu.close().remove();
		if (q == "1") {
			dialog({
				title: '������Ϣ',
				content: str
			}).show();
		} else {
			if (str == 0) {
				uu.close().remove();
				var d = dialog({
					title: '�Ե�����,��ʾ��',
					content: '<font color=\"#006600\">Y(^_^)Y �õ��Ű�ȫ��δɨ��,�����ʹ�á�</font>',
					ok: function() {}
				});
				d.showModal();
			} else {
				
				if (str == 2){
				uu.close().remove();
				var d = dialog({
					title: '�Ե�����,��ʾ��',
					content: '<font color=\"#FF0000\">�õ���δ�ڹ涨��32Сʱ��ɨ��,����������ȡ��</font>',
					ok: function() {}
					
				});
				d.showModal();		
					}else{
				uu.close().remove();
				var str = str.split(",")	
				var d = dialog({
					title: '�Ե�����,��ʾ��',
					content: '<font color=\"#FF0000\">-_-��sorry�� �õ�����ɨ��,����ϸ�ȶ�ʱ�䡣<br/>�ռ�ʱ�䣺<br/>'+str[0]+ ' '+str[1]+'</font>',
					ok: function() {
						
						$("#qs" + qid).html("<font color=\"#FF0000\">" + str[0] + "</font><a href=\"javascript:\" title=\"�����ѯ״̬\" onclick=\"sncx('"+str[0]+" "+str[1]+"')\"><img src=\"images/so.jpg\"></a>");
						nus = $("#nn" + qid).html();
						nus = nus.replace('/Ԫ','')
						if (nus != "0.25"){
						nus = nus/2;
						$("#nn" + qid).html(nus+'/Ԫ');
						}
						$("#gm"+ qid ).attr("onclick","shopQik('"+qid+"','"+nus+"')");


					}
				});
				d.showModal();
				}
			}
		}
	}
}






function showadr(str) {
	var divadr;
	var btn;
	divadr = document.getElementById("adr");
	btn = btn ? btn : (window.event ? window.event : null);
	//divadr.style.left=document.body.scrollWidth/2-225+"px";
	//divadr.style.top="200px";
	gethtml("Qistr", str);
	divadr.style.display = "block";
}

function guanbi(cstr) {
	document.getElementById(cstr).style.display = "none";
}

function getv(dd) {
	return document.getElementById(dd);
}

function copyinfo() {
	var info = getv("infotr");
	var clipBoardContent = info.innerText;
	window.clipboardData.setData("Text", clipBoardContent);
	alert("���Ƴɹ�");
}

function writeCookie(name, value, day) {
	expire = "";
	expire = new Date();
	expire.setTime(expire.getTime() + day * 24 * 3600 * 1000);
	expire = expire.toGMTString();
	document.cookie = name + "=" + escape(value) + ";expires=" + expire;
}

function readCookie(name) {
	cookieValue = "";
	search1 = name + "=";
	if (document.cookie.length > 0) {
		offset = document.cookie.indexOf(search1);
		if (offset != -1) {
			offset += search1.length;
			end = document.cookie.indexOf(";", offset);
			if (end == -1) end = document.cookie.length;
			cookieValue = unescape(document.cookie.substring(offset, end));
		}
	}
	return cookieValue;
}

function DQCookie(name) {
 var  nn = "";
	nn = document.cookie.indexOf(name)
	return nn;
}


function delCookie(name,value){
	expire = "";
	expire = new Date();
	expire.setTime(expire.getTime() - 1000000);
	expire = expire.toGMTString();
	document.cookie = name + "=" + escape(value) + ";expires=" + expire;
	
}

function shopQik(uid,mon,sm) {
	if (sm ==  2){
    dialog({
        title: 'ȷ�Ͽ�',
        content: '<font color=\"#ff0000\">�õ��ŷ���״̬Ϊ��ɨ��<br/>��δ��ѯ������,�����ѯ�������Ȳ�ѯ��<br/>�����ѯ������ֱ�ӵ��ȷ������</font>',
        button: [{
            value: 'ȷ��',
            callback: function() {
				 if(confirm("������˵�����Ҫ"+mon+"Ԫ����ȷ��Ҫ����")==true)
   					{
    				gm(uid,mon);
   					}
                
            },
            autofocus: true
        },
        {
            value: 'ȡ��'
        }]
    }).showModal();		
		}else{
    dialog({
        title: 'ȷ�Ͽ�',
        content: '������˵�����Ҫ'+mon+'Ԫ����ȷ��Ҫ����',
        button: [{
            value: 'ȷ��',
            callback: function() {
                gm(uid,mon);
            },
            autofocus: true
        },
        {
            value: 'ȡ��'
        }]
    }).showModal();

    function gm(uid,mon) {
        $.ajax({
            type: 'post',
            url: 'Refund.asp?qi=Shop',
            dataType: 'html',
            data: {"uid": uid,"mon": mon},
            timeout: 0,
            cache: false,
            error: err,
            success: suc
        })
        function err() {
            var s = dialog({
                title: '�Ե�����,��ʾ��',
                content: '����'
            });
            s.show();
        }
        function suc(str) {
            if (str == "Success") {
                if ($("#qindex").val() == "1") {
                    var s = dialog({
                        title: '�Ե�����,��ʾ��',
                        content: "����ɹ�,�뵽���ѹ��򵥺š�ҳ��鿴��",
                        cancel: function() {
                            location.reload();
                        },
                        cancelDisplay: false
                    });
                    s.show();
                    setTimeout(function() {
                        location.reload();
                        s.close().remove();
                    },
                    2000);

                } else {
                    var s = dialog({
                        title: '�Ե�����,��ʾ��',
                        content: '����ɹ�,�뵽���ѹ��򵥺š�ҳ��鿴��',
                        cancel: function() {
                            shopshowre(readCookie("p"),1);
                        },
                        cancelDisplay: false
                    });
                    s.show();
                    setTimeout(function() {
                        shopshowre(readCookie("p"),1);
                        s.close().remove();
                    },
                    2000);

                }

            } else if (str == "moneyerror") {
                var s = dialog({
                    title: '�Ե�����,��ʾ��',
                    content: '���ǱҲ��㣬�������ȳ�ֵ��'
                });
                s.show();
                setTimeout(function() {
                    s.close().remove();
                },
                2000);

            } else if (str == "Errorord") {
                var s = dialog({
                    title: '�Ե�����,��ʾ��',
                    content: '�˵����ѱ�������Ա����'
                });
                s.show();
                setTimeout(function() {
                    s.close().remove();
                },
                2000);

            }else if (str == "errorlogin") {
             alert('����ǰ��û�е�¼,�����ȵ�¼��');location.href='../login'
        }

    }

  }
 }
}



function qigm() {
		var temp = document.getElementsByName("id");
		var ii = 0;
		for (i = 0; i < temp.length; i++) {
			if (temp[i].checked) {
				var ii = ii + 1;
			}
		}
	dialog({
		title: 'ȷ�Ͽ�',
		content: '��ȷ������������ѡ��� '+ii+' ����',
		button: [{
			value: 'ȷ��',
			callback: function() {
				gmm();
			},
			autofocus: true
		}, {
			value: 'ȡ��'
		}]
	}).show();

	function gmm() {

		var temp = document.getElementsByName("id");
		var ii = 0;
		for (i = 0; i < temp.length; i++) {
			if (temp[i].checked) {
				var ii = ii + 1;
			}
		}
		if (ii < 1) {
			alert("��ѡ��");
			return;
		}
		var qiid = '';
		for (i = 0; i < temp.length; i++) {
			if (temp[i].checked) {
				qiid += temp[i].value + '.';
			}
		}

		$.ajax({
			type: 'post',
			url: 'Refund.asp?qi=Shopism',
			dataType: 'html',
			data: {
				id: qiid,
				ii: ii
			},
			timeout: 0,
			cache: false,
			error: err,
			success: suc
		})

		function err() {
			var s = dialog({
				title: '�Ե�����,��ʾ��',
				content: '���������ԡ�'
			});
			s.show();
			setTimeout(function() {
				s.close().remove();
			}, 2000);
		}

		function suc(str) {

			if (str == "no") {
				var s = dialog({
					title: '�Ե�����,��ʾ��',
					content: '���ǱҲ��㣬�������ȳ�ֵ��'
				});
				s.show();
				setTimeout(function() {
					s.close().remove();
				}, 2000);
			} else if (str == "nn") {
				var s = dialog({
					title: '�Ե�����,��ʾ��',
					content: '�㹴ѡ�ĵ����ѱ�����, 2����Զ�ˢ����ҳ��'
				});
				s.show();
				setTimeout(function() {
					location.reload();
				}, 2000);
			} else if (str == "ns") {
				var s = dialog({
					title: '�Ե�����,��ʾ��',
					content: 'δ���ֹ�ѡ����ĵ���, 2����Զ�ˢ����ҳ��'
				});
				s.show();
				setTimeout(function() {
					location.reload();
				}, 2000);
			} else {
				if ($("#qindex").val() == "1") {
					var s = dialog({
						title: '�Ե�����,��ʾ��',
						content: str+"<br/> 2����Զ�Ϊ��ˢ�¡�",
						cancel: function() {
							location.reload();
						},
						cancelDisplay: false
					});
					s.show();
					setTimeout(function() {
						location.reload();
						s.close().remove();
					}, 2000);
				} else {
					var s = dialog({
						title: '�Ե�����,��ʾ��',
						content: str+"<br/> 2����Զ�Ϊ��ˢ�¡�",
						cancel: function() {
							shopshowre(readCookie("p"),1);
						},
						cancelDisplay: false
					});
					s.show();
					setTimeout(function() {
						shopshowre(readCookie("p"),1);
						s.close().remove();
					},2000);
				}
			}

		}


	}
}

$(function(){
if(readCookie("seller")!=""){
var sc = document.getElementById("seller").options;
for (var i=0; i<sc.length; i++) {
if (sc[i].value==readCookie("seller")) {
sc[i].selected=true;
break;
	}
  }
 
}
    
});  

function timer(time) {
    var btn = $("#select");
    btn.attr("disabled", true);  //��ť��ֹ���
    btn.val(time <= 0 ? "" : ("�ύ��ѯ (" + (time)+")" ));
    var hander = setInterval(function() {
        if (time <= 0) {
            clearInterval(hander); //�������ʱ
            btn.val("�ύ��ѯ");
            btn.attr("disabled", false);
            return false;
        }else {
            btn.val("�ύ��ѯ (" + (time--) +")");
        }
    }, 1000);
}


function sncx(str) {
var str = unescape(str)	
var s = dialog({
    title: '�Ե�����,��ʾ��',
    content: "�ռ�ʱ�䣺<br/>"+ str +"<br/> ����ϸ�ȶ�ɨ��ʱ�䣡",
    cancel: function() {
        s.close().remove();

    },
    cancelDisplay: false

});
s.showModal();;
setTimeout(function() {
    s.close().remove();

},
2000);
}

function Coss(com, id, f) {	
	 dialog({
		id: 'ccx',
		content: '���ڼ����,�����Եȣ�........'
	}).showModal();
      jc = dialog.get('ccx').title('�Ե�����,��ʾ��');	
	  
		$.ajax({
		type: 'get',
		url: 'Refund.asp?qi=noss',
		dataType: 'text',
		data: {
			ord: com,
			ordlx1: id,
		},
		timeout: 0,
		cache: false,
		error: err,
		success: suc
		
	}) 

	function err() {
	jc.close().remove();	
		var s = dialog({
			title: '�Ե�����,��ʾ��',
			content: '���ӿڲ�ѯ����,��ʱ���ɼ�⣡'
		});
		s.show();
	}
 function suc(str) {
	jc.close().remove();			
			if (str == 1){	
				var d = dialog({
					title: '�Ե�����,��ʾ��',
					content: '<font color=\"#FF0000\">�˵��Ų���ʹ��,��ɾ��,���Ok���²�ѯ��</font>',
					ok: function() {
						if (f==0){showre(readCookie("p"),1);};
						if (f==1){shopshowre(readCookie("p"),1);};
						if (f==2){location.reload();};
						}	
				});
				d.showModal();						
		 }
		 if(str == 0){
			 var d = dialog({
					title: '�Ե�����,��ʾ��',
					content: '<font color=\"#145887\">�˵��ŵ�ǰ������ʹ��,��������һ����������</font>',
					ok: function() {}	
				});
				d.showModal();
			 }
			 
		 if(str == 3){
			 var d = dialog({
					title: '�Ե�����,��ʾ��',
					content: '<font color=\"#ff6000\">ϵͳ������,��ѯ���ڷ�æ,�������¼�⣡</font>',
					ok: function() {}	
				});
				d.showModal();

			 } 

			if(str == "Error"){
			 var d = dialog({
					title: '�Ե�����,��ʾ��',
					content: '<font color=\"#ff0000\">ϵͳ���������ش���,����ϵ���߿ͷ������</font>',
					ok: function() {}	
				});
				d.showModal();

			 } 

			if(str == "sotime"){
			 var d = dialog({
					title: '�Ե�����,��ʾ��',
					content: '<font color=\"#a422ef\">������Ƶ��,ϵͳ���Ƽ��3����һ�Ρ�<br/>���Ժ��ڳ��Լ�������</font>',
					ok: function() {}	
				});
				d.showModal();

			 }   
	 }	 		 
 }
