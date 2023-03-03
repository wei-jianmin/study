echo "oes链接静态库log2，阅读器链接静态log1,阅读器显示调用oes共享库"
rm *.a
rm *.o
rm *.so
rm *.bin
#gcc -fPIC -shared log1.cpp -o liblog1.so
#gcc -fPIC -shared log2.cpp -o liblog2.so
gcc -c log1.cpp -o log1.o
ar -rc liblog1.a log1.o
gcc -c log2.cpp -o log2.o
ar -rc liblog2.a log2.o
gcc -fPIC -shared oes.cpp -o liboes.so -L"." -llog2 
gcc reader.cpp -o reader.bin -ldl -L"." -llog1 
chmod a+x reader.bin
