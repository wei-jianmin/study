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

<title>配置VSM</title>
<meta name="keywords" content="">
<meta name="description" content="">
</head>
<body>
<article class="page-container">
	
	<c:choose>
		<c:when test="${vsmInfo.id==null || vsmInfo.id ==''}">
			<div class="row cl">
				<div class="formControls col-xs-5 col-sm-5"></div>
				<div class="formControls col-xs-6 col-sm-6" style="color: red;">VSM已关机</div>
			</div>
		</c:when>
		<c:otherwise>
		<form action="${ctx}/vsm/editVsmNetWork.html" method="post" class="form form-horizontal" id="form-netWork" title="网络配置">
				<div class="row cl">
					<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"> vsmID： </label>
					<div class="formControls col-xs-8 col-sm-9"> ${vsmInfo.id} </div>
				 </div>
				 <div class="row cl">
					<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"> vsm类型： </label>
					<div class="formControls col-xs-8 col-sm-9"> ${vsmInfo.type} </div>
				 </div>
				<div class="row cl">
					<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>配置ip类型：</label>
					<div class="formControls col-xs-8 col-sm-9">
						<span class="select-box"> 
						<select class="select" size="1" name="ipFlg" id="ipFlg">
								<option value="0">请选择</option>
								<!-- <option value="1">配置服务ip</option>
								<option value="2">配置管理ip</option> -->
								<option value="3" selected="selected">全部IPV4</option>
								<!-- <option value="4">配置服务IPV6</option>
								<option value="5">配置管理IPV6</option> -->
								<option value="6">全部IPV6</option>
						</select>
						</span>
					</div>
				</div>
				<div id="ipv4Config">
					<div class="row cl">
					<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>IP地址：</label>
					<div class="formControls col-xs-8 col-sm-9">
						<input type="text" class="input-text" value="${vsmInfo.ip}" placeholder="请输入ip" id="ip" name="ip">
					</div>
					</div>
					<div class="row cl">
						<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>子网掩码：</label>
						<div class="formControls col-xs-8 col-sm-9">
							<input type="text" class="input-text" value="${vsmInfo.mask}" placeholder="请输入子网掩码" id="mask" name="mask">
						</div>
					</div>
					<div class="row cl">
						<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>默认网关：</label>
						<div class="formControls col-xs-8 col-sm-9">
							<input type="text" class="input-text" value="${vsmInfo.gateway}" placeholder="请输入默认网关" id="gateway" name="gateway">
						</div>
					</div>
				</div>
				
				<div id="ipv6Config">
					<div class="row cl">
					<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>IPV6地址：</label>
					<div class="formControls col-xs-8 col-sm-9">
						<input type="text" class="input-text" value="${vsmInfo.ip6}" placeholder="请输入IPV6地址" id="ip6" name="ip6">
					</div>
					</div>
					<div class="row cl">
						<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>IPV6子网前缀：</label>
						<div class="formControls col-xs-8 col-sm-9">
							<input type="text" class="input-text" value="${vsmInfo.ip6hlen}" placeholder="请输入IPV6子网前缀" id="ip6hlen" name="ip6hlen">
						</div>
					</div>
					<div class="row cl">
						<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>IPV6网关：</label>
						<div class="formControls col-xs-8 col-sm-9">
							<input type="text" class="input-text" value="${vsmInfo.gateway6}" placeholder="请输入IPV6网关" id="gateway6" name="gateway6">
						</div>
					</div>
				</div>
				
				<div class="row cl">
					<div class="col-xs-8 col-sm-9 col-xs-offset-4 col-sm-offset-3">
						<button class="btn btn-primary radius" id="netConfig" type="button">配置网络</button>
					</div>
				</div>
			</form>
			<form action="" method="post" class="form form-horizontal" id="form-mac" title="MAC配置">
					<div class="row cl">
						<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>mac：</label>
						<div class="formControls col-xs-8 col-sm-9">
							<input type="text" class="input-text" value="${vsmInfo.mac}" placeholder="请输入mac地址" id="mac" name=mac>
						</div>
					</div>
					<!-- <div class="row cl">
						<div class="col-xs-8 col-sm-9 col-xs-offset-4 col-sm-offset-3">
							<button class="btn btn-primary radius" onclick="vsmMacEdit()" type="button" disabled="disabled">配置MAC</button> (最新版管控已去掉此功能)
						</div>
					</div> -->
			</form>
				
			<form action="" method="post" class="form form-horizontal" id="form-mtu" title="MTU配置">
				<div class="row cl">
					<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>mtu：</label>
					<div class="formControls col-xs-8 col-sm-9">
						<input type="text" class="input-text" value="${vsmInfo.mtu}" placeholder="请输入mtu(取值范围1280-10000)" id="mtu" name=mtu>
					</div>
				</div>
				<!-- <div class="row cl">
						<div class="col-xs-8 col-sm-9 col-xs-offset-4 col-sm-offset-3">
							<button class="btn primary radius" onclick="vsmMtuEdit()" type="button" disabled="disabled">配置MTU</button>(最新版管控已去掉此功能)
						</div>
					</div> -->
				</form>
				
				<form action="" method="post" class="form form-horizontal" id="form-vlan" title="VLAN配置">
					<div class="row cl">
					<label class="form-label col-xs-3 col-sm-3"
						style="text-align: right;">vlan：</label>
					<div class="formControls col-xs-8 col-sm-9">
						<input type="text" class="input-text" value="${vsmInfo.vlanTag}"
							placeholder="请输入vlan值(取值范围1-4094)" id="vlan" name=vlan>
					</div>
				</div>
				<div class="row cl" style="display: none;">
					<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>vlan：</label>
					<div class="formControls col-xs-8 col-sm-9">
						<input type="text" class="input-text" value="${vsmInfo.vlanTag}" id="vlanTag" name=vlanTag>
					</div>
				</div>
				<!-- <div class="row cl">
						<div class="col-xs-8 col-sm-9 col-xs-offset-4 col-sm-offset-3">
							<button class="btn btn-default active" onclick="vsmVlanEdit()" type="button" disabled="disabled">配置VLAN</button>(最新版管控已暂停使用)
						</div>
					</div> -->
				</form>
				
			</c:otherwise>
		</c:choose>

	
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
	$(function(){
		$("#ipv4Config").show();
		$("#ipv6Config").hide();
		
		$("#ipFlg").change(function(){
			const ipFlg = $("#ipFlg").val();
			if(ipFlg <= 3){
				$("#ipv4Config").show();
				$("#ipv6Config").hide();
			}else if(ipFlg >= 4 ){
				$("#ipv4Config").hide();
				$("#ipv6Config").show();
				
			}
		});
		
		
		$("#netConfig").click(function(){
			var mask = $("#mask").val();
			var gateway = $("#gateway").val();
			var ip = $("#ip").val();
			var ipFlg = $("#ipFlg").val();
			var ip6 = $("#ip6").val();
			var ip6Len = $("#ip6hlen").val();
			var gateway6 = $("#gateway6").val();

			//ip格式校验
			var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
			//子网掩码格式校验
			var exp = /^(254|252|248|240|224|192|128|0)\.0\.0\.0|255\.(254|252|248|240|224|192|128|0)\.0\.0|255\.255\.(254|252|248|240|224|192|128|0)\.0|255\.255\.255\.(254|252|248|240|224|192|128|0)$/;

			var checkIp6=/^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/;
			var checkPwdRE = /^[^ ]+$/;//不能包含空格
			if (ipFlg == "") {
				layer.msg("请选择类型", {icon : 7,time : 2000});
				return false;
			}
			if (ipFlg <4 && mask.length == 0) {
				layer.msg("子网掩码不能为空", {icon : 7,time : 2000});
				return false;
			}
			if (ipFlg <4 &&!exp.test(mask)) {
				layer.msg("子网掩码格式不正确！", {icon : 7,time : 2000});
				return false;
			}
			if (ipFlg <4 && gateway.length == 0) {
				layer.msg("默认网关不能为空", {icon : 7,time : 2000});
				return false;
			}
			if (ipFlg <4 && !checkPwdRE.test(gateway)) {
				layer.msg("默认网关不能包含空格！", {icon : 7,time : 2000});
				return false;
			}
			if (ipFlg <4 && ip.length == 0) {
				layer.msg("IP地址不能为空", {icon : 7,time : 2000});
				return false;
			}
			if (ipFlg <4 && ip.length > 0 && !reg.test(ip)) {
				layer.msg("IP地址格式不正确！", {icon : 7,time : 2000});
				return false;
			}

			if(ipFlg >3 && ip6.length == 0){
				layer.msg("IPV6地址不能为空", {icon : 7,time : 2000});
				return false;
			}
			
			if (ipFlg >3 && ip.length > 0 && !reg.test(ip)) {
				layer.msg("IPV6地址格式不正确！", {icon : 7,time : 2000});
				return false;
			}
			if(ipFlg >3 && !isNaN(ip6Len) && (parseInt(ip6Len)<1|| parseInt(ip6Len)>127)){
				layer.msg("IPV6子网前缀有效范围(1-127)！",{icon:7,time:2000});
		      	return false;
			}
			
			if(ipFlg >3 && gateway6.length == 0){
				layer.msg("IPV6网关地址不能为空", {icon : 7,time : 2000});
				return false;
			}
			if (ipFlg >3 && !checkPwdRE.test(gateway6)) {
				layer.msg("IPV6网关地址不能包含空格！", {icon : 7,time : 2000});
				return false;
			}
			
			var index = layer.load();
			$.ajax({
				url : "${ctx}/vsm/editVsmNetWork.html",
				type : 'POST',
				crossOrigin : true,
				dataType : "text",
				cache : false,
				async : true,
				data : {
					"vsmId" : '${vsmInfo.id}',
					"mask" : mask,
					"gateway" : gateway,
					"ip" : ip,
					"ipFlg" : ipFlg,
				//	"mac" : mac,
				//	"vlanTag" : vlanTag,
				//	"vlan" : vlan,
				//	"mtu" : mtu,
					"ip6":ip6,
					"ip6Len":ip6Len,
					"gateway6":gateway6,
					"type":'${vsmInfo.type}'
				},
				success : function(data) {
					layer.close(index);
					if (data == "success") {
						layer.msg("修改VSM成功", {icon : 1,time : 2000}, function() {
							layer.load(2);
							window.parent.location.reload();
						});
					} else if (data == "fail") {
						layer.msg("修改VSM失败", {icon : 2,time : 2000});
					} else if (data == "status") {
						layer.msg("VSM关闭,请重启再试", {icon : 2,time : 2000}, function() {
							layer.load(2);
							window.parent.location.reload();
						});
					} else if (data == "network") {
						layer.msg("VSM配置网络地址失败", {icon : 2,time : 2000});
					} else if (data == "mac") {
						layer.msg("VSM配置mac地址失败", {icon : 2,time : 2000});
					} else if (data == "vlan") {
						layer.msg("VSM配置vlan值失败", {icon : 2,time : 2000});
					} else if (data == "mtu") {
						layer.msg("VSM配置mtu值失败", {icon : 2,time : 2000});
					} else if (data == "operation") {
						layer.msg("有VSM在操作", {icon : 7,time : 2000});
					}
				},
				error : function(data) {
					layer.close(index);
					layer.msg("出错了", {icon : 5,time : 2000});
				}
			});
			
		});
		
	});
		function vsmMacEdit(){
			var mac = $("#mac").val();
			if (mac.length == 0) {
				layer.msg("mac地址不能为空", {icon : 7,time : 2000});
				return false;
			}
			if(mac == '${vsmInfo.mac}'){
				layer.msg("没有修改MAC", {icon : 7,time : 2000});
				return false;
			}
			$.ajax({
				url : "${ctx}/vsm/editVsmMac.html",
				type : 'POST',
				crossOrigin : true,
				dataType : 'text',
				cache : false,
				async : true,
				data : {
					"vsmId" : '${vsmInfo.id}',
					"mac" : mac
				},
				success : function(data) {
					if (data == "success") {
						layer.msg("修改VSM成功", {icon : 1,time : 2000}, function() {
							layer.load(2);
							window.parent.location.reload();
						});
					} else if (data == "fail") {
						layer.msg("修改VSM失败", {icon : 2,time : 2000});
					} else if (data == "status") {
						layer.msg("VSM关闭,请重启再试", {icon : 2,time : 2000}, function() {
							layer.load(2);
							window.parent.location.reload();
						});
					} else if (data == "mac") {
						layer.msg("VSM配置mac地址失败", {icon : 2,time : 2000});
					} else if (data == "operation") {
						layer.msg("有VSM在操作", {icon : 7,time : 2000});
					}
				},
				error : function(data) {
					layer.msg("出错了", {icon : 5,time : 2000});
				}
			});
		}
		function vsmMtuEdit(){
			var mtu = $("#mtu").val();
			if (mtu.length == 0) {
				layer.msg("mtu值不能为空", {icon : 7,time : 2000});
				return false;
			}
			if (!(mtu >= 1280 && mtu <= 10000)) {
				layer.msg("VSM的MTU值(取值范围1280-10000)", {icon : 7,time : 2000});
				return false;
			}
			if(mtu == '${vsmInfo.mtu}'){
				layer.msg("没有修改MTU", {icon : 7,time : 2000});
				return false;
			}
			$.ajax({
				url : "${ctx}/vsm/editVsmMtu.html",
				type : 'POST',
				crossOrigin : true,
				dataType : 'text',
				cache : false,
				async : true,
				data : {
					"vsmId" : '${vsmInfo.id}',
					"mtu" : mtu
				},
				success : function(data) {
					if (data == "success") {
						layer.msg("修改VSM成功", {icon : 1,time : 2000}, function() {
							layer.load(2);
							window.parent.location.reload();
						});
					} else if (data == "fail") {
						layer.msg("修改VSM失败", {icon : 2,time : 2000});
					} else if (data == "status") {
						layer.msg("VSM关闭,请重启再试", {icon : 2,time : 2000}, function() {
							layer.load(2);
							window.parent.location.reload();
						});
					} else if (data == "mtu") {
						layer.msg("VSM配置mtu值失败", {icon : 2,time : 2000});
					} else if (data == "operation") {
						layer.msg("有VSM在操作", {icon : 7,time : 2000});
					}
				},
				error : function(data) {
					layer.msg("出错了", {icon : 5,time : 2000});
				}
			});
		}
		
		function vsmVlanEdit(){
			var vlan = $("#vlan").val();
			var vlanTag = $("#vlanTag").val();
			
			if (!(vlan.length == 0)) {
				if (!(vlan >= 1 && vlan <= 4094)) {
					layer.msg("VLAN的tag值(取值范围1-4094)", {icon : 7,time : 2000});
					return false;
				}
			} else {
				vlan = -1;
			}
			if (vlanTag.length == 0) {
				vlanTag = -1;
			}
			if(vlan == vlanTag){
				layer.msg("没有修改vlan值", {icon : 7,time : 2000});
				return false;
			}
			
			$.ajax({
				url : "${ctx}/vsm/editVsmVlan.html",
				type : 'POST',
				crossOrigin : true,
				dataType : 'text',
				cache : false,
				async : true,
				data : {
					"vsmId" : '${vsmInfo.id}',
					"vlanTag" : vlanTag,
					"vlan" : vlan
				},
				success : function(data) {
					if (data == "success") {
						layer.msg("修改VSM成功", {icon : 1,time : 2000}, function() {
							layer.load(2);
							window.parent.location.reload();
						});
					} else if (data == "fail") {
						layer.msg("修改VSM失败", {icon : 2,time : 2000});
					} else if (data == "status") {
						layer.msg("VSM关闭,请重启再试", {icon : 2,time : 2000}, function() {
							layer.load(2);
							window.parent.location.reload();
						});
					} else if (data == "vlan") {
						layer.msg("VSM配置vlan值失败", {icon : 2,time : 2000});
					} else if (data == "operation") {
						layer.msg("有VSM在操作", {icon : 7,time : 2000});
					}
				},
				error : function(data) {
					layer.msg("出错了", {icon : 5,time : 2000});
				}
			});
		}
	</script>
	<!--/请在上方写此页面业务相关的脚本-->
</body>
</html>