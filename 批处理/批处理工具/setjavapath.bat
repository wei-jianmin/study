@echo off
echo �������߷�����jdk&jreƽ��Ŀ¼��
pause
set jdk=%~dp0jdk1.8.0_131
set jre=%~dp0jre1.8.0_131
setx JAVA_HOME "%jdk%"
setx path "%path%;%jdk%\bin;%jre%\bin"
setx CLASSPATH ".;%jdk%\lib\dt.jar;%jdk%\bin\tools.jar"
pause