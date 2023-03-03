<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<%@ include file="/common/ctx.jsp"%>
<title>江南天安云服务器密码机单机版工具</title>
<link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon">
<meta name="keywords" content="云服务器密码机单机版工具">
<meta name="description" content="云服务器密码机单机版工具">
</head>
<body>
<div class="Login">
  <div class="LoginHeader">
    <img src="${ctx}/images/img/logo.png" />
  </div>
  <div class="LoginCont">
    <img src="${ctx}/images/img/bg.png" />
     <!--    用户登录-->
    <div class="LoginForm"  style="max-height:400px;">
      	<h3 style="text-align:center;">管理工具登录</h3>
   		<form class="form-horizontal" style="height: 120px; padding-top:-20px;" id="loginForm" action="${ctx}/login.html" method="post">
       		<div class="form-group">
   				<div class="col-sm-12" >
   					<span id="info" style="color:red;font-size:15px;">${loginerror}</span>
       				<div class="input-group" style="margin-top:20px;">
          				<span class="input-group-addon"><span class="glyphicon">账号</span></span>
          				<input  class="form-control" type="text" id="userName" name="userName"/>	
       				</div>
       				<div class="input-group" style="margin-top:20px;">
		 				<span class="input-group-addon"><span class="glyphicon">密码</span></span>
						<input  class="form-control" type="${sessionScope.inputType }" id="userPwd" name="passwd"/>	
					</div>
       				<div class="input-group" style="margin-top:20px;">
		 				<div class="formControls">
							<input name="veryCode" class="form-control" id="veryCode" maxlength="6" placeholder="验证码" /> 
							<img  class="form-control" id="imgObj" src="${ctx}/verifyCodeServlet" onclick="changeImg();" style="float:right;height:34px;width:90px;margin-top:-34px;">

						</div>
					</div>
       				<div id="errorTip" style="color:red;"></div>
       			</div>
       		</div>
       		
        	<div style="text-align: center;">
        	<br/>
          		<a class="btn btn-primary radius" onclick="login();" style="width:70px;" href="javascript:void(0)" id="loginBtn">登录</a>
        	</div>
   		</form>
    </div>
   </div>
</div>
<p style="text-align: center;padding: 30px 0;;color:#999;font-size:12px;"> Copyright©2018 版权所有 江南天安科技有限公司  版本号：${version}</p>
<%@ include file="/common/commonCSS.jsp" %>
<script type="text/javascript" src="lib/jquery/1.9.1/jquery.min.js"></script>
<script type="text/javascript" src="lib/layer/2.1/layer.js"></script>
<script type="text/javascript" src="static/h-ui/js/H-ui.js"></script>
<script type="text/javascript">
document.onkeydown = function(event) {
	var e = event || window.event
			|| arguments.callee.caller.arguments[0];
	if (e && e.keyCode == 13) { // enter 键
		login();
	}
};
// 判断是否有错误信息
$(function(){
	var status ="${status}";
	if(status!=null&&status!=""){
		layer.msg("${loginerror}", {icon : 7,time : 2000});
	}
});
//登录验证
function login() {
	var userName = $("#userName").val();
	var userPwd = $("#userPwd").val();
	if (userName.length <= 0 || userPwd.length <= 0) {
		layer.msg("账号或密码不可为空！", {
			icon : 7,
			time : 2000
		});
		return false;
	}
	isRightCode();
}

//换一张验证码
function changeImg() {
	var imgSrc = $("#imgObj");
	$("#veryCode").val("");
	var src = imgSrc.attr("src");
	imgSrc.attr("src", chgUrl(src));
}
//时间戳  
//为了使每次生成图片不一致，即不让浏览器读缓存，所以需要加上时间戳  
function chgUrl(url) {
	var timestamp = (new Date()).valueOf();
	url = url + "?timestamp=" + timestamp;
	return url;
}

//验证码验证
function isRightCode() {
	var code = $("#veryCode").val();
	code = "c=" + code;
	$.ajax({
		type : "POST",
		url : "${ctx}/resultServlet",
		data : code,
		success : callback
	});
}

//验证码返回值
function callback(data) {
	if (data == 1) {
		layer.msg("请输入验证码", {
			icon : 7,
			time : 2000
		});
		return false;
	} else if (data == 2) {
		// 验证通过 
// 		$("#loginForm").submit();
		login2();
	} else {
		layer.msg("验证码错误！", {icon:2,time:500},function() {
			changeImg();
		});
		return false;
	}
}

function login2(){
	// 数据已经校验完毕
	var userName = $("#userName").val();
	var userPwd = $("#userPwd").val();
	var btnSubmit = document.getElementById("loginBtn");
	
	$.ajax({
		type: "post",
    	url:"${ctx}/login.html", //"${ctx}/testJson.html", 
    	dateType : "text",
    	async: false,
   		data: {
   			"userName" : userName,
			"passwd" :userPwd
    	},
    	beforeSend:function(){
			layer.load(3); 
		  	btnSubmit.disabled= true;
		},	
        success: function(data) {
        	console.log(data);
        	layer.closeAll();
        	var result = data.split(",")[0];
        	console.log(data);
        	if(result == "yes"){ // 登录通过
        		layer.msg('登录成功!', {icon:1,time:2000},function() {	
        			document.location.replace("${ctx}/index.html");
				});
    		}else if(result == "isTerm"){
    			btnSubmit.disabled= false;
    			layer.msg("该用户已过期，请联系管理员",{icon:7,time:2000});
    			changeImg();
    		}else if(result == "empty"){
    			btnSubmit.disabled= false;
    			layer.msg("用户名和密码不能为空",{icon:7,time:2000});
    			changeImg();
    		}else if(result == "noUse"){
    			btnSubmit.disabled= false;
    			layer.msg("该用户不存在或未启用",{icon:7,time:2000});
    			changeImg();
    		}else if(result == "passW"){
    			btnSubmit.disabled= false;
    			layer.msg("密码错误，请重新输入",{icon:7,time:2000});
    			changeImg();
    	    //判断如果后台返回的结果是连续登录失败次数大于5次，则给于提示，并跳转到404错误页面
/*     		}else if(result == "outTime"){
    			btnSubmit.disabled= false;
    			layer.msg("对不起，您的登录次数已经超过限制，请3分钟之后重新登录！",{icon:7,time:3000},function(){
	        		document.location.replace("${ctx}/toError.html");
    			}); */
    		}else if (result == "emptys"){
    			btnSubmit.disabled= false;
    			layer.msg("连接不上该ip地址，请查看该服务器是否打开",{icon:7,time:2000});
    			changeImg();
    		}else{
    			btnSubmit.disabled= false;
    			layer.msg('登录失败！',{icon:7,time:2000});
    			changeImg();
    		}
        },
		error:function(data){
			layer.closeAll();
			layer.msg('出错了', {icon:5,time:2000});
		}
        
    });
}		
// 点击取消重置输入框
function freset(){
	var obj = document.getElementById("loginForm");
	obj.reset();
}
</script>
</body>
</html>
