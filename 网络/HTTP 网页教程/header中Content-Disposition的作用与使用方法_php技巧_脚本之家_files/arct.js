jbMap = window.jbMap || {};
function jbViaJs(locationId) {
    var _f = undefined;
    var _fconv = 'jbMap[\"' + locationId + '\"]';
    try {
        _f = eval(_fconv);
        if (_f != undefined) {
            _f()
        }
    } catch(e) {}
}
function jbLoader(closetag) {
    var jbTest = null,
    jbTestPos = document.getElementsByTagName("span");
    for (var i = 0; i < jbTestPos.length; i++) {
        if (jbTestPos[i].className == "jbTestPos") {
            jbTest = jbTestPos[i];
            break
        }
    }
    if (jbTest == null) return;
    if (!closetag) {
        document.write("<span id=jbTestPos_" + jbTest.id + " style=display:none>");
        jbViaJs(jbTest.id);
        return
    }
    document.write("</span>");
    var real = document.getElementById("jbTestPos_" + jbTest.id);
    for (var i = 0; i < real.childNodes.length; i++) {
        var node = real.childNodes[i];
        if (node.tagName == "SCRIPT" && /closetag/.test(node.className)) continue;
        jbTest.parentNode.insertBefore(node, jbTest);
        i--
    }
    jbTest.parentNode.removeChild(jbTest);
    real.parentNode.removeChild(real)
}

var logo_m='<a href="http://www.6379965.com/logo.htm" target="_blank"><img src="http://files.jb51.net/image/shouji_jbbc.jpg" width=370 height=60 /></a>';
var logo_r='<a href="http://vps.zzidc.com/tongji/jb51.html" target="_blank"><img src="http://files.jb51.net/image/zzidc370.gif" width=370 height=60 /></a>';

var aliyun1000='<div class="mainlr"><a href="http://click.aliyun.com/m/29949/" target="_blank"><img src="http://files.jb51.net/image/ali1000.png" alt="cdnoss" width="1000" height="60"></a></div><div class="blank5"></div>';
aliyun1000+='<div class="mainlr"><a href="https://cloud.tencent.com/act/bargin?fromSource=gwzcw.684050.684050.684050" target="_blank"><img src="http://files.jb51.net/image/tengxunyun.gif" alt="mtyun" width="1000" height="60"></a></div><div class="blank5"></div>';
var aliyun10002='<div class="blank5"></div><div class="mainlr"><a href="https://www.niaoyun.com/act/20171111/?utm_source=jbzj&utm_medium=cpc&utm_term=jbzj&utm_content=jbzj&utm_campaign=jbzj" target="_blank"><img src="http://files.jb51.net/image/xiaoniaoyun1000.png" alt="yipinweike" width="1000" height="60"></a></div>';	
aliyun10002+='<div class="blank5"></div><div class="mainlr"><iframe src="https://union.zbj.com/adrc?iKey=DtY%2B1%2F3N2HD46859xrw2lbvI0sYTs6k9LuTZPwJ9tEYw43hcC5ZjB%2FzP0dX7JPHT&uf=showad" width="1000" height="60" align="center,center" vspace="0" hspace="0" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" style="border:0; vertical-align:bottom;margin:0;" allowtransparency="true"></iframe></div>';

var idctu="";
idctu+='<scr'+'ipt async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></scr'+'ipt><!--thea+300*250--><ins class="adsbygoogle"style="display:inline-block;width:300px;height:250px"data-ad-client="ca-pub-6389290466807248"data-ad-slot="6788945816"></ins><scr'+'ipt>(adsbygoogle=window.adsbygoogle||[]).push({});</scr'+'ipt><div class="blank10"></div>';
idctu+='<A href="http://click.aliyun.com/m/21950/" target=_blank><IMG alt="" src="http://files.jb51.net/image/ali_300_1.jpg" width="300" height="100"></A><div class="blank10"></div>';
idctu+='<A href="http://http.zhimaruanjian.com/" target=_blank><IMG alt="" src="http://files.jb51.net/image/zhimaruanjian.gif" width="300" height="100"></A><div class="blank10"></div>';
idctu+='<A href="https://youhui.jb51.net/" target=_blank><IMG alt="" src="http://files.jb51.net/image/yh1212.png" width="300" height="100"></A><div class="blank10"></div>';

