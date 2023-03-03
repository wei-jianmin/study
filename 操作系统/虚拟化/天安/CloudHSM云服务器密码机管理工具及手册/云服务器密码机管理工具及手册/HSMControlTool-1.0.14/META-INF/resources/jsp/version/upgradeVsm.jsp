<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ include file="/common/ctx.jsp"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta charset="utf-8">
<meta name="renderer" content="webkit|ie-comp|ie-stand">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no" />
<meta http-equiv="Cache-Control" content="no-siteapp" />
<meta http-equiv="Access-Control-Allow-Origin" content="*" />
<LINK rel="Bookmark" href="favicon.ico" >
<LINK rel="Shortcut Icon" href="favicon.ico" />
<meta name="keywords" content="江南天安" />
<meta name="description" content="江南天安" />
<!--[if lt IE 9]>
<script type="text/javascript" src="js/lib/html5.js"></script>
<script type="text/javascript" src="js/lib/respond.min.js"></script>
<![endif]-->
<link rel="stylesheet" type="text/css" href="${ctx}/static/iconfont/1.0.8/iconfont.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/Ui/css/H-ui.min.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/Ui.admin/css/H-ui.admin.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/Ui.admin/skin/default/skin.css" id="skin" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/Ui.admin/css/style.css" />
<!--[if IE 6]>
<script type="text/javascript" src="js/lib/DD_belatedPNG_0.0.8a-min.js" ></script>
<script>DD_belatedPNG.fix('*');</script>
<![endif]-->
<title>升级VSM</title>
</head>
<body>
<article class="page-container">
	<form method="post" enctype="multipart/form-data" class="form form-horizontal" id="form-article-add">
	    <div class="row cl">
			<label class="form-label col-xs-3 col-sm-2" style="text-align:right;"><span class="c-red">*</span>升级文件：</label>
			<div class="formControls col-xs-8 col-sm-9">
				<input type="file" id="authFile" onchange="fileSelectedAuthFile()" name="authFile" style="visibility:hidden;width:10px;">
				<input type="button" style="float:left;font-size:12px;color:#fff;height:27px;"id="filebutton" value="上传升级文件" class="btn btn-primary radius" onclick="updateFile()">
				<input type="textfield" id="filepathAuthFile"  class="input-text"  readonly style="float:left;width:250px;height:27px;border-radius:3px;"  class="input-text" placeholder="请上传升级文件">
			</div>
		</div>
	    <div class="row cl">
			<label class="form-label col-xs-3 col-sm-2" style="text-align:right;">VSMID：</label>
			<div class="formControls col-xs-8 col-sm-9">
                <input value="${vsmid}" name="vsmid" id="vsmid" class="input-text" readonly="readonly"/>
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-3 col-sm-2" style="text-align:right;">版本号：</label>
			<div class="formControls col-xs-8 col-sm-9">
                <input value="${version}" name="version" id="version" class="input-text" readonly="readonly">
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-3 col-sm-2" style="text-align:right;"><span class="c-red">*</span>签名值：</label>
			<div class="formControls col-xs-8 col-sm-9">
                <input value="${digest}" name="digest" id="digest" class="input-text"  placeholder="请输入签名值">
			</div>
		</div>		
	    <div class="row cl">
			<div class="col-xs-8 col-sm-9 col-xs-offset-4 col-sm-offset-3">
				 <button onClick="upgradeVsm();" class="btn btn-primary radius" type="button">升级</button>
				 <button onClick="layer_close();" class="btn btn-default radius" type="button">取消</button>
			</div>
	    </div>
	</form>
</article>

<script type="text/javascript" src="${ctx}/lib/jquery/1.9.1/jquery.min.js"></script> 
<script type="text/javascript" src="${ctx}/lib/layer/2.1/layer.js"></script>
<script type="text/javascript" src="${ctx}/lib/laypage/1.2/laypage.js"></script> 
<script type="text/javascript" src="${ctx}/static/Ui/js/H-ui.js"></script> 
<script type="text/javascript" src="${ctx}/static/Ui.admin/js/H-ui.admin.js"></script>
<script type="text/javascript" src="${ctx}/common/common.js"></script>
<script type="text/javascript">
//点击上传按钮清空文件名
function updateFile(){
	$("#filepathAuthFile").val("");
	$("#authFile").val("");
	$("#authFile").click();
}
//授权文件名显示框
function fileSelectedAuthFile() {
   	var file = document.getElementById('authFile').files[0];
   	var filename=file.name;
   	var version = filename.split("_")[1].substring(0,filename.split("_")[1].length-4);
   	$("#version").val(version);
   	$("#filepathAuthFile").val(filename);
    	var fileType=filename.split(".")[1];
    	uploadFileAuthFile();
}
//授权文件选择框
   function uploadFileAuthFile() {
    var authFile = $("#authFile").val();
    if(authFile!=""&&authFile!=null){
      	var fd = new FormData();
      	fd.append("authFile", document.getElementById('authFile').files[0]);
      	var xhr = new XMLHttpRequest();
      	xhr.open("POST", "");//修改成自己的接口
      	xhr.send(fd);
     	}
   }
//导入授权文件
 function upgradeVsm() {
	var fileContext=$("#authFile").val();	
	var version = $("#version").val().trim();
	var digest = $("#digest").val().trim();
	if(fileContext==""||fileContext==null){
   		layer.msg("请选择授权文件！",{icon:7,time:2000});
   	    return false;
   	}
   	//判断升级文件大小
 	var file = document.getElementById('authFile').files[0];
    if(file.size>104857600){
       layer.msg("升级文件大于100M！", {icon:0,time:2000});
       return;
    } 
    //判断升级文件格式
    var fileType = file.name.substring(file.name.length-4,file.name.length);
    if(fileType!=".pup"){
       layer.msg('请上传.pup格式的文件！', {icon:7,time:2000});
   	   return false;
    }
	if(version.length<=0){
		layer.msg('版本不能为空', {icon:7,time:2000});
		return false;
	}
	if(digest.length<=0){
		layer.msg('摘要不能为空', {icon:7,time:2000});
		return false;
	}
	$("#form-article-add").ajaxSubmit(options);
} 
var options={
		type:"post",
		resetForm: true,
		url:"${ctx}/version/wholePackageUpgradeVsm.html",
		beforeSend:function(){
			layer.load(3); 
			layer.msg("升级中，请耐心等待！", {icon:16,time:60000});
		},
		success:function(data){
			layer.closeAll();
			if(data=="success"){
				layer.msg('升级中,请查看耗时任务!', {
					icon : 1,
					time : 2000
				}, function() {
					window.top.$("[data-title='耗时任务管理']").click();
					layer.load(2);
					window.parent.location.reload(); 
				});
			}else{
				layer.msg("VSM升级失败！", {icon:2,time:2000},function(){
					window.location.reload();
				});
			}
		},
		error:function(data){
			layer.closeAll();
			layer.msg("出错了！", {icon:5,time:2000});
		}
	};
</script> 
<!--/请在上方写此页面业务相关的脚本-->
</body>
</html>