xpath
    XPath，全称 XML Path Language，即 XML 路径语言，
    它是一门在XML文档中查找信息的语言
    XPath 可用来在 XML 文档中对元素和属性进行遍历
    XPath 包含一个标准函数库, 使用路径表达式在 XML 文档中进行导航
        XPath 使用路径表达式来选取 XML 文档中的节点或者节点集
        XPath 含有超过 100 个内建的函数。
        这些函数用于字符串值、数值、日期和时间比较、
            节点和 QName 处理、序列处理、逻辑值等等
    在 XPath 中，有七种类型的节点：元素、属性、文本、命名空间、处理指令、注释以及文档节点（或称为根节点）。
        XML 文档是被作为节点树来对待的。树的根被称为文档节点或者根节点。
    XPath 使用路径表达式来选取 XML 文档中的节点或节点集。
    节点是通过沿着路径 (path) 或者步 (steps) 来选取的。
    路径表达式语法：
        表达式	            描述
        ‘nodename’	        选取此节点的所有子节点。
        /	                从根节点选取（绝对路径），不以/开头，直接就是节点名，则表明是相对路径
        //	                从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。
        .	                选取当前节点。
        ..	                选取当前节点的父节点。
        @	                选取属性。
        []                  跟随在节点之后，用于在节点集中进行筛选，相当于伪选择器
        *                   匹配任何元素节点
        @*                  匹配任何属性节点。
        |                   或运算，将多个路径进行组合，达到选取多个路径的效果
        node()              匹配任何类型的节点。
        伪节点（轴）        内置关键字（伪节点之后，跟随:: ，用于明确真实节点）
            ancestor	        选取当前节点的所有先辈（父、祖父等）。
            ancestor-or-self	选取当前节点的所有先辈（父、祖父等）以及当前节点本身。
            attribute	        选取当前节点的所有属性。
            child	            选取当前节点的所有子元素。
            descendant	        选取当前节点的所有后代元素（子、孙等）。
            descendant-or-self	选取当前节点的所有后代元素（子、孙等）以及当前节点本身。
            following	        选取文档中当前节点的结束标签之后的所有节点。
            namespace	        选取当前节点的所有命名空间节点。
            parent	            选取当前节点的父节点。
            preceding	        选取文档中当前节点的开始标签之前的所有节点。
            preceding-sibling	选取当前节点之前的所有同级节点。
            self	            选取当前节点。
    举例：
        <?xml version="1.0" encoding="ISO-8859-1"?>
        <bookstore>
        <book>
          <title lang="eng">Harry Potter</title>
          <price>29.99</price>
        </book>
        <book>
          <title lang="eng">Learning XML</title>
          <price>39.95</price>
        </book>
        </bookstore>
        ------------------------------------------------------------------------------------------------
        路径表达式	        结果
        bookstore	        选取 bookstore 元素的所有子节点。
        /bookstore	        选取根元素 bookstore。
                            注释：假如路径起始于正斜杠( / )，则此路径始终代表到某元素的绝对路径！
        bookstore/book	    选取属于 bookstore 的子元素的所有 book 元素。
        //book	            选取所有 book 子元素，而不管它们在文档中的位置。
        bookstore//book	    选择属于 bookstore 元素的后代的所有 book 元素，
                            而不管它们位于 bookstore 之下的什么位置。
        //@lang	            选取名为 lang 的所有属性。
        /bookstore/*	    选取 bookstore 元素的所有子元素。
        //*	                选取文档中的所有元素。
        //title[@*]	        选取所有带有属性的 title 元素。
        ------------------------------------------------------------------------------------------------
        路径表达式	                        结果
        /bookstore/book[1]	                选取属于 bookstore 子元素的第一个 book 元素。
        /bookstore/book[last()]	            选取属于 bookstore 子元素的最后一个 book 元素。
        /bookstore/book[last()-1]	        选取属于 bookstore 子元素的倒数第二个 book 元素。
        /bookstore/book[position()<3]	    选取最前面的两个属于 bookstore 元素的子元素的 book 元素。
        //title[@lang]	                    选取所有拥有名为 lang 的属性的 title 元素。
        //title[@lang='eng']	            选取所有 title 元素，且这些元素拥有值为 eng 的 lang 属性。
        /bookstore/book[price>35.00]	    选取 bookstore 元素的所有 book 元素，
                                            且其中的 price 元素的值须大于 35.00。
        /bookstore/book[price>35.00]/title	选取 bookstore 元素中的 book 元素的所有 title 元素，
                                            且其中的 price 元素的值须大于 35.00
        //book/title | //book/price	        选取 book 元素的所有 title 和 price 元素。
        //title | //price	                选取文档中的所有 title 和 price 元素。
        /bookstore/book/title | //price	    选取属于 bookstore 元素的 book 元素的所有 title 元素，
                                            以及文档中所有的 price 元素。
        ------------------------------------------------------------------------------------------------                                            
        路径表达式              结果
        child::book	            选取所有属于当前节点的子元素的 book 节点。
        attribute::lang	        选取当前节点的 lang 属性。
        child::*	            选取当前节点的所有子元素。
        attribute::*	        选取当前节点的所有属性。
        child::text()	        选取当前节点的所有文本子节点。
        child::node()	        选取当前节点的所有子节点。
        descendant::book	    选取当前节点的所有 book 后代。
        ancestor::book	        选择当前节点的所有 book 先辈。
        ancestor-or-self::book	选取当前节点的所有 book 先辈以及当前节点（如果此节点是 book 节点）
        child::*/child::price	选取当前节点的所有 price 孙节点。
    运算符
        运算符	        描述	        实例	        返回值
        |	            计算两个节点集	//book | //cd	返回所有拥有 book 和 cd 元素的节点集
        +	            加法	        6 + 4	        10
        -	            减法	        6 - 4	        2
        *	            乘法	        6 * 4	        24
        div	            除法	        8 div 4	        2
        =	            等于	        price=9.80	    如果 price 是 9.80，则返回 true。
                                                        如果 price 是 9.90，则返回 false。
        !=	            不等于	        price!=9.80	    如果 price 是 9.90，则返回 true。
                                                        如果 price 是 9.80，则返回 false。
        <	            小于	        price<9.80	    如果 price 是 9.00，则返回 true。
                                                        如果 price 是 9.90，则返回 false。
        <=	            小于或等于	    price<=9.80	    如果 price 是 9.00，则返回 true。
                                                        如果 price 是 9.90，则返回 false。
        >	            大于	        price>9.80	    如果 price 是 9.90，则返回 true。
                                                        如果 price 是 9.80，则返回 false。
        >=	            大于或等于	    price>=9.80	    如果 price 是 9.90，则返回 true。
                                                        如果 price 是 9.70，则返回 false。
        or	            或	            price=9.80 or 	如果 price 是 9.80，则返回 true。
                                        price=9.70      如果 price 是 9.50，则返回 false。
        and	            与	            price>9.00 and 	如果 price 是 9.80，则返回 true。
                                        price<9.90      如果 price 是 8.50，则返回 false。
        mod	            计算除法的余数	5 mod 2	        1
        
