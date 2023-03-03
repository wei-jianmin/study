https://blog.51cto.com/enchen/157981

xfrm_lookup函数是个非常重要的函数, 
用来根据安全策略构造数据包的路由项链表, 
该路由项链表反映了对数据包进行IPSEC封装的多层次的处理, 
每封装一次, 就增加一个路由项.

该函数被路由查找函数ip_route_output_flow()调用, 
针对的是转发或发出的数据包.