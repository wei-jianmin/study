��ʽ�����ַ���
    \a ��֮��������ַ���Ϊб�壬�����հ׽���
    \c ��֮��������ַ����ȳ����ַ�����ϸСһЩ�������հ׽���
    \link ... \linkend �� �м���ַ���Ϊ������
doxygen�ĵ����ɹ���
    https://blog.csdn.net/qq_19528953/category_6362185.html
    doxygen��֧��Markdown�﷨��HTML�﷨  
    ��������һ����\����@��ͷ 
    �����Ϊ���õ�@brief��@details����һ��ע�͵ļ���������ϸ�������磺
    //! @brief ���ڶԻ���
    //! @details ������ʾ���������Ϣ�ĶԻ��򣬵��������������ʱ��ʾ�˶Ի���
    Doxygen���ڲ�֧�ֵ�markdown�﷨
        ����
            markdown������﷨û�ж���һ˵�������Ҫ�ֶεĵط����һ�У��Ϳ��Ա�ʾ���䣬���磺
            Here is text for one paragraph.
            We continue with more text in another paragraph.
        ����
            ����ͨ��markdownһ��������������������-����=��ʵ�ֶ��������һ�����⣬��Ȼ������ֻҪ�������������ٶ��У����磺
            This is a level 1 header
            ====================
            This is a level 2 header
            -------
            ���⣬����Ҳ����ʹ��#���õ���ʹ�õ�#����Ŀ�Ƕ��پʹ�����ټ����⣬���磺
            # This is a level 1 header
            ### This is level 3 header #######
            sss
        ������
            ͨ���ڴ���ע�͵Ŀ�ͷ����һ������>���Ž���
            > This is a block quote
            > spanning multiple lines
        �б�
            Ϊ����ע����ʾ�б�����ʹ��-, +,*�����磺
            - Item 1
              More text for this item.
            - Item 2
              + nested list item.
              + another nested item.
            - Item 3
            �б���Ŀ���Կ�Խ��Σ�ͬʱ�б�Ҳ֧��Ƕ�ף�Ҳ����ʹ�������б����磺
            1. First item.
            2. Second item.
        �����
            ��������ͨ����ͷ���ĸ��ո���ʵ�֣����磺
            This a normal paragraph
                This is a code block
            We continue with a normal paragraph again.
            Ҳ����ʹ������������`���Ż�������\~����Ȼ�������Ŵ�������ԣ����磺
            ~~~~~~~~~~~~~~{C++}
            ~~~~~~~~~{.py}
        ǿ��
            ʹ��һ��*����_����б��ǿ����ʹ������*����_��������ǿ�������磺
             single asterisks*
            _single underscores_
              double asterisks**
            __double underscores__
            ע�⣺���׼markdown��ͬ��doxygen�޷������ڲ���_��*�����a_nice_identifier�����ľ��Ӿ��޷�ʹ��nice���б��ǿ����
            ���⣬_��*��ǿ����ʼ������һ����ĸ�����ַ�������(���纺��)���������俪ͷ����һ���ո�
            ���л���������ַ�<{([,:;����βҲ���������������ͬʱ��ǿ���Ŀ�������ڵ����Ķ��䣡
        �����
            �������Ҫ�������ַ���`��֮�䣬���磺
            Use the `printf()` function.
            Ϊ�����ڲ�ʹ��������Ʋ���ţ���Ҫʹ��������Ʋ���ţ����磺
            To assign the output of command `ls` to `var` use ``var=`ls```.
        ����
            Doxygen֧���ڲ����Ӻ���������
            1 �ڲ�����
                �ڲ�������һ�������ı�(�÷�����������)��һ��ͳһ��Դ��λ��(��С����������)��һ����ѡ���ַ���(������ʾ��)��ɣ����磺
                [The link text](http://example.net/)
                [The link text](http://example.net/ "Link title")
                [The link text](/relative/path/to/index.html "Link title") 
                [The link text](somefile.html) 
                ���⣬���ṩһ�ַ����������ĵ��е����ݣ����磺
                [The link text](@ref MyClass)
            2 ��������
                ����ʹ��ͳһ��Դ��λ�����������Լ�����һ�����ӣ�Ȼ�����ı��ڲ����ã����巽ʽ���£�
                [link name]: http://www.example.com "Optional title"
                ����ú��������������ʹ�����ӣ�
                [link text][link name]
                ��������ı���������ͬ������Լ�д�ɣ�
                [link name][] ����д�� [link name]
                ע�⣺����ƥ���Сд�����У����磺
        ͼƬ
            ͼƬ���Ӻ�����һ������֮ͬ���ǿ�ͷ����һ��!�����磺
            ![Caption text](@ref image.png)
            ![img def]
            [img def]: @ref image.png "Caption text"
        ���
            ������ʹ��|���Ų��������磺
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
            ���Ͼ���Doxygen֧�ֵ�markdown�﷨��
    Doxygen������������
        Doxygen�ڽ���ע�͵�ʱ���кܶ���@����\��ͷ�������һ������������ֶΣ�
        Ȼ��Ϳ����������ĵ���ʱ�������������
        @addtogroup [(title)]
            ʹ��@defgroupͬ�����Զ���һ���飬�������֮�£����ʹ����ͬ<name>��@addtogroup���������־��棬������һ���������и�����title���ĵ����кϲ����顣
            title�ǿ�ѡ�ģ����Ը��������ʹ��@{��@}���һ��������ʵ�嵽һ���Ѵ��ڵ�������磺
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
            ����������õ�һ�������򷽷���ע�Ϳ��У���HAVE_DOT��ΪYES��doxygen������һ������ͼ��
        @callergraph
            ����������õ�һ�������򷽷���ע�Ϳ��У���HAVE_DOT��ΪYES��doxygen������һ��������ͼ��
        @hidecallgraph
            ����������õ�һ�������򷽷���ע�Ϳ��У���HAVE_DOT��ΪYES��doxygen��������һ������ͼ��
        @hidecallergraph
            ����������õ�һ�������򷽷���ע�Ϳ��У���HAVE_DOT��ΪYES��doxygen��������һ��������ͼ��
        @category [] []
            ֻ������Object-C��Ϊһ����Ϊ<name>����ָ��һ���ĵ�ע�Ϳ飬���������Ӧ��@class��ͬ
        @class [] []
            Ϊһ������Ϊ<name>��ָ��һ���ĵ�ע�Ϳ飬��ѡ��ָ����һ��ͷ�ļ���һ��ͷ���ơ����ָ����һ��ͷ�ļ�����HTML�ĵ��н�����һ��ָ���ͷ�ļ�����ȫ���������ӡ�<header-name>���������ڸ���<header-file>֮������ĵ�����ʹ���������ƣ������Ĭ�ϰ���·�����޷���λ�����ļ�(��
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
            ���ڶ���һ��#define��ע�ͣ����磺
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
            Ϊ�ࡢ�ļ��������ռ���飬ָ��һ���ĵ�ע�Ϳ飬���������ࡢ�ļ��������ռ���ĵ������������й��࣬Ҳ���Խ�����Ϊ������ĳ�Ա�������Ϳ��Դ���һ����Ĳ�Ρ�
        @dir []
            Ϊһ��Ŀ¼ָ��һ���ĵ�ע�Ϳ飬path fragment����Ӧ����һ��·������һ������Ŀ������·����һ����Ψһһ��ȫ·��(The ��path fragment�� argument should include the directory name and enough of the path to be unique with respect to the other directories in the project.)
            enum
            Ϊһ������Ϊ<name>��ö������ָ��һ���ĵ�ע�Ϳ飬�����ö�������е�һ����Ա�����ĵ��鴦���ඨ��֮�⣬���������ͬ����Ҫָ�������һ��ע�Ϳ�λ��ö������֮ǰ����ô@enumע�Ϳ��ܱ�ʡ�ԡ�
            ע�⣺һ��������ö�����ͽ����ܱ��ĵ�������һ��������ö��ֵ�ǿ���ʹ�õġ�
            ���磺
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
            Ϊһ��Դ�������ָ��һ���ĵ�ע�Ϳ飬<file-name>��Դ���ļ�������ע�Ϳ�������ĵ�֮�󣬽��������ļ����ı������е����ӽ�������һ���б��У�Ϊ�����ĵ����ĳ�Ա���࣬���ĵ�֮��Ľ������ã�����Դ�����ɨ�裬Դ�ļ���Ŀ¼����doxygen�������ļ���ʹ��EXAMPLE_PATH���ָ����
            ���<file-name>Ҳ������EXAMPLE_PATH���ָ���������ļ�����������Ψһ�ģ�����Ҫ�������ľ���·�������������Ķ����ԡ�
            �����������Ҫ���Դ�ļ�������ʹ��@include������磺
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
            �����������ļ�example_test.cpp
            void main()
            { 
                Example_Test t; 
                t.example();
            }   
        @endinternal
            ����������һ����@internal��ͷ���ĵ��顣ֻҪ��INTERNAL_DOCS����ΪYESʱ��@internal��@endinternal֮����ĵ��ſɼ���
        @extends
            ��������Բ�֧���������ʱ������C���ԣ�������������ֶ�ָ��һ���̳й�ϵ����
            ������Ŀ¼��manual.c�ļ�����ʾ���ʹ��������
        @file []
            Ϊһ������Ϊ<name>��Դ�ļ�����ͷ�ļ���ָ��һ���ĵ�ע�Ϳ顣����ļ�����������Ψһ�ģ���ô����ļ������ܰ���(���ְ���)������·����������ļ�����ʡ��(��@file������)����ô����@file������ĵ��齫�������Ѷ�λ�����Ǹ��ļ���
            Ҫ�㣺ȫ�ֺ���������������ת����ö�ٵ��ĵ�ֻ�ܰ���������У���������Ҳ�ѱ��ĵ�����
            ���ӣ�
            /** @file file.h 
             * A brief file description. 
             * A more elaborated file description. 
             */
            /** 
             * A global integer value. 
             * More details about this value. 
             */
            extern int globalValue;
            ע�⣺�����������JAVADOC_AUTOBRIEF�Ѿ�����ΪYES
        @fn (function declaration)
            Ϊһ������(ȫ�ֺ���������ĳ�Ա����)ָ��һ���ĵ�ע�Ϳ飬������ֻ����һ��ע�Ϳ�û�зŵ���������ǰ����ߺ���ʱ����Ҫ��
            ���ע�Ϳ�ŵ��˺���������ǰ����ߺ��棬�������ʡ��(Ϊ�˱����ظ�)��
            ���棺�ڴ��������Ǿ�����Ҫʱ��Ҫʹ�ã����򽫵�����Ϣ�ظ��Ĵ���
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
            �����࣬�ṹ�����ϵ��ĵ���ͬʱ��Щ�ĵ���λ�����Ƕ����ǰ�档������Ĳ�����@cmdclass����ĵڶ�������������ͬ��header-file���ƻ�����һ���ļ������ܱ�Ӧ�ó���Ϊ��ȡ�࣬�ṹ�����ϵĶ����������<header-name>���������ڸ���<header-file>֮������ĵ�����ʹ���������ƣ������Ĭ�ϰ���·�����޷���λ�����ļ�(��
            @headerfile test.h "test.h"
            @headerfile test.h ""
            @headerfile "" 
            ʹ�ü�����ʱ������ָ��Ŀ�꣬�����ϣ����ȷ��ָ����Ҳ����ʹ��һ�·�ʽ��
            @headerfile test.h <test.h>
            @headerfile test.h <>
            @headerfile <>     
        @hideinitializer
            һ�������ȱʡֵ��һ�������ĳ�ʼ��������ʾ���ĵ��У��������ǵ���������30�����ø�������һ��������߱�����ע�Ϳ��У���ʼ����һֱ�����ء�
        @idlexcept
            �����˸�ע�Ϳ�������ĵ���Ϊ��һ������Ϊ<name>��IDL�쳣
        @implements
            �����ֶ�ָ��һ���̳й�ϵ����������Բ�֧���������ʱ(��C����)��
        @ingroup ( [ ])
            ����������õ�һ���࣬�ļ��������ռ��ע�Ϳ��У��������һ��<groupname>�����������id��
        @interface [] []
            Ϊһ������Ϊ<name>�Ľӿ�ָ��һ���ĵ�ע�Ϳ飬������@class������ͬ
        @internal
            �����ʼһ������Ϊ���ڲ�ʹ�õ��ĵ��Σ����������ע�Ϳ��β����������Ҳ����ͨ��ʹ������@endinternal��ǰ�������ڲ��ĵ��Ρ�
            �����������õ�һ��С����(��@section�е�����)����ô������������С�ڽ�������internal��ֻ��������ͬһ�㼶���½ڲ������¿ɼ���
        @mainpage [(title)]
            �����������õ�һ��ע�Ϳ飬�˿齫�����ڶ���HTML������ҳ����latex�����¡�����ܳ��ã��������ɶ���Ŀ�ʼҳ������ݣ���һ��ʼ�о��˺þò���stackoverflow����鵽Ӧ�������ã���
            title�����ǿ�ѡ�ģ������滻��doxygen���ɵ�Ĭ�ϱ��⡣����㲻��Ҫ�κα��⣬�����������ָ��notitle��
            ���磺
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
            ������ʹ�����е�һ����Ա������@relates����ͬ�Ĺ��ܡ� ֻ���������������ܱ�����Ϊһ�����������Ա����������Բ�֧�ֳ�Ա�����ĸ���ʱ�����ǳ�����(��C����)��
        @name [(header)]
            �������Ա���е�ͷ����ת���һ��ע�Ϳ飬ע�Ϳ齫λ��һ��������Ա���//@{ ... //@} �顣
        @namespace
            Ϊһ������Ϊ<name>�������ռ�ָ��һ���ĵ�ע�Ϳ�
        @nosubgrouping
            �ɷ�����һ�����ĵ��У������ںϲ���Ա��ʱ������doxygen����һ�����У���������˽�е��ӷ��顣
        @overload [(function declaration)]
            ����Ϊһ�����س�Ա�������ɺ����ı�׼�ı�������һ��δ���������ṩ�����غ���������ͬ������������ֻ������Щ�����ܵĲ�����
            ����ں����������߶���֮ǰ���޷���λ���س�Ա�������ĵ������ÿ�ѡ������ָ����ȷ�ĺ����������ɵ���Ϣ֮�󽫻ḽ���ĵ������������ĵ���
            ע�⣺��Ҫ�е���ȷ���ĵ������س�Ա��ȷ�������Σ������������Ϊ�˷�ֹ�ĵ��������У����뽫SORT_MEMBER_DOCS����ΪNO��
            ע�⣺��һ��ע����@overload�����޷�����
            ���磺
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
            Ϊһ������Ϊ<name>��Java��ָ��һ���ĵ�ע�Ϳ顣
        @page (title)
            ָ��һ��ע�Ϳ飬��������һ�����ض����࣬�ļ�����Ա��ֱ�ӹ������ĵ��顣HTML������������һ���������ĵ���ҳ�棬��latex���������ڡ�ҳ�ĵ������½��п�ʼһ���µ�С�ڡ�
            ���磺
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
            ָ��ע�Ϳ��е�˽���ĵ�����Ա����ֻ�ܱ�ͬһ���������Ա���ʡ�
            ע�⣺doxygen���Զ�ȷ����Զ��������еĳ�Ա�����㼶�����������ڲ�֧�ֱ����㼶�ĸ�������ԡ�(��C���Ժ�PHP4)
            ˽�г�ԱС�ڵĿ�ʼ������һ����C++��private:���Ƶı�Ƿ���ʹ��@privatesection
        @privatesection
            ��ʼһ��˽�г�Ա��С�ڣ���C++��private���Ƶı�Ƿ���ָ��ע�Ϳ��е�˽���ĵ�����Ա����ֻ�ܱ�ͬһ���������Ա���ʡ�
        @property (qualified property name)
            Ϊһ������(������ȫ��Ҳ����һ�����Ա)ָ��һ���ĵ�ע�Ϳ飬������ȼ���@var @fn
        @protected
            ָ��ע���ĵ��еı����ĵ�����Ա����ֻ�ܱ�ͬһ���������Ա����������ʡ�
            ע�⣺doxygen���Զ�ȷ����Զ��������еĳ�Ա�����㼶�����������ڲ�֧�ֱ����㼶�ĸ�������ԡ�(��C���Ժ�PHP4)
            ������Ա��ʼ������һ����C++��protected:���Ƶı�Ƿ���ʹ��@privatesection
        @protocol [] []
            ΪObject-C������Ϊ<name>��Э��ָ��һ���ĵ�ע�Ϳ飬���Ĳ�����@class��ͬ��
        @public
            ָ��ע���ĵ��еĹ����ĵ�����Ա����ֻ��������������ʡ�
            ע�⣺doxygen���Զ�ȷ����Զ��������еĹ��в㼶�����������ڲ�֧�ֹ��в㼶�ĸ�������ԡ�(��C���Ժ�PHP4)
            ���г�Ա��ʼ������һ����C++��public:���Ƶı�Ƿ���ʹ��@publicsection
        @pure
            ָ��ע���ĵ��д����Ա�����ǳ����û�б�ʵʩ�ĳ�Ա��
            ע�⣺���������ڲ�֧���鷽���ĸ�������ԡ�(��C���Ժ�PHP4)
        @relates
            ��������Ϊ<name>�ǳ�Ա�������ĵ��������Է�����������������ĵ��ġ�����������С���ڣ���������ڷ���Ԫ��������֮�佨��ǿ����Ƿǳ����õġ����޷������ļ���ֻ�����ں�����
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
            ͬ@relates
        @relatesalso
            ��������Ϊ<name>�ǳ�Ա�������ĵ��������Է�����������������ĵ��ġ�����������С���ڣ�Ҳ����Զ���������ĵ���λ�á���������ڷ���Ԫ��������֮�佨��ǿ����Ƿǳ����õġ�ֻ�����ں�����
        @showinitializer
            ֻ��ʾ�����Ĭ��ֵ�ͱ����ĳ�ʼ����������ǵ��ı�����С��30���ڱ��������ע�Ϳ��з�����������ʼ�����̽�����������ʾ������
        @static
            ָ��ע���ĵ��о�̬��Ա�������������У������������ʵ�����������������࣡
            ע�⣺���������ڲ�֧��̬�����ĸ�������ԡ�(��C���Ժ�PHP4)
        @struct [] []
            Ϊһ������Ϊ<name>�Ľṹ��ָ��һ���ĵ�ע�Ϳ飬�������@class��ͬ
        @typedef (typedef declaration)
            Ϊһ������ת��ָ��һ���ĵ�ע�Ϳ飬�������@var @fn��ͬ
        @union [] []
            Ϊһ������Ϊ<name>��������ָ��һ���ĵ�ע�Ϳ飬�������@class��ͬ
        @var (variable declaration)
            Ϊһ����������ö��ֵָ��һ���ĵ�ע�Ϳ飬�������@typedef @fn��ͬ
        @vhdlflow [(title for the flow chart)]
            ����һ��Ӳ�����������ض���������Է����ĵ��в���һ���߼����̵�����ͼ������ͼ�ı����������ָ����
        @weakgroup [(title)]
            �÷���@addtogroup���ƣ���������鶨���ͻʱ����������һ�����͵����ȼ���
    ����������֮"С��ָʾ����"
        @attention { attention text }
            ��ʼһ����������Ҫ������Ϣ�Ķ��䣬�ζ��佫�����ţ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ��������Է��õ��ö����У�������ڵ�@attention�������ϵ�һ�������Ķ����У�������һ���հ��л�����������С�������ô@attention����ֹ��
            @author { list of authors }
            ��ʼһ��������һ�����߶���������Ķ��䣬�˶��佫�����ţ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ������Է��õ��ö����У�������ڵ�@author�������ϵ�һ�������Ķ����У�ÿ������������������һ�����У�����һ�� @author������ܻ������ɸ����ߣ�������һ���հ��л�����������С�������ô@author����ֹ�����磺
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
            ͬ@author�ȼ�
        @brief { brief description }
            ��ʼһ����Ϊ���������Ķ��䣬���ĵ�ҳ����ʼ���ֿ�ʹ������ļ��ļ����������б�����ϸ��������ǰ�˺ͳ�Ա�������������Ա���ļ���Ա�ļ���������һ����������������Ҫ������(���ܽ��������ּ����ķ��)��������һ���հ��л�����������С�������ô������������ֹ��������ֶ��@brief�����ô���ǽ��������һ�𡣲鿴����@authhor�����ӡ���ͬ������@short
        @bug { bug description }
            ��ʼһ���ɱ���һ������bug�Ķ��䣬�˶��佫�����ţ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ������Է��õ��ö����У�������ڵ�@bug�������ϵ�һ�������Ķ����У�ÿ��bug��������һ�����У�����һ�� @bug������ܻ������ɸ�bug��������һ���հ��л�����������С�������ô@bug����ֹ���鿴����@authhor�����ӡ�
        @cond [(section-label)]
            ��ʼһ����������С�ڣ�ʹ������@endcond����ֹ��С�ڣ�ͨ����������ע�Ϳ��пɲ��ҵ�@endcond���˶������Ŀ���ǣ�(������)�ڴ����н�һ�����ļ��ų���
            С�ڽ�����������@cond��@endcond֮�䣬����С�ڵı�ż��뵽����ѡ��ENABLED_SECTIONS�У������ű����ԣ���С��Ҳ���ڴ����б����������ԡ�
            ��ע�Ϳ��е�����С�ڣ���ʹ��һ��@if...@endif�顣
            ����С���ܱ�Ƕ�ף�����������£��������Ƕ�׵�С�ڶ����������У���ôֻ�б�Ƕ�׵�С�ڲŻ���ʾ�����磺
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
            ��ʼ����һ��ʵ��İ�Ȩ�Ķ��䣬��������յ�Լ����������������û��������ڲ��ṹ���鿴����@authhor�����ӡ�
        @date { date description }
            ��ʼһ���ɿ�����һ���������ڵĶ��䣬�˶��佫�����ţ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ������Է��õ��ö����У�������ڵ�@date�������ϵ�һ�������Ķ����У�ÿ��date��������һ�����У�����һ�� @date������ܻ������ɸ�date��������һ���հ��л�����������С�������ô@date����ֹ���鿴����@authhor�����ӡ�
        @deprecated { description }
            ��ʼһ��ָʾ�ĵ����Ƿ����õĶ��䣬�������������������Ԥ���������ڵ�
        @details { detailed description }
            ��ͬ@brief��ʼһ������������@details����ʼһ��ϸ����������Ҳ���Կ�ʼһ���¶���(����հ���)���������������@details��
        @else
            ��ʼһ������С�ڣ����ǰһ������С����Ч��ǰһ��С�ڿ�ʹ������@if,@ifnot,@elseif��ʼ��
        @elseif (section-label)
            ��ʼһ������С�ڣ����ǰһ������С����Ч��������С��Ĭ��Ϊ��Чʱ���������ø������section-label�����ñ��ENABLED_SECTIONS��ʹ������@elseif��Ч�����������Ƕ�ף��������Ƕ�׵���������Ч����ôҲֻ�����ڲ��Ƕ��С�ڲŻᱻ��ȡ��
        @endcond
            ����һ����@cond��ʼ������С�ڡ�
        @endif
            ����һ����@if��@ifnot��ʼ������С�ڣ�ÿ��@if��@ifnotֻ��һһ��Ӧƥ��֮���@endif��
        @exception { exception description }
            Ϊһ������Ϊ<exception-object>�쳣�������ʼһ������������Ǵ��쳣������������ȥ����Ƿ��������쳣���󡣶�����ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ��������Է��õ��ö����У�������ڵ�@exception�������ϵ�һ�������Ķ����У�ÿ��������������������һ�����У�������һ���հ��л�����������С�������ô@exception����ֹ��
            ��@exceptionһ����
        @if (section-label)
            ��ʼһ�����������ĵ�С�ڣ���ʹ��һ��ƥ�������@endif������������С��Ĭ��Ϊ��Чʱ���������ø������section-label�����ñ��ENABLED_SECTIONS��ʹ������@if��Ч�����������Ƕ�ף��������Ƕ�׵���������Ч����ôҲֻ�����ڲ��Ƕ��С�ڲŻᱻ��ȡ�����磺
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
            �������alias��ʹ���������������������������ĵ���һ���࣬���������ʹ�ã�
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
            һ���������ļ��е�alias��
            ALIASES  = "english=\if english" \
                       "endenglish=\endif" \
                       "dutch=\if dutch" \
                       "enddutch=\endif" 
            ��ôENABLED_SECTIONS������ЧenglishҲ����Чdutch
        @ifnot (section-label)
            ��ʼһ�����������ĵ�С�ڣ���ʹ��һ��ƥ�������@endif������������С��Ĭ��Ϊ��Чʱ���������ø������section-label�����ñ��ENABLED_SECTIONS��ʹ������@ifnot��Ч��
        @invariant { description of invariant }
            ��ʼһ������������ʽ�Ķ��䣬�˶��佫�����ţ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ��������Է��õ��ö����У�������ڵ�@invariant�������ϵ�һ�������Ķ����У�ÿ��invariant������������һ�����У�����һ��@invariant������ܻ������ɸ�����ʽ��������һ���հ��л�����������С�������ô@exception����ֹ��
        @note { text }
            ��ʼһ��������ʾ�Ķ��䣬�˶��佫�����ţ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ��������Է��õ��ö����У�������ڵ�@note�������ϵ�һ�������Ķ����У�ÿ��note������������һ�����У�����һ��@note������ܻ������ɸ���ʾ��������һ���հ��л�����������С�������ô@note����ֹ���鿴@par��������ӡ�
        @par [(paragraph title)] { paragraph }
            ���һ����������Ѿ��������������ʼһ���û��Զ���Ķ�ͷ����ͷ����ռ��һ�У������Ķ�ͷ�������š�
            ����������δ�������������ʼһ���¶��䣬Ҳ�ɲ���������������(��@param��@warning)����ֹ�����
            ������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ��������Է��õ��ö����У�������һ���հ��л�����������С�������ô@par����ֹ�����磺
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
            Ϊһ������Ϊ<parameter-name>����������ʼһ����������������ȥ����Ƿ���ڡ�����ں������������У��ò���(����������)���ĵ���ʧ��δ���֣��������һ�����档
            @param������һ����ѡ���ԣ���ָ�������ķ������ԣ���Ϊinto��out������һ�����ӣ�
            /*! * Copies bytes from a source memory area to a destination memory area, 
             * where both areas may not overlap. 
             * @param[out] dest The memory area to copy to.
             * @param[in]  src  The memory area to copy from.
             * @param[in]  n    The number of bytes to copy 
             */void 
            memcpy(void *dest, const void *src, size_t n); 
            ��������ȿ�������Ҳ���������ʹ��[in,out]ָ���������ԣ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ��������Է��õ��ö����У�������ڵ�@param�������ϵ�һ�������Ķ����У�ÿ������������������һ�����У�������һ���հ��л�����������С�������ô@param����ֹ��
        @parblock
            ������Щ���۵�һ����Ĳ���( @par, @param �� @warning)��@parblock������Ϊһ����Խ���ж������������������endparblock���������磺
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
            ����һ����@parblock��ͷ�Ķ���顣
        @tparam { description }
            Ϊһ������Ϊ<template-parameter-name>�����ģ�������ʼһ��ģ�������������ͬ��@cmdparam
        @post { description of the postcondition }
            ��ʼһ���������ĺ��������Ķ��䣬�˶��佫�����ţ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ��������Է��õ��ö����У�������ڵ�@post�������ϵ�һ�������Ķ����У�ÿ������������������һ�����У�����һ��@post������ܻ������ɸ���ʾ��������һ���հ��л�����������С�������ô@post����ֹ��
        @pre { description of the precondition }
            ��ʼһ����������ǰ�������Ķ��䣬�˶��佫�����ţ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ��������Է��õ��ö����У�������ڵ�@pre�������ϵ�һ�������Ķ����У�ÿ��ǰ������������������һ�����У�����һ��@pre������ܻ������ɸ���ʾ��������һ���հ��л�����������С�������ô@pre����ֹ��
        @remark { remark text }
            ��ʼһ��������һ��������ע�Ķ��䣬�˶��佫�����ţ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ��������Է��õ��ö����У�������ڵ�@remark�������ϵ�һ�������Ķ����У�ÿ����ע��������һ�����У�����һ��@remark������ܻ������ɸ���ʾ��������һ���հ��л�����������С�������ô@remark����ֹ��
        @remarks { remark text }
            ͬ@remark��
        @result { description of the result value }
            ͬ@return��
        @return { description of the return value }
            ��ʼһ��������һ��������ע�Ķ��䣬�˶��佫�����ţ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ��������Է��õ��ö����У�������һ���հ��л�����������С�������ô@remark����ֹ���ο�@fn�����е����ӡ�
        @returns { description of the return value }
            ͬ@return��
        @retval { description }
            Ϊһ������Ϊ<return value>������ʼһ������ֵ��������������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ��������Է��õ��ö����У�������ڵ�@retval�������ϵ�һ�������Ķ����У�ÿ����ע��������һ�����У�������һ���հ��л�����������С�������ô@retval����ֹ��
        @sa { references }
            Ϊָ�����ࡢ�������������������ļ���URL��һ�������������ÿ�ʼһ�����䣬ʹ��::����#��Ϊ�������һ����Ա���������ӷ�����������������ơ��ڷ�������֮�����һ�������ŵĲ��������б��������ɸ����ط������߹�������ѡ��
        @see { references }
            Ϊ�˼���JavaDoc����ͬ��@sa��
        @short { short description }
            ͬ@brief��
        @since { text }
            ����ָ��һ����Ч�İ汾��ʱ�䣬@since֮��Ķ��䲻��ָ��һ���ڲ��ṹ�������Ӿ���ǿ��������Է��õ��ö����У�������һ���հ��л�����������С�������ô@since����ֹ��
        @test { paragraph describing a test case }
            ��ʼһ���������Ĳ��������Ķ��䣬������������������������һ�������Ĳ����б��У����������������ɽ������á��ڲ����б��е�ÿһ������������ǰ�ˣ�������һ��ָ����������ͷ��
        @throw { exception description }
            ͬ@exception��
        @throws { exception description }
            ͬ@throw��
        @todo { paragraph describing what is to be done }
            ��ʼһ����������todo��Ŀ�Ķ��䣬����������������Ŀ��һ��������todo�б��У����������������ɽ������á��ڲ����б��е�ÿһ������������ǰ�ˣ�������һ��ָ����������ͷ��
        @version { version number }
            ��ʼһ���ɿ�����һ�������汾�ַ����Ķ��䣬�˶��佫�����ţ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ������Է��õ��ö����У�������ڵ�@version�������ϵ�һ�������Ķ����У�ÿ���汾����������һ�����У�����һ�� @version������ܻ������ɸ��汾�ַ�����������һ���հ��л�����������С�������ô@version����ֹ���鿴����@authhor�����ӡ�
        @warning { warning message }
            ��ʼһ���ɿ�����һ������������Ϣ�Ķ��䣬�˶��佫�����ţ�������ı�����ָ��һ���ڲ��ṹ�������Ӿ���ǿ������Է��õ��ö����У�������ڵ�@warning�������ϵ�һ�������Ķ����У�ÿ���汾����������һ�����У�����һ�� @warning������ܻ������ɸ����棬������һ���հ��л�����������С�������ô@warning����ֹ���鿴����@authhor�����ӡ�
        @xrefitem ��(heading)�� ��(list title)�� { text }
            ��������һ��������@todo,@bug�ļ��ϣ����ڴ����û��Զ����ı�С�ڣ����������ӵ������ҳ��֮���Զ����ɽ������ã��������Ѽ�����ҳ���е�������ͬ���͵�С�ڡ���һ��������һ������С�����͵�Ψһ��ʶ���ڶ���������һ���������ŵ��ַ����������ڱ������ĸ����������ı��µ�С��ͷ��Ϊ����ͬһ����ʶ��������Ŀ���ҳ�棬��������������Ϊһ��������ʹ�ã�һЩ�Ѿ�Ԥ����ı�ʶ��todo,test,bug,deprecated��
            �������ʹ��@xrefitem����������к�Ľ�������ֻ����todo�б�������ȥ������һ��alias��
            \xrefitem todo "Todo" "Todo List"
            Ϊÿ��С�ڶ����ظ��������ǰ������������ʹ�����ǳ��״�������Ҳ�����ںϲ������ļ��е�ALIAESѡ��������һ��������@reminder�������һ�����ݵ������ļ���
            ALIASES += "reminder=\xrefitem reminders \"Reminder\" \"Reminders\""
            ע�⣺�����еڶ��͵�������ʹ��ת�����š�
            ��һ������(heading)����һ�����ַ�����û��heading���ɡ�����@page��������ʹ��ʱ��ǳ����á����磺
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
            �����@error����Ϊ��
            ALIASES += "error=\xrefitem my_errors \"\" \"\""
    ����������֮"������������" 
        @addindex (text)
            ���1�ı���latex������
        @anchor
            ����һ�����ɼ�����������anchor(�̶���)���ĵ��У�����ʹ��@ref����������á�
            ע�⣺anchorĿǰֻ�ܷ�����һ����ǳ�ҳ��(ʹ��@page)����ҳ(ʹ��@mainpage)��ע�Ϳ���
        @cite
            ����һ���鼮�ο���һ���ı�����Ŀ�ο��б��
        @endlink
            ��ֹһ������@link��ʼ������
        @link
            ��������doxygen�Զ����ɵģ���һֱ��һ��ָ��Ķ�������Ϊ�����ı���������������ڴ���һ������(һ���ļ�������߳�Ա)�����ӣ������û���ָ������������ı�����������Ա�@endlink��ֹ����������֮����ı�������Ϊָ��@link��һ������<link-object>�������ı���
        @ref [��(text)��]
            ����һ��������С�ڣ���С�ڣ�ҳ���anchor(�̶���)�����ã���HTML�ĵ��и��������һ��ָ��С�ڵ����ӡ���һ��С�ڻ�����С���н�ʹ��С�ڱ�����Ϊ�����ı�����anchor(�̶���)�п�ʹ�����ż��text���ߵ�text����ʱʹ��<name>��Ϊ�����ı�������latex�ĵ��У����<name>���õ���һ��anchor(�̶���)�������С������һ����Ż�����ʹ��һ��ҳ���ź���ı���
        @refitem
            ����@ref�����������һ������С�ڵ����ã����������һ����@secreflist��ʼ��@endsecreflist�������б��С�
        @secreflist
            ��ʼһ�������б���@refitem������ÿһ�������ӵ���Ӧ������С��
        @endsecreflist
            ��ʼ��@secreflist��ͷ�ı����б�
        @subpage [��(text)��]
            ��������ҳ���һ����Σ���ͬ�ṹҲ����ʹ��@defgroup,@ingroup�������ҳ����ʹ��@subpage��������㡣��ҳ@mainpageͨ���ǲ�εĸ��ڵ㡣
            ������������@ref�������ڴ���һ����<name>ҳ���ǩ�����ã����ҿ�ѡ��ڶ�������ָ����text��Ϊ�����ı���
            ����ͬ��@ref����֮�����ڣ���ֻ�ܹ�����ҳ���У���ҳ���д���һ�����ӹ�����������ҳ��ʹ��<name>���б�ʶ��
            ���磺
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
            ��ҳ�涥�˴���һ�����ݱ���г�ҳ��������С�ں���С��
            ���棺������ֻ�ܹ�����һ�����ҳ�ĵ����С���У����޷������������ĵ����ж��ҽ�����HTML�������Ч��
        @section (section title)
            ����һ����Ϊ<section-name>��С�ڣ�С�ڵı����ʹ������ĵڶ�����ָ����
            ���棺������ֻ�ܹ�����һ�����ҳ�ĵ����С���У����޷������������ĵ����С�
        @subsection (subsection title)
            ����һ����Ϊ<section-name>����С�ڣ�С�ڵı����ʹ������ĵڶ�����ָ����
            ���棺������ֻ�ܹ�����һ�����ҳ�ĵ����С���У����޷������������ĵ����С�
        @subsubsection (subsubsection title)
            ����һ����Ϊ<section-name>����С�ڵ�С�ڣ�С�ڵı����ʹ������ĵڶ�����ָ����
            ���棺������ֻ�ܹ�����һ�����ҳ�ĵ����С���У����޷������������ĵ����С�
        @paragraph (paragraph title)
            ����һ����Ϊ<paragraph-name>�Ķ��䣬���ı����ʹ������ĵڶ�����ָ����
            ���棺������ֻ�ܹ�����һ�����ҳ�ĵ����С���У����޷������������ĵ����� 
    ����������֮"������ʾ���ӵ�����"
        @dontinclude
            ���ڽ���һ��Դ�ļ����Ҳ����Ƿ��ĵ���������(��ͬ@include����������)�������ϣ����Դ�ļ��ָ����С�Ŀ飬������Щ���м�����ĵ����Ǵ������ǳ����á�Դ�ļ�����Ŀ¼��ʹ�������ļ��е�EXAMPLE_PATH�����ָ����
            �ڽ�������@dotinclude�����ע�Ϳ��ڼ䣬���������ͳ�Ա�������Ͷ��彫�������䡯��
            ���ڵ��п�ʹ��Դ�ļ��ĵ�������������ʾһ�л�������ӿ�ʹ��@line,@skip,@skipline,@until���Ϊ����Щ�����ʹ��һ���ڲ�ָ�룬@dontinclude���趨���ָ��ָ�����ӵĵ�һ�С�
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
            �����ļ�example_test.cpp���£�
            void main()
            {
                Example_Test t;  
                t.example();
            } 
        @include
            ���ڰ���һ��Դ�ļ���Ϊһ������飬���������һ�������ļ����Ĳ�����Դ�ļ�����Ŀ¼��ʹ�������ļ��е�EXAMPLE_PATH�����ָ����
            �����EXAMPLE_PATH�����ָ����<file-name>�������ļ����趨��������Ψһ�ģ��ͱ������<file-name>�ľ���·�������������ԡ�
            ʹ��@include����ȼ������ĵ��в����ļ�����ʹ��@code,@endcode�����޶��ļ��ķ�Χ��
        @include�������ҪĿ���ǣ������ڰ������Դ�ļ���ͷ�ļ������ӿ��г��ִ����ظ���
            Դ�ļ��ĵ�����������ʹ�������@line,@skip,@skipline,@until�����@dotinclude���
            ע�⣺doxygen�����������޷��ڴ�����й����ģ��������ڴ�����з���Ƕ�׵�C���ע�͡�Ҳ�ɲ鿴@example,@dontinclude,@verbatim���
        @includelineno
            �߱���@include������ͬ�Ĺ���ģʽ����������кŵ������ļ��С�
        @line ( pattern )
            ���������У����Ǹ������ҵ�һ���ǿ��У����������������@include��@dontinclude���������ӣ�������а���ָ����ģʽ����д�������
            �������л�ʹ��һ�����ٵ�ǰ�е��ڲ�ָ�룬���ҵ��ǿ�����Ϊ��ʼ�У����趨�ڲ�ָ�롣(���δ�ҵ�����Ҫ����У�ָ��Ҳ��ָ�����ӵ�ĩ��)
        @skip ( pattern )
            ���������У����Ǹ������ҵ�һ������ָ��ģʽ���з��������������@include��@dontinclude���������ӡ�
            �������л�ʹ��һ�����ٵ�ǰ�е��ڲ�ָ�룬���ҵ�������Ϊ��ʼ�У����趨�ڲ�ָ�롣(���δ�ҵ�����Ҫ���ģʽ��ָ��Ҳ��ָ�����ӵ�ĩ��)
        @skipline ( pattern )
            ���������У����Ǹ������ҵ�һ������ָ��ģʽ���У����������������@include��@dontinclude����������,��������д�������
            �������л�ʹ��һ�����ٵ�ǰ�е��ڲ�ָ�룬��д�������������Ϊ��ʼ�У����趨�ڲ�ָ�롣(���δ�ҵ�����Ҫ���ģʽ��ָ��Ҳ��ָ�����ӵ�ĩ��)
        @snippet ( block_id )
            ����@include���������������һ���������ļ���ΪԴ���룬����������������һ��������Ϊԭ�ļ��������������<file-name>��ǰ�ļ���Ϊ�ļ���Ƭ�Ρ�
            ����,������������ĵ���,����һ��Ƭ���ļ������ӡ�cppפ����һ����Ŀ¼Ӧ��EXAMPLE_PATHָ����
            \snippet snippets/example.cpp Adding a resource
            �ļ�������ı�Ƭ�ε�Ωһ��ʶ�������������������Ƭ���ļ������õĴ���������ʾ����ʾ,��Ӧ������\Ƭ������:
                QImage image(64, 64, QImage::Format_RGB32);    
                image.fill(qRgb(255, 160, 128));//! [Adding a resource]    
                document->addResource(QTextDocument::ImageResource,        
                QUrl("mydata://image.png"), QVariant(image));//! [Adding a resource]    ...
            ע��,�������������ǲ��ᱻ����,�������������:
            document->addResource(QTextDocument::ImageResource,    QUrl("mydata://image.png"), QVariant(image));
            ��Ҫע��(block_id)���Ӧ����ȫ��Դ�ļ��г������Ρ���������
            ��һ�ַ����μ�\ dontinclude������Ƭ��Դ�ļ�����Ҫ��ǡ�
        @until ( pattern )
            ��������@include��@dontinclude�������е�������д��������������ҵ�һ������ָ��ģʽ���У���ֻд�����ָ��ģʽ��һ�С�
            �������л�ʹ��һ�����ٵ�ǰ�е��ڲ�ָ�룬��д�������������Ϊ��ʼ�У����趨�ڲ�ָ�롣(���δ�ҵ�����Ҫ���ģʽ��ָ��Ҳ��ָ�����ӵ�ĩ��)
        @verbinclude
            ���ĵ�������������Ϊ<file-name>�ļ���������ȼ������ĵ��з���@verbatim,@endverbatim�����޶�<file-name>�ļ���
        @htmlinclude
            ��HTML�ĵ�������������Ϊ<file-name>�ļ���������ȼ������ĵ��з���@htmlonly
        @latexinclude
            �������������ļ�<�ļ���>�ĵ��������൱��ճ���ļ��ĵ��ͷ���@ latexonly��@endlatexonly���������
            ���ļ���Ŀ¼,doxygenӦ��Ѱ�ҿ���ָ��ʹ��doxygen EXAMPLE_PATH��ǩ�������ļ���
    ����������֮"�����Ӿ���ǿ������"
        @a
            ʹ��һ��ָ����������ʾ<word>�����������е��ı�ʹ�ô���������Ա���������á����ӣ�
            ... the \a x and \a y coordinates are used to ...
            һ������ʾ�����
            �� the x and y coordinates are used to ��
        @arg { item-description }
            ���Ǹ����������һ���հ��л�������@arg������������һ��������������������һ���򵥵ģ���Ƕ�׵Ĳ����б�ÿһ��������ʹ��һ��@arg���ʼ�����磺
              @arg @c AlignLeft left alignment.
              @arg @c AlignCenter center alignment.
              @arg @c AlignRight right alignment
              No other types of alignment are supported.
            �������ʾ��
            AlignLeft left alignment.
            AlignCenter center alignment.
            AlignRight right alignment
            No other types of alignment are supported.
            ע�⣺ʹ��HTML����ɴ���Ƕ���б�
            �ȼ���@li
        @b
            ʹ��һ��������ʾ<word>�������ȼ���<b>word</b>��Ҳ�ɷ��ö���֣���<b>multiple words</b>��
        @c
            ʹ��һ����ӡ������ʾ<word>������ʹ�ø���������Word�ı��룬�ȼ���<tt>word</tt>
            ���ӣ�
            ... This function returns @c void and not @c int ...
            �����ǽ���ı���
            �� This function returns void and not int ��
        @code [ ��{����}��]
            ��ʼһ������飬һ�������Ĵ���ͬ����ͨ�ı�����Ĭ�ϱ�������C/C++���룬�ĵ�������ͳ�Ա�����ƽ��Զ���ָ���ĵ������Ӵ��档
        @copydoc
            ��ָ����<link-object>�����и���һ���ĵ��飬��ʹ�ñ���������н�����Ϊ�����ĵ����ظ��������������ǳ����ã�����������չһ��������Ա���ĵ���
            ���Ӷ����ָ��һ����Ա(�ɴ���һ���࣬�ļ�����)��һ���࣬һ�������ռ䣬һ���飬һ��ҳ�����һ���ļ�(��˳����)��ע�⣬����˶���ָ��һ����Ա(�����ں���������������ת����)��Ϊ��ʹ�乤�����������ĸ�����(�࣬�ļ�����)�����ĵ�����
            Ϊ�˸������Ա���ĵ��������ĵ��з���һ�����ݣ�
            /*! @copydoc MyClass::myfunction()
             *  More documentation.
            ����ó�Ա�����أ���ָ����ͬ�Ĳ�������(���Ա��֮�䲻���ո�)�����£�
            //! @copydoc MyClass::myfunction(type1,type2)
            ������ĵ����в鵽����ó�Ա���ı�������Ҫ����ƥ������ơ�
            Copydoc��������ڵݹ飬���ݹ��ÿһ�㼶������ʱ�жϲ���¼����ͬ����һ������
            - @copybrief
        @copydoc����ļ��׹�����ʽ��ֻ���Ƽ�����������������ϸ������
        @copydetails
        @copydoc����ļ��׹�����ʽ��ֻ���Ƽ�����������������ϸ������
        @docbookonly
            ��ʼһ���ı��飬����ı��齫���������ֵİ��������ɵ�docbook�ĵ��С�����ı�����@enddocbookonly�������
            @dot [��caption��] [=]
            ��ʼһ���ɰ���dotͼ���������ı��Σ����ı��ο���@enddot������Doxygen�����ı���dot����������Ľ��ͼƬ(һ��ͼƬӳ��)�а�����Щ�ı���ͼ�еĽڵ��ǿɵ����ģ���������URL����ʹ��URL�е�@ref����������doxygen�е���Ŀ�����磺
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
         @msc [��caption��] [=]
            ��ʼһ���ɰ�����Ϣ����ͼ�������ı��Σ��鿴�����ַ��һЩ���ӡ����ı��ο�������@endmsc������
            ע�⣺��msc{��}���еĸ��ı���ֻ������Ϣ����ͼ��һ���֡�����Ҫ��װmscgen���ߣ�����ʹ�ô�������磺
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
        @startuml [{file}] [��caption��] [=]
            ��ʼһ���ɰ���һ��PlanUMLͼ����Ч�������ı��Σ��鿴�����ַ��һЩ���ӡ����ı��ο�������@enduml������
            ע�⣺����Ҫ��װJava��PlantUML��s jar�ļ�����ʹ�ô����jar�ļ�������Ҫʹ��PLANTUML_JAR_PATHָ����
            ��һ�������ǿ�ѡ�Ĳ�����Ϊ����doxygenǰ��һ��Ԥ�����裬Ϊ�˺�����PlantUML���ݡ���Ҳ������@startuml֮��Ļ�����������ͼ����ļ������֣����磺
              @startuml{myimage.png} "Image Caption" width=5cm
              Alice -> Bob : Hello
              @enduml
              ```
            ��ָ��ͼ�������ʱ��doxygen�������һ�����Ǹ�����������ͼƬ�����û�����֣�doxygen�����Զ�ѡ��һ�����֡�
            �ڶ��������ǿ�ѡ�Ĳ��ҿ�������ָ����ͼƬ����ı��⡣���������������������֮��ָ����ʹ���������κοո������ڱ�����ʾǰ�ᱻȥ����
            ����������ͬ����ѡ��������ָ��ͼƬ�ĸ߶ȺͿ�ȡ�
            ������һ��ʹ����`@startuml`��������ӣ�
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
        @dotfile [��caption��] [=]
            ���ĵ��в���һ��dot���ɵ�<file>ͼƬ��
            ��һ������ָ����ͼƬ�����ơ�Doxygen������DOTFILE_DIRS��Ǻ�ָ����·���в����ļ���������ҵ�����Ϊdot���ߵ������ļ������ͼƬ�����õ���ȷ������Ŀ¼�С����dot�ļ����а����ո���Ҫʹ�����Ž������Ρ�
            �ڶ���������ѡ������ָ��ͼƬ����ʾ�ı��⣬��ʹ��û�а����ո�Ҳ������õ�����֮ǰ���ڱ�����ʾ֮ǰ���Żᱻɾ����
        @mscfile [��caption��] [=]
            ���ĵ��в���һ��mscgen���ɵ�<file>ͼƬ���鿴�����ַ��һЩ���ӡ�
            ��һ������ָ����ͼƬ���ļ�����doxygen����Ѱ����ָ����MSCFILE_DIRS��ǩ�����·�����ļ������msc�ļ����ҵ���������������Ϊmscgen���ߵ������ļ������ͼƬ�����ŵ���ȷ�����Ŀ¼�����msc�ļ��������ո��㽫����������Χ���Ϸ���(������)��
            �ڶ��������ǿ�ѡ�Ĳ��ҿ�������ָ����ͼƬ����ı��⡣���������������������֮��ָ����ʹ���������κοո������ڱ�����ʾǰ�ᱻȥ����
            ����������ͬ����ѡ��������ָ��ͼƬ�ĸ߶ȺͿ�ȡ�
        @diafile [��caption��] [=]
            ���ĵ��в���һ��dia���ɵ�<file>ͼƬ��
            ��һ������ָ����ͼƬ���ļ�����doxygen����Ѱ����ָ����DIAFILE_DIRS��ǩ�����·�����ļ������msc�ļ����ҵ���������������Ϊmscgen���ߵ������ļ������ͼƬ�����ŵ���ȷ�����Ŀ¼�����msc�ļ��������ո��㽫����������Χ���Ϸ���(������)��
            �ڶ��������ǿ�ѡ�Ĳ��ҿ�������ָ����ͼƬ����ı��⡣���������������������֮��ָ����ʹ���������κοո������ڱ�����ʾǰ�ᱻȥ����
            ����������ͬ����ѡ��������ָ��ͼƬ�ĸ߶ȺͿ�ȡ�
        @e
            ʹ��б����ʾ<word>������ͻ��word��
            �ȼ���@em��Ϊ��ͻ������ֿ���<em>multiplewords</em>
        @em
            ʹ��б����ʾ<word>������ͻ��word��
            �ȼ���@e
        @endcode
            ����һ�������
            Ҳ�ɲ鿴@code����
        @enddocbookonly
            ����һ��@docbookonly��ʼ�Ŀ�
        @enddot
            ����һ��@dot��ʼ�Ŀ�
        @endmsc
            ����һ��@msc��ʼ�Ŀ�
        @enduml
            ����һ��@enduml��ʼ�Ŀ�
        @endhtmlonly
            ����һ��@htmlonly��ʼ�Ŀ�
        @endlatexonly
            ����һ��@latexonly��ʼ�Ŀ�
        @endmanonly
            ����һ��@manonly��ʼ�Ŀ�
        @endrtfonly
            ����һ��@msc��ʼ�Ŀ�
        @endverbatim
            ����һ��@verbatim��ʼ�Ŀ�
        @endxmlonly
            ����һ��@xmlonly��ʼ�Ŀ�
        @f$
            ��ǹ�ʽ�ı��Ŀ�ʼ�ͽ���
        @f[
            �ڵ�����һ������ʾ�ӳ���ʽ����ʼ���
        @f]
            �ڵ�����һ������ʾ�ӳ���ʽ�Ľ������
        @f{environment}{
            ��һ��ָ����������ʾ��ʽ����ʼ���
        @f}
            ��һ��ָ����������ʾ��ʽ�Ľ������
        @htmlonly [��[block]��]
            ��ʼһ���ı��飬ֻ�ܱ��������������ɵ�HTML�ĵ��С�����@endhtmlonly���������
            �������Ϊdoxygen�������ӵ�HTML����(��applets,java-scripts,html���)��Ҳ����@latexonly,@endlatexonly�����ṩһ�ݺ��ʵ�latex�ĵ���
            ע�⣺��һ��ֻ����HTML�Ŀ��п��Խ�����������(��$(HOME))
        @image [��caption��] [=]
            ���ĵ��в���һ��ͼƬ��ͼƬ�ĸ�ʽ��ָ���������ϣ��������ָ�ʽ��ͼƬ����ô�����Ϊÿ�ָ�ʽ�趨һ�θ����
            ��һ������ָ���������ʽ��Ŀǰֻ֧��html,latex,docbook �� rtf.
            �ڶ�������ָ��ͼƬ�ļ�����doxygen����IMAGE_PATH��Ǻ�ָ����·���в����ļ���������ҵ������Ƶ���ȷ�����Ŀ¼�С����ͼƬ�ļ����а����ո�ʹ���������Ρ�Ҳ����ָ��һ��URL������ļ�������ôdoxygen�����Ḵ�����ͼƬ��������ͼƬ�Ƿ���ڡ�
            ������������ѡ������ָ��ͼƬ����ʾ�ı��⡣��ʹ��û�а����ո�Ҳ������õ�����֮�У��ڱ�����ʾ֮ǰ���Żᱻɾ����
            ���ĸ�����Ҳ��ѡ������ָ��ͼƬ�ĸ߶ȺͿ�ȡ���ֻ��latex�����Ч(��format=latex), sizeindication�ȿ�����ͼƬ�Ŀ��Ҳ������ͼƬ�ĸ߶ȣ��óߴ����latex��ָ��һ����Ч�ĳߴ�(����10cm��6Ӣ�����һ�����ſ��@textwidth)��
            ���磺
              /*! Here is a snapshot of my new application:
               *  \image html application.jpg
               *  \image latex application.eps "My application" width=10cm
               */
            <div class="se-preview-section-delimiter"></div>
            ������һ���ɲ��ҵ��������ļ����������ӣ�
            IMAGE_PATH = my_image_dir
            ���棺HTML����֧�ֵ�ͼƬ��ʽ������������ļ����ԡ�Latex�е�ͼƬ��ʽ������eps(Encapsulated PostScript)��
            Doxygen�޷����ͼƬ��ʽ�Ƿ���ȷ����������Ҫ��ϰȷ�ϡ�
        @latexonly
            ��ʼһ���ı��飬ֻ�ܱ��������������ɵ�latex�ĵ��С�����@endlatexonly���������
            �������Ϊdoxygen�������ӵ�HTML����(��ͼƬ����ʽ�������ַ�)��Ҳ����@htmlonly,@endhtmlonly�����ṩһ�ݺ��ʵ�latex�ĵ���
            ע�⣺��һ��ֻ����latex�Ŀ��п��Խ�����������(��$(HOME))
        @manonly
            ��ʼһ���ı��飬ֻ�ܱ��������������ɵ�MAN�ĵ��С�����@endmanonly���������
            �������ΪMANҳ����ֱ�Ӱ���groff���룬Ҳ����@htmlonly,@endhtmlonly�����@latexonly,@endlatexonly�����ṩһ�ݺ��ʵ�HTML��latex�ĵ���
        @li { item-description }
            ���Ǹ����������һ���հ��л�������@li������������һ��������������������һ���򵥵ģ���Ƕ�׵Ĳ����б�ÿһ��������ʹ��һ��@li���ʼ��
            ע�⣺ʹ��HTML����ɴ���Ƕ���б�
            �ȼ���@arg
        @n
            ����һ�����У��ȼ���<br>���ɱ���ӡ����ʹ�á�
        @p
            ʹ�ô�ӡ������ʾ<word>������ʹ�ø�����������е��ı������ó�Ա������
            �ȼ���@c
        @rtfonly
            ��ʼһ���ı��飬ֻ�ܱ��������������ɵ�RTF�ĵ��С�����@endrtfonly���������
            �������Ϊdoxygen�������ӵ�RFT���롣
            ע�⣺��һ��ֻ����RFT�Ŀ��п��Խ�����������(��$(HOME))
        @verbatim
            ��ʼһ���ܱ�HTML��latex�ĵ������������ı��飬����@endverbatim�����������һ���������в������κ�ע�͡�
            ���棺ȷ��ÿ��@verbatim����Ӧ��һ��@endverbatim�����������������ֳ�ͻ��
        @xmlonly
            ��ʼһ���ܱ�XML�����������ı��飬����@endxmlonly���������
            ������������Զ����XML��ǡ�
        @\
            д��һ����б�ܵ�HTML��latex������У���Ϊdoxygen���ô�б����Ϊ����֮��ķָ��������Դ������������������ԡ�
            @@
            д��һ��at���ŵ�HTML��latex������У���Ϊdoxygen���ô˷�����ΪJavaDoc����֮��ķָ��������Դ������������������ԡ�
            @~[LanguageId]
            ʹ��/ȡ��һ��ָ�������Թ����������ڷ��ò�ͬ���Ե��ĵ���һ��ע�Ϳ��У�ʹ��OUTPUT_LANGUAGE��ǹ��˵�δָ�������ԡ�ʹ��~[LanguageId]����Чһ�������ָ�����ԣ�@~���ʾ��������������Ծ���Ч��(��Ҳ��Ĭ�����õ�)�����ӣ�
            /*! \~english This is English \~dutch Dit is Nederlands \~german Dies ist
                Deutsch. \~ output for all languages.
             */
        @&
            д��һ��&���ŵ�����У���Ϊ�˷�����HTML�������⺯�������Դ������������������ԡ�
        @$
            д��һ��$���ŵ�����У���Ϊ�˷��ſ�������չ�������������Դ������������������ԡ�
        @#
            д��һ��#���ŵ�����У���Ϊ�˷��ſ����������ĵ��������壬���Դ������������������ԡ�
        @<
            д��һ��<���ŵ�����У���Ϊ�˷�����HTML�������⺯�������Դ������������������ԡ�
        @>
            д��һ��>���ŵ�����У���Ϊ�˷�����HTML�������⺯�������Դ������������������ԡ�
        @%
            д��һ��%���ŵ�����У���Ϊ�˷��ſɷ�ֹ�Զ����ӵ�һ���ĵ�����ṹ�У����Դ������������������ԡ�
        @��
            д��һ�������ŵ�����У���Ϊ�˷��ſ�����ָʾһ���޸�ʽ���ı��Σ����Դ������������������ԡ�
            ������һ���ɲ��ҵ��������ļ����������ӣ�
            `IMAGE_PATH = my_image_dir`
            ���棺HTML����֧�ֵ�ͼƬ��ʽ������������ļ����ԡ�Latex�е�ͼƬ��ʽ������eps(Encapsulated PostScript)��
            Doxygen�޷����ͼƬ��ʽ�Ƿ���ȷ����������Ҫ��ϰȷ�ϡ�
        - @latexonly
            ��ʼһ���ı��飬ֻ�ܱ��������������ɵ�latex�ĵ��С�����`@endlatexonly`���������
            �������Ϊdoxygen�������ӵ�HTML����(��ͼƬ����ʽ�������ַ�)��Ҳ����`@htmlonly,@endhtmlonly`�����ṩһ�ݺ��ʵ�latex�ĵ���
            ע�⣺��һ��ֻ����latex�Ŀ��п��Խ�����������(��$(HOME))
        - @manonly
            ��ʼһ���ı��飬ֻ�ܱ��������������ɵ�MAN�ĵ��С�����`@endmanonly`���������
            �������ΪMANҳ����ֱ�Ӱ���groff���룬Ҳ����`@htmlonly,@endhtmlonly`�����`@latexonly,@endlatexonly`�����ṩһ�ݺ��ʵ�HTML��latex�ĵ���
        - @li { item-description }
            ���Ǹ����������һ���հ��л�������`@li`������������һ��������������������һ���򵥵ģ���Ƕ�׵Ĳ����б�ÿһ��������ʹ��һ��`@li`���ʼ��
            ע�⣺ʹ��HTML����ɴ���Ƕ���б�
            �ȼ���`@arg`
        - @n
            ����һ�����У��ȼ���`<br>`���ɱ���ӡ����ʹ�á�
        - @p <word>
            ʹ�ô�ӡ������ʾ`<word>`������ʹ�ø�����������е��ı������ó�Ա������
            �ȼ���`@c`
        - @rtfonly
            ��ʼһ���ı��飬ֻ�ܱ��������������ɵ�RTF�ĵ��С�����`@endrtfonly`���������
            �������Ϊdoxygen�������ӵ�RFT���롣
            ע�⣺��һ��ֻ����RFT�Ŀ��п��Խ�����������(��$(HOME))
        - @verbatim
            ��ʼһ���ܱ�HTML��latex�ĵ������������ı��飬����`@endverbatim`�����������һ���������в������κ�ע�͡�
            ���棺ȷ��ÿ��`@verbatim`����Ӧ��һ��`@endverbatim`�����������������ֳ�ͻ��
        - @xmlonly
            ��ʼһ���ܱ�XML�����������ı��飬����`@endxmlonly`���������
            ������������Զ����XML��ǡ�
        - @\
            д��һ����б�ܵ�HTML��latex������У���Ϊdoxygen���ô�б����Ϊ����֮��ķָ��������Դ������������������ԡ�
        - @@
            д��һ��at���ŵ�HTML��latex������У���Ϊdoxygen���ô˷�����ΪJavaDoc����֮��ķָ��������Դ������������������ԡ�
        - @~[LanguageId]
            ʹ��/ȡ��һ��ָ�������Թ����������ڷ��ò�ͬ���Ե��ĵ���һ��ע�Ϳ��У�ʹ��`OUTPUT_LANGUAGE`��ǹ��˵�δָ�������ԡ�ʹ��~[LanguageId]����Чһ�������ָ�����ԣ�@~���ʾ��������������Ծ���Ч��(��Ҳ��Ĭ�����õ�)�����ӣ�
            ```C++
            /*! \~english This is English \~dutch Dit is Nederlands \~german Dies ist
                Deutsch. \~ output for all languages.
             */
        @&
            д��һ��&���ŵ�����У���Ϊ�˷�����HTML�������⺯�������Դ������������������ԡ�
        @$
            д��һ��$���ŵ�����У���Ϊ�˷��ſ�������չ�������������Դ������������������ԡ�
        @#
            д��һ��#���ŵ�����У���Ϊ�˷��ſ����������ĵ��������壬���Դ������������������ԡ�
        @<
            д��һ��<���ŵ�����У���Ϊ�˷�����HTML�������⺯�������Դ������������������ԡ�
        @>
            д��һ��>���ŵ�����У���Ϊ�˷�����HTML�������⺯�������Դ������������������ԡ�
        @%
            д��һ��%���ŵ�����У���Ϊ�˷��ſɷ�ֹ�Զ����ӵ�һ���ĵ�����ṹ�У����Դ������������������ԡ�
        @��
            д��һ�������ŵ�����У���Ϊ�˷��ſ�����ָʾһ���޸�ʽ���ı��Σ����Դ������������������ԡ�
        @.
            ��������������дһ�����(.)�������һ����������±Ƚ����ã�1.���Ե�JAVADOC_AUTOBRIEF����Ϊ��ʹ�õ�ʱ���ֹ����һ����̵�������2. ���Է�ֹ��ʼһ�����е���һ�����Ҫ����һ�����ֺ���ʱ��
        @::
            ��������������дһ��˫ð��(::)��
        @|
            ��������������дһ���ܵ���(|)�����������ĳЩ�����Ҫ���ܿ�����Ϊ��Ҳ������Markdown���
        @�C
            �������д���������ۺ�(�C)�������������������ۺ�д�����������һ��n-dash�ַ�(-)��
        @��
            �������д�������ۺ�(��)�����������д�������������ۺ����������һ��m-dash�ַ�(-)��