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
function showre(p, x) {
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
    } else {
        var radios = 1
    }
    // if(p==0 && x==0 ){if(code==""){alert("请填写验证码,验证码不能为空！");return false;}}
    if (sa == "" && sb == "") {
        alert("发货地址 和 收货地址 不能同时为空！\n\n 请您先任意选择一项收发货地址！");
        return false;
    }
    if (x == 0) {
        timer(3);
    }
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
    gethtml("imglist", "<div style='color:red;text-align:center;'><img src='/static/images/wait.gif'/>正在查询中。。。</div>");
    var url = "Qiso?sja=" + sja + "&sa=" + sa + "&sb=" + sb + "&kd=" + com + "&sm=" + sm + "&x=" + x + "&p=" + p + "&token=" + token + "&radios=" + radios + "&code=" + code;
    var lx = showhtml;
    //var csrftoken = $('meta[name=csrf-token]').attr('content');
    xmlHttp = GetXmlHttpObject(lx)
    xmlHttp.open("GET", url, true)
    //xmlHttp.setRequestHeader("Content-Type", "text/xml; charset=utf-8")
    xmlHttp.send(null)
}

function showhtml() {
    if (xmlHttp.readyState == 4 || xmlHttp.readyState == "complete") {


        var Nums = xmlHttp.responseXML.getElementsByTagName("data")[0].getAttribute('Nums');
        xmltitle = xmlHttp.responseXML.getElementsByTagName("title")
        xmlfh = xmlHttp.responseXML.getElementsByTagName("fh")
        xmlsh = xmlHttp.responseXML.getElementsByTagName("sh")
        var imglist = "<TABLE class='table table-bordered table-condensed table-striped' style='font-size: 12px;'><THEAD><TR><TH align='center' style='text-align: center; width:7%;'>序号</TH><TH align='center' style='text-align: center; width:12%;'>快递单号</TH><TH align='center' style='text-align: center; width:10%;'>快递类型</TH><TH align='center' style='text-align: center; width:41%;'>发货地址/收货地址</TH><TH align='center' style='text-align: center; width:19%;'>扫描时间</TH><TH style='text-align: center; width:8%;'>领取操作</TH><TH align='center' style='text-align: center; width:3%;'><input type='checkbox' id='chkAll'  value='checkbox' style='border:0' onClick=checkAll()><input id='qindex' type='hidden' value='0'/></TH></TR></THEAD><TBODY>";
        for (i = 0; i < xmltitle.length; i++) {
            var title = xmltitle[i].firstChild.data;
            var jh = xmltitle[i].getAttribute("jh");
            if (title == "loginerror") {
                gethtml("imglist", "<div style='color:red;text-align:center;'><img src='/static/images/error_01.png'/>登录已经失效,请重新登录！</div>");
            }
            if (title == "tokenerror") {
                gethtml("imglist", "<div style='color:red;text-align:center;'><img src='/static/images/error_01.png'/>提交失败,请重新提交查询！</div>");
            }
            if (jh == 0) {
                gethtml("jhs", "<div style='color:red;text-align:center;margin-top: 10px;margin-bottom: 15px;'>您好，您当前帐号没有激活,查询只显示10条单号。帐号激活后,查询显示所有单号。<a href='wybjihuo'><img src='/static/images/jihuo.gif'  border='0' align='top' title='点击此按钮激活帐号' /></a></div>");
            }
            if (title == "没有") {
                imglist = "<div style='color:red;text-align:center;margin-top: 10px;margin-bottom: 15px;'><img src='/static/images/error_01.png'/>未查找到,请扩大查找范围! <br /><br />未查找到? 建议您尝试发空包！<a href='buykongbao' target='_blank' class='btn'>我要发空包</a></div>";
                gethtml("imglist");
            } else if (title == "timererror") {
                imglist = "<div style='color:red;text-align:center;'><img src='/static/face/018.gif'/>压力山大，由于您查询过于频繁,请歇歇,预计3秒内可再次查询！</div>";
                gethtml("imglist");
            } else if (title == "codeerror") {
                imglist = "<div style='color:red;text-align:center;'><img src='/static/images/error_01.png'/>您输入的验证码错误,请重新输入后在提交查询!</div>";
                $("#code").val("");
                getcode();
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
                if (cc == 0) {
                    imglist += "<td style='line-height: 40px;'>" + htmlid + " </td>";
                } else {
                    imglist += "<td style='line-height: 40px;'>" + htmlid + " <input name=\"COSS\" type=\"button\" onclick=\"Coss(" + Qid + ",'" + cc + "',0);\" value=\"检测\" class=\"zdybutton\"></td>";
                }
                imglist += "<td style='line-height: 40px;text-align:center;'>" + title + "</td>";
                imglist += "<td style='text-align: center;'>发货地址：" + fh + "<br/><font color=#EE5C42>收货地址：" + sh + "</font></td>";
                if (sm == 0 || sm == 2 ||sm == 1) {
                    imglist += "<td style='color: #1E90FF;line-height: 40px;text-align:center;' id='qs" + Qid + "'>点击查询<a href='javascript:' title='点击查询状态' onClick=Qikd('" + kda + "',1,'" + Qid + "','0')><img src='/static/images/so.jpg'></a></td>"
                    imglist += "<td style='text-align: center;'><input type='button' id='fs" + Qid + "' class='btnumey' value='领  取' onClick=Qik('" + Qid + "','" + sm + "') style='cursor:hand;margin-top: 9px'></td>";
                } else {
                    imglist += "<td style='line-height: 40px;'><font color='red'>" + sm + "</font><a href='javascript:' title='点击查询状态' onClick=sncx('" + escape(sm) + "&nbsp;" + escape(saomiaotxt) + "')><img src='/static/images/so.jpg'></a></td>";
                    imglist += "<td style='text-align: center;'><input type='button' class='btnumey' value='领  取' onClick=Qik('" + Qid + "','" + escape(sm) + "') style='cursor:hand;margin-top: 9px'></td>";
                }
                imglist += "<TD style='text-align:center;'><span class='qiall'><input id='Qidd' type='checkbox' name='Qidd' value='" + Qid + "' style='margin-top: 12px'></span></TD>";
                imglist += "</tr>";
            }
        }
        if (P_Nums > 1) {
            var Plist = "<tr><td colspan='9'><div id='page'><ul>";
            if (page < 2) {
                Plist += "<li><span>首　页</span></li><li><span>上一页</span></li>"
            } else {
                Plist += "<li><a href='javascript:' onclick=showre(1,1) title='首　页'>首　页</a></li><li><a href='javascript:' onclick=showre(" + (page - 1) + ",1) title='上一页'>上一页</a></li>"
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
                Plist += "<li><span>下一页</span></li><li><span>末　页</span></li>"
            } else {
                Plist += "<li><a href='javascript:' onclick=showre(" + (page * 1 + 1) + ",1) title='下一页'>下一页</a></li><li><a href='javascript:' onclick=showre(" + P_Nums + ",1) title='末　页'>末　页</a></li>"
            }
            Plist += "</ul></div></td></tr></TBODY></TABLE>"
        } else {
            var Plist = "</TBODY></TABLE>";
        }
        gethtml("imglist", imglist + Plist)

        //if (imglist.indexOf("查询") > 0 ){$("#code").val("");getcode();}
    }
}