var aliwenzi='<li><a href="http://click.aliyun.com/m/15321/" target="_blank"><span style="color:red;">30??????????????????6????>></span></a></li>';
var ali237='<li><A href="http://click.aliyun.com/m/28331/" target=_blank><IMG alt="" src="http://files.jb51.net/image/ali237.jpg" width="237" height="60"></A></li>';
var ali2371='<li><A href="http://click.aliyun.com/m/17168/" target=_blank><IMG alt="" src="http://files.jb51.net/image/ali2371.jpg" width="237" height="60"></A></li>';

var tgtxt="";
tgtxt+='<div id="txtlink"><ul>';
tgtxt+='<li><a href="http://www.qqll.me/" target="_blank"><span style="color:red;">????????????10000IP????8??</span></a></li>';
tgtxt+=aliwenzi;
tgtxt+='<li><a href="http://www.zoneidc.com/" target="_blank"><span style="color:red;">1G??????49??/??????49??/??????89??</span></a></li>';
tgtxt+='<li><a href="http://edu.51cto.com/center/course/buy?qd=wenzi" target="_blank"><span style="color:red;">????IT????1????</span></a></li>';

tgtxt+='<li><a href="http://http.zhimaruanjian.com/" target="_blank"><span style="color:blue;">????????HTTP????IP,????????????</span></a></li>';
tgtxt+='<li><a href="http://www.2016idc.com/cdn.html" target="_blank"><span style="color:blue;">????????????????????CDN??????????</span></a></li>';
tgtxt+='<li><a href="http://www.kaivps.com/about-7-723.html" target="_blank"><span style="color:blue;">??????/????/????/??????????VPS????????</span></a></li>';
tgtxt+='<li><a href="http://youhui.jb51.net/" target="_blank"><span style="color:blue;">???????????????????? ??????????</span></a></li>';

tgtxt+='<li><a href="http://www.laoyuming.com" target="_blank"><span style="color:red;">??3000??????????????100???? ????????</span></a></li>';
tgtxt+='<li><a href="http://www.enkj.com/idc/" target="_blank"><span style="color:red;">????????DELL????????????????799????</span></a></li>';
tgtxt+='<li><a href="http://s.jb51.net" target="_blank"><span style="color:red;">??????????????????????</span></a></li>';
tgtxt+='<li><A href="http://www.jjidc.com/" target=_blank><span style="color:red;">???????? ?? ??????????????????IDC??????</span></A></li>';

tgtxt+='<li><a href="http://www.jhsm.cn/" target="_blank"><span style="color:blue;">??????/??????/????????/????????</span></a></li>';
tgtxt+='<li><a href="http://tools.jb51.net " target="_blank"><span style="color:blue;">????????????????</span></a></li>';
tgtxt+='<li><a href="http://www.021.net" target="_blank"><span style="color:blue;">???????? ????????????????????????????????</span></a></li>';
tgtxt+='<li><a href="http://www.xmwzidc.cn/" target="_blank"><span style="color:blue;">??????????????????????????????????</span></a></li>';

tgtxt+='<li><a href="http://www.ku86.com/" target="_blank"><span style="color:red;">??????????618??????????????4??</span></a></li>';
tgtxt+='<li><a href="http://vps.zzidc.com/tongji/jb51w.html" target="_blank"><span style="color:red;">????????????5??????????????????????</span></a></li>';
tgtxt+='<li><a href="http://www.hkcn2.com/51.htm" target="_blank"><span style="color:red;">**????????10m????????????????999??**</span></a></li>';
tgtxt+='<li><a href="http://s.jb51.net/?txt" target="_blank"><span style="color:red;">??????????????????</span></a></li>';

tgtxt+='<li><a href="https://www.50vm.com/" target="_blank"><span style="color:blue;">4??????199/16??????360|????????</span></a></li>';
tgtxt+='<li><a href="http://cloud.pdidc.com/" target="_blank"><span style="color:blue;">????????????????????4????????30??/????</span></a></li>';
tgtxt+='<li><a href="http://www.zitian.cn/Products/zhongyuan/overview.aspx" target="_blank"><span style="color:blue;">??????????????????????????????????</span></a></li>';
tgtxt+='<li><a href="http://www.7yc.com/rent.html" target="_blank"><span style="color:blue;">????????????????100G????????450??</span></a></li>';

