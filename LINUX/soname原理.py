��̬��İ汾�ŷֱ��Ǵ�汾�ţ�С��ã�ά����
��汾���ڸı������κ����к����ӿ�ʱ�Ž��иı䣬
С�汾���ǲ��ı��κκ����Ľӿڣ�ֻ���˼����µĺ���������ǰ��ĳ���Ҳ�����У�
ά�������޸����к�����bugʱ�Ÿı䡣  

������һ����̬�⣺libbar.so.1.1.0�����Ӧ�������������¡�
realname��libbar.so.1.1.0  �������Ķ�̬��
soname��  libbar.so.1      ��������
linkname��libbar.so        ��������
1. ������һ��libbar.so��ͨ��-Wl,-sonameָ��sonameΪlibbar.so.1
   g++ -fPIC -shared -Wl,-soname,libbar.so.1 -o libbar.so.1.1.0
2. �����ɿ�ִ�г�������libbar��̬��
   gcc main.cpp -L. -lbar -Wl,-rpath='$ORIGIN'   
   ��ʱ���õ� linkname:libbar.so ����ļ���������ʾ cannot find -lbar
3. ִ�����ɵ� a.out ����   
   ��ʱ���õ� soname:libbar.so.1 ����ļ���������ʾ 
   error while loading shared libraries: libbar.so.1: 
   cannot open shared object file: No such file or directory
4. readelf -d a.out������ a.out ��¼��������Ϊ��libbar.so.1 

���죺
1. gcc����linkname���ҵ���ָ��Ķ�̬�⣬��ȡ��soname����¼���������ɳ��������so�б���
2. lddʱ�����ִ���ļ���ִ��ʱ�����ݼ�¼��soname���Ҿ������soname��ȫ��ͬ���ļ�������ĵ�3����
   ��ʹ libbar.so.1 ָ��һ�� libbarx.so.2.1.1����sonameΪlibbarx.so.2����
   ֻҪ���ҵ������ĺ������ţ�����Ҳ������ִ�У���ʱ���õ�ʱ libbarx.so.2.1.1 �еĺ�������
   ���Կ��Եó����ۣ�libbar.so.1 'Ӧ���ɳ����ʹ����ȷ����ָ����ȷ�Ķ�̬��'
3. ��ִ�г���ʹ�ö�̬��ʱ����������ǰ��Ϊ���������Զ�ʹ�þ��иߵĶ����汾��/�����汾�ŵĶ�̬��
   ���ǿ�ִ�г���ֻ�Ǽ�¼/ָʾ��Ҫ���õĶ�̬���soname��soname����嵽һ���汾�ţ���
   ��������Ҫ�ɳ���������û�ȥ���Ƹ�soname���ӣ�ָ���ĸ�realname�Ķ�̬�⡣
4. ͨ����̬���Զ�����ʱ����ϵͳ��̬���Զ����£�
   ���һ���汾�ű��ˣ��� libbar.so.1.1.0 ��� libbar.so.2.1.0 �ˣ�
   �򲻻�ı�ԭ�� libbar.so.1 ��ָ����ָ�� libbar.so.1.1.0����
   ���Ǵ����µ����� libbar.so.2��soname��ָ�� libbar.so.2.1.0 ��
   �����ֻ�Ƕ����汾�Ż������汾�ű䶯���� libbar.so.1.1.0 ��� libbar.so.1.2.0 �ˣ�
   ����޸�ԭ�� libbar.so.1 ��ָ�򣬸�Ϊָ�� libbar.so.1.2.0 ��
   �����ֹ����£�ϵͳ��ԭ��ʹ�� soname=libbar.so.1 �ĳ��������в����ܵ�Ӱ�졣
   