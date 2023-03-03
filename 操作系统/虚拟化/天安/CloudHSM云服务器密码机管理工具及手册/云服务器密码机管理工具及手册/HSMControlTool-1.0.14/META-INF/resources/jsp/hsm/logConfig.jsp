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

<title>日志配置</title>
<meta name="keywords" content="H-ui.admin ">
<meta name="description" content="H-ui.admin ">
</head>
<body>
<!-- <nav class="breadcrumb"> -->
<!-- 	<i class="Hui-iconfont">&#xe67f;</i> 首页  -->
<!-- 	<span class="c-gray en">&gt;</span> HSM管理 -->
<!-- 	<span class="c-gray en">&gt;</span> 日志配置 -->
<!-- 	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" > -->
<!-- 	<i class="Hui-iconfont">&#xe68f;</i> -->
<!-- 	</a> -->
<!-- </nav> -->
<article class="page-container">						
  <form class="form form-horizontal" >	
	   <input type="hidden" value="${uploadImgFlg}" id="uploadImgFlg" name="uploadImgFlg">
	   <div class="row cl">
			<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>日志服务器类型:</label>
			<div class="formControls col-xs-5 col-sm-6"> <span class="select-box">
				<select class="select" name="logType" id="logType" size="1" onchange="changeType()">
				    <option value="" <c:if test="${logType==''}">selected</c:if>>请选择</option>
					<option value="0" <c:if test="${logType==0}">selected</c:if>>阿里SLS日志服务器</option>
					<option value="1" <c:if test="${logType==1}">selected</c:if>>日志文件服务器</option>
					<option value="2" <c:if test="${logType==2}">selected</c:if>>SYSLOG服务器</option>
				</select>
				</span> 
			</div>
		</div>		
		<div class="row cl" id="other" style="display: none;">			
			<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>服务器地址:</label>
			<div class="formControls col-xs-5 col-sm-6">
				<input type="text" class="input-text" value="${logAddr}" placeholder="请输入正确的服务器地址" id="logAddr" name="logAddr">
			</div>
		</div>
		<div id="sls" style="display: none;">
			<div class="row cl">			
				<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>slsAccessKey:</label>
				<div class="formControls col-xs-5 col-sm-6">
					<input type="text" class="input-text" value="${slsAccessKey}" placeholder="请输入slsAccessKey" id="slsAccessKey" name="slsAccessKey">
				</div>
			</div>
			<div class="row cl">			
				<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>slsEndpoint:</label>
				<div class="formControls col-xs-5 col-sm-6">
					<input type="text" class="input-text" value="${slsEndpoint}" placeholder="请输入slsEndpoint" id="slsEndpoint" name="slsEndpoint">
				</div>
			</div>
			<div class="row cl">			
				<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>slsLogstore:</label>
				<div class="formControls col-xs-5 col-sm-6">
					<input type="text" class="input-text" value="${slsLogstore}" placeholder="请输入slsLogstore" id="slsLogstore" name="slsLogstore">
				</div>
			</div>
			<div class="row cl">			
				<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>slsProject:</label>
				<div class="formControls col-xs-5 col-sm-6">
					<input type="text" class="input-text" value="${slsProject}" placeholder="请输入slsProject" id="slsProject" name="slsProject">
				</div>
			</div>
			<div class="row cl">			
				<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>slsSecretkey:</label>
				<div class="formControls col-xs-5 col-sm-6">
					<input type="text" class="input-text" value="${slsSecretKey}" placeholder="请输入slsSecretKey" id="slsSecretKey" name="slsSecretKey">
				</div>
			</div>
			<div class="row cl">			
				<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>slsSyncPeriod:</label>
				<div class="formControls col-xs-5 col-sm-6">
					<input type="text" class="input-text" value="${slsSyncPeriod}" placeholder="请输入slsSyncPeriod" id="slsSyncPeriod" name="slsSyncPeriod">
				</div>
			</div>	
		</div>	
		<br/>
		<br/>				
	    <div class="row cl" style="text-align: center;">
				<button onClick="logConfig()" class="btn btn-primary radius" type="button" >保存配置</button>
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
$(function(){
	var logType=$("#logType").val();
	if(logType==''){
		$("#sls").css("display","none");
		$("#other").css("display","none");
	}else if(logType==0){
		$("#sls").css("display","block");
		$("#other").css("display","none");
	}else{
		$("#other").css("display","block");
		$("#sls").css("display","none");
	}
})
/**
 * 根据输出格式显示或隐藏对应输入框
 */