tgtxt+='<li><a href="http://www.33ip.com/" target="_blank"><span style="color:red;">????????-????????10M????-399/??</span></a></li>';
tgtxt+='<li><a href="http://www.gwidc.com/html/server_zy_xz.asp" target="_blank"><span style="color:red;">????????-????????16??32G 999/??~</span></a></li>';
tgtxt+='<li><a href="http://www.ssf.cc/" target="_blank"><span style="color:red;">????vps20/????799/????350/45????</span></a></li>';
tgtxt+='<li><a href="http://www.xiaozhiyun.com/2016/" target="_blank"><span style="color:red;">????\????\?????????????? ????????</span></a></li>';

tgtxt+='<li><a href="http://www.139w.com/" target="_blank"><span style="color:blue;">??????????????????????????999??</span></a></li>';
tgtxt+='<li><a href="http://www.360jq.com/hkshuang.htm" target="_blank"><span style="color:blue;">[??????????]????CC??DDOS/??????????</span></a></li>';
tgtxt+='<li><a href="http://www.cyidc.cc/" target="_blank"><span style="color:blue">???????? ?????????? ?????? 998??</span></a></li>';
tgtxt+='<li><a href="http://www.wdw6.com/" target="_blank"><span style="color:blue;">??????????  199????</span></a></li>';

tgtxt+='<li><a href="http://www.wsisp.net/sale/20170518/?indexjb" target="_blank"><span style="color:red;">???~?}5M??????????599/???}?~??</span></a></li>';
tgtxt+='<li><a href="http://www.qy.com.cn/" target="_blank"><span style="color:red;">??????????????10M????30G????,49????</span></a></li>';
tgtxt+='<li><a href="http://www.tuidc.com/" target="_blank"><span style="color:red;">??????????/????-????????/????????????</span></a></li>';
tgtxt+='<li><a href="https://www.zllyun.com/cloud.shtml" target="_blank"><span style="color:red;">????????,??????????????-Opstack??????</span></a></li>';
tgtxt+='</ul><DIV class=clearfix></DIV></div>';
tgtxt+=aliyun10002;

var tonglan1="";
tonglan1+=aliyun1000;
tonglan1+=tgtxt;
tonglan1+='<div class="blank6"></div>';
tonglan1+='<div class="topimg"><ul>';
tonglan1+='<li><A href="https://www.west.cn/services/cloudhost/?link=jb51" target=_blank><IMG alt="" src="http://files.jb51.net/image/west263_index.gif" width="237" height="60"></A></li>';
tonglan1+=ali2371;
tonglan1+='<li><A href="http://www.haikeyun.net/new/cloud/cloud.asp" target=_blank><IMG alt="" src="http://files.jb51.net/image/xinghaivps.gif" width="237" height="60"></A></li>';
tonglan1+='<li><A href="http://www.8dwww.com/product/list/11754.html" target=_blank><IMG alt="" src="http://files.jb51.net/image/8dwww.gif" width="237" height="60"></A></li>';
tonglan1+='</ul></div><div class="blank6"></div>';

var tonglan1_2="";
tonglan1_2+=aliyun1000;
tonglan1_2+=tgtxt;
tonglan1_2+='<div class="blank6"></div>';
tonglan1_2+='<div class="topimg"><ul>';
tonglan1_2+='<li><A href="http://www.8dwww.com/product/list/11754.html" target=_blank><IMG alt="" src="http://files.jb51.net/image/8dwww.gif" width="237" height="60"></A></li>';
tonglan1_2+='<li><A href="https://www.wsisp.net/sale/20170110/?jb51" target=_blank><IMG alt="" src="http://files.jb51.net/image/ws237.gif" width="237" height="60"></A></li>';
tonglan1_2+=ali237;
tonglan1_2+='<li><A href="http://www.haikeyun.net/new/cloud/cloud.asp" target=_blank><IMG alt="" src="http://files.jb51.net/image/xinghaivps.gif" width="237" height="60"></A></li>';
tonglan1_2+='</ul></div><div class="blank6"></div>';

var tonglan2='<a href="http://www.v01.cn" alt="????????" target="_blank"><img src="http://files.jb51.net/image/zs960.gif" width="1000" height="60" border="0" /></a><div class="blank3"></div><a href="http://tuidc.com" alt="???????? ????????" target="_blank"><img src="http://files.jb51.net/image/host5_960.gif" width="1000" height="60" border="0" /></a>';
var tonglan2_1='<a href="http://www.v01.cn" alt="????????" target="_blank"><img src="http://files.jb51.net/image/zs960.gif" width="1000" height="60" border="0" /></a>';
var tonglan2_2='<a href="http://www.tuidc.com" alt="????" target="_blank"><img src="http://files.jb51.net/image/tuidc_1000.gif" width="1000" height="60" border="0" /></a>';

