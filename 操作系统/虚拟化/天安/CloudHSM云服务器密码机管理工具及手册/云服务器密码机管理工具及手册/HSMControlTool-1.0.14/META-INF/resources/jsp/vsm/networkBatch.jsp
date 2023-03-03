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

<title>批量配置网络</title>
<meta name="keywords" content="">
<meta name="description" content="">
</head>
<body>
<article class="page-container">
	<form action="" method="post" class="form form-horizontal" id="form-member-add" >
	<c:set var="fill" value="1"></c:set>
	<!-- <button class="btn btn-primary radius"  onclick="automatic()" type="button" style="float: right;">填充</button> -->
		<c:forEach items="${vsmInfoList}" var="item" varStatus="status">		    
		    <c:choose>
		    	<c:when test="${item.type=='' || item.type ==null }">
		    		<div class="row cl">
						<label class="form-label col-xs-3 col-sm-2" style="text-align: right;"><span class="c-red">*</span>uuid：</label>
						<div class="formControls col-xs-8 col-sm-9">
						<input type="text" class="input-text" value="" placeholder="${item.vsmid}"  readonly >
						</div>
					</div>
					<div class="row cl">						
						<div class="c-red col-xs-5 col-sm-5"></div>
						<div class="c-red col-xs-5 col-sm-5">
							<span >已经关机,不参与操作</span>
						</div>
					</div>															
		    	</c:when>
		    	<c:otherwise>	
			    	    	     
		    		<div class="row cl">
						<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">uuid：</label>
						<div class="formControls col-xs-8 col-sm-9">
						<input type="text" class="input-text" value="${item.vsmid}"  name="uuid" disabled="disabled" >
						</div>
						<c:if test="${fill ==1 }">
			    			<button class="btn btn-primary radius"  onclick="automatic()" type="button" style="float: right;">填充</button>	
				    	</c:if>
				    	<c:set var="fill" value="2"></c:set>
					</div>
			    	<div class="row cl">
						<label class="form-label col-xs-5 col-sm-2" style="text-align: right;">序列号：</label>
						<div class="formControls col-xs-5 col-sm-3">
						<input type="text" class="input-text" value="${item.serialNo}" placeholder="${item.serialNo}"  disabled="disabled">
						</div>
						<label class="form-label col-xs-5 col-sm-2" style="text-align: right;">类型：</label>
						<div class="formControls col-xs-5 col-sm-4">
						<input type="text" class="input-text" value="${item.type}" placeholder="${item.type}" name="types"  disabled="disabled">
						</div>
					</div>
					<div class="row cl">
					<label class="form-label col-xs-5 col-sm-2" style="text-align: right;"><span class="c-red">*</span>配置ip类型：</label>
					<div class="formControls col-xs-5 col-sm-3">
						<span class="select-box"> 
						<select class="select" size="1" name="ipFlg" id="ipFlg0">
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
					<div class="row cl">
						<label class="form-label col-xs-5 col-sm-2" style="text-align: right;"><span class="c-red">*</span>IP地址：</label>
						<div class="formControls col-xs-5 col-sm-3">
							<input type="text" class="input-text" value="${item.ip}"  name="ip" >
						</div>
						<label class="form-label col-xs-5 col-sm-2" style="text-align: right;"><span class="c-red">*</span>掩码：</label>
						<div class="formControls col-xs-5 col-sm-4">
							<input type="text" class="input-text" value="${item.mask}" name="mask" >
						</div>
					</div>
					<div class="row cl">
						<label class="form-label col-xs-5 col-sm-2" style="text-align: right;"><span class="c-red">*</span>网关：</label>
						<div class="formControls col-xs-5 col-sm-3">
							<input type="text" class="input-text" value="${item.gateway}"  name="gateway">
						</div>
						<label class="form-label col-xs-5 col-sm-2" style="text-align: right;">vlan：</label>
						<div class="formControls col-xs-5 col-sm-4">
						<input type="text" class="input-text" value="${item.vlan_tag}"  placeholder="请输入vlan值(取值范围1-4094)" name="vlan">
						</div>
					</div>
				
					<div class="row cl">
					<label class="form-label col-xs-5 col-sm-2" style="text-align: right;">IPV6地址：</label>
					<div class="formControls col-xs-5 col-sm-3">
						<input type="text" class="input-text" value="${item.ip6}"  name="ip6">
					</div>
					<label  class="form-label col-xs-5 col-sm-2" style="text-align: right;">IPV6子网前缀：</label>
						<div class="formControls col-xs-5 col-sm-4">
							<input type="text" class="input-text" value="${item.ip6hlen}"  name="ip6hlen">
						</div>
					</div>
					<div class="row cl">
						<label class="form-label col-xs-5 col-sm-2" style="text-align: right;">IPV6网关：</label>
						<div class="formControls col-xs-5 col-sm-3">
							<input type="text" class="input-text" value="${item.gateway6}"   name="gateway6">
						</div>
						
						<input type="hidden" class="input-text" value="${item.vlan_tag}"  name="vlanTag">
					</div>
					
		    	</c:otherwise>
		    	
		    </c:choose>
		    <c:if test="${!status.last}">
			     <br/>
			    <br/>
				<span class=" col-xs-8 col-sm-12">-----------------------------------------------------------------------------------------------------------------------------------</span>
				<br/>
				<br/>
		    </c:if>
		</c:forEach>
		<br/>
		<br/>
		<div class="row cl">
			<div class="col-xs-12 col-sm-12 col-xs-offset-5 col-sm-offset-5">
				 <button class="btn btn-primary radius"  onclick="networkBatch()" type="button">配置</button>
				<button onClick="layer_close();" class="btn btn-default radius" type="button">取消</button>
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
	$(function(){
		$("#ipFlg0").change(function(){
			const ipFlg = $("#ipFlg0").val();
			$("[name='ipFlg'").find("option[value='"+ipFlg+"']").attr("selected",true);
		});
	});

	//ip格式校验
	var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
	var exp = /^(254|252|248|240|224|192|128|0)\.0\.0\.0|255\.(254|252|248|240|224|192|128|0)\.0\.0|255\.255\.(254|252|248|240|224|192|128|0)\.0|255\.255\.255\.(254|252|248|240|224|192|128|0)$/;
	//ip6格式校验
	var checkIp6=/^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/;
	
	//自动填充
	function automatic(){
		//获取所有的ip标签
		var ipFlgs = $("[name='ipFlg']");
		if(parseInt(ipFlgs[0].value) == 3){ //配置ipv4
			//获取所有的掩码
			var masks =$("[name='mask']");
			if(masks[0]==null||masks[0]==undefined){
				layer.msg("没有需要配置的VSM", {icon : 7,time : 2000});
				return false;
			}
			//获取第一个掩码的值
			var value =masks[0].value;
			if(value==null||value==undefined|| value==""){
				layer.msg("没有填充第一个掩码", {icon : 7,time : 2000});
				return false;
			}
			if (!exp.test(value)) {
				layer.msg("掩码格式不正确！", {icon : 7,time : 2000});
				return false;
			}
			//获取所有的网关
			var gateway =$("[name='gateway']");
			//获取第一个网关的值
			var value =gateway[0].value;
			if(value==null||value==undefined|| value==""){
				layer.msg("没有填充第一个网关", {icon : 7,time : 2000});
				return false;
			}
			//获取所有的vlan
			var vlan =$("[name='vlan']");
			//获取第一个vlan的值
			var value =vlan[0].value;
			if(!(value == null || value == undefined ||  value == "")){
				if (!(value>=1&&value<=4094)) {
					layer.msg("vlan值不在范围", {icon : 7,time : 2000});
					return false;
				}
			}
			//填充ip
			if(!automaticIp())
				return false;
			//填充掩码,网关,vlan
			for(var i =1;i<masks.length;i++){
				masks[i].value=masks[0].value;
				gateway[i].value=gateway[0].value;
				vlan[i].value=vlan[0].value;
			}
			
		}else{//配置ipv6  parseInt(ipFlgs[0].value) == 6
			var ip6hlens = $("[name='ip6hlen']");
			var gateway6s = $("[name='gateway6']");
			
			var ip6hlen =ip6hlens[0].value;
			if(ip6hlen == null||ip6hlen == undefined|| ip6hlen == ""){
				layer.msg("没有填充第一个IPV6子网前缀", {icon : 7,time : 2000});
				return false;
			}
			
			var gateway6 =gateway6s[0].value;
			if(gateway6 == null||gateway6 == undefined|| gateway6 == ""){
				layer.msg("没有填充第一个IPV6网关", {icon : 7,time : 2000});
				return false;
			}
			//获取所有的vlan
			var vlan =$("[name='vlan']");
			//获取第一个vlan的值
			var value =vlan[0].value;
			if(!(value == null || value == undefined ||  value == "")){
				if (!(value>=1&&value<=4094)) {
					layer.msg("vlan值不在范围", {icon : 7,time : 2000});
					return false;
				}
			}
			//填充ip
			if(!automaticIp())
				return false;
			
			//填充掩码,网关,vlan
			for(var i =1;i<ip6hlens.length;i++){
				ip6hlens[i].value=ip6hlens[0].value;
				gateway6s[i].value=gateway6s[0].value;
				vlan[i].value=vlan[0].value;
			}
		}
		
		
	} 
	
	//ip自动填充
	function automaticIp(){
		//获取所有的ip标签
		var ipFlgs = $("[name='ipFlg']");
		
		if(parseInt(ipFlgs[0].value) == 3){ //配置ipv4
			//获取所有的ip
			var ips =$("[name='ip']");
			//获取第一个ip的值
			var value =ips[0].value;
			if(value==null||value==undefined|| value==""){
				layer.msg("没有填充第一个ip", {icon : 7,time : 2000
				});
				return false;
			}
			if (!reg.test(value)) {
				layer.msg("IP地址格式不正确！", {icon : 7,time : 2000});
				return false;
			}
			//截取ip
			var index = value.lastIndexOf('.')+1;
			var subValue =parseInt(value.substr(index));
			//判断填充的最后一个ip是否大于255
			var lastValue =subValue+(ips.length-1);
			if(lastValue>255){
				layer.msg("填充后的ip值大于255", {icon : 7,time : 2000});
				return false;
			}
			//填充
			for(var i =1;i<ips.length;i++){
				subValue++;
				ips[i].value=value.substring(0,index)+subValue;
			}
			
		}else{//配置ipv6  parseInt(ipFlgs[0].value) == 6
			var ip6s =$("[name='ip6']");
			
			//获取第一个ip的值
			var value =ip6s[0].value;
			if(value == null || value == undefined || value==""){
				layer.msg("没有填充第一个ipv6", {icon : 7,time : 2000
				});
				return false;
			}
			if (!checkIp6.test(value)) {
				layer.msg("IPV6地址格式不正确！", {icon : 7,time : 2000});
				return false;
			}
			//截取ipv6 2051::51:128
			var index = value.lastIndexOf(":")+1;
			var subValue = parseInt(value.substr(index));
			
			//判断填充的最后一个ip是否大于255
			var lastValue = subValue + (ip6s.length-1);
			if(lastValue > 9999){
				layer.msg("填充后的ipv6 值大于9999", {icon : 7,time : 2000});
				return false;
			}
			//填充
			for(var i =1;i<ip6s.length;i++){
				subValue++;
				ip6s[i].value=value.substring(0,index)+subValue;
			}
		}
		
		return true;
	}
	function networkBatch(){
		//获取所有的掩码
		var masks =$("[name='mask']");
		//获取所有的网关
		var gateway =$("[name='gateway']");
		//获取所有的vlan（修改后）
		var vlan =$("[name='vlan']");
		//获取所有的ip
		var ips =$("[name='ip']");
		//获取所有的uuid
		var uuids =$("[name='uuid']");
		//获取所有的vlanTag(修改前)
		var vlanTags =$("[name='vlanTag']");
		//获取所有的类型
		var types =$("[name='types']");
		
		var ipFlgs = $("[name='ipFlg']");
		var ip6s =$("[name='ip6']");
		var ip6hlens = $("[name='ip6hlen']");
		var gateway6s = $("[name='gateway6']");
		
		
		if(uuids[0] == null || uuids[0] == undefined){
			layer.msg("没有需要配置的VSM", {icon : 7,time : 2000});
			return false;
		}
		
		if(parseInt(ipFlgs[0].value) == 3){ //配置ipv4
			for(var i =0;i<ips.length;i++){
				for(var j =(i+1);j<ips.length;j++){
					if(ips[i].value==ips[j].value &&(ips[i].value!="" && ips[j].value!="")){
						layer.msg("ip地址重复", {icon : 7,time : 2000});
						console.log(ips[i].value+":"+ips[j].value+"==="+(ips[i].value==ips[j].value));
						return false;
					}
					
				}
			}
		}else{//配置ipv6  parseInt(ipFlgs[0].value) == 6
			for(var i =0;i<ip6s.length;i++){
				for(var j =(i+1);j<ip6s.length;j++){
					if(ip6s[i].value==ip6s[j].value &&(ip6s[i].value!="" && ip6s[j].value!="")){
						layer.msg("ip地址重复", {icon : 7,time : 2000});
						console.log(uuids[i].value+","+ip6s[i].value+":"+uuids[j].value+","+ip6s[j].value+"==="+(ip6s[i].value==ip6s[j].value));
						return false;
					}
					
				}
			}
		}
		var masksArray = "", gatewayArray= "", vlanArray = "",ipArray = "";
		var uuidArray = "",valnTagArray = "",typeArray = "",ipFlgArray = "";
		var ip6Array = "", ip6hlenArray = "",gateway6Array = "";
		
		
		for(var i =0;i<uuids.length;i++){
			if(parseInt(ipFlgs[0].value) == 3){ //配置ipv4
				var value =ips[i].value;
				if(value==null||value==undefined|| value==""){
					layer.msg(uuids[i].value+"没有填充ip", { icon : 7, time : 2000, maxWidth:1000 });
					return false;
				}
				if (!reg.test(value)) {
					layer.msg(uuids[i].value+"IP地址格式不正确！", { icon : 7, time : 2000, maxWidth:1000 });
					return false;
				}
				
				var value =masks[i].value;
				if(value == null || value == undefined || value == ""){
					layer.msg(uuids[i].value+"没有填充掩码", {icon : 7,time : 2000,maxWidth:1000});
					return false;
				}
				if (!exp.test(value)) {
					layer.msg(uuids[i].value+"的掩码格式不正确！", {icon : 7,time : 2000,maxWidth:1000});
					return false;
				}
			}else{//配置ipv6  parseInt(ipFlgs[0].value) == 6
				var value =ip6s[i].value;
				if(value == null||value == undefined || value == ""){
					layer.msg(uuids[i].value+"没有填充ipv6", { icon : 7, time : 2000, maxWidth:1000 });
					return false;
				}
				if (!checkIp6.test(value)) {
					layer.msg(uuids[i].value+"IPV6地址格式不正确！", { icon : 7, time : 2000, maxWidth:1000 });
					return false;
				}
				value = ip6hlens[i].value;
				if(value == null || value == undefined|| value == ""){
					layer.msg(uuids[i].value+"没有填充IPV6子网前缀", { icon : 7, time : 2000, maxWidth:1000 });
					return false;
				}
				if(parseInt(value)<1|| parseInt(value)>127){
					layer.msg(uuids[i].value+"IPV6子网前缀不在配置有效范围(1-127)", { icon : 7, time : 2000, maxWidth:1000 });
					return false;
				}
				
				value = gateway6s[i].value;
				if(value == null || value == undefined|| value == ""){
					layer.msg(uuids[i].value+"没有填充IPV6网关", { icon : 7, time : 2000, maxWidth:1000 });
					return false;
				}
				
			}
			
			value =vlan[i].value;
			if(!(value == null || value == undefined || value == "")){
				if (!(value>=1&&value<=4094)) {
					layer.msg("vlan值不在范围", { icon : 7, time : 2000 });
					return false;
				}
			}
			
			if(i == uuids.length - 1){
				masksArray = masksArray + masks[i].value;
				gatewayArray = gatewayArray + gateway[i].value;
				vlanArray = vlanArray + vlan[i].value;
				ipArray = ipArray + ips[i].value;
				uuidArray = uuidArray + uuids[i].value;
				valnTagArray = valnTagArray + vlanTags[i].value;	
				typeArray = typeArray + types[i].value;
				
				ipFlgArray = ipFlgArray + ipFlgs[i].value;
				ip6Array = ip6Array + ip6s[i].value;	
				ip6hlenArray = ip6hlenArray + ip6hlens[i].value;
				gateway6Array = gateway6Array + gateway6s[i].value;
			}else{
				masksArray = masksArray + masks[i].value + ",";
				gatewayArray = gatewayArray + gateway[i].value + ",";
				vlanArray = vlanArray + vlan[i].value + ",";
				ipArray = ipArray + ips[i].value + ",";
				valnTagArray = valnTagArray + vlanTags[i].value + ",";	
				uuidArray = uuidArray + uuids[i].value + ",";
				typeArray = typeArray + types[i].value + ",";
				
				ipFlgArray = ipFlgArray + ipFlgs[i].value + ",";
				ip6Array = ip6Array + ip6s[i].value + ",";	
				ip6hlenArray = ip6hlenArray + ip6hlens[i].value + ",";
				gateway6Array = gateway6Array + gateway6s[i].value + ",";
			}
			
		}
		
		var index =layer.load();
		$.ajax({
			url : "${ctx}/vsm/networkBatch.html",
			type : 'POST',
			crossOrigin : true,
			dataType : 'text',
			cache : false,
			async : true,
			data : {
				"vsmIds" : uuidArray,
				"masks" : masksArray,
				"gateways" : gatewayArray,
				"ips" : ipArray,
				"vlans" : vlanArray,
				"valnTags":valnTagArray,
				"types":typeArray,
				"ipFlgs":ipFlgArray,
				"ip6s":ip6Array,
				"ip6hlens":ip6hlenArray,
				"gateway6s":gateway6Array
			},
			success : function(data) {
				layer.close(index);
				if (data == "success") {
					layer.msg("修改VSM成功", {icon : 1,time : 2000,maxWidth:1000}, function() {
						layer.load(2);
						window.parent.location.reload();
					});
				} else if (data == "fail") {
					layer.msg("修改VSM失败", {icon : 2,time : 2000,maxWidth:1000});
				}else if (data == "operation") {
					layer.msg("有VSM在操作", {icon :7,time : 2000,maxWidth:1000});
				} else{
					layer.msg(data+"", {icon : 7,time : 2000,maxWidth:1000});
				}
			},
			error : function(data) {
				layer.close(index);
				layer.msg("出错了", {icon : 5,time : 2000,maxWidth:1000});
			}
		});
	}
</script> 
<!--/请在上方写此页面业务相关的脚本-->
</body>
</html>