function changeType(){
	var logType=$("#logType").val();
	if(logType==''){
		$("#sls").css("display","none");
		$("#other").css("display","none");
	}else if(logType==0){
		$("#sls").css("display","block");
		$("#other").css("display","none");
	}else{
		$("#other").css("display","block");
		$("#sls").css("display","none");
	}
}
//日志配置
function logConfig(){
	var logType=$("#logType").val();
	var logAddr=$("#logAddr").val().trim();
	var uploadImgFlg=$("#uploadImgFlg").val();
	var slsAccessKey=$("#slsAccessKey").val().trim();
	var slsEndpoint=$("#slsEndpoint").val().trim();
	var slsLogstore=$("#slsLogstore").val().trim();
	var slsProject=$("#slsProject").val().trim();
	var slsSecretKey=$("#slsSecretKey").val().trim();
	var slsSyncPeriod=$("#slsSyncPeriod").val().trim();
	var slsStr="";
	//验证IP
	var checkIp = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])(\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])){3}$/;
	//验证IPV6
	var checkIp6=/^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/;	
		
	var reg="^((https|http|ftp|rtsp|mms)?://)?" // schema
    	+ "(([0-9a-zA-Z_!~*\'().&=+$%-]+: )?[0-9a-zA-Z_!~*\'().&=+$%-]+@)?"//ftp的user@
    	+ "(([0-9]{1,3}\\.){3}[0-9]{1,3}" // IP形式的URL- 199.194.52.184
    	+ "|" // 允许IP和DOMAIN（域名）
   		+ "([0-9a-zA-Z_!~*\'()-]+\\.)*" // 域名- www.
    	+ "([0-9a-zA-Z][0-9a-zA-Z-]{0,61})?[0-9a-zA-Z]\\." // 二级域名
    	+ "[a-zA-Z]{2,6})" // first level domain- .com or .museum
    	+ "(:[0-9]{1,4})?" // 端口- :80
    	+ "((/?)|" // a slash isn't required if there is no file name
    	+ "(/[0-9a-zA-Z_!~*\'().;?:@&=+$,%#-]+)+/?)$";
	
	if(logType.length == 0){
      	layer.msg("请选择日志类型！",{icon:7,time:2000});
      	return false;
    }
	if(logType==0){
		if(slsAccessKey.length==0){
	      	layer.msg("请输入slsAccessKey！",{icon:7,time:2000});
	      	return false;
	    }
		if(slsEndpoint.length==0){
	      	layer.msg("请输入slsEndpoint！",{icon:7,time:2000});
	      	return false;
	    }
		if(slsLogstore.length==0){
	      	layer.msg("请输入slsLogstore！",{icon:7,time:2000});
	      	return false;
	    }
		if(slsProject.length==0){
	      	layer.msg("请输入slsProject！",{icon:7,time:2000});
	      	return false;
	    }
		if(slsSecretKey.length==0){
	      	layer.msg("请输入slsSecretKey！",{icon:7,time:2000});
	      	return false;
	    }
		if(slsSyncPeriod.length==0){
	      	layer.msg("请输入slsSyncPeriod！",{icon:7,time:2000});
	      	return false;
	    }
		slsStr=slsAccessKey+";"+slsEndpoint+";"+slsLogstore+";"+slsProject+";"+slsSecretKey+";"+slsSyncPeriod;
		logAddr="";
	}else{
	 	if(logAddr.length==0){
       		layer.msg("请输入服务器地址！",{icon:7,time:2000});
       		return false;
     	}
	 	if(!(new RegExp(reg).test(logAddr)||checkIp6.test(logAddr)||checkIp.test(logAddr))){
	 		layer.msg("请输入有效的服务器地址！",{icon:7,time:2000});
        	return false;
	 	}
		slsStr="";
	}	
	$.ajax({
		url : "${ctx}/hsm/configLog.html",
		type : 'POST',
		crossOrigin : true,
		dataType : 'text',
		cache : false,
		async : true,
		data : {
			"logType" : logType,
			"logAddr" : logAddr,
			"uploadImgFlg" : uploadImgFlg,
			"slsStr" : slsStr
		},
		success : function(data) {
			layer.closeAll();
			var flag = data.split(",")[0];
			if(flag=="success"){
				layer.msg("重置日志配置成功！", {icon:1,time:2000},function() {
// 					window.location.reload();
					window.location.href="${ctx}/hsm/systemManage.html?typeIndex=4";
				});
			}else {
				layer.msg("重置日志配置失败！", {icon:2,time:2000});
			}
		} ,
		error:function(data){
			layer.closeAll();
			layer.msg("出错了！", {icon:5,time:2000});
		}
	});
}
</script> 
</body>
</html>