function shopshowre(p, x) {
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
    } else {
        var radios = 1
    }
    //if(p==0 && x==0 ){if(code==""){alert("请填写验证码,验证码不能为空！");return false;}}
    if (sa == "" && sb == "") {
        alert("发货地址 和 收货地址 不能同时为空！\n\n 请您先任意选择一项收发货地址！");
        return false;
    }
    if (x == 0) {
        timer(3);
    }
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
    gethtml("imglist", "<div style='color:red;text-align:center;'><img src='/static/images/wait.gif'/>正在查询中。。。</div>");
    var url = "ShopQiso?sja=" + sja + "&sa=" + sa + "&sb=" + sb + "&kd=" + com + "&sm=" + sm + "&p=" + p + "&seller=" + seller + "&token=" + token + "&radios=" + radios + "&code=" + code;
    var lx = shopshowhtml;
    xmlHttp = GetXmlHttpObject(lx)
    xmlHttp.open("GET", url, true)
    xmlHttp.send(null)
}

function shopshowhtml() {
    if (xmlHttp.readyState == 4 || xmlHttp.readyState == "complete") {
        var Nums = xmlHttp.responseXML.getElementsByTagName("data")[0].getAttribute('Nums');
        xmltitle = xmlHttp.responseXML.getElementsByTagName("title");
        console.log(xmltitle[0].firstChild.data);
        xmlfh = xmlHttp.responseXML.getElementsByTagName("fh")
        xmlsh = xmlHttp.responseXML.getElementsByTagName("sh")
        var imglist = "<TABLE class='table table-bordered table-condensed table-striped'style='font-size: 12px;'><THEAD><TR><TH align='center'style='text-align:center;'width='7%'>序号</TH><TH align='center'style='text-align:center;'width='12%'>快递单号</TH><TH align='center'style='text-align:center;'width='9%'>快递类型</TH><TH align='center'style='text-align:center;'width='29%'>发货地址/收货地址</TH><TH align='center'style='text-align:center;'width='8%'>单价</TH><TH align='center'style='text-align:center;'width='17%'>扫描时间</TH><TH align='center'style='text-align:center;'width='7%'>发布方</TH><TH align='center'style='text-align:center;'width='12%'>全选/反选<input type='checkbox'id='chkAll'value='checkbox'style='border:0'onClick='shopcheckAll()'><input id='qindex'type='hidden'value='0'/></TH></TR></THEAD><TBODY>";
        for (i = 0; i < xmltitle.length; i++) {
            var title = xmltitle[i].firstChild.data;
            var jh = xmltitle[i].getAttribute("jh");
            if (title == "loginerror") {
                gethtml("imglist", "<div style='color:red;text-align:center;'><img src='/static/images/error_01.png'/>登录已经失效,请重新登录！</div>");
            }
            if (title == "tokenerror") {
                gethtml("imglist", "<div style='color:red;text-align:center;'><img src='/static/images/error_01.png'/>提交失败,请重新提交查询！</div>");
            }
            if (title == "没有") {
                imglist = "<div style='color:red;text-align:center;margin-top: 10px;margin-bottom: 15px;'><img src='/static/images/error_01.png'/>未查找到,请扩大查找范围2!  <br /><br />未查找到? 建议您尝试发空包！<a href='buykongbao' target='_blank' class='btn'>我要发空包</a></div>";
                gethtml("imglist");
            } else if (title == "timererror") {
                imglist = "<div style='color:red;text-align:center;'><img src='face/018.gif'/>压力山大，由于您查询过于频繁,请歇歇,预计3秒内可再次查询！</div>";
                gethtml("imglist");
            } else if (title == "codeerror") {
                imglist = "<div style='color:red;text-align:center;'><img src='/static/images/error_01.png'/>您输入的验证码错误,请重新输入后在提交查询!</div>";
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

                imglist += "<tr id='yc" + Qid + "'>";
                imglist += "<td style='line-height: 40px;text-align:center;'>" + Qoi + "</td>";
                if (cc == 0) {
                    imglist += "<td style='line-height: 40px;'>" + htmlid + " </td>";
                } else {
                    imglist += "<td style='line-height: 40px;'>" + htmlid + " <input name=\"COSS\" type=\"button\" onclick=\"Coss(" + Qid + ",'" + cc + "',1);\" value=\"检测\" class=\"zdybutton\"></td>";
                }
                imglist += "<td style='line-height: 40px;text-align:center;'>" + title + "</td>";
                imglist += "<td style='text-align: center;'>发货地址：" + fh + "<br/><font color=#EE5C42>收货地址：" + sh + "</font></td>";
                imglist += "<td style='color:#2E2EFE;line-height: 40px;text-align:center;' id='nn" + Qid + "'>" + shopmoney + "/元</td>";
                if (sm == 0 || sm == 2 || sm == 1) {
                    imglist += "<td style='color: #1E90FF;line-height: 40px;text-align:center;' id='qs" + Qid + "'>点击查询<a href='javascript:' title='录入时间：" + Time + "' onClick=Qikd('" + kda + "',1,'" + Qid + "','1')><img src='/static/images/so.jpg'></a></td>"
                } else {
                    imglist += "<td style='line-height: 40px;text-align:center;'><font color='red'>" + sm + "</font><a href='javascript:' title='点击查询状态' onClick=sncx('" + escape(sm) + "&nbsp;" + escape(saomiaotxt) + "')><img src='/static/images/so.jpg'></a></td>";
                }
                if (shopuser == 0) {
                    imglist += "<td style='color:#603;line-height: 40px;text-align:center;'>管理员</td>";
                } else {
                    imglist += "<td style='color:#ea00ff;line-height: 40px;text-align:center;'>" + shopuser + "</td>";

                }
                if (sm == 2) {
                    imglist += "<td style='line-height: 40px;text-align:center;'><a href='javascript:' id='gm" + Qid + "' onclick='shopQik(" + Qid + "," + shopmoney + ",2)' style='cursor:hand;'>立即购买</a> <span class='qiall'><input id='id' type='checkbox' name='id' value='" + Qid + "'></span></td>";
                } else {
                    imglist += "<td style='line-height: 40px;text-align:center;'><a href='javascript:' id='gm" + Qid + "' onclick='shopQik(" + Qid + "," + shopmoney + ")' style='cursor:hand;'>立即购买</a> <span class='qiall'><input id='id' type='checkbox' name='id' value='" + Qid + "'></span></td>";
                }

                imglist += "</tr>";
            }
        }
        if (P_Nums > 1) {
            var Plist = "<tr><td colspan='9'><div id='page'><ul>";
            if (page < 2) {
                Plist += "<li><span>首　页</span></li><li><span>上一页</span></li>"
            } else {
                Plist += "<li><a href='javascript:' onclick=shopshowre(1,1) title='首　页'>首　页</a></li><li><a href='javascript:' onclick=shopshowre(" + (page - 1) + ",1) title='上一页'>上一页</a></li>"
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
                Plist += "<li><span>下一页</span></li><li><span>末　页</span></li>"
            } else {
                Plist += "<li><a href='javascript:' onclick=shopshowre(" + (page * 1 + 1) + ",1) title='下一页'>下一页</a></li><li><a href='javascript:' onclick=shopshowre(" + P_Nums + ",1) title='末　页'>末　页</a></li>"
            }
            Plist += "</ul></div></td></tr></TBODY></TABLE>"
        } else {
            var Plist = "</TBODY></TABLE>";
        }
        gethtml("imglist", imglist + Plist)

        //if (imglist.indexOf("查询") > 0 ){$("#code").val("");getcode();}

    }
}