xquery  
    简介：
        XQuery 天生支持 XPath 并将其作为 XQuery 语法的一部分，
        XQuery 显然能完成 XPath 所能完成的任何任务
        XQuery 采用一种简单的语法，
        混合了 XML、XPath、注释、函数以及将其结合在一起的专用表达式语法
        XQuery 代码完全由表达式组成，没有语句
        它和 SQL 非常类似，但是 XQuery 还额外提供了表达对结果集进行任意转换的功能
        如同从 XML 文档中检索数据应该使用 XPath 一样，
        从大型 XML 存储库中检索和转换数据时则应该使用 XQuery
        XPath 不支持函数，但XQuery 提供了一批重要的内置函数和运算符，
        而且还允许用户定义自己的函数                
        XQuery 函数是强类型的，支持递归，可声明为内部函数或外部函数 
        内部函数是函数体紧跟函数声明之后的标准函数。
        外部函数是一种开放实现的函数声明类型，用户可以用不同的编程语言定义函数体。
    用途：
        可以从现有的xml数据中按条件筛选结果，
        并可以对筛选结果内容进行修饰改造，
        最终对结果进行输出。
        不能起到修改原有xml数据的作用。
    简例：
        "books.xml" :
            <bookstore>
            <book category="烹饪">
              <title lang="中">鲁菜大全</title>
              <price>30.00</price>
            </book>
            <book category="儿童">
              <title lang="英">哈利波特</title>
              <price>29.99</price>
            </book>
            </bookstore>
        选择： doc("books.xml")/bookstore/book/title
        结果： <title lang="中">鲁菜大全</title>
               <title lang="英">哈利波特</title>
        附注： doc("books.xml")用于打开 "books.xml" 文件
    一些基本的语法规则：
        XQuery 对大小写敏感
        XQuery 的元素、属性以及变量必须是合法的 XML 名称。
        XQuery 字符串值可使用单引号或双引号。
        XQuery 变量由 “$” 并跟随一个名称来进行定义，举例，$bookstore
        XQuery 注释被 (: 和 :) 分割，例如，(: XQuery 注释 :)
        XQuery 把属性、文本内容、注释等，也分别视为节点
    使用for语句选择
        for $x  in doc("books.xml")/bookstore/book   
        where       $x/price>30         //选取条件，可省略
        order by    $x/title            //排序依据，可省略
        return $x/title
        说明：
            效果类似于：doc("books.xml")/bookstore/book[price>30]/title
            在执行完for后，搜索结果集已经存放于$x中了
            where把$x中不符合条件的删除掉
            order by把$x中的数据进行排序
        使用for语句可以做的更多：
            <ul>
            {
                for $x in doc("books.xml")/bookstore/book/title
                order by $x
                return <li>{$x}</li>    
            }
            </ul>
            以上代码的结果：
            <ul>
            <li><title lang="中">鲁菜大全</title></li>
            <li><title lang="英">哈利波特</title></li>
            </ul>
            而把上面的return语句改为：return <li>{data($x)}</li>，则结果为：
            <ul>
            <li>鲁菜大全</li>
            <li>哈利波特</li>
            </ul>
    使用if语句
        例：
        for $x in doc("books.xml")/bookstore/book
            return	if  ($x/@category = "儿童")
                    then <child>{data($x/title)}</child>
                    else <adult>{data($x/title)}</adult>
        结果：
        <adult>鲁菜大全</adult>
        <child>哈利波特</child>
        比较运算符：
            在 XQuery 中，有两种方法来比较值。
            1. 通用比较：=, !=, <, <=, >, >=
            2. 值的比较：eq、ne、lt、le、gt、ge
            例：
            $bookstore//book/@q > 10        
                如果 q 属性的值大于 10，上面的表达式的返回值为 true。
            $bookstore//book/@q gt 10   
                如果仅返回一个 q，且它的值大于 10，那么表达式返回 true。
                如果不止一个 q 被返回，则会发生错误。
    使用let语句
        let用于给变量赋值，如：
        let $xml:= 
          <a>
            <one>She drew a circle that shut me out</one>
            <two>Heretic rebel, a thing to flout</two>
          </a>
        return $xml//one/text()

        
XPath vs. XQuery
    XPath 最突出的局限性是没有提供任何办法转换结果集
    这两种语言都能够从 XML 文档或者 XML 文档存储库中选择数据
    XPath 还是 XQuery 完整不可分割的一部分
    XQuery 天生支持 XPath 并将其作为 XQuery 语法的一部分
    XPath 和 XQuery 都能实现一些相同的功能
    XPath 和 XQuery 都能实现一些相同的功能
    对于很多查询来说 XPath 非常合适
    如果需要表达更复杂的记录选择条件的表达式、
    转换结果集或者进行递归查询，则需要使用 XQuery
               

函数参考手册： https://www.w3school.com.cn/xpath/xpath_functions.asp