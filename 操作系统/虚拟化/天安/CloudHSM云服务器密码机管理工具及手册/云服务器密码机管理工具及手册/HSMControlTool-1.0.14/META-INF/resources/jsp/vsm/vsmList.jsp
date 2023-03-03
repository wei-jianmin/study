<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ include file="/common/ctx.jsp"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta charset="utf-8">
<meta name="renderer" content="webkit|ie-comp|ie-stand">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport"content="width=device-width,initial-scale=1,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no" />
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
	<nav class="breadcrumb"> <i class="Hui-iconfont">&#xe67f;</i> 首页
	<span class="c-gray en">&gt;</span> VSM管理 <span class="c-gray en">&gt;</span>
	VSM管理 <a class="btn btn-success radius r"
		style="line-height:1.6em;margin-top:3px" href="javascript:void(0);"
		title="刷新" onclick="refresh()"> <i class="Hui-iconfont">&#xe68f;</i>
	</a> </nav>

	<div class="page-container">
		<div class="cl pd-5 bg-1 bk-gray mt-20">
			<span class="l"> <input type="hidden" value="${curUserId}"
				id="curUserId" /> <a href="javascript:;" onclick="vsmAdd();"
				class="btn btn-primary radius"> <i class="Hui-iconfont">&#xe600;</i>
					创建VSM
			</a> <a href="javascript:;" onclick="tokenEdit();"
				class="btn btn-primary radius"> <i class="Hui-iconfont">&#xe60c;</i>
					修改token
			</a> 
			<a href="javascript:;" onclick="networkBatch();"
				class="btn btn-primary radius"> <i class="Hui-iconfont">&#xe60c;</i>
					批量配置
			</a> 
			</span>
		</div>
		<div class="mt-20">
			<table
				class="table table-border table-bordered table-hover table-bg table-sort">
				<thead>
					<tr class="text-c">
						<th><input type="checkbox" id="checkbox-list" name="checkAll" /></th>
						<th style="min-width:50px;">序号</th>
						<th style="min-width:200px;">UUID</th>
						<th style="min-width:95px;">IP</th>
						<th style="min-width:50px;">状态</th>
						<th style="min-width:50px;">token</th>
						<th style="min-width:50px;">类型</th>
						<th style="min-width:55px;">版本号</th> 
						<th style="min-width:200px;">操作</th>
					</tr>
				</thead>
				<tbody>
					<c:forEach items="${vsmList}" var="item" varStatus="status">
						<tr class="text-c">
							<td><input type="checkbox" name="uIds" value="${item.vsmid}"
								id="checkbox-list-${status.index}"></input> <span
								style="display:none">${item.status}</span></td>
							<td>${ status.index + 1}</td>
							<td><a title="${item.vsmid}"
								onclick="vsmDetails('${item.vsmid}')" href="javascript:void(0)"
								style="color:#5a98de;">${item.vsmid}</a></td>
							<td>${item.ip}</td>
							<td>${item.status}</td>
							<td>${item.token}</td>
							<td>${item.type}</td>
							<td>${item.version}</td>
							<!-- <td style="min-width:50px;"></td> -->
							<td class="td-manage">
								<a title="VSM状态管理" style="color:#5eb95e;" href="javascript:;" onclick="configVsmStatus('${item.vsmid}');" class="ml-5"> VSM状态管理&nbsp;&nbsp; </a>
							
								<%-- <a title="停止" style="color:#dd514c;" href="javascript:;" onclick="updateVsmStatus('${item}');" class="ml-5"> 停止&nbsp;&nbsp; </a>
								<a title="启动" style="color:#5eb95e;" href="javascript:;" onclick="updateVsmStatus('${item}');" class="ml-5" style="text-decoration:none"> 启动&nbsp;&nbsp; </a>
								<a title="重启" style="color:#5eb95e;" href="javascript:;" onclick="restart('${item}');" class="ml-5" style="text-decoration:none"> 重启&nbsp;&nbsp; </a>
								<a title="重置" style="color:#5eb95e;" href="javascript:;" onclick="resetVsm('${item}');" class="ml-5" style="text-decoration:none"> 重置&nbsp;&nbsp; </a>
							    <a title="删除" style="color:#5eb95e;" href="javascript:;" onclick="deleteVSM('${item}')" class="ml-5" style="text-decoration:none"> 删除&nbsp;&nbsp; </a> --%>
								
								
								<a title="VSM配置" style="color:#5eb95e;" href="javascript:;" onClick="vsmEdit('${item.vsmid}');" style="text-decoration:none"> VSM配置&nbsp;&nbsp; </a>
								<a title="下载日志" style="color:#5eb95e;" href="javascript:;" onClick="logVsm('${item.vsmid}');" style="text-decoration:none"> 下载日志&nbsp;&nbsp; </a>
								
								
								<%-- <c:choose>
								<c:when test="${item.status=='ok'}">
										<a title="停止" style="color:#dd514c;" href="javascript:;"
											onclick="updateVsmStatus('${item.vsmid}','${item.status}','true');"
											class="ml-5"> 停止&nbsp;&nbsp; </a>
										<a title="配置" style="color:#5eb95e;" href="javascript:;"
											onClick="vsmEdit('${item.vsmid}');"
											style="text-decoration:none"> 配置&nbsp;&nbsp; </a>
										<a title="下载日志" style="color:#5eb95e;" href="javascript:;"
											onClick="logVsm('${item.vsmid}');"
											style="text-decoration:none"> 下载日志&nbsp;&nbsp; </a>
										<a title="重置" style="color:#dd514c;" href="javascript:;"
											onclick="resetVsm('${item.vsmid}');" class="ml-5"
											style="text-decoration:none"> 重置&nbsp;&nbsp; </a>
										<a title="重启" style="color:#dd514c;" href="javascript:;"
											onclick="restart('${item.vsmid}');" class="ml-5"
											style="text-decoration:none"> 重启&nbsp;&nbsp; </a>
									</c:when>
									<c:otherwise>

										<a title="启动" style="color:#dd514c;" href="javascript:;"
											onclick="updateVsmStatus('${item.vsmid}','no','false');"
											class="ml-5" style="text-decoration:none"> 启动&nbsp;&nbsp;
										</a>
										<a title="删除" style="color:#dd514c;" href="javascript:;"
											onclick="deleteVSM('${item.vsmid}','${item.status}')"
											class="ml-5" style="text-decoration:none"> 删除&nbsp;&nbsp;
										</a>
									</c:otherwise>
								</c:choose> 
								<a title="升級" style="color:#5eb95e;" href="javascript:;"
								onclick="upgradeVsm('${item.version}','${item.vsmid}','${item.digest}')"
								class="ml-5" style="text-decoration:none"> 升級&nbsp;&nbsp; </a> --%>
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
		$(function() {
			$("[name='uIds']").prop("checked", false);
		})
		//分页列表
		$('.table-sort').dataTable({
			"columnDefs" : [ {"targets" : [ 0 ],"searchable" : false},//设置第一列不参与搜索
			{"targets" : [ 3 ],"searchable" : false},//设置第4列不参与搜索
			{"orderable" : false,"aTargets" : [ 0 ]},//设置第一列不参与排序
			{"orderable" : false,"aTargets" : [ 3 ]} ],//设置第五列不参与排序
			"aaSorting" : [ [ 1, "asc" ] ],//默认第几个排序
			"bStateSave" : false,//状态保存
			"iDisplayLength" : 50});
		$(function() {
			//全选功能
			$("#checkbox-list").click(function() {
				$("[name='uIds']").prop("checked", $(this).prop("checked"));
			});

			//全选操作相关
			$("[name='uIds']").click(function() {
				var j = 0;
				var x = document.getElementsByName("uIds");

				for ( var i = 0; i < x.length; i++) {
					if (x[i].checked)
						j++;
				}
				if (x.length == j){
					$("#checkbox-list").prop("checked",
					$(this).prop("checked"));
				}else {
					document.getElementById("checkbox-list").checked = false;
				}
			});
		});

		function refresh() {
			layer.load();
			window.location.reload();
		}

		//获取所有的选中的多选框
		function getSelected() {
			var selected = new Array();
			var checkbox = $("[name='uIds']");
			var j = 0;
			for ( var i = 0; i < checkbox.length; i++) {
				if (checkbox[i].checked) {
					selected[j] = checkbox[i];
					j++;
				}
			}
			return selected;
		}

		//是否有选中的多选框
		function isSelected() {
			var selected = getSelected();
			if (selected.length == 0)
				return false;
			return true;
		}

		//是否选中一个多选框
		function isSelectedOne() {
			var selected = getSelected();
			if (selected.length == 1)
				return true;
			return false;
		}

		//是否全都开机
		function isStatus() {
			var selected = getSelected();
			for ( var i = 0; i < selected.length; i++) {
				var status = $(selected[i]).next().html();
				console.log(status);
				if (status == "")
					return false;
			}
			return true;

		}

		//批量配置token
		function tokenEdit() {
			if (!isSelected()) {
				layer.msg("至少选中一个VSM进行操作", {icon : 7,time : 2000});
				return false;
			}
			if (!isStatus()) {
				layer.msg("不能有关机的VSM", {icon : 7,time : 2000});
				return false;
			}
			var selected = getSelected();
			var param;
			for ( var i = 0; i < selected.length; i++) {
				if (i == 0) {
					param = selected[i].value
				} else {
					param = param + "," + selected[i].value;
				}

			}

			layer_show("配置token", '${ctx}/vsm/tokenView.html?vsmIds=' + param,'500', '180');

		}

		//批量配置网络
		function networkBatch() {
			if (!isSelected()) {layer.msg("至少选中一个VSM进行操作", {icon : 7,time : 2000});
				return false;
			}
			if (!isStatus()) {
				layer.msg("不能有关机的VSM", {icon : 7,time : 2000});
				return false;
			}
			var selected = getSelected();
			var vsmIds;
			for ( var i = 0; i < selected.length; i++) {
				if (i == 0) {
					vsmIds = selected[i].value
				} else {
					vsmIds = vsmIds + "," + selected[i].value;
				}

			}

			layer_show("配置网络", '${ctx}/vsm/networkBatchView.html?vsmIds='+ vsmIds, '900', '500');

		}

		//VSM添加页面跳转
		function vsmAdd() {
			layer_show("创建VSM", '${ctx}/vsm/addView.html', '600', '340');
		}
		
		//vsm状态管理
		function configVsmStatus(vsmId){
			layer_show("VSM状态管理", '${ctx}/vsm/toConfigStatus.html?vsmId=' + vsmId,'600', '350');
		}

		//VSM修改页面跳转
		function vsmEdit(vsmId) {
			layer_show("VSM配置", '${ctx}/vsm/editView.html?vsmId=' + vsmId,'900', '600');
		}

		//VSM详情页面跳转
		function vsmDetails(vsmId) {
			layer_show("VSM详情", '${ctx}/vsm/detailsView.html?vsmId=' + vsmId,'900', '550');
		}
		
		

		//VSM详情页面跳转
		// 	function vsmDetails(vsmId){
		// 		layer_show("VSM详情", '${ctx}/vsm/detailsView.html?vsmId='+vsmId,'600','500');
		// 	}
		//svm升级
		function upgradeVsm(vsmid) {
			layer_show("VSM升级", '${ctx}/version/toUpgradeVsm.html?vsmid='+ vsmid, '600', '350');

		}

		

		//下载日志
		function logVsm(vsmId) {

			var index = layer.load();
			$.ajax({
				url : "${ctx}/vsm/getLogVsm.html",
				type : 'POST',
				crossOrigin : true,
				dataType : 'text',
				cache : false,
				async : true,
				data : {
					"vsmId" : vsmId
				},
				timeout : 5000,
				success : function(data) {
					layer.close(index);
					if (data == "fail") {
						layer.msg('VSM日志下载失败', {
							icon : 2,
							time : 2000
						}, function() {
							setTimeout(function() {
								layer_close();
							}, 500);
						});
					} else if (data == "status") {
						layer.msg('VSM关闭,请重启再试', {
							icon : 7,
							time : 2000
						}, function() {
							layer.load();
							window.location.reload();
						});
					} else if (data == "operation") {
						layer.msg('有VSM在操作', {
							icon : 7,
							time : 2000
						}, function() {
							setTimeout(function() {
								layer_close();
							}, 500);
						});
					} else {
						var datas = data.split(" ");
						
						layer.open({
						    type: 1
						    ,title: "VSM日志下载" //不显示标题栏   title : false/标题
						    ,closeBtn: false
						    ,area: '888px;'
						    ,shade: 0.8
						    ,resize: false
						    ,btn: ['关闭']
						    ,moveType: 1 //拖拽模式，0或者1
						    ,content: '<div style="padding: 50px; line-height: 22px; font-weight: 200;"><B>复制下面日志地址到浏览器下载：</B><br>'+datas[0]+'<br>'+datas[1]+'</div>'
						    ,btn1:function(){ //按钮1的回调
						    	layer.close();
						    }
						});
						
					}
				},
				error : function(data) {
					layer.close(index);
					layer.closeAll();
					layer.msg('出错了', {
						icon : 5,
						time : 2000
					});
				}
			});

		}

		
	</script>
</body>
</html>