TinyXml
    TiXmlBase
        无父类
        友元类：TiXmlNode、TiXmlElement、TiXmlDocument
        函数成员
            公有方法：
                格式打印自身内容到文件
                    virtual void Print( FILE* cfile, int depth ) const = 0;
                控制是否合并连续空白字符，默认为压缩合并
                    static void SetCondenseWhiteSpace( bool condense );
                获取行号、列号
                    int Row() 
                    int Column() 
                设置、获取一个指向任意用户数据的指针
                    void  SetUserData( void* user )	
                解析xml字符串
                    virtual const char* Parse(	const char* p, 
                                    TiXmlParsingData* data, 
                                    TiXmlEncoding encoding)=0;
                编码字符串？
                    static void EncodeString( const TIXML_STRING& str, TIXML_STRING* out );
            保护成员
                跳过空白字符 SkipWhiteSpace
                判断是否为空白字符 IsWhiteSpace
                从输入字符串截取出名字部分 ReadName
                从输入字符串截取出文本部分 ReadText
                从输入字符串截取出一个字符（支持中文）GetChar
                从输入字符串截取出一个数值 GetEntity
                判断字符串相等 StringEqual
                判断是否为英文字符 IsAlpha
                判断是否为数字字符 IsAlphaNum
                大写转小写 ToLower
                utf32转utf8 ConvertUTF32ToUTF8
            私有成员
                等号运算符
        数据成员
            保护类型
                void*			userData;
                TiXmlCursor location;
            私有成员
                static Entity entity[ NUM_ENTITY ];
                    struct Entity
                    {
                        const char*     str;
                        unsigned int	strLength;
                        char		    chr;
                    };
                static bool condenseWhiteSpace;
    TiXmlNode
        继承自：TiXmlBase
        友元类：TiXmlDocument、TiXmlElement
        函数成员：
            公有：
                设置、获取节点的内容
                    void SetValue(const char * _value)
                    const char *Value()；
                    Document节点获取的是文件名
                    Element节点获取的是节点名
                    Comment获取的是注释文本
                    Text获取的是文本字符串
                    Unknown获取的是tag的内容
                删除所有子节点
                    void Clear()
                节点导航
                    TiXmlNode* Parent()
                    TiXmlNode* FirstChild()
                    TiXmlNode* LastChild()
                    TiXmlNode* PreviousSibling()
                    TiXmlNode* NextSibling()	
                    TiXmlElement* NextSiblingElement()     
                    TiXmlElement* FirstChildElement()
                    TiXmlNode* IterateChildren( const TiXmlNode* previous )
                        child = 0;
                        while( child = parent->IterateChildren( child ) 
                        等同于
                        for( child = parent->FirstChild(); child; 
                             child = child->NextSibling() )
                增删节点
                    TiXmlNode* InsertEndChild( const TiXmlNode& addThis );
                    TiXmlNode* LinkEndChild( TiXmlNode* addThis ); //末尾添加
                    TiXmlNode* InsertBeforeChild( TiXmlNode* beforeThis, const TiXmlNode& addThis );
                    TiXmlNode* InsertAfterChild(  TiXmlNode* afterThis, const TiXmlNode& addThis );
                    TiXmlNode* ReplaceChild( TiXmlNode* replaceThis, const TiXmlNode& withThis );
                    bool RemoveChild( TiXmlNode* removeThis );
                获取节点类型
                    int Type()
                获取文件节点（根节点）
                    TiXmlDocument* GetDocument()
                判断是否有子节点
                    bool NoChildren()
                节点类型转换（期待子类实现）
                    virtual TiXmlDocument*          ToDocument()   
                    virtual TiXmlElement*           ToElement()	   
                    virtual TiXmlComment*           ToComment()    
                    virtual TiXmlUnknown*           ToUnknown()	   
                    virtual TiXmlText*	            ToText() 
                    virtual TiXmlDeclaration*       ToDeclaration()  
                克隆节点
                    TiXmlNode* Clone()=0；
                接受访问
                    virtual bool Accept( TiXmlVisitor* visitor )=0；
                    设计模式-访问者模式，数据和操作相分离
                    TiXmlPrinter printer;
                    tinyxmlDoc.Accept( &printer );
                    const char* xmlcstr = printer.CStr();
            保护：
                复制到
                    void CopyTo( TiXmlNode* target )
        数据成员
            保护
                TiXmlNode*		parent;
                NodeType		type;
                TiXmlNode*		firstChild;
                TiXmlNode*		lastChild;
                TIXML_STRING	value;
                TiXmlNode*		prev;
                TiXmlNode*		next;
    TiXmlAttribute
        继承自：TiXmlBase
        友元类：TiXmlAttributeSet
        函数成员
            公有：
                设置、读取名字及属性值
                    char*		Name() 
                    void        SetName( const char* _name )
                    char*		Value()    
                    void        SetValue( const char* _value )
                    int			IntValue()
                    void        SetIntValue( int _value );	
                    double		DoubleValue()
                    void        SetDoubleValue( double _value )
                导航
                    TiXmlAttribute* Next() 
                    TiXmlAttribute* Previous()
                运算符
                    bool operator==( const TiXmlAttribute& rhs )
                    bool operator<( const TiXmlAttribute& rhs )	
                    bool operator>( const TiXmlAttribute& rhs ) 
                解析属性部分
                    输入p指向“属性名=属性值”的开始部分，
                    返回的是“属性名=属性值”的结尾部分。
                    virtual const char* Parse( const char* p, 
                                               TiXmlParsingData* data, 
                                               TiXmlEncoding encoding );
                打印输出到文件或字符串
                    void Print( FILE* cfile, int depth, TIXML_STRING* str )
                设置文档节点指针    
                    void SetDocument( TiXmlDocument* doc )
            私有
                =运算符
        数据成员
            私有
                TiXmlDocument*	document;	// A pointer back to a document, for error reporting.
                TIXML_STRING name;
                TIXML_STRING value;
                TiXmlAttribute*	prev;
                TiXmlAttribute*	next;
    TiXmlAttributeSet
        无父类、无友元类
        公有函数成员
            void Add( TiXmlAttribute* attribute );
            void Remove( TiXmlAttribute* attribute );
            TiXmlAttribute* First();
            TiXmlAttribute* Last();
            TiXmlAttribute*	Find( const char* _name );
        私有函数成员
            void operator=( const TiXmlAttributeSet& );
        私有数据成员
            TiXmlAttribute sentinel;
    TiXmlElement
        继承自：TiXmlNode
        成员函数
            公有
                设置、获取、删除属性值
                    const char* Attribute( const char* name ) const;
                    const char* Attribute( const char* name, int* i ) const;
                    const char* Attribute( const char* name, double* d ) const;
                    void SetAttribute( const char* name, const char * _value );
                    void SetAttribute( const char * name, int value );
                    void SetDoubleAttribute( const char * name, double value );
                    void RemoveAttribute( const char * name );
                    TiXmlAttribute* FirstAttribute()
                    TiXmlAttribute* LastAttribute()
                获取文本值
                    const char* GetText() const;
                克隆节点
                    virtual TiXmlNode* Clone() const;
                打印数据节点内容
                    virtual void Print( FILE* cfile, int depth ) const;
                解析节点部分
                    解析开始自‘<’，结束自‘>’
                    virtual const char* Parse( const char* p, TiXmlParsingData* data, 
                                               TiXmlEncoding encoding );
                节点类型转换
                    TiXmlElement* ToElement()
                接受访问
                    设计模式-访问者模式，数据与操作隔离
                    virtual bool Accept( TiXmlVisitor* visitor ) const;
        数据成员
            私有
                TiXmlAttributeSet attributeSet;
    TiXmlComment               
        继承自：TiXmlNode
        函数成员
            公有
                赋值运算符
                    void operator=( const TiXmlComment& base );
                克隆
                    virtual TiXmlNode* Clone() const;
                打印输出到文件
                    virtual void Print( FILE* cfile, int depth ) const;
                解析注释部分
                    解析开始自!--，结束自>
                    virtual const char* Parse( const char* p, 
                                               TiXmlParsingData* data, 
                                               TiXmlEncoding encoding );
                类型转换
                    virtual TiXmlComment*  ToComment() ;
                接受访问
                    virtual bool Accept( TiXmlVisitor* visitor ) const;
            保护：
                复制到
                    void CopyTo( TiXmlComment* target ) const;
    TiXmlText
        继承自：TiXmlNode
        友元类：TiXmlElement
        函数成员：
            公有：
                等号运算符
                    void operator=( const TiXmlText& base )							 	{ base.CopyTo( this ); }
                打印输出
                    virtual void Print( FILE* cfile, int depth ) const;
                解析文本部分
                    virtual const char* Parse( const char* p, TiXmlParsingData* data, TiXmlEncoding encoding );
                类型转换
                    virtual TiXmlText*       ToText()       { return this; }
                CDATA
                    知识点介绍
                        像 "<" 和 "&" 字符在 XML 元素中都是非法的。
                        "<" 会产生错误，因为解析器会把该字符解释为新元素的开始。
                        "&" 会产生错误，因为解析器会把该字符解释为字符实体的开始。
                        某些文本，比如 JavaScript 代码，包含大量 "<" 或 "&" 字符。
                        为了避免错误，可以将脚本代码定义为 CDATA。
                        CDATA 部分中的所有内容都会被解析器忽略。
                        CDATA 部分由 "<![CDATA[" 开始，由 "]]>" 结束
                        CDATA 部分不能包含字符串 "]]>"。也不允许嵌套的 CDATA 部分。
                        标记 CDATA 部分结尾的 "]]>" 不能包含空格或换行。
                    打开或关闭文本的CDATA表示
                        void SetCDATA( bool _cdata )
                    查询是否使用CDATA节表示文本
                        bool CDATA()
            保护：
                克隆
                    virtual TiXmlNode* Clone() const;
                复制到
                    void CopyTo( TiXmlText* target ) const;
                是否为空（全为空白时也认为为空）
                    bool Blank() const;
        数据成员
            私有
                bool cdata;	
    TiXmlDeclaration
        继承自：TiXmlNode
        说明：xml声明，位于xml文件的第一行
        公有函数成员：
            const char *                Version()            
            const char *                Encoding()
            const char *                Standalone()
            virtual TiXmlNode*          Clone()
            virtual void                Print( FILE* cfile, int depth, 
                                               TIXML_STRING* str ) const;
            virtual const char*         Parse( const char* p, 
                                       TiXmlParsingData* data, 
                                       TiXmlEncoding encoding );
            virtual TiXmlDeclaration*   ToDeclaration() 
            virtual bool                Accept( TiXmlVisitor* visitor );
        私有数据成员：
            TIXML_STRING version;
            TIXML_STRING encoding;
            TIXML_STRING standalone;
    TiXmlUnknown
        继承自：TiXmlNode
        公有函数成员：
            void operator                =( const TiXmlUnknown& copy )	
            virtual TiXmlNode*           Clone() const;
            virtual void                 Print( FILE* cfile, int depth ) const;
            virtual const char*          Parse( const char* p, 
                                                TiXmlParsingData* data, 
                                                TiXmlEncoding encoding );
            virtual const TiXmlUnknown*  ToUnknown()      
            virtual bool                 Accept( TiXmlVisitor* content ) const;
        保护函数成员：
            void CopyTo( TiXmlUnknown* target ) const;
    TiXmlDocument
        继承自：TiXmlNode
        函数成员：
            等号运算符
                void operator=( const TiXmlDocument& copy );
            加载、保存文件    
                bool LoadFile( const char * filename, TiXmlEncoding encoding);
                bool SaveFile( FILE* ) const;
            解析xml数据
                virtual const char* Parse( const char* p, TiXmlParsingData* data = 0, 
                                           TiXmlEncoding encoding = TIXML_DEFAULT_ENCODING );
            获取根节点
                TiXmlElement* RootElement()	
            获取错误
                bool Error()
                const char * ErrorDesc()
                int ErrorId()
                int ErrorRow()
                int ErrorCol()
            清空错误
                void ClearError()
            设置错误（内部使用）
                void SetError( int err, const char* errorLocation, 
                               TiXmlParsingData* prevData, TiXmlEncoding encoding );
            设置缩进
                设置缩进（即一个tab对应几个空格）
                可以保证ErrorRow() 和 ErrorCol()能得到正确的行和列
                应该在parse之前设置，默认为4
                void SetTabSize( int _tabsize )	
                int TabSize()
            打印输出
                virtual void Print( FILE* cfile, int depth = 0 ) const;
            类型转换
                TiXmlDocument*          ToDocument()
            接受访问
                virtual bool Accept( TiXmlVisitor* content ) const;
        私有
            复制到
                void CopyTo( TiXmlDocument* target )
        数据成员
            私有
                bool error;
                int  errorId;
                TIXML_STRING errorDesc;
                int tabsize;
                TiXmlCursor errorLocation;
                bool useMicrosoftBOM;
    TiXmlHandle
        无父类、无友元
        公有函数成员
            节点导航
                TiXmlHandle FirstChild() const;
                TiXmlHandle FirstChild( const char * value ) const;
                TiXmlHandle FirstChildElement() const;
                TiXmlHandle FirstChildElement( const char * value ) const;
                TiXmlHandle Child( const char* value, int index ) const;
                TiXmlHandle Child( int index ) const;
                TiXmlHandle ChildElement( const char* value, int index ) const;
                TiXmlHandle ChildElement( int index ) const;
            节点类型转换
                TiXmlNode* ToNode()         或 TiXmlNode* Node()
                TiXmlElement* ToElement()   或 TiXmlElement* Element()
                TiXmlText* ToText()         或 TiXmlText* Text() 
                TiXmlUnknown* ToUnknown()   或 TiXmlUnknown* Unknown()
        私有数据成员
            TiXmlNode* node;
    TiXmlVisitor
        无父类，无友元
        公有函数成员
            所有这些成员均无实际实现，直接返回true，起到访问者模式接口定义的作用
            virtual bool VisitEnter( const TiXmlDocument& /*doc*/ )	
            virtual bool VisitExit( const TiXmlDocument& /*doc*/ )	    
            virtual bool VisitEnter( const TiXmlElement& /*element*/, 
                                     const TiXmlAttribute* /*firstAttribute*/ )
            virtual bool VisitExit( const TiXmlElement& /*element*/ )
            virtual bool Visit( const TiXmlDeclaration& /*declaration*/ )
            virtual bool Visit( const TiXmlText& /*text*/ )	
            virtual bool Visit( const TiXmlComment& /*comment*/ )
            virtual bool Visit( const TiXmlUnknown& /*unknown*/ )
    TiXmlPrinter
        继承自：TiXmlVisitor
            公有成员函数：
                实现父类的VisitEnter、VisitExit、Visit方法
                设置、读取tab缩进量
                    void SetIndent( const char* _indent )
                    const char* Indent()
                设置、读取换行符
                    默认\n为换行符
                    void SetLineBreak( const char* _lineBreak )	
                    const char* LineBreak()
                切换成流式打印（就是紧凑模式，去掉无用的换行和空白符）
                    void SetStreamPrinting()
                返回结果
                    const char* CStr()	
                返回结果长度
                    size_t Size()
            私有数据成员
                int depth;
                bool simpleTextPrint;
                TIXML_STRING buffer;
                TIXML_STRING indent;
                TIXML_STRING lineBreak;
TinyXPath
    TinyXPath是TinyXml的扩展类
    平常使用TinyXPath时，只需包含xpath_static.h头文件就可以了,内部会自动包含tinyxml.h
    头文件包含层级：
        xpath_static.h
            xpath_processor.h
                action_store.h
                    tinyxml.h
                xpath_expression.h
                    tinyxpath_conf.h
                    tinyxml.h
                    node_set.h
                        tinyxml.h
                        tinyxpath_conf.h
                xpath_stream.h
                    lex_util.h
                        tinyxpath_conf.h
                        tinyxml.h
                    byte_stream.h
                        <string.h>
                        lex_util.h
                    xpath_syntax.h
                        <assert.h>
                        <stdio.h>
                        tokenlist.h
                    tinyxml.h
                    tinystr.h
                xpath_stack.h
                    tinyxpath_conf.h
                    xpath_expression.h
                        tinyxpath_conf.h
                        tinyxml.h
                        node_set.h
                            tinyxml.h
                            tinyxpath_conf.h
                    xpath_stream.h
                        lex_util.h
                            tinyxpath_conf.h
                            tinyxml.h
                        byte_stream.h
                            <string.h>
                            lex_util.h
                        xpath_syntax.h
                            <assert.h>
                            <stdio.h>
                            tokenlist.h
                        tinyxml.h
                        tinystr.h
    namespace TinyXPath         //xpath_static.h
       //不带检查机制的
       extern int               i_xpath_int (const TiXmlNode * XNp_source_tree, const char * cp_xpath_expr);
       extern double            d_xpath_double (const TiXmlNode * XNp_source_tree, const char * cp_xpath_expr);
       extern bool              o_xpath_bool (const TiXmlNode * XNp_source_tree, const char * cp_xpath_expr);
       extern TIXML_STRING      S_xpath_string (const TiXmlNode * XNp_source_tree, const char * cp_xpath_expr);
       extern TiXmlNode *       XNp_xpath_node (const TiXmlNode * XNp_source_tree, const char * cp_xpath_expr);
       extern TiXmlAttribute *  XAp_xpath_attribute (const TiXmlNode * XNp_source_tree, const char * cp_xpath_expr);
       //带检查机制的
       extern bool              o_xpath_int (const TiXmlNode * XNp_source_tree, const char * cp_xpath_expr, int & i_res);
       extern bool              o_xpath_double (const TiXmlNode * XNp_source_tree, const char * cp_xpath_expr, double & d_res);
       extern bool              o_xpath_bool (const TiXmlNode * XNp_source_tree, const char * cp_xpath_expr, bool & o_res);
       extern bool              o_xpath_string (const TiXmlNode * XNp_source_tree, const char * cp_xpath_expr, TIXML_STRING & S_res);
       extern bool              o_xpath_node (const TiXmlNode * XNp_source_tree, const char * cp_xpath_expr, const TiXmlNode * & XNp_node);
       extern bool              o_xpath_attribute (const TiXmlNode * XNp_source_tree, const char * cp_xpath_expr, const TiXmlAttribute * & XAp_attrib);
    分别可用于检索int、double、bool、字符串（TIXML_STRING）、节点（TiXmlNode）、属性（TiXmlAttribute）
    对于不带检查机制的检索函数，第一输入参数是节点，第二输入词句是xpath字符串，检索结果通过返回值得到
    对于带检查机制的检索函数，检索结果通过第三参数得到，函数返回值表明是否检索成功。
    XNp_xpath_node和XAp_xpath_attribute，得到的是XNp_source_tree对应子节点的指针，不应手动释放（由tinyXml控制其释放）
    对于有多个匹配的，只返回第一个
    cp_xpath_expr举例：
        <a>
            <b val="123">
                <b />
                <c />
                <!-- -122.0 -->
                <d />
            </b>
            <!-- 500.0 -->
            <x target='xyz'>sub text</x>
        </a>
        使用S_xpath_string的查找结果：
        "/a/*[name()!='b']" : "x"
        "//b/@val" : "123"
        "//x/text()" : "sub text"
        "//*/comment()" : " -122.0 "
        "( //dummy1 or  //dummy2  or /dummy/dummy2 or /a/b )" : "true"
        "( //dummy1 or  //dummy2  or /dummy/dummy2  )" : "false"
        "translate('aabbccdd','aaabc','AXYB')" : "AABBdd"
        "translate('aabbccdde','abcd','')" : "e"
        "translate('aabbccdd','','ASDF')" : "aabbccdd"
        "translate('aabbccdd','abcd','ABCD')" : "AABBCCDD"
        "translate('aabbccdd','','')" : "aabbccdd"
        "count(//*/comment())" : "2"
        "sum(//@*)" : "123"
        "sum(//*/comment())" : "378"
        "true()" : "true"
        "not(false())" : "true"
        "//*[position()=1]" : "b"
        "count(//*[position()=1])" : "3"
        "//*[position()=2]" : "c"
        "count(//*[position()=2])" : "2"
        "//*[position()=3]" : "d"
        "count(//*[position()=3])" : "1"
        "name(/*/*/*[position()=2])" : "c"
        "name(/*/*/*[last()])" : "d"
        "count(//c/following::*)" : "2"
        "count(/a/b/b/following::*)" : "3"
        "count(//d/preceding::*)" : "2"
        "name(//attribute::*)" : "val"
        "count(//b/child::*)" : "3"
        "count(//x/ancestor-or-self::*)" : "2"
        "count(//b/descendant-or-self::*)" : "4"
        "count(//self::*)" : "6"
        "count(/a/descendant::*)" : "5"
        "count(/a/descendant::x)" : "1"
        "count(/a/descendant::b)" : "2"
        "count(/a/descendant::b[@val=123])" : "1"
        "count(//c/ancestor::a)" : "1"
        "name(//d/parent::*)" : "b"
        "count(//c/ancestor::*)" : "2"
        "name(/a/b/ancestor::*)" : "a"
        "name(/a/b/c/following-sibling::*)" : "d"
        "count(//b/following-sibling::*)" : "3"
        "count(//b|//a)" : "3"
        "count(//d/preceding-sibling::*)" : "2"
        "-3 * 4" : "-12"
        "-3.1 * 4" : "-12.4"
        "12 div 5" : "2.4"
        "3 * 7" : "21"
        "-5.5 >= -5.5" : "true"
        "-5.5 < 3" : "true"
        "-6.0 < -7" : "false"
        "12 < 14" : "true"
        "12 > 14" : "false"
        "14 <= 14" : "true"
        "/a or /b" : "true"
        "/c or /b" : "false"
        "/a and /b" : "false"
        "/a and /*/b" : "true"
        "18-12" : "6"
        "18+12" : "30"
        "count(//a|//b)" : "3"
        "count(//*[@val])" : "1"
        "name(//*[@val=123])" : "b"
        "3=4" : "false"
        "3!=4" : "true"
        "12=12" : "true"
        "'here is a string'='here is a string'" : "true"
        "'here is a string'!='here is a string'" : "false"
        "/a/b/@val" : "123"
        "count(//*/b)" : "2"
        "name(/*/*/*[2])" : "c"
        "name(/*)" : "a"
        "name(/a)" : "a"
        "name(/a/b)" : "b"
        "name(/*/*)" : "b"
        "name(/a/b/c)" : "c"
        "count(/a/b/*)" : "3"
        "ceiling(3.5)" : "4"
        "concat('first ','second',' third','')" : "first second third"
        "ceiling(5)" : "5"
        "floor(3.5)" : "3"
        "floor(5)" : "5"
        "string-length('try')" : "3"
        "concat(name(/a/b[1]/*[1]),' ',name(/a/b/*[2]))" : "b c"
        "count(/a/b/*)" : "3"
        "count(//*)" : "6"
        "count(//b)" : "2"
        "contains('base','as')" : "true"
        "contains('base','x')" : "false"
        "not(contains('base','as'))" : "false"
        "starts-with('blabla','bla')" : "true"
        "starts-with('blebla','bla')" : "false"
        "substring('12345',2,3)" : "234"
        "substring('12345',2)" : "2345"
        "substring('12345',2,6)" : "2345"
        "concat('[',normalize-space('  1  2'),']')" : "[1 2]"
        "2+3+4+5" : "14"
        "20-2-3+5" : "20"
        "count(/a/x[1])" : "1"
        "name(/a/*[2])" : "x"
        "name(/a/*[1])" : "b"
        "name(/a/x[1])" : "x"
        "count(/a/b/c[1])" : "1"
        "count(/a/b/c[position()=1])" : "1"
        "count(/a/b/d[position()=3])" : "0"
        "//x[text()='sub text']/@target" : "xyz"
        "/xml/text/text()" : "within"

-------------------------------------------------------------             
                