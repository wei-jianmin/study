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

<title>控制公钥配置</title>
<meta name="keywords" content="H-ui.admin ">
<meta name="description" content="H-ui.admin ">
</head>
<body>
<!-- <nav class="breadcrumb"> -->
<!-- 	<i class="Hui-iconfont">&#xe67f;</i> 首页  -->
<!-- 	<span class="c-gray en">&gt;</span> HSM配置 -->
<!-- 	<span class="c-gray en">&gt;</span> 认证公钥 -->
<!-- 	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" > -->
<!-- 	<i class="Hui-iconfont">&#xe68f;</i> -->
<!-- 	</a> -->
<!-- </nav> -->
<article class="page-container">
	<form action="" method="post" class="form form-horizontal" id="form-member-add" >
	    <div class="row cl">
			<label class="form-label col-xs-3 col-sm-2" >公钥指纹1：</label>
			<div class="formControls col-xs-8 col-sm-9">
				<input type="text" class="input-text" value="${Fingerprint1}" id="Fingerprint1" name="Fingerprint1" disabled="disabled">
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-3 col-sm-2" ><span class="c-red">*</span>公钥1：</label>
			<div class="formControls col-xs-8 col-sm-9">
				<input type="text" class="input-text" value="${publicKey1}" id="publicKey1" name="publicKey1"  placeholder="请输入Base64编码格式的公钥！">
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-3 col-sm-2" >公钥指纹2：</label>
			<div class="formControls col-xs-8 col-sm-9">
				<input type="text" class="input-text" value="${Fingerprint2}" id="Fingerprint2" name="Fingerprint2" disabled="disabled">
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-3 col-sm-2" ><span class="c-red">*</span>公钥2：</label>
			<div class="formControls col-xs-8 col-sm-9">
				<input type="text" class="input-text" value="${publicKey2}" id="publicKey2" name="publicKey2"  placeholder="请输入Base64编码格式的公钥！">
			</div>
		</div>
		<br/>
		<br/>	
		<div class="row cl" style="text-align: center;">
				 <button class="btn btn-primary radius"  onclick="configPublicKey()" type="button">保存配置</button>
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
<script type="text/javascript">

/**
* 保存配置
*/
function configPublicKey() {	
	var publicKey1 = $("#publicKey1").val().trim();
	var publicKey2 = $("#publicKey2").val().trim();
	if(publicKey1.length<=0){
		layer.msg("公钥1不能为空!", {icon:7,time:2000});
		return false;
	}
	if(publicKey2.length<=0){
		layer.msg("公钥2不能为空!", {icon:7,time:2000});
		return false;
	}
	$.ajax({
		url : "${ctx}/hsm/configPublicKey.html",
		type : 'POST',
		crossOrigin : true,
		dataType : 'text',
		cache : false,
		async : true,
		data : {			
			"publicKey1" : publicKey1,
			"publicKey2" : publicKey2
		},
		success : function(data) {
			if(data=="success"){
				layer.msg("保存配置成功!", {icon:1,time:2000},function() {	
// 					window.location.reload();
					window.location.href="${ctx}/hsm/systemManage.html?typeIndex=1";
				});
			}
			/* else if(data=="verifyFail"){
				layer.msg("验签失败!", {icon:2,time:2000});
			} */
			else{
				layer.msg("保存配置失败!", {icon:2,time:2000});
			}
		} ,
		error:function(data){
			layer.msg("出错了!", {icon:5,time:2000});
		}
	});
}
</script> 
</body>
</html>