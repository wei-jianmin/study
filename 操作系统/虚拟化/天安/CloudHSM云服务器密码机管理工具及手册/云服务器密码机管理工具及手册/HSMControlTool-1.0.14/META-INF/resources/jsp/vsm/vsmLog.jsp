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
<!--[if lt IE 9]>
<script type="text/javascript" src="lib/html5.js"></script>
<script type="text/javascript" src="lib/respond.min.js"></script>
<script type="text/javascript" src="lib/PIE_IE678.js"></script>
<![endif]-->
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui/css/H-ui.min.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/css/H-ui.admin.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/lib/Hui-iconfont/1.0.8/iconfont.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/lib/icheck/icheck.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/skin/default/skin.css" id="skin" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/css/style.css" />
<title>服务日志</title>

</head>
<body>
<nav class="breadcrumb">
	<i class="Hui-iconfont">&#xe67f;</i> 首页
 	<span class="c-gray en">&gt;</span> VSM管理
 	<span class="c-gray en">&gt;</span> VSM日志 
 	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" >
 		<i class="Hui-iconfont">&#xe68f;</i>
 	</a>
</nav>
<div class="page-container">
  <table class="table table-border table-bordered table-bg table-hover table-sort">
    <thead>
      <tr class="text-c">
        <th width="10%">序号</th>
        <th width="60%">文件名</th>
        <th width="20%">操作</th>
      </tr>
    </thead>
    <tbody>
	    <c:forEach items="${serverLogList}" var="item" varStatus="status">
	      	<tr class="text-c">
		        <td>${status.index+1}</td>
		        <td>${item.fileName}</td>
		        <td>
			        <a title="详情" style="color:#5a98de;" href="javascript:;" onclick="logDetail('${item.filePath}','${item.fileName}')" class="ml-5" style="text-decoration:none">
				    		详情&nbsp;&nbsp;
				    </a> 
				   <a title="下载" style="color:#5a98de;" href="javascript:;" href="javascript:;"  onclick="downloadLogContent('${item.filePath}','${item.fileName}')" class="ml-5" style="text-decoration:none">
							  下载&nbsp;&nbsp; 
				   </a>
				   <c:if test="${roleid!=2}">
				        <a title="删除" style="color:#dd514c;" href="javascript:;" onclick="deleteLogFile('${item.filePath}','${item.fileName}')" class="ml-5" style="text-decoration:none">
							删除&nbsp;&nbsp; 
					    </a>
			        </c:if>
			        <span style="display:none" id="${status.index+1}_fileContent">${item.fileContent}</span>
		        </td>
	      	</tr>
	    </c:forEach>
    </tbody>
  </table>
  <div id="pageNav" class="pageNav"></div>
</div>
<script type="text/javascript" src="${ctx}/lib/jquery/1.9.1/jquery.min.js"></script> 
<script type="text/javascript" src="${ctx}/lib/layer/2.1/layer.js"></script>
<script type="text/javascript" src="${ctx}/lib/datatables/1.10.0/jquery.dataTables.min.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui/js/H-ui.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui.admin/js/H-ui.admin.js"></script>
<script type="text/javascript" src="${ctx}/common/common.js"></script>
<script type="text/javascript">
$(function(){
	//渲染分页表
	$('.table-sort').dataTable({
		"columnDefs":[{"targets":[2], "searchable":false},//设置第六列不参与搜索
		              {"orderable":false,"aTargets":[2]}],//设置第六列不参与排序
		 "bFilter": false,    //去掉搜索框：这种方法可以
// 		 "bLengthChange": false,   //去掉每页显示多少条数据方法
	    "aaSorting": [[ 0, "asc" ]],//默认第几个排序
	  	"bStateSave": false,//状态保存
		"iDisplayLength" : 10 //默认显示的记录数  
	});
});
//判断是否存在
function isExist(filePath){
	var isExist="";
	//判断密钥别名是否存在
	$.ajax({
		type:"post",
		data:{"filePath":filePath},
		dateType:"text",
		async: false,
		url:"${ctx}/hsm/isExistFile.html",
		success:function(data){
			if(data=="yes"){//用户账号已存在
				isExist="yes";
			}else if(data=="no"){
				isExist="no";
			}
		},
		error:function(data){
			layer.closeAll();
			layer.msg('出错了', {icon:5,time:2000});
		}
	});	
	if(isExist=="no"){
		layer.confirm('该数据已被删除，是否获取最新数据!', function(index) {
			window.location.reload();
		});
		return false;
	}else{
		return true;
	}
}
//日志文件详情
function logDetail(filePath,fileName){
    filePath=filePath+"/"+fileName;
    if(isExist(filePath)){    
        layer_show("日志文件详情", '${ctx}/hsm/logDetail.html?filePath='+filePath+'&fileName='+fileName,'800','500');
    }
}
//日志下载
function downloadLogContent(filePath,fileName) {
	filePath=filePath+"/"+fileName;
	if(isExist(filePath)){ 
		layer.msg("下载日志成功！", {icon:1,time:2000},function() {
	       window.location.href="${ctx}/hsm/downLoadLogFile.html?filePath="+filePath+"&fileName="+fileName;
		});
	}
}
//日志删除
function deleteLogFile(filePath,fileName){
	layer.confirm('确认要删除吗？', function(index) {
		$.ajax({
			url : "${ctx}/hsm/deleteLogFile.html",
			type : 'POST',
			crossOrigin : true,
			dataType : 'text',
			cache : false,
			async : true,
			data : {
				"filePath" : filePath+"/"+fileName,
				"fileName" : fileName
			},
			beforeSend:function(){
				layer.load(3); 
			},
			timeout : 5000,
			success:function(data){
				layer.closeAll();
				if(data=="success"){
					layer.msg("删除日志成功", {icon:1,time:2000},function() {
						window.location.reload();					 
					});
				}else if(data=="fail"){
					layer.msg("删除日志失败", {icon:2,time:2000});
				}
			},
			error:function(data){
				layer.closeAll();
				layer.msg("出错了", {icon:5,time:2000});
			}
		});
	});
}
</script>
</body>
</html>