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

<title>影像自动上传</title>
<meta name="keywords" content="H-ui.admin ">
<meta name="description" content="H-ui.admin ">
</head>
<body>
<!-- <nav class="breadcrumb"> -->
<!-- 	<i class="Hui-iconfont">&#xe67f;</i> 首页  -->
<!-- 	<span class="c-gray en">&gt;</span> HSM管理 -->
<!-- 	<span class="c-gray en">&gt;</span> 网络配置 -->
<!-- 	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" > -->
<!-- 	<i class="Hui-iconfont">&#xe68f;</i> -->
<!-- 	</a> -->
<!-- </nav> -->
<article class="page-container">
	<form action="" method="post" class="form form-horizontal" id="form-member-add" >
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>是否自动上传影像：</label>
			<div class="formControls col-xs-5 col-sm-6"> <span class="select-box">
				<select class="select" name="uploadImgFlg" id="uploadImgFlg" size="1"  onchange="changeType()">
					<option value="0" <c:if test="${uploadImgFlg==0}">selected</c:if>>不上传</option>
					<option value="1" <c:if test="${uploadImgFlg==1}">selected</c:if>>上传</option>
				</select>
				</span> 
			</div>
		</div>	
		<div id="img" style="display: none;">
			<div class="row cl">
				<label class="form-label col-xs-4 col-sm-3" ><span class="c-red">*</span>影像上传地址：</label>
				<div class="formControls col-xs-5 col-sm-6">
					<input type="text" class="input-text" value="${url}" id="url" name="url" >
				</div>
			</div>
			<div class="row cl">
				<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>间隔周期：</label>
				<div class="formControls col-xs-5 col-sm-6">
					<input type="text" class="input-text" value="${time}"  maxlength="32" id="time" name="time">
				</div>
			</div>			
		</div>
		<br/>
		<br/>
		<div class="row cl" style="text-align: center;">
			<button class="btn btn-primary radius"  onclick="configImage()" type="button">保存配置</button>
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
	var uploadImgFlg=$("#uploadImgFlg").val();
	if(uploadImgFlg==1){
	    $("#img").css("display","block");	
	}else{
		$("#img").css("display","none");	
	}
})

/**
 * 根据输出格式显示或隐藏对应输入框
 */
function changeType(){
	var uploadImgFlg=$("#uploadImgFlg").val();
	if(uploadImgFlg==1){
	    $("#img").css("display","block");	
	}else{
		$("#img").css("display","none");	
	}
}
/**
* 保存配置
*/
function configImage() {
	var uploadImgFlg=$("#uploadImgFlg").val();	
	var url = $("#url").val().trim();
	var time = $("#time").val().trim();
	var checkInteger=/^[0-9]*$/;
	var checkIp = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])(\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])){3}$/;	
	//验证IPV6
	var checkIp6=/^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/;	
	
	var reg="^((https|http|ftp|rtsp|mms)?://)?" // schema
    	+ "(([0-9a-zA-Z_!~*\'().&=+$%-]+: )?[0-9a-zA-Z_!~*\'().&=+$%-]+@)?"//ftp的user@
    	+ "(([0-9]{1,3}\\.){3}[0-9]{1,3}" // IP形式的URL
    	+ "|" // 允许IP和DOMAIN（域名）
   		+ "([0-9a-zA-Z_!~*\'()-]+\\.)*" // 域名- www.
    	+ "([0-9a-zA-Z][0-9a-zA-Z-]{0,61})?[0-9a-zA-Z]\\." // 二级域名
    	+ "[a-zA-Z]{2,6})" // first level domain- .com or .museum
    	+ "(:[0-9]{1,4})?" // 端口- :80
    	+ "((/?)|" // a slash isn't required if there is no file name
    	+ "(/[0-9a-zA-Z_!~*\'().;?:@&=+$,%#-]+)+/?)$";
	
	if(uploadImgFlg.length==0){
      	layer.msg("请选择是否自动上传影像！",{icon:7,time:2000});
      	return false;
    }
	if(uploadImgFlg==1){
	 	if(url.length==0){
       		layer.msg("请输入影像上传地址！",{icon:7,time:2000});
       		return false;
     	}
	 	/* if(!new RegExp(reg).test(url)){
	 		layer.msg("请输入有效的影像上传地址！",{icon:7,time:2000});
        	return false;
	 	} */
		if(time.length==0){
	      	layer.msg("请输入间隔周期！",{icon:7,time:2000});
	      	return false;
	    }
		 if(!checkInteger.test(time)){
	 		layer.msg("间隔周期格式为[秒(31-60)]！",{icon:7,time:2000});
	      	return false;
	 	}	
		if(time>60||time<31){
			layer.msg("间隔周期格式为[秒(31-60)]！",{icon:7,time:2000});
	   		return false;
		}
	}
	$.ajax({
		url : "${ctx}/hsm/configImage.html",
		type : 'POST',
		crossOrigin : true,
		dataType : 'text',
		cache : false,
		async : true,
		data : {	
			"uploadImgFlg":uploadImgFlg,
			"url" : url,
			"time" : time
		},
		success : function(data) {
			if(data=="success"){
				layer.msg('保存配置成功!', {icon:1,time:2000},function() {	
// 					window.location.reload();
					window.location.href="${ctx}/hsm/systemManage.html?typeIndex=2";
				});
			}else if(data=="fail"){
				layer.msg('保存配置失败!', {icon:2,time:2000});
			}
		} ,
		error:function(data){
			layer.msg('出错了!', {icon:5,time:2000});
		}
	});
}
</script> 
</body>
</html>