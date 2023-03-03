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
<LINK rel="Bookmark" href="/favicon.ico">
<LINK rel="Shortcut Icon" href="/favicon.ico" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui/css/H-ui.min.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/css/H-ui.admin.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/lib/Hui-iconfont/1.0.8/iconfont.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/lib/icheck/icheck.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/skin/default/skin.css" id="skin" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/css/style.css" />
<!--/meta 作为公共模版分离出去-->

<title>VSM状态管理</title>
<meta name="keywords" content="">
<meta name="description" content="">
</head>
<body>
	<article class="page-container">
	<form action="" method="post" class="form form-horizontal" id="form-member-add">
	
		<div class="row cl">
				<label class="form-label col-xs-3 col-sm-3" style="text-align: right;">
					vsmID：
				</label>
				<div class="formControls col-xs-8 col-sm-9">
					${vsmInfo.id}
				</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-3 col-sm-3" style="text-align: right;">
				VSM当前状态：
			</label>
			<div class="formControls col-xs-8 col-sm-9">
				<c:choose>
					<c:when test="${vsmInfo.status == 'ok'}">
						${vsmInfo.status} VSM运行中
					</c:when>
					<c:otherwise>
						${vsmInfo.status} VSM已关机
					</c:otherwise>
				</c:choose>
			</div>
		</div>
		<c:if test="${vsmInfo.status == 'ok'}">
			<div class="row cl">
				<label class="form-label col-xs-3 col-sm-3" style="text-align: right;">
					vsm类型：
				</label>
				<div class="formControls col-xs-8 col-sm-9">
					${vsmInfo.type}
				</div>
			</div>
			<div class="row cl">
				<label class="form-label col-xs-3 col-sm-3" style="text-align: right;">
					vsm版本号：
				</label>
				<div class="formControls col-xs-8 col-sm-9">
					${vsmInfo.version}
				</div>
			</div>
		
		</c:if>
				
		<div class="row cl">
			<div class="col-xs-8 col-sm-9 col-xs-offset-4 col-sm-offset-3">
				<c:choose>
					<c:when test="${vsmInfo.status == 'ok'}"> <!--开机状态  -->
						<button class="btn btn-primary radius" onclick="updateVsmStatus('${vsmInfo.id}', '${vsmInfo.status}','true')" type="button">停止</button>
						<button class="btn btn-primary radius" onclick="restart('${vsmInfo.id}')" type="button">重启</button>
						<button class="btn btn-primary radius" onclick="upgradeVsm('${vsmInfo.id}')" type="button">升级</button>
					</c:when>
					<c:otherwise>
						<button class="btn btn-primary radius" onclick="updateVsmStatus('${vsmInfo.id}', 'no' ,'false')" type="button">启动</button>
						<button class="btn btn-danger radius" onclick="deleteVSM('${vsmInfo.id}')" type="button">删除</button>
					</c:otherwise>
				</c:choose>
				<button class="btn btn-danger radius" onclick="resetVsm('${vsmInfo.id}')" type="button">重置</button>
			</div>
		</div>
		

	</form>
	</article>
	<!--_footer 作为公共模版分离出去-->
	<script type="text/javascript" src="${ctx}/lib/jquery/1.9.1/jquery.min.js"></script>
	<script type="text/javascript" src="${ctx}/lib/layer/2.1/layer.js"></script>
	<script type="text/javascript" src="${ctx}/lib/icheck/jquery.icheck.min.js"></script>
	<script type="text/javascript" src="${ctx}/static/h-ui/js/H-ui.js"></script>
	<script type="text/javascript" src="${ctx}/static/h-ui.admin/js/H-ui.admin.js"></script>
	<script type="text/javascript" src="${ctx}/common/common.js"></script>
	<!--/_footer /作为公共模版分离出去-->

	<!--请在下方写此页面业务相关的脚本-->
	<script type="text/javascript">
	//停用/启用
	function updateVsmStatus(vsmId, status, isOnline) {
		var confirmTips = "";
		var tips = "";
		var fail = "";
		if (status == "ok") {
			tips = "正在停止VSM,请查看耗时任务！！";
			fail = "停止VSM失败";
			confirmTips = "停用当前VSM";
		} else {
			tips = "正在启用VSM,请查看耗时任务！";
			fail = "启动VSM失败";
			confirmTips = "启用当前VSM";
		}

		layer.confirm("确认要" + confirmTips + "吗？", function(index) {
			var index = layer.load();
			$.ajax({
				url : "${ctx}/vsm/updateVsmStatus.html",
				type : 'POST',
				crossOrigin : true,
				dataType : 'text',
				cache : false,
				async : true,
				data : {
					"vsmId" : vsmId,
					"isOnline" : isOnline
				},
				timeout : 5000,
				success : function(data) {
					layer.close(index);
					if (data == "success") {
						layer.msg(tips, {icon : 1,time : 2000}, function() {
							window.parent.parent.$("[data-title='耗时任务管理']").click();
							layer.load(2);
							window.location.reload();
						});
					} else if (data == "fail") {
						layer.msg(fail, {icon : 2,time : 2000});
					} else if (data == "operation") {
						layer.msg("有VSM在操作", {icon : 7,time : 2000});
					}
				},
				error : function(data) {
					layer.close(index);
					layer.closeAll();
					layer.msg("出错了", {icon : 5,time : 2000});
				}
			});
		});

	}
	//删除
	function deleteVSM(vsmId) {
		layer.confirm("确认要删除VSM吗？", function(index) {
			var index = layer.load();
			$.ajax({
				url : "${ctx}/vsm/deleteVsm.html",
				type : 'POST',
				crossOrigin : true,
				dataType : 'text',
				cache : false,
				async : true,
				data : {
					"vsmId" : vsmId
				},
				timeout : 5000,
				success : function(data) {
					layer.close(index);
					if (data == "success") {
						layer.msg("正在删除VSM,请查看耗时任务！", {icon : 1,time : 2000}, function() {
							window.parent.parent.$("[data-title='耗时任务管理']").click();
							layer.load(2);
							window.location.reload();
						});
					} else if (data == "fail") {
						layer.msg("删除VSM失败", {icon : 2,time : 2000}, function() {
							setTimeout(function() {
								layer_close();
							}, 500);
						});
					} else if (data == "operation") {
						layer.msg("有VSM在操作", {icon : 7,time : 2000});
					}
				},
				error : function(data) {
					layer.close(index);
					layer.closeAll();
					layer.msg("出错了", {icon : 5,time : 2000});
				}
			});
		});

	}
	//重置
	function resetVsm(vsmId) {
		layer.confirm("确认要重置VSM吗？", function(index) {
			var index = layer.load();
			$.ajax({
				url : "${ctx}/vsm/resetVsm.html",
				type : 'POST',
				crossOrigin : true,
				dataType : 'text',
				cache : false,
				async : true,
				data : {
					"vsmId" : vsmId
				},
				timeout : 5000,
				success : function(data) {
					layer.close(index);
					if (data == "success") {
						layer.msg("正在重置VSM,请查看耗时任务！", {icon : 1,time : 2000}, function() {
							window.parent.parent.$("[data-title='耗时任务管理']").click();
							layer.load(2);
							window.location.reload();
						});
					} else if (data == "fail") {
						layer.msg("重置VSM失败", {icon : 2,time : 2000}, function() {
							setTimeout(function() {
								layer_close();
							}, 500);
						});
					} else if (data == "status") {
						layer.msg("VSM关闭,请重启再试", {icon : 7,time : 2000}, function() {
							layer.load();
							window.location.reload();
						});
					} else if (data == "operation") {
						layer.msg('有VSM在操作', {icon : 7,time : 2000}, function() {
							setTimeout(function() {
								layer_close();
							}, 500);
						});
					}
				},
				error : function(data) {
					layer.close(index);
					layer.closeAll();
					layer.msg("出错了", {icon : 5,time : 2000});
				}
			});
		});

	}
	//重启
	function restart(vsmId) {
		layer.confirm("确认要重启VSM吗？", function(index) {
			var index = layer.load();
			$.ajax({
				url : "${ctx}/vsm/restartVsm.html",
				type : 'POST',
				crossOrigin : true,
				dataType : 'text',
				cache : false,
				async : true,
				data : {
					"vsmId" : vsmId
				},
				timeout : 5000,
				success : function(data) {
					layer.close(index);
					if (data == "success") {
						layer.msg("正在重启VSM,请查看耗时任务！", {icon : 1,time : 2000}, function() {
							window.parent.parent.$("[data-title='耗时任务管理']").click();
							layer.load(2);
							window.location.reload();
						});
					} else if (data == "fail") {
						layer.msg("重启VSM失败", {icon : 2,time : 2000}, function() {
							setTimeout(function() {
								layer_close();
							}, 500);
						});
					} else if (data == "status") {
						layer.msg("VSM关闭,请重启再试", {icon : 7,time : 2000}, function() {
							layer.load()
							window.location.reload();
						});
					} else if (data == "operation") {
						layer.msg("有VSM在操作", {icon : 7,time : 2000}, function() {
							setTimeout(function() {
								layer_close();
							}, 500);
						});
					}
				},
				error : function(data) {
					layer.close(index);
					layer.closeAll();
					layer.msg("出错了", {icon : 5,time : 2000});
				}
			});
		});
	}
	
	//VSM升級
	function upgradeVsm(vsmid) {
		layer_show("VSM升级", "${ctx}/version/toUpgradeVsm.html?vsmid="+ vsmid , "600","350");
	}
	
	</script>
	<!--/请在上方写此页面业务相关的脚本-->
</body>
</html>