var tonglan3_1='<div class="mainlr"><a href="http://www.qy.com.cn" target="_blank"><img src="http://files.jb51.net/image/qy_1000.gif" width="1000" height="60"></a></div><div class="blank5"></div>';

var tonglan3_2='<div class="topimg"><ul>';
tonglan3_2+='<li><A href="https://www.west.cn/services/cloudhost/?link=jb51" target=_blank><IMG alt="" src="http://files.jb51.net/image/west263_index.gif" width="237" height="60"></A></li>';
tonglan3_2+='<li><A href="http://www.jjidc.com" target=_blank><IMG alt="" src="http://files.jb51.net/image/jjidc237.gif" width="237" height="60"></A></li>';
tonglan3_2+='<li><A href="http://www.enkj.com/idc/" target=_blank><IMG alt="" src="http://files.jb51.net/image/enkj237.gif" alt="????????" width="237" height="60"></A></li>';
tonglan3_2+='<li><A href="http://www.cyidc.cc/" target=_blank><IMG alt="" src="http://files.jb51.net/image/cyidc237.gif" width="237" height="60"></A></li>';
tonglan3_2+='</ul></div>';

var botad='<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>';
botad+='<ins class="adsbygoogle" style="display:inline-block;width:336px;height:280px" data-ad-client="ca-pub-6384567588307613" data-ad-slot="6445926239" data-override-format="true" data-page-url="http://www.jb51.net"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>';

var idctu1='<div class="idc3"><a href="http://www.021.net" target="_blank"><h1>????????</h1><span>??????????????</span> </a><a href="http://www.geisnic.com/" target="_blank"><h1>????????</h1><span>VPS????</span> </a><a href="http://www.33ip.com" target="_blank"><h1>????????</h1><span>IDC??????</span> </a></div>';

var idctu2='<a href="http://tuidc.com" target="_blank"><img src="http://files.jb51.net/image/tengyou300.gif" width="300" height="100"></a>';
idctu2+='<div class="blank10"></div><a href="http://www.enkj.com/encloud/" target="_blank"><img src="http://files.jb51.net/image/enkj300.gif" alt="????????" width="300" height="100"></a>';
//idctu2+='<div class="blank10"></div><iframe src="http://union.zbj.com/adrc?iKey=DtY%2B1%2F3N2HD46859xrw2ld23lcRFYmEfqdYH8tMD8F%2BBOiMXY9peXQ%3D%3D&uf=showad" width="300" height="100" align="center,center" vspace="0" hspace="0" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" style="border:0; vertical-align:bottom;margin:0;" allowtransparency="true"></iframe>';

/*******---------????????start----------********/
var bctools='<li><a href="http://tools.jb51.net/code/css" target="_blank"><font color="red">CSS????????</font></a></li>';
bctools+='<li><a href="http://tools.jb51.net/code/js" target="_blank"><font color="red">JavaScript??????????????</font></a></li>';
bctools+='<li><a href="http://tools.jb51.net/code/xmlformat" target="_blank">????XML??????/????????</a></li>';
bctools+='<li><a href="http://tools.jb51.net/code/phpformat" target="_blank"><font color="red">php??????????????????????</font></a></li>';
bctools+='<li><a href="http://tools.jb51.net/code/sqlcodeformat" target="_blank">sql??????????????????????</a></li>';
bctools+='<li><a href="http://tools.jb51.net/transcoding/html_transcode" target="_blank">????HTML????/??????????</a></li>';
bctools+='<li><a href="http://tools.jb51.net/code/json" target="_blank">????JSON????????/????/????/??????</a></li>';
bctools+='<li><a href="http://tools.jb51.net/regex/javascript" target="_blank">JavaScript????????????????</a></li>';
bctools+='<li><a href="http://tools.jb51.net/transcoding/jb51qrcode" target="_blank">??????????????????(??????)</a></li>';
bctools+='<li><a href="http://tools.jb51.net/" target="_blank">????????????</a></li>';
/*******---------????????end----------********/


//u336546
var tonglanbd='<scr'+'ipt type="text/javascript" src="http://dm.jb51.net/cmds5flr1.js"></scr'+'ipt>';

