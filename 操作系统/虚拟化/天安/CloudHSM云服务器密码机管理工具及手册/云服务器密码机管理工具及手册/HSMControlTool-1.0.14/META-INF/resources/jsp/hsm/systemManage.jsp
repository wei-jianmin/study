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

<title>系统管理</title>
<meta name="keywords" content="H-ui.admin ">
<meta name="description" content="H-ui.admin ">
</head>
<body>
    <nav class="breadcrumb">
		<i class="Hui-iconfont">&#xe67f;</i> 首页 
		<span class="c-gray en">&gt;</span> HSM管理
		<span class="c-gray en">&gt;</span> 系统配置
		<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" >
			<i class="Hui-iconfont">&#xe68f;</i>
		</a>
	</nav>
	<div class="page-container">
	<input type="hidden" value="${typeIndex}"  id="typeIndex">
		<div class="mt-20">
		    <div id="tab-system" class="HuiTab">
			    <div class="tabBar cl">
				  <span onclick="load('0')">系统时间</span>
				  <span onclick="load('1')">认证公钥</span>
				  <span onclick="load('2')">影像自动上传</span>
				  <span onclick="load('3')">Restful服务</span>
				  <span onclick="load('4')">日志配置</span>
			   </div>
			   <!--系统时间  -->
			   <div class="tabCon">
			       <article class="page-container" id="systemTime">						

	              </article>
               </div>			
			   <!--认证公钥-->
			   <div class="tabCon">
			       <article class="page-container" id="publicKey">						

	              </article>
               </div>
               <!--影像自动上传  -->
			   <div class="tabCon">
			       <article class="page-container" id="image">						

	              </article>
               </div>			
			   <!-- Restful服务 -->
			   <div class="tabCon">
			       <article class="page-container" id="restful">						

	              </article>
               </div>
               <!--日志配置  -->
			   <div class="tabCon" >
					<article class="page-container" id="logConfig">	
							
					</article>
               </div>	
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
$(function(){
	var typeIndex=$("#typeIndex").val().trim();
	if(typeIndex=='0'){
		load(0);
	}else if(typeIndex=='1'){
		load(1);
	}else if(typeIndex=='2'){
		load(2);
	}else if(typeIndex=='3'){
		load(3);
	}else if(typeIndex=='4'){
		load(4);
	}else{
		load(0);
	}
	$('.skin-minimal input').iCheck({
		checkboxClass: 'icheckbox-blue',
		radioClass: 'iradio-blue',
		increaseArea: '20%'
	});	
	$.Huitab("#tab-system .tabBar span","#tab-system .tabCon","current","click",typeIndex);
});
//加载签发证书页面
function load(type){
	var curUrl = "${ctx}/hsm/timeConfig.html";
	if(type=='0'){
		curUrl = "${ctx}/hsm/timeConfig.html";
	}else if(type=='1'){
		curUrl = "${ctx}/hsm/publicKeyConfig.html";
	}else if(type=='2'){
		curUrl = "${ctx}/hsm/imageConfig.html";
	}else if(type=='3'){
		curUrl = "${ctx}/hsm/restfulConfig.html";
	}else if(type=='4'){
		curUrl = "${ctx}/hsm/logConfig.html";
	}  
	$.ajax({
		type : "POST",
		data : {},
		url : curUrl,
		dataType: "text",
		beforeSend:function(){
			layer.load(3); 
		},
		success : function(data) {
			layer.closeAll();
			if(type=='0'){
				$("#systemTime").html(data);
			}else if(type=='1'){
				$("#publicKey").html(data);
			}else if(type=='2'){
				$("#image").html(data);
			}else if(type=='3'){
				$("#restful").html(data);
			}else if(type=='4'){
				$("#logConfig").html(data);
			}  
		},
		error:function(){
			layer.closeAll();
			$("#systemTime").html("");
			layer.msg('出错了！', {icon:5,time:2000});
		}
	});
}
</script>
</body>
</html>