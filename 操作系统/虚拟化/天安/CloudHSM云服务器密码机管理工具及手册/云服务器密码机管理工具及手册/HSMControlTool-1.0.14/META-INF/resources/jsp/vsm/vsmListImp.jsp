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
<title>VSM管理</title>

</head>
<body>
<div class="page-container">
	<div class="mt-20">
	<input type="hidden" value="${vsm}" id="vsm"/>
		<table class="table table-border table-bordered table-hover table-bg table-sort">
			<thead>
				<tr class="text-c">
				    <th>序号</th>
					<th>vsmId</th>
					<!-- <th>IP</th> -->
					<th>操作</th>
				</tr>
			</thead>
			<tbody>
			<c:forEach items="${vsmList}" var="item" varStatus="status">
				<tr class="text-c">
				    <td>${status.index+1}</td>
					<td>${item.vsmid}</td>
					<%-- <td>${item.ip}</td> --%>
					<td class="td-manage">
				       <a title="选择" href="javascript:;" onclick="choseSym('${item.vsmid}')" class="ml-5" style="text-decoration:none;color:#5a98de;">
					   		选择
				       </a>
					</td>
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
$('.table-sort').dataTable({
	"columnDefs":[{"targets":[0], "searchable":false},//设置第一列不参与搜索
        {"targets":[2], "searchable":false},//设置最后一列不参与搜索
        {"orderable":false,"aTargets":[0]},//设置第一列不参与排序
        {"orderable":false,"aTargets":[2]}],//设置最后一列不参与排序
        "aaSorting": [[0, "asc" ]],//默认第几个排序
   	  	"bStateSave": false,//状态保存
   	    "iDisplayLength" : 50
});
function choseSym(vsmid){
	parent.$("#vsmid").val(vsmid);
	var vsm = $("#vsm").val();
	if(vsm==2){
		window.parent.$("#vsmMonitorInfo").click();
	}
	var index = parent.layer.getFrameIndex(window.name);
	parent.layer.close(index);
 }
</script> 
</body>
</html>