var art_up = '<scri'+'pt type="text/javascript" src="http://dm.jb51.net/gn3a1ecf96f1ccff30db1c7481b2b03ded00b3930a3ef6.js"></s'+'cript>';

//u3025827(u776243)
var art_down = '<scr'+'ipt type="text/javascript" src="http://dm.jb51.net/z8dje9abx1.js"></scr'+'ipt>';

var art_down2 = '<scrip'+'t type="text/javascript" src="http://dm.jb51.net/tb3a1ecf96f1cdf739db1c7481b2b03ded00b3930a3ef6.js"></s'+'cript>';

//var art_down3 = '<scri'+'pt type="text/javascript" src="http://dm.jb51.net/mhzqnndqnkon.js"></s'+'cript>';

var side_up = '<scri'+'pt async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></scri'+'pt>';
side_up+='<ins class="adsbygoogle" style="display:inline-block;width:300px;height:250px" data-ad-client="ca-pub-6384567588307613" data-ad-slot="2817964327"></ins><scri'+'pt>(adsbygoogle = window.adsbygoogle || []).push({});</s'+'cript>';

var r_2 = '<script type="text/javascript">var cpro_id="u1397867";(window["cproStyleApi"] = window["cproStyleApi"] || {})[cpro_id]={at:"3",rsi0:"300",rsi1:"380",pat:"6",tn:"baiduCustNativeAD",rss1:"#FFFFFF",conBW:"1",adp:"1",ptt:"0",titFF:"%E5%BE%AE%E8%BD%AF%E9%9B%85%E9%BB%91",titFS:"14",rss2:"#000000",titSU:"0",ptbg:"90",piw:"0",pih:"0",ptp:"0"}</script><script src="http://cpro.baidustatic.com/cpro/ui/c.js" type="text/javascript"></script>';

var fudong = '<scri'+'pt type="text/javascript">var cpro_id="u1397867";(window["cproStyleApi"] = window["cproStyleApi"] || {})[cpro_id]={at:"3",rsi0:"300",rsi1:"380",pat:"6",tn:"baiduCustNativeAD",rss1:"#FFFFFF",conBW:"1",adp:"1",ptt:"0",titFF:"%E5%BE%AE%E8%BD%AF%E9%9B%85%E9%BB%91",titFS:"14",rss2:"#000000",titSU:"0",ptbg:"90",piw:"0",pih:"0",ptp:"0"}</sc'+'ript>';
fudong += '<scrip'+'t src="http://cpro.baidustatic.com/cpro/ui/c.js" type="text/javascript"></scr'+'ipt>';

var gg_l = '<scri'+'pt async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></scri'+'pt>';
gg_l += '<ins class="adsbygoogle" style="display:inline-block;width:300px;height:250px" data-ad-client="ca-pub-6384567588307613" data-ad-slot="6438537127"></ins>';
gg_l += '<scri'+'pt>(adsbygoogle = window.adsbygoogle || []).push({});</s'+'cript>';

//u811641
var gg_r = '<scri'+'pt type="text/javascript" src="http://dm.jb51.net/bwyffvsfzdec.js"></sc'+'ript>';

var r1gg='<scri'+'pt async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></scri'+'pt>';
r1gg+='<ins class="adsbygoogle" style="display:inline-block;width:300px;height:250px" data-ad-client="ca-pub-6384567588307613" data-ad-slot="2817964327"></ins><scri'+'pt>(adsbygoogle = window.adsbygoogle || []).push({});</s'+'cript>';
/*
var r1gg = '<scri'+'pt async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></scri'+'pt><ins class="adsbygoogle" style="display:inline-block;width:300px;height:250px" data-ad-client="ca-pub-1247620132145618" data-ad-slot="2253650178" data-override-format="true" data-page-url="http://www.jb51.net"></ins><scri'+'pt>(adsbygoogle = window.adsbygoogle || []).push({});</s'+'cript>';
*/
//u2261513
//var bd200 = '<scri'+'pt type="text/javascript" src="http://dm.jb51.net/hod9xqa8sj.js"></sc'+'ript>';

