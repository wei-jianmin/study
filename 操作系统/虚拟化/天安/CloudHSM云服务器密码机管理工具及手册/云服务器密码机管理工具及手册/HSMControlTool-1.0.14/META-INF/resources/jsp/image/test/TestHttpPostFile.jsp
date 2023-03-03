<%@ page language="java" pageEncoding="UTF-8" import="java.util.*" %>
<!DOCTYPE HTML>
<html>
<head>
<title>文件上传测试页面</title>
</head>

<%
  	request.setCharacterEncoding("utf-8");  
	response.setCharacterEncoding("utf-8");  
	response.setContentType("text/html;charset=utf-8"); 
	
	// ********************************************************************
			
	String requestId = request.getParameter("requestId");
	requestId = requestId == null ? UUID.randomUUID().toString() : requestId.trim();
	
	String info = request.getParameter("info");
	info = info == null ? "{&quot;uuid&quot;: &quot;vsm-79231&quot;, &quot;version&quot;: &quot;V5.23.12&quot;, &quot;sign&quot;:&quot;01b08bb5485ac730df19af55ba4bb01c&quot;}" : info.trim();
	
  %>

<body>
    <FORM name="form1" METHOD="POST" ACTION="<%=request.getContextPath()%>/image/upLoadImgFile" ENCTYPE="multipart/form-data">
      <input type="hidden" name="htype" value="jsptotest">
	 	<table style="width:100%;border:1px solid A1C3E7; font-weight: bold;font-size:14pt;margin-top:0px" >		
			<tr>
				<td width="20%">请求ID</td>
				<td><input type="text" name="requestId" style="width:98%;height:36px;" value="<%=requestId%>"></td>
			</tr>
			<tr>
			  <td>文件:</td>
			  <td><input name="file" type="FILE" id="attach" size="100" style="width:98%;height:36px;"></td>
			</tr>
			<tr>
				<td>文件附件信息</td>
				<td><input type="text" name="info" style="width:98%;height:36px;" value="<%=info%>"></td>
			</tr>
			<tr>
			  <td colspan="2"><input name="ok" type= "submit" value=" 提交 "></td>
			</tr>
		</table>
	</form>
    </body>
     </html>