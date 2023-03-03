<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions"  prefix="fn"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<%
    String path = request.getContextPath();
//     String basePath = request.getScheme() + "://" + request.getServerName() + ":" + request.getServerPort() + path;
String basePath =     path;
request.setAttribute("ctx", basePath);
%>

