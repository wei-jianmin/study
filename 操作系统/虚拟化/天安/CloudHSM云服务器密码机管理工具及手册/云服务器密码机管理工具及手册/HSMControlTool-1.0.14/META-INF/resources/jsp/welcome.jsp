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
<meta http-equiv="Pragma" content="no-cache">
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui/css/H-ui.min.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/css/H-ui.admin.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/lib/Hui-iconfont/1.0.8/iconfont.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/lib/icheck/icheck.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/skin/default/skin.css" id="skin" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/h-ui.admin/css/style.css" />

<title>欢迎页面</title>
<style type="text/css">
	body{ 
/* 		text-align:center;  */
		margin:0 auto;
/* 		background-image: url(${ctx}/images/xlogo.jpg); */
/* 		background-repeat: no-repeat; */
	} 
	pre{
		line-height:40px;
		font-size:20px;
	}
	.bg {
		margin:190px auto; 
		width:100%;
		font-size:20px;
	} 
</style>
</head>
<body onload="startTime()">
<div class="page-container">
<div style="margin-top:5px;">
	<div id="timeShow" style="float:right;margin-right:10px;"></div> 
</div>

	<br/><br/>
    <nav class="breadcrumb">
		<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" >
			<i class="Hui-iconfont">&#xe68f;</i>
		</a>
	</nav>		<table class="table table-border table-bordered table-bg table-hover table-sort" >
			<thead>
			    <tr class="text-c" >
					<th colspan="2" >设备信息 </th>
					<th colspan="2" >设备配置</th>
				</tr>
			</thead>
			<tbody>
				<tr class="text-c">
					<td width= "20% " style="font-weight:bold;">UUID </td>
					<td width= "30% ">${id} </td>
					<td width= "20% " style="font-weight:bold;">IPV4地址</td>
					<td width= "30% "> ${ip} </td>
				</tr>
				<tr class="text-c">
					<td width= "20% " style="font-weight:bold;">硬件型号</td>
					<td width= "30% ">${hardwareType} </td>
					<td width= "20% " style="font-weight:bold;">子网掩码</td>
					<td width= "30% "> ${mask} </td>
				</tr>
				<tr  class="text-c">			
					<td width= "20% " style="font-weight:bold;">系统版本</td>
					<td width= "30% "> ${systemVersion} </td>
					<td width= "20% " style="font-weight:bold;">网关地址</td>
					<td width= "30% "> ${gateway} </td>
				</tr>
				<tr  class="text-c">
					<td width= "20% " style="font-weight:bold;">管控版本</td>
					<td width= "30% ">${controlledVersion} </td>
					<td width= "20% " style="font-weight:bold;">dns服务器 </td>
					<td width= "30% "> ${dns} </td>								
				</tr>
				<tr  class="text-c">
					<td width= "20% " style="font-weight:bold;">密码卡版本</td>
					<td width= "30% "> ${cardVersion} </td>
					<td width= "20% " style="font-weight:bold;">VLAN-TAG</td>
					<td width= "30% "> ${vlanTag} </td>
				
				</tr>
				<tr  class="text-c">
					<td width= "20% " style="font-weight:bold;">设备序列号</td>
					<td width= "30% "> ${deviceSerial} </td>
					<td width= "20% " style="font-weight:bold;">MAC地址</td>
					<td width= "30% "> ${mac}</td>
				
				</tr>
				<tr  class="text-c">
					<td width= "20% " style="font-weight:bold;">总资源数</td>
					<td width= "30% "> ${totalRes} </td>
					<td width= "20% " style="font-weight:bold;">mtu</td>
					<td width= "30% "> ${mtu} </td>
				
				</tr>
				<tr  class="text-c">
					<td width= "20% " style="font-weight:bold;">剩余资源数</td>
					<td width= "30% ">${remainRes} </td>
					<td width= "20% " style="font-weight:bold;">ntp服务器地址</td>
					<td width= "30% "> ${ntpAddr}</td>
				
				</tr>
				<tr  class="text-c">
					<td width= "20% " style="font-weight:bold;">PKP公钥 </td>
					<td width= "30% ">${pkpKey}</td>
					<td width= "20% " style="font-weight:bold;">日志上传类型</td>
				    <td width= "30% ">
					    <c:choose>
					        <c:when test="${logType=='0'}">sls</c:when>
					        <c:when test="${logType=='1'}">日志文件服务器</c:when>
					        <c:when test="${logType=='2'}">syslog服务器</c:when>
					        <c:otherwise> </c:otherwise>
					    </c:choose>
					</td>
				</tr>
				<tr  class="text-c">
				    <td width= "20% " style="font-weight:bold;">运行状态 </td>
					<td width= "30% ">
					    <c:choose>
					        <c:when test="${status=='ok'}">正常</c:when>
					        <c:otherwise>异常</c:otherwise>
					    </c:choose>
					</td>
					
					<td width= "20% " style="font-weight:bold;">日志上传地址</td>
					<td width= "30% "> 　${logAddr} </td>
				
				</tr>
				<tr  class="text-c">
					<td width= "20% " style="font-weight:bold;">启动时间</td>
					<td width= "30% "> ${upTime} </td>
					<td width= "20% " style="font-weight:bold;">影像自动上传地址</td>
					<td width= "30% ">${imageUploaderUrl} </td>
				
				</tr>
				<tr  class="text-c">
					<td width= "20% " style="font-weight:bold;">restful服务状态</td>
					<td width= "30% ">
					    <c:choose>
					        <c:when test="${restfulStatus=='1'}">开启</c:when>
					        <c:when test="${restfulStatus=='0'}">关闭</c:when>
					        <c:otherwise>异常</c:otherwise>
					    </c:choose>
					</td>
					 <td width= "20% " style="font-weight:bold;">IPV6地址</td>
					<td width= "30% ">${ip6} </td>
				</tr>
				<tr  class="text-c">
					<td width= "20% " style="font-weight:bold;">IPV6子网前缀</td>
					<td width= "30% ">
					    ${ip6hlen}
					</td>
					 <td width= "20% " style="font-weight:bold;">IPV6网关</td>
					<td width= "30% ">${gateway6} </td>
				</tr>
			</tbody>
         </table> 
