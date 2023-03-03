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

<title>VSM详情</title>
<meta name="keywords" content="">
<meta name="description" content="">
</head>
<body>
<article class="page-container">
	<form action="" method="post" class="form form-horizontal" id="form-member-add" >
	
		<c:choose>
			<c:when test="${vsmInfoAll.status==null || vsmInfoAll.status ==''}">
				<div class="row cl">
					<div class="formControls col-xs-5 col-sm-5">
							
					</div>
					<div class="formControls col-xs-6 col-sm-6" style="color: red;">
						获取VSM信息失败,服务器已关机
					</div>
				</div>
			</c:when>
			<c:otherwise>
				<div class="row cl">
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">uuid：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text" value="${vsmInfo.id}" disabled >
					</div>
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">IP地址：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text" value="${vsmInfo.ip }" disabled>
					</div>					
				</div>
				<div class="row cl">
				    <label class="form-label col-xs-3 col-sm-2" style="text-align: right;">类型：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfo.type }"  disabled>
					</div>
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">IPV6地址：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text" value="${vsmInfo.ip6 }" disabled>
					</div>																									
				</div>
				<div class="row cl">				
				    <label class="form-label col-xs-3 col-sm-2" style="text-align: right;">版本号：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfo.version }"  disabled>
					</div>
					
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">子网掩码：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfo.mask }"  disabled>
					</div>
															
				</div>
				<div class="row cl">				
				    <label class="form-label col-xs-3 col-sm-2" style="text-align: right;">序列号：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfoAll.serialNo }"  disabled>
					</div>
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">网关地址：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfo.gateway }"  disabled>
					</div>
														
				</div>
				<div class="row cl">				
				   <label class="form-label col-xs-3 col-sm-2" style="text-align: right;">资源数：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfoAll.resNum }"  disabled>
					</div>
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">vlan-tag：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfo.vlanTag }"  disabled>
					</div>
				</div>
				<div class="row cl">				
				   <label class="form-label col-xs-3 col-sm-2" style="text-align: right;">运行状态：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfo.status }"  disabled>
					</div>
					 <label class="form-label col-xs-3 col-sm-2" style="text-align: right;">mac地址：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfo.mac }"  disabled>
					</div>	
				</div>   												
				<div class="row cl">				
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">token：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfo.token }"  disabled>
					</div>
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">mtu：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfo.mtu }"  disabled>
					</div>
				</div>
				<div class="row cl">				
				    <label class="form-label col-xs-3 col-sm-2" style="text-align: right;">IPV6子网前缀：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfoAll.ip6hlen}"  disabled>
					</div>
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">IPV6网关地址：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfo.gateway6}"  disabled>
					</div>
														
				</div>
				<div class="row cl">
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">密钥摘要：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfo.digest_key }"  disabled>
					</div>
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">影像摘要：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"   value="${vsmInfo.digest}"  disabled>
					</div>
				</div>
				<div class="row cl">
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">通讯方式：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<c:if test="${vsmInfo.communication==1 }">
							<input type="text" class="input-text"   value="密文"  disabled>
						</c:if>
						<c:if test="${vsmInfo.communication==2 }">
							<input type="text" class="input-text"   value="明文"  disabled>
						</c:if>
						
					</div>	
					<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">启动时间：</label>
					<div class="formControls col-xs-4 col-sm-4">
						<input type="text" class="input-text"     id="uptime" disabled>
					</div>				
				</div>
<!-- 				<div class="row cl" style="text-align: center;"> -->
<!-- 						<button onClick="layer_close();" class="btn btn-default radius" type="button">返回</button> -->
<!-- 				</div> -->
			</c:otherwise>
		</c:choose>
	
		
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

	var extensions =${vsmInfo.extensions};
	console.log(extensions.upTime);
	
	$("#uptime")[0].value=extensions.upTime;
	
	
	
</script> 
<!--/请在上方写此页面业务相关的脚本-->
</body>
</html>