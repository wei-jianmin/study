内存分配原理
    STL提供的一个默认的allocator实现的
        大多数情况下，STL默认的allocator就已经足够了
        这个allocator是一个由两级分配器构成的内存管理器
        当申请的内存大小大于128byte时
            就使用__malloc_alloc_template分配器分配内存，
            内部就是直接调用malloc，
            不过当分配失败时，会调用类似内存清理的处理函数，
            然后再调用malloc，分配失败，则重复上一步，
            直到内存分配成功，或处理函数指针为空。
            my_malloc_handler函数的作用是当malloc内存分配失败时，
            做一些处理工作，以使得再次调用malloc能成功。
            从循环的特点可以知道，应该在my_malloc_handler函数的最后，
            指定下一个内存分配失败处理函数（使用set_malloc_handler），
            从而做到本地的内存分配失败处理函数处理失败(仍没使得malloc成功分配内存）时，
            继续可以使用下个处理函数。
        如果申请的内存大小小于128byte时
            就使用__default_alloc_template分配器
            从一个预先分配好的内存池中取一块内存交付给用户
            这个内存池由16个不同大小（8的倍数，8~128byte）的空闲列表组成，
            allocator会根据申请内存的大小（将这个大小round up成8的倍数）
            从对应的空闲块列表取表头块给用户。
        优点：
            小对象的快速分配
            避免了内存碎片的生成
        实现：
            allocator维护一个“存储16个空闲块列表表头的”数组
              union _Obj {
                union _Obj* _M_free_list_link;
                char _M_client_data[1]; 
                };
              static _Obj* _S_free_list[16]; 
            释放内存块的函数实现
              static void deallocate(void* __p, size_t __n)
              {
                if (__n > 128)
                  malloc_alloc::deallocate(__p, __n);
                else {
                  _Obj* __my_free_list = _S_free_list + f(__n){计算n为8的多少倍};
                  _Obj* __q = (_Obj*)__p;
                  __q -> _M_free_list_link = *__my_free_list;
                  *__my_free_list = __q;
                }
              }
    用户也可以定制自己的allocator
        只要实现allocator模板所定义的接口方法即可，
        然后通过将自定义的allocator作为模板参数传递给STL容器，
        创建一个使用自定义allocator的STL容器对象
        如：stl::vector <int, UserDefinedAllocator> array；
各种容器的内存管理方式
    序列式容器
        vector
            数组结构，动态分配
            插入会引起之后的迭代器失效，插入点之前的迭代器不影响
            如果引起扩容，则全部迭代器失效
            删除会使得之后的迭代器失效
        list
            双向链表或双向循环链表
            插入/拼接不会使得当前迭代器失效
            删除只会使得当前迭代器失效
        deque/stack/queue
            deque(double ended queue)是双向开口的连续线性空间，
            所谓的连续空间只是对外看来是这样的，
            其内部实际是动态将多个连续空间通过指针数组接合在一起，
            它可以随时可以增加一段新的空间串接在deque的尾端，
            而不会有像vector结构那样存在内存不够，重新扩容的问题
            deque头尾两端分别做插入和删除操作都是常数时间
            虽然deque也和vector那样提供随机访问迭代器，
            但两者效率差距不在一个数量级。
            deque内部实际是通过一个value_type** map来记录各个
            非连续内存分段的指针，另有一个int map_size记录数组大小。
            每个map数组元素都是一个value_type*类型指针，指向一块内存区域，
            如果当前map满载了，就重新找一个更大的空间来存放map。
            std::deque通过其迭代器的++和--操作，维护其“整体连续”的假象。
            stack和queue，都是deque的适配器类。
            当中间删除元素时，会引起内部数据的向前或向后移动，insert类似。
    关联式容器
        set
        map
        multiset
        multimap
        hashtable（非标准）
        hash_map（非标准）
        hash_set（非标准）
        hash_multimap（非标准）
        hash_multiset（非标准）
        RB-tree(红黑树，内置，非公开)
常见的树结构
    二叉树
        二叉树的每个结点至多只有二棵子树
        二叉树的子树有左右之分，次序不能颠倒
    满二叉树
        除最后一层无任何子节点外，
        每一层上的所有结点都有两个子结点的二叉树
    完全二叉树
        *
    二叉排序树（二叉查找树、二叉搜索树）
        1) 若它的左子树不空，则左子树上所有结点的值
           均小于它的根结点的值；
        2) 若它的右子树不空，则右子树上所有结点的值
           均大于或等于它的根结点的值；
        3) 它的左、右子树也分别为二叉排序树。
        使用二叉排序树，查找的时候，可以折半查找，
        在最坏的情况下，查找事件取决于树深度。
        最坏的二叉排序树是各级子节点全都是右子节点（或左子节点）
    AVL平衡二叉树
        平衡二叉树首先是一颗二叉排序树，
        为了提高查找效率，所以希望最小的树深度，具体为：
            左子树和右子树的深度相差不超过1
        平衡二叉树的左子树和右子树都是平衡二叉树
    红黑树
        特点：
            根结点是黑色
            所有叶子都是黑色
            每个红色结点的两个子结点都是黑色
                (意味着从每个叶子到根的所有路径上不能有两个连续的红色结点)
            从任一节结点其每个叶子的所有路径都包含相同数目的黑色结点
        红黑树的本质是对2-3-4树(4阶B树)的模拟  https://zhuanlan.zhihu.com/p/273829162
            2节点(有2个孩子的节点)对应一个黑色节点
            3节点对应一个黑节点+一个红孩子
            4节点对应一个黑节点+两个红孩子
            红孩子可以理解为与黑节点处于同一层，如此一来，就是一颗4阶B树了
            这样就可以理解一些红黑树的特性了：
                红节点因为要旋转45度，与其父节点变为同一层，
                所以红节点的子节点必须是黑节点，
                否则这些子节点也要旋转，那这个树的阶数可能就不止4。
                根节点和叶子节点不应旋转，所以他们都是黑色节点。
    B-树(B树/平衡树，这里的-，是横杠，不是减号)
        在平衡树要求的基础上，要求所有叶子节点处于同一层
        一颗m阶的B树定义如下：
            1）每个结点最多有m-1个关键字。（最多有m个子女）
            2）根结点最少可以只有1个关键字。（根节点至少有两个子女）
            3）非根结点至少有Math.ceil(m/2)-1个关键字(floor(m),接近一半)。
               （枝节点最少有m/2个子女）
            4）每个结点中的关键字都按照从小到大的顺序排列，
               每个关键字的左子树中的所有关键字都小于它，而右子树中的所有关键字都大于它。
            5）所有叶子结点都位于同一层，或者说根结点到每个叶子结点的长度都相同
            https://blog.csdn.net/apriaaaa/article/details/102975155
    B+树
        对B树的变形，比B树有更广泛的应用
        1.节点关键字个数与孩子个数相同
        2.枝节点有m/2到m个孩子
        3.所有叶节点处于同一层，且不含任何信息(致使查找失败)
        B+树的查找与B树不同，当索引部分某个结点的关键字与所查的关键字相等时，
        并不停止查找，应继续沿着这个关键字左边的指针向下，
        一直查到该关键字所在的叶子结点为止。
    B*树