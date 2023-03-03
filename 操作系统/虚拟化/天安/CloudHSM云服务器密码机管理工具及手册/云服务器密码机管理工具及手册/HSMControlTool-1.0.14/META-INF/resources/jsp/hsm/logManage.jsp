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

<title>日志管理</title>
<meta name="keywords" content="H-ui.admin ">
<meta name="description" content="H-ui.admin ">
</head>
<body>
<nav class="breadcrumb">
	<i class="Hui-iconfont">&#xe67f;</i> 首页 
	<span class="c-gray en">&gt;</span> HSM管理
	<span class="c-gray en">&gt;</span> 日志管理 
	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" >
		<i class="Hui-iconfont">&#xe68f;</i>
	</a>
</nav>
 <article class="page-container">
	<form action="" method="post" class="form form-horizontal" id="form-member-add" >
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3"><span class="c-red">*</span>日志类型:</label>
			<div class="formControls col-xs-5 col-sm-6"> <span class="select-box">
				<select class="select" name="logType" id="logType" size="1">
					<option value="0">HSM日志（系统、管控）</option>
					<option value="1">硬件监控日志</option>
				</select>
				</span> 
			</div>
		</div>	
		<br/><br/><br/>
		<div class="row cl" style="text-align: center;">
				 <button onClick="logDownload();" class="btn btn-primary radius" type="button" style="margin-left:20px;">下载</button>
	    </div>		
	</form>
</article>
<!--_footer 作为公共模版分离出去--> 
<script type="text/javascript" src="${ctx}/lib/jquery/1.9.1/jquery.min.js"></script> 
<script type="text/javascript" src="${ctx}/lib/layer/2.1/layer.js"></script>
<script type="text/javascript" src="${ctx}/lib/datatables/1.10.0/jquery.dataTables.min.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui/js/H-ui.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui.admin/js/H-ui.admin.js"></script>
<script type="text/javascript" src="${ctx}/lib/icheck/jquery.icheck.min.js"></script> 
<script type="text/javascript" src="${ctx}/common/common.js"></script>
<script type="text/javascript">
function logDownload(){
	var logType=$("#logType").val();
	$.ajax({
		url : "${ctx}/hsm/logDownload.html",
		type : 'POST',
		crossOrigin : true,
		dataType : 'text',
		cache : false,
		async : true,
		data : {"logType":logType},
		beforeSend:function(){
			layer.load(5); //转圈圈的效果
		},
		success : function(data) {
			layer.closeAll();	
			var result = data.split(",");
			var flag=result[0];
			var urls=result[1];
			if(result[0]=="success"){
				if(logType==0){
					
					layer.open({
					    type: 1
					    ,title: "VSM日志下载" //不显示标题栏   title : false/标题
					    ,closeBtn: false
					    ,area: '888px;'
					    ,shade: 0.8
					    ,resize: false
					    ,btn: ['关闭']
					    ,moveType: 1 //拖拽模式，0或者1
					    ,content: '<div style="padding: 50px; line-height: 22px; font-weight: 200;"><B>复制下面日志地址到浏览器下载：</B><br>'+urls.split(" ")[0]+'<br>'+urls.split(" ")[1]+'</div>'
					    ,btn1:function(){ //按钮1的回调
					    	layer.close();
					    }
					});
					
					/* layer.msg('下载成功!', {icon:1,time:2000},function() {	
					//	window.location.href=urls.split(" ")[0];
						window.open(urls.split(" ")[0]);
					});
					layer.msg('下载成功!', {icon:1,time:2000},function() {	
					//	window.location.href=urls.split(" ")[1];
						window.open(urls.split(" ")[1]);
					}); */
				}else {
					
					layer.open({
					    type: 1
					    ,title: "VSM日志下载" //不显示标题栏   title : false/标题
					    ,closeBtn: false
					    ,area: '888px;'
					    ,shade: 0.8
					    ,resize: false
					    ,btn: ['关闭']
					    ,moveType: 1 //拖拽模式，0或者1
					    ,content: '<div style="padding: 50px; line-height: 22px; font-weight: 200;"><B>复制下面日志地址到浏览器下载：</B><br>'+urls+'</div>'
					    ,btn1:function(){ //按钮1的回调
					    	layer.close();
					    }
					});
					
					/* layer.msg('下载成功!', {icon:1,time:2000},function() {	
					//	window.location.href=urls;
						window.open(urls);
					}); */
				}					
			}else{
				layer.msg('下载失败！', {icon:2,time:2000});
			}
		} ,
		error:function(data){
			layer.closeAll();
			layer.msg('出错了', {icon:5,time:2000});
		}
	});
}
</script>
</body>
</html>