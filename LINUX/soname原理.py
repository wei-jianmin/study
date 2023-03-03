动态库的版本号分别是大版本号，小版好，维护号
大版本号在改变库里的任何已有函数接口时才进行改变，
小版本号是不改变任何函数的接口，只加了几个新的函数，这样前面的程序也能运行，
维护号是修改现有函数的bug时才改变。  

假设有一个动态库：libbar.so.1.1.0，其对应的三个名称如下。
realname：libbar.so.1.1.0  ：真正的动态库
soname：  libbar.so.1      ：软连接
linkname：libbar.so        ：软连接
1. 先生成一个libbar.so，通过-Wl,-soname指定soname为libbar.so.1
   g++ -fPIC -shared -Wl,-soname,libbar.so.1 -o libbar.so.1.1.0
2. 再生成可执行程序，依赖libbar动态库
   gcc main.cpp -L. -lbar -Wl,-rpath='$ORIGIN'   
   此时会用到 linkname:libbar.so 这个文件，否则提示 cannot find -lbar
3. 执行生成的 a.out 程序   
   此时会用到 soname:libbar.so.1 这个文件，否则提示 
   error while loading shared libraries: libbar.so.1: 
   cannot open shared object file: No such file or directory
4. readelf -d a.out，看到 a.out 记录的依赖库为：libbar.so.1 

延伸：
1. gcc根据linkname，找到其指向的动态库，并取其soname，记录在最终生成程序的依赖so列表中
2. ldd时，或可执行文件在执行时，根据记录的soname，找具有与该soname完全相同的文件（上面的第3步）
   即使 libbar.so.1 指向一个 libbarx.so.2.1.1（其soname为libbarx.so.2），
   只要能找到期望的函数符号，程序也能正常执行（此时调用的时 libbarx.so.2.1.1 中的函数），
   所以可以得出结论：libbar.so.1 '应该由程序的使用者确保其指向正确的动态库'
3. 可执行程序使用动态库时，并不像以前以为的那样，自动使用具有高的二级版本号/三级版本号的动态，
   而是可执行程序只是记录/指示了要调用的动态库的soname（soname会具体到一级版本号），
   而最终是要由程序的最终用户去控制该soname链接，指向哪个realname的动态库。
4. 通常动态库自动更新时（如系统动态库自动更新）
   如果一级版本号变了，如 libbar.so.1.1.0 变成 libbar.so.2.1.0 了，
   则不会改变原来 libbar.so.1 的指向（仍指向 libbar.so.1.1.0），
   而是创建新的链接 libbar.so.2（soname）指向 libbar.so.2.1.0 ，
   而如果只是二级版本号或三级版本号变动，如 libbar.so.1.1.0 变成 libbar.so.1.2.0 了，
   则会修改原来 libbar.so.1 的指向，改为指向 libbar.so.1.2.0 ，
   在这种规则下，系统中原来使用 soname=libbar.so.1 的程序，其运行不会受到影响。
   