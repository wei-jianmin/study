<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ include file="/common/ctx.jsp"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta charset="utf-8">
<meta name="renderer" content="webkit|ie-comp|ie-stand">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport"
	content="width=device-width,initial-scale=1,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no" />
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

<title>修改Token</title>
<meta name="keywords" content="">
<meta name="description" content="">
</head>
<body>
	<article class="page-container">
	<form action="" method="post" class="form form-horizontal" id="form-member-add">
		<c:forEach items="${vsmidArray}" var="item">
			<div class="row cl" style="display:none;">
				<label class="form-label col-xs-3 col-sm-3"
					style="text-align: right;"><span class="c-red">*</span>vsmid：</label>
				<div class="formControls col-xs-8 col-sm-9">
					<input type="text" class="input-text" value="${item}"
						placeholder="" name="vsmids">
				</div>
			</div>
		</c:forEach>
		<div class="row cl">
			<label class="form-label col-xs-3 col-sm-3"
				style="text-align: right;"><span class="c-red">*</span>Token：</label>
			<div class="formControls col-xs-8 col-sm-9">
				<input type="text" class="input-text" value=""
					placeholder="请输入Token数字和字母（1-100位）" id="token">
			</div>
		</div>
		<div class="row cl">
			<div class="col-xs-8 col-sm-9 col-xs-offset-4 col-sm-offset-3">
				<button class="btn btn-primary radius" onclick="editToken()"
					type="button">修改</button>
				<button onClick="layer_close();" class="btn btn-default radius"
					type="button">取消</button>
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
		function editToken() {
			var token = $("#token").val();
			var regex = /^[A-Za-z0-9]+$/ ;
			if (token.length == 0) {
				layer.msg("token不能为空", {icon : 7,time : 2000});
				return false;
			}else if(token.length > 100){
				layer.msg("token最大长度100", {icon : 7,time : 2000});
				return false;
			}else if(!regex.test(token)){
				layer.msg("token只允许输入数字和字母", {icon : 7,time : 2000});
				return false;
			}

			var vsmids = $("[name=vsmids]");
			var param;
			for ( var i = 0; i < vsmids.length; i++) {
				if (i == 0) {
					param = vsmids[i].value
				} else {
					param = param + "," + vsmids[i].value;
				}
			}
			var index = layer.load();
			$.ajax({
				url : "${ctx}/vsm/tokenEdit.html",
				type : 'POST',
				crossOrigin : true,
				dataType : 'text',
				cache : false,
				async : true,
				data : {
					"vsmIds" : param,
					"token" : token,
				},
				success : function(data) {
					layer.close(index);
					if (data == "success") {
						layer.msg('修改Token成功', {
							icon : 1,
							time : 2000
						}, function() {
							layer.load(2);
							window.parent.location.reload();
						});
					} else if (data == "fail") {
						layer.msg('修改Token失败', {
							icon : 2,
							time : 2000
						});
					} else if (data == "operation") {
						layer.msg('有VSM在操作', {
							icon : 7,
							time : 2000,
							maxWidth : 1000
						});
					} else {
						console.log(data);
						layer.msg(data, {
							icon : 7,
							time : 2000,
							maxWidth : 450,
							offset : [ '25px', '45px' ]
						}, function() {
						});
					}
				},
				error : function(data) {
					layer.close(index);
					layer.msg('出错了', {
						icon : 5,
						time : 2000
					});
				}
			});
		}
	</script>
	<!--/请在上方写此页面业务相关的脚本-->
</body>
</html>