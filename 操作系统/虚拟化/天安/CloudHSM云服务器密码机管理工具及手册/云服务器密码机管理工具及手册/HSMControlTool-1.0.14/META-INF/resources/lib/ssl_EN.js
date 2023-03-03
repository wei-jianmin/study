function Dsy()
		{
			this.Items = {};
		}
		Dsy.prototype.add = function(id,iArray)
		{
			this.Items[id] = iArray;
		}
		Dsy.prototype.Exists = function(id)
		{
			if(typeof(this.Items[id]) == "undefined") return false;
			return true;
		}

		function change(v){
			var str="0";
			for(i=0;i <v;i++){ str+=("_"+(document.getElementById(s[i]).selectedIndex-1));};
			var ss=document.getElementById(s[v]);
			with(ss){
				length = 0;
				options[0]=new Option(opt0[v],opt0[v]);
				if(v && document.getElementById(s[v-1]).selectedIndex>0 || !v)
				{
					if(dsy.Exists(str)){
						ar = dsy.Items[str];
						for(i=0;i <ar.length;i++)options[length]=new Option(ar[i],ar[i]);
						if(v)options[1].selected = true;
					}
				}
				if(++v <s.length){change(v);}
			}
		}

		var dsy = new Dsy();

		dsy.add("0",["CN-中国"]);

		dsy.add("0_0",["请选择省/自治区","Anhui","Beijing","Fujian","Gansu","Guangdong","Guangxi","Guizhou","Hainan","Hainan","Henan","HeiLongjiang","Hubei ","Hunan ","Jilin ","Jiangsu ","Jiangxi ","Liaoning ","Nei Menggu","Ningxia","Qinghai","Shandong","Shanxi","Shaanxi","Shanghai","Sichuan","Tianjin","Xizang","Xinjiang","Yunnan","Zhejiang","Chongqing"]);

		dsy.add("0_0_1",["请选择市县","Anqing","Bengbu","Chaohu","Chizhou","Chuzhou","Fuyang","Hefei","Huaibei","Huainan","Mount Huang","Liuan","Ma Anshan","Suzhou","Tongling","Wuhu","Xuancheng","Bozhou"]);
		dsy.add("0_0_2",["请选择市县","Beijing"]);
		dsy.add("0_0_3",["请选择市县","Fuzhou ","Longyan","Nanping","Ningde","Putian","Quanzhou","Sanming","Xiamen","Zhangzhou"]);
		dsy.add("0_0_4",["请选择市县","Baiyin","Dingxi","Tibetan Autonomous Prefecture of Gannan","Jiayuguan","Jinchang","Jiuquan","Lanzhou","Hui Autonomous Prefecture of Linxia","Longnan","Pingliang","Qingyang","Tianshui","Wuwei","Zhangye"]);
		dsy.add("0_0_5",["请选择市县","Chaozhou","Dongguan","Foshan","Guangzhou","Heyuan","Huizhou","Jiangmen","Jieyang","Maoming","Meizhou","Qingyuan","Shantou","Shanwei","Shaoguan","Shenzhen","Yangjiang","Yunfu","Zhanjiang","Zhaoqing","Zhongshan","Zhuhai"]);
		dsy.add("0_0_6",["请选择市县","Bose","Beihai","Chongzuo","Fang Chenggang","Guilin","Guigang","Hechi","Hezhou","Laibin","Liuzhou","Nanning","Qinzhou","Wuzhou","Yulin"]);
		dsy.add("0_0_7",["请选择市县","Anshun","Bijie","Guiyang","Liu Panshui","Qiandongnan Miao and Dong Autonomous Prefecture","Qiannan Buyei and Miao Autonomous Prefecture","Qianxi'nan Buyei and Miao Autonomous Prefecture","Tongren","Zunyi"]);
		dsy.add("0_0_8",["请选择市县","Baisha Li Autonomous County","Baoting Li and Miao Autonomous County","Changjiang Li Autonomous County","Cheng Maixain","Ding Anxain","Dongfang","Haikou","Ledong Li Autonomous County","Lin Gaoxian","Lingshui Li Autonomous County","Qionghai","Qiongzhong Li and Miao Autonomous County","Sanya","Tun Changxian","Wanning","Wenchang","Wu Zhishan","Danzhou"]);
		dsy.add("0_0_9",["请选择市县","Baoding","Cangzhou","Chengde","Handan","Hengshui","Langfang","Qinhuangdao","Shijiazhuang","Tangshan","Xingtai","Zhangjiakou"]);
		dsy.add("0_0_10",["请选择市县","Anyang","Hebi","Jiyuan","Jiaozuo","Kaifeng","Luoyang","Nanyang","Pingdingshan","Sanmenxia","Shangqiu","Xinxiang","Xinyang","Xuchang","Zhengzhou","Zhoukou","Zhumadian","Louhe","Puyang"]);
		dsy.add("0_0_11",["请选择市县","Daqing","Great Khingan","Harbin","Hegang","Heihe","Jixi","Kiamusze","Mudanjiang","Qitaihe","Tsitsihar","Shuangyashan","Suihua","Yichun"]);
		dsy.add("0_0_12",["请选择市县","Ezhou","Enshi Tujia and Miao Autonomous Prefecture","Huanggang","Yellowstone","Jingmen","Jingzhou","Qianjiang","Shennongjia Forestry District","Shiyan","Suizhou","Tianmen","Wuhan ","Xiantao","Xianning","Xiangfan","Xiaogan","Yichang"]);
		dsy.add("0_0_13",["请选择市县","Changde","Changsha","Chenzhou","Hengyang","Huaihua","Loudi","Shaoyang","Xiangtan","Xiangxi Tujia and Miao Autonomous Prefect","Yiyang","Yongzhou","Yueyang","Zhangjiajie","Zhuzhou"]);
		dsy.add("0_0_14",["请选择市县","Baicheng","Baisahn","Changchun ","Jilin","Liaoyuan","Siping","Songyuan","Tonghua ","Yanbian Korean Autonomous Prefecture"]);
		dsy.add("0_0_15",["请选择市县","Changzhou","Huaian","Lianyungang","Nanjing","Nantong","Suzhou","Suqian","Taizhou","Wuxi","Xuzhou","Yancheng","Yangzhou","Zhenjiang"]);
		dsy.add("0_0_16",["请选择市县","Fuzhou","Gan Zhou","Ji'an","Jingdezhen","Jiujiang","Nanchang","Pingxiang","Shangrao","Xinyu","Yichun","Yingtan"]);
		dsy.add("0_0_17",["请选择市县","Anshan","Benxi","Chaoyang","Dalian","Dandong","Fushun","Fuxin","Huludao","Jinzhou","Liaoyang","Panjin","Shenyang","Tieling","Yingkow"]);
		dsy.add("0_0_18",["请选择市县","Alxa League","Bayanzhuo'er Meng","Baotou","Chifeng","Erdos","Hohhot","Hulun Buir","Tongliao","Wuhai ","Ulanqab","Xilin Gol League","Xinganmeng"]);
		dsy.add("0_0_19",["请选择市县","Guyuan","Shizuishan","Wuzhong","Yinchuan"]);
		dsy.add("0_0_20",["请选择市县","Golog Tibetan Autonomous Prefecture","Haibei Tibetan Autonomous Prefecture","Haidong","Hainan Tibetan Autonomous Prefecture","Haixi Mongol and Tibetan Autonomous Prefecture","Huangnan Tibetan Autonomous Prefecture","Sining","Yushu Tibetan Autonomous Prefecture"]);
		dsy.add("0_0_21",["请选择市县","Binzhou","Dezhou","Dongying","Heze","Jinan","Jining","Laiwu","Liaocheng","Linyi","Qingdao","Rizhao","Tai'an","Weihai","Weifang","Yantai","Zaozhuang","Zibo"]);
		dsy.add("0_0_22",["请选择市县","Changzhi ","Datong","Jincheng","Jinzhong","Linfen","Lvliang","Shuozhou","Taiyuan","Xinzhou","Yangquan","Yuncheng "]);
		dsy.add("0_0_23",["请选择市县","Ankang","Baoji","Hanzhong","Shangluo","Tongchuan","Weinan","Xi'an","Xianyang","Yan'an","yulan"]);
		dsy.add("0_0_24",["请选择市县","Shanghai"]);
		dsy.add("0_0_25",["请选择市县","Aba Tibetan and qiang autonomous prefecture","Bazhong","Chengtu","Dazhou","Deyang","Ganzi Tibetan Autonomous Prefecture","Ziyang","GuangYuan","Leshan","Yi Autonomous Prefecture of Liangshan","Meisan","Mianyang","Nanchong","Neijiang","Panzhihua","Suining","Ya'an","Yibin","Ziyang","Zigong","Luzhou"]);
		dsy.add("0_0_26",["请选择市县","Tianjin"]);
		dsy.add("0_0_27",["请选择市县","Ali","Qamdo","Lhasa","Nyingchi","Naqu","Rikeze","Shannan"]);
		dsy.add("0_0_28",["请选择市县","Aksu","Alear","Bayingolin Mongol Autonomous Prefecture","Bortala Mongol Autonomous Prefecture","Changji Hui Autonomous Prefecture","Hami","Hetain","Kashgar","Karamay","Kizilsu Kirghiz Autonomous Prefecture","Shihezi","Tumushuke","Turpan","Urumchi","Wujiaqu","Ili Kazakh Autonomous Prefecture"]);
		dsy.add("0_0_29",["请选择市县","Baoshan","Chuxiong Yi Autonomous Prefectur","Dali Bai Autonomous prefecture","Dehong Dai and Jingpo Autonomous Prefecture","Deqen Tibetan Autonomous Prefecture","Honghe Hani and Yi Autonomous Prefecture","Kunming","Lijing","Lincang","The nu river lisu autonomous prefecture","Qujing","Simao","Wenshan Zhuang and Miao Autonomous Prefecture","Xishuangbanna Dai Autonomous Prefecture","Yuxi","Zhaotong"]);
		dsy.add("0_0_30",["请选择市县","Hangzhou","Huzhou","Jiaxing","Jinhua","Lishui","Ningbo","Shaoxing","Taizhou","Wenzhou","Zhoushan","Quzhou"]);
		dsy.add("0_0_31",["请选择市县","Chongqing"]);
		
		
		
		
		
		
		var s=["s1","s2","s3"];
		var opt0 = ["国家"];
	/* 	var opt0 = ["国家","",""]; */
		function setup()
		{
			for(i=0;i <s.length;i++)
				document.getElementById(s[i]).onchange=new Function("change("+(i+1)+")");
			change(0);
		}