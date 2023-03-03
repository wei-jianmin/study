#!/bin/bash

DEBFULLNAME=""
DEBEMAIL=""
basedir=""
foldname=""
appname=""
version=""
arch="unknown"
exepath=""	#在file_move函数中被赋值
iconpath=""	#在file_move函数中被赋值

if [ "$1" = "-q" ]; then
	quiet="y"
else
	quiet="n"
fi

function show_help()
{
	echo "说明："
	echo "该脚本为统信打包辅助脚本，需在普通用户下执行该脚本"
	echo "该脚本应放置于符合'包名-版本号'格式的目录下"
	echo "执行脚本前，将待打包的文件放到当前脚本目录下的files文件夹中"
	echo "如果脚本在待打包文件中发现可执行文件，则默认创建桌面快捷方式"
	echo "可在打包前，将桌面快捷方式图标文件放在当前脚本目录下并命名为icon.png [可选]"
	echo "打包完成后，files文件夹及icon.png文件都将被移动到相应目录下，请提前做好备份"
	echo "支持 -q 参数，使用 -q 参数时，自动完成安装包的全部创建过程，此时所有选项采用默认值"
}

#参数：min,max
function _get_sel() 
{
    while [ 1 ]; do
	echo "请选择($1~$2):"
	read sel
	if [ $sel -ge $1 -a $sel -le $2 ]; then
		return $sel
	else
		echo "您的输入有误，请重新输入"
	fi
    done
}

function _do_sel()
{
	if [ $quiet = "y" ]; then
		return 1
	fi
	while [ 1 ]; do
	echo -n "确定(y:默认)|手动指定(h):"
	read sel
	if [ -z "$sel" -o "$sel" = "y" ]; then
		return 1	
	elif [ "$sel" = "h" ]; then
		return 2
	else
		echo "输入错误"
	fi
	done
}

function _do_sel2()
{
	if [ $quiet = "y" ]; then
		return 1
	fi
	while [ 1 ]; do
	echo -n "是(y:默认)|否(n/q):"
	read sel
	if [ -z "$sel" -o "$sel" = "y" ]; then
		return 1	
	elif [ "$sel" = "q" -o "$sel" = "n" ]; then
		return 2
	else
		echo "输入错误"
	fi
	done
}

function _find_exepath()
{
	if [ -d $foldname/files/lib ]; then
		if [ "$(ls -A $foldname/files/lib)" ]; then
		    for f in $foldname/files/lib/*; do
			f2=${f##*/}
			if [ "${f2:0:5}" = "libQt" ]; then
				continue
			fi
			ft=`file -b --mime-type $f`
			if [[ "$ft" =~ "executable" ]]; then
				has_main=`nm -D $f | grep "main"`
				if [ -z "$has_main" ]; then
					continue	
				fi
				has_elf_interpreter=`file $f | grep interpreter`
				if [ -n "$has_elf_interpreter" ]; then
					echo "找到可执行文件: $f，是否为该文件创建桌面快捷方式？"
					_do_sel2
					if [ $? = 1 ]; then
						exepath=$f
						break
					fi
				fi
			fi
		    done
		fi
	fi
}

function _find_iconpath()
{
	count=`find $foldname/entries/icons/hicolor/ -name "*icon.png" | wc -l`
	if [[ $count > 1 ]]; then
		echo "在$foldname目录下发现如下多个程序图标，请指定使用哪个文件作为程序图标"
		index=1
		for f in `find $foldname/entries/icons/hicolor/ -name "*icon.png"`; do
			printf "$index. %s\n" $f
			let index+=1
		done
		_get_sel 1 $count
		iconpath=`find $foldname/entries/icons/hicolor/ -name "*icon.png" | sed -n "$?p"`

	else
		iconpath=`find $foldname/entries/icons/hicolor/ -name "*icon.png"`
	fi
}

