��һ��
    ��3�� �����﷨
        Java���ִ�Сд��ÿ�����ӱ����÷ֺŽ�����
        main����
            ���п��԰���main������main�����Ĳ���Ϊ Strings[] args
            ÿ������ǰ��� public �ؼ��֣�main����ǰ�滹Ӧ�ô� static �ؼ���
            ����ֵΪ void����������˳�����javaӦ�ó��򷵻�0��
            ���ϣ����ֹʱ�����������룬��Ӧ����System.exit()����
        �ඨ�壺
            �����������淶Ϊ���շ�������
            Դ�����ļ������֣��빫�����������ͬ������.java��Ϊ��չ����
            ����ǰ����public�ؼ��֣���Ľ��������ź�������� ; ��Ϊ������
            ����������ͨ��java�������г���ʱ�����������������������class�ļ���
        ע�ͣ�
            ����ע�ͣ�//
            ����ע�ͣ�/*   */
            �ĵ�ע�ͣ�/**  */
                ����ע�ͷ����������Զ������ĵ�
        �������ͣ�
            ���ͣ�byte(1�ֽ�) short(2�ֽ�) int(4�ֽ�) long(8�ֽ�) 
            ���㣺float(4�ֽ�) double(8�ֽ�)
            ��ֵ��������ǰ׺ΪL��l��ʮ������ǰ׺Ϊ0x��0X��
                  �˽���ǰ׺Ϊ0��������ʹ��8����������������ǰ׺Ϊ0b��0B
                  ��ֵ֧��ʹ���»��߷ָ�����ʹ��ֵ�׶�����������ȥ����Щ�»���
                  float���к�׺F��f��double��׺ΪD��d������Ĭ��Ϊdouble
                  NaN ����������/������󣬷�0ֵ��0�Ľ��������󣬶�������ƽ���Ľ���� NaN
                  ���߷ֱ��ʾΪ��Double.POSITIVE_INFINITY, Double.NEGTIVE_INFINITY, Double.NaN
                  ����ͨ�� if(x==Double.NaN) �жϣ���Ӧͨ�� if(Double.isNan(x)) �ж�
            �ַ���char����ռ2���ֽ�
                ���˿ɸ�ֵ' '��ʾ���ַ������⣬
                ���ɸ�ֵʮ������������ \u �� \U ��ͷ����Χ�� \u0000 �� \uffff
                ע�⣬\u�����ܱ����ͨ�ַ��⣬���ܱ��ת���ַ���
                �� \u000a ��ͬ�� \n�� " ��ͬ�� \u0022
                ���� "\u0022+\u0022" ��ͬ�� "" + ""�������� "\" + \""
                �ر�ģ��� //c:\users\administrator �ᱨ��
                ��Ϊ \u ����û�и���4��ʮ��������
            ������boolean
                �� C �У���ֵ�Ƿ�Ϊ0��ָ���Ƿ�Ϊ�տ���Ϊ�����ж����ݣ���java�в�����
            �������ڱ�������ǰ�ӹؼ��� finial ָʾ����
                finialָʾ�������ֻ�ܱ���ֵ1�Σ�c�����õ���const�ؼ��֣�
        �������
            ͬ C ����
        ����ת����
            ͬ C ���ԣ��� double a=3.2; int b = (int) a;
        ��λ���㣺
            ��C��ȣ�������>>>����0����λ����>>�����÷���λ����λ
            C/C++�У�>>��ʵ�ַ�ʽû�й涨������ʵ���߿���ʹ��������λ����չ����λ��
            ����ʹ���߼���λ����λ���0����Ҳ����˵��C/C++��>>��λ��������ھ���ʵ��
        ö�٣�
            enum Size { SMALL, MEDIUM, LARGE };
            Size s = Size.SMALL;
        �ַ�����
            javaͨ��String�����������ַ���
            ������c++��string�࣬java��String�಻֧�ֱ������޸�
            java�е����ֳ����أ�
                https://cloud.tencent.com/developer/article/1450501
                JVM��������Ҫ��ΪClass�ļ������ء�����ʱ�����أ�ȫ���ַ��������أ��������Ͱ�װ���������
                Class�ļ�������
                    �� javap -v class�ļ����ɲ鿴class�ļ��ĳ���������
                    class�ļ���������Ҫ������������������ͷ�������
                    1) ������
                        �� �ı��ַ������� String s = "abc";�е�"abc"
                        �� ��final���εĳ�Ա������������̬������ʵ�������;ֲ�����
                    2) ��������
                        ����������Ҫ���漰����ԭ����ĸ�������������ೣ��:
                        �� ��ͽӿڵ�ȫ�޶�����Ҳ����java/lang/String
                        �� �ֶε����ƺ����������ֶ�Ҳ��������߽ӿ��������ı����������༶�������ʵ�����ı���
                        �� �����е����ƺ���������Ҳ����������+����ֵ
                ����ʱ������
                    ����ʱ�������Ƿ�������һ���֣�����Ҳ��ȫ�ֹ��׵�
                    jvm��ִ��ĳ�����ʱ�򣬱��뾭�����ء����ӣ���֤��׼��������������ʼ����
                    ��������ͨ�����ǲ�ͬ�ģ�
                    �������������ص�ʱ����ɵģ���jvm�����Ĳ����ǵ����ģ���Ϊ��������罻������ڣ�
                    ����ͨ�Ķ���һ�����ڵ���new֮�󴴽���
                    �����ʱ���Ѳ�ͬ��class�ೣ���ؼ��ص�����ʱ�����أ���ͬ���๲��һ������ʱ������
                    ��ͬclass�ļ��������е���ͬ���ַ����ᱻ�Ż�Ϊһ��
                    ����Ľ����׶Σ�����ѷ������÷���Ϊ������ʱ��������ֵ������
                ȫ���ַ���������
                    ȫ���ַ�����������������������ɣ�������֤��׼���׶�֮���ڶ��������ַ�������ʵ����
                    Ȼ�󽫸��ַ�������ʵ��������ֵ�浽string pool�У�ʵ�ʵĶ���ʵ�����Ǵ��ڶ���
                    Java�д����ַ�����������ַ�ʽ�� String s0 = "hello", s1 = new String("hello");
                    ��1�ַ����е�"hello"ֵ�����ڱ����ھ��Ѿ�ȷ���ģ�����ֱ�ӽ���class�ļ��������У�
                    �����������ַ������󴴽���ʽ���������֣������ڶ��ϴ���һ��"hello"����
                    �ڴ���s0�����ʱ�򣬻���Ѹö�������ô�ŵ�ȫ���ַ����������У�
                    ���������������� String s2 = "hello" �����ľ���ʱ��
                    ���������ȥ�ַ����������Ƿ���equals("hello")��String�������ã�
                    ����У��Ͱ����ַ�������"Hello"�����ø��Ƹ�s2�������ͱ������µĶ���Ĵ���
                    ������s1������Ϊ������new�ؼ��֣�����һ�����ڶ��д���һ���¶���
                    ��ȫ���ַ��������ص����þ���Ϊ�˼��ٶ���Ĵ��������ڵģ�
                    ������s1���������ᴴ������ģ���û��Ҫ�������ô����ȫ���ַ����������е�
            String��ĳ�Ա������50�������
                + : ƴ���ַ���
                substring(��ʼλ�ã�����λ��)����ȡ���ַ���
                join(�ָ������ַ���1��...,�ַ���n) : ƴ�Ӷ���ַ�������ָ���ָ���
                char charAt(int index)������ָ��λ�õĴ��뵥Ԫ
                int codePointAt(int index)������ָ��λ�õ����
                int compareTo(String other): �ַ����Ƚϴ�С
                IntStream codePoints()�������ַ����������Ϊһ��������
                new String(int[] codePoints��int offset,int count)���������д�offset��ʼ��count����㹹��һ���ַ���
                boolean equals(Object other) : �ж��ַ����Ƿ����
                boolean equalsIgnoreCase(String other)���ж��ַ����Ƿ���ȣ����Դ�Сд
                boolean startsWith(String prefix)
                boolean endsWith(string suffix)
                int indexOf(String str, int fromIndex=0)
                int indexOf(int cp, int fromIndex) : cp��ʶ��㣨0ƽ��������ڴ��뵥Ԫ��
                int lastindexOf(int cp)
                int lastindexOf(int cp, int formIndex)
                int length()
                int codePointCount(int startIndex,int ednIndex) : ���������������û����Գɹ���Ҳ����������
                String replace(CharSequence oldString, CharSequence newString) : �滻���ַ���������һ�����ַ�������
                String substring(int beginIndex) : ��ȡ���ַ���������һ�����ַ�������
                String substring(int beginIndex, int endIndex): ��ȡ���ַ���������һ�����ַ�������
                String toLowerCase()
                String toUpperCase()
                String trim() : ɾ��ͷ����β���Ŀո񣬷���һ�����ַ�������
                String join(CharSequence delimiter, CharSequence... elements): �ö������������Ԫ��
            �����ַ����Ƿ���ȣ�
                Ӧ��ʹ��String��equals()������equalsIgnortCase()����
                ==�����ж����������Ƿ���ȣ����õ�ͬһ������
            �մ���Null����
                �մ�""�ǳ���Ϊ0���ַ���, �� if(str.length()==0) �� if(str.equals("")) �ж�
                String���������Դ��һ�������ֵ:null���жϷ���Ϊ�� if(str == null)
                ��ʱҪ��������������ͬʱ�жϣ����ܱ�֤���ַ���������Ч�Ҳ�Ϊ�գ�
                if(str!=null && str.length()>0)
            ���ʹ��뵥Ԫ��
                ��㣨��λ���ʹ��뵥Ԫ����Ԫ�� ��
                    ��������ĳ���ַ���Ӧ����ֵ����Unicode��׼�У����ı�ʶ������ U+ Ϊǰ׺
                    ��Ϊ2���ֽ��޷����ȫ�������е��ַ������֣����Խ�����Ϊ��17��������
                    ��0����(/ƽ��)���ķ�Χ��U+0000 ~ U+FFFF�����Ǿ���� Unicode ����
                    ��1����(/ƽ��)���ķ�Χ��U+10000 ~ U+1FFFF
                    ��2����(/ƽ��)���ķ�Χ��U+20000 ~ U+2FFFF
                    ������
                    ��16����(/ƽ��)���ķ�Χ��U+100000 ~ U+10FFFF
                    ���м���(/ƽ��)���ķ�Χ��U+0000 ~ U+10FFFF
                    ����һ����㣬Ҳ����2���ֽڣ�1�����뵥Ԫ����Ҳ������4���ֽڣ�2�����뵥Ԫ��
                ����λ�õ���Ԫ��
                    ���ȣ�Unicode�涨���ڵ�0ƽ�棨BMPƽ�棩��U+D800 ~ U+DFFF��Χ�ڵ�ֵ����Ӧ�κ��ַ�
                    ������1ƽ��~��16ƽ�����㷶Χ�ǣ�U+1000 ~ U+10FFFF,
                    �������Χֵ��ȥ 0x1000 �󣬷�Χ��Ϊ�� U+0000 ~ U+0FFFFF, ��Ҫ�� 20bit ���ܴ���
                    Ҳ����˵����Ҫ2��˫�ֽڣ�2�����뵥Ԫ�����ܴ��£�һ��˫�ֽ�16bit��
                    ���ǿ��Խ��� 20bit ��Ϊ�ߵ� 2 �� 10bit��10bit�ķ�Χ 0x0 ~ 0x3FF��
                    ��ÿ�����뵥Ԫ�棨��16bit���ĵ�10bit�������Щ��ֵ��
                    Ϊ����0ƽ�����λ�������֣����ǻ�ҪΪ��2�����뵥Ԫָ��ǰ׺��
                    ��Ϊǰ��˵�ˣ��ڵ�0ƽ��ģ�U+D800 ~ U+DFFF��Χ�ڵ�ֵ����Ӧ�κ��ַ�
                    �������ǽ��� 10bit ���� U+D800��0B1101_1000_0000_0000���õ���
                    0B1101_1000_0000_0000 ~ 0B1101_1011_1111_1111���� 0XD800 ~ 0XDBFF
                    �ٽ��� 10bit ���� U+DC00��0B1101_1100_0000_0000���õ���
                    0B1101_1100_0000_0000 ~ 0B1101_1111_1111_1111���� 0XDC00 ~ 0XDFFF
                    ���ԣ����ǿ����жϣ�
                    ���һ����Ԫ��2�ֽڣ����� 0XD800 ~ 0XDBFF ֮�䣨��6λ�� 1101_10����
                    �������Ԫ���˷�0ƽ����λ�ĸ� 10bit
                    ���һ����Ԫ��2�ֽڣ����� 0XDC00 ~ 0XDFFF ֮�䣨��6λ�� 1101_11����
                    �������Ԫ���˷�0ƽ����λ�ĵ� 10bit
                    ���һ����Ԫ��2�ֽڣ�û������ 0XD800 ~ 0XDFFF ֮�䣨��5λ���� 1101_1����
                    �������Ԫ�Ǹ�0ƽ�����ֵ
            StringBuilder �� StringBuffer��
                 �����ַ��������޸ĵ�ʱ����Ҫʹ�� StringBuffer �� StringBuilder �ࡣ
                 �� String �಻ͬ���ǣ�StringBuffer �� StringBuilder ��Ķ����ܹ�����ε��޸ģ����Ҳ������µ�δʹ�ö���
                 ��ʹ�� StringBuffer ��ʱ��ÿ�ζ���� StringBuffer ��������в����������������µĶ���
                 ���������Ҫ���ַ��������޸��Ƽ�ʹ�� StringBuffer��
                 StringBuilder ���� Java 5 �б���������� StringBuffer ֮������ͬ���� 
                 StringBuilder �ķ��������̰߳�ȫ�ģ�����ͬ�����ʣ�
                 ���� StringBuilder ����� StringBuffer ���ٶ����ƣ����Զ�������½���ʹ�� StringBuilder ��
                 StringBuffer ����
                    1	StringBuffer append(String s)                   ��ָ�����ַ���׷�ӵ����ַ����С�
                    2	StringBuffer reverse()                          �����ַ��������䷴ת��ʽȡ����
                    3	publicelete(int start, int end)                 �Ƴ������е����ַ����е��ַ���
                    4	insert(int offset, int i)                       �� int �������ַ�����ʾ��ʽ����������С�
                    5	insert(int offset, String str)                  �� str �������ַ�������������С�
                    6	replace(int start, int end, String str)         ʹ�ø��� String �е��ַ��滻�����е����ַ����е��ַ�
                    7	int lastIndexOf(String str)                     �������ұ߳��ֵ�ָ�����ַ����ڴ��ַ����е�������
                    8	int lastIndexOf(String str, int fromIndex)      ���� String ���������ַ��������ֵ�λ�á�
                    9	int length()                                    ���س��ȣ��ַ�������
                    10	void setCharAt(int index, char ch)              ���������������ַ�����Ϊ ch��
                    11	void setLength(int newLength)                   �����ַ����еĳ��ȡ�
                    12	CharSequence subSequence(int start, int end)    ����һ���µ��ַ����У����ַ������Ǵ����е������С�
                    13	String substring(int start)                     ����һ���µ� String�����������ַ����е�ǰ���������ַ������С�
                    14	String substring(int start, int end)            ����һ���µ� String�������������е�ǰ���������ַ������С�
                    15	String toString()                               ���ش����������ݵ��ַ�����ʾ��ʽ
                    17	int capacity()                                  ���ص�ǰ������
                    18	char charAt(int index)                          ���ش�������ָ���������� char ֵ��
                    19	void ensureCapacity(int minimumCapacity)        ȷ���������ٵ���ָ������Сֵ��
                    20	void getChars(int srcBegin, int srcEnd, char[] dst, int dstBegin)   ���ַ��Ӵ����и��Ƶ�Ŀ���ַ����� dst��
                    21	int indexOf(String str)                         ���ص�һ�γ��ֵ�ָ�����ַ����ڸ��ַ����е�������
                    22	int indexOf(String str, int fromIndex)          ��ָ������������ʼ�����ص�һ�γ��ֵ�ָ�����ַ����ڸ��ַ����е�������
        ���������
            ��ӡ������� ��׼���������������̨���ڣ�ֻҪ���� System.out.println ����    
            Ȼ������ȡ�� ��׼�������� System.in ��û����ô����
            Ҫ��ͨ������̨�������ˣ�������Ҫ����һ�� Scanner ���󣬲��롰 ��׼�������� System.in ���� 
            Scanner in = new Scanner(System.in);
            �Ϳ���ʹ�� Scanner ��ĸ��ַ���ʵ�����������
            ���磬 nextLine() ����������һ�С�next()��ȡһ�����ʣ��Կհ�Ϊ�ָ�������
            nextInt()��ȡһ��������nextDouble()��ȡһ��������
            ����ڳ�����ʼ�����һ��  import java.util.*;  //Scanner �ඨ����java.util ����
            ��ʹ�õ��಻�Ƕ����ڻ���java.lang ����ʱ�� һ��Ҫʹ�� import ָʾ�ֽ���Ӧ�İ����ؽ���
            �ӿ���̨��ȡ����
                ��Ϊ�����ǿɼ��ģ� ���� Scanner �಻�����ڴӿ���̨��ȡ����
                Java SE 6 �ر������� Console ��ʵ�����Ŀ�ģ�
                Console cons = System.console();
                String username = cons.readLine("User name: ")��
                char [] passwd = cons.readPassword("Password: ");
                ���� Console ���������벻����� Scanner ���㡣ÿ��ֻ�ܶ�ȡһ�����룬 
                ��û���ܹ���ȡһ�����ʻ�һ����ֵ�ķ���
            Scanner���ṩ�ķ���
                ? Scanner (InputStream in)  �ø���������������һ�� Scanner ����
                ? String nextLine( )        ��ȡ�������һ�����ݡ�
                ? String next( )            ��ȡ�������һ�����ʣ��Կո���Ϊ�ָ���)��
                ? int nextlnt( )
                ? double nextDouble( )      ��ȡ��ת����һ����ʾ�����򸡵������ַ����С�
                ? boolean hasNext( )        ����������Ƿ����������ʡ�
                ? boolean hasNextInt( )
                ? boolean hasNextDouble( )  ����Ƿ��б�ʾ�����򸡵�������һ���ַ����С�
            ��ʽ�����
                ����ʹ�� SyStem.0Ut.print(x) ����ֵ x ���������̨��
                ��������� x ��Ӧ���������͵����з�0����λ����ӡ��� X ����ζ������С��λ�����ӡ������
                Java SE 5.0 ������ C ���Կ⺯���е� printf�������� System.out.printf("%,.2f",10/3.0);
                ע������ʹ�� %s ת������ʽ������Ķ���
                    ��������ʵ���� Formattable �ӿڵĶ��󶼽����� formatTo ����
                    ���򽫵��� toString ������ �����Խ�����ת��Ϊ�ַ���
                ����ʹ�þ�̬�� String.format ��������һ����ʽ�����ַ�����
                String message = String.format("Hello, %s. Next year , you'll be %d", name, age) ;
                ����ʱ��ĸ�ʽ������
                    �ھɵĴ����У�ʹ���� Date() �࣬���´����У�Ӧ��ʹ�� java.time ���еķ�������II���6�»���ܣ�
                    System.out.printfC("%l$s %2$tB %2$te, %2$tY", "Due date:", new DateQ)�� //��ʽ���Ʋα����59ҳ
            �ļ����������
                Ҫ����ļ����ж�ȡ�� ����Ҫһ���� File ������һ�� Scanner ����
                Scanner in = new Scanner(Paths.get("niyflle.txt") , "UTF-8") ;
                ���ʡ���ַ����룬 ���ʹ��������� Java ����Ļ����ġ� Ĭ�ϱ��롱�����ܻ���Ӱ�죩
                ���ڣ��Ϳ�������ǰ����ܵ��κ�һ�� Scanner �������ļ����ж�ȡ
                Ҫ��д���ļ��� ����Ҫ����һ�� PrintWriter ����
                PrintWriter out = new PrintWriter("myfile.txt", "UTF-8") ;
                ����ļ������ڣ��������ļ���
                ����������� System.out����ʹ�� print�� println �Լ� printf���
                ���棺Scanner��֧���ַ�����Ϊ���������������ַ������ж�ȡ
                    �� Scanner in = new Scanner("c:/myfile.txt"); 
                    �Ⲣ���Ǵ�һ���ļ����ж�ȡ�����Ƕ�ȡ����ַ���
                ���ʹ�ü��ɿ��������� ��ô����·������ IDE ���ƣ����Ӱ��������·�����ļ���
                ����ʹ�����ַ�����ȡ��ǰ·����String dir = System.getProperty("user.dir"):
                �����һ�������ڵ��ļ�����һ�� Scanner, 
                ������һ�����ܱ��������ļ�������һ�� PrintWriter,��ô�ͻᷢ���쳣
        ���̿��ƣ�
            ������
                Java �Ŀ������̽ṹ�� C �� C++ �Ŀ������̽ṹһ���� ֻ�к��ٵ��������
                û�� goto ��䣬 �� break �����Դ���ǩ�� ����������ʵ�ִ��ڲ�ѭ��������Ŀ��
                ���⣬����һ�ֱ��ε� for ѭ���� �� C �� C++ ��û������ѭ���� 
                ���е������� C Sharp �е� foreach ѭ��
            ��c++����
                ��������
                    �� C++ �У� ������Ƕ�׵Ŀ����ض���һ�����������ڲ㶨��ı����Ḳ������㶨��ı�����
                    ������ �п��ܻᵼ�³�����ƴ��� ����� Java �в�����������
                �� Java SE 7 ��ʼ�� case ��ǩ���������ַ������������磺
                    String s = ...��
                    switch (s.toLowerCase())
                    {
                        case "yes":
                            ...
                            break;
                        ...
                    }
                java�в�֧��goto����֧�ִ���ת��ǩ��break���磺
                    ...
                    mark:
                    while(...)
                    {
                        ...
                        for(...)
                        {
                            ...
                            break mark;
                            ...
                        }
                    }
                    ...
                    ע��continue���Ҳ֧����ת��ǩ��break��ת���Ҳ���Գ�����if�����
                forö�٣�
                    for (variable : collection) statement
                    collection ��һ���ϱ��ʽ������һ�����������һ��ʵ���� Iterable �ӿڵ������
                    �磺 for(int element:arr) System.out.println(element);
        ����ֵ
            ��������������͸��������Ȳ��ܹ��������� ��ô����ʹ��jaVa.math ���е�����
            �����õ��ࣺBiglnteger �� BigDecimaL ����������Դ���������ⳤ���������е���ֵ��
            Biglnteger ��ʵ�������⾫�ȵ��������㣬 BigDecimal ʵ�������⾫�ȵĸ��������㡣
            ʹ�þ�̬�� valueOf �������Խ���ͨ����ֵת��Ϊ����ֵ��
            Biglnteger a = Biglnteger.valueOf(100);
            ����ʹ��������Ϥ��������������磺+ �� *) �������ֵ��
            ��Ӧʹ�ô���ֵ���ṩ��add��multiply����
            ע���� C++ ��ͬ�� Java û���ṩ��������ع��ܣ�����Ա�޷��ض��� + �� * �����
            Biglnteger��Ա������
                ? Biglnteger add(Biglnteger other)
                ? Biglnteger subtract(Biglnteger other)
                ? Biglnteger multipiy(Biginteger other)
                ? Biglnteger divide(Biglnteger other)
                ? Biglnteger mod(Biglnteger other)
                  �����������������һ�������� other �ĺ͡� � ���� ���Լ�������
                ? int compareTo(Biglnteger other)
                  ����������������һ�������� other ��ȣ� ���� 0; 
                  ������������С����һ�������� other, ���ظ����� ���� ����������
                ? static Biglnteger valueOf(1ong x) ����ֵ���� x �Ĵ�����
            BigDecimal��Ա������
                ? BigDecimal add(BigDecimal other)
                ? BigDecimal subtract(BigDecimal other)
                ? BigDecimal multipiy(BigDecimal other)
                ? BigDecimal divide(BigDecimal other RoundingMode mode) 5.0
                  ���������ʵ������һ����ʵ�� other �ĺ͡� � ���� �̡�
                  Ҫ������̣� ����������뷽ʽ �� rounding mode��) 
                  RoundingMode.HALF UP ����ѧУ��ѧϰ���������뷽ʽ
                  �������ڳ���ļ��㡣�й����������뷽ʽ��ο� Apr�ĵ���
                ? int compareTo(BigDecimal other)
                  ��������ʵ������һ����ʵ����ȣ� ���� 0 ; 
                  Ҫ������̣� ��������᷵�ظ����� ���򣬷���������
                ? static BigDecimal valueOf(1 ong x)
                ? static BigDecimal valueOf(1 ong x ,int scale)
                  ����ֵΪ X �� x / 10^scale ��һ����ʵ����
        ����
            ����������
                ����������ʽ������int[] a;  
                ������ ����ֻ�����˱��� a�� ��û�н� a ��ʼ��Ϊһ������������
                ��ʹ�� new ������������飺int[] a = new int[len];
                ava�У����������������ͣ�����������ֻ������������ռ䣬
                ����c++��ͬ��c++�У�int a[100]; ͬʱ����˶���ͷ���ռ�Ĺ���
                ����һ����������ʱ�� ����Ԫ�ض���ʼ��Ϊ 0��boolean �����Ԫ�ػ��ʼ��Ϊ false 
                ���������Ԫ�����ʼ��Ϊһ������ֵ null, ���ʾ��ЩԪ�أ�����δ����κζ���
                �磺String[] names = new String[10] ;
                �ᴴ��һ������ 10 ���ַ��������飬 �����ַ�����Ϊnull
                ��C++��ͬ��һ���ǣ��������������֧�ַ���length���ԣ��� a.length
                ��������ʱ��ʼ��������int[] small Primes = new int[] { 2, 3, 5, 7, 11, 13 };
                �����������ü���ʽ��int[] small Primes = { 2, 3, 5, 7, 11, 13 }; 
                ��c++�����һ���ǣ�����a����ָ�룬����ͨ��a+1�õ��������һ��Ԫ��
            ���鿽����
                �� Java �У� ����һ�����������������һ�����飬�磺int[] luckyNumbers = smallPrimes;
                ���ϣ����һ�����������ֵ������һ���µ������У�Ӧ�ý���Array���copyOf������
                int[] luckyNumbers = Arrays.copyOf(smallPrimes, luckyNumbers.length) ;
            �����в������飺
                public static void main(String[] args)
                ��c++��ͬ���ǣ�args[0]���ǳ����������������д����ĵ�һ������
            ��������
                ������Array.sort(����) �������������ʹ�õ��ǿ������򷨣�
            java,util.Arrays�ṩ�ķ�����
                ? static String toString(type[] a) 
                  ���ذ��� a ������Ԫ�ص��ַ����� ��Щ����Ԫ�ر����������ڣ� ���ö��ŷָ���
                  ������ a ����Ϊ int��long��short��char�� byte��boolean��float �� double �����顣
                ? static type copyOf(type[] a, int length)
                ? static type copyOfRange(type[] a , int start , int end)
                  ������ a ������ͬ��һ�����飬 �䳤��Ϊ length ���� end-start�� ����Ԫ��Ϊ a ��ֵ��
                  ������ a ����Ϊ int�� long��short��char��byte��boolean��float �� double �����顣
                  start  ��ʼ�±꣨�������ֵ��0��
                  end    ��ֹ�±꣨���������ֵ���� ���ֵ���ܴ��� a.length����ʱ�����Ϊ 0 �� false��
                  length ����������Ԫ�س��ȡ���� length ֵ���� a.length�� ���Ϊ 0 �� false ;
                         ���� ������ֻ��ǰ�� length ������Ԫ�صĿ� W ֵ��
                ? static void sort(t y p e [ 2 a)
                  �����Ż��Ŀ��������㷨�������������
                  ������a ����Ϊ int��long��short��char��byte��boolean��float �� double �����顣
                ? static int binarySearch(type[] a , type v)
                ? static int binarySearch(type[] a, int start, int end , type v) 
                  ���ö��������㷨����ֵ v��������ҳɹ��� �򷵻���Ӧ���±�ֵ�� 
                  ���򷵻�һ������ֵr�� -r-1 ��Ϊ���� a ���� v Ӧ�����λ�á�
                  ������ 
                  a     ����Ϊ int�� long�� short�� char�� byte�� boolean �� float �� double ���������顣
                  start ��ʼ�±꣨�������ֵ����
                  end   ��ֹ�±꣨���������ֵ��)
                  v     ͬ a ������Ԫ��������ͬ��ֵ��
                ? static void fi11(type[] a , type v)
                  ���������������Ԫ��ֵ����Ϊ v��
                  ������ 
                  a     ����Ϊ int�� long��short��char��byte��boolean �� float �� double �����顣
                  v     �� a ����Ԫ��������ͬ��һ��ֵ��
                ? static boolean equals(type[] a, type[] b)
                  ������������С��ͬ�� �����±���ͬ��Ԫ�ض���Ӧ��ȣ� ���� true��
                  ������ a�� b ����Ϊ int��long��short��char��byte��boolean��float �� double ���������顣
            ��ά����
                double[] [] balances;
                double[] [] balances = new double[NYEARS] [NRATES]
                int[][] magicSquare = { {16, 3, 2, 13}��{5, 10, 11, 8},(9, 6, 7, 12},{4, 15, 14, 1} }��
                ע forö�ٲ���һ����ö�ٶ�ά�����ÿһ��Ԫ�أ���Ӧ��һ��2��ѭ��ö��һ����ά����
                ������Arrays.deepToString(����)������������תΪһ���ַ���
            ����������
                javaʵ����û�ж�ά���飬ֻ��һά���飬��ά���鱻����Ϊ"���������"��
                ���ά���飬����һ��һά������󣬸������ÿ��Ԫ���ֶ���һ��һά���������
                ���ԣ����Է���Ľ������balances��ά��������н��н�����
                    double[] temp = balances[i]:
                    balances[i] = balances[i + 1];
                    balances[i + 1] = temp;
                �����Թ���һ�����������飬�������ÿһ�ж��в�ͬ�ĳ��ȣ�
                    int [][] odds = new int [MAX] [] ;  //����MAX��һά���飬ÿ��Ԫ���ֶ���int[]����
                    for (int n = 0; n < MAX ; n++)
                        odds[n] = new int [n + 1] ;
    ��4�� �������