</div>
<script type="text/javascript" src="${ctx}/lib/jquery/1.9.1/jquery.min.js"></script> 
<script type="text/javascript" src="${ctx}/lib/Highcharts/highcharts.js"></script> 
<script type="text/javascript" src="${ctx}/lib/Highcharts/exporting.js"></script> 
<script type="text/javascript" src="${ctx}/lib/layer/2.1/layer.js"></script>
<script type="text/javascript" src="${ctx}/lib/My97DatePicker/WdatePicker.js"></script> 
<script type="text/javascript" src="${ctx}/lib/datatables/1.10.0/jquery.dataTables.min.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui/js/H-ui.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui.admin/js/H-ui.admin.js"></script> 
<script type="text/JavaScript" src="${ctx}/static/pdf/pdfobject.js"></script>
<script type="text/javascript"> 
function startTime(){ 
	var today=new Date(); 
	var strDate=(" "+today.getFullYear()+"年"+(today.getMonth()+1)+"月"+today.getDate()+"日"); 
	var n_day=today.getDay(); 
	switch(n_day){ 
	case 0: 
	{strDate=strDate+" 星期日 "}break; 
	case 1: 
	{strDate=strDate+" 星期一 "}break; 
	case 2: 
	{strDate=strDate+" 星期二 "}break; 
	case 3: 
	{strDate=strDate+" 星期三 "}break; 
	case 4: 
	{strDate=strDate+" 星期四 "}break; 
	case 5: 
	{strDate=strDate+" 星期五 "}break; 
	case 6: 
	{strDate=strDate+" 星期六 "}break; 
	case 7: 
	{strDate=strDate+" 星期日 "}break; 
	} 
	//增加时分秒 
	// add a zero in front of numbers<10 
	var h=today.getHours(); 
	var m=today.getMinutes(); 
	var s=today.getSeconds() 
	m=checkTime(m); 
	s=checkTime(s); 
	strDate=strDate+" "+h+":"+m+":"+s; 
	document.getElementById('timeShow').innerHTML=strDate; 
	t=setTimeout('startTime()',500) 
	} 
	
	function checkTime(i){ 
	if (i<10) {i="0" + i} 
	return i 
	} 
</script> 
</body>
</html>