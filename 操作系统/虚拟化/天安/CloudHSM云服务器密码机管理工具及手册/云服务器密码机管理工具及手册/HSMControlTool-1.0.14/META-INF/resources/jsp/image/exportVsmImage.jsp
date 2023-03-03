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

<title>导出影像</title>
<meta name="keywords" content="H-ui.admin ">
<meta name="description" content="H-ui.admin ">
</head>
<body>
<nav class="breadcrumb"><i class="Hui-iconfont">&#xe67f;</i> 首页 
	<span class="c-gray en">&gt;</span> 数据影像管理
	<span class="c-gray en">&gt;</span> 导出影像
	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" >
	<i class="Hui-iconfont">&#xe68f;</i>
	</a>
</nav>
<article class="page-container">
	<form action="" method="post" class="form form-horizontal" id="form-member-add" >
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3" style="text-align: right;"><span class="c-red">*</span>选择VSM：</label>
			<div class="formControls col-xs-4 col-sm-3">
				<input type="text" class="input-text" value="${vsmid}"  id="vsmid" name="vsmid" readonly="readonly">
			</div>
			<button onclick="selectParent();" class="btn btn-primary radius" id="selectPar" type="button">选择</button>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-4 col-sm-3">导出内容：</label>
			<div class="formControls col-xs-4 col-sm-3"> <span class="select-box">
				<select class="select" name="format" id="format" size="1" >
					<option value="1"<c:if test="${format=='1'}">selected</c:if>>影像</option>
					<option value="2"<c:if test="${format=='2'}">selected</c:if>>密钥</option>
				</select>
				</span> 
			</div>
		</div>
		<div class="row cl">
			<div class="col-xs-8 col-sm-9 col-xs-offset-4 col-sm-offset-3">
				 <button class="btn btn-primary radius"  onclick="exportVsm()" type="button">导出</button>
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
<script type="text/javascript">

/**
* 导出影像
*/
function exportVsm() {	
	var vsmid = $("#vsmid").val().trim();
	var format = $("#format").val().trim();
	if(vsmid.length<=0){
		layer.msg('vsmId不能为空', {icon:7,time:2000});
		return false;
	}
	$.ajax({
		url : "${ctx}/image/exportVsmImage.html",
		type : 'POST',
		crossOrigin : true,
		dataType : 'text',
		cache : false,
		async : true,
		data : {			
			"vsmid" : vsmid,
			"format" : format,
		},
		beforeSend:function(){
			layer.load(5); //转圈圈的效果
		},
		success : function(data) {
			var result = data.split(",");
			var url = result[1];
			var sign = result[2];
			if(result[0]=="success"){
				window.location.href=url;//下载导出的影像数据
				layer.confirm("导出影像成功,签名内容为:"+sign+",是否下载签名内容？", function(index) {
					window.location.href="${ctx}/image/downLoadSign.html?sign="+sign;	
					layer.msg('下载成功!', {icon : 1,time : 2000}, function() {
						window.parent.$("[data-title='耗时任务管理']").click();
						layer.load(2);
						window.location.reload();
					});
				},function(index){
					window.parent.$("[data-title='耗时任务管理']").click();
					layer.load(2);
					window.location.reload();
				});
			}else if(result[0]=="fail"){
				layer.msg("导出失败", {icon:2,time:2000});
			}else if(result[0]=="statusFail"){
				layer.msg("VSM关闭,请重启再试", {icon:2,time:2000});
			}
			
		} ,
		error:function(data){
			layer.msg('出错了', {icon:5,time:2000});
		}
	});
}
/**
 * 选择VSM列表
 */
function selectParent(){
	 layer_show("选择VSM", '${ctx}/vsm/getVsmList.html?vsm=1','600','350');
} 
</script> 
</body>
</html>