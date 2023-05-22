ctypes是一个Python的三方库，提供了兼容C的数据类型，并允许调用动态库中的函数方法

注意：有些代码使用了 c_int 类型，在 sizeof(long) == sizeof(int) 的平台上，c_int 被指定为 c_long
      所以你打印 c_int 的类型是，看到的可能是 c_long

加载动态库
    