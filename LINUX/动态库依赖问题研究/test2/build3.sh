echo "阅读器链接log1静态库，oes隐式调用log2共享库，阅读器显式调用oes共享库"
rm *.a
rm *.o
rm *.so
rm *.bin
#gcc -fPIC -shared log1.cpp -o liblog1.so
#gcc -fPIC -shared log2.cpp -o liblog2.so
#gcc -shared log1.cpp -o liblog1.so
gcc -c log1.cpp -o log1.o
ar -rc liblog1.a log1.o
gcc -shared log2.cpp -o liblog2.so
#gcc -fPIC -shared oes.cpp -o liboes.so -L. -llog2 -Wl,-rpath='$ORIGIN'
gcc -shared oes.cpp -o liboes.so -L. -llog2 -Wl,-rpath='$ORIGIN'
gcc reader.cpp -o reader.bin -ldl -L. -llog1 -Wl,-rpath='$ORIGIN'
chmod a+x reader.bin
