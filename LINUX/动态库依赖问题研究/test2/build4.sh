echo "oes链接log2静态库，阅读器隐式调用log1共享库，阅读器显式调用oes共享库"
rm *.a
rm *.o
rm *.so
rm *.bin
#gcc -fPIC -shared log1.cpp -o liblog1.so
#gcc -fPIC -shared log2.cpp -o liblog2.so
gcc -shared log1.cpp -o liblog1.so
gcc -c log2.cpp -o log2.o
ar -rc liblog2.a log2.o
#gcc -shared log2.cpp -o liblog2.so
#gcc -fPIC -shared oes.cpp -o liboes.so -L. -llog2 -Wl,-rpath='$ORIGIN'
gcc -shared oes.cpp -o liboes.so -L. -llog2 -Wl,-rpath='$ORIGIN'
gcc reader.cpp -o reader.bin -ldl -L. -llog1 -Wl,-rpath='$ORIGIN'
chmod a+x reader.bin
