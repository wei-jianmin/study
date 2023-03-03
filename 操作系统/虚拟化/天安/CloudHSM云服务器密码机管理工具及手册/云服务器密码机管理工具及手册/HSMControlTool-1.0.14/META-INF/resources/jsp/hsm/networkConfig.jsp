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

<title>HSM网络配置</title>
<meta name="keywords" content="H-ui.admin ">
<meta name="description" content="H-ui.admin ">
</head>
<body>
<nav class="breadcrumb">
	<i class="Hui-iconfont">&#xe67f;</i> 首页 
	<span class="c-gray en">&gt;</span> HSM管理
	<span class="c-gray en">&gt;</span> 网络配置
	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" >
	<i class="Hui-iconfont">&#xe68f;</i>
	</a>
</nav>
<input type="hidden" value="${ip}" id="ipOld">
<input type="hidden" value="${mask}" id="maskOld">
<input type="hidden" value="${gateway}" id="gatewayOld">
<input type="hidden" value="${vlan}" id="vlanOld">
<input type="hidden" value="${ip6}" id="ipv6Old">
<input type="hidden" value="${ip6hlen}" id="ip6hlenOld">
<input type="hidden" value="${gateway6}" id="gateway6Old">
<article class="page-container">
	<form action="" method="post" class="form form-horizontal" id="form-member-add" >
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>IP地址：</label>
			<div class="formControls col-xs-5 col-sm-6">
				<input type="text" class="input-text" value="${ip}" maxlength="32" id="ip" name="ip">
			</div>
		</div>
		
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>子网掩码：</label>
			<div class="formControls col-xs-5 col-sm-6">
				<input type="text" class="input-text" value="${mask}"  maxlength="32" id="mask" name="mask">
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>网关地址：</label>
			<div class="formControls col-xs-5 col-sm-6">
				<input type="text" class="input-text" value="${gateway}"  maxlength="32" id="gateway" name="gateway">
			</div>
		</div>
		
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3">IPV6地址：</label>
			<div class="formControls col-xs-5 col-sm-6">
				<input type="text" class="input-text" value="${ip6}" maxlength="32" id="ipv6" name="ipv6">
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3">IPV6子网前缀：</label>
			<div class="formControls col-xs-5 col-sm-6">
				<input type="text" class="input-text" value="${ip6hlen}" maxlength="3" id="ip6hlen" name="ip6hlen">
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3">IPV6网关：</label>
			<div class="formControls col-xs-5 col-sm-6">
				<input type="text" class="input-text" value="${gateway6}" maxlength="32" id="gateway6" name="gateway6">
			</div>
		</div>
		
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>首选DNS地址：</label>
			<div class="formControls col-xs-5 col-sm-6">
				<input type="text" class="input-text" value="${dns1}"  maxlength="32" id="dns1" name="dns1">
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>备选DNS地址：</label>
			<div class="formControls col-xs-5 col-sm-6">
				<input type="text" class="input-text" value="${dns2}"  maxlength="32" id="dns2" name="dns2">
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3">vlan：</label>
			<div class="formControls col-xs-5 col-sm-6">
				<input type="text" class="input-text" value="${vlan}"  maxlength="32" id="vlan" name="vlan">
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3">mac：</label>
			<div class="formControls col-xs-5 col-sm-6">
				<input type="text" class="input-text" value="${mac}"  maxlength="32" id="mac" name="mac" disabled="disabled">
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3">mtu：</label>
			<div class="formControls col-xs-5 col-sm-6">
				<input type="text" class="input-text" value="${mtu}"  maxlength="32" id="mtu" name="mtu" disabled="disabled">
			</div>
		</div>
		<br/>
		<br/>	
		<div class="row cl" style="text-align: center;">
				 <button class="btn btn-primary radius"  onclick="configNetwork()" type="button">保存配置</button>
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
function configNetwork() {	
	var ip = $("#ip").val().trim();
	var mask = $("#mask").val().trim();
	var gateway = $("#gateway").val().trim();
	var dns1 = $("#dns1").val().trim();
	var dns2 = $("#dns2").val().trim();
	var vlan = $("#vlan").val().trim();
	var vlanOld=$("#vlanOld").val().trim();
	
	var ip6=$("#ipv6").val().trim();
	var ip6Len=$("#ip6hlen").val().trim();
	var gateway6=$("#gateway6").val().trim();
	
	//验证IP
	var checkIp = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])(\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])){3}$/;
	//验证子网掩码
	var checkMask=/^(254|252|248|240|224|192|128|0)\.0\.0\.0|255\.(254|252|248|240|224|192|128|0)\.0\.0|255\.255\.(254|252|248|240|224|192|128|0)\.0|255\.255\.255\.(254|252|248|240|224|192|128|0)$/;
	//验证数字
	var checkInteger=/^[0-9]*$/;
	//验证IPV6
	var checkIp6=/^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/;	
	if(ip.length==0){
      	layer.msg("请输入IP地址！",{icon:7,time:2000});
      	return false;
    }
    if(!checkIp.test(ip) && ip.length !=0){
  		layer.msg("IP地址格式错误，请输入有效的IP地址！",{icon:7,time:2000});
      	return false;
    } 
    var numIp=ip.split(".");
	if(Math.round(numIp[0])+Math.round(numIp[1])+Math.round(numIp[2])+Math.round(numIp[3])==0){
		layer.msg("IP地址格式错误，请输入有效的IP地址！",{icon:7,time:2000});
      	return false;
	}
	if(mask.length==0){
      	layer.msg("请输入子网掩码！",{icon:7,time:2000});
      	return false;
    }
	if(!checkMask.test(mask) && mask.length !=0){
  		layer.msg("子网掩码格式错误，请输入有效的子网掩码！",{icon:7,time:2000});
      	return false;
    }
	if(gateway.length==0){
      	layer.msg("请输入网关地址！",{icon:7,time:2000});
      	return false;
    }
	if(!checkIp.test(gateway) && gateway.length !=0){
	  		layer.msg("网关地址格式错误，请输入有效的网关地址！",{icon:7,time:2000});
	      	return false;
	} 
	var numaddr=gateway.split(".");
	if(Math.round(numaddr[0])+Math.round(numaddr[1])+Math.round(numaddr[2])+Math.round(numaddr[3])==0){
		layer.msg("网关地址格式错误，请输入有效的网关地址！",{icon:7,time:2000});
      	return false;
	}
	if(ip6!="" && !(checkIp6.test(ip6))){
		layer.msg("IPV6地址格式错误，请输入有效的IPV6地址！",{icon:7,time:2000});
      	return false;
	}
	if(ip6!="" && !checkInteger.test(ip6Len) && (parseInt(ip6Len)<1|| parseInt(ip6Len)>127)){
		layer.msg("IPV6子网前缀有效范围(1-127)！",{icon:7,time:2000});
      	return false;
	}
	if (ip6!="" && gateway6.length ==0) {
		layer.msg("IPV6网关地址不能为为空！", {icon : 7,time : 2000});
		return false;
	}
	
	if(dns1.length=0 || dns1 == ""){
		layer.msg("首选DNS地址不能为空", {icon:7,time:2000});
		return false;
	}
	if(!checkIp.test(dns1) && dns1 != ""){
  		layer.msg("首选DNS地址格式错误，请输入有效的首选DNS地址！",{icon:7,time:2000});
      	return false;
	} 
	var numdns1=dns1.split(".");
	if(Math.round(numdns1[0])+Math.round(numdns1[1])+Math.round(numdns1[2])+Math.round(numdns1[3])==0){
		layer.msg("首选DNS地址格式错误，请输入有效的首选DNS地址！",{icon:7,time:2000});
	  	return false;
	}
	if(dns2.length=0 || dns2 == ""){
		layer.msg("备选DNS地址不能为空", {icon:7,time:2000});
		return false;
	}
	if(!checkIp.test(dns2) && dns2 != ""){
  		layer.msg("备选DNS地址格式错误，请输入有效的备选DNS地址！",{icon:7,time:2000});
      	return false;
	} 
	var numdns2=dns2.split(".");
	if(Math.round(numdns2[0])+Math.round(numdns2[1])+Math.round(numdns2[2])+Math.round(numdns2[3])==0){
		layer.msg("备选DNS地址格式错误，请输入有效的备选DNS地址！",{icon:7,time:2000});
	  	return false;
	}
	if(vlan.length!=0){
		if(!checkInteger.test(vlan)){
			layer.msg("vlan的取值范围1-4094！",{icon:7,time:2000});
	      	return false;
	    }
		if(vlan<1||vlan>4094){
			layer.msg("vlan的取值范围1-4094！",{icon:7,time:2000});
	      	return false;
	    }
    }
	$.ajax({
		url : "${ctx}/hsm/configNetwork.html",
		type : "POST",
		crossOrigin : true,
		dataType : "text",
		cache : false,
		async : true,
		data : {	
			"ip":ip,
			"mask" : mask,
			"gateway" : gateway,
			"dns1" : dns1,
			"dns2" : dns2,
			"vlan" : vlan,
			"ip6" : ip6,
			"ip6hlen" : ip6Len,
			"gateway6" : gateway6,
			"vlanOld" : vlanOld
		},
		beforeSend:function(){
			layer.load(3); //转圈圈的效果
		},
		success : function(data) {
			if(data=="success"){
				var ipOld = $("#ipOld").val().trim();
				var maskOld = $("#maskOld").val().trim();
				var gatewayOld = $("#gatewayOld").val().trim();
				if(ipOld!=ip||maskOld!=mask||gatewayOld!=gateway||vlan!=vlanOld){
					layer.confirm("保存配置成功，重启后生效，确认要重启吗？", function(index) {
						restartHSM();
					},function(index) {
						window.location.reload();
					});
				}else{
					layer.msg("保存配置成功！", {icon:1,time:2000},function() {
						window.location.reload();
					});
				}
				
			}else if(data=="fail"){
				layer.msg("保存配置失败!", {icon:2,time:2000},function() {
					window.location.reload();
				});
			}
		} ,
		error:function(data){
			layer.msg('出错了!', {icon:5,time:2000});
		}
	});
}
/*
 * 重启HSM
 */
function restartHSM() {
	$.ajax({
		url : "${ctx}/hsm/restartHSM.html",
		type : 'POST',
		crossOrigin : true,
		dataType : 'text',
		cache : false,
		async : true,
		data : {},
		beforeSend:function(){
			layer.load(5); 
			layer.msg("正在重启服务,请耐心等待!", {icon:16,time:5000}); 
		},
		success : function(data) {					
			window.parent.location.href="${ctx}/signOut.html";
		},
		error:function(data){
			window.parent.location.href="${ctx}/signOut.html";
		}
	});
}
</script> 
</body>
</html>