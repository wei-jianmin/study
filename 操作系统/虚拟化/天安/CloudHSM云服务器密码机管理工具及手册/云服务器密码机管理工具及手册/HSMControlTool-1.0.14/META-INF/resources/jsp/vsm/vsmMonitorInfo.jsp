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

<title>运行状态监控</title>
<meta name="keywords" content="H-ui.admin ">
<meta name="description" content="H-ui.admin ">
<body>
<nav class="breadcrumb">
	<i class="Hui-iconfont">&#xe67f;</i> 首页
 	<span class="c-gray en">&gt;</span> VSM管理
	<span class="c-gray en">&gt;</span> VSM监控
 	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" >
 		<i class="Hui-iconfont">&#xe68f;</i>
 	</a>
</nav>
<div class="page-container" style="width: 1210px; margin: 0 auto">

	<br/><br/>
	   <div class="row cl">
			<label class="form-label col-xs-3 col-sm-2" style="text-align: right;">选择VSM：</label>
			<div class="formControls col-xs-4 col-sm-4" >
				<input type="text" class="input-text" value="${vsmid}" id="vsmid" name="vsmid" readonly="readonly">
			</div>
			<button onclick="selectParent();" class="btn btn-primary radius" id="selectPar" type="button">选择</button>
			<button class="btn btn-primary radius"  onclick="vsmMonitorInfo()" id="vsmMonitorInfo" type="button">获取监控信息</button>
		</div><br/>
		<table class="table table-border table-bordered table-bg table-hover table-sort" >
			<thead>
			    <tr class="text-c" >
					<th colspan="6" >VSM监控信息</th>
				</tr>
			</thead>
			<tbody>
				<tr class="text-c">
					<td width= "4%" style="font-weight:bold;">管控服务版本号</td>
					<td width= "10% ">${version} </td>
					<td width= "4% " style="font-weight:bold;">类型</td>
					<td width= "10% "> ${type} </td>
					<td width= "4% " style="font-weight:bold;">IP</td>
					<td width= "10% "> ${ip} </td>
				</tr>
				<tr class="text-c">
					<td width= "4% " style="font-weight:bold;">Token</td>
					<td width= "10% ">${token} </td>
					<td width= "4% " style="font-weight:bold;">CPU使用率</td>
					<td width= "10% "> ${cpuused} </td>
					<td width= "4% " style="font-weight:bold;">内存使用率</td>
					<td width= "10% "> ${memused} </td>
				</tr>
			</tbody>
         </table> 
</div>
<div id="container" style="width: 1210px; height: 230px; margin: 0 auto"></div>
<div id="container1" style="width: 1210px; height: 230px; margin: 0 auto"></div>
<script type="text/javascript" src="${ctx}/lib/jquery/1.9.1/jquery.min.js"></script> 
<script type="text/javascript" src="${ctx}/lib/layer/2.1/layer.js"></script>
<script type="text/javascript" src="${ctx}/static/h-ui/js/H-ui.js"></script> 
<script type="text/javascript" src="${ctx}/static/h-ui.admin/js/H-ui.admin.js"></script>
<script type="text/javascript" src="${ctx}/lib/icheck/jquery.icheck.min.js"></script> 
<script type="text/javascript" src="${ctx}/lib/jquery/1.9.1/jquery.min.js"></script> 
<script type="text/javascript" src="${ctx}/lib/Highcharts/highcharts.js"></script>
<script type="text/javascript" src="${ctx}/common/common.js"></script>
<script language="javascript">
$(function(){
	//隐藏获取监控信息按钮
	$("#vsmMonitorInfo").hide();
	var ip='${ip}';
	if(ip==''||ip.length==0){
		vsmMonitorInfo();
	}
})
$(document).ready(function () {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    $('#container').highcharts({
        chart: {
            type: 'spline',
            animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: function () {
                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                            y =  getCpuInfo();
                        series.addPoint([x, y], true, true);
                    }, 3000);
                }
            }
        },
        title: {
            text: 'CPU使用率'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: 'CPU使用率(%)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                    Highcharts.numberFormat(this.y, 2);
            }
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: [{
            name: 'CPU当前已使用(%)',
            data: (function () {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;
                for (i = -19; i <= 0; i += 1) {
                    data.push({
                        x: time + i * 1000,
						y: 0
                    });
                }
                return data;
            }())
        }]
    });
});
$(document).ready(function () {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    $('#container1').highcharts({
        chart: {
            type: 'spline',
            animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: function () {
                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                            y =  getMemInfo();
                        series.addPoint([x, y], true, true);
                    }, 3000);
                }
            }
        },
        title: {
            text: '内存使用率'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: '内存使用率(%)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                    Highcharts.numberFormat(this.y, 2);
            }
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: [{
            name: '内存当前已使用(%)',
            data: (function () {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;
                for (i = -19; i <= 0; i += 1) {
                    data.push({
                        x: time + i * 1000,
						y: 0
                    });
                }
                return data;
            }())
        }]
    });
});
function getCpuInfo(){
	var value= '';
	var vsmid = $("#vsmid").val().trim();
	$.ajax({
		url : "${ctx}/vsm/getCPU.html",
		type : 'GET',
		crossOrigin : true,
		dataType : 'json',
		cache : false,
		async : false,
		data : {
			"vsmid" : vsmid,
		},
		timeout : 10000,
		success : function(data) {
// 			alert(data);
			value =  data;
		}
	});
	return value;
}
function getMemInfo(){
	var value= '';
	var vsmid = $("#vsmid").val().trim();
	$.ajax({
		url : "${ctx}/vsm/getMemory.html",
		type : 'GET',
		crossOrigin : true,
		dataType : 'json',
		cache : false,
		async : false,
		data : {
			"vsmid" : vsmid,
		},
		timeout : 10000,
		success : function(data) {
// 			alert(data);
			value =  data;
		}
	});
	return value;
}
/**
 * 选择VSM列表
 */
function selectParent(){
	 layer_show("选择VSM", '${ctx}/vsm/getVsmList.html?vsm=2','600','350');
} 
/**
* 获取VSM监控信息
*/
 function vsmMonitorInfo() {	
	 var vsmid = $("#vsmid").val().trim();
	 if(vsmid.length<=0){
		layer.msg('vsmID不能为空', {icon:7,time:2000});
		return false;
	}
	$.ajax({
		url : "${ctx}/vsm/getVsmMonitorInfo.html",
		type : 'POST',
		crossOrigin : true,
		dataType : 'text',
		cache : false,
		async : true,
		data : {
			"vsmid" : vsmid,
		},
		success : function(data) {
			window.location.href="${ctx}/vsm/getVsmMonitorInfo.html?vsmid="+vsmid;
		} ,
		error:function(data){
			layer.msg('出错了', {icon:5,time:2000});
		}
	});
}
</script>
</body>
</html>