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
<LINK rel="Bookmark" href="/favicon.ico" >
<LINK rel="Shortcut Icon" href="/favicon.ico" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui/css/H-ui.min.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/css/H-ui.admin.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/lib/Hui-iconfont/1.0.8/iconfont.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/lib/icheck/icheck.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/skin/default/skin.css" id="skin" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/css/style.css" />
<!--/meta 作为公共模版分离出去-->

<title>导入影像</title>
<meta name="keywords" content="H-ui.admin ">
<meta name="description" content="H-ui.admin ">
</head>
<body>
<nav class="breadcrumb"><i class="Hui-iconfont">&#xe67f;</i> 首页 
	<span class="c-gray en">&gt;</span> 数据影像管理
	<span class="c-gray en">&gt;</span> 导入影像
	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" >
	<i class="Hui-iconfont">&#xe68f;</i>
	</a>
</nav>
<article class="page-container">
	<form id="form-article-add" method="post" enctype="multipart/form-data" class="form form-horizontal">
	     <div class="row cl">
				<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>影像文件：</label>
				<input type="file" id="authFile" onchange="fileSelectedAuthFile()" name="authFile" style="visibility:hidden;" >
				<div class="formControls col-xs-4 col-sm-4">
					<input type="text" id="filepathAuthFile" readonly style="float:left;border-radius:3px;"class="input-text" placeholder="请上传影像文件">
				</div>
				<input type="button" style="float:left;font-size:12px;color:#fff;height:30px;"id="filebutton" value="上传影像文件" class="btn btn-primary radius" onclick="updateFile()">
		    </div> 
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3" style="text-align: right;"><span class="c-red">*</span>选择VSM：</label>
			<div class="formControls col-xs-4 col-sm-4">
				<input type="text" class="input-text" value="${vsmid}"  id="vsmid" name="vsmid" readonly="readonly" placeholder="请选择导出影像时的VSM">
			</div>
			<button onclick="selectParent();" class="btn btn-primary radius" id="selectPar" type="button">选择</button>
		</div>
		 
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>影像签名值：</label>
			<div class="formControls col-xs-4 col-sm-4">
				<input type="text" class="input-text" value="${sign}" id="sign" name="sign" placeholder="请输入导出影像时返回的数字签名">
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3">导入内容：</label>
			<div class="formControls col-xs-4 col-sm-4"> <span class="select-box">
				<select class="select" name="format" id="format" size="1" >
					<option value="1"<c:if test="${format=='1'}">selected</c:if>>影像</option>
					<option value="2"<c:if test="${format=='2'}">selected</c:if>>密钥</option>
				</select>
				</span> 
			</div>
		</div>
		<div class="row cl">
			<div class="col-xs-8 col-sm-9 col-xs-offset-4 col-sm-offset-3">
				 <button class="btn btn-primary radius"  onclick="importVsm()" type="button">导入</button>
			</div>
		</div>
	</form>
</article>

<!--_footer 作为公共模版分离出去--> 
<script type="text/javascript" src="${ctx}/lib/jquery/1.9.1/jquery.min.js"></script> 
<script type="text/javascript" src="${ctx}/lib/layer/2.1/layer.js"></script>
<script type="text/javascript" src="${ctx}/lib/laypage/1.2/laypage.js"></script> 
<script type="text/javascript" src="${ctx}/static/Ui/js/H-ui.js"></script> 
<script type="text/javascript" src="${ctx}/static/Ui.admin/js/H-ui.admin.js"></script> 
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
    	var fileType=filename.split(".")[1];
    	uploadFileAuthFile();
}
//影像文件选择框
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
//导入影像文件
 function importVsm() {
	var fileContext=$("#authFile").val();	
	var vsmid = $("#vsmid").val().trim();
	var sign = $("#sign").val().trim();
	var format = $("#format").val().trim();
	if(fileContext==""||fileContext==null){
   		layer.msg("请选择影像文件！",{icon:7,time:2000});
   	    return false;
   	}
	if(vsmid.length<=0){
		layer.msg('vsmId不能为空', {icon:7,time:2000});
		return false;
	}
	if(sign.length<=0){
		layer.msg('影像数字签名不能为空', {icon:7,time:2000});
		return false;
	}
   	//判断授权大小
 	var file = document.getElementById('authFile').files[0];
    	if(file.size>104857600){
        layer.msg("影像文件大于100M！", {icon:0,time:2000});
        return;
    }    
    if(file.name.split("_")[0]!="imagefile"){
    	layer.msg("请选择正确的影像格式文件！", {icon:0,time:2000});
        return;
    }
	$("#form-article-add").ajaxSubmit(options);
} 
var options={
		type:"post",
		resetForm: true,
		url:"${ctx}/image/importVsmImage.html",
		beforeSend:function(){
			layer.load(3); 
			layer.msg("导入中，请耐心等待！", {icon:16,time:60000});
		},
		success:function(data){
			layer.closeAll();
			if(data=="success"){
				layer.msg('导入影像中,请查看耗时任务!', {
					icon : 1,
					time : 2000
				}, function() {
					window.top.$("[data-title='耗时任务管理']").click();
				});
			} else if (data == "statusFail") {
				layer.msg("获取VSM状态失败", {icon : 2,time : 2000});
			} else if (data == "status") {
				layer.msg("VSM关闭,请重启再试", {icon : 2,time : 2000}, function() {
					layer.load(2);
					window.parent.location.reload();
				});
			}else{
				layer.msg("导入影像失败！", {icon:2,time:2000},function(){
					window.location.reload();
				});
			}
		},
		error:function(data){
			layer.msg("出错了！", {icon:5,time:2000});
		}
	};
/**
 * 选择VSM列表
 */
function selectParent(){
	 layer_show("选择VSM", '${ctx}/vsm/getVsmList.html?vsm=1','600','350');
} 
</script> 
</body>
</html>