function precheck()
{
	#检查用户角色
	if [ `whoami` = root ]; then
		echo "请切换到普通用户下执行"
		echo ""
		return 1
	fi

	if [ "`which dh_make`" = "" ]; then
		echo "请先安装dh_make工具"
		return 1
	fi
	if [ "`which dpkg-source`" = "" ]; then
		echo "请先安装dpkg-source工具"
		return 1
	fi
	if [ "`which dpkg-buildpackage`" = "" ]; then
		echo "请先安装dpkg-buildpackage工具"
		return 1
	fi
	
	#配置环境变量
	DEBFULLNAME="tongzhiweiye"
	DEBEMAIL="Service@tongzhi.com.cn"
	echo "环境变量"
	echo "DEBFULLNAME = $DEBFULLNAME"
	echo "DEBEMAIL    = $DEBEMAIL"
	_do_sel
	if [ $? = 2 ]; then
		echo -n "DEBFULLNAME : "
		read DEBFULLNAME
		echo -n "DEBEMAIL    : "
		read DEBEMAIL
		break
	fi
	echo ""
	
	#获取版本号
	path=`pwd`
	version=${path##*-}
	echo "版本号为:$version"
	_do_sel
	if [ $? = 2 ]; then
		echo -n "手动指定版本号 : "
		read version
		#echo "版本号为:$version"
		break
	fi
	echo ""
	
	#文件夹名字检查
	name=`pwd`
	basedir=$name
	name=${name##*/}
	name=${name%-*}
	if [ ! -d $name ]; then
		mkdir $name
	fi
	foldname=$name
	appname=${name##*.}
	echo "应用名称为: $appname "
	_do_sel
	if [ $? = 2 ]; then
		echo -n "指定应用名字为: "
		read appname
	fi	
	echo ""
	
	#cpu架构
	_get_arch	
	echo "CPU架构为: $arch "
	_do_sel
	if [ $? = 2 ]; then
		echo -n "指定CPU架构为: "
		read arch
	fi	
	echo ""

	#exepath
	_find_exepath
	echo "在$foldname目录下发现可执行文件路径为：$exepath"
	#if [ -n "$exepath" ]; then
	_do_sel
	if [ $? = 2 ]; then
		echo -n "指定可执行文件路径为(从当前路径开始)："
		read exepath
		echo ""
	fi
	#fi
	echo ""

	#iconpath
	#if [ -d $foldname/entries/icons/hicolor ]; then
	#	for d in $foldname/entries/icons/hicolor/*/apps
	#	do
	#	    if [ $(ls -A $d) ]; then
	#	        for f in $d/*.png
	#	        do
	#	    	if [ -z "$iconpath" ]; then
	#	    		iconpath=$f
	#	    	else
	#	    		rm -f $f
	#	    	fi
	#	        done	
	#	    fi
	#	done
	#fi
	_find_iconpath
	echo "在$foldname目录下发现程序图标文件路径为：$iconpath"
	echo ""

	return 0
}

function make_entries()
{
	echo "make entries folder"
	cd $basedir/$foldname
	#检查目录是否已存在
	if [ -e entries ]; then
		echo "entries 目录已经存在，输入y表示使用该目录，输入q表示删除重建该目录(默认为y)"
		_do_sel2
		if [ $? = 2 ]; then
			rm -rdf entries
		else
			echo ""
			return 0
		fi
	fi
	#创建entries目录树
	mkdir entries
	if [ ! $? = 0 ]; then
		echo "创建目录是否，请检查是否是权限问题"
		echo ""
		return 0
	fi
	cd entries
	mkdir applications
	mkdir autostart
	mkdir GConf
	mkdir glib-2.0
	mkdir icons
	cd icons
	mkdir hicolor
	cd hicolor
	mkdir -p 16x16/apps
	mkdir -p 24x24/apps
	mkdir -p 32x32/apps
	mkdir -p 48x48/apps
	mkdir -p 128x128/apps
	mkdir -p 256x256/apps
	mkdir -p 512x512/apps
	mkdir -p scalable/apps
	cd ../..
	mkdir locale
	mkdir plugins
	mkdir services
	mkdir help
	cd ..
	if [ ! -d files ]; then
		mkdir files
	fi
	if [ ! -e info ]; then
		touch info
	fi
	echo "make entries filder ok"
	echo ""
	return 0
}

function _get_arch()
{
   case `uname -m` in
        i[3456789]86|x86|i86pc)
            arch='x86'
            ;;
        x86_64|amd64|AMD64)
            arch='amd64'
            ;;
        aarch64)
           arch='arm64'
           ;;
        *)
           arch=`uname -m`
           ;;
    esac
}

