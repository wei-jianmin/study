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
<meta name="keywords" content="tass" />
<meta name="description" content="tass" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/iconfont/1.0.8/iconfont.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/Ui/css/H-ui.min.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/Ui.admin/css/H-ui.admin.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/Ui.admin/skin/default/skin.css" id="skin" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/Ui.admin/css/style.css" />
<title>导入授权文件</title>
</head>
<body>
<!-- <nav class="breadcrumb"><i class="Hui-iconfont">&#xe67f;</i> 首页  -->
<!-- 	<span class="c-gray en">&gt;</span> HSM配置  -->
<!-- 	<span class="c-gray en">&gt;</span> 导入授权文件 -->
<!-- 	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" > -->
<!-- 	<i class="Hui-iconfont">&#xe68f;</i> -->
<!-- 	</a> -->
<!-- </nav> -->
<article class="page-container">
	<form id="form-article-add" method="post" enctype="multipart/form-data" class="form form-horizontal">	
		   <div class="row cl">
				<label class="form-label col-xs-3 col-sm-2" style="text-align:right;"><span class="c-red">*</span>请选择授权文件：</label>
				<div class="formControls col-xs-8 col-sm-9">
	                <input type="file" id="authFile" onchange="fileSelectedAuthFile()" name="authFile" style="visibility:hidden;width:10px;" >
					<input type="button" style="float:left;font-size:12px;color:#fff;height:27px;"id="filebutton" value="上传授权文件" class="btn btn-primary radius" onclick="updateFile()">
					<input type="textfield" id="filepathAuthFile" readonly style="float:left;width:250px;height:27px;border-radius:3px;"class="input-text" placeholder="请上传授权文件">
				</div>
		    </div>
		    <br/>
		    <div class="row cl" style="text-align: center;">
					<button onClick="authFileImport();" class="btn btn-primary radius" type="button">导入</button>
				    <button onClick="layer_close();" class="btn btn-default radius" type="button">取消</button>
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
   	$("#filepathAuthFile").val(filename);
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
function authFileImport() {
	var fileContext=$("#authFile").val();	
   	if(fileContext==""||fileContext==null){
   		layer.msg("请选择授权文件！",{icon:7,time:2000});
   	    return false;
   	}
   	//判断授权大小
 	var file = document.getElementById('authFile').files[0];
   	if(file.size>104857600){
       layer.msg("授权文件大于100M！", {icon:0,time:2000});
       return;
   	}    
  //判断文件格式
 	var fileSplitLenght = file.name.split(".").length;
  	var fileType = file.name.split(".")[fileSplitLenght-1];
  	if(fileType!="license"){
		layer.msg('请上传license格式的文件！', {icon:7,time:2000});
   		return false;
  	}
	$("#form-article-add").ajaxSubmit(options);
}

var options={
	type:"post",
	resetForm: true,
	url:"${ctx}/hsm/authFileImport.html",
	beforeSend:function(){
		layer.load(3); 
		layer.msg("导入中，请耐心等待！", {icon:16,time:60000});
	},
	success:function(data){
		layer.closeAll();
		if(data=="success"){
			layer.msg("导入授权文件成功！", {icon:1,time:2000},function(){
				window.location.reload();
			});
		}else{
			layer.msg("导入授权文件失败！", {icon:2,time:2000});
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