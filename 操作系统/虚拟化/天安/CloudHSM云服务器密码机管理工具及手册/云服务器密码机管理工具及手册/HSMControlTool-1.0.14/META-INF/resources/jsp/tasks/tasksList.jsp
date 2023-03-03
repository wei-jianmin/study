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
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui/css/H-ui.min.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/css/H-ui.admin.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/lib/Hui-iconfont/1.0.8/iconfont.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/lib/icheck/icheck.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/skin/default/skin.css" id="skin" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/css/style.css" />
<title>耗时任务管理</title>

</head>
<body>
<nav class="breadcrumb"><i class="Hui-iconfont">&#xe67f;</i> 首页 
	<span class="c-gray en">&gt;</span> 耗时任务管理
	<span class="c-gray en">&gt;</span> 耗时任务状态
	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" >
	<i class="Hui-iconfont">&#xe68f;</i>
	</a>
</nav>

<div class="page-container">
	<div class="mt-20">
		<table class="table table-border table-bordered table-hover table-bg table-sort">
			<thead>
				<tr class="text-c">
					<th><input type="checkbox" id="checkbox-list" name="checkAll"/></th>
					<th style="min-width:50px;">任务流水号</th>
					<th style="min-width:50px;">任务名称</th>
					<th style="min-width:50px;">任务开始时间</th>
					<th style="min-width:50px;">虚拟机Id</th>
					<!-- <th style="min-width:50px;">虚拟机类型</th> -->
					<th style="min-width:50px;">任务状态</th>
					<th style="min-width:100px;">刷新结果</th>
					<th style="min-width:150px;">任务信息</th>
				</tr>
			</thead>
			<tbody>
			<c:forEach items="${tasks}" var="item" varStatus="status">
				<tr class="text-c">
					<td >
						<input type="checkbox" name="uIds"  value="${item.requestId}" id="checkbox-list-${status.index}"></input>
					</td>
					<td>${item.requestId}</td>
					<td>${item.taskName}</td>
					<td>${item.startTime}</td>
					<td>${item.vsmId}</td>
					<%-- <td>${item.vsmType}</td> --%>
					<td>
						<c:choose>
							<c:when test="${item.taskStatus=='fail'}"><span style="color:red">处理失败</span></c:when>
							<c:when test="${item.taskStatus=='success'}"><span style="color:green">处理成功</span></c:when>
							<c:when test="${item.taskStatus=='handling'}"><span style="color:blue">处理中...</span></c:when>
						</c:choose>
					</td>
					<td>
						<c:choose>
							<c:when test="${item.updateStatus=='fail'}"><span style="color:red">刷新失败</span></c:when>
							<c:when test="${item.updateStatus=='success'}"><span style="color:green">刷新成功</span></c:when>
						</c:choose>
					</td>
					<td>${item.updateMsg}</td>
				</tr>
				</c:forEach>
			</tbody>
		</table>
	</div>
</div>
<script type="text/javascript" src="${ctx}/lib/jquery/1.9.1/jquery.min.js"></script> 
<script type="text/javascript" src="${ctx}/lib/layer/2.1/layer.js"></script>
<script type="text/javascript" src="${ctx}/lib/My97DatePicker/WdatePicker.js"></script> 
<script type="text/javascript" src="${ctx}/lib/datatables/1.10.0/jquery.dataTables.min.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui/js/H-ui.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui.admin/js/H-ui.admin.js"></script> 
<script type="text/javascript" src="${ctx}/common/common.js"></script>
<script type="text/javascript">
$(function(){
	$("[name='uIds']").prop("checked",false);
});
//分页列表
$('.table-sort').dataTable({
	"columnDefs":[{"targets":[0], "searchable":false},//设置第一列不参与搜索
	              {"targets":[6], "searchable":false},//设置第五列不参与搜索
	              {"orderable":false,"aTargets":[0]},//设置第一列不参与排序
	              {"orderable":false,"aTargets":[6]}],//设置最后一列不参与排序
    "aaSorting": [[ 3, "desc" ]],//默认第几个排序
  	"bStateSave": false,//状态保存
	"iDisplayLength" : 10 //默认显示的记录数  
});
$(function(){
	//全选功能
	$("#checkbox-list").click(function() {
		$("[name='uIds']").prop("checked", $(this).prop("checked"));
	});
	
	//全选操作相关
	$("[name='uIds']").click(function() {
		var j=0;
		var x = document.getElementsByName("uIds");
	
		for (var i = 0; i < x.length; i++) {
			if (x[i].checked)
				j++;
		}
		if(x.length==j)
		$("#checkbox-list").prop("checked", $(this).prop("checked"));
		else{
		document.getElementById("checkbox-list").checked=false;
		}
	});
});

	
	
	$(function(){
		window.setInterval(updateList, 10000);
	});
	function updateList(){
		window.location.reload();
	}
	
	function show(msg){
		$("#showMsg").attr("type","text");
	}
</script> 
</body>
</html>