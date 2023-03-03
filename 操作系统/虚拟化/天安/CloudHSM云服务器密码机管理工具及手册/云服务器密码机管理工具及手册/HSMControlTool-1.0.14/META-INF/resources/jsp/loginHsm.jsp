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
    <div class="LoginForm" style="max-height:350px;">
      	<h3 style="text-align:center;margin-top:-10px;">管理工具登录</h3>
   		<form class="form-horizontal" style="height: 180px; padding-top:-20px;" id="loginForm" action="${ctx}/login.html" method="post">
       		<div class="form-group">
   				<div class="col-sm-12" >
   					<span id="info" style="color:red;font-size:15px;">${loginerror}</span>
   					<input type="hidden" id="authentication" name="authentication" value="false"/>
       				
       				<div class="input-group" style="margin-top:10px;">
          				<span class="input-group-addon"><span class="glyphicon">HSM IP:</span></span>
<!--           				<input class="form-control" type="text" placeholder="请输入HSM IP地址" id="hsmIp" name="hsmIp" value="192.168.18.90"/>	 -->
						<input class="form-control" type="text" placeholder="请输入HSM IP地址" id="hsmIp" name="hsmIp"/>
       				</div>
       				<div  id="pubCheck" style="display: none;">
						<div class="row cl"  style="margin-top:10px;">
							<label class="form-label col-xs-4 col-sm-3">
								<span class="input-group-addon" style="border-top-left-radius:4px;border-bottom-left-radius:4px;display:block;width:68px;margin-top:-3px;">
								<span class="glyphicon" style="height:20px;">
									私钥:
								</span></span>
							</label>
							<div class="formControls col-xs-8 col-sm-9">
<!-- 								<input class="form-control" type="text" placeholder="请输入认证私钥" id="privateKey" name="privateKey" value="YWTa/lJVOdVk9bG6oqbjJMPNMKV+duH6Ww0iC4a2FRs="/>	 -->
								<input class="form-control" type="text" placeholder="请输入认证私钥" id="privateKey" name="privateKey"/>
							</div>
						</div>
						<div class="row cl" style="margin-top:10px;">
							<label class="form-label col-xs-4 col-sm-3">
								<span class="input-group-addon" style="border-top-left-radius:4px;border-bottom-left-radius:4px;display:block;width:68px;margin-top:-3px;">
								<span class="glyphicon" style="height:20px;">
									公钥:
								</span></span>
							</label>
							<div class="formControls col-xs-8 col-sm-9">
<!-- 								<input class="form-control" type="text" placeholder="请输入认证公钥" id="publicKey" name="publicKey" value="ey3LdmGy6dxbTBTZLg3rkoBgEDusBVrMqnd/Ntd9BXKnhprTz+BdeN8Cr9nSYHqIn4/8Z2twAKkOSXKELLPQ5Q=="/>	 -->
								<input class="form-control" type="text" placeholder="请输入认证公钥" id="publicKey" name="publicKey" />
							</div>
						</div>
       				</div>
       				<div class="input-group" style="margin-top:30px;"  id="numImg">
		 				<div class="formControls">
							<input name="veryCode" class="form-control" id="veryCode" maxlength="6" placeholder="验证码" /> 
							<img class="form-control" id="imgObj" src="${ctx}/verifyCodeServlet" onclick="changeImg();" style="float:right;height:34px;width:90px;margin-top:-34px;">
						</div>
					</div>
       				<div id="errorTip" style="color:red;"></div>
       			</div>
       		</div>
       		
        	<div style="text-align: center; margin-top:50px;" id="loginBtn">
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
	var hsmIp = $("#hsmIp").val().trim();
	if (hsmIp.length <= 0) {
		layer.msg("HSM IP不可为空！", {
			icon : 7,
			time : 2000
		});
		return false;
	}
	var authentication =$("#authentication").val().trim();
	if(authentication=="true"){
		var privateKey = $("#privateKey").val().trim();
		if (privateKey.length <= 0) {
			layer.msg("认证私钥不可为空！", {
				icon : 7,
				time : 2000
			});
			return false;
		}
		var publicKey = $("#publicKey").val().trim();
		if (publicKey.length <= 0) {
			layer.msg("认证公钥不可为空！", {
				icon : 7,
				time : 2000
			});
			return false;
		}
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
	var hsmIp = $("#hsmIp").val().trim();
	var authentication =$("#authentication").val().trim();
	var privateKey = $("#privateKey").val().trim();
	var publicKey = $("#publicKey").val().trim();
	var btnSubmit = document.getElementById("loginBtn");	
	$.ajax({
		type: "post",
    	url:"${ctx}/login.html", //"${ctx}/testJson.html", 
    	dateType : "text",
    	async: false,
   		data: {
   			"hsmIp" : hsmIp,
			"authentication" :authentication,
			"privateKey" :privateKey,
			"publicKey" :publicKey
    	},
    	beforeSend:function(){
			layer.load(3); 
		  	btnSubmit.disabled= true;
		},	
        success: function(data) {
        	layer.closeAll();
        	var result = data.split(",")[0];
        	if(result == "yes"){ // 登录通过       		
        		layer.msg('登录成功!', {icon:1,time:2000},function() {	
        			document.location.replace("${ctx}/index.html");
				});
    		}else if(result == "empty"){
    			btnSubmit.disabled= false;
    			layer.msg("此HSM需要认证公钥，请输入公私钥！",{icon:7,time:2000});
    			$("#authentication").val("true");
    			$("#pubCheck").css("display","block");
    			$("#numImg").css("margin-top","10px");
    			$("#loginBtn").css("margin-top","0px");
    			changeImg();
    		}else if (result == "emptys"){
    			btnSubmit.disabled= false;
    			layer.msg("输入ip地址有误，连接不上该ip",{icon:7,time:2000});
    			changeImg();
    		}else{
    			btnSubmit.disabled= false;
    			layer.msg("登录失败！",{icon:7,time:2000});
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
