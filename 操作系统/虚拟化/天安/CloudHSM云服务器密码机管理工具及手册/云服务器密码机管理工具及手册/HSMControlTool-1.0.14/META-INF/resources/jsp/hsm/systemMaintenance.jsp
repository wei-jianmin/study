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

<title>系统维护</title>
<meta name="keywords" content="H-ui.admin ">
<meta name="description" content="H-ui.admin ">
</head>
<body>
    <nav class="breadcrumb">
		<i class="Hui-iconfont">&#xe67f;</i> 首页 
		<span class="c-gray en">&gt;</span> HSM管理
		<span class="c-gray en">&gt;</span> 系统维护
		<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" >
			<i class="Hui-iconfont">&#xe68f;</i>
		</a>
	</nav>
	<div class="page-container">	
		<div class="mt-20">
			<div class="cl pd-5 bg-1 bk-gray mt-20">
				<a class="btn btn-primary radius" onclick="upGrade()" href="javascript:;">HSM升级</a>
				
				<a class="btn btn-primary radius" onclick="importAuthFile('导入授权文件','${ctx}/hsm/importAuthFile.html','650','250')" href="javascript:;">
					<i class="Hui-iconfont">&#xe6f7;</i> 导入授权文件
				</a>
				<a class="btn btn-primary radius" onclick="restartHSM()" href="javascript:;">
					<i class="Hui-iconfont">&#xe6f7;</i> 重启密码机
				</a>

			</div>
		</div>	
	</div>
<!--_footer 作为公共模版分离出去--> 
<script type="text/javascript" src="${ctx}/lib/jquery/1.9.1/jquery.min.js"></script> 
<script type="text/javascript" src="${ctx}/lib/layer/2.1/layer.js"></script> 
<script type="text/javascript" src="${ctx}/lib/icheck/jquery.icheck.min.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui/js/H-ui.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui.admin/js/H-ui.admin.js"></script> 
<script type="text/javascript" src="${ctx}/common/common.js"></script>
<script type="text/javascript">
<!--服务升级-->
function upGrade(){
	layer_show("HSM升级", '${ctx}/version/toUpgradeHsm.html','600','300');
}
<!--导入授权文件-->
function importAuthFile(title,url,w,h){
	layer_show(title,url,w,h);
}
function restartHSM(){
	layer.confirm('系统将自动断开连接,确认要重启吗？', function(index) {
		$.ajax({
			url : "${ctx}/hsm/restartHSM.html",
			type : 'POST',
			crossOrigin : true,
			dataType : 'text',
			cache : false,
			async : true,
			data : {},
			success : function(data) {
				if(data=="success"){
					layer.msg('重启HSM成功!', {icon:1,time:2000},function() {	
						window.parent.location.href="${ctx}/signOut.html";
					});
				}else{
					layer.msg('重启HSM失败!', {icon:2,time:2000});
				}
			} ,
			error:function(data){
				layer.msg('出错了', {icon:5,time:2000});
			}
		});
	});
}
</script>
</body>
</html>