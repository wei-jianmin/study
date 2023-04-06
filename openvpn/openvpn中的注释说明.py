格式控制字符：
    \a ：之后紧跟的字符串为斜体，遇到空白结束
    \c ：之后紧跟的字符串比常规字符串更细小一些，遇到空白结束
    \link ... \linkend ： 中间的字符串为超链接
doxygen文档生成工具
    https://blog.csdn.net/qq_19528953/category_6362185.html
    doxygen还支持Markdown语法和HTML语法  
    特殊命令一般以\或者@开头 
    比如较为常用的@brief和@details代表一个注释的简单描述和详细描述，如：
    //! @brief 关于对话框
    //! @details 用来显示程序基本信息的对话框，单击“关于软件”时显示此对话框
    Doxygen的内部支持的markdown语法
        段落
            markdown本身的语法没有段落一说，因此需要分段的地方多空一行，就可以表示段落，例如：
            Here is text for one paragraph.
            We continue with more text in another paragraph.
        标题
            跟普通的markdown一样，标题可以在下面插入-或者=来实现二级标题和一级标题，当然其数量只要大于两个，多少都行，例如：
            This is a level 1 header
            ====================
            This is a level 2 header
            -------
            另外，标题也可以使用#来得到，使用的#的数目是多少就代表多少级标题，例如：
            # This is a level 1 header
            ### This is level 3 header #######
            sss
        块引用
            通过在代码注释的开头加入一个或多个>符号进行
            > This is a block quote
            > spanning multiple lines
        列表
            为了让注释显示列表，可以使用-, +,*，例如：
            - Item 1
              More text for this item.
            - Item 2
              + nested list item.
              + another nested item.
            - Item 3
            列表项目可以跨越多段，同时列表也支持嵌套，也可以使用数字列表，例如：
            1. First item.
            2. Second item.
        代码块
            代码块可以通过开头空四个空格来实现，例如：
            This a normal paragraph
                This is a code block
            We continue with a normal paragraph again.
            也可以使用三个或以上`符号或者三个\~符号然后后面跟着代码的语言，例如：
            ~~~~~~~~~~~~~~{C++}
            ~~~~~~~~~{.py}
        强调
            使用一个*或者_代表斜体强调，使用两个*或者_则代表加重强调，例如：
             single asterisks*
            _single underscores_
              double asterisks**
            __double underscores__
            注意：与标准markdown不同，doxygen无法处理内部的_和*因此向a_nice_identifier这样的句子就无法使得nice变成斜体强调。
            此外，_和*的强调开始必须是一个字母数字字符，否则(比如汉字)，必须在其开头加上一个空格、
            换行或者下面的字符<{([,:;。结尾也必须满足这个规则！同时，强调的跨度限制在单独的段落！
        代码段
            代码段需要包含在字符”`”之间，比如：
            Use the `printf()` function.
            为了在内部使用字面上撇符号，需要使用两个上撇符号，例如：
            To assign the output of command `ls` to `var` use ``var=`ls```.
        链接
            Doxygen支持内部链接和引用链接
            1 内部链接
                内部链接由一个链接文本(用方括号括起来)和一个统一资源定位符(用小括号括起来)和一个可选的字符串(链接提示符)组成，例如：
                [The link text](http://example.net/)
                [The link text](http://example.net/ "Link title")
                [The link text](/relative/path/to/index.html "Link title") 
                [The link text](somefile.html) 
                此外，还提供一种方法来访问文档中的内容，例如：
                [The link text](@ref MyClass)
            2 引用链接
                除了使用统一资源定位符，还可以自己定义一个链接，然后在文本内部引用，定义方式如下：
                [link name]: http://www.example.com "Optional title"
                定义好后可以向下面这样使用链接：
                [link text][link name]
                如果链接文本和名字相同，则可以简写成：
                [link name][] 甚至写成 [link name]
                注意：链接匹配大小写不敏感，例如：
        图片
            图片链接和链接一样，不同之处是开头多了一个!，例如：
            ![Caption text](@ref image.png)
            ![img def]
            [img def]: @ref image.png "Caption text"
        表格
            表格可以使用|符号产生，例如：
            First Header  | Second Header
            ------------- | -------------
            Content Cell  | Content Cell 
            Content Cell  | Content Cell 
            1
            2
            3
            4
            | Right | Center | Left  |
            | ----: | :----: | :---- |
            | 10    | 10     | 10    |
            | 1000  | 1000   | 1000  |
            1
            2
            3
            4
            以上就是Doxygen支持的markdown语法。
    Doxygen的特殊命令字
        Doxygen在进行注释的时候，有很多以@或者\开头后面加上一个特殊命令的字段，
        然后就可以在生成文档的时候有特殊的作用
        @addtogroup [(title)]
            使用@defgroup同样可以定义一个组，但是相比之下，多次使用相同<name>的@addtogroup命令并不会出现警告，而它是一个将命令中附带的title与文档进行合并的组。
            title是可选的，所以该命令可以使用@{和@}添加一定数量的实体到一个已存在的组里。例如：
            /*! \addtogroup mygrp
               *  Additional documentation for group 'mygrp'
               *  @{
               */
              /*!
               *  A function
               */
              void func1()
              {
              }
              /*! Another function */
              void func2()
              {
              }
              /*! @} */
        @callgraph
            当该命令放置到一个函数或方法的注释块中，且HAVE_DOT设为YES，doxygen将创建一个调用图。
        @callergraph
            当该命令放置到一个函数或方法的注释块中，且HAVE_DOT设为YES，doxygen将创建一个调用者图。
        @hidecallgraph
            当该命令放置到一个函数或方法的注释块中，且HAVE_DOT设为YES，doxygen将不创建一个调用图。
        @hidecallergraph
            当该命令放置到一个函数或方法的注释块中，且HAVE_DOT设为YES，doxygen将不创建一个调用者图。
        @category [] []
            只适用于Object-C：为一个名为<name>的类指定一个文档注释块，此命令参数应与@class相同
        @class [] []
            为一个名字为<name>类指定一个文档注释块，可选择指定的一个头文件和一个头名称。如果指定了一个头文件，在HTML文档中将包含一个指向次头文件的完全副本的链接。<header-name>参数可用于覆盖<header-file>之外的类文档中所使用链接名称，如果在默认包含路径中无法定位包含文件(如
            /* A dummy class */
            class Test
            {
            };
            /*! \class Test class.h "inc/class.h" 
             *  \brief This is a test class. 
             * 
             * Some details about the Test class. 
             */            
        @def
            用于定义一个#define的注释，例如：
            /*! \file define.h    
                \brief testing defines
                This is to test the documentation of defines.
            */
            /*! \def MAX(x,y) 
                Computes the maximum of \a x and \a y.
            */
            /*!    
                Computes the absolute value of its argument \a x.
            */
            #define ABS(x) (((x)>0)?(x):-(x))
            #define MAX(x,y) ((x)>(y)?(x):(y))
            #define MIN(x,y) ((x)>(y)?(y):(x))         
                /*!< Computes the minimum of \a x and \a y. */
        @defgroup (group title)
            为类、文件或命名空间的组，指定一个文档注释块，可以用于类、文件、命名空间和文档的其他类别进行归类，也可以将组作为其他组的成员，这样就可以创建一个组的层次。
        @dir []
            为一个目录指定一个文档注释块，path fragment参数应包含一个路径名和一个与项目中其他路径不一样的唯一一个全路径(The “path fragment” argument should include the directory name and enough of the path to be unique with respect to the other directories in the project.)
            enum
            为一个名字为<name>的枚举类型指定一个文档注释块，如果此枚举是类中的一个成员，且文档块处于类定义之外，类的作用于同样需要指定。如果一个注释块位于枚举声明之前，那么@enum注释可能被省略。
            注意：一个无名的枚举类型将不能被文档化，但一个无名的枚举值是可以使用的。
            例如：
            class Enum_Test
            {  
            public:    
                enum TEnum { Val1, Val2 };    
                /*! Another enum, with inline docs */    
                enum AnotherEnum     
                {       
                    V1, /*!< value 1 */      
                    V2  /*!< value 2 */    
                };
            };
            /*! \class Enum_Test 
             * The class description. 
             */
            /*! @enum Enum_Test::TEnum 
             * A description of the enum type. 
             */
            /*! @var Enum_Test::TEnum Enum_Test::Val1 
             * The description of the first enum value. 
            */
        @example
            为一个源码的例子指定一个文档注释块，<file-name>是源码文件名，在注释块包含的文档之后，将包含此文件的文本。所有的例子将被放入一个列表中，为了已文档化的成员和类，与文档之间的交叉引用，将对源码进行扫描，源文件或目录将在doxygen的配置文件中使用EXAMPLE_PATH标记指定。
            如果<file-name>也就是在EXAMPLE_PATH标记指定的例子文件名，并非是唯一的，你需要包含它的绝对路径，以消除它的二义性。
            如果例子中需要多个源文件，可以使用@include命令，例如：
            /** A Example_Test class. 
             *  More details about this class. 
             */
            class Example_Test
            {
            public:    
            /** An example member function.     
             *  More details about this function.    
             */    
             void example();
            };
            void Example_Test::example() {}
            /** @example example_test.cpp 
             * This is an example of how to use the Example_Test class. 
             * More details about this example. 
             */
            下面是例子文件example_test.cpp
            void main()
            { 
                Example_Test t; 
                t.example();
            }   
        @endinternal
            这个命令结束一个以@internal开头的文档块。只要当INTERNAL_DOCS设置为YES时在@internal和@endinternal之间的文档才可见。
        @extends
            当编程语言不支持这个特性时，比如C语言，就用这个命令手动指定一个继承关系，。
            在例子目录中manual.c文件将显示如何使用这个命令。
        @file []
            为一个名字为<name>的源文件或者头文件，指定一个文档注释块。如果文件名本身并不是唯一的，那么这个文件名可能包含(部分包含)了它的路径，如果该文件名被省略(如@file后留空)，那么包含@file命令的文档块将属于它已定位到的那个文件。
            要点：全局函数，变量，类型转换，枚举的文档只能包含在输出中，并且他们也已被文档化。
            例子：
            /** @file file.h 
             * A brief file description. 
             * A more elaborated file description. 
             */
            /** 
             * A global integer value. 
             * More details about this value. 
             */
            extern int globalValue;
            注意：上面的例子中JAVADOC_AUTOBRIEF已经设置为YES
        @fn (function declaration)
            为一个函数(全局函数或者类的成员函数)指定一个文档注释块，此命令只有在一个注释块没有放到函数声明前面或者后面时才需要。
            如果注释块放到了函数声明的前面或者后面，此命令可省略(为了避免重复)。
            警告：在此命名并非绝对需要时不要使用，否则将导致信息重复的错误。
            class Fn_Test
            { 
            public: 
                const char *member(char,int) throw(std::out_of_range);
            };
            const char *Fn_Test::member(char c,int n) throw(std::out_of_range) {}
            /*! @class Fn_Test 
             * @brief Fn_Test class. 
             * 
             * Details about Fn_Test. 
             */
            /*! @fn const char *Fn_Test::member(char c,int n)  
             *  @brief A member function.
             *  @param c a character.
             *  @param n an integer. 
             *  @exception std::out_of_range parameter is out of range. 
             *  @return a character pointer. 
             */   
        @headerfile []
            用于类，结构，联合的文档，同时这些文档都位于它们定义的前面。此命令的参数与@cmdclass命令的第二、三个参数相同。header-file名称会引用一个文件，它能被应用程序为获取类，结构，联合的定义而包含。<header-name>参数可用于覆盖<header-file>之外的类文档中所使用链接名称，如果在默认包含路径中无法定位包含文件(如
            @headerfile test.h "test.h"
            @headerfile test.h ""
            @headerfile "" 
            使用尖括号时你无需指定目标，如果你希望明确地指出，也可以使用一下方式：
            @headerfile test.h <test.h>
            @headerfile test.h <>
            @headerfile <>     
        @hideinitializer
            一个定义的缺省值和一个变量的初始化都将显示在文档中，除非它们的行数超过30。放置该命令在一个定义或者变量的注释块中，初始化将一直被隐藏。
        @idlexcept
            表明了该注释块包含的文档是为了一个名字为<name>的IDL异常
        @implements
            用于手动指定一个继承关系，当编程语言不支持这个特性时(如C语言)。
        @ingroup ( [ ])
            若该命令被放置到一个类，文件，命名空间的注释块中，它将添加一个<groupname>的组或者是组id。
        @interface [] []
            为一个名字为<name>的接口指定一个文档注释块，参数与@class命令相同
        @internal
            该命令开始一个仅仅为了内部使用的文档段，这个段落在注释块结尾处结束。你也可以通过使用命令@endinternal提前结束该内部文档段。
            如果该命令被放置的一个小节中(见@section中的例子)，那么命令后的所有子小节将被看成internal，只有与其在同一层级的新节才能重新可见。
        @mainpage [(title)]
            如果该命令被放置到一个注释块，此块将被用于定制HTML的索引页，或latex的首章。这个很常用，就是生成段落的开始页面的内容，我一开始研究了好久才在stackoverflow上面查到应该这样用！！
            title参数是可选的，并能替换掉doxygen生成的默认标题。如果你不需要任何标题，可以在命令后指定notitle。
            例如：
            /*! \mainpage My Personal Index Page
             *
             * \section intro_sec Introduction
             *
             * This is the introduction.
             *
             * \section install_sec Installation
             *
             * \subsection step1 Step 1: Opening the box
             *
             * etc...
             */   
        @memberof
            该命令使得类中的一个成员函数与@relates有相同的功能。 只有用这个命令函数才能被表述为一个类的真正成员。当编程语言不支持成员函数的概念时它将非常有用(如C语言)。
        @name [(header)]
            该命令将成员组中的头定义转变成一个注释块，注释块将位于一个包含成员组的//@{ ... //@} 块。
        @namespace
            为一个名字为<name>的命名空间指定一个文档注释块
        @nosubgrouping
            可放置在一个类文档中，用于在合并成员组时，避免doxygen放置一个公有，保护或者私有的子分组。
        @overload [(function declaration)]
            用于为一个重载成员函数生成后续的标准文本：这是一个未来便利而提供的重载函数，它不同于上述函数，只包含那些它接受的参数。
            如果在函数声明或者定义之前，无法定位重载成员函数的文档，能用可选参数来指定正确的函数。在生成的消息之后将会附带文档块内其他的文档。
            注意：你要承担起确认文档的重载成员正确与否的责任，在这种情况下为了防止文档重新排列，必须将SORT_MEMBER_DOCS设置为NO。
            注意：在一行注释中@overload命令无法工作
            例如：
            class Overload_Test 
            {
            public: 
                void drawRect(int,int,int,int); 
                void drawRect(const Rect &r);
            };
            void Overload_Test::drawRect(int x,int y,int w,int h) {}
            void Overload_Test::drawRect(const Rect &r) {}
            /*! @class Overload_Test 
             *  @brief A short description. 
             *
             *  More text. 
             */
            /*! @fn void Overload_Test::drawRect(int x,int y,int w,int h) 
             * This command draws a rectangle with a left upper corner at ( \a x , \a y ), 
             * width \a w and height \a h.  
             */
            /*!
             * @overload void Overload_Test::drawRect(const Rect &r) 
             */
        @package
            为一个名字为<name>的Java包指定一个文档注释块。
        @page (title)
            指定一个注释块，它包含了一个与特定的类，文件，成员非直接关联的文档块。HTML生成器将创建一个包含此文档的页面，而latex生成器将在’页文档’的章节中开始一个新的小节。
            例如：
            /*! @page page1 A documentation page  
                @tableofcontents  Leading text.  
                @section sec An example section  This page contains the subsections @ref subsection1 and @ref subsection2.  
                For more info see page @ref page2.  
                @subsection subsection1 The first subsection  Text.  
                @subsection subsection2 The second subsection  
                More text.
             */
            /*! @page page2 Another page  
                Even more info.
            */   
        @private
            指定注释块中的私有文档化成员，它只能被同一类的其他成员访问。
            注意：doxygen会自动确认面对对象语言中的成员保护层级，此命令用于不支持保护层级的概念的语言。(如C语言和PHP4)
            私有成员小节的开始处，有一种与C++中private:类似的标记法，使用@privatesection
        @privatesection
            开始一个私有成员的小节，与C++中private类似的标记法，指定注释块中的私有文档化成员，它只能被同一类的其他成员访问。
        @property (qualified property name)
            为一个属性(即可是全局也可是一个类成员)指定一个文档注释块，此命令等价于@var @fn
        @protected
            指定注释文档中的保护文档化成员，它只能被同一类的其他成员或派生类访问。
            注意：doxygen会自动确认面对对象语言中的成员保护层级，此命令用于不支持保护层级的概念的语言。(如C语言和PHP4)
            保护成员开始处，有一种与C++中protected:类似的标记法，使用@privatesection
        @protocol [] []
            为Object-C中名字为<name>的协议指定一个文档注释块，它的参数与@class相同。
        @public
            指定注释文档中的公有文档化成员，它只能其他类或函数访问。
            注意：doxygen会自动确认面对对象语言中的公有层级，此命令用于不支持公有层级的概念的语言。(如C语言和PHP4)
            公有成员开始处，有一种与C++中public:类似的标记法，使用@publicsection
        @pure
            指定注释文档中纯虚成员，它是抽象的没有被实施的成员。
            注意：此命令用于不支纯虚方法的概念的语言。(如C语言和PHP4)
        @relates
            用于名字为<name>非成员函数的文档，它可以放置在这个函数到类文档的“关联函数”小节内，该命令对于非友元函数与类之间建立强耦合是非常有用的。它无法用于文件，只能用于函数。
            /*!  
             * A String class. 
             */
            class String
            { 
                friend int strcmp(const String &,const String &);
            };
            /*! 
             * Compares two strings. 
             */
            int strcmp(const String &s1,const String &s2)
            {
            }
            /*! @relates String 
             * A string debug function. 
             */
            void stringDebug() 
            {
            }
        @related
            同@relates
        @relatesalso
            用于名字为<name>非成员函数的文档，它可以放置在这个函数到类文档的“关联函数”小节内，也可是远离它正常文档的位置。该命令对于非友元函数与类之间建立强耦合是非常有用的。只能用于函数。
        @showinitializer
            只显示定义的默认值和变量的初始化，如果它们的文本行数小于30，在变量或定义的注释块中放置这个命令，初始化过程将无条件被显示出来。
        @static
            指定注释文档中静态成员，它定义在类中，但不属于类的实例化，它属于整个类！
            注意：此命令用于不支静态方法的概念的语言。(如C语言和PHP4)
        @struct [] []
            为一个名字为<name>的结构体指定一个文档注释块，它与参数@class相同
        @typedef (typedef declaration)
            为一个类型转换指定一个文档注释块，它与参数@var @fn相同
        @union [] []
            为一个名字为<name>的联合体指定一个文档注释块，它与参数@class相同
        @var (variable declaration)
            为一个变量或者枚举值指定一个文档注释块，它与参数@typedef @fn相同
        @vhdlflow [(title for the flow chart)]
            这是一个硬件描述语言特定的命令，可以放在文档中产生一个逻辑过程的流程图。流程图的标题可以随意指定。
        @weakgroup [(title)]
            用法与@addtogroup相似，但当解决组定义冲突时，它将会有一个更低的优先级。
    特殊命令字之"小节指示命令"
        @attention { attention text }
            开始一个可输入需要处理信息的段落，次段落将会缩排，段落的文本不会指定一个内部结构，所有视觉增强的命令可以放置到该段落中，多个相邻的@attention命令将被组合到一个单独的段落中，当遇到一个空白行或者是其他的小节命令，那么@attention将终止。
            @author { list of authors }
            开始一个可输入一个或者多个作者名的段落，此段落将会缩排，段落的文本不会指定一个内部结构，所有视觉增强命令可以放置到该段落中，多个相邻的@author命令将被组合到一个单独的段落中，每个作者描述都将开启一个新行，另外一个 @author命令可能会有若干个作者，当遇到一个空白行或者是其他的小节命令，那么@author将终止。例如：
            /*!  
             *  @brief     Pretty nice class. 
             *  @details   This class is used to demonstrate a number of section commands. 
             *  @author    John Doe 
             *  @author    Jan Doe 
             *  @version   4.1a *  \date      1990-2011 
             *  @pre       First initialize the system.
             *  @bug       Not all memory is freed when deleting an object of this class. 
             *  @warning   Improper use can crash your application
             *  @copyright GNU Public License. 
             */
            class SomeNiceClass {};
        @authors { list of authors }
            同@author等价
        @brief { brief description }
            开始一个作为简明描述的段落，在文档页的起始部分可使用类和文件的简明描述的列表，可在细节描述的前端和成员声明处放置类成员和文件成员的简明描述。一个简明描述可能需要若干行(尽管建议它保持简明的风格)。当遇到一个空白行或者是其他的小节命令，那么简明描述将终止。如果出现多个@brief命令，那么它们将被组合在一起。查看命令@authhor的例子。等同于命令@short
        @bug { bug description }
            开始一个可报告一个或多个bug的段落，此段落将会缩排，段落的文本不会指定一个内部结构，所有视觉增强命令可以放置到该段落中，多个相邻的@bug命令将被组合到一个单独的段落中，每个bug都将开启一个新行，另外一个 @bug命令可能会有若干个bug，当遇到一个空白行或者是其他的小节命令，那么@bug将终止。查看命令@authhor的例子。
        @cond [(section-label)]
            开始一个带条件的小节，使用命令@endcond来终止该小节，通常在其他的注释块中可查找到@endcond。此对命令的目的是，(条件化)在处理中将一部分文件排除。
            小节将包含在命令@cond和@endcond之间，并将小节的标号加入到配置选项ENABLED_SECTIONS中，如果标号被忽略，该小节也将在处理中被无条件忽略。
            在注释块中的条件小节，可使用一个@if...@endif块。
            条件小节能被嵌套，在这种情况下，如果它和嵌套的小节都包含在其中，那么只有被嵌套的小节才会显示。例如：
            /** An interface */
            class Intf
            {
              public:
                /** A method */
                virtual void func() = 0;
                /// @cond TEST
                /** A method used for testing */
                virtual void test() = 0;
                /// @endcond
            };
            /// @cond DEV
            /*
             *  The implementation of the interface
             */
            class Implementation : public Intf
            {
              public:
                void func();
                /// @cond TEST
                void test();
                /// @endcond
                /// @cond
                /** This method is obsolete and does
                 *  not show up in the documentation.
                 */
                void obsolete();
                /// @endcond
            };
            /// @endcond
        @copyright { copyright description }
            开始描述一个实体的版权的段落，这个段落收到约束，这个段落的内容没有特殊的内部结构。查看命令@authhor的例子。
        @date { date description }
            开始一个可可输入一个或多个日期的段落，此段落将会缩排，段落的文本不会指定一个内部结构，所有视觉增强命令可以放置到该段落中，多个相邻的@date命令将被组合到一个单独的段落中，每个date都将开启一个新行，另外一个 @date命令可能会有若干个date，当遇到一个空白行或者是其他的小节命令，那么@date将终止。查看命令@authhor的例子。
        @deprecated { description }
            开始一个指示文档块是否弃用的段落，可用于描述替代方法，预定生命周期等
        @details { detailed description }
            如同@brief开始一个简明描述，@details将开始一个细节描述，你也可以开始一个新段落(加入空白行)，而无需加入命令@details。
        @else
            开始一个条件小节，如果前一个条件小节无效。前一个小节可使用命令@if,@ifnot,@elseif开始。
        @elseif (section-label)
            开始一个条件小节，如果前一个条件小节无效。当条件小节默认为无效时，你必须放置该命令的section-label到配置标记ENABLED_SECTIONS中使得命令@elseif有效。条件块可以嵌套，如果所有嵌套的条件都有效，那么也只有做内层的嵌套小节才会被读取。
        @endcond
            结束一个由@cond开始的条件小节。
        @endif
            结束一个由@if或@ifnot开始的条件小节，每个@if或@ifnot只能一一对应匹配之后的@endif。
        @exception { exception description }
            为一个名字为<exception-object>异常对象而开始一个描述，其次是此异常的描述。不会去检查是否存在这个异常对象。段落的文本不会指定一个内部结构，所有视觉增强的命令可以放置到该段落中，多个相邻的@exception命令将被组合到一个单独的段落中，每个参数的描述都将开启一个新行，当遇到一个空白行或者是其他的小节命令，那么@exception将终止。
            与@exception一样。
        @if (section-label)
            开始一个条件化的文档小节，并使用一个匹配的命令@endif结束。当条件小节默认为无效时，你必须放置该命令的section-label到配置标记ENABLED_SECTIONS中使得命令@if有效。条件块可以嵌套，如果所有嵌套的条件都有效，那么也只有做内层的嵌套小节才会被读取。例如：
            /*! Unconditionally shown documentation.
               *  \if Cond1
               *    Only included if Cond1 is set.
               *  \endif
               *  \if Cond2
               *    Only included if Cond2 is set.
               *    \if Cond3
               *      Only included if Cond2 and Cond3 are set.
               *    \endif
               *    More text.
               *  \endif
               *  Unconditional text.
               */ 
            如果你在alias中使用了条件命令，如果在两种语言中文档化一个类，你可以这样使用：
            /*! \english
             *  This is English.
             *  \endenglish
             *  \dutch
             *  Dit is Nederlands.
             *  \enddutch
             */
            class Example
            {
            }; 
            一下是配置文件中的alias：
            ALIASES  = "english=\if english" \
                       "endenglish=\endif" \
                       "dutch=\if dutch" \
                       "enddutch=\endif" 
            那么ENABLED_SECTIONS即可有效english也可有效dutch
        @ifnot (section-label)
            开始一个条件化的文档小节，并使用一个匹配的命令@endif结束。当条件小节默认为有效时，你必须放置该命令的section-label到配置标记ENABLED_SECTIONS中使得命令@ifnot无效。
        @invariant { description of invariant }
            开始一个可描述不变式的段落，此段落将会缩排，段落的文本不会指定一个内部结构，所有视觉增强的命令可以放置到该段落中，多个相邻的@invariant命令将被组合到一个单独的段落中，每个invariant描述都将开启一个新行，另外一个@invariant命令可能会有若干个不变式，当遇到一个空白行或者是其他的小节命令，那么@exception将终止。
        @note { text }
            开始一个输入提示的段落，此段落将会缩排，段落的文本不会指定一个内部结构，所有视觉增强的命令可以放置到该段落中，多个相邻的@note命令将被组合到一个单独的段落中，每个note描述都将开启一个新行，另外一个@note命令可能会有若干个提示，当遇到一个空白行或者是其他的小节命令，那么@note将终止。查看@par命令的例子。
        @par [(paragraph title)] { paragraph }
            如果一个段落标题已经给定，此命令将开始一个用户自定义的段头。段头将会占用一行，命令后的段头将会缩排。
            如果段落标题未给出，此命令将开始一个新段落，也可插入其他段落命令(如@param或@warning)来终止该命令。
            段落的文本不会指定一个内部结构，所有视觉增强的命令可以放置到该段落中，当遇到一个空白行或者是其他的小节命令，那么@par将终止。例如：
            /*! @class Par_Test 
             * Normal text. 
             * 
             * @par User defined paragraph: 
             * Contents of the paragraph. 
             * 
             * @par 
             * New paragraph under the same heading. 
             *
             * @note 
             * This note consists of two paragraphs. 
             * This is the first paragraph. 
             * 
             * @par 
             * And this is the second paragraph. 
             *
             * More normal text. 
             */ 
            class Par_Test {}; 
        @param [(dir)] { parameter description }
            为一个名字为<parameter-name>函数参数开始一个参数描述，将会去检查是否存在。如果在函数声明或定义中，该参数(或其他参数)的文档丢失或未出现，将会给出一个警告。
            @param命令有一个可选属性，能指定参数的方向属性，可为into或out，这有一个例子：
            /*! * Copies bytes from a source memory area to a destination memory area, 
             * where both areas may not overlap. 
             * @param[out] dest The memory area to copy to.
             * @param[in]  src  The memory area to copy from.
             * @param[in]  n    The number of bytes to copy 
             */void 
            memcpy(void *dest, const void *src, size_t n); 
            如果参数既可以输入也可输出，则使用[in,out]指定方向属性，段落的文本不会指定一个内部结构，所有视觉增强的命令可以放置到该段落中，多个相邻的@param命令将被组合到一个单独的段落中，每个参数描述都将开启一个新行，当遇到一个空白行或者是其他的小节命令，那么@param将终止。
        @parblock
            不像那些评论单一段落的参数( @par, @param 和 @warning)，@parblock可以作为一个跨越多行段落描述的命令，并且以endparblock结束。例如：
            /** Example of a param command with a description consisting of two paragraphs
             *  \param p 
             *  \parblock
             *  First paragraph of the param description.
             *
             *  Second paragraph of the param description.
             *  \endparblock
             *  Rest of the comment block continues.
             */ 
        @endparblock
            结束一个以@parblock开头的段落块。
        @tparam { description }
            为一个名字为<template-parameter-name>类或函数模板参数开始一个模板参数描述，等同于@cmdparam
        @post { description of the postcondition }
            开始一个可描述的后置条件的段落，此段落将会缩排，段落的文本不会指定一个内部结构，所有视觉增强的命令可以放置到该段落中，多个相邻的@post命令将被组合到一个单独的段落中，每个后置描述都将开启一个新行，另外一个@post命令可能会有若干个提示，当遇到一个空白行或者是其他的小节命令，那么@post将终止。
        @pre { description of the precondition }
            开始一个可描述的前置条件的段落，此段落将会缩排，段落的文本不会指定一个内部结构，所有视觉增强的命令可以放置到该段落中，多个相邻的@pre命令将被组合到一个单独的段落中，每个前置条件描述都将开启一个新行，另外一个@pre命令可能会有若干个提示，当遇到一个空白行或者是其他的小节命令，那么@pre将终止。
        @remark { remark text }
            开始一个可输入一个或多个备注的段落，此段落将会缩排，段落的文本不会指定一个内部结构，所有视觉增强的命令可以放置到该段落中，多个相邻的@remark命令将被组合到一个单独的段落中，每个备注都将开启一个新行，另外一个@remark命令可能会有若干个提示，当遇到一个空白行或者是其他的小节命令，那么@remark将终止。
        @remarks { remark text }
            同@remark。
        @result { description of the result value }
            同@return。
        @return { description of the return value }
            开始一个可输入一个或多个备注的段落，此段落将会缩排，段落的文本不会指定一个内部结构，所有视觉增强的命令可以放置到该段落中，当遇到一个空白行或者是其他的小节命令，那么@remark将终止。参考@fn命令中的例子。
        @returns { description of the return value }
            同@return。
        @retval { description }
            为一个名字为<return value>函数开始一个返回值的描述，段落的文本不会指定一个内部结构，所有视觉增强的命令可以放置到该段落中，多个相邻的@retval命令将被组合到一个单独的段落中，每个备注都将开启一个新行，当遇到一个空白行或者是其他的小节命令，那么@retval将终止。
        @sa { references }
            为指定的类、函数、方法、变量、文件、URL的一个或多个交叉引用开始一个段落，使用::或者#作为类和它的一个成员的引用连接符来组合上述两个名称。在方法名称之后包含一个带括号的参数类型列表，用于若干个重载方法或者构造器的选择。
        @see { references }
            为了兼容JavaDoc，等同于@sa。
        @short { short description }
            同@brief。
        @since { text }
            用于指定一个有效的版本和时间，@since之后的段落不会指定一个内部结构，所有视觉增强的命令可以放置到该段落中，当遇到一个空白行或者是其他的小节命令，那么@since将终止。
        @test { paragraph describing a test case }
            开始一个可描述的测试用例的段落，此描述会添加这个测试用例到一个单独的测试列表中，而这两种描述将可交叉引用。在测试列表中的每一个测试用例的前端，都还有一个指明它出处的头。
        @throw { exception description }
            同@exception。
        @throws { exception description }
            同@throw。
        @todo { paragraph describing what is to be done }
            开始一个可描述的todo条目的段落，此描述会添加这个条目到一个单独的todo列表中，而这两种描述将可交叉引用。在测试列表中的每一个测试用例的前端，都还有一个指明它出处的头。
        @version { version number }
            开始一个可可输入一个或多个版本字符串的段落，此段落将会缩排，段落的文本不会指定一个内部结构，所有视觉增强命令可以放置到该段落中，多个相邻的@version命令将被组合到一个单独的段落中，每个版本描述将开启一个新行，另外一个 @version命令可能会有若干个版本字符串，当遇到一个空白行或者是其他的小节命令，那么@version将终止。查看命令@authhor的例子。
        @warning { warning message }
            开始一个可可输入一个或多个警告信息的段落，此段落将会缩排，段落的文本不会指定一个内部结构，所有视觉增强命令可以放置到该段落中，多个相邻的@warning命令将被组合到一个单独的段落中，每个版本描述将开启一个新行，另外一个 @warning命令可能会有若干个警告，当遇到一个空白行或者是其他的小节命令，那么@warning将终止。查看命令@authhor的例子。
        @xrefitem “(heading)” “(list title)” { text }
            此命令是一个类似于@todo,@bug的集合，用于创建用户自定义文本小节，它会在连接点与关联页面之间自动生成交叉引用，并且能搜集关联页面中的所有相同类型的小节。第一个参数是一个表述小节类型的唯一标识，第二个参数是一个加了引号的字符串，它用于表述第四个参数放置文本下的小节头，为包含同一个标识的所有条目相关页面，第三个参数将作为一个标题来使用，一些已经预定义的标识：todo,test,bug,deprecated。
            想想如果使用@xrefitem命令和它运行后的结果，如果只考虑todo列表，它看上去更像是一个alias：
            \xrefitem todo "Todo" "Todo List"
            为每个小节都将重复该命令的前三个参数，这使得它非常易错，该命令也可用于合并配置文件中的ALIAES选项，如果定义一个新命令@reminder，可添加一下内容到配置文件：
            ALIASES += "reminder=\xrefitem reminders \"Reminder\" \"Reminders\""
            注意：命令中第二和第三参数使用转义引号。
            万一参数”(heading)”是一个空字符串则没有heading生成。当和@page命令联合使用时这非常有用。例如：
            /** @page my_errors My Errors
             *  @brief Errors page
             *
             *  Errors page contents.
             */
            /** \error ERROR 101: in case a file can not be opened.
                Check about file system read/write access. */
            #define MY_ERR_CANNOT_OPEN_FILE                   101
            /** \error ERROR 102: in case a file can not be closed.
                Check about file system read/write access. */
            #define MY_ERR_CANNOT_CLOSE_FILE                  102 
            里面的@error定义为：
            ALIASES += "error=\xrefitem my_errors \"\" \"\""
    特殊命令字之"创建连接命令" 
        @addindex (text)
            添加1文本到latex索引中
        @anchor
            放置一个不可见的已命名的anchor(固定点)到文档中，且能使用@ref命令进行引用。
            注意：anchor目前只能放置在一个标记成页面(使用@page)或主页(使用@mainpage)的注释块中
        @cite
            增加一个书籍参考到一个文本和数目参考列表里。
        @endlink
            终止一个命令@link开始的连接
        @link
            连接是由doxygen自动生成的，且一直有一个指向的对象名作为连接文本。该命令可以用于创建一个对象(一个文件，类或者成员)的连接，并且用户可指定对象的连接文本。此命令可以被@endlink终止，所有在其之间的文本都将作为指向@link第一个参数<link-object>的连接文本。
        @ref [“(text)”]
            创建一个已命名小节，子小节，页面或anchor(固定点)的引用，在HTML文档中该命令将生成一个指向小节的连接。在一个小节或者子小节中将使用小节标题作为连接文本，在anchor(固定点)中可使用引号间的text或者当text忽略时使用<name>作为连接文本，而在latex文档中，如果<name>引用的是一个anchor(固定点)，该命令将小节生成一个编号或者是使用一个页面编号后的文本。
        @refitem
            就像@ref命令，这个命令创建一个名字小节的引用，但是这个在一个以@secreflist开始，@endsecreflist结束的列表中。
        @secreflist
            开始一个标题列表，用@refitem创建，每一个都连接到对应的名字小节
        @endsecreflist
            开始以@secreflist开头的标题列表。
        @subpage [“(text)”]
            创建若干页面的一个层次，相同结构也可以使用@defgroup,@ingroup命令，但在页面中使用@subpage命令更方便。主页@mainpage通常是层次的根节点。
            该命令类似于@ref，它用于创建一个到<name>页面标签的引用，并且可选择第二个参数指定的text作为连接文本。
            它不同于@ref命令之处在于，它只能工作在页面中，在页面中创建一个父子关联，并且子页面使用<name>进行标识。
            例如：
            /*! @mainpage A simple manual
            Some general info.
            This manual is divided in the following sections:
            - @subpage intro
            - @subpage advanced "Advanced usage"
            */
            //-----------------------------------------------------------
            /*! @page intro Introduction
            This page introduces the user to the topic.
            Now you can proceed to the @ref advanced "advanced section".
            */
            //-----------------------------------------------------------
            /*! @page advanced Advanced Usage
            This page is for advanced users.
            Make sure you have first read @ref intro "the introduction". 
        @tableofcontents
            在页面顶端创建一个内容表格，列出页面中所有小节和子小节
            警告：该命令只能工作在一个相关页文档块的小节中，而无法工作于其他文档块中而且仅仅在HTML输出中有效。
        @section (section title)
            创建一个名为<section-name>的小节，小节的标题可使用命令的第二参数指定。
            警告：该命令只能工作在一个相关页文档块的小节中，而无法工作于其他文档块中。
        @subsection (subsection title)
            创建一个名为<section-name>的子小节，小节的标题可使用命令的第二参数指定。
            警告：该命令只能工作在一个相关页文档块的小节中，而无法工作于其他文档块中。
        @subsubsection (subsubsection title)
            创建一个名为<section-name>的子小节的小节，小节的标题可使用命令的第二参数指定。
            警告：该命令只能工作在一个相关页文档块的小节中，而无法工作于其他文档块中。
        @paragraph (paragraph title)
            创建一个名为<paragraph-name>的段落，它的标题可使用命令的第二参数指定。
            警告：该命令只能工作在一个相关页文档块的小节中，而无法工作于其他文档块中 
    特殊命令字之"用于显示例子的命令"
        @dontinclude
            用于解析一个源文件，且不论是否被文档完整包含(如同@include命令所做的)，如果你希望将源文件分割成最小的块，并在这些块中间添加文档，那此命令会非常有用。源文件或是目录可使用配置文件中的EXAMPLE_PATH标记来指定。
            在解析包含@dotinclude命令的注释块期间，代码段中类和成员的声明和定义将被’记忆’。
            对于单行可使用源文件的单行描述，而显示一行或多行例子可使用@line,@skip,@skipline,@until命令，为了这些命令将会使用一个内部指针，@dontinclude可设定这个指针指向例子的第一行。
            /*! A test class. */
            class Include_Test
            {
            public: 
                /// a member function
                void example();
            };
            /*! @page example 
             *  @dontinclude include_test.cpp 
             *  Our main function starts like this: 
             *  @skip main 
             *  @until { 
             *  First we create an object @c t of the Include_Test class. 
             *  @skipline Include_Test 
             *  Then we call the example member function  
             *  \line example
             *  After that our little test routine ends.
             *  \line }
             */ 
            例子文件example_test.cpp如下：
            void main()
            {
                Example_Test t;  
                t.example();
            } 
        @include
            用于包含一个源文件作为一个代码块，此命令带有一个包含文件名的参数，源文件或是目录可使用配置文件中的EXAMPLE_PATH标记来指定。
            如果在EXAMPLE_PATH标记中指定的<file-name>此例子文件的设定，并非是唯一的，就必须包含<file-name>的绝对路径以消除二义性。
            使用@include命令等价于在文档中插入文件，并使用@code,@endcode命令限定文件的范围。
        @include命令的主要目的是，避免在包含多个源文件和头文件的例子块中出现代码重复。
            源文件的单行描述，可使用组合了@line,@skip,@skipline,@until命令的@dotinclude命令。
            注意：doxygen特殊命令是无法在代码块中工作的，但允许在代码块中放置嵌套的C风格注释。也可查看@example,@dontinclude,@verbatim命令。
        @includelineno
            具备与@include命令相同的工作模式，但可添加行号到包含文件中。
        @line ( pattern )
            用于搜索行，除非该命令找到一个非空行，否则将搜索至最后用@include或@dontinclude包含的例子，如果该行包含指定的模式，将写入输出。
            在例子中会使用一个跟踪当前行的内部指针，将找到非空行作为起始行，并设定内部指针。(如果未找到符合要求的行，指针也将指向例子的末端)
        @skip ( pattern )
            用于搜索行，除非该命令找到一个包含指定模式的行否则将搜索至最后用@include或@dontinclude包含的例子。
            在例子中会使用一个跟踪当前行的内部指针，将找到那行作为起始行，并设定内部指针。(如果未找到符合要求的模式，指针也将指向例子的末端)
        @skipline ( pattern )
            用于搜索行，除非该命令找到一个包含指定模式的行，否则将搜索至最后用@include或@dontinclude包含的例子,并将此行写入输出。
            在例子中会使用一个跟踪当前行的内部指针，将写入输出的哪行作为起始行，并设定内部指针。(如果未找到符合要求的模式，指针也将指向例子的末端)
        @snippet ( block_id )
            不像@include命令可以用来包含一个完整的文件作为源代码，这个命令中用来标记一个段落作为原文件。如果这是用作<file-name>当前文件作为文件的片段。
            例如,下面的命令在文档中,引用一个片段文件的例子。cpp驻留在一个子目录应由EXAMPLE_PATH指出。
            \snippet snippets/example.cpp Adding a resource
            文件名后的文本片段的惟一标识符。这是用来划定相关片段文件中引用的代码如以下示例所示,对应于上述\片段命令:
                QImage image(64, 64, QImage::Format_RGB32);    
                image.fill(qRgb(255, 160, 128));//! [Adding a resource]    
                document->addResource(QTextDocument::ImageResource,        
                QUrl("mydata://image.png"), QVariant(image));//! [Adding a resource]    ...
            注意,包含块的线条标记不会被包括,所以输出将会是:
            document->addResource(QTextDocument::ImageResource,    QUrl("mydata://image.png"), QVariant(image));
            还要注意(block_id)标记应该完全在源文件中出现两次。　　　　
            另一种方法参见\ dontinclude包括碎片的源文件不需要标记。
        @until ( pattern )
            将最后包含@include或@dontinclude的例子中的所有行写入输出，除非它找到一个包含指定模式的行，而只写入包含指定模式的一行。
            在例子中会使用一个跟踪当前行的内部指针，将写入输出的那行作为起始行，并设定内部指针。(如果未找到符合要求的模式，指针也将指向例子的末端)
        @verbinclude
            在文档中完整包含名为<file-name>文件，此命令等价于在文档中放置@verbatim,@endverbatim命令限定<file-name>文件。
        @htmlinclude
            在HTML文档中完整包含名为<file-name>文件，此命令等价于在文档中放置@htmlonly
        @latexinclude
            　这个命令包括文件<文件名>文档。命令相当于粘贴文件文档和放置@ latexonly和@endlatexonly命令。　　　
            　文件或目录,doxygen应该寻找可以指定使用doxygen EXAMPLE_PATH标签的配置文件。
    特殊命令字之"用于视觉增强的命令"
        @a
            使用一种指定的字体显示<word>参数，在运行的文本使用此命令建立与成员参数的引用。例子：
            ... the \a x and \a y coordinates are used to ...
            一下是显示结果：
            … the x and y coordinates are used to …
        @arg { item-description }
            除非该命令后遇到一个空白行或是其他@arg命令，此命令都会有一个参数。它可用于生成一个简单的，无嵌套的参数列表。每一个参数都使用一个@arg命令开始。例如：
              @arg @c AlignLeft left alignment.
              @arg @c AlignCenter center alignment.
              @arg @c AlignRight right alignment
              No other types of alignment are supported.
            结果将显示：
            AlignLeft left alignment.
            AlignCenter center alignment.
            AlignRight right alignment
            No other types of alignment are supported.
            注意：使用HTML命令可创建嵌套列表。
            等价于@li
        @b
            使用一个黑体显示<word>参数，等价于<b>word</b>。也可放置多个字，如<b>multiple words</b>。
        @c
            使用一个打印字体显示<word>参数，使用该命令引用Word的编码，等价于<tt>word</tt>
            例子：
            ... This function returns @c void and not @c int ...
            以下是结果文本：
            … This function returns void and not int …
        @code [ ‘{‘’}’]
            开始一个代码块，一个代码块的处理不同于普通文本，它默认被解析成C/C++代码，文档化的类和成员的名称将自动被指向文档的连接代替。
        @copydoc
            从指定的<link-object>对象中复制一个文档块，并使用本地命令进行解析。为避免文档块重复的情况，该命令将非常有用，或是用于扩展一个派生成员的文档。
            连接对象可指向一个成员(可从属一个类，文件或组)，一个类，一个命名空间，一个组，一个页面或是一个文件(按顺序检查)，注意，如果此对象指向一个成员(从属于函数，变量，类型转换等)，为了使其工作，包含它的复合体(类，文件或组)将被文档化。
            为了复制类成员的文档，可在文档中放置一下内容：
            /*! @copydoc MyClass::myfunction()
             *  More documentation.
            如果该成员被重载，可指定相同的参数类型(与成员名之间不留空格)，如下：
            //! @copydoc MyClass::myfunction(type1,type2)
            如果在文档块中查到请求该成员的文本，则需要有能匹配的名称。
            Copydoc命令可用于递归，但递归的每一层级都会暂时中断并记录，如同出现一个错误。
            - @copybrief
        @copydoc命令的简易工作方式，只复制简明描述，而不处理细节描述
        @copydetails
        @copydoc命令的简易工作方式，只复制简明描述，而不处理细节描述
        @docbookonly
            开始一个文本块，这个文本块将仅仅被逐字的包含在生成的docbook文档中。这个文本块以@enddocbookonly命令结束
            @dot [“caption”] [=]
            开始一个可包含dot图形描述的文本段，此文本段可用@enddot结束。Doxygen传递文本给dot，并在输出的结果图片(一级图片映射)中包含这些文本。图中的节点是可单击的，且能连接URL。可使用URL中的@ref命令方便的连接doxygen中的条目，例如：
            /*! class B */
            class B {};
            /*! class C */
            class C {};
            /*! @mainpage   
             *  Class relations expressed via an inline dot graph: 
             *  @dot
             *  digraph example { 
             *      node [shape=record, fontname=Helvetica, fontsize=10];
             *      b [ label="class B" URL="@ref B"];
             *      c [ label="class C" URL="@ref C"]; 
             *      b -> c [ arrowhead="open", style="dashed" ]; 
             *  }
             *  @enddot 
             *  Note that the classes in the above graph are clickable
             *  (in the HTML output). 
         @msc [“caption”] [=]
            开始一个可包含消息序列图描述的文本段，查看这个网址的一些例子。此文本段可用命令@endmsc结束。
            注意：在msc{…}块中的该文本段只包含消息序列图的一部分。你需要安装mscgen工具，才能使用此命令。例如：
            /** Sender class. Can be used to send a command to the server. 
             *  The receiver will acknowledge the command by calling Ack(). 
             *  @msc 
             *    Sender,Receiver;
             *    Sender->Receiver [label="Command()", URL="@ref Receiver::Command()"];  *    Sender<-Receiver [label="Ack()", URL="@ref Ack()", ID="1"]; 
             *  @endmsc 
             */
            class Sender
            {  public:    
                /** Acknowledgment from server */   
                void Ack(bool ok);
            };
            /** Receiver class. Can be used to receive and execute commands.
             *  After execution of a command, the receiver will send an acknowledgment 
             *  \msc 
             *    Receiver,Sender; 
             *    Receiver<-Sender [label="Command()", URL="\ref Command()"]; 
             *    Receiver->Sender [label="Ack()", URL="\ref Sender::Ack()", ID="1"];
             *  \endmsc 
             */
            class Receiver
            {  
                public:    
                /** Executable a command on the server */   
                void Command(int commandId);
            };
        @startuml [{file}] [“caption”] [=]
            开始一个可包含一个PlanUML图的有效描述的文本段，查看这个网址的一些例子。此文本段可用命令@enduml结束。
            注意：你需要安装Java和PlantUML’s jar文件才能使用此命令。jar文件的名字要使用PLANTUML_JAR_PATH指明。
            第一个参数是可选的并且作为运行doxygen前的一个预处理步骤，为了和运行PlantUML兼容。你也可以在@startuml之后的花括号内增加图像的文件的名字，例如：
              @startuml{myimage.png} "Image Caption" width=5cm
              Alice -> Bob : Hello
              @enduml
              ```
            当指明图像的名字时，doxygen将会产生一个以那个名字命名的图片。如果没有名字，doxygen将会自动选择一个名字。
            第二个参数是可选的并且可以用来指明在图片下面的标题。这个参数必须在两个引号之接指明即使它不包含任何空格。引号在标题显示前会被去掉。
            第三个参数同样可选可以用来指明图片的高度和宽度。
            下面是一个使用了`@startuml`命令的例子：
            ```C++
            /** Sender class. Can be used to send a command to the server. 
             *  The receiver will acknowledge the command by calling Ack(). 
             *  @startuml
             *    Sender->Receiver  : Command() 
             *    Sender<--Receiver : Ack() 
             *  @enduml
             */
            class Sender
            {  
            public:    
                /** Acknowledgment from server */   
                void Ack(bool ok);
            };
            /** Receiver class. Can be used to receive and execute commands. 
             *  After execution of a command, the receiver will send an acknowledgment 
             *  @startuml 
             *    Receiver<-Sender  : Command() 
             *    Receiver-->Sender : Ack() 
             *  @enduml 
             */
            class Receiver
            {
            public:  
                /** Executable a command on the server */    
                void Command(int commandId);
            };
            <div class="se-preview-section-delimiter"></div>
        @dotfile [“caption”] [=]
            在文档中插入一副dot生成的<file>图片。
            第一个参数指定了图片的名称。Doxygen将会在DOTFILE_DIRS标记后指定的路径中查找文件名。如果找到将作为dot工具的输入文件。结果图片将放置到正确的输入目录中。如果dot文件名中包含空格，需要使用引号进行修饰。
            第二个参数可选，用于指定图片中显示的标题，即使它没有包含空格也必须放置到引号之前，在标题显示之前引号会被删除。
        @mscfile [“caption”] [=]
            在文档中插入一副mscgen生成的<file>图片。查看这个网址的一些例子。
            第一个参数指明了图片的文件名。doxygen将会寻找你指明在MSCFILE_DIRS标签后面的路径或文件。如果msc文件被找到，它将被用来作为mscgen工具的输入文件。结果图片将被放到正确的输出目录。如果msc文件名包含空格，你将必须在其周围加上符号(“…”)。
            第二个参数是可选的并且可以用来指明在图片下面的标题。这个参数必须在两个引号之接指明即使它不包含任何空格。引号在标题显示前会被去掉。
            第三个参数同样可选可以用来指明图片的高度和宽度。
        @diafile [“caption”] [=]
            在文档中插入一副dia生成的<file>图片。
            第一个参数指明了图片的文件名。doxygen将会寻找你指明在DIAFILE_DIRS标签后面的路径或文件。如果msc文件被找到，它将被用来作为mscgen工具的输入文件。结果图片将被放到正确的输出目录。如果msc文件名包含空格，你将必须在其周围加上符号(“…”)。
            第二个参数是可选的并且可以用来指明在图片下面的标题。这个参数必须在两个引号之接指明即使它不包含任何空格。引号在标题显示前会被去掉。
            第三个参数同样可选可以用来指明图片的高度和宽度。
        @e
            使用斜体显示<word>，用于突出word。
            等价于@em，为了突出多个字可用<em>multiplewords</em>
        @em
            使用斜体显示<word>，用于突出word。
            等价于@e
        @endcode
            结束一个代码块
            也可查看@code命令
        @enddocbookonly
            结束一个@docbookonly开始的块
        @enddot
            结束一个@dot开始的块
        @endmsc
            结束一个@msc开始的块
        @enduml
            结束一个@enduml开始的块
        @endhtmlonly
            结束一个@htmlonly开始的块
        @endlatexonly
            结束一个@latexonly开始的块
        @endmanonly
            结束一个@manonly开始的块
        @endrtfonly
            结束一个@msc开始的块
        @endverbatim
            结束一个@verbatim开始的块
        @endxmlonly
            结束一个@xmlonly开始的块
        @f$
            标记公式文本的开始和结束
        @f[
            在单独的一行中显示加长公式的起始标记
        @f]
            在单独的一行中显示加长公式的结束标记
        @f{environment}{
            在一个指定环境中显示公式的起始标记
        @f}
            在一个指定环境中显示公式的结束标记
        @htmlonly [“[block]”]
            开始一个文本块，只能被完整包含在生成的HTML文档中。可用@endhtmlonly命令结束。
            此命令可为doxygen包含复杂的HTML代码(如applets,java-scripts,html标记)，也可用@latexonly,@endlatexonly命令提供一份合适的latex文档。
            注意：在一个只包含HTML的块中可以解析环境变量(如$(HOME))
        @image [“caption”] [=]
            在文档中插入一张图片，图片的格式可指定，如果你希望插入多种格式的图片，那么你必须为每种格式设定一次该命令。
            第一个参数指定了输出格式，目前只支持html,latex,docbook 和 rtf.
            第二个参数指定图片文件名，doxygen将在IMAGE_PATH标记后指定的路径中查找文件名。如果找到将复制到正确的输出目录中。如果图片文件名中包含空格将使用引号修饰。也可以指定一个URL来替代文件名，那么doxygen将不会复制这个图片，而会检查图片是否存在。
            第三个参数可选，用于指定图片中显示的标题。即使它没有包含空格也必须放置到引号之中，在标题显示之前引号会被删除。
            第四个参数也可选，用于指定图片的高度和宽度。且只对latex输出有效(即format=latex), sizeindication既可用于图片的宽度也可用于图片的高度，该尺寸可在latex中指定一个有效的尺寸(例如10cm或6英寸或是一个符号宽度@textwidth)。
            例如：
              /*! Here is a snapshot of my new application:
               *  \image html application.jpg
               *  \image latex application.eps "My application" width=10cm
               */
            <div class="se-preview-section-delimiter"></div>
            以下是一个可查找的与配置文件关联的例子：
            IMAGE_PATH = my_image_dir
            警告：HTML中所支持的图片格式受限于浏览器的兼容性。Latex中的图片格式必须是eps(Encapsulated PostScript)。
            Doxygen无法检查图片格式是否正确，所以你需要自习确认。
        @latexonly
            开始一个文本块，只能被完整包含在生成的latex文档中。可用@endlatexonly命令结束。
            此命令可为doxygen包含复杂的HTML代码(如图片，公式，特殊字符)，也可用@htmlonly,@endhtmlonly命令提供一份合适的latex文档。
            注意：在一个只包含latex的块中可以解析环境变量(如$(HOME))
        @manonly
            开始一个文本块，只能被完整包含在生成的MAN文档中。可用@endmanonly命令结束。
            此命令可为MAN页面中直接包含groff代码，也可用@htmlonly,@endhtmlonly命令和@latexonly,@endlatexonly命令提供一份合适的HTML和latex文档。
        @li { item-description }
            除非该命令后遇到一个空白行或是其他@li命令，此命令都会有一个参数。它可用于生成一个简单的，无嵌套的参数列表。每一个参数都使用一个@li命令开始。
            注意：使用HTML命令可创建嵌套列表
            等价于@arg
        @n
            加入一条新行，等价于<br>，可被打印函数使用。
        @p
            使用打印字体显示<word>参数，使用该命令可在运行的文本中引用成员函数。
            等价于@c
        @rtfonly
            开始一个文本块，只能被完整包含在生成的RTF文档中。可用@endrtfonly命令结束。
            此命令可为doxygen包含复杂的RFT代码。
            注意：在一个只包含RFT的块中可以解析环境变量(如$(HOME))
        @verbatim
            开始一个能被HTML和latex文档完整包含的文本块，可用@endverbatim命令结束，在一个完整块中不允许任何注释。
            警告：确认每个@verbatim都对应有一个@endverbatim，否则解析器将会出现冲突。
        @xmlonly
            开始一个能被XML完整包含的文本块，可用@endxmlonly命令结束。
            该命令可用于自定义的XML标记。
        @\
            写入一个反斜杠到HTML和latex的输出中，因为doxygen可用此斜杠作为命令之间的分隔符，所以大多数情况下它将被忽略。
            @@
            写入一个at符号到HTML和latex的输出中，因为doxygen可用此符号作为JavaDoc命令之间的分隔符，所以大多数情况下它将被忽略。
            @~[LanguageId]
            使能/取消一个指定的语言过滤器，用于放置不同语言的文档到一个注释块中，使用OUTPUT_LANGUAGE标记过滤掉未指定的语言。使用~[LanguageId]可有效一种输出的指定语言，@~则表示在输出中所有语言均有效。(这也是默认设置的)，例子：
            /*! \~english This is English \~dutch Dit is Nederlands \~german Dies ist
                Deutsch. \~ output for all languages.
             */
        @&
            写入一个&符号到输出中，因为此符号在HTML中有特殊函数，所以大多数情况下它将被忽略。
        @$
            写入一个$符号到输出中，因为此符号可用于扩展环境变量，所以大多数情况下它将被忽略。
        @#
            写入一个#符号到输出中，因为此符号可用于引用文档化的主体，所以大多数情况下它将被忽略。
        @<
            写入一个<符号到输出中，因为此符号在HTML中有特殊函数，所以大多数情况下它将被忽略。
        @>
            写入一个>符号到输出中，因为此符号在HTML中有特殊函数，所以大多数情况下它将被忽略。
        @%
            写入一个%符号到输出中，因为此符号可防止自动连接到一个文档化或结构中，所以大多数情况下它将被忽略。
        @”
            写入一个”符号到输出中，因为此符号可用于指示一个无格式的文本段，所以大多数情况下它将被忽略。
            以下是一个可查找的与配置文件关联的例子：
            `IMAGE_PATH = my_image_dir`
            警告：HTML中所支持的图片格式受限于浏览器的兼容性。Latex中的图片格式必须是eps(Encapsulated PostScript)。
            Doxygen无法检查图片格式是否正确，所以你需要自习确认。
        - @latexonly
            开始一个文本块，只能被完整包含在生成的latex文档中。可用`@endlatexonly`命令结束。
            此命令可为doxygen包含复杂的HTML代码(如图片，公式，特殊字符)，也可用`@htmlonly,@endhtmlonly`命令提供一份合适的latex文档。
            注意：在一个只包含latex的块中可以解析环境变量(如$(HOME))
        - @manonly
            开始一个文本块，只能被完整包含在生成的MAN文档中。可用`@endmanonly`命令结束。
            此命令可为MAN页面中直接包含groff代码，也可用`@htmlonly,@endhtmlonly`命令和`@latexonly,@endlatexonly`命令提供一份合适的HTML和latex文档。
        - @li { item-description }
            除非该命令后遇到一个空白行或是其他`@li`命令，此命令都会有一个参数。它可用于生成一个简单的，无嵌套的参数列表。每一个参数都使用一个`@li`命令开始。
            注意：使用HTML命令可创建嵌套列表
            等价于`@arg`
        - @n
            加入一条新行，等价于`<br>`，可被打印函数使用。
        - @p <word>
            使用打印字体显示`<word>`参数，使用该命令可在运行的文本中引用成员函数。
            等价于`@c`
        - @rtfonly
            开始一个文本块，只能被完整包含在生成的RTF文档中。可用`@endrtfonly`命令结束。
            此命令可为doxygen包含复杂的RFT代码。
            注意：在一个只包含RFT的块中可以解析环境变量(如$(HOME))
        - @verbatim
            开始一个能被HTML和latex文档完整包含的文本块，可用`@endverbatim`命令结束，在一个完整块中不允许任何注释。
            警告：确认每个`@verbatim`都对应有一个`@endverbatim`，否则解析器将会出现冲突。
        - @xmlonly
            开始一个能被XML完整包含的文本块，可用`@endxmlonly`命令结束。
            该命令可用于自定义的XML标记。
        - @\
            写入一个反斜杠到HTML和latex的输出中，因为doxygen可用此斜杠作为命令之间的分隔符，所以大多数情况下它将被忽略。
        - @@
            写入一个at符号到HTML和latex的输出中，因为doxygen可用此符号作为JavaDoc命令之间的分隔符，所以大多数情况下它将被忽略。
        - @~[LanguageId]
            使能/取消一个指定的语言过滤器，用于放置不同语言的文档到一个注释块中，使用`OUTPUT_LANGUAGE`标记过滤掉未指定的语言。使用~[LanguageId]可有效一种输出的指定语言，@~则表示在输出中所有语言均有效。(这也是默认设置的)，例子：
            ```C++
            /*! \~english This is English \~dutch Dit is Nederlands \~german Dies ist
                Deutsch. \~ output for all languages.
             */
        @&
            写入一个&符号到输出中，因为此符号在HTML中有特殊函数，所以大多数情况下它将被忽略。
        @$
            写入一个$符号到输出中，因为此符号可用于扩展环境变量，所以大多数情况下它将被忽略。
        @#
            写入一个#符号到输出中，因为此符号可用于引用文档化的主体，所以大多数情况下它将被忽略。
        @<
            写入一个<符号到输出中，因为此符号在HTML中有特殊函数，所以大多数情况下它将被忽略。
        @>
            写入一个>符号到输出中，因为此符号在HTML中有特殊函数，所以大多数情况下它将被忽略。
        @%
            写入一个%符号到输出中，因为此符号可防止自动连接到一个文档化或结构中，所以大多数情况下它将被忽略。
        @”
            写入一个”符号到输出中，因为此符号可用于指示一个无格式的文本段，所以大多数情况下它将被忽略。
        @.
            这个命令在输出中写一个点号(.)。这个在一下两种情况下比较有用：1.可以当JAVADOC_AUTOBRIEF设置为可使用的时候防止结束一个简短的描述。2. 可以防止开始一个数列当有一个点号要跟在一个数字后面时。
        @::
            这个命令在输出中写一个双冒号(::)。
        @|
            这个命令在输出中写一个管道号(|)。这个符号在某些情况下要被避开，因为它也被用于Markdown表格。
        @–
            这个命令写了两个破折号(–)。这允许连续两个破折号写入输出而不是一个n-dash字符(-)。
        @—
            这个命令写三个破折号(—)输出。这允许写三个连续的破折号输出而不是一个m-dash字符(-)。