function topip(randomFlag, min, max) {
    var str = "",
        range = min,
        arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];

    // 随机产生
    if (randomFlag) {
        range = Math.round(Math.random() * (max - min)) + min;
    }
    for (var i = 0; i < range; i++) {
        pos = Math.round(Math.random() * (arr.length - 1));
        str += arr[pos];
    }
    var date = new Date();
    date.setTime(date.getTime() + 10000);
    document.cookie = "Tokenkey" + "=" + escape(str) + "; expires=" + date.toGMTString() + "; path=/";
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
        alert('批量领取至少选择2单,如你还没有查询,请先查询！');
        return;
    }
    if (idlen > 20) {
        alert('每次最多领取20单,领取后可重新勾选领取！');
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
    location = "BatchGetNumber?" + Qiids + "";
}

function Qik(uid, sm) {
    if (sm == 2) {
        var d = dialog({
            title: '淘单无忧,提示您',
            content: '该单号已扫描,但未查询过物流,你可以先查询物流！<br/>您确定要领取吗,领取后不可退单哦？',
            okValue: '确定',
            ok: function () {
                var url = "GetNumber?uid=" + uid;
                location = url;
                return false;
            },
            cancelValue: '取消',
            cancel: function () {
            }
        });
        d.show();
    } else {
        if (sm != 0) {
            var sm = unescape(sm)
            var d = dialog({
                title: '淘单无忧,提示您',
                content: '该单号已扫描,领取前请先比对扫描时间！<br/>扫描时间：' + sm + '<br/>您确定要领取吗,领取后不可退单哦？',
                okValue: '确定',
                ok: function () {
                    var url = "GetNumber?uid=" + uid;
                    location = url;
                    return false;
                },
                cancelValue: '取消',
                cancel: function () {
                }
            });
            d.show();
        }
        else {
            var url = "GetNumber?uid=" + uid;
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
        var ids = $("input[name='Qidd']");
        for (var i = 0; i < ids.length; i++) {
            if (ids[i].checked == true) {
                ids[i].checked = "";
            } else {
                ids[i].checked = "checked";
            }
        }
    } else {
        $(".qiall input").attr("checked", false);
    }
}


function shopcheckAll() {
    if ($("#chkAll").is(":checked")) {
        var ids = $("input[name='id']");
        for (var i = 0; i < ids.length; i++) {
            if (ids[i].checked == true) {
                ids[i].checked = "";
            } else {
                ids[i].checked = "checked";
            }
        }
    } else {
        $(".qiall input").attr("checked", false);
    }
}


function gethtml(name, lx) {
    document.getElementById(name).innerHTML = lx;
}

function get(name) {
    return document.getElementById(name).value;
}

function Qikd(com, id, qid, i) {
    var csrftoken = $('meta[name=csrf-token]').attr('content')
    //xhr.setRequestHeader("X-CSRFToken", csrftoken);
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })
    if (id == "0") {
        var q = 1;
    } else {
        var q = 0;
    }
    if (i == "0") {
        $.ajax({
            type: 'post',
            url: 'Qikd',
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
    } else {
        $.ajax({
            type: 'post',
            url: 'Qikd',
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
        content: '正在努力查询中........'
    }).showModal();
    uu = dialog.get('ccx').title('淘单无忧,提示您');
    setInterval(function () {
        if (DQCookie("qi" + qid) != -1) {
            uu.close().remove();
            delCookie("qi" + qid, "1")

        }

    }, 100);


    function err() {
        writeCookie("qi" + qid, "1", "1");
        var s = dialog({
            title: '淘单无忧,提示您',
            content: '查询错误！'
        });
        s.show();
    }

    function suc(str) {
        writeCookie("qi" + qid, "1", "1");
        uu.close().remove();
        if (q == "1") {
            dialog({
                title: '物流信息',
                content: str
            }).show();
        } else {
            if (str == 0) {
                uu.close().remove();
                var d = dialog({
                    title: '淘单无忧,提示您',
                    content: '<font color=\"#006600\">Y(^_^)Y 该单号安全暂未扫描,请放心使用。</font>',
                    ok: function () {
                    }
                });
                d.showModal();
            } else {

                if (str == 2) {
                    uu.close().remove();
                    var d = dialog({
                        title: '淘单无忧,提示您',
                        content: '<font color=\"#FF0000\">该单号未在规定的32小时内扫描,请您谨慎领取。</font>',
                        ok: function () {
                        }

                    });
                    d.showModal();
                } else {
                    uu.close().remove();
                    var str = str.split(",")
                    var d = dialog({
                        title: '淘单无忧,提示您',
                        content: '<font color=\"#FF0000\">-_-。sorry！ 该单号已扫描,请仔细比对时间。<br/>收件时间：<br/>' + str[0] + ' ' + str[1] + '</font>',
                        ok: function () {
                            $("#fs" + qid).attr("onclick", "Qik('" + qid + "','" + escape(str[0]) + "')");
                            $("#qs" + qid).html("<font color=\"#FF0000\">" + str[0] + "</font><a href=\"javascript:\" title=\"点击查询状态\" onclick=\"sncx('" + str[0] + " " + str[1] + "')\"><img src=\"/static/images/so.jpg\"></a>");


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
                title: '物流信息',
                content: str
            }).show();
        } else {
            if (str == 0) {
                uu.close().remove();
                var d = dialog({
                    title: '淘单无忧,提示您',
                    content: '<font color=\"#006600\">Y(^_^)Y 该单号安全暂未扫描,请放心使用。</font>',
                    ok: function () {
                    }
                });
                d.showModal();
            } else {

                if (str == 2) {
                    uu.close().remove();
                    var d = dialog({
                        title: '淘单无忧,提示您',
                        content: '<font color=\"#FF0000\">该单号未在规定的32小时内扫描,请您谨慎领取。</font>',
                        ok: function () {
                        }

                    });
                    d.showModal();
                } else {
                    uu.close().remove();
                    var str = str.split(",")
                    var d = dialog({
                        title: '淘单无忧,提示您',
                        content: '<font color=\"#FF0000\">-_-。sorry！ 该单号已扫描,请仔细比对时间。<br/>收件时间：<br/>' + str[0] + ' ' + str[1] + '</font>',
                        ok: function () {

                            $("#qs" + qid).html("<font color=\"#FF0000\">" + str[0] + "</font><a href=\"javascript:\" title=\"点击查询状态\" onclick=\"sncx('" + str[0] + " " + str[1] + "')\"><img src=\"/static/images/so.jpg\"></a>");
                            nus = $("#nn" + qid).html();
                            nus = nus.replace('/元', '')
                            if (nus != "0.25") {
                                nus = nus / 2;
                                $("#nn" + qid).html(nus + '/元');
                            }
                            $("#gm" + qid).attr("onclick", "shopQik('" + qid + "','" + nus + "')");


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
    alert("复制成功");
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
    var nn = "";
    nn = document.cookie.indexOf(name)
    return nn;
}


function delCookie(name, value) {
    expire = "";
    expire = new Date();
    expire.setTime(expire.getTime() - 1000000);
    expire = expire.toGMTString();
    document.cookie = name + "=" + escape(value) + ";expires=" + expire;

}

function shopQik(uid, mon, sm) {
    if (sm == 2) {
        dialog({
            title: '确认框',
            content: '<font color=\"#ff0000\">该单号发布状态为已扫描<br/>但未查询过物流,如需查询物流请先查询！<br/>无需查询物流可直接点击确定购买！</font>',
            button: [{
                value: '确定',
                callback: function () {
                    if (confirm("您购买此单号需要" + mon + "元，您确认要购买？") == true) {
                        gm(uid, mon);
                    }

                },
                autofocus: true
            },
                {
                    value: '取消'
                }]
        }).showModal();
    } else {
        dialog({
            title: '确认框',
            content: '您购买此单号需要' + mon + '元，您确认要购买？',
            button: [{
                value: '确定',
                callback: function () {
                    gm(uid, mon);
                },
                autofocus: true
            },
                {
                    value: '取消'
                }]
        }).showModal();

        function gm(uid, mon) {
            var csrftoken = $('meta[name=csrf-token]').attr('content')
            //xhr.setRequestHeader("X-CSRFToken", csrftoken);
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken)
                    }
                }
            })
            $.ajax({
                type: 'post',
                url: 'Refund?qi=Shop',
                dataType: 'html',
                data: {"uid": uid, "mon": mon},
                timeout: 0,
                cache: false,
                error: err,
                success: suc
            })
            function err() {
                var s = dialog({
                    title: '淘单无忧,提示您',
                    content: '错误！'
                });
                s.show();
            }

            function suc(str) {
                if (str == "Success") {
                    if ($("#qindex").val() == "1") {
                        var s = dialog({
                            title: '淘单无忧,提示您',
                            content: "购买成功,请到【已购买单号】页面查看！",
                            cancel: function () {
                                location.reload();
                            },
                            cancelDisplay: false
                        });
                        s.show();
                        setTimeout(function () {
                                location.reload();
                                s.close().remove();
                            },
                            2000);

                    } else {
                        var s = dialog({
                            title: '淘单无忧,提示您',
                            content: '购买成功,请到【已购买单号】页面查看！',
                            cancel: function () {
                                shopshowre(readCookie("p"), 1);
                            },
                            cancelDisplay: false
                        });
                        s.show();
                        setTimeout(function () {
                                shopshowre(readCookie("p"), 1);
                                s.close().remove();
                            },
                            2000);

                    }

                } else if (str == "moneyerror") {
                    var s = dialog({
                        title: '淘单无忧,提示您',
                        content: '无忧币不足，购买请先充值。'
                    });
                    s.show();
                    setTimeout(function () {
                            s.close().remove();
                        },
                        2000);

                } else if (str == "Errorord") {
                    var s = dialog({
                        title: '淘单无忧,提示您',
                        content: '此单号已被其他会员购买。'
                    });
                    s.show();
                    setTimeout(function () {
                            s.close().remove();
                        },
                        2000);

                } else if (str == "errorlogin") {
                    alert('您当前还没有登录,请您先登录！');
                    location.href = '../login'
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
        title: '确认框',
        content: '您确认批量购买已选择的 ' + ii + ' 单？',
        button: [{
            value: '确定',
            callback: function () {
                gmm();
            },
            autofocus: true
        }, {
            value: '取消'
        }]
    }).show();

    function gmm() {
        var csrftoken = $('meta[name=csrf-token]').attr('content')
        //xhr.setRequestHeader("X-CSRFToken", csrftoken);
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
        })
        var temp = document.getElementsByName("id");
        var ii = 0;
        for (i = 0; i < temp.length; i++) {
            if (temp[i].checked) {
                var ii = ii + 1;
            }
        }
        if (ii < 1) {
            alert("请选择！");
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
            url: 'Refund?qi=Shopism',
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
                title: '淘单无忧,提示您',
                content: '错误，请重试。'
            });
            s.show();
            setTimeout(function () {
                s.close().remove();
            }, 2000);
        }

        function suc(str) {

            if (str == "no") {
                var s = dialog({
                    title: '淘单无忧,提示您',
                    content: '无忧币不足，购买请先充值。'
                });
                s.show();
                setTimeout(function () {
                    s.close().remove();
                }, 2000);
            } else if (str == "nn") {
                var s = dialog({
                    title: '淘单无忧,提示您',
                    content: '你勾选的单号已被购买, 2秒后自动刷新网页。'
                });
                s.show();
                setTimeout(function () {
                    location.reload();
                }, 2000);
            } else if (str == "ns") {
                var s = dialog({
                    title: '淘单无忧,提示您',
                    content: '未发现勾选购买的单号, 2秒后自动刷新网页。'
                });
                s.show();
                setTimeout(function () {
                    location.reload();
                }, 2000);
            } else {
                if ($("#qindex").val() == "1") {
                    var s = dialog({
                        title: '淘单无忧,提示您',
                        content: str + "<br/> 2秒后自动为您刷新。",
                        cancel: function () {
                            location.reload();
                        },
                        cancelDisplay: false
                    });
                    s.show();
                    setTimeout(function () {
                        location.reload();
                        s.close().remove();
                    }, 2000);
                } else {
                    var s = dialog({
                        title: '淘单无忧,提示您',
                        content: str + "<br/> 2秒后自动为您刷新。",
                        cancel: function () {
                            shopshowre(readCookie("p"), 1);
                        },
                        cancelDisplay: false
                    });
                    s.show();
                    setTimeout(function () {
                        shopshowre(readCookie("p"), 1);
                        s.close().remove();
                    }, 2000);
                }
            }

        }


    }
}

$(function () {
    if (readCookie("seller") != "") {
        var sc = document.getElementById("seller").options;
        for (var i = 0; i < sc.length; i++) {
            if (sc[i].value == readCookie("seller")) {
                sc[i].selected = true;
                break;
            }
        }

    }

});

function timer(time) {
    var btn = $("#select");
    btn.attr("disabled", true);  //按钮禁止点击
    btn.val(time <= 0 ? "" : ("提交查询 (" + (time) + ")" ));
    var hander = setInterval(function () {
        if (time <= 0) {
            clearInterval(hander); //清除倒计时
            btn.val("提交查询");
            btn.attr("disabled", false);
            return false;
        } else {
            btn.val("提交查询 (" + (time--) + ")");
        }
    }, 1000);
}


function sncx(str) {
    var str = unescape(str)
    var s = dialog({
        title: '淘单无忧,提示您',
        content: "收件时间：<br/>" + str + "<br/> 请仔细比对扫描时间！",
        cancel: function () {
            s.close().remove();

        },
        cancelDisplay: false

    });
    s.showModal();
    ;
    setTimeout(function () {
            s.close().remove();

        },
        2000);
}

function Coss(com, id, f) {
    var csrftoken = $('meta[name=csrf-token]').attr('content')
    //xhr.setRequestHeader("X-CSRFToken", csrftoken);
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })
    dialog({
        id: 'ccx',
        content: '正在检测中,请您稍等！........'
    }).showModal();
    jc = dialog.get('ccx').title('淘单无忧,提示您');

    $.ajax({
        type: 'get',
        url: 'Refund?qi=noss',
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
            title: '淘单无忧,提示您',
            content: '检测接口查询错误,暂时不可检测！'
        });
        s.show();
    }

    function suc(str) {
        jc.close().remove();
        if (str == 1) {
            var d = dialog({
                title: '淘单无忧,提示您',
                content: '<font color=\"#FF0000\">此单号不可使用,已删除,点击Ok重新查询。</font>',
                ok: function () {
                    if (f == 0) {
                        showre(readCookie("p"), 1);
                    }
                    ;
                    if (f == 1) {
                        shopshowre(readCookie("p"), 1);
                    }
                    ;
                    if (f == 2) {
                        location.reload();
                    }
                    ;
                }
            });
            d.showModal();
        }
        if (str == 0) {
            var d = dialog({
                title: '淘单无忧,提示您',
                content: '<font color=\"#145887\">此单号当前可正常使用,您可以下一步操作啦！</font>',
                ok: function () {
                }
            });
            d.showModal();
        }

        if (str == 3) {
            var d = dialog({
                title: '淘单无忧,提示您',
                content: '<font color=\"#ff6000\">系统检查程序,查询过于繁忙,请您重新检测！</font>',
                ok: function () {
                }
            });
            d.showModal();

        }

        if (str == "Error") {
            var d = dialog({
                title: '淘单无忧,提示您',
                content: '<font color=\"#ff0000\">系统检查程序严重错误,请联系在线客服解决！</font>',
                ok: function () {
                }
            });
            d.showModal();

        }

        if (str == "sotime") {
            var d = dialog({
                title: '淘单无忧,提示您',
                content: '<font color=\"#a422ef\">检测过于频繁,系统限制间隔3秒检测一次。<br/>请稍后在尝试检测操作！</font>',
                ok: function () {
                }
            });
            d.showModal();

        }
    }
}
