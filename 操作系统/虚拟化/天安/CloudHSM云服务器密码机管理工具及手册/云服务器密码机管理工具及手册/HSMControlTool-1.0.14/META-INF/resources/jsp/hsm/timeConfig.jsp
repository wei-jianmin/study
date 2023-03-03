<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ include file="/common/ctx.jsp"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" type="text/css" href="${ctx}/static/iconfont/1.0.8/iconfont.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/Ui/css/H-ui.min.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/Ui.admin/css/H-ui.admin.css" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/Ui.admin/skin/default/skin.css" id="skin" />
<link rel="stylesheet" type="text/css" href="${ctx}/static/Ui.admin/css/style.css" />

<script type="text/javascript" src="${ctx}/lib/My97DatePicker/WdatePicker.js"></script>
<script type="text/javascript" src="${ctx}/lib/jquery/1.9.1/jquery.min.js"></script> 
<script type="text/javascript" src="${ctx}/lib/layer/2.1/layer.js"></script>
<script type="text/javascript" src="${ctx}/lib/time/jquery-1.12.3.min.js"></script>

<title>clock</title>
</head>
<style>
    body,div,p{ font-family: 'Microsoft Yahei' ;font-size: 14px;}
    .box{ width: 300px; height: 300px; border:10px solid #8bf2f1; margin:100px 100px; border-radius: 50%;
        box-shadow: 0px 0px 20px 3px #444 inset; position: relative;}
    /*原点*/
    .origin{ width: 15px; height: 15px; border-radius: 50%; background: #ff0000; top:140px; left: 140px; position: absolute;}
    /* 指针 */
    .clock_line{ position: absolute;position:absolute;z-index:20;}
    .hour_line{width:100px;height:4px;top:148px;left:150px;background-color:#000;border-radius:2px;
        transform-origin:0 50%;box-shadow:1px -3px 8px 3px #aaa;}
    .minute_line{width:130px;height:2px;top:149px;left:140px;background-color:#000;
        transform-origin:7.692% 50%;box-shadow:1px -3px 8px 1px #aaa;}
    .second_line{width:170px;height:1px;top:149.5px;left:130px;background-color:#f60;
        transform-origin:11.765% 50%;box-shadow:1px -3px 7px 1px #bbb;}
    .dot_box{width: inherit; height: inherit;}
    /*时钟数*/
    .dot{ width: 40px; height: 40px; line-height: 40px; text-align: center; font-size: 18px; position: absolute;}
    .clock-scale{width:195px;height:2px;transform-origin:0% 50%;z-index:7;
      position:absolute;top:149px;left:150px;}
    .scale-show{ width:12px;height:2px;background-color:#555;float:left;}
    .scale-hidden{width:133px;height:1px;float:left;}
    /*日期*/
    .date_info{width:160px;height:28px; 
        line-height:28px;text-align:center;position:absolute;top:180px;left:70px;z-index:11;color:#555;
        font-weight:bold;}
    .time_info{ width: 80px; height: 25px; line-height: 25px;text-align:center;position:absolute;top:220px;left:110px;z-index:11;color:#555; background: #253e3e; }
    .time{ width: 25px ;height:25px; float: left; color: #fff; font-size: 18px;}
     #minute_time{border-left:1px solid #fff;border-right:1px solid #fff;}
.demo{margin:30px auto 40px auto;width:320px}
.input{padding:6px;border:1px solid #d3d3d3}
</style>
<body>
<!-- <nav class="breadcrumb"> -->
<!-- 	<i class="Hui-iconfont">&#xe67f;</i> 首页  -->
<!-- 	<span class="c-gray en">&gt;</span> HSM配置 -->
<!-- 	<span class="c-gray en">&gt;</span> 系统时间 -->
<!-- 	<a class="btn btn-success radius r" style="line-height:1.6em;margin-top:3px" href="javascript:location.replace(location.href);" title="刷新" > -->
<!-- 	<i class="Hui-iconfont">&#xe68f;</i> -->
<!-- 	</a> -->
<!-- </nav> -->
<input type="hidden" value="${year}" id="year">
<input type="hidden" value="${month}" id="month">
<input type="hidden" value="${day}" id="day">
<input type="hidden" value="${hour}" id="hour">
<input type="hidden" value="${minute}" id="minute">
<input type="hidden" value="${second}" id="second">
<div>
<div class="box" id="clock" style="float: left;margin-right: 50px;">
    <!-- 原点 -->
    <div class="origin"></div>
    <!-- 时钟数 -->
    <div class="dot_box" style="display:none;">
        <div class="dot" style="margin:-50px;">6</div>
        <div class="dot" style="margin:-50px;">5</div>
        <div class="dot" style="margin:-50px;">4</div>
        <div class="dot" style="margin:-50px;">3</div>
        <div class="dot" style="margin:-50px;">2</div>
        <div class="dot" style="margin:-50px;">1</div>
        <div class="dot" style="margin:-50px;">12</div>
        <div class="dot" style="margin:-50px;">11</div>
        <div class="dot" style="margin:-50px;">10</div>
        <div class="dot" style="margin:-50px;">9</div>
        <div class="dot" style="margin:-50px;">8</div>
        <div class="dot" style="margin:-50px;">7</div>
    </div>
    <!-- 时、分、秒针 -->
    <div class="clock_line hour_line" id="hour_line"></div>
    <div class="clock_line minute_line" id="minute_line"></div>
    <div class="clock_line second_line" id="second_line"></div>
    <!-- 日期 -->
    <div class="date_info" id="date_info"></div>
    <!-- 时间 -->
    <div class="time_info" >
        <div class="time" id="hour_time"></div>
        <div class="time" id="minute_time"></div>
        <div class="time" id="second_time"></div>
    </div>
</div>
<div id="main"style="width: 400px; height: 300px;margin-top:100px;float: left;">
<article class="page-container">
	<form action="" method="post" class="form form-horizontal" id="form-client-add">
			<div class="row cl" style="margin-bottom:20px;">
				<label class="form-label col-xs-4 col-sm-2">
					<input type="checkbox" id="NTPCheck" name="NTPCheck"/>
				</label>
				<div class="formControls col-xs-8 col-sm-9" style="margin-top:-5px;">
					设置NTP自动同步
				</div>
			</div>
			<div id="NTPIPDiv" style="display:none; margin-bottom: 40px;">
			        <p>&nbsp;&nbsp;&nbsp;&nbsp;当前时间：<input type="text" class="input" id="dateTime" value="${dateTime}" disabled="disabled"></p>
			        <p>&nbsp;&nbsp;&nbsp;&nbsp;同步周期：<input type="text" class="input" id="NTPCycle" value="${NTPCycle}" placeholder="请输入同步周期！">(分钟)</p>					
					<p>&nbsp;服务器地址：<input type="text" class="input" id="NTPIP" value="${NTPIP}" placeholder="请输入服务器地址！"/></p>
					
			</div>
	
			<div class="demo" id="setDateTime">
				  <p>请选择日期：<input class="input-text Wdate" type="text" value="${dateTime}" onfocus="WdatePicker({dateFmt:'yyyy-MM-dd HH:mm:ss'})" readonly="readonly" maxlength="0" id="currentTime" style="width:180px;"/></p>
		    </div>
			<div style="width:100%;height:50px;">
				<div class="col-xs-8 col-sm-9 col-xs-offset-4 col-sm-offset-3" >
					<button onClick="configTime();" class="btn btn-primary radius" type="button" id="timeButton">保存配置</button>
				</div>
			</div>	
		</form>
</article>
</div>
</div>
<script type="text/javascript" src="${ctx}/common/common.js"></script>
<script>
$(document).ready(function() { 
	$("#NTPCheck").click(function() {
		if(this.checked == true){
			$("#NTPIPDiv").css("display","block");	
			$("#setDateTime").css("display","none");
		}else{
			$("#NTPIPDiv").css("display","none");
			$("#setDateTime").css("display","block");
// 			$("#NTPIP").val("");
		}
	});
});
//日期格式化
Date.prototype.Format = function (fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}
/**
 * 时钟图表
 */
$(function(){	
	var NTPIP = $("#NTPIP").val();
	if(NTPIP!=null && NTPIP!=""){
		document.getElementById("NTPCheck").checked = true;
		$("#NTPIPDiv").css("display","block");	
		$("#setDateTime").css("display","none");
	}		
	layer.msg("时钟会在<span style='color:red;'>2s</span>后刷新，请耐心等待！",{icon:7,time:1000});
	$(".dot_box").css("display","block");
    var clock = document.getElementById("clock");
    function initNumXY(){
        // 1、12个数字的位置设置
        var radius = 110;//大圆半价
        var dot_num = 360/$(".dot").length;//每个div对应的弧度数
        //每一个dot对应的弧度;
        var ahd = dot_num*Math.PI/180;
        $(".dot").each(function(index, el) {
            $(this).css({
                "left":180+Math.sin((ahd*index))*radius,
                "top":180+Math.cos((ahd*index))*radius
            });
        });
        // 2、刻钟设置
        for(var i = 0; i < 60; i++) {
            clock.innerHTML += "<div class='clock-scale'> " + 
                   "<div class='scale-hidden'></div>" + 
                   "<div class='scale-show'></div>" + 
                  "</div>";
        }
        var scale = document.getElementsByClassName("clock-scale");
            for(var i = 0; i < scale.length; i++) {
                scale[i].style.transform="rotate(" + (i * 6 - 90) + "deg)";
        }
    }
    initNumXY();//调用上面的函数
    //获取时钟id
    var hour_line = document.getElementById("hour_line"),
        minute_line = document.getElementById("minute_line"),
        second_line = document.getElementById("second_line"),
        date_info=document.getElementById("date_info"),//获取date_info
        hour_time = document.getElementById("hour_time"),// 获去时间id
        minute_time = document.getElementById("minute_time"),
        second_time = document.getElementById("second_time");
    //3、设置动态时间
    function setTime(){
    	 var year= Number($("#year").val());
     	var month= Number($("#month").val());
         var day= Number($("#day").val());
        var hours= Number($("#hour").val());
    	var minutes= Number($("#minute").val());
        var seconds= Number($("#second").val()); 
        // 获取日期id
        date_info.innerHTML=year+"年"+month+"月"+day+"日   ";
        hour_time.innerHTML = hours >=10 ? hours : "0"+hours;
        minute_time.innerHTML = minutes >=10 ? minutes : "0"+minutes;
        second_time.innerHTML = seconds >=10 ? seconds : "0"+seconds;
        console.log(year+"年"+month+"月"+day+"日   ");
        //时分秒针设置
        var hour_rotate = (hours*30-90) + (Math.floor(minutes / 12) * 6);
        hour_line.style.transform = 'rotate(' + hour_rotate + 'deg)';
        minute_line.style.transform = 'rotate(' + (minutes*6 - 90) + 'deg)';
        second_line.style.transform = 'rotate(' + (seconds*6 - 90)+'deg)';
    }
    // setTime();
    setInterval(setTime, 1000);
});
function configTime(){
	var timeButton = document.getElementById("timeButton");
	var currentTime=$("#currentTime").val().trim();
	var NTPCycle=$("#NTPCycle").val().trim();
	var NTPIP=$("#NTPIP").val().trim();
	
	var checkInteger=/^[0-9]*$/;	//验证数字
	//验证IP
	var checkIp = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])(\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])){3}$/;
	//验证IPV6
	var checkIp6=/^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/;	
	
	var reg="^((https|http|ftp|rtsp|mms)?://)?" // schema
    	+ "(([0-9a-zA-Z_!~*\'().&=+$%-]+: )?[0-9a-zA-Z_!~*\'().&=+$%-]+@)?"//ftp的user@
    	+ "(([0-9]{1,3}\\.){3}[0-9]{1,3}" // IP形式的URL- 199.194.52.184
    	+ "|" // 允许IP和DOMAIN（域名）
   		+ "([0-9a-zA-Z_!~*\'()-]+\\.)*" // 域名- www.
    	+ "([0-9a-zA-Z][0-9a-zA-Z-]{0,61})?[0-9a-zA-Z]\\." // 二级域名
    	+ "[a-zA-Z]{2,6})" // first level domain- .com or .museum
    	+ "(:[0-9]{1,4})?" // 端口- :80
    	+ "((/?)|" // a slash isn't required if there is no file name
    	+ "(/[0-9a-zA-Z_!~*\'().;?:@&=+$,%#-]+)+/?)$";
	
	if(!$('[id=NTPCheck]:eq(0)').is(':checked')){
		NTPIP="";
		NTPCycle="0";
		if(currentTime.length==0){
			layer.msg('请选择日期！',{icon:7,time:2000});
	      	return false;
		}
	}else{
		if(NTPCycle.length==0){
       		layer.msg("请设置同步周期！",{icon:7,time:2000});
       		return false;
     	}else if(!checkInteger.test(NTPCycle)){
     		layer.msg("同步周期格式为[分钟(1-59)]！",{icon:7,time:2000});
	      	return false;
     	}	
		if(NTPCycle>59||NTPCycle<1){
			layer.msg("同步周期格式为[分钟(1-59)]！",{icon:7,time:2000});
       		return false;
		}
	 	if(NTPIP.length==0){
       		layer.msg("请输入服务器地址！",{icon:7,time:2000});
       		return false;
     	}	 	
 		if(!(new RegExp(reg).test(NTPIP)||checkIp.test(NTPIP)||checkIp6.test(NTPIP))){
	 		layer.msg("请输入有效的服务器地址！",{icon:7,time:2000});
        	return false;
	 	}	    
	}
	if(currentTime.length==0){
		currentTime = new Date().Format("yyyy-MM-dd hh:mm:ss");  
    }
	$.ajax({
		url : "${ctx}/hsm/configTime.html",
		type : 'POST',
		dataType : "text",
		cache : false,
		async : true,
		data : {
			"currentTime" : currentTime,
			"NTPCycle" : NTPCycle,
			"NTPIP" : NTPIP
		},
		beforeSend:function(){
			timeButton.disabled = true;
			layer.load(3); 
		},
		success : function(data) {
			layer.closeAll();
			var falg1 = data.split(",")[0];
			if(falg1=="success"){
				if(NTPIP!=null && NTPIP!=""){
					layer.msg('设置NTP同步成功！', {icon:1,time:2000},function() {
// 						window.location.reload();
						window.location.href="${ctx}/hsm/systemManage.html?typeIndex=0";
					});
				}else{
					layer.msg('时间配置成功！', {icon:1,time:2000},function() {
// 						window.location.reload();
						window.location.href="${ctx}/hsm/systemManage.html?typeIndex=0";
					});
				}
			}else if(falg1=="fail"){
				timeButton.disabled = false; 
				layer.msg("时间配置配置失败！错误信息="+data.split(",")[1], {icon:2,time:2000});
			}
			
		} ,
		error:function(data){
			layer.closeAll();
		 layer.msg("出错了！", {icon:5,time:2000});
		 timeButton.disabled = false;
		}
   });
	
}
</script>
<div style="text-align:center;clear:both;margin-top:160px">
<!--<script src="/gg_bd_ad_720x90.js" type="text/javascript"></script> -->
<!--<script src="/follow.js" type="text/javascript"></script> -->
</div>
</body>
</html>