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
<LINK rel="Bookmark" href="favicon.ico" >
<link rel="shortcut icon" href="favicon.ico" type="image/x-icon">
<link rel="stylesheet" type="text/css" href="static/h-ui/css/H-ui.min.css" />
<link rel="stylesheet" type="text/css" href="static/h-ui.admin/css/H-ui.admin.css" />
<link rel="stylesheet" type="text/css" href="static/iconfont/1.0.8/iconfont.css" />
<link rel="stylesheet" type="text/css" href="lib/icheck/icheck.css" />
<link rel="stylesheet" type="text/css" href="static/h-ui.admin/skin/default/skin.css" id="skin" />
<link rel="stylesheet" type="text/css" href="static/h-ui.admin/css/style.css" />
<title>云服务器密码机管理工具</title>
<link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon">
</head>
<body>
<header class="navbar-wrapper">
	<div class="navbar navbar-fixed-top">
		<div class="container-fluid cl" style="height:80px;background-image: url(${ctx}/images/topbg.png);"> 
			<a class="logo navbar-logo f-l mr-10 hidden-xs" href="index.html" style="color:black;height:80px;line-height:80px;">江南天安云服务器密码机管理工具</a> 
			<a aria-hidden="false" class="nav-toggle Hui-iconfont visible-xs" href="javascript:;">&#xe667;</a>
			<nav id="Hui-userbar" class="nav navbar-nav navbar-userbar hidden-xs">
				<ul class="cl" style="margin-right:20px;">
					<li class="dropDown dropDown_hover"> 
						<a href="#" class="dropDown_A" id="uname" style="color:black;height:80px;line-height:80px;">HSMIP:${hsmIp}
							<i class="Hui-iconfont">&#xe6d5;</i>
						</a>
						<ul class="dropDown-menu menu radius box-shadow">
							<li><a onclick="signOut()">切换账户</a></li>
							<%-- <li><a href="${ctx}/static/pdf/helpCenter.pdf" target="_blank">帮助中心</a></li> --%>
							<li><a onclick="signOut()">退出系统</a></li>
						</ul>
					</li>
				</ul>
			</nav>
		</div>
	</div>
</header>
<aside class="Hui-aside" style="margin-top:35px;">
	<input runat="server" id="divScrollValue" type="hidden" value="" />
	<div class="menu_dropdown bk_2" style="font-size: 16px;">
		<dl id="menu-system">
       	  	<dt><i class="Hui-iconfont">&#xe6b6;</i>HSM管理<i class="Hui-iconfont menu_dropdown-arrow">&#xe6d5;</i></dt>
			<dd>
				<ul>
                   <li><a _href="${ctx}hsm/networkConfig.html" data-title="网络配置" href="javascript:;">网络配置</a></li>	
                   <li><a _href="${ctx}hsm/logManage.html" data-title="日志管理" href="javascript:;">日志管理</a></li>
                   <li><a _href="${ctx}hsm/systemManage.html" data-title="系统配置" href="javascript:;">系统配置</a></li>
                   <li><a _href="${ctx}hsm/runStatusMonitor.html" data-title="运行监控" href="javascript:;">运行监控</a></li>
                   <li><a _href="${ctx}hsm/systemMaintenance.html" data-title="系统维护" href="javascript:;">系统维护</a></li>				
               </ul>
			</dd>
			<dt><i class="Hui-iconfont">&#xe639;</i>VSM管理<i class="Hui-iconfont menu_dropdown-arrow">&#xe6d5;</i></dt>
			<dd>
				<ul>
                   <li><a _href="${ctx}vsm/getVsmList.html" data-title="VSM管理" href="javascript:;">VSM管理</a></li>	
                   <li><a _href="${ctx}vsm/toVsmMonitorInfoResult.html" data-title="VSM监控" href="javascript:;">VSM监控</a></li>	     
               </ul>
			</dd>
			<dt><i class="Hui-iconfont">&#xe63c;</i>数据影像管理<i class="Hui-iconfont menu_dropdown-arrow">&#xe6d5;</i></dt>
			<dd>
				<ul>
                   <li><a _href="${ctx}image/toImport.html" data-title="导入影像" href="javascript:;">导入影像</a></li>	
                   <li><a _href="${ctx}image/toExport.html" data-title="导出影像" href="javascript:;">导出影像</a></li>
               </ul>
			</dd>
			<dt><i class="Hui-iconfont">&#xe72d;</i>耗时任务管理<i class="Hui-iconfont menu_dropdown-arrow">&#xe6d5;</i></dt>
			<dd>
				<ul>
                   <li><a _href="${ctx}tasks/tasksList.html" data-title="耗时任务管理" href="javascript:;">耗时任务管理</a></li>	
               </ul>
			</dd>
       	</dl>
    </div>
</aside>
<div class="dislpayArrow hidden-xs">
	<a class="pngfix" href="javascript:void(0);" onClick="displaynavbar(this)"></a>
</div>
<section class="Hui-article-box" style="margin-top:35px;">
	<div id="Hui-tabNav" class="Hui-tabNav hidden-xs">
		<div class="Hui-tabNav-wp">
			<ul id="min_title_list" class="acrossTab cl">
				<li class="active">
						<span title="我的密码机" data-href="welcome.html">
							我的密码机
						</span>
					<em></em>
				</li>
			</ul>
		</div>
		<div class="Hui-tabNav-more btn-group">
			<a id="js-tabNav-prev" class="btn radius btn-default size-S" href="javascript:;">
				<i class="Hui-iconfont">&#xe6d4;</i>
			</a>
			<a id="js-tabNav-next" class="btn radius btn-default size-S" href="javascript:;">
				<i class="Hui-iconfont">&#xe6d7;</i>
			</a>
		</div>
	</div>
	<div id="iframe_box" class="Hui-article">
		<div class="show_iframe">
			<div style="display:none" class="loading"></div>
               <iframe scrolling="yes" frameborder="0" src="${ctx}/welcome.html"></iframe>
		</div>
	</div>
</section>
<script type="text/javascript" src="lib/jquery/1.9.1/jquery.min.js"></script> 
<script type="text/javascript" src="lib/layer/2.1/layer.js"></script> 
<script type="text/javascript" src="static/h-ui/js/H-ui.js"></script> 
<script type="text/javascript" src="static/h-ui.admin/js/H-ui.admin.js"></script> 
<script type="text/javascript">

/**退出登录*/
function signOut(){
	window.location.href="${ctx}/signOut.html";
}
/**刷新*/
function toIndex(){
	window.location.href="${ctx}/index.html";
}
/**帮助中心*/
function alertPDF(){
	layer_show("帮助中心", '${ctx}/static/pdf/helpCenter.pdf','1000','600');
}
</script> 
</body>
</html>