function make_info()
{
	echo "make info file"
	cd $basedir/$foldname
	if [ -e info ]; then
		size=`stat -c "%s" info`
		#echo size=$size
		if [[ $size > 0 ]]; then
			echo "info 文件不为空，输入y表示使用该文件，输入q表示删除并重建该文件(默认为y)"
			_do_sel2
			if [ $? = 1 ]; then
			    echo ""
			    return 1
			fi
		fi
	fi
	#echo "write info"
cat << EOF > info 
{
  "appid": "$foldname",
  "name": "$appname",
  "version": "$version",
  "arch": ["$arch"],
  "permissions": {
    "autostart": false,
    "notification": false,
    "trayicon": false,
    "clipboard": true,
    "account": false,
    "bluetooth": false,
    "camera": false,
    "audio_record": false,
    "installed_apps": false
}
EOF
	echo "info 文件内容为:"
	cat info
	echo "请检查 info 文件内容是否正确，如有问题，需手动进行更改"
	echo ""
	return 0
}

function file_move()
{
	#文件
	cd $basedir
	echo "移动文件"
	if [ ! -d $foldname/files/lib ]; then
		mkdir -p $foldname/files/lib
	fi
	if [ -d files ]; then
	    echo "将当前files文件夹中的所有文件移动到$foldname/files/lib目录下"
	    mv -f files/* $foldname/files/lib/
	    rm -d files	
	fi
	if [ -z "$exepath" ]; then
	    _find_exepath
	fi
	echo "可执行文件路径为：$exepath"
	#if [ -n "$exepath" ]; then
	_do_sel
	if [ $? = 2 ]; then
		echo -n "指定可执行文件路径为(从当前路径开始)："
		read exepath
		echo ""
	fi
	#fi

	#图标
	if [ -f icon.png ]; then
		png=`file -b icon.png | cut -f1 -d\ `
		if [ $png = PNG ]; then
			sz=`file -b icon.png | cut -f4 -d\ `
			res=""
			case $sz in
			16)
				res=16x16	
				;;
			24)
				res=24x24
				;;
			32)
				res=32x32
				;;
			48)
				res=48x48
				;;
			128)
				res=128x128
				;;
			256)
				res=256x256
				;;
			512)
				res=512x512
				;;
			*)
				echo "图像分辨率(=$sz)不能识别或不符合标准"
				;;
			esac
			if [ -n "$res" ]; then
				echo "识别到图标icon.png文件的分辨率为$res"
				echo "将当前目录下的icon.png图标文件移动到$foldname/entries/icons相应目录下"
				mv -f icon.png $foldname/entries/icons/hicolor/$res/apps/${appname}_icon.png
				iconpath=$foldname/entries/icons/hicolor/$res/apps/${appname}_icon.png
			fi
		else
			echo "icon.png不是真实的png格式图片"
		fi
	else
		iconpath=""
		for d in $foldname/entries/icons/hicolor/*/apps
		do
		    if [ $(ls -A $d) ]; then
		        for f in $d/*.png
		        do
		    	if [ -z "$iconpath" ]; then
		    		iconpath=$f
		    	else
		    		rm -f $f
		    	fi
		        done	
		    fi
		done
	fi
	echo "iconpath=$iconpath"
	echo ""
}

function make_desktop()
{
	echo "make desktop file"
	cd $basedir/$foldname	
	desktop_file=""
	if [ $(ls -A entries/applications) ]; then
	    for f in entries/applications/*.desktop
	    do
		#echo "f=$f"
		size=`stat -c "%s" $f`
		if [[ $size > 0 ]]; then
			if [ -z $desktop_file ]; then
				desktop_file=$f
			else
				echo "错误:在 entries/applications 下发现多个不为空的desktop文件"
				echo ""
				return 1
			fi
		else
			echo "删除空文件$f"
			rm -f $f
		fi
	    done
	fi
	if [ -n "$desktop_file" ]; then
		echo "发现desktop文件，输入y表示使用该文件，输入q表示删除并重建该文件(默认为y)"
		_do_sel2
		if [ $? = 1 ]; then
			echo ""
			return 0
		fi
	fi	
	if [ -e info ]; then
		size=`stat -c "%s" info`
	fi
	if [ -z "$exepath" ]; then
		echo "可执行程序路径为空，不创建桌面快捷方式"
		echo ""
		return 1
	fi
	if [ -z "$iconpath" ]; then
		echo "没有找到程序图标，桌面快捷方式使用系统默认图标"
	fi
	echo -n "请指定桌面图标的中文名(默认为空) : "
	read ch_name
cat >entries/applications/$appname.desktop <<EOF
[Desktop Entry]
Comment="$appname"
Exec="/opt/apps/$exepath"
Icon=/opt/apps/$iconpath
Name=$appname
Name[zh_CN]=$ch_name
Type=Application
X-Deepin-Vendor=user-custom
EOF
	if [ -z "$iconpath" ]; then
		sed -i "/^Icon/d" entries/applications/$appname.desktop
	fi
	if [ -z "$ch_name" ]; then
		sed -i "/^Name\[/d" entries/applications/$appname.desktop
	fi
	echo ""
	return 0
}

function _fix_control()
{
	if [ ! -d debian ]; then
		echo "debian目录不存在"
		echo ""
		return 1
	fi
	cd debian
	if [ ! -e control ]; then
		echo "control文件不存在"
		echo ""
		return 1
	fi
	sed -i "s/^Section.*$/Section\: utils/" control
	sed -i "s/^Architecture.*$/Architecture\: $arch/" control
	sed -i "s/^Homepage.*$/Homepage\: $DEBEMAIL/" control
	#sed -i "s/^Section.*$/Section\:utils/" control
	cd ..
}

function make_package_1()
{
	#生成debian目录
	echo "make package 1, 生成打包关键文件(debian目录)"
	cd $basedir

	#echo ""
	#echo "删除历史文件"
	#rm ../${foldname}_$version* >/dev/null 2>/dev/null
	#rm ../${foldname}_$version*.dsc > /dev/null
	#rm ../${foldname}_$version*.xz > /dev/null

	echo ""
	echo "创建debian目录"
	if [ -e debian ]; then
		#echo "当前目录下存在 debian 文件夹，输入y表示使用现有文件夹，输入q表示删除并重建该文件夹(默认为y)"
		#_do_sel2
		#if [ $? = 1 ]; then
		#	echo ""
		#	return 0
		#else
		#	rm -rdf debian
		#fi
		echo "存在旧的debian文件夹，删除该文件夹"
		rm -rdf debian
		if [ ! $? = 0 ]; then
			echo "删除失败，请检查是否是权限问题"
			echo ""
			return 1
		fi
	fi

	echo ""
	echo "打包初始化"
	dh_make --createorig -s
	rm debian/*.ex
	rm debian/*.EX
	
	echo "修复control文件"
	_fix_control

	echo ""
	echo "创建install文件"
	echo "$foldname/ /opt/apps" > debian/install

	echo ""
	echo "修改rules文件"
	sed -i "/\tdh\ /a override_dh_auto_build:\noverride_dh_shlibdeps:\noverride_dh_strip:\n" debian/rules

	add_autostart="yes"
	add_menu="yes"
	add_desktop="yes"
	if [ -e  $foldname/entries/applications/$appname.desktop ]; then
		if [ ! -e debian/postinst ]; then 
			echo ""
			echo "创建postinst文件"	
		if [ -f "$exepath" ]; then
			echo ""
			echo "是否创建桌面快捷方式？(默认为y)"
			_do_sel2
			if [ $? = 2 ]; then
				add_desktop="no"
			fi
			echo "是否创建添加到开始菜单？（默认为y）"
			_do_sel2
			if [ $? = 2 ]; then
				add_menu="no"
			fi
			echo "是否设置为开机自启动?（默认为y）"
			_do_sel2
			if [ $? = 2 ]; then
				add_autostart="no"
			fi
		fi
if [ "$add_desktop" = "yes" ]; then
cat <<EOF >>debian/postinst
if [ -d /home/$USER/Desktop ]; then
	chmod a+x /opt/apps/$foldname/entries/applications/$appname.desktop
	cp /opt/apps/$foldname/entries/applications/$appname.desktop /home/$USER/Desktop/
elif [ -d /home/$USER/桌面 ]; then
	chmod a+x /opt/apps/$foldname/entries/applications/$appname.desktop
	cp /opt/apps/$foldname/entries/applications/$appname.desktop /home/$USER/桌面/
fi
EOF
fi

if [ "$add_menu" = "yes" ]; then
cat <<EOF >>debian/postinst
cp /opt/apps/$foldname/entries/applications/$appname.desktop /usr/share/applications/
EOF
fi

if [ "$add_autostart" = "yes" ]; then
cat <<EOF >>debian/postinst
if [ -e /etc/xdg/autostart ]; then
cp /opt/apps/$foldname/entries/applications/$appname.desktop /etc/xdg/autostart/
fi
EOF
fi
if [ "$add_autostart" = "yes" ]; then
	cp $foldname/entries/applications/$appname.desktop $foldname/entries/autostart
	if [ -f $foldname/info ]; then
		sed -i 's/"autostart":.*$/"autostart": true,/' $foldname/info
	fi
fi
		fi
		if [ ! -e debian/prerm ]; then
			echo ""
			echo "创建prerm文件"
cat <<EOF >debian/prerm
tmp="/home/$USER/Desktop/$appname.desktop"
if [ -e \$tmp ]; then
	rm \$tmp
fi
tmp="/usr/$USER/桌面/$appname.desktop"
if [ -e \$tmp ]; then
	rm \$tmp
fi
tmp="/usr/share/applications/$appname.desktop"
if [ -e \$tmp ]; then
	rm \$tmp
fi
tmp="/etc/xdg/autostart/$appname.desktop"
if [ -e \$tmp ]; then
	rm \$tmp
fi
EOF
		fi
	fi	

	echo ""
	return 0
}

function make_package_2()
{
	cd $basedir
	chk=`ls ../${foldname}_$version* | grep -v .deb$`
	if [ -z "$chk" ]; then
		echo "缺少打包所需的相关文件，请先执行第5步，完成打包前的准备工作"
		echo ""
		return 0
	fi

	echo "make package 2, 执行打包"
	dpkg-source -b .
	dpkg-buildpackage -us -uc -nc
	
	echo ""
	echo "make package ok 打包完成,安装包生成在本文件夹上级目录下"
	echo ""
}

function do_choice()
{
	while [ 1 ]; do
	echo "1. 创建entries目录"
	echo "2. 移动files文件夹中的文件和图标文件"
	echo "3. 创建info文件"
	echo "4. 创建desktop文件"
	echo "5. 创建并修改debian文件夹"
	echo "6. 生成deb安装包文件"
	echo "7. 退出"
	echo -n "请选择要进行的操作:"
	read choice
	echo ""
	if [ "$choice" = "1" ]; then
		make_entries
	elif [ "$choice" = "2" ]; then
		file_move
	elif [ "$choice" = "3" ]; then
		make_info
	elif [ "$choice" = "4" ]; then
		make_desktop
	elif [ "$choice" = "5" ]; then
		make_package_1
	elif [ "$choice" = "6" ]; then
		make_package_2
	elif [ "$choice" = "7" ]; then
		echo "清除创建文件包时产生的临时文件？"
		_do_sel2
		if [ "$?" = "1" ]; then
			ls ../${foldname}_$version* | grep -v .deb$ | xargs rm
			echo "清理打包产生的临时文件完成"
		fi
		echo ""
		return
	else
		echo "输入错误"
	fi 
	done
}

if [ "$1" = "-h" ]; then
	show_help
	exit
fi

if [ -z "$1" ]; then
show_help
echo "按回车键继续。。。"
read key
echo "----------------------------------------------------"
echo ""
fi

precheck
if [ ! $? = 0 ]; then
	exit
fi

if [ "$1" = "-q" ]; then
	make_entries
	file_move
	make_info
	make_desktop
	make_package
else
	do_choice
fi
