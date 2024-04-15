第16行~最后一行，构成一个自调用函数
22行： 声明jQuery函数对象
25行： 声明jQuery.jQuery函数对象
30~34：_jQuery = window.jQuery,_$ = window.$,可以看出以_开头的，是全局对象（window的成员变量）
41~67： 声明了一些正则表达式对象
70行： 声明fcamelCase函数对象
87~92： 把一些js原生对象的方法重命名，方便以后使用
97~320： 定义了jQuery函数对象的原型
98： 定义constructor属性
99~208： init: function( selector, context, rootjQuery )
103： 如果selector参数为空，返回this（即jQuery的原型）