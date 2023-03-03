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
<!--[if lt IE 9]>
<script type="text/javascript" src="lib/html5.js"></script>
<script type="text/javascript" src="lib/PIE_IE678.js"></script>
<![endif]-->
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui/css/H-ui.min.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/css/H-ui.admin.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/lib/Hui-iconfont/1.0.8/iconfont.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/lib/icheck/icheck.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/skin/default/skin.css" id="skin" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/css/style.css" />
<title>Restful服务</title>
</head>
<body>
<!-- <nav class="breadcrumb"> -->
<!-- 	<i class="Hui-iconfont">&#xe67f;</i> 首页 -->
<!--  	<span class="c-gray en">&gt;</span> HSM管理 -->
<!--  	<span class="c-gray en">&gt;</span> Restful服务 -->
<!--  	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" > -->
<!--  		<i class="Hui-iconfont">&#xe68f;</i> -->
<!--  	</a> -->
<!-- </nav> -->
<article class="page-container">
	<form class="form form-horizontal" id="form-admin-add">
	<label class="form-label col-xs-4 col-sm-3">Restful服务状态：</label>
	   <input type="text" class="input-text" value="${status}" id="status" name="status" style="display:none"/>
		<span style="margin-left:15px;">
			<c:if test="${status=='0'}">关闭</c:if>
			<c:if test="${status=='1'}">开启</c:if>
		</span>&nbsp;&nbsp;
	  <input class="btn btn-success radius" type="button" value="" onclick="on();" id="change" name="change" style="margin-left:85px;width:80px;"/>	
		<br/><br/><br/>
	</form>
</article>
<script type="text/javascript" src="${ctx}/lib/jquery/1.9.1/jquery.min.js"></script> 
<script type="text/javascript" src="${ctx}/lib/layer/2.1/layer.js"></script>
<script type="text/javascript" src="${ctx}/lib/My97DatePicker/WdatePicker.js"></script> 
<script type="text/javascript" src="${ctx}/lib/datatables/1.10.0/jquery.dataTables.min.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui/js/H-ui.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui.admin/js/H-ui.admin.js"></script> 
<script type="text/javascript" src="${ctx}/common/common.js"></script>
<script type="text/javascript">
//进入页面首先判断从后台传入进来的状态
$(function(){
	var status = $("#status").val();
	var btnSubmit = document.getElementById("change");
	if(status=='1'){
		$("#status").val("0");
		$("#change").val("关闭");
		btnSubmit.setAttribute("class","btn btn-danger radius");
	}else{
		$("#status").val("1");
		$("#change").val("开启");
		btnSubmit.setAttribute("class","btn btn-success radius");
	}
});
//根据开关的按钮显示相应内容
function on(){
	var status = $("#status").val();
	$.ajax({
		url : "${ctx}/hsm/configRestful.html",
		type : 'POST',
		crossOrigin : true,
		dataType : 'text',
		cache : false,
		async : true,
		data : {
			"status" : status
		},
		success : function(data) {
			if(data=="startSuccess"){
				layer.msg('Restful服务开启成功!', {icon:1,time:2000},function() {	
// 					window.location.reload();
					window.location.href="${ctx}/hsm/systemManage.html?typeIndex=3";
				});
			}else if(data=="stopSuccess"){
				layer.msg('Restful服务关闭成功!', {icon:1,time:2000},function() {	
// 					window.location.reload();
					window.location.href="${ctx}/hsm/systemManage.html?typeIndex=3";
				});
			}else if(data=="startFail"){
				layer.msg('Restful服务开启失败', {icon:2,time:2000});
			}else if(data=="stopFail"){
				layer.msg('Restful服务关闭失败', {icon:2,time:2000});
			}
		} ,
		error:function(data){
			layer.msg('出错了', {icon:5,time:2000});
		}
	});
}
</script>
</body>
</html>