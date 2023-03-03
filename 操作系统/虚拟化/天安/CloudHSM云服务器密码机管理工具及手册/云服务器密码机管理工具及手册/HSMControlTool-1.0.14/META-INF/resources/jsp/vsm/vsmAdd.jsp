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

<title>添加用户</title>
<meta name="keywords" content="">
<meta name="description" content="">
</head>
<body>
<article class="page-container">
	<form action="" method="post" class="form form-horizontal" id="form-member-add" >
		<div class="row cl">
			<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>类型：</label>
			<div class="formControls col-xs-8 col-sm-9"> <span class="select-box">
				<select class="select" size="1" name="vsmType" id="vsmType">
						<option value="">请选择</option>
						<option value="E">EVSM</option>
						<option value="G">GVSM</option>
						<option value="S">SVSM</option>
				</select>
				</span> 
			</div>
		</div>
		<div class="row cl">
			<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>剩余资源数：</label>
			<div class="formControls col-xs-8 col-sm-9">
				<input type="text" class="input-text" value="" placeholder="${remainRes}" id="remainRes" name=remainRes  maxlength="32" readonly="readonly">
			</div>
		</div>		
		<div class="row cl">
			<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>占用资源数：</label>
			<div class="formControls col-xs-8 col-sm-9">
				<input type="text" class="input-text" value="" placeholder="请输入的VSM的占用资源数" id="resouces" name=resouces  maxlength="32">
			</div>
		</div>
		<!-- <div class="row cl">
			<label class="form-label col-xs-3 col-sm-3" style="text-align: right;"><span class="c-red">*</span>创建数量：</label>
			<div class="formControls col-xs-8 col-sm-9">
				<input type="text" class="input-text" value="" placeholder="请输入需要创建的数量" id="number" name=number  maxlength="32">
			</div>
		</div> -->			
		<div class="row cl">
			<div class="col-xs-8 col-sm-9 col-xs-offset-4 col-sm-offset-3">
				 <button class="btn btn-primary radius"  onclick="vsmAdd()" type="button">添加</button>
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

	/**
	* 添加用户
	*/
	function vsmAdd() {
		var resouces = $("#resouces").val();
		var vsmType = $("#vsmType").val();
		var number = 1;
		var remainRes = $("#remainRes")[0].placeholder;
		var nu=/^\+?[1-9][0-9]*$/;//只能是数字
		var checkPwdRE =/^[^ ]+$/;//不能包含空格
		if(vsmType==""){
			layer.msg("请选择类型", {icon:7,time:2000});
			return false;
		}
		if(resouces.length==0){
			layer.msg("资源数不能为空", {icon:7,time:2000});
			return false;
		}
		if(!checkPwdRE.test(resouces)){
		 	layer.msg("资源数不能包含空格！",{icon:7,time:2000});
	      	return false;
		}
		if(!nu.test(resouces)){
		 	layer.msg("资源数只能是正整数！",{icon:7,time:2000});
	      	return false;
		}
		
		/* if(number.length==0){
			layer.msg("创建数量不能为空", {icon:7,time:2000});
			return false;
		}
		if(!checkPwdRE.test(number)){
		 	layer.msg("创建数量不能包含空格！",{icon:7,time:2000});
	      	return false;
		}
		if(!nu.test(number)){
		 	layer.msg("创建数量只能是正整数！",{icon:7,time:2000});
	      	return false;
		} */
		
		if((number*resouces)>remainRes){
		 	layer.msg("创建需要的资源数大于剩余资源数！",{icon:7,time:2000});
	      	return false;
		}
		
		var index =layer.load();
		
		$.ajax({
			url : "${ctx}/vsm/addVsm.html",
			type : 'POST',
			crossOrigin : true,
			dataType : 'text',
			cache : false,
			async : true,
			data : {
				"resouces" : resouces,
				"vsmType" : vsmType,
				"number" : number
			},
			success : function(data) {
				layer.close(index);
				if(data=="success"){
					layer.msg('正在添加VSM,请查看耗时任务！', {
						icon : 1,
						time : 2000
					}, function() {
						window.top.$("[data-title='耗时任务管理']").click();
						layer.load(2);
						window.parent.location.reload(); 
					});
				}else if(data=="fail"){
					layer.msg('添加VSM失败', {icon:2,time:2000});
				}else if(data=="resouces"){
					layer.msg('HSM资源不足', {icon:2,time:2000});
				}else if(data=="operation"){
					layer.msg('有VSM在操作', {icon:7,time:2000},function() {	
					});
				}
			} ,
			error:function(data){
				layer.close(index);
				layer.msg('出错了', {icon:5,time:2000});
			}
		});
	}
</script> 
<!--/请在上方写此页面业务相关的脚本-->
</body>
</html>