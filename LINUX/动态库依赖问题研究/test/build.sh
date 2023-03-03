#! /bin/bash
if [ $1 = suwell ]
then
    g++ suwell.cpp -O0 -g -ldl -o suwell.bin
elif [ $1 = oes ]
then
g++ oes.cpp -O0 -g -fPIC -shared -ldl -o oes.so
elif [ $1 = qt ]
then
g++ -O0 -g -fPIC -shared qt.cpp -o qt.so
fi
