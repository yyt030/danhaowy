
<style>body{padding:0;margin:0;font-family:"微软雅黑",Verdana,Arial;font-size:12px}.upfile{cursor:pointer;direction:rtl;height:35px;opacity:0;width:70px;filter:alpha(opacity=0);position:absolute;top:0;left:0}#xxnb2{position:relative;cursor:pointer;display:inline-block;background:url(../images/stkb2.gif) repeat-x;color:#fff;border:0;padding:5px 15px;width:50px;text-decoration:none}</style>
<script>function Qpost(){var filename=document.getElementById("file").value;var mime=filename.toLowerCase().substr(filename.lastIndexOf("."));if(mime!=".csv"){alert("请选择csv格式的文件上传!");return false}else{document.getElementById("upfrm").submit()}};</script>
<form action="upload.asp" method="post" enctype="multipart/form-data" target="upload" id="upfrm"><a href="javascript:void(0);" id="xxnb2"><input type="file" id="file" name="file" class="upfile" onchange="Qpost();"/>导入文件</a></form>