var bd200 = '<scri'+'pt type="text/javascript">var cpro_id="u2261513";(window["cproStyleApi"] = window["cproStyleApi"] || {})[cpro_id]={at:"3",rsi0:"300",rsi1:"300",pat:"6",tn:"baiduCustNativeAD",rss1:"#FFFFFF",conBW:"1",adp:"1",ptt:"0",titFF:"%E5%BE%AE%E8%BD%AF%E9%9B%85%E9%BB%91",titFS:"14",rss2:"#000000",titSU:"0",ptbg:"90",piw:"0",pih:"0",ptp:"0"}</sc'+'ript>';
bd200 += '<scrip'+'t src="http://cpro.baidustatic.com/cpro/ui/c.js" type="text/javascript"></scr'+'ipt>';

var dxy728 = '<a href="http://www.33ip.com" target="_blank"><img src="http://files.jb51.net/image/33ip_728.gif"></a>';
var dxy230 = '<a href="http://edu.jb51.net/" target="_blank"><img src="http://files.jb51.net/image/edu230.png" width=260 height=90></a>';

//u1424765
var qq_index = '<scri'+'pt type="text/javascript" src="http://dm.jb51.net/rldzo3l5kz.js"></scri'+'pt>';

jbMap['logo_m'] = function() {
	document.writeln(logo_m);
};

jbMap['logo_r'] = function() {
	document.writeln(logo_r);
};

jbMap['idctu'] = function() {
	document.writeln(idctu);
};

jbMap['tonglanbd'] = function() {
	document.writeln(tonglanbd);
};

jbMap['tonglan1'] = function() {
	document.writeln(tonglan1);
};

jbMap['tonglan1_2'] = function() {
	document.writeln(tonglan1_2);
};

jbMap['tonglan2'] = function() {
	document.writeln(tonglan2);
};

jbMap['tonglan2_1'] = function() {
	document.writeln(tonglan2_1);
};

jbMap['tonglan2_2'] = function() {
	document.writeln(tonglan2_2);
};

jbMap['tonglan3_1'] = function() {
	document.writeln(tonglan3_1);
};

jbMap['tonglan3_2'] = function() {
	document.writeln(tonglan3_2);
};

jbMap['botad'] = function() {
	document.writeln(botad);
};

jbMap['idctu1'] = function() {
	document.writeln(idctu1);
};

jbMap['idctu2'] = function() {
	document.writeln(idctu2);
};


jbMap['art_up'] = function() {
	document.writeln(art_up);
};

jbMap['art_down'] = function() {
	document.writeln(art_down);
};

jbMap['art_down2'] = function() {
	document.writeln(art_down2);
};

jbMap['side_up'] = function() {
	document.writeln(side_up);
};

jbMap['r_2'] = function() {
	document.writeln(r_2);
};

jbMap['fudong'] = function() {
	document.writeln(fudong);
};


jbMap['gg_l'] = function() {
	document.writeln(gg_l);
};

jbMap['gg_r'] = function() {
	document.writeln(gg_r);
};

jbMap['r1gg'] = function() {
	document.writeln(r1gg);
};

jbMap['bd200'] = function() {
	document.writeln(bd200);
};


jbMap['bctools'] = function() {
	document.writeln(bctools);
};

jbMap['dxy728'] = function() {
	document.writeln(dxy728);
};

jbMap['dxy230'] = function() {
	document.writeln(dxy230);
};

jbMap['qq_index'] = function() {
	document.writeln(qq_index);
};

if (jQuery) { 
$jb51_top = $('#jb51_topbar');
if($jb51_top){
    $jb51_top.html('<div class="userbar"><a href="http://tougao.jb51.net" target="_blank">????????</a><img style="width:32px; height:22px" src="http://img.jb51.net/skin/2016/images/newn.gif" alt="hot"></div>');
}

$addnav = $('.watch');
if($addnav){
    $addnav.before('<li><div class="one"><a href="http://wxbj.jb51.net" target="_blank">??????????</a></div></li>');
	$(".watch .one a").attr("href","http://www.jb51.net/about.htm");
}


if ("undefined" != typeof ourl) {
    if (ourl) {
        $content = $('#content');
        if($content){
			if(ourl.indexOf(":") > 0 ){
            $content.append('<p>??????????' + ourl +'</p>');
			}else{
			$content.append('<p>??????????' + base64decode(ourl) +'</p>');
			}
        }
    }
}

var shequlink = '<p class="content-shequ">????????????????????????????????????????????????????????????  <a href="http://shequ.jb51.net" target="_blank">????????????</a></p>'
$content = $('#content');
if($content){$content.append(shequlink);}

//var el = $('#footer'); 
//el.html(el.html().replace(/????????/ig, '????????????????????????'));
}