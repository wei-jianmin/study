https://blog.csdn.net/it_hue/category_7462826.html
1. 前言
    在Linux2.6内核中自带了IPSEC的实现,这样就不用象2.4那样打补丁来实现了
    该实现包括以下几个部分:
        PF_KEY类型套接口, 用来提供和用户层空间进行PF_KEY通信，代码在net/key目录下；
        （注：后来增加了netlink通信方式）
        安全联盟SA和安全策略SP管理，是使用xfrm库来实现的，代码在net/xfrm/目录下定义
        ESP，AH等协议实现，在net/ipv4(6)下定义
        加密认证算法库，在crypto目录下定义，这些算法都是标准代码了
    本系列文章主要描述XFRM库的实现以及在IPV4下相关协议的处理部分, IPV6的忽略。
    3 种数据结构：
        策略(xfrm policy)
        模板(template)
        状态(xfrm state)
    本文Linux内核代码版本为2.6.19.2
    xfrm是内核中变化比较大的部分,每个版本中都有不小的差异, 同时也说明了该模块的不成熟性
    在net/xfrm目录下的各文件大致功能说明如下
        xfrm_state.c    : xfrm状态管理
        xfrm_policy.c   : xfrm策略管理
        xfrm_algo.c     : 算法管理
        xfrm_hash.c     : HASH计算函数
        xfrm_input.c    : 安全路径(sec_path)处理,用于进入的ipsec包
        xfrm_user.c     :  netlink接口的SA和SP管理
    在net/ipv4目录下的和ipsec相关各文件大致功能说明如下:
        ah4.c               : IPV4的AH协议处理
        esp4.c              : IPV4的ESP协议处理
        ipcomp.c            : IP压缩协议处理
        xfrm4_input         : 接收的IPV4的IPSEC包处理
        xfrm4_output        : 发出的IPV4的IPSEC包处理
        xfrm4_state         : IPV4的SA处理
        xfrm4_policy        : IPV4的策略处理
        xfrm4_tunnel        : IPV4的通道处理
        xfrm4_mode_transport: 传输模式
        xfrm4_mode_tunnel   : 通道模式
        xfrm4_mode_beet     : BEET模式
2. 数据结构
    内核SA的定义用xfrm_state结构定义，SP用xfrm_policy结构定义，
    在include/net/xfrm.h中定义
    2.1 状态(SA)
        xfrm_state状态结构用来描述SA在内核中的具体实现:
        struct xfrm_state
        {
            /* Note: bydst is re-used during gc */
            // 每个状态结构挂接到三个HASH链表中
            struct hlist_node bydst; // 按目的地址HASH
            struct hlist_node bysrc; // 按源地址HASH
            struct hlist_node byspi; // 按SPI值HASH
            atomic_t  refcnt; // 所有使用计数
            spinlock_t  lock;   // 状态锁
            struct xfrm_id  id; // ID结构， 即目的地址，SPI，协议三元组
            struct xfrm_selector sel; // 状态选择子
            u32   genid; // 状态的标志值, 防止发生碰撞
            /* Key manger bits */
            struct {
                u8  state;
                u8  dying;
                u32  seq;
            } km;  // KEY回调管理处理结构参数
            /* Parameters of this state. */
            struct {
                u32  reqid; // 请求ID
                u8  mode;  // 模式: 传输/通道
                u8  replay_window; // 回放窗口
                u8  aalgo, ealgo, calgo; // 认证,加密,压缩算法ID值
                u8  flags; // 一些标准
                u16  family; // 协议族
                xfrm_address_t saddr;  // 源地址
                int  header_len;  // 添加的协议头长度
                int  trailer_len; //
            } props; // SA相关参数结构
            struct xfrm_lifetime_cfg lft; // 生存时间配置
            /* Data for transformer */
            struct xfrm_algo *aalg; // hash算法
            struct xfrm_algo *ealg; // 加密算法
            struct xfrm_algo *calg; // 压缩算法
            /* Data for encapsulator */
            struct xfrm_encap_tmpl *encap; // NAT-T封装信息
            /* Data for care-of address */
            xfrm_address_t *coaddr;
            /* IPComp needs an IPIP tunnel for handling uncompressed packets */
            struct xfrm_state *tunnel;  // 通道, 实际是另一个SA
            /* If a tunnel, number of users + 1 */
            atomic_t  tunnel_users; // 通道的使用数
            /* State for replay detection */
            struct xfrm_replay_state replay; // 回放检测结构,包含各种序列号掩码等信息
            /* Replay detection state at the time we sent the last notification */
            struct xfrm_replay_state preplay; // 上次的回放记录值
            /* internal flag that only holds state for delayed aevent at the moment */
            u32   xflags; // 标志
            /* Replay detection notification settings */
            u32   replay_maxage; // 回放最大时间间隔
            u32   replay_maxdiff; // 回放最大差值
            /* Replay detection notification timer */
            struct timer_list rtimer; // 回放检测定时器
            /* Statistics */
            struct xfrm_stats stats; // 统计值
            struct xfrm_lifetime_cur curlft; // 当前时间计数器
            struct timer_list timer;  // SA定时器
            /* Last used time */
            u64   lastused; // 上次使用时间
            /* Reference to data common to all the instances of this transformer */
            struct xfrm_type *type;  // 协议, ESP/AH/IPCOMP
            struct xfrm_mode *mode;  // 模式, 通道或传输
            /* Security context */
            struct xfrm_sec_ctx *security; // 安全上下文, 加密时使用
            /* Private data of this transformer, format is opaque,
            * interpreted by xfrm_type methods. */
            void   *data; // 内部数据
        };
    2.2 安全策略(SP)
        xfrm_policy结构用于描述SP在内核内部的具体实现:
        struct xfrm_policy
        {
            struct xfrm_policy *next; // 下一个策略
            struct hlist_node bydst; // 按目的地址HASH的链表
            struct hlist_node byidx; // 按索引号HASH的链表
            /* This lock only affects elements except for entry. */
            rwlock_t  lock;  // 策略结构锁
            atomic_t  refcnt; // 引用次数
            struct timer_list timer; // 策略定时器
            u8   type;     // 类型
            u32   priority; // 策略优先级
            u32   index;    // 策略索引号
            struct xfrm_selector selector; // 选择子
            struct xfrm_lifetime_cfg lft;     // 策略生命期
            struct xfrm_lifetime_cur curlft;  // 当前的生命期数据
            struct dst_entry       *bundles;  // 路由链表
            __u16   family;   // 协议族
            __u8   action;   // 策略动作, 接受/加密/阻塞...
            __u8   flags;    // 标志
            __u8   dead;     // 策略死亡标志
            __u8   xfrm_nr;  // 使用的xfrm_vec的数量
            struct xfrm_sec_ctx *security; // 安全上下文
            struct xfrm_tmpl        xfrm_vec[XFRM_MAX_DEPTH]; // 状态模板
        };
        xfrm模板结构, 用于状态和策略的查询:
        struct xfrm_tmpl
        {
            /* id in template is interpreted as:
            * daddr - destination of tunnel, may be zero for transport mode.
            * spi   - zero to acquire spi. Not zero if spi is static, then
            *    daddr must be fixed too.
            * proto - AH/ESP/IPCOMP
            */
            // SA三元组, 目的地址, 协议, SOI
            struct xfrm_id  id;
            /* Source address of tunnel. Ignored, if it is not a tunnel. */
            // 源地址
            xfrm_address_t  saddr;
            // 请求ID
            __u32   reqid;
            /* Mode: transport, tunnel etc. */
            __u8   mode;
            /* Sharing mode: unique, this session only, this user only etc. */
            __u8   share;
            /* May skip this transfomration if no SA is found */
            __u8   optional;
            /* Bit mask of algos allowed for acquisition */
            __u32   aalgos;
            __u32   ealgos;
            __u32   calgos;
        };
    2.3 协议结构
        对ESP, AH, IPCOMP等协议的描述是通过xfrm_type结构来描述的, 
        多个协议的封装就是靠多个协议结构形成的链表来实现:
        struct xfrm_type
        {
            char   *description; // 描述字符串
            struct module  *owner; // 协议模块
            __u8   proto;  // 协议值
            __u8   flags;  // 标志
            #define XFRM_TYPE_NON_FRAGMENT 1
            // 初始化状态
            int   (*init_state)(struct xfrm_state *x);
            // 析构函数
            void   (*destructor)(struct xfrm_state *);
            // 数据输入函数
            int   (*input)(struct xfrm_state *, struct sk_buff *skb);
            // 数据输出函数
            int   (*output)(struct xfrm_state *, struct sk_buff *pskb);
            // 拒绝函数
            int   (*reject)(struct xfrm_state *, struct sk_buff *, struct flowi *);
            // 头部偏移
            int   (*hdr_offset)(struct xfrm_state *, struct sk_buff *, u8 **);
            // 本地地址
            xfrm_address_t  *(*local_addr)(struct xfrm_state *, xfrm_address_t *);
            // 远程地址
            xfrm_address_t  *(*remote_addr)(struct xfrm_state *, xfrm_address_t *);
            /* Estimate maximal size of result of transformation of a dgram */
            // 最大数据报长度
            u32   (*get_max_size)(struct xfrm_state *, int size);
        };
        具体的协议结构定义如下, 通常只定义初始化,析构,输入和输出四个成员函数:
        AH协议定义
            /* net/ipv4/ah4.c */
            static struct xfrm_type ah_type =
            {
                .description = "AH4",
                .owner  = THIS_MODULE,
                .proto       = IPPROTO_AH,
                .init_state = ah_init_state,
                .destructor = ah_destroy,
                .input  = ah_input,
                .output  = ah_output
            };
        ESP协议定义:
            /* net/ipv4/esp4.c */
            static struct xfrm_type esp_type =
            {
                .description = "ESP4",
                .owner  = THIS_MODULE,
                .proto       = IPPROTO_ESP,
                .init_state = esp_init_state,
                .destructor = esp_destroy,
                .get_max_size = esp4_get_max_size,
                .input  = esp_input,
                .output  = esp_output
            };
        IP压缩协议定义:
            /* net/ipv4/ipcomp.c */
            static struct xfrm_type ipcomp_type = {
                .description = "IPCOMP4",
                .owner  = THIS_MODULE,
                .proto       = IPPROTO_COMP,
                .init_state = ipcomp_init_state,
                .destructor = ipcomp_destroy,
                .input  = ipcomp_input,
                .output  = ipcomp_output
            };
        IPIP协议定义:
            /* net/ipv4/xfrm4_tunnel.c */
            static struct xfrm_type ipip_type = {
                .description = "IPIP",
                .owner  = THIS_MODULE,
                .proto       = IPPROTO_IPIP,
                .init_state = ipip_init_state,
                .destructor = ipip_destroy,
                .input  = ipip_xfrm_rcv,
                .output  = ipip_output
            };
    2.4 模式结构
        模式结构用于描述IPSEC连接描述, 可为通道模式或传输模式两种:
        struct xfrm_mode {
            // 数据输入函数
            int (*input)(struct xfrm_state *x, struct sk_buff *skb);
            // 数据输出函数
            int (*output)(struct xfrm_state *x,struct sk_buff *skb);
            // 模块指针
            struct module *owner;
            // 封装
            unsigned int encap;
        };
        通道模式结构定义:
            /* net/ipv4/xfrm4_mode_tunnel.c */
            static struct xfrm_mode xfrm4_tunnel_mode = {
                .input = xfrm4_tunnel_input,
                .output = xfrm4_tunnel_output,
                .owner = THIS_MODULE,
                .encap = XFRM_MODE_TUNNEL,
            };
        传输模式结构定义:
            /* net/ipv4/xfrm4_mode_transport.c */
            static struct xfrm_mode xfrm4_transport_mode = {
                .input = xfrm4_transport_input,
                .output = xfrm4_transport_output,
                .owner = THIS_MODULE,
                .encap = XFRM_MODE_TRANSPORT,
            };
        beet模式, 不知道在哪用
            /* net/ipv4/xfrm4_mode_beet.c */
            static struct xfrm_mode xfrm4_beet_mode = {
                .input = xfrm4_beet_input,
                .output = xfrm4_beet_output,
                .owner = THIS_MODULE,
                .encap = XFRM_MODE_BEET,
            };
    2.5 策略的相关协议处理结构
        以下结构用于描述具体协议族下的的策略处理:
        struct xfrm_policy_afinfo {
            // 协议族
            unsigned short  family;
            // 协议类型
            struct xfrm_type *type_map[IPPROTO_MAX];
            // 模式
            struct xfrm_mode *mode_map[XFRM_MODE_MAX];
            // 目的操作结构
            struct dst_ops  *dst_ops;
            // 垃圾搜集
            void   (*garbage_collect)(void);
            // 路由选择
            int   (*dst_lookup)(struct xfrm_dst **dst, struct flowi *fl);
            // 获取源地址
            int   (*get_saddr)(xfrm_address_t *saddr, xfrm_address_t *daddr);
            // 查找路由项
            struct dst_entry *(*find_bundle)(struct flowi *fl, struct xfrm_policy *policy);
            // 创建新路由项
            int   (*bundle_create)(struct xfrm_policy *policy, 
            struct xfrm_state **xfrm, 
            int nx,
            struct flowi *fl, 
            struct dst_entry **dst_p);
            // 解码会话
            void   (*decode_session)(struct sk_buff *skb,
            struct flowi *fl);
        };
        IPV4的策略协议相关处理结构定义如下:
        /* net/ipv4/xfrm4_policy.c */
        static struct xfrm_policy_afinfo xfrm4_policy_afinfo = {
            .family =   AF_INET,
            .dst_ops =  &xfrm4_dst_ops,
            .dst_lookup =  xfrm4_dst_lookup,
            .get_saddr =  xfrm4_get_saddr,
            .find_bundle =   __xfrm4_find_bundle,
            .bundle_create = __xfrm4_bundle_create,
            .decode_session = _decode_session4
        }
    2.6 状态的相关协议处理结构
        以下结构用于描述具体协议族下的的状态处理:
        struct xfrm_state_afinfo {
            // 协议族
            unsigned short  family;
            // 初始化标志
            int   (*init_flags)(struct xfrm_state *x);
            // 初始化模板选择
            void   (*init_tempsel)(struct xfrm_state *x, struct flowi *fl,
            struct xfrm_tmpl *tmpl,
            xfrm_address_t *daddr, xfrm_address_t *saddr);
            // 模板排序
            int   (*tmpl_sort)(struct xfrm_tmpl **dst, struct xfrm_tmpl **src, int n);
            // 状态排序
            int   (*state_sort)(struct xfrm_state **dst, struct xfrm_state **src, int n);
        };
        IPV4的状态相关协议处理结构
        /* net/ipv4/xfrm4_state.c */
        static struct xfrm_state_afinfo xfrm4_state_afinfo = {
            .family   = AF_INET,
            .init_flags  = xfrm4_init_flags,
            .init_tempsel  = __xfrm4_init_tempsel,
        };
    2.7 回调通知信息结构
        struct xfrm_mgr
        {
            struct list_head list;
            char   *id;
            // 状态通知
            int   (*notify)(struct xfrm_state *x, struct km_event *c);
            // 获取, 如获取SA
            int   (*acquire)(struct xfrm_state *x, struct xfrm_tmpl *, struct xfrm_policy *xp, int dir);
            // 编译策略
            struct xfrm_policy *(*compile_policy)(struct sock *sk, int opt, u8 *data, int len, int *dir);
            // 映射
            int   (*new_mapping)(struct xfrm_state *x, xfrm_address_t *ipaddr, u16 sport);
            // 策略通知
            int   (*notify_policy)(struct xfrm_policy *x, int dir, struct km_event *c);
            // 报告
            int   (*report)(u8 proto, struct xfrm_selector *sel, xfrm_address_t *addr);
        };
        在net/key/pf_key.c中定义了pkeyv2_mgr结构:
        static struct xfrm_mgr pfkeyv2_mgr =
        {
            .id  = "pfkeyv2",
            .notify  = pfkey_send_notify,
            .acquire = pfkey_send_acquire,
            .compile_policy = pfkey_compile_policy,
            .new_mapping = pfkey_send_new_mapping,
            .notify_policy = pfkey_send_policy_notify,
        };
3. 初始化
    xfrm初始化函数包括状态, 策略和输入处理的三初始化函数
        /* net/xfrm/xfrm_policy.c */
        // xfrm是不支持模块方式的
        void __init xfrm_init(void)
        {
            xfrm_state_init();
            xfrm_policy_init();
            xfrm_input_init();
        }
    3.1 xfrm状态初始化
        /* net/xfrm/xfrm_state.c */
        void __init xfrm_state_init(void)
        {
            unsigned int sz;
            // 初始HASH表不大, 每个HASH中初始化为8个链表, 但随着状态数量的增加
            // 会动态增加HASH表数量
            sz = sizeof(struct hlist_head) * 8;
            // 建立3组HASH, 分别按SA的源地址, 目的地址和SPI值
            xfrm_state_bydst = xfrm_hash_alloc(sz);
            xfrm_state_bysrc = xfrm_hash_alloc(sz);
            xfrm_state_byspi = xfrm_hash_alloc(sz);
            if (!xfrm_state_bydst || !xfrm_state_bysrc || !xfrm_state_byspi)
                panic("XFRM: Cannot allocate bydst/bysrc/byspi hashes.");
            // xfrm_state_hmask初始值为=7, 计算出的HASH值与该值与来得到链表号
            xfrm_state_hmask = ((sz / sizeof(struct hlist_head)) - 1);
            // 初始化工作队列work_queue, 完成对状态垃圾的搜集和释放
            INIT_WORK(&xfrm_state_gc_work, xfrm_state_gc_task, NULL);
        }
    3.2 策略初始化
        static void __init xfrm_policy_init(void)
        {
            unsigned int hmask, sz;
            int dir;
            // 建立一个内核cache, 用于分配xfrm_dst结构()
            xfrm_dst_cache = kmem_cache_create("xfrm_dst_cache",
                                                sizeof(struct xfrm_dst),
                                                0, SLAB_HWCACHE_ALIGN|SLAB_PANIC,
                                                NULL, NULL);
            // 分配状态HASH表, 初始是8个HASH链表,以后随着策略数量的增加
            // 会动态增加HASH表的数量
            hmask = 8 - 1;
            sz = (hmask+1) * sizeof(struct hlist_head);
            // 该HASH表是按策略的index参数进行索引的
            xfrm_policy_byidx = xfrm_hash_alloc(sz);
            xfrm_idx_hmask = hmask;
            if (!xfrm_policy_byidx)
            panic("XFRM: failed to allocate byidx hash\n");
            // 输入, 输出, 转发三个处理点, 双向
            for (dir = 0; dir < XFRM_POLICY_MAX * 2; dir++) {
                struct xfrm_policy_hash *htab;
                // 初始化inexact链表头, inexact处理选择子相关长度不是标准值的一些特别策略
                INIT_HLIST_HEAD(&xfrm_policy_inexact[dir]);
                // 分配按地址HASH的HASH表
                htab = &xfrm_policy_bydst[dir];
                htab->table = xfrm_hash_alloc(sz);
                htab->hmask = hmask;
                if (!htab->table)
                panic("XFRM: failed to allocate bydst hash\n");
            }
            // 初始化策略垃圾搜集的工作队列, 完成对策略垃圾的搜集和释放
            INIT_WORK(&xfrm_policy_gc_work, xfrm_policy_gc_task, NULL);
            // 登记网卡通知
            register_netdevice_notifier(&xfrm_dev_notifier);
        }
        xfrm的网卡通知回调结构
        static struct notifier_block xfrm_dev_notifier = {
            xfrm_dev_event,
            NULL,
            0
        };
        // 网卡通知回调函数
        static int xfrm_dev_event(struct notifier_block *this, unsigned long event, void *ptr)
        {
            switch (event) {
                // 如果网卡down掉的话, 清除相关的所有的xfrm路由项
                case NETDEV_DOWN:
                xfrm_flush_bundles();
            }
            return NOTIFY_DONE;
        }
        // 清除相关的所有的xfrm路由项
        static int xfrm_flush_bundles(void)
        {
            // 将不用的路由项删除
            xfrm_prune_bundles(stale_bundle);
            return 0;
        }       
    3.3 输入初始化
        /* net/xfrm/xfrm_input.c */
        void __init xfrm_input_init(void)
        {
            // 建立一个内核cache, 用于分配sec_path结构(安全路径)
            secpath_cachep = kmem_cache_create("secpath_cache",
                                                sizeof(struct sec_path),
                                                0, SLAB_HWCACHE_ALIGN|SLAB_PANIC,
                                                NULL, NULL);
        }
        struct sec_path结构是对输入的加密包进行层层解包的处理, 
        在sk_buff中有该结构的指针sp, 如果sp非空表示这是个IPSEC解密后的包。
4. 状态(xfrm_state)处理
    本节所介绍的函数都在net/xfrm/xfrm_state.c中定义。
    4.1 状态分配
        状态分配函数为xfrm_state_alloc(), 该函数被pfkey_msg2xfrm_state()函数调用, 
        pfkey_msg2xfrm_state()函数是将标准的pfkey_msg(SA结构)转换为xfrm状态,
        同时该函数也被其他状态处理函数调用.
        struct xfrm_state *xfrm_state_alloc(void)
        {
            struct xfrm_state *x;
            // 分配空间
            x = kzalloc(sizeof(struct xfrm_state), GFP_ATOMIC);
            if (x) {
                // 使用数初始化为1
                atomic_set(&x->refcnt, 1);
                // 被0个ipsec通道使用
                atomic_set(&x->tunnel_users, 0);
                // 初始化链表节点, 状态可按目的地址, 源地址和SPI挂接到不同链表
                INIT_HLIST_NODE(&x->bydst);
                INIT_HLIST_NODE(&x->bysrc);
                INIT_HLIST_NODE(&x->byspi);
                // 状态定时器
                init_timer(&x->timer);
                // 定时器处理函数
                x->timer.function = xfrm_timer_handler;
                x->timer.data  = (unsigned long)x;
                // 回放检测定时器
                init_timer(&x->rtimer);
                // 回放定时器处理函数
                x->rtimer.function = xfrm_replay_timer_handler;
                x->rtimer.data     = (unsigned long)x;
                x->curlft.add_time = (unsigned long)xtime.tv_sec;
                // SA生命期参数
                x->lft.soft_byte_limit = XFRM_INF;
                x->lft.soft_packet_limit = XFRM_INF;
                x->lft.hard_byte_limit = XFRM_INF;
                x->lft.hard_packet_limit = XFRM_INF;
                // 回放处理参数
                x->replay_maxage = 0;
                x->replay_maxdiff = 0;
                // 初始化状态锁
                spin_lock_init(&x->lock);
            }
            return x;
        }
        EXPORT_SYMBOL(xfrm_state_alloc);
        // 状态定时器超时处理函数
        static void xfrm_timer_handler(unsigned long data)
        {
            struct xfrm_state *x = (struct xfrm_state*)data;
            unsigned long now = (unsigned long)xtime.tv_sec;
            long next = LONG_MAX;
            int warn = 0;
            spin_lock(&x->lock);
            // 如果该xfrm状态已经处于死亡状态, 可以返回了
            if (x->km.state == XFRM_STATE_DEAD)
                goto out;
            // 如果处于生命期到期状态, 转到期处理
            if (x->km.state == XFRM_STATE_EXPIRED)
                goto expired;
            // 如果到期了还要强制要增加一些时间
            if (x->lft.hard_add_expires_seconds) {
                // 计算强制增加的超时时间
                long tmo = x->lft.hard_add_expires_seconds +
                x->curlft.add_time - now;
                // 没法增加超时了, 到期
                if (tmo <= 0)
                goto expired;
                if (tmo < next)
                next = tmo;
            }
            // 如果到期了还要强制要增加的使用时间
            if (x->lft.hard_use_expires_seconds) {
                // 计算强制增加的使用时间
                long tmo = x->lft.hard_use_expires_seconds +
                (x->curlft.use_time ? : now) - now;
                // 没法增加超时了, 到期
                if (tmo <= 0)
                goto expired;
                if (tmo < next)
                next = tmo;
            }
            // dying表示软性增加超时已经不可用
            if (x->km.dying)
                goto resched;
            // 如果到期了还要软性要增加一些时间
            if (x->lft.soft_add_expires_seconds) {
                // 计算软性增加的时间
                long tmo = x->lft.soft_add_expires_seconds +
                x->curlft.add_time - now;
                // 软性增加超时不可用了
                if (tmo <= 0)
                warn = 1;
                else if (tmo < next)
                next = tmo;
            }
            // 如果到期了还要软性要增加的使用时间
            if (x->lft.soft_use_expires_seconds) {
                // 计算软性增加的使用时间
                long tmo = x->lft.soft_use_expires_seconds +
                (x->curlft.use_time ? : now) - now;
                // 软性增加超时不可用了
                if (tmo <= 0)
                warn = 1;
                else if (tmo < next)
                next = tmo;
            }
            // dying即为软性增加超时是否可用标志
            x->km.dying = warn;
            // 软性增加超时已比不可用, 进行状态的超时到期通知
            if (warn)
                km_state_expired(x, 0, 0);
            resched:
                // 如果增加的超时有效, 修改定时器超时时间
                if (next != LONG_MAX)
                    mod_timer(&x->timer, jiffies + make_jiffies(next));
                goto out;
            expired:
                // 状态到期
                if (x->km.state == XFRM_STATE_ACQ && x->id.spi == 0) {
                // 如果这个状态是ACQ类型状态(不是用户空间主动建立的状态,而是内核根据策略主动要求
                // 用户空间进行IKE协商建立的状态)
                // 状态设置为到期
                x->km.state = XFRM_STATE_EXPIRED;
                // 唤醒等待队列准备进行垃圾搜集操作
                wake_up(&km_waitq);
                next = 2;
                goto resched;
                }
                // 删除状态, 进行状态的到期通知
                if (!__xfrm_state_delete(x) && x->id.spi)
                // 1表示是硬性到期了
                km_state_expired(x, 1, 0);
            out:
                spin_unlock(&x->lock);
        }
        // 回放定时器超时回调函数
        static void xfrm_replay_timer_handler(unsigned long data)
        {
            struct xfrm_state *x = (struct xfrm_state*)data;
            spin_lock(&x->lock);
            // 只是状态为有效时才检查
            if (x->km.state == XFRM_STATE_VALID) {
                // 是否有NETLINK的监听者
                if (xfrm_aevent_is_on())
                    // 通知回放超时事件
                    xfrm_replay_notify(x, XFRM_REPLAY_TIMEOUT);
                else
                    // 设置通知推迟标志
                    x->xflags |= XFRM_TIME_DEFER;
            }
            spin_unlock(&x->lock);
        }
        状态初始化:
        int xfrm_init_state(struct xfrm_state *x)
        {
            struct xfrm_state_afinfo *afinfo;
            int family = x->props.family;
            int err;
            err = -EAFNOSUPPORT;
            // 获取协议族信息结构
            afinfo = xfrm_state_get_afinfo(family);
            if (!afinfo)
                goto error;
            err = 0;
            // 协议族信息初始化
            if (afinfo->init_flags)
                err = afinfo->init_flags(x);
            xfrm_state_put_afinfo(afinfo);
            if (err)
                goto error;
            err = -EPROTONOSUPPORT;
            // 获取可用协议(ah, esp, ipcomp, ip)
            x->type = xfrm_get_type(x->id.proto, family);
            if (x->type == NULL)
                goto error;
            err = x->type->init_state(x);
            if (err)
                goto error;
            // 获取可用模式(transport, tunnel)
            x->mode = xfrm_get_mode(x->props.mode, family);
            if (x->mode == NULL)
                goto error;
            // 状态设置为VALID
            x->km.state = XFRM_STATE_VALID;
            error:
                return err;
        }
        EXPORT_SYMBOL(xfrm_init_state);
    4.2 状态删除
        状态删除函数为xfrm_state_delete(), 该函数被pfkey_delete函数调用.
        // 这个函数只是__xfrm_state_delete()加锁的包裹函数
        int xfrm_state_delete(struct xfrm_state *x)
        {
            int err;
            spin_lock_bh(&x->lock);
            err = __xfrm_state_delete(x);
            spin_unlock_bh(&x->lock);
            return err;
        }
        EXPORT_SYMBOL(xfrm_state_delete);
        // 实际的相同删除操作函数, 必须保证在x->lock加锁状态下执行
        int __xfrm_state_delete(struct xfrm_state *x)
        {
            int err = -ESRCH;
            // 如果状态已经是DEAD就不操作了
            if (x->km.state != XFRM_STATE_DEAD) {
                // 设置状态为DEAD
                x->km.state = XFRM_STATE_DEAD;
                // xfrm_state_lock是全局的状态链表操作锁
                spin_lock(&xfrm_state_lock);
                // 从目的地址索引的链表中断开
                hlist_del(&x->bydst);
                // 从源地址索引的链表中断开
                hlist_del(&x->bysrc);
                // 从SPI索引的链表中断开
                if (x->id.spi)
                    hlist_del(&x->byspi);
                // xfrm状态总数减一
                xfrm_state_num--;
                spin_unlock(&xfrm_state_lock);
                /* All xfrm_state objects are created by xfrm_state_alloc.
                * The xfrm_state_alloc call gives a reference, and that
                * is what we are dropping here.
                */
                // 减少该状态引用计数
                __xfrm_state_put(x);
                err = 0;
            }
            return err;
        }
        EXPORT_SYMBOL(__xfrm_state_delete);
    4.3 删除全部状态
        删除全部状态函数为xfrm_state_flush(), 该函数被pfkey_flush函数调用.
        // 删除某种协议proto的所有状态
        void xfrm_state_flush(u8 proto)
        {
            int i;
            spin_lock_bh(&xfrm_state_lock);
            // 循环所有HASH链表
            for (i = 0; i <= xfrm_state_hmask; i++) {
                struct hlist_node *entry;
                struct xfrm_state *x;
                restart:
                    // 在按目的地址进行索引的链表中循环（支持内嵌函数？）
                    hlist_for_each_entry(x, entry, xfrm_state_bydst+i, bydst) 
                    {
                        // 要满足两个条件:
                        // 非正在被ipsec通道使用的状态; 协议类型匹配
                        if (!xfrm_state_kern(x) &&
                            xfrm_id_proto_match(x->id.proto, proto)) 
                        {
                            // 先hold住状态,防止在解开xfrm_state_lock锁, 
                            // 又没被进入xfrm_state_delete()前
                            // 被意外删除了, 此处考虑得比较仔细
                            xfrm_state_hold(x);
                            // 先解开xfrm_state_lock, 在xfrm_state_delete()中要重新上锁
                            spin_unlock_bh(&xfrm_state_lock);
                            // 删除状态
                            xfrm_state_delete(x);
                            // 减少刚才的引用计数
                            xfrm_state_put(x);
                            // 重新加锁, 循环
                            spin_lock_bh(&xfrm_state_lock);
                            goto restart;
                        }
                    }
            }
            spin_unlock_bh(&xfrm_state_lock);
            wake_up(&km_waitq);
        }
        EXPORT_SYMBOL(xfrm_state_flush);
    4.4 状态增加或更新
        状态增加函数为xfrm_state_add(), 状态更新函数为xfrm_state_update(),
        这两个函数都被pfkey_add函数调用.
        // 添加xfrm状态
        int xfrm_state_add(struct xfrm_state *x)
        {
            struct xfrm_state *x1;
            int family;
            int err;
            // 当协议为为ESP, AH, COMP以及ANY时为真, 其他为假
            int use_spi = xfrm_id_proto_match(x->id.proto, IPSEC_PROTO_ANY);
            family = x->props.family;
            spin_lock_bh(&xfrm_state_lock);
            // 根据xfrm的地址, SPI, 协议, 协议族等信息查找内核中是否已经存在相同的xfrm
            x1 = __xfrm_state_locate(x, use_spi, family);
            if (x1) {
                // 确实已经存在, 返回错误
                xfrm_state_put(x1);
                x1 = NULL;
                err = -EEXIST;
                goto out;
            }
            if (use_spi && x->km.seq) {
                // 如果序列号有效, 根据序列号查找内核中是否已经存在相同的xfrm
                x1 = __xfrm_find_acq_byseq(x->km.seq);
                // 找到, 但如果目的地址不符合的话, 仍试为没找到
                if (x1 && xfrm_addr_cmp(&x1->id.daddr, &x->id.daddr, family)) {
                    xfrm_state_put(x1);
                    x1 = NULL;
                }
            }
            // 如果没找到x1, 根据各种信息再查找xfrm
            if (use_spi && !x1)
                x1 = __find_acq_core(family, x->props.mode, x->props.reqid,
                                     x->id.proto,
                                     &x->id.daddr, &x->props.saddr, 0);
            // 如果x和现在内核中的xfrm匹配的话为x生成genid参数
            // 会用到一个静态单文件全局变量: xfrm_state_genid
            __xfrm_state_bump_genids(x);
            // 将新xfrm插入内核的各xfrm表, 这些表是以HASH表形式实现的, 分别根据
            // 源地址, 目的地址形成两个HASH表
            __xfrm_state_insert(x);
            err = 0;
            out:
                spin_unlock_bh(&xfrm_state_lock);
                // 如果按后来的条件找到x1, 删除之, 该状态不需要了
                if (x1) {
                    // 将找到的x1从链表中删除,
                    xfrm_state_delete(x1);
                    // 释放x1
                    xfrm_state_put(x1);
                }
            return err;
        }
        EXPORT_SYMBOL(xfrm_state_add);
        // 更新xfrm状态
        int xfrm_state_update(struct xfrm_state *x)
        {
            struct xfrm_state *x1;
            int err;
            int use_spi = xfrm_id_proto_match(x->id.proto, IPSEC_PROTO_ANY);
            spin_lock_bh(&xfrm_state_lock);
            // 查找内核中相应的xfrm, 找不到的话出错
            x1 = __xfrm_state_locate(x, use_spi, x->props.family);
            err = -ESRCH;
            if (!x1)
                goto out;
            // 如果该xfrm正在被IPSEC通道使用, 返回错误
            if (xfrm_state_kern(x1)) {
                xfrm_state_put(x1);
                err = -EEXIST;
                goto out;
            }
            // 找到的x1本来就是在acquire状态, 直接将x插入系统xfrm表就行了
            if (x1->km.state == XFRM_STATE_ACQ) {
                __xfrm_state_insert(x);
                x = NULL;
            }
            err = 0;
            out:
                spin_unlock_bh(&xfrm_state_lock);
                if (err)
                    return err;
                if (!x) {
                    // 将找到的acquire状态的xfrm删除, 正确返回
                    xfrm_state_delete(x1);
                    xfrm_state_put(x1);
                    return 0;
                }
            // 找到了x1, 状态也不是acquire, 即进行正常的更新x1中的数据为x的数据
            err = -EINVAL;
            spin_lock_bh(&x1->lock);
            if (likely(x1->km.state == XFRM_STATE_VALID)) {
                // 拷贝封装处理
                if (x->encap && x1->encap)
                    memcpy(x1->encap, x->encap, sizeof(*x1->encap));
                // 拷贝care of的地址
                if (x->coaddr && x1->coaddr) {
                    memcpy(x1->coaddr, x->coaddr, sizeof(*x1->coaddr));
                }
                // 没有SPI时拷贝选择子
                if (!use_spi && memcmp(&x1->sel, &x->sel, sizeof(x1->sel)))
                    memcpy(&x1->sel, &x->sel, sizeof(x1->sel));
                // 拷贝生命期
                memcpy(&x1->lft, &x->lft, sizeof(x1->lft));
                x1->km.dying = 0;
                // 1秒钟的超时
                mod_timer(&x1->timer, jiffies + HZ);
                if (x1->curlft.use_time)
                    xfrm_state_check_expire(x1);
                err = 0;
            }
            spin_unlock_bh(&x1->lock);
            xfrm_state_put(x1);
            return err;
        }
        EXPORT_SYMBOL(xfrm_state_update);
    4.5 状态插入
        状态插入函数为xfrm_state_insert(), 该函数被ipcomp_tunnel_attach()函数(net/ipv4/ipcomp.c)调用
        // xfrm_state_insert只是个包裹函数, 加xfrm_state_lock锁后调用__xfrm_state_bump_genids和
        // __xfrm_state_insert
        void xfrm_state_insert(struct xfrm_state *x)
        {
            spin_lock_bh(&xfrm_state_lock);
            __xfrm_state_bump_genids(x);
            __xfrm_state_insert(x);
            spin_unlock_bh(&xfrm_state_lock);
        }
        EXPORT_SYMBOL(xfrm_state_insert);
        /* xfrm_state_lock is held */
        // 碰撞检查, 看是否有多个连接状态, 要进行区别
        static void __xfrm_state_bump_genids(struct xfrm_state *xnew)
        {
            unsigned short family = xnew->props.family;
            u32 reqid = xnew->props.reqid;
            struct xfrm_state *x;
            struct hlist_node *entry;
            unsigned int h;
            // 计算状态HASH值来找相关链表
            h = xfrm_dst_hash(&xnew->id.daddr, &xnew->props.saddr, reqid, family);
            hlist_for_each_entry(x, entry, xfrm_state_bydst+h, bydst)
            {
                // 如果已经在链表中的状态的协议族, 请求ID, 源地址, 目的地址都和新状态匹配
                if (x->props.family == family && x->props.reqid == reqid &&
                    !xfrm_addr_cmp(&x->id.daddr, &xnew->id.daddr, family) &&
                    !xfrm_addr_cmp(&x->props.saddr, &xnew->props.saddr, family))
                    // 将这些状态的genid参数设置为当前xfrm_state_genid(全局变量)
                    x->genid = xfrm_state_genid;
            }
        }
        static void __xfrm_state_insert(struct xfrm_state *x)
        {
            unsigned int h;
            // 将新状态的genid设置为当前xfrm_state_genid值加一,和其他碰撞的状态区分开
            x->genid = ++xfrm_state_genid;
            // 添加到按目的地址HASH的链表
            h = xfrm_dst_hash(&x->id.daddr, &x->props.saddr,
            x->props.reqid, x->props.family);
            hlist_add_head(&x->bydst, xfrm_state_bydst+h);
            // 添加到按源地址HASH的链表
            h = xfrm_src_hash(&x->id.daddr, &x->props.saddr, x->props.family);
            hlist_add_head(&x->bysrc, xfrm_state_bysrc+h);
            if (x->id.spi) {
                // 添加到按SPI进行HASH的链表
                h = xfrm_spi_hash(&x->id.daddr, x->id.spi, x->id.proto,
                x->props.family);
                hlist_add_head(&x->byspi, xfrm_state_byspi+h);
            }
            // 修改定时器, 超时仅1秒
            mod_timer(&x->timer, jiffies + HZ);
            // 如果设置了回放最大时间间隔, 超时改为该值
            if (x->replay_maxage)
                mod_timer(&x->rtimer, jiffies + x->replay_maxage);
            // 唤醒等待队列
            wake_up(&km_waitq);
            // 状态总数加1
            xfrm_state_num++;
            // HASH扩大检查, 检查是否需要扩展HASH表数量
            xfrm_hash_grow_check(x->bydst.next != NULL);
        }
    4.6 状态查找
        状态查找函数有好几个, 分别按不同条件来查找状态, 注意找到状态后, 都会增加状态的引用计数.
        4.6.1 xfrm_state_lookup
            // 只是__xfrm_state_lookup的包裹函数， 是根据SPI进行HASH后查找
            struct xfrm_state *
            xfrm_state_lookup(xfrm_address_t *daddr, __be32 spi, u8 proto,
                              unsigned short family)
            {
                struct xfrm_state *x;
                spin_lock_bh(&xfrm_state_lock);
                x = __xfrm_state_lookup(daddr, spi, proto, family);
                spin_unlock_bh(&xfrm_state_lock);
                return x;
            }
            EXPORT_SYMBOL(xfrm_state_lookup);
            static struct xfrm_state *__xfrm_state_lookup(xfrm_address_t *daddr, __be32 spi, u8 proto, unsigned short family)
            {
                // 根据SPI进行HASH
                unsigned int h = xfrm_spi_hash(daddr, spi, proto, family);
                struct xfrm_state *x;
                struct hlist_node *entry;
                // 循环相应的SPI链表
                hlist_for_each_entry(x, entry, xfrm_state_byspi+h, byspi) 
                {
                    // 比较协议族, SPI, 和协议是否相同
                    if (x->props.family != family ||
                        x->id.spi       != spi ||
                        x->id.proto     != proto)
                        continue;
                    // 比较目的地址是否相同
                    switch (family) {
                        case AF_INET:
                            if (x->id.daddr.a4 != daddr->a4)
                                continue;
                            break;
                        case AF_INET6:
                            if (!ipv6_addr_equal((struct in6_addr *)daddr,
                                (struct in6_addr *)
                                x->id.daddr.a6))
                                continue;
                            break;
                    };
                    // 找到, 增加状态引用计数, 返回
                    xfrm_state_hold(x);
                    return x;
                }
                return NULL;
            }
        4.6.2 按地址查找状态
            // 只是__xfrm_state_lookup_byaddr的包裹函数，是根据目的地址进行HASH后查找
            struct xfrm_state *
            xfrm_state_lookup_byaddr(xfrm_address_t *daddr, xfrm_address_t *saddr,
                                     u8 proto, unsigned short family)
            {
                struct xfrm_state *x;
                spin_lock_bh(&xfrm_state_lock);
                x = __xfrm_state_lookup_byaddr(daddr, saddr, proto, family);
                spin_unlock_bh(&xfrm_state_lock);
                return x;
            }
            EXPORT_SYMBOL(xfrm_state_lookup_byaddr);
            static struct xfrm_state *__xfrm_state_lookup_byaddr(xfrm_address_t *daddr, xfrm_address_t *saddr, u8 proto, unsigned short family)
            {
                // 根据目的地址计算HASH值
                unsigned int h = xfrm_src_hash(daddr, saddr, family);
                struct xfrm_state *x;
                struct hlist_node *entry;
                // 循环相应的源地址链表
                hlist_for_each_entry(x, entry, xfrm_state_bysrc+h, bysrc) 
                {
                    // 比较协议族和协议是否相同
                    if (x->props.family != family ||
                        x->id.proto     != proto)
                        continue;
                    // 比较源地址和目的地址是否相同
                    switch (family) {
                        case AF_INET:
                            if (x->id.daddr.a4 != daddr->a4 ||
                                x->props.saddr.a4 != saddr->a4)
                                continue;
                            break;
                        case AF_INET6:
                            if (!ipv6_addr_equal((struct in6_addr *)daddr,
                                (struct in6_addr *)
                                x->id.daddr.a6) ||
                                !ipv6_addr_equal((struct in6_addr *)saddr,
                                (struct in6_addr *)
                                x->props.saddr.a6))
                                continue;
                            break;
                    };
                    // 找到, 增加状态引用计数, 返回
                    xfrm_state_hold(x);
                    return x;
                }
                return NULL;
            }
        4.6.3 __xfrm_state_locate
            这个函数只是__xfrm_state_lookup和__xfrm_state_lookup_byaddr的组合函数
            static inline struct xfrm_state *
            __xfrm_state_locate(struct xfrm_state *x, int use_spi, int family)
            {
                if (use_spi)
                    return __xfrm_state_lookup(&x->id.daddr, x->id.spi,
                                               x->id.proto, family);
                else
                    return __xfrm_state_lookup_byaddr(&x->id.daddr,
                                                      &x->props.saddr,
                                                      x->id.proto, family);
            }
        4.6.4 查找ACQUIRE类型的状态
            ACQUIRE类型的SA的产生是内核发现数据需要进行保护, 但却没有找到相关的SA, 就向用户空间的IKE协商程序发送ACQUIRE请求, 并生成一个ACQUIRE类型的SA, 如果用户空间协议协商成功会生成合适的SA传内核, 内核就会替换此ACQUIRE的SA, 因此ACQUIRE不是真正可用的SA, 只是表示有此SA的需求, 等待用户空间程序协商结果。
            // 只是__find_acq_core的包裹函数
            struct xfrm_state *
            xfrm_find_acq(u8 mode, u32 reqid, u8 proto, 
                          xfrm_address_t *daddr, xfrm_address_t *saddr, 
                          int create, unsigned short family)
            {
                struct xfrm_state *x;
                spin_lock_bh(&xfrm_state_lock);
                x = __find_acq_core(family, mode, reqid, proto, daddr, saddr, create);
                spin_unlock_bh(&xfrm_state_lock);
                return x;
            }
            EXPORT_SYMBOL(xfrm_find_acq);
            /* xfrm_state_lock is held */
            static struct xfrm_state *__find_acq_core(unsigned short family, u8 mode, u32 reqid, u8 proto, xfrm_address_t *daddr, xfrm_address_t *saddr, int create)
            {
                // 根据源地址，目的地址,请求ID进行目的地址类型HASH
                unsigned int h = xfrm_dst_hash(daddr, saddr, reqid, family);
                struct hlist_node *entry;
                struct xfrm_state *x;
                hlist_for_each_entry(x, entry, xfrm_state_bydst+h, bydst) 
                {
                    // 比较请求ID，数据模式，协议族
                    // 要求状态的类型为XFRM_STATE_ACQ，SPI值为0
                    if (x->props.reqid  != reqid ||
                        x->props.mode   != mode ||
                        x->props.family != family ||
                        x->km.state     != XFRM_STATE_ACQ ||
                        x->id.spi       != 0)
                        continue;
                    // 再比较源地址和目的地址是否相同
                    switch (family) {
                        case AF_INET:
                            if (x->id.daddr.a4    != daddr->a4 ||
                                x->props.saddr.a4 != saddr->a4)
                                continue;
                            break;
                        case AF_INET6:
                            if (!ipv6_addr_equal((struct in6_addr *)x->id.daddr.a6,
                                (struct in6_addr *)daddr) ||
                                !ipv6_addr_equal((struct in6_addr *)
                                x->props.saddr.a6,
                                (struct in6_addr *)saddr))
                                continue;
                            break;
                    };
                    // 找到, 增加状态引用计数, 返回
                    xfrm_state_hold(x);
                    return x;
                }
                // 没找到
                // 如果不需要创建, 返回NULL
                if (!create)
                    return NULL;
                // 创建ACQ类型的xfrm_state
                // 分配空间
                x = xfrm_state_alloc();
                if (likely(x)) {
                    // 填写网络地址基本参数
                    switch (family) {
                        case AF_INET:
                            x->sel.daddr.a4 = daddr->a4;
                            x->sel.saddr.a4 = saddr->a4;
                            x->sel.prefixlen_d = 32;
                            x->sel.prefixlen_s = 32;
                            x->props.saddr.a4 = saddr->a4;
                            x->id.daddr.a4 = daddr->a4;
                            break;
                        case AF_INET6:
                            ipv6_addr_copy((struct in6_addr *)x->sel.daddr.a6,
                            (struct in6_addr *)daddr);
                            ipv6_addr_copy((struct in6_addr *)x->sel.saddr.a6,
                            (struct in6_addr *)saddr);
                            x->sel.prefixlen_d = 128;
                            x->sel.prefixlen_s = 128;
                            ipv6_addr_copy((struct in6_addr *)x->props.saddr.a6,
                            (struct in6_addr *)saddr);
                            ipv6_addr_copy((struct in6_addr *)x->id.daddr.a6,
                            (struct in6_addr *)daddr);
                            break;
                    };
                    // 状态类型设置为XFRM_STATE_ACQ
                    x->km.state = XFRM_STATE_ACQ;
                    // 状态其他参数赋值
                    x->id.proto = proto;
                    x->props.family = family;
                    x->props.mode = mode;
                    x->props.reqid = reqid;
                    // 硬性可增加的超时
                    x->lft.hard_add_expires_seconds = XFRM_ACQ_EXPIRES;
                    xfrm_state_hold(x);
                    // 超时XFRM_ACQ_EXPIRES秒
                    x->timer.expires = jiffies + XFRM_ACQ_EXPIRES*HZ;
                    add_timer(&x->timer);
                    // 添加到目的HASH链表
                    hlist_add_head(&x->bydst, xfrm_state_bydst+h);
                    // 添加到源地址HASH链表
                    h = xfrm_src_hash(daddr, saddr, family);
                    hlist_add_head(&x->bysrc, xfrm_state_bysrc+h);
                    wake_up(&km_waitq);
                    // 增加状态总数     
                }
            }
    注：list_for_each_entry用法
        https://blog.csdn.net/u012503639/article/details/77771814
        在Linux内核源码中，经常要对链表进行操作，其中一个很重要的'宏'是list_for_each_entry：
        意思大体如下
             它实际上是一个 for 循环，利用传入的 pos 作为循环变量，
             从表头 head 开始，逐项向后（next 方向）移动 pos，直至又回head
             在程序中的使用如下：
                var pos;
                list_for_each_entry（pos , head,member）
                {       
                    ………………
                    addr =    pos;  
                    //对返回值pos的操作，这样更容易去理解list_for_each_entry，
                    //可以把它看作for()循环
                    ………………
                }
        宏list_for_each_entry的实现：
            #define list_for_each_entry(pos, head, member)				    \
            for (pos = list_entry((head)->next, typeof(*pos), member);	\
                   prefetch(pos->member.next), &pos->member != (head); 	    \
                   pos = list_entry(pos->member.next, typeof(*pos), member)
                  )
            1. pos = list_entry((head)->next, typeof(*pos), member)
                pos相当于循环中返回的循环变量，这里就是返回一个结构体指针
                #define list_entry container_of
                这个函数的做用是:
                   根据一个结构体变量中的一个域成员变量的指针
                   来获取指向整个结构体变量的指针。
                #define container_of(ptr, type, member) ({               \
                   const typeof(((type *)0)->member)*__mptr = (ptr);   \
                   (type *)((char *)__mptr - offsetof(type, member)); })
                所以list_entry()的作用为：
                    通过已知的指向member子项的指针，获得整个结构体的指针（地址）
            2. prefetch(pos->member.next),&pos->member!= (head);  
                refetch的含义是告诉cpu那些元素有可能马上就要用到，
                告诉cpu预取一下，这样可以提高速度，用于预取以提高遍历速度；
                &pos->member !=(head)  ，这个判断循环条件。
            3. pos= list_entry(pos->member.next, typeof(*pos), member)) 
                和第（1）实现相似，用于逐项向后（next 方向）移动 pos。
5. 安全策略(xfrm_policy)处理
    本节所介绍的函数都在net/xfrm/xfrm_policy.c中定义。
    5.1 策略分配
        策略分配函数为xfrm_policy_alloc(), 该函数被pfkey_spdadd()函数调用
        struct xfrm_policy *xfrm_policy_alloc(gfp_t gfp)
        {
            struct xfrm_policy *policy;
            // 分配struct xfrm_policy结构空间并清零
            policy = kzalloc(sizeof(struct xfrm_policy), gfp);
            if (policy)
            {
                // 初始化链接节点
                INIT_HLIST_NODE(&policy->bydst);
                INIT_HLIST_NODE(&policy->byidx);
                // 初始化锁
                rwlock_init(&policy->lock);
                // 策略引用计数初始化为1
                atomic_set(&policy->refcnt, 1);
                // 初始化定时器
                init_timer(&policy->timer);
                policy->timer.data = (unsigned long)policy;
                policy->timer.function = xfrm_policy_timer;
            }
            return policy;
        }
        EXPORT_SYMBOL(xfrm_policy_alloc);
        定时器函数:
        static void xfrm_policy_timer(unsigned long data)
        {
            struct xfrm_policy *xp = (struct
                                      xfrm_policy*)data;
            unsigned long now = (unsigned
                                 long)xtime.tv_sec;
            long next = LONG_MAX;
            int warn = 0;
            int dir;
            // 加锁
            read_lock(&xp->lock);
            // 如果策略已经是死的, 退出
            if (xp->dead)
                goto out;
            // 根据策略索引号确定策略处理的数据的方向, 看索引号的后3位
            dir =
                xfrm_policy_id2dir(xp->index);
            // 如果到期了还要强制要增加一些时间
            if
            (xp->lft.hard_add_expires_seconds)
            {
                // 计算强制增加的超时时间
                long tmo = xp->lft.hard_add_expires_seconds +
                           xp->curlft.add_time - now;
                // 没法增加超时了, 到期
                if (tmo <= 0)
                    goto expired;
                if (tmo < next)
                    next = tmo;
            }
            // 如果到期了还要强制要增加的使用时间
            if (xp->lft.hard_use_expires_seconds)
            {
                // 计算强制增加的使用时间
                long tmo = xp->lft.hard_use_expires_seconds +
                           (xp->curlft.use_time ? : xp->curlft.add_time) - now;
                // 没法增加超时了, 到期
                if (tmo <= 0)
                    goto expired;
                if (tmo < next)
                    next = tmo;
            }
            // 如果到期了还要软性要增加一些时间
            if (xp->lft.soft_add_expires_seconds)
            {
                // 计算软性增加的时间
                long tmo = xp->lft.soft_add_expires_seconds +
                           xp->curlft.add_time - now;
                // 软性增加超时小于0, 设置报警标志, 并将超时设置为XFRM_KM_TIMEOUT, 这点和其他不同
                if (tmo <= 0)
                {
                    warn = 1;
                    tmo = XFRM_KM_TIMEOUT;
                }
                if (tmo < next)
                    next = tmo;
            }
            // 如果到期了还要软性要增加的使用时间
            if (xp->lft.soft_use_expires_seconds)
            {
                // 计算软性增加的使用时间
                long tmo = xp->lft.soft_use_expires_seconds +
                           (xp->curlft.use_time ? : xp->curlft.add_time) - now;
                // 软性增加超时小于0, 设置报警标志, 并将超时设置为XFRM_KM_TIMEOUT, 这点和其他不同
                if (tmo <= 0)
                {
                    warn = 1;
                    tmo = XFRM_KM_TIMEOUT;
                }
                if (tmo < next)
                    next = tmo;
            }
            // 需要报警, 调用到期回调
            if (warn)
                km_policy_expired(xp, dir, 0, 0);
            // 如果更新的超时值有效, 修改定时器超时, 增加策略使用计数
            if (next != LONG_MAX && !mod_timer(&xp->timer, jiffies + make_jiffies(next)))
                xfrm_pol_hold(xp);
            out:
                read_unlock(&xp->lock);
                xfrm_pol_put(xp);
                return;
            expired:
                read_unlock(&xp->lock);
                // 如果确实到期, 删除策略
                if (!xfrm_policy_delete(xp, dir))
                    // 1表示是硬性到期了
                    km_policy_expired(xp, dir, 1, 0);
                xfrm_pol_put(xp);
        }
    5.2 策略插入
        策略插入函数为xfrm_policy_insert(), 该函数被pfkey_spdadd()函数调用,
        注意策略链表是按优先权大小进行排序的有序链表, 因此插入策略时要进行优先权比较后插入到合适的位置.
        int xfrm_policy_insert(int dir, struct xfrm_policy *policy, int excl)
        {
            struct xfrm_policy *pol;
            struct xfrm_policy *delpol;
            struct hlist_head *chain;
            struct hlist_node *entry, *newpos, *last;
            struct dst_entry *gc_list;
            write_lock_bh(&xfrm_policy_lock);
            // 找到具体的hash链表
            chain = policy_hash_bysel(&policy->selector, policy->family, dir);
            delpol = NULL;
            newpos = NULL;
            last = NULL;
            // 遍历链表, 该链表是以策略的优先级值进行排序的链表, 因此需要根据新策略的优先级大小
            // 将新策略插到合适的位置
            hlist_for_each_entry(pol, entry, chain, bydst)
            {
                // delpol要为空
                if (!delpol &&
                    // 策略类型比较
                    pol->type == policy->type
                    &&
                    // 选择子比较
                    !selector_cmp(&pol->selector, &policy->selector)
                    &&
                    // 安全上下文比较
                    xfrm_sec_ctx_match(pol->security, policy->security))
                {
                    // 新策略和已有的某策略匹配
                    if (excl)
                    {
                        // 如果是排他性添加操作, 要插入的策略在数据库中已经存在, 发生错误
                        write_unlock_bh(&xfrm_policy_lock);
                        return -EEXIST;
                    }
                    // 保存好要删除的策略位置
                    delpol = pol;
                    // 要更新的策略优先级值大于原有的优先级值, 重新循环找到合适的插入位置
                    // 因为这个链表是以优先级值进行排序的, 不能乱
                    // 现在delpol已经非空了,  前面的策略查找条件已经不可能满足了
                    if (policy->priority > pol->priority)
                        continue;
                }
                else if (policy->priority >= pol->priority)
                {
                    // 如果新的优先级不低于当前的优先级, 保存当前节点, 继续查找合适插入位置
                    last = &pol->bydst;
                    continue;
                }
                // 这里是根据新策略的优先级确定的插入位置
                if (!newpos)
                    newpos = &pol->bydst;
                // 如果已经找到要删除的策略, 中断
                if (delpol)
                    break;
                last = &pol->bydst;
            }
            if (!newpos)
                newpos = last;
            // 插入策略到按目的地址HASH的链表的指定位置
            if (newpos)
                hlist_add_after(newpos, &policy->bydst);
            else
                hlist_add_head(&policy->bydst, chain);
            // 增加策略引用计数
            xfrm_pol_hold(policy);
            // 该方向的策略数增1
            xfrm_policy_count[dir]++;
            atomic_inc(&flow_cache_genid);
            // 如果有相同的老策略, 要从目的地址HASH和索引号HASH这两个表中删除
            if (delpol)
            {
                hlist_del(&delpol->bydst);
                hlist_del(&delpol->byidx);
                xfrm_policy_count[dir]--;
            }
            // 获取策略索引号, 插入索引HASH链表
            policy->index = delpol ?
                            delpol->index :
                            xfrm_gen_index(policy->type, dir);
            hlist_add_head(&policy->byidx,
                           xfrm_policy_byidx+idx_hash(policy->index));
            // 策略插入实际时间
            policy->curlft.add_time = (unsigned long)xtime.tv_sec;
            policy->curlft.use_time = 0;
            if (!mod_timer(&policy->timer, jiffies + HZ))
                xfrm_pol_hold(policy);
            write_unlock_bh(&xfrm_policy_lock);
            // 释放老策略
            if (delpol)
                xfrm_policy_kill(delpol);
            else if (xfrm_bydst_should_resize(dir, NULL))
                schedule_work(&xfrm_hash_work);
            // 下面释放所有策略当前的路由cache
            read_lock_bh(&xfrm_policy_lock);
            gc_list = NULL;
            entry = &policy->bydst;
            // 遍历链表, 搜集垃圾路由cache建立链表
            hlist_for_each_entry_continue(policy, entry, bydst)
            {
                struct dst_entry *dst;
                write_lock(&policy->lock);
                // 策略的路由链表头
                dst = policy->bundles;
                if (dst)
                {
                    // 直接将整个策略路由链表加到垃圾链表前面
                    struct dst_entry *tail = dst;
                    while (tail->next)
                        tail = tail->next;
                    tail->next = gc_list;
                    gc_list = dst;
                    // 当前策略的路由为空
                    policy->bundles = NULL;
                }
                write_unlock(&policy->lock);
            }
            read_unlock_bh(&xfrm_policy_lock);
            // 释放垃圾路由cahce
            while (gc_list)
            {
                struct dst_entry *dst = gc_list;
                gc_list = dst->next;
                dst_free(dst);
            }
            return 0;
        }
        EXPORT_SYMBOL(xfrm_policy_insert);
    5.3  删除某类型的全部安全策略
        该函数被pfkey_spdflush()等函数调用
        void xfrm_policy_flush(u8 type)
        {
            int dir;
            write_lock_bh(&xfrm_policy_lock);
            for (dir = 0; dir < XFRM_POLICY_MAX; dir++)
            {
                struct xfrm_policy *pol;
                struct hlist_node *entry;
                int i, killed;
                killed = 0;
                again1:
                    // 遍历inexact HASH链表
                    hlist_for_each_entry(pol, entry,
                                         &xfrm_policy_inexact[dir], bydst)
                    {
                        // 判断类型
                        if (pol->type != type)
                            continue;
                        // 将策略从bydst链表中断开
                        hlist_del(&pol->bydst);
                        // 将策略从byidt链表中断开
                        hlist_del(&pol->byidx);
                        write_unlock_bh(&xfrm_policy_lock);
                        // 将策略状态置为dead, 并添加到系统的策略垃圾链表进行调度处理准备删除
                        xfrm_policy_kill(pol);
                        killed++;
                        write_lock_bh(&xfrm_policy_lock);
                        goto again1;
                    }
                    // 遍历所有目的HASH链表
                    for (i = xfrm_policy_bydst[dir].hmask; i >= 0; i--)
                    {
                        again2:
                            // 遍历按目的地址HASH的链表
                            hlist_for_each_entry(pol,
                                                 entry,
                                                 xfrm_policy_bydst[dir].table + i,
                                                 bydst)
                            {
                                if
                                (pol->type != type)
                                    continue;
                                // 将节点从链表中断开
                                hlist_del(&pol->bydst);
                                hlist_del(&pol->byidx);
                                write_unlock_bh(&xfrm_policy_lock);
                                // 释放节点
                                xfrm_policy_kill(pol);
                                killed++;
                                write_lock_bh(&xfrm_policy_lock);
                                goto again2;
                            }
                    }
                    xfrm_policy_count[dir] -= killed;
            }
            atomic_inc(&flow_cache_genid);
            write_unlock_bh(&xfrm_policy_lock);
        }
        EXPORT_SYMBOL(xfrm_policy_flush);
        // 策略释放到垃圾链表
        static void xfrm_policy_kill(struct xfrm_policy *policy)
        {
            int dead;
            write_lock_bh(&policy->lock);
            // 保留老的DEAD标志
            dead = policy->dead;
            // 设置策略DEAD标志
            policy->dead = 1;
            write_unlock_bh(&policy->lock);
            // 为什么不在前面判断DEAD呢?
            if (unlikely(dead))
            {
                WARN_ON(1);
                return;
            }
            spin_lock(&xfrm_policy_gc_lock);
            // 将该策略节点从当前链表断开, 插入策略垃圾链表
            hlist_add_head(&policy->bydst,
                           &xfrm_policy_gc_list);
            spin_unlock(&xfrm_policy_gc_lock);
            // 调度策略垃圾策略工作结构
            schedule_work(&xfrm_policy_gc_work);
        }
    5.4 策略查找
        5.4.1 策略查找并删除
            根据选择子和安全上下文查找策略, 可查找策略并删除, 被pfkey_spddelete()函数调用
            struct xfrm_policy *xfrm_policy_bysel_ctx(u8 type, int dir,
                                                      struct xfrm_selector *sel,
                                                      struct xfrm_sec_ctx *ctx, int delete)
            {
                struct xfrm_policy *pol, *ret;
                struct hlist_head *chain;
                struct hlist_node *entry;
                write_lock_bh(&xfrm_policy_lock);
                // 定位HASH表
                chain = policy_hash_bysel(sel, sel->family, dir);
                ret = NULL;
                // 遍历链表
                hlist_for_each_entry(pol, entry, chain, bydst)
                {
                    // 根据类型, 选择子和上下文进行匹配
                    if (pol->type == type && !selector_cmp(sel, &pol->selector)
                        && xfrm_sec_ctx_match(ctx, pol->security))
                    {
                        xfrm_pol_hold(pol);
                        if (delete)
                        {
                            // 要的删除话将策略节点从目的地址HASH链表和索引HASH链表中断开
                            hlist_del(&pol->bydst);
                            hlist_del(&pol->byidx);
                            xfrm_policy_count[dir]--;
                        }
                        ret = pol;
                        break;
                    }
                }
                write_unlock_bh(&xfrm_policy_lock);
                if (ret && delete)
                {
                    // 增加genid
                    atomic_inc(&flow_cache_genid);
                    // 将策略状态置为dead, 并添加到系统的策略垃圾链表进行调度处理准备删除
                    xfrm_policy_kill(ret);
                }
                return ret;
            }
            EXPORT_SYMBOL(xfrm_policy_bysel_ctx);
        5.4.2 按索引号查找并删除
            struct xfrm_policy *xfrm_policy_byid(u8 type, int dir, u32 id, int delete)
            {
                struct xfrm_policy *pol, *ret;
                struct hlist_head *chain;
                struct hlist_node *entry;
                write_lock_bh(&xfrm_policy_lock);
                // 根据索引号定位链表
                chain = xfrm_policy_byidx + idx_hash(id);
                ret = NULL;
                // 遍历链表
                hlist_for_each_entry(pol, entry, chain, byidx)
                {
                    // 策略的类型和索引号相同
                    if (pol->type == type && pol->index == id)
                    {
                        xfrm_pol_hold(pol);
                        // 如果要删除, 将策略节点从链表中删除
                        if (delete)
                        {
                            hlist_del(&pol->bydst);
                            hlist_del(&pol->byidx);
                            xfrm_policy_count[dir]--;
                        }
                        ret = pol;
                        break;
                    }
                }
                write_unlock_bh(&xfrm_policy_lock);
                if (ret && delete)
                {
                    // 增加genid
                    atomic_inc(&flow_cache_genid);
                    // 将策略状态置为dead, 并添加到系统的策略垃圾链表进行调度处理准备删除
                    xfrm_policy_kill(ret);
                }
                return ret;
            }
            EXPORT_SYMBOL(xfrm_policy_byid);
        5.4.3 根据路由查找策略
            // 参数fl是路由相关的结构, 常用于路由查找中
            // 注意返回值是整数, 0成功, 非0失败, 找到的策略通过参数objp进行传递
            static int xfrm_policy_lookup(struct flowi *fl, u16 family, u8 dir,
                                          void **objp, atomic_t **obj_refp)
            {
                struct xfrm_policy *pol;
                int err = 0;
                #ifdef CONFIG_XFRM_SUB_POLICY
                    // 子策略查找, 属于Linux自己的扩展功能, 非标准功能
                    pol = xfrm_policy_lookup_bytype(XFRM_POLICY_TYPE_SUB, 
                                                    fl, family, dir);
                    if (IS_ERR(pol))
                    {
                        err = PTR_ERR(pol);
                        pol = NULL;
                    }
                    if (pol || err)
                        goto end;
                #endif
                // 查找MAIN类型的策略
                pol = xfrm_policy_lookup_bytype(XFRM_POLICY_TYPE_MAIN, 
                                                fl, family, dir);
                if (IS_ERR(pol))
                {
                    err = PTR_ERR(pol);
                    pol = NULL;
                }
                #ifdef CONFIG_XFRM_SUB_POLICY
                    end:
                #endif
                // 将找到的策略赋值给objp返回
                if ((*objp = (void *) pol) != NULL)
                    *obj_refp = &pol->refcnt;
                return err;
            }
            // 按类型查找策略
            static struct xfrm_policy *xfrm_policy_lookup_bytype(u8 type,
                                                                struct flowi *fl,
                                                                u16 family, u8 dir)
            {
                int err;
                struct xfrm_policy *pol, *ret;
                xfrm_address_t *daddr, *saddr;
                struct hlist_node *entry;
                struct hlist_head *chain;
                u32 priority = ~0U;
                // 由流结构的目的和源地址
                daddr = xfrm_flowi_daddr(fl, family);
                saddr = xfrm_flowi_saddr(fl, family);
                if (unlikely(!daddr || !saddr))
                    return NULL;
                read_lock_bh(&xfrm_policy_lock);
                // 根据地址信息查找HASH链表
                chain = policy_hash_direct(daddr, saddr, family, dir);
                ret = NULL;
                // 循环HASH链表
                hlist_for_each_entry(pol, entry, chain, bydst)
                {
                    // 检查流结构,类型和协议族是否匹配策略, 返回0表示匹配
                    err = xfrm_policy_match(pol, fl, type, family, dir);
                    if (err)
                    {
                        if (err == -ESRCH)
                            continue;
                        else
                        {
                            ret = ERR_PTR(err);
                            goto fail;
                        }
                    }
                    else
                    {
                        // 备份找到的策略和优先级
                        ret = pol;
                        priority = ret->priority;
                        break;
                    }
                }
                // 再在inexact链表中查找策略, 如果也找到策略, 而且优先级更小,
                // 将新找到的策略替代前面找到的策略
                chain = &xfrm_policy_inexact[dir];
                // 循环HASH链表
                hlist_for_each_entry(pol, entry, chain, bydst)
                {
                    // 检查流结构,类型和协议族是否匹配策略, 返回0表示匹配
                    err = xfrm_policy_match(pol, fl, type, family, dir);
                    if (err)
                    {
                        if (err == -ESRCH)
                            continue;
                        else
                        {
                            ret = ERR_PTR(err);
                            goto fail;
                        }
                    }
                    else if (pol->priority < priority)
                    {
                        // 如果新找到的策略优先级更小, 将其取代原来找到的策略
                        ret = pol;
                        break;
                    }
                }
                if (ret)
                    xfrm_pol_hold(ret);
                fail:
                    read_unlock_bh(&xfrm_policy_lock);
                    return ret;
            }
            // 检查xfrm策略是否和流参数匹配
            // 返回0表示匹配成功
            static int xfrm_policy_match(struct xfrm_policy *pol, struct flowi
                                         *fl,
                                         u8 type, u16 family, int dir)
            {
                // 选择子
                struct xfrm_selector *sel = &pol->selector;
                int match, ret = -ESRCH;
                // 检查策略协议族和类型是否匹配
                if (pol->family != family || pol->type != type)
                    return ret;
                // 检查选择子是否匹配, 返回非0值表示匹配成功
                match = xfrm_selector_match(sel, fl, family);
                if (match)
                    // 这种security函数可以不用考虑, 当作返回0的函数即可
                    ret = security_xfrm_policy_lookup(pol, fl->secid, dir);
                return ret;
            }
            // 选择子匹配,分别对IPV4和IPV6协议族比较
            static inline int
            xfrm_selector_match(struct xfrm_selector *sel, struct flowi
                                *fl, unsigned short family)
            {
                switch (family)
                {
                    case AF_INET:
                        return
                            __xfrm4_selector_match(sel, fl);
                    case AF_INET6:
                        return
                            __xfrm6_selector_match(sel, fl);
                }
                return 0;
            }
            //IPV4协议族选择子比较
            static inline int
            __xfrm4_selector_match(struct xfrm_selector *sel, struct flowi
                                   *fl)
            {
                // 比较V4目的地址, V4源地址, 目的端口, 源端口, 协议, 网卡索引号
                return
                    addr_match(&fl->fl4_dst, &sel->daddr, sel->prefixlen_d)
                    && addr_match(&fl->fl4_src, &sel->saddr, sel->prefixlen_s)
                    && !((xfrm_flowi_dport(fl) ^ sel->dport) & sel->dport_mask)
                    && !((xfrm_flowi_sport(fl) ^ sel->sport) & sel->sport_mask)
                    && (fl->proto == sel->proto || !sel->proto)
                    && (fl->oif == sel->ifindex || !sel->ifindex);
            }
            //IPV6协议族选择子比较
            static inline int
            __xfrm6_selector_match(struct xfrm_selector *sel, struct flowi
                                   *fl)
            {
                // 比较V6目的地址, V6源地址, 目的端口, 源端口, 协议, 网卡索引号
                return addr_match(&fl->fl6_dst, &sel->daddr, sel->prefixlen_d)
                    && addr_match(&fl->fl6_src, &sel->saddr, sel->prefixlen_s)
                    && !((xfrm_flowi_dport(fl) ^ sel->dport) & sel->dport_mask)
                    && !((xfrm_flowi_sport(fl) ^ sel->sport) &  sel->sport_mask)
                    && (fl->proto == sel->proto || !sel->proto)
                    && (fl->oif == sel->ifindex || !sel->ifindex);
            }
        5.4.4 查找和sock对应的策略
            static struct xfrm_policy *xfrm_sk_policy_lookup(struct sock *sk, int dir,
                                                             struct flowi *fl)
            {
                struct xfrm_policy *pol;
                read_lock_bh(&xfrm_policy_lock);
                // sock结构中有sk_policy用来指向双向数据的安全策略
                if ((pol = sk->sk_policy[dir]) != NULL)
                {
                    // 检查该策略的选择子是否和流结构匹配
                    int match = xfrm_selector_match(&pol->selector,
                                                    fl,
                                                    sk->sk_family);
                    int err = 0;
                    // 如果匹配的话将策略作为结果返回
                    if (match)
                    {
                        // 这个security函数可视为返回0的空函数
                        err = security_xfrm_policy_lookup(pol, fl->secid,
                                                        policy_to_flow_dir(dir));
                        if (!err)
                            xfrm_pol_hold(pol);
                        else if (err == -ESRCH)
                            pol = NULL;
                        else
                            pol = ERR_PTR(err);
                    }
                    else
                        pol = NULL;
                }
                read_unlock_bh(&xfrm_policy_lock);
                return pol;
            }
    5.5 遍历安全策略
        该函数被pfkey_spddump()等函数中调用
        // func函数用来指定对遍历的策略进行的查找
        // 实际遍历了两次所有策略
        int xfrm_policy_walk(u8 type, 
                             int (*func)(struct xfrm_policy *, int, int, void*),
                             void *data)
        {
            struct xfrm_policy *pol;
            struct hlist_node *entry;
            int dir, count, error;
            read_lock_bh(&xfrm_policy_lock);
            count = 0;
            // 先统计符合类型的策略的总数量, 方向是双向的
            for (dir = 0; dir < 2*XFRM_POLICY_MAX; dir++)
            {
                struct hlist_head *table = xfrm_policy_bydst[dir].table;
                int i;
                // inexact HASH表
                hlist_for_each_entry(pol, entry,
                                     &xfrm_policy_inexact[dir], bydst)
                {
                    if (pol->type == type)
                        count++;
                }
                // 遍历按地址HASH的链表
                for (i = xfrm_policy_bydst[dir].hmask; i >= 0; i--)
                {
                    // 遍历链表
                    hlist_for_each_entry(pol, entry, table + i, bydst)
                    {
                        if (pol->type == type)
                            count++;
                    }
                }
            }
            if (count == 0)
            {
                error = -ENOENT;
                goto out;
            }
            // 重新遍历HASH表, 当前的count值作为SA的序号, 因此用户空间收到的序号是递减的
            for (dir = 0; dir < 2*XFRM_POLICY_MAX; dir++)
            {
                struct hlist_head *table = xfrm_policy_bydst[dir].table;
                int i;
                // 遍历inexact链表
                hlist_for_each_entry(pol, entry,
                                     &xfrm_policy_inexact[dir], bydst)
                {
                    if  (pol->type != type)
                        continue;
                    // 对符合类型的策略调用func函数
                    error = func(pol, dir % XFRM_POLICY_MAX, --count, data);
                    if (error)
                        goto out;
                }
                // 遍历按地址HASH的链表
                for (i = xfrm_policy_bydst[dir].hmask; i >= 0; i--)
                {
                    hlist_for_each_entry(pol, entry, table + i, bydst)
                    {
                        if (pol->type != type)
                            continue;
                        // 对符合类型的策略调用func函数, 当count递减到0时表示是最后一个策略了
                        error = func(pol, dir % XFRM_POLICY_MAX, --count, data);
                        if (error)
                            goto out;
                    }
                }
            }
            error = 0;
            out:
                read_unlock_bh(&xfrm_policy_lock);
                return error;
        }
        EXPORT_SYMBOL(xfrm_policy_walk);
    5.6 策略检查
        __xfrm_policy_check函数也是一个比较重要的函数, 被xfrm_policy_check()调用,
        又被xfrm4_policy_check()和xfrm6_policy_check()调用,
        而这两个函数在网络层的输入和转发处调用.
        对普通包就返回合法, 对IPSEC包检查策略是否合法, 是否和路由方向匹配
        // 返回1表示合法, 0表示不合法, 对于该函数返回0的数据包通常是被丢弃
        int __xfrm_policy_check(struct sock *sk, int dir, struct sk_buff
                                *skb, unsigned short family)
        {
            struct xfrm_policy *pol;
            struct xfrm_policy *pols[XFRM_POLICY_TYPE_MAX];
            int npols = 0;
            int xfrm_nr;
            int pi;
            struct flowi fl;
            // 将策略方向转换为流方向, 其实值是一样的
            u8 fl_dir = policy_to_flow_dir(dir);
            int xerr_idx = -1;
            // 调用协议族的decode_session()函数, 对IPV4来说就是_decode_session4
            // 将skb中的地址端口等信息填入流结构fl中
            if (xfrm_decode_session(skb, &fl, family) < 0)
                return 0;
            // 如果内核支持NETFILTER, 将调用ip_nat_decode_session函数填写NAT信息
            // 否则的话就是个空函数
            nf_nat_decode_session(skb, &fl, amily);
            if (skb->sp)
            {
                // 该包是进行了解密后的IPSEC包
                int i;
                for (i=skb->sp->len-1; i>=0; i--)
                {
                    // 获取该包相关的SA信息
                    struct xfrm_state *x = skb->sp->xvec[i];
                    // 检查SA选择子和流参数(路由)是否匹配, 结果为0表示不匹配, 不匹配的话返回
                    if (!xfrm_selector_match(&x->sel, &fl, family))
                        return 0;
                }
            }
            pol = NULL;
            // 如果sock结构中有策略
            if (sk && sk->sk_policy[dir])
            {
                // 检查策略是否和流结构匹配, 匹配的话返回策略
                pol = xfrm_sk_policy_lookup(sk, dir, &fl);
                if (IS_ERR(pol))
                    return 0;
            }
            // 查找路由信息, 如果没有就创建路由, xfrm_policy_lookup()函数作为参数传递给
            // flow_cache_lookup()函数, 查找和该路由对应的安全策略
            if (!pol)
                pol = flow_cache_lookup(&fl, family, fl_dir, xfrm_policy_lookup);
            // 查找过程中出错,返回0
            if (IS_ERR(pol))
                return 0;
            // 策略不存在
            if (!pol)
            {
                // 如果该包是IPSEC包而且安全路径中的SA不是传输模式,
                // 转发时, 对于已经封装的包没必要再次封装;
                // 输入时, 是自身的IPSEC通信包封装基本也无意义
                if (skb->sp &&
                    secpath_has_nontransport(skb->sp, 0, &xerr_idx))
                {
                    // 拒绝该安全路径, 返回0失败
                    xfrm_secpath_reject(xerr_idx, skb, &fl);
                    return 0;
                }
                // 普通包处理, 安全策略不存在, 返回1
                return 1;
            }
            // 找到安全策略, 对该包要根据策略进行IPSEC处理
            // 更新策略当前使用时间
            pol->curlft.use_time = (unsigned long)xtime.tv_sec;
            pols[0] = pol;
            npols ++;
            #ifdef CONFIG_XFRM_SUB_POLICY
                // 如果定义了子策略的话极限查找子策略, 这是标准IPSEC中没定义的, 可以不考虑
                if (pols[0]->type != XFRM_POLICY_TYPE_MAIN)
                {
                    pols[1] = xfrm_policy_lookup_bytype(XFRM_POLICY_TYPE_MAIN,
                                                        &fl, family,
                                                        XFRM_POLICY_IN);
                    if (pols[1])
                    {
                        if (IS_ERR(pols[1]))
                            return 0;
                        pols[1]->curlft.use_time = (unsigned long)xtime.tv_sec;
                        npols ++;
                    }
                }
            #endif
            // 策略动作是允许通过
            if (pol->action == XFRM_POLICY_ALLOW)
            {
                struct sec_path *sp;
                // 先伪造个安全路径
                static struct sec_path dummy;
                struct xfrm_tmpl *tp[XFRM_MAX_DEPTH];
                struct xfrm_tmpl *stp[XFRM_MAX_DEPTH];
                struct xfrm_tmpl **tpp = tp;
                int ti = 0;
                int i, k;
                // 如果数据包没有安全路径, 路径指针初始化为伪造的安全路径
                if ((sp = skb->sp) == NULL)
                    sp = &dummy;
                // 遍历策略数组, 包括主策略和子策略(内核支持子策略的话),一般情况下就一个策略
                for (pi = 0; pi
                        < npols; pi++)
                {
                    // 如果有非允许通过的其他安全策略, 放弃
                    if (pols[pi] != pol && pols[pi]->action != XFRM_POLICY_ALLOW)
                        goto reject;
                    // 如果策略层次太多, 放弃
                    if (ti + pols[pi]->xfrm_nr >= XFRM_MAX_DEPTH)
                        goto reject_error;
                    // 备份策略中的xfrm向量模板, ti是数量
                    for (i = 0; i < pols[pi]->xfrm_nr; i++)
                        tpp[ti++] = &pols[pi]->xfrm_vec[i];
                }
                // 策略数量
                xfrm_nr = ti;
                if (npols > 1)
                {
                    // 如果超过一个策略,进行排序, 只是在内核支持子系统时才用, 否则只是返回错误
                    // 但该错误可以忽略
                    xfrm_tmpl_sort(stp, tpp, xfrm_nr, family);
                    tpp = stp;
                }
                // 遍历检查策略模板是否OK
                for (i = xfrm_nr-1, k = 0; i >= 0; i--)
                {
                    // 注意k既是输入, 也是输出值, k初始化为0
                    // 返回值大于等于0表示策略合法可用
                    k = xfrm_policy_ok(tpp[i], sp, k, family);
                    if (k < 0)
                    {
                        if (k < -1) 
                            xerr_idx = -(2+k);
                        goto reject;
                    }
                }
                // 存在非传输模式的策略, 放弃
                if (secpath_has_nontransport(sp, k, &xerr_idx))
                    goto reject;
                xfrm_pols_put(pols, npols);
                return 1;
            }
            // 放弃, 返回0表示检查不通过
            reject:
                xfrm_secpath_reject(xerr_idx, skb, &fl);
            reject_error:
                xfrm_pols_put(pols, npols);
                return 0;
        }
        EXPORT_SYMBOL(__xfrm_policy_check);
        static inline int xfrm_policy_ok(struct xfrm_tmpl *tmpl, 
                                         struct sec_path *sp, 
                                         int start,
                                         unsigned short family)
        {
            int idx = start;
            if (tmpl->optional)
            {
                // 如果是传输模式, 直接返回
                if (tmpl->mode == XFRM_MODE_TRANSPORT)
                    return start;
            }
            else
                start = -1;
            for (; idx < sp->len; idx++)
            {
                // sp->xvec是xfrm状态
                // 如果安全路径和模板匹配,返回索引位置
                if (xfrm_state_ok(tmpl,
                                  sp->xvec[idx], family))
                    return  ++idx;
                // 如果安全路径中的SA不是传输模式,返回错误
                if (sp->xvec[idx]->props.mode != XFRM_MODE_TRANSPORT)
                {
                    if (start == -1)
                        start = -2-idx;
                    break;
                }
            }
            return start;
        }
    5.7 安全策略路由查找
        xfrm_lookup函数是个非常重要的函数, 用来根据安全策略构造数据包的路由项链表,
        该路由项链表反映了对数据包进行IPSEC封装的多层次的处理, 每封装一次, 就增加一个路由项.
        该函数被路由查找函数ip_route_output_flow()调用, 针对的是转发或发出的数据包.
        // 返回0表示超过, 负数表示失败
        int xfrm_lookup(struct dst_entry **dst_p, struct flowi *fl,
                        struct sock *sk, int flags)
        {
            struct xfrm_policy *policy;
            struct xfrm_policy *pols[XFRM_POLICY_TYPE_MAX];
            int npols;
            int pol_dead;
            int xfrm_nr;
            int pi;
            struct xfrm_state *xfrm[XFRM_MAX_DEPTH];
            struct dst_entry *dst, *dst_orig = *dst_p;
            int nx = 0;
            int err;
            u32 genid;
            u16 family;
            u8 dir =
                policy_to_flow_dir(XFRM_POLICY_OUT);
            restart:
            // 初始化清零操作
            genid =
                atomic_read(&flow_cache_genid);
            policy = NULL;
            for (pi = 0; pi < ARRAY_SIZE(pols); pi++)
                pols[pi] = NULL;
            npols = 0;
            pol_dead = 0;
            xfrm_nr = 0;
            if (sk && sk->sk_policy[1])
            {
                // 如果在sock中定义了安全策略, 查找该sock相关的策略
                // 一个socket的安全策略可通过setsockopt()设置, socket选项为
                // IP_IPSEC_POLICY或IP_XFRM_POLICY(net/ipv4/ip_sockglue.c)
                policy = xfrm_sk_policy_lookup(sk, XFRM_POLICY_OUT, fl);
                if (IS_ERR(policy))
                    return PTR_ERR(policy);
            }
            if (!policy)
            {
                // 没找到sock自身定义的安全策略
                // 如果初始路由中设置了非IPSEC标志或没有发出方向的安全策略, 直接返回
                if ((dst_orig->flags & DST_NOXFRM) ||
                    !xfrm_policy_count[XFRM_POLICY_OUT])
                    return 0;
                // 查找路由信息, 如果没有就创建路由, xfrm_policy_lookup()函数作为参数传递给
                // flow_cache_lookup()函数, 查找和该路由对应的安全策略
                policy = flow_cache_lookup(fl, dst_orig->ops->family,
                                           dir, xfrm_policy_lookup);
                if (IS_ERR(policy))
                    return PTR_ERR(policy);
            }
            // 找不到策略的话返回, 就是普通包普通路由项
            if (!policy)
                return 0;
            // 以下是存在安全策略的情况, 要对该包建立安全路由链表
            // 初始路由的协议族
            family = dst_orig->ops->family;
            // 安全策略最近使用时间
            policy->curlft.use_time = (unsigned long)xtime.tv_sec;
            // 将找到的策略作为策略数组的第一项
            pols[0] = policy;
            npols ++;
            xfrm_nr += pols[0]->xfrm_nr;
            // 根据策略操作结果进行相关处理, 只有两种情况: 阻塞或通过
            switch (policy->action)
            {
                case XFRM_POLICY_BLOCK:
                    // 阻塞该数据包, 返回错误
                    err = -EPERM;
                    goto error;
                case XFRM_POLICY_ALLOW:
                    // 允许该包通过, 这样就要对该包进行IPSEC处理
                    #ifndef CONFIG_XFRM_SUB_POLICY
                        // 对子策略操作忽略
                        if
                        (policy->xfrm_nr == 0)
                        {
                            xfrm_pol_put(policy);
                            return 0;
                        }
                    #endif
                    // 查找是否已经存在安全路由, bundle可以理解为描述安全处理的安全路由, 数据包走该路由
                    // 就是进行某种安全封装, 和普通路由项一样, 用过的安全路由也被缓存起来
                    dst = xfrm_find_bundle(fl, policy, family);
                    if (IS_ERR(dst))
                    {
                        err = PTR_ERR(dst);
                        goto error;
                    }
                    // 如果找到安全路由, 退出switch
                    if (dst)
                        break;
                    #ifdef CONFIG_XFRM_SUB_POLICY
                        // 对子策略操作, 由于是非标准IPSEC,忽略
                        if (pols[0]->type != XFRM_POLICY_TYPE_MAIN)
                        {
                            pols[1] = xfrm_policy_lookup_bytype(XFRM_POLICY_TYPE_MAIN,
                                                                fl, family,
                                                                XFRM_POLICY_OUT);
                            if (pols[1])
                            {
                                if (IS_ERR(pols[1]))
                                {
                                    err = PTR_ERR(pols[1]);
                                    goto error;
                                }
                                if
                                (pols[1]->action == XFRM_POLICY_BLOCK)
                                {
                                    err = -EPERM;
                                    goto error;
                                }
                                npols ++;
                                xfrm_nr += pols[1]->xfrm_nr;
                            }
                        }
                        if (xfrm_nr == 0)
                        {
                            xfrm_pols_put(pols, npols);
                            return 0;
                        }
                    #endif
                    // 没找到安全路由, 准备构造新的路由项
                    // 利用策略, 流等参数构造相关SA(xfrm_state)保存在xfrm中, nx为SA数量
                    nx = xfrm_tmpl_resolve(pols, npols, fl, xfrm, family);
                    if (unlikely(nx<0))
                    {
                        // nx<0表示失败, 没找到SA
                        // 但如果是-EAGAIN表示已经通知用户空间的IKE进行协商新的SA了,
                        // 目前只生成了ACQUIRE类型的xfrm_state
                        err = nx;
                        if (err == -EAGAIN && flags)
                        {
                            // 进程进入阻塞状态
                            DECLARE_WAITQUEUE(wait, current);
                            add_wait_queue(&km_waitq, &wait);
                            set_current_state(TASK_INTERRUPTIBLE);
                            schedule();
                            set_current_state(TASK_RUNNING);
                            remove_wait_queue(&km_waitq, &wait);
                            // 阻塞解除, 重新解析SA
                            nx = xfrm_tmpl_resolve(pols, npols, fl, xfrm, family);
                            if (nx == -EAGAIN && signal_pending(current))
                            {
                                err = -ERESTART;
                                goto error;
                            }
                            if (nx == -EAGAIN || genid != atomic_read(&flow_cache_genid))
                            {
                                xfrm_pols_put(pols, npols);
                                goto restart;
                            }
                            err = nx;
                        }
                        if (err < 0)
                            goto error;
                    }
                    if (nx == 0)
                    {
                        // nx==0表示数据是不需要进行IPSEC处理的, 返回
                        xfrm_pols_put(pols, npols);
                        return 0;
                    }
                    // 保存初始路由
                    dst = dst_orig;
                    // 创建新的安全路由, 返回0 表示成功, 失败返回负数
                    // dst在成功返回时保存安全路由项, 每个SA处理对应一个安全路由, 这些安全路由通过
                    // 路由项中的child链接为一个链表, 这样就可以对数据包进行连续变换, 如先压缩,
                    // 再ESP封装, 再AH封装等.
                    // 路由项链表的构造和协议族相关, 后续文章中介绍具体协议族中的实现时再详细描述
                    // 所构造出的路由项的具体结构情况
                    err = xfrm_bundle_create(policy, xfrm, nx, fl, &dst, family);
                    if (unlikely(err))
                    {
                        // 失败的话释放刚获取的SA
                        int i;
                        for (i=0; i<nx; i++) 
                            xfrm_state_put(xfrm[i]);
                        goto error;
                    }
                    // 检查所有策略的dead状态
                    for (pi = 0; pi < npols; pi++)
                    {
                        read_lock_bh(&pols[pi]->lock);
                        pol_dead |= pols[pi]->dead;
                        read_unlock_bh(&pols[pi]->lock);
                    }
                    write_lock_bh(&policy->lock);
                    // 如果有策略是dead或获取的安全路由项有问题, 释放安全路由
                    if (unlikely(pol_dead ||
                                 stale_bundle(dst)))
                    {
                        write_unlock_bh(&policy->lock);
                        if (dst)
                            dst_free(dst);
                        err = -EHOSTUNREACH;
                        goto error;
                    }
                    // 将安全路由加入到策略的路由项链表头, 该链表是以NULL结尾的单向链表
                    // 不过一般情况下应该只有一个元素
                    dst->next = policy->bundles;
                    policy->bundles = dst;
                    dst_hold(dst);
                    write_unlock_bh(&policy->lock);
            }
            // 将安全链表作为
            *dst_p = dst;
            dst_release(dst_orig);
            xfrm_pols_put(pols, npols);
            return 0;
            error:
                dst_release(dst_orig);
                xfrm_pols_put(pols, npols);
                *dst_p = NULL;
                return err;
        }
        EXPORT_SYMBOL(xfrm_lookup);
        以下是在xfrm_lookup中用到的两个bundle的操作函数:
        查找和创建, 由于使用了地址参数, 是和协议族相关的,
        因此具体实现是在各协议族中实现的, 在后续文章中介绍协议族中的xfrm实现时再详细介绍.
        static struct dst_entry *
        xfrm_find_bundle(struct flowi *fl, struct xfrm_policy *policy,
                         unsigned short family)
        {
            struct dst_entry *x;
            struct xfrm_policy_afinfo *afinfo = xfrm_policy_get_afinfo(family);
            if (unlikely(afinfo == NULL))
                return ERR_PTR(-EINVAL);
            x = afinfo->find_bundle(fl,
                                    policy);
            xfrm_policy_put_afinfo(afinfo);
            return x;
        }
        static int xfrm_bundle_create( struct xfrm_policy *policy, struct xfrm_state
                                       **xfrm, int nx,
                                       struct flowi *fl, struct dst_entry **dst_p,
                                       unsigned short family)
        {
            int err;
            struct xfrm_policy_afinfo *afinfo = xfrm_policy_get_afinfo(family);
            if (unlikely(afinfo == NULL))
                return -EINVAL;
            err = afinfo->bundle_create(policy, xfrm, nx, fl, dst_p);
            xfrm_policy_put_afinfo(afinfo);
            return err;
        }
        // 策略解析, 生成SA
        static int xfrm_tmpl_resolve( struct xfrm_policy **pols, 
                                      int npols, struct
                                      flowi *fl,
                                      struct
                                      xfrm_state **xfrm,
                                      unsigned
                                      short family)
        {
            struct xfrm_state *tp[XFRM_MAX_DEPTH];
            // npols > 1是定义了子策略的情况, 这时用tp数组保存找到的SA,
            但没法返回原函数中了
            // 不明白为什么这么作
            struct xfrm_state **tpp = (npols > 1) ? tp : xfrm;
            int cnx = 0;
            int error;
            int ret;
            int i;
            // 遍历策略, 一般情况下npols其实只是1
            for (i = 0; i < npols; i++)
            {
                // 检查保存SA的缓冲区是否还够大
                if (cnx + pols[i]->xfrm_nr >= XFRM_MAX_DEPTH)
                {
                    error = -ENOBUFS;
                    goto fail;
                }
                // 协议一个策略模板
                ret =  xfrm_tmpl_resolve_one(pols[i], fl, &tpp[cnx], family);
                if (ret < 0)
                {
                    error = ret;
                    goto fail;
                }
                else
                    cnx += ret;
            }
            // 多个策略的话对找到的SA排序, 在没定义子策略的情况下是个空函数
            if (npols > 1)
                xfrm_state_sort(xfrm, tpp, cnx,
                                family);
            return cnx;
            fail:
                for (cnx--; cnx>=0; cnx--)
                    xfrm_state_put(tpp[cnx]);
                return error;
        }
        static int
        xfrm_tmpl_resolve_one(struct xfrm_policy *policy, struct flowi
                              *fl,
                              struct xfrm_state **xfrm,
                              unsigned short family)
        {
            int nx;
            int i, error;
            // 从流结构中获取地址信息
            xfrm_address_t *daddr = xfrm_flowi_daddr(fl,
                                    family);
            xfrm_address_t *saddr = xfrm_flowi_saddr(fl,
                                    family);
            xfrm_address_t tmp;
            // 遍历策略中的所有SA
            for (nx=0, i = 0; i <
                    policy->xfrm_nr; i++)
            {
                struct xfrm_state *x;
                xfrm_address_t *remote =
                    daddr;
                xfrm_address_t
                *local  = saddr;
                struct xfrm_tmpl *tmpl =
                            &policy->xfrm_vec[i];
                if (tmpl->mode == XFRM_MODE_TUNNEL)
                {
                    // 如果是通道模式, 会添加外部IP头, 内部IP头都封装在内部, 因此地址信息使用外部地址
                    // 即策略的SA模板中的地址信息
                    remote =
                        &tmpl->id.daddr;
                    local =
                        &tmpl->saddr;
                    // 如果local地址没定义, 选取个源地址作为本地地址, 选取过程是协议族相关的
                    if
                    (xfrm_addr_any(local, family))
                    {
                        error
                        = xfrm_get_saddr(&tmp, remote, family);
                        if
                        (error)
                            goto
                            fail;
                        local
                        = &tmp;
                    }
                }
                // 根据地址,流,策略等新查找SA(xfrm_state),如果找不到现成的会通知IKE程序进行协商
                // 生成新的SA, 但生成可用SA前先返回ACQUIRE类型的SA, 见前一篇文章
                x = xfrm_state_find(remote, local, fl, tmpl, policy, &error, family);
                if (x && x->km.state == XFRM_STATE_VALID)
                {
                    // 如果SA是合法, 保存
                    xfrm[nx++] = x;
                    daddr = remote;
                    saddr =  local;
                    continue;
                }
                if (x)
                {
                    // x存在但不是VALID的, 只要不出错, 应该是ACQUIRE类型的, 等IKE进程协商结果, 返回-EAGAIN
                    error = (x->km.state == XFRM_STATE_ERROR ? -EINVAL : -EAGAIN);
                    xfrm_state_put(x);
                }
                if (!tmpl->optional)
                    goto fail;
            }
            return nx;
            fail:
                for (nx--; nx>=0; nx--)
                    xfrm_state_put(xfrm[nx]);
                return error;
        }
        关于路由处理过程在后面介绍IPSEC包的发出过程时会介绍路由处理过程, 从而了解安全路由的作用.
    5.8 变更HASH表大小
        改变策略状态表的是通过工作队列来实现的, 和xfrm_state类似
        工作定义:
        static DECLARE_WORK(xfrm_hash_work, xfrm_hash_resize, NULL);
        // 更改HASH表大小
        static void xfrm_hash_resize(void *__unused)
        {
            int dir, total;
            mutex_lock(&hash_resize_mutex);
            total = 0;
            // 注意策略都是双向的
            for (dir = 0; dir < XFRM_POLICY_MAX * 2; dir++)
            {
                // 按目的地址进行HASH的链表: 如果需要更改HASH表大小, 修改之
                if (xfrm_bydst_should_resize(dir, &total))
                    xfrm_bydst_resize(dir);
            }
            // 按索引号进行HASH的链表更新
            if (xfrm_byidx_should_resize(total))
                xfrm_byidx_resize(total);
            mutex_unlock(&hash_resize_mutex);
        }
        // 检查按目的地址HASH的HASH链表
        static inline int xfrm_bydst_should_resize(int dir, int
                *total)
        {
            // 该方向是策略的数量
            unsigned int cnt = xfrm_policy_count[dir];
            // 该方向是策略的掩码
            unsigned int hmask = xfrm_policy_bydst[dir].hmask;
            // 累加策略数量
            if (total)
                *total += cnt;
            // 如果策略数量大于策略掩码量, 该增加了
            if ((hmask + 1) < xfrm_policy_hashmax &&
                cnt > hmask)
                return 1;
            // 否则不用
            return 0;
        }
        // 检查按索引号HASH的HASH链表
        static inline int xfrm_byidx_should_resize(int total)
        {
            unsigned int hmask = xfrm_idx_hmask;
            // 策略总量超过当前的索引号掩码, 该扩大了
            if ((hmask + 1) < xfrm_policy_hashmax &&
                total > hmask)
                return 1;
            return 0;
        }
        // 更改按目的地址HASH的HASH链表大小
        static void xfrm_bydst_resize(int dir)
        {
            // 该方向的HASH表掩码(最大值, 一般是2^N-1)
            unsigned int hmask =
                xfrm_policy_bydst[dir].hmask;
            // 新HASH表掩码(2^(N+1)-1)
            unsigned int nhashmask = xfrm_new_hash_mask(hmask);
            // 新HASH表大小
            unsigned int nsize = (nhashmask + 1) *
                                 sizeof(struct hlist_head);
            // 老HAHS表
            struct hlist_head *odst = xfrm_policy_bydst[dir].table;
            // 新HASH表
            struct hlist_head *ndst = xfrm_hash_alloc(nsize);
            int i;
            // 新HASH表空间分配不出来, 返回
            if (!ndst)
                return;
            write_lock_bh(&xfrm_policy_lock);
            // 将所有策略节点转到新HASH表
            for (i = hmask; i >= 0; i--)
                xfrm_dst_hash_transfer(odst + i, ndst, nhashmask);
            // 将全局变量值更新为新HASH表参数
            xfrm_policy_bydst[dir].table = ndst;
            xfrm_policy_bydst[dir].hmask = nhashmask;
            write_unlock_bh(&xfrm_policy_lock);
            // 释放老HASH表参数
            xfrm_hash_free(odst, (hmask + 1) * sizeof(struct hlist_head));
        }
        // 更改按索引号HASH的HASH链表大小, 操作和上面类似
        static void xfrm_byidx_resize(int total)
        {
            unsigned int hmask = xfrm_idx_hmask;
            unsigned int nhashmask = xfrm_new_hash_mask(hmask);
            unsigned int nsize = (nhashmask + 1) *
                                 sizeof(struct hlist_head);
            struct hlist_head *oidx = xfrm_policy_byidx;
            struct hlist_head *nidx = xfrm_hash_alloc(nsize);
            int i;
            if (!nidx)
                return;
            write_lock_bh(&xfrm_policy_lock);
            for (i = hmask; i >= 0; i--)
                xfrm_idx_hash_transfer(oidx + i, nidx, nhashmask);
            xfrm_policy_byidx = nidx;
            xfrm_idx_hmask = nhashmask;
            write_unlock_bh(&xfrm_policy_lock);
            xfrm_hash_free(oidx, (hmask + 1) * sizeof(struct hlist_head));
        }
    5.9 垃圾搜集
        垃圾搜集的是不用的安全路由项, 是和协议族相关的
        afinfo->garbage_collect =
            __xfrm_garbage_collect;
        // 就是xfrm_prune_bundles()函数的包装函数,条件是unused_bundle()函数定义
        static void __xfrm_garbage_collect(void)
        {
            xfrm_prune_bundles(unused_bundle);
        }
        // 删减安全路由
        static void xfrm_prune_bundles(int (*func)(struct dst_entry
                                       *))
        {
            // 垃圾链表
            struct dst_entry *gc_list = NULL;
            int dir;
            read_lock_bh(&xfrm_policy_lock);
            // 循环所有方向
            for (dir = 0; dir <
                    XFRM_POLICY_MAX * 2; dir++)
            {
                struct xfrm_policy *pol;
                struct hlist_node *entry;
                struct hlist_head *table;
                int i;
                // 遍历inexact链表
                hlist_for_each_entry(pol,
                                     entry,
                                     &xfrm_policy_inexact[dir], bydst)
                // 如果节点满足条件就删除挂接到垃圾链表
                prune_one_bundle(pol,
                                 func, &gc_list);
                // 遍历目的地址HASH的链表
                table =
                    xfrm_policy_bydst[dir].table;
                for (i =
                            xfrm_policy_bydst[dir].hmask; i >= 0; i--)
                {
                    // 如果节点满足条件就删除挂接到垃圾链表
                    hlist_for_each_entry(pol,
                                         entry, table + i, bydst)
                    prune_one_bundle(pol,
                                     func, &gc_list);
                }
            }
            read_unlock_bh(&xfrm_policy_lock);
            // 如果搜集到的垃圾, 释放安全路由
            while (gc_list)
            {
                struct dst_entry *dst =
                            gc_list;
                gc_list =
                    dst->next;
                dst_free(dst);
            }
        }
        // 没用的路由, 使用数为0
        static int unused_bundle(struct dst_entry *dst)
        {
            return
                !atomic_read(&dst->__refcnt);
        }
        // 删除单个路由
        static void prune_one_bundle(struct xfrm_policy *pol, int
                                     (*func)(struct dst_entry *), struct dst_entry **gc_list_p)
        {
            struct dst_entry *dst, **dstp;
            // 策略写锁
            write_lock(&pol->lock);
            // 策略的路由项链表起点
            dstp =
                &pol->bundles;
            // 遍历链表
            while ((dst=*dstp) != NULL)
            {
                if (func(dst))
                {
                    // 如果满足条件, 将节点从链表中删除, 添加到垃圾链表
                    *dstp =
                        dst->next;
                    dst->next
                    = *gc_list_p;
                    *gc_list_p =
                        dst;
                }
                else
                {
                    dstp =
                        &dst->next;
                }
            }
            write_unlock(&pol->lock);
        }
    5.10 杂项
        这些杂项并不是策略的直接处理函数, 而是xfrm的一些相关处理, 只是也放在xfrm_policy.c中了.
        5.10.1 协议处理类型处理
            xfrm_type用来定义各种协议处理类型, 如AH,ESP, IPCOMP, IPIP等
            // 登记协议处理类型, 返回0成功, 非0失败
            int xfrm_register_type(struct xfrm_type *type, unsigned short
                                   family)
            {
                // 找到协议族相关的策略信息结构
                struct xfrm_policy_afinfo *afinfo =
                    xfrm_policy_lock_afinfo(family);
                struct xfrm_type **typemap;
                int err = 0;
                if (unlikely(afinfo == NULL))
                    return -EAFNOSUPPORT;
                // 策略信息结构中的类型数组
                typemap = afinfo->type_map;
                // 如果数组中相应协议对应元素非空, 则赋值, 否则发生错误
                if (likely(typemap[type->proto] ==
                           NULL))
                    typemap[type->proto]
                    = type;
                else
                    err = -EEXIST;
                xfrm_policy_unlock_afinfo(afinfo);
                return err;
            }
            EXPORT_SYMBOL(xfrm_register_type);
            // 拆除协议处理类型, 返回0成功, 非0失败
            int xfrm_unregister_type(struct xfrm_type *type, unsigned short family)
            {
                // 找到协议族相关的策略信息结构
                struct xfrm_policy_afinfo *afinfo =
                    xfrm_policy_lock_afinfo(family);
                struct xfrm_type **typemap;
                int err = 0;
                if (unlikely(afinfo == NULL))
                    return -EAFNOSUPPORT;
                // 策略信息结构中的类型数组
                typemap = afinfo->type_map;
                // 如果数组中相应协议对应元素等于要删除的结构, 元素清空, 否则发生错误
                if (unlikely(typemap[type->proto]
                             != type))
                    err = -ENOENT;
                else
                    typemap[type->proto]
                    = NULL;
                xfrm_policy_unlock_afinfo(afinfo);
                return err;
            }
            EXPORT_SYMBOL(xfrm_unregister_type);
            // 根据协议号和协议族查找类型
            struct xfrm_type *xfrm_get_type(u8 proto, unsigned short family)
            {
                struct xfrm_policy_afinfo *afinfo;
                struct xfrm_type **typemap;
                struct xfrm_type *type;
                int modload_attempted = 0;
                retry:
                    // 找到协议族相关的策略信息结构
                    afinfo = xfrm_policy_get_afinfo(family);
                    if (unlikely(afinfo == NULL))
                        return NULL;
                    // 策略信息结构中的类型数组
                    typemap = afinfo->type_map;
                    // 数组中对应指定协议的元素
                    type = typemap[proto];
                    // 增加type模块的使用计数
                    if (unlikely(type
                                 &&
                                 !try_module_get(type->owner)))
                        type = NULL;
                    // 如果当前type为空, 则加载type的内核模块, 重新查找
                    if (!type &&
                            !modload_attempted)
                    {
                        xfrm_policy_put_afinfo(afinfo);
                        request_module("xfrm-type-%d-%d",
                                       (int) family, (int) proto);
                        modload_attempted = 1;
                        goto retry;
                    }
                    xfrm_policy_put_afinfo(afinfo);
                    return type;
            }
            // 释放类型模块使用计数
            void xfrm_put_type(struct xfrm_type *type)
            {
                module_put(type->owner);
            }
        5.10.2 协议模式处理
            模式目前包括通道和传输两种.
            // 登记模式, 返回0成功, 非0失败
            int xfrm_register_mode(struct xfrm_mode *mode, int family)
            {
                struct xfrm_policy_afinfo *afinfo;
                struct xfrm_mode **modemap;
                int err;
                if (unlikely(mode->encap
                             >= XFRM_MODE_MAX))
                    return -EINVAL;
                // 找到协议族相关的策略信息结构
                afinfo = xfrm_policy_lock_afinfo(family);
                if (unlikely(afinfo == NULL))
                    return -EAFNOSUPPORT;
                err = -EEXIST;
                // 策略信息结构中的模式数组
                modemap = afinfo->mode_map;
                // 数组元素非空的话赋值, 返回成功
                if (likely(modemap[mode->encap] ==
                           NULL))
                {
                    modemap[mode->encap]
                    = mode;
                    err = 0;
                }
                xfrm_policy_unlock_afinfo(afinfo);
                return err;
            }
            EXPORT_SYMBOL(xfrm_register_mode);
            // 拆除模式, 返回0成功, 非0失败
            int xfrm_unregister_mode(struct xfrm_mode *mode, int family)
            {
                struct xfrm_policy_afinfo *afinfo;
                struct xfrm_mode **modemap;
                int err;
                if (unlikely(mode->encap
                             >= XFRM_MODE_MAX))
                    return -EINVAL;
                // 找到协议族相关的策略信息结构
                afinfo = xfrm_policy_lock_afinfo(family);
                if (unlikely(afinfo == NULL))
                    return -EAFNOSUPPORT;
                err = -ENOENT;
                // 策略信息结构中的模式数组
                modemap = afinfo->mode_map;
                // 数组元素等于要拆除的模式, 清空, 返回成功
                if (likely(modemap[mode->encap] ==
                           mode))
                {
                    modemap[mode->encap]
                    = NULL;
                    err = 0;
                }
                xfrm_policy_unlock_afinfo(afinfo);
                return err;
            }
            EXPORT_SYMBOL(xfrm_unregister_mode);
            // 查找模式
            struct xfrm_mode *xfrm_get_mode(unsigned int encap, int family)
            {
                struct xfrm_policy_afinfo *afinfo;
                struct xfrm_mode *mode;
                int modload_attempted = 0;
                if (unlikely(encap >=
                             XFRM_MODE_MAX))
                    return NULL;
                retry:
                    // 找到协议族相关的策略信息结构
                    afinfo = xfrm_policy_get_afinfo(family);
                    if (unlikely(afinfo == NULL))
                        return NULL;
                    // 策略信息结构中的模式数组
                    mode =
                        afinfo->mode_map[encap];
                    // 增加模式模块的使用计数
                    if (unlikely(mode
                                 &&
                                 !try_module_get(mode->owner)))
                        mode = NULL;
                    // 如果当前模式为空, 则加载模式对应的内核模块, 重新查找
                    if (!mode &&
                            !modload_attempted)
                    {
                        xfrm_policy_put_afinfo(afinfo);
                        request_module("xfrm-mode-%d-%d",
                                       family, encap);
                        modload_attempted = 1;
                        goto retry;
                    }
                    xfrm_policy_put_afinfo(afinfo);
                    return mode;
            }
            // 释放模式模块使用计数
            void xfrm_put_mode(struct xfrm_mode *mode)
            {
                module_put(mode->owner);
            }
        5.10.3 协议信息处理
            // 登记协议信息结构
            int xfrm_policy_register_afinfo(struct xfrm_policy_afinfo *afinfo)
            {
                int err = 0;
                if (unlikely(afinfo == NULL))
                    return -EINVAL;
                if (unlikely(afinfo->family
                             >= NPROTO))
                    return -EAFNOSUPPORT;
                write_lock_bh(&xfrm_policy_afinfo_lock);
                // 数组中的对应协议的协议信息结构元素应该为空
                if
                (unlikely(xfrm_policy_afinfo[afinfo->family] !=
                          NULL))
                    err = -ENOBUFS;
                else
                {
                    // 安全路由操作结构
                    struct dst_ops *dst_ops =
                                afinfo->dst_ops;
                    // 安全路由操作结构的参数和操作函数赋值
                    if
                    (likely(dst_ops->kmem_cachep == NULL))
                        dst_ops->kmem_cachep
                        = xfrm_dst_cache;
                    if
                    (likely(dst_ops->check == NULL))
                        dst_ops->check
                        = xfrm_dst_check;
                    if
                    (likely(dst_ops->negative_advice == NULL))
                        dst_ops->negative_advice
                        = xfrm_negative_advice;
                    if
                    (likely(dst_ops->link_failure == NULL))
                        dst_ops->link_failure
                        = xfrm_link_failure;
                    if
                    (likely(afinfo->garbage_collect == NULL))
                        afinfo->garbage_collect
                        = __xfrm_garbage_collect;
                    // 数组中的对应协议的协议信息结构元素填为协议信息结构
                    xfrm_policy_afinfo[afinfo->family]
                    = afinfo;
                }
                write_unlock_bh(&xfrm_policy_afinfo_lock);
                return err;
            }
            EXPORT_SYMBOL(xfrm_policy_register_afinfo);
            // 拆除协议信息结构
            int xfrm_policy_unregister_afinfo(struct xfrm_policy_afinfo *afinfo)
            {
                int err = 0;
                if (unlikely(afinfo == NULL))
                    return -EINVAL;
                if (unlikely(afinfo->family
                             >= NPROTO))
                    return -EAFNOSUPPORT;
                write_lock_bh(&xfrm_policy_afinfo_lock);
                if
                (likely(xfrm_policy_afinfo[afinfo->family] != NULL))
                {
                    // 数组中的协议信息结构等于指定的信息结构
                    if
                    (unlikely(xfrm_policy_afinfo[afinfo->family] !=
                              afinfo))
                        err =
                            -EINVAL;
                    else
                    {
                        // 清空协议信息数组元素和路由操作结构参数
                        struct
                                dst_ops *dst_ops = afinfo->dst_ops;
                        xfrm_policy_afinfo[afinfo->family]
                        = NULL;
                        dst_ops->kmem_cachep
                        = NULL;
                        dst_ops->check
                        = NULL;
                        dst_ops->negative_advice
                        = NULL;
                        dst_ops->link_failure
                        = NULL;
                        afinfo->garbage_collect
                        = NULL;
                    }
                }
                write_unlock_bh(&xfrm_policy_afinfo_lock);
                return err;
            }
            EXPORT_SYMBOL(xfrm_policy_unregister_afinfo);
            // 查找协议信息结构, 加读锁
            static struct xfrm_policy_afinfo *xfrm_policy_get_afinfo(unsigned short family)
            {
                struct xfrm_policy_afinfo *afinfo;
                if (unlikely(family >=
                             NPROTO))
                    return NULL;
                read_lock(&xfrm_policy_afinfo_lock);
                // 获取指定协议位置处的协议信息结构
                afinfo = xfrm_policy_afinfo[family];
                // 如果该协议信息结构不存在, 解锁
                if (unlikely(!afinfo))
                    read_unlock(&xfrm_policy_afinfo_lock);
                return afinfo;
            }
            // 释放协议信息结构, 解读锁
            static void xfrm_policy_put_afinfo(struct xfrm_policy_afinfo *afinfo)
            {
                read_unlock(&xfrm_policy_afinfo_lock);
            }
            // 协议信息结构加写锁, 返回指定的协议信息结构, 错误时返回NULL
            static struct xfrm_policy_afinfo *xfrm_policy_lock_afinfo(unsigned int family)
            {
                struct xfrm_policy_afinfo *afinfo;
                if (unlikely(family >=
                             NPROTO))
                    return NULL;
                write_lock_bh(&xfrm_policy_afinfo_lock);
                // 获取指定协议位置处的协议信息结构
                afinfo = xfrm_policy_afinfo[family];
                // 如果该协议信息结构不存在, 解锁
                if (unlikely(!afinfo))
                    write_unlock_bh(&xfrm_policy_afinfo_lock);
                return afinfo;
            }
            // 协议信息结构解写锁
            static void xfrm_policy_unlock_afinfo(struct xfrm_policy_afinfo *afinfo)
            {
                write_unlock_bh(&xfrm_policy_afinfo_lock);
            }
        5.10.4 网卡回调
            // 网卡通知结构
            static struct notifier_block xfrm_dev_notifier =
            {
                xfrm_dev_event,
                NULL,
                0
            };
            // 回调函数
            static int xfrm_dev_event(struct notifier_block *this, unsigned
                                      long event, void *ptr)
            {
                switch (event)
                {
                    // 就只响应网卡停事件, 删除和网卡相关的所有安全路由项
                case NETDEV_DOWN:
                    xfrm_flush_bundles();
                }
                return NOTIFY_DONE;
            }
            static int xfrm_flush_bundles(void)
            {
                // 也是使用xfrm_prune_bundles()函数进行删除操作
                // 条件函数是stale_bundle
                xfrm_prune_bundles(stale_bundle);
                return 0;
            }
            // 判断安全路由项是否可用
            // 返回1表示不可用, 0表示可用
            static int stale_bundle(struct dst_entry *dst)
            {
                return !xfrm_bundle_ok(NULL, (struct xfrm_dst
                                              *)dst, NULL, AF_UNSPEC, 0);
            }
            // 返回0表示不可用, 1表示可用
            int xfrm_bundle_ok(struct xfrm_policy *pol, struct xfrm_dst
                               *first,
                               struct flowi *fl, int family,
                               int strict)
            {
                struct dst_entry *dst =
                            &first->u.dst;
                struct xfrm_dst *last;
                u32 mtu;
                // 检查路由项
                if (!dst_check(dst->path, ((struct
                                            xfrm_dst *)dst)->path_cookie) ||
                        // 检查网卡是否在运行
                        (dst->dev &&
                         !netif_running(dst->dev)))
                    return 0;
                last = NULL;
                do
                {
                    // 安全路由
                    struct xfrm_dst *xdst = (struct
                                             xfrm_dst *)dst;
                    // 检查SA选择子是否匹配流结构
                    if (fl
                            &&
                            !xfrm_selector_match(&dst->xfrm->sel,
                                                 fl, family))
                        return
                            0;
                    if (fl
                            &&
                            !security_xfrm_flow_state_match(fl, dst->xfrm,
                                                            pol))
                        return
                            0;
                    // 检查SA状态是否合法
                    if
                    (dst->xfrm->km.state !=
                            XFRM_STATE_VALID)
                        return
                            0;
                    if (xdst->genid
                            != dst->xfrm->genid)
                        return
                            0;
                    // 严格检查时, 检查非通道模式下的SA地址和流结构参数是否匹配
                    if (strict
                            && fl
                            &&
                            dst->xfrm->props.mode !=
                            XFRM_MODE_TUNNEL &&
                            !xfrm_state_addr_flow_check(dst->xfrm, fl,
                                                        family))
                        return
                            0;
                    // 子路由项的MTU
                    mtu =
                        dst_mtu(dst->child);
                    if
                    (xdst->child_mtu_cached != mtu)
                    {
                        last =
                            xdst;
                        xdst->child_mtu_cached
                        = mtu;
                    }
                    // 通用路由检查
                    if
                    (!dst_check(xdst->route,
                                xdst->route_cookie))
                        return
                            0;
                    // 安全路由相关的普通路由的MTU
                    mtu =
                        dst_mtu(xdst->route);
                    if
                    (xdst->route_mtu_cached != mtu)
                    {
                        last =
                            xdst;
                        xdst->route_mtu_cached
                        = mtu;
                    }
                    // 遍历安全路由链表
                    dst =
                        dst->child;
                }
                while (dst->xfrm);
                // last是最后一个和子路由和普通路由的MTU不同的安全路由, 一般都是相同的
                if (likely(!last))
                    return 1;
                // 调整各路由项中的MTU
                mtu =
                    last->child_mtu_cached;
                for (;;)
                {
                    dst =
                        &last->u.dst;
                    mtu =
                        xfrm_state_mtu(dst->xfrm, mtu);
                    if (mtu >
                            last->route_mtu_cached)
                        mtu =
                            last->route_mtu_cached;
                    dst->metrics[RTAX_MTU-1]
                    = mtu;
                    if (last == first)
                        break;
                    last =
                        last->u.next;
                    last->child_mtu_cached
                    = mtu;
                }
                return 1;
            }
    5.11 小结
        xfrm_policy相关函数的调用被调用关系可如下简单表示:
        ip_route_output_flow
            -> xfrm_lookup:  find xfrm_dst form the skb, create dst_list
            -> xfrm_sk_policy_lookup
            -> flow_cache_lookup
            -> xfrm_find_bundle
            -> xfrm_policy_lookup_bytype
            -> xfrm_tmpl_resolve
                -> xfrm_tmpl_resolve_one
                    -> xfrm_get_saddr
                        -> afinfo->get_saddr == xfrm4_get_saddr
                            -> xfrm4_dst_lookup
                    -> xfrm_state_find
                        -> __xfrm_state_lookup
                        -> xfrm_state_alloc
                        -> km_query
                            -> km->acquire (pfkey_acquire, xfrm_send_acquire)
                -> xfrm_state_sort
                    -> afinfo->state_sort == NULL
                -> km_wait_queue
                -> xfrm_bundle_create 
        do_ip_setsockopt
            -> xfrm_user_policy
                -> km->compile_policy
            -> xfrm_sk_policy_insert
        pfkey_compile_policy
            -> xfrm_policy_alloc
                timer.func=xfrm_policy_timer
        pfkey_spdadd
           -> xfrm_policy_alloc
           -> xfrm_policy_insert
           -> policy_hash_bysel
           -> selector_cmp
           -> xfrm_sel_ctx_match
        pfkey_spddelete
           -> xfrm_policy_bysel_ctx
               -> policy_hash_bysel
               -> xfrm_sel_ctx_match
        pfkey_spdget
            -> xfrm_policy_byid
        xfrm_flush_policy
        pfkey_policy_flush
            -> xfrm_policy_flush
                -> xfrm_policy_kill
        xfrm_dump_policy
            -> xfrm_policy_walk
                -> dump_one_policy
        pfkey_spddump
            -> xfrm_policy_walk
                -> dump_sp
        gen_reqid
            -> xfrm_policy_walk
                -> check_reqid
        xfrm_add_pol_expire
        xfrm_policy_timer
            -> xfrm_policy_delete
                -> __xfrm_policy_unlink
                -> xfrm_policy_kill
        xfrm_sk_policy_insert
            -> xfrm_get_index
            -> __xfrm_policy_link
            -> __xfrm_policy_unlink
            -> xfrm_policy_kill
        xfrm_sk_clone_policy
            -> __xfrm_sk_clone_policy
                -> clone_policy
                    -> xfrm_policy_alloc
                    -> __xfrm_policy_link
        xfrm_decode_session
            -> xfrm4_decode_session
        xfrm4_route_forward
            -> xfrm_route_forward
                -> __xfrm_route_forward
                    -> xfrm4_decode_session
                    -> xfrm_lookup
        xfrm4_policy_check
            -> xfrm_policy_check
                -> __xfrm_policy_check
                    -> xfrm4_decode_session
                    -> __xfrm_sk_policy_lookup
                        -> xfrm_selector_match
                    -> __flow_cache_lookup
                        -> xfrm_policy_lookup
                        -> xfrm_policy_lookup_bytype
                            -> policy_hash_direct
                            -> xfrm_policy_match
                                -> xfrm_selector_match
                    -> xfrm_policy_lookup_bytype
                    -> xfrm_tmpl_sort
                    -> xfrm_policy_ok
                        -> xfrm_state_ok
        xfrm_flush_bundles
            -> xfrm_prune_bundles
                -> prune_one_bundles
                -> stale_bundle
6. XFRM的其他操作
    6.1 HASH处理
        关于HASH值的计算方法主要在net/xfrm/xfrm_hash.h中定义:
        // IPV4地址HASH
        static inline unsigned int __xfrm4_addr_hash(xfrm_address_t *addr)
        {
            // 就是地址本身
            return ntohl(addr->a4);
        }
        // IPV6地址HASH
        static inline unsigned int __xfrm6_addr_hash(xfrm_address_t *addr)
        {
            // 取后2个32位数异或
            return ntohl(addr->a6[2] ^ addr->a6[3]);
        }
        // IPV4源,目的地址HASH
        static inline unsigned int __xfrm4_daddr_saddr_hash(xfrm_address_t *daddr, xfrm_address_t *saddr)
        {
            // 将两个地址异或
            return ntohl(daddr->a4 ^ saddr->a4);
        }
        // IPV4源,目的地址HASH
        static inline unsigned int __xfrm6_daddr_saddr_hash(xfrm_address_t *daddr, xfrm_address_t *saddr)
        {
            // 两个V6地址都取后2个32位数异或
            return ntohl(daddr->a6[2] ^ daddr->a6[3] ^
                         saddr->a6[2] ^ saddr->a6[3]);
        }
        // 目的地址HASH
        static inline unsigned int __xfrm_dst_hash(xfrm_address_t *daddr, xfrm_address_t *saddr,
                                                    u32 reqid, unsigned short family,
                                                    unsigned int hmask)
        {
            // 协议族和请求ID异或
            unsigned int h = family ^ reqid;
            switch (family)
            {
            // HASH值再和源目的地址HASH结果进行异或
            case AF_INET:
                h ^= __xfrm4_daddr_saddr_hash(daddr, saddr);
                break;
            case AF_INET6:
                h ^= __xfrm6_daddr_saddr_hash(daddr, saddr);
                break;
            }
            // 将HASH结果高低16位异或存低16位,高16位不动, 然后用HASH掩码相与
            return (h ^ (h >> 16)) & hmask;
        }
        // 源地址HASH, 只是没有请求ID项, 其他HASH过程和上面相同
        static inline unsigned __xfrm_src_hash(xfrm_address_t *daddr,
                                               xfrm_address_t *saddr,
                                               unsigned short family,
                                               unsigned int hmask)
        {
            unsigned int h = family;
            switch (family)
            {
                case AF_INET:
                    h ^= __xfrm4_daddr_saddr_hash(daddr, saddr);
                    break;
                case AF_INET6:
                    h ^= __xfrm6_daddr_saddr_hash(daddr, saddr);
                    break;
            };
            return (h ^ (h >> 16)) & hmask;
        }
        // 根据SPI计算HASH值
        static inline unsigned int
        __xfrm_spi_hash(xfrm_address_t *daddr, __be32 spi, u8 proto, unsigned short family,
                        unsigned int hmask)
        {
            // 先将SPI和协议进行异或
            unsigned int h = (__force u32)spi ^ proto;
            switch (family)
            {
            // HASH值再和目的地址进行单一地址HASH值异或
            case AF_INET:
                h ^= __xfrm4_addr_hash(daddr);
                break;
            case AF_INET6:
                h ^= __xfrm6_addr_hash(daddr);
                break;
            }
            // HASH值再和本身的高22位, 高12位异或后再和掩码相与
            return (h ^ (h >> 10) ^ (h >> 20)) & hmask;
        }
        // 索引号HASH
        static inline unsigned int __idx_hash(u32 index, unsigned int hmask)
        {
            // 低24位和高24位异或, 高8位不动, 再和掩码相与
            return (index ^ (index >> 8)) & hmask;
        }
        // 选择子HASH
        static inline unsigned int __sel_hash(struct xfrm_selector *sel, unsigned short family, unsigned int hmask)
        {
            // 提前源和目的地址
            xfrm_address_t *daddr = &sel->daddr;
            xfrm_address_t *saddr = &sel->saddr;
            unsigned int h = 0;
            switch (family)
            {
                // 用源,目的地址同时进行HASH
                case AF_INET:
                    if (sel->prefixlen_d != 32 ||
                            sel->prefixlen_s != 32)
                        return hmask + 1;
                    h = __xfrm4_daddr_saddr_hash(daddr, saddr);
                    break;
                case AF_INET6:
                    if (sel->prefixlen_d != 128 ||
                            sel->prefixlen_s != 128)
                        return hmask + 1;
                    h = __xfrm6_daddr_saddr_hash(daddr, saddr);
                    break;
            };
            // 高16位与低16位异或,高16位不变
            h ^= (h >> 16);
            // 与掩码相与, 其实HASH值中不带协议族因素, 因为地址本身就包含了
            return h & hmask;
        }
        // 地址HASH
        static inline unsigned int __addr_hash(xfrm_address_t *daddr, xfrm_address_t *saddr, unsigned short family, unsigned int hmask)
        {
            unsigned int h = 0;
            switch (family)
            {
            // 用源,目的地址同时进行HASH
            case AF_INET:
                h = __xfrm4_daddr_saddr_hash(daddr, saddr);
                break;
            case AF_INET6:
                h = __xfrm6_daddr_saddr_hash(daddr, saddr);
                break;
            };
            // 高16位与低16位异或,高16位不变
            h ^= (h >> 16);
            // 与掩码相与
            return h & hmask;
        }
        在net/xfrm/xfrm_hash.c 文件中定义了HASH表的分配和释放函数:
        struct hlist_head *xfrm_hash_alloc(unsigned int sz)
        {
            struct hlist_head *n;
            // 根据HASH表大小选择合适的分配方法
            // 大小不超过PAGE_SIZE, 用kmalloc分配
            if (sz <= PAGE_SIZE)
                n = kmalloc(sz, GFP_KERNEL);
            // 这是在内核定义NUMA和IA64下用vmalloc分配
            else if (hashdist)
                n = __vmalloc(sz, GFP_KERNEL, PAGE_KERNEL);
            else
            // 其他类型的内核用get_free_page分配
                n = (struct hlist_head *)
                    __get_free_pages(GFP_KERNEL, get_order(sz));
            // 空间清零
            if (n)
                memset(n, 0, sz);
            return n;
        }
        // 释放HASH表空间
        void xfrm_hash_free(struct hlist_head *n, unsigned int sz)
        {
            if (sz <= PAGE_SIZE)
                kfree(n);
            else if (hashdist)
                vfree(n);
            else
                free_pages((unsigned long)n, get_order(sz));
        }
    6.2 算法操作
        IPSEC操作中用到的认证, 加密, 压缩等算法具体实现是在crypto目录下, 而在xfrm中只是定义这些算法的说明, 表示最大可以支持这些算法, 在使用时会探测这些算法是否在内核中存在从而确定可使用的算法.
        关于算法的数据结构如下:
        /* include/net/xfrm.h */
        // 认证算法参数
        struct xfrm_algo_auth_info
        {
            u16 icv_truncbits; // 初始向量截断位数
            u16 icv_fullbits;  // 初始向量总的位数
        };
        // 加密算法参数
        struct xfrm_algo_encr_info
        {
            u16 blockbits;  // 块位数
            u16 defkeybits; // 密钥长度位数
        };
        // 压缩算法参数
        struct xfrm_algo_comp_info
        {
            u16 threshold;  // 阈值
        };
        // xfrm算法描述
        struct xfrm_algo_desc
        {
            char *name;  // 名称
            char *compat; // 名称缩写
            u8 available:1; // 算法是否可用(是否在内核中)
            union
            {
                struct xfrm_algo_auth_info auth;
                struct xfrm_algo_encr_info encr;
                struct xfrm_algo_comp_info comp;
            } uinfo; // 算法信息联合
            struct sadb_alg desc; // 通用算法描述
        };
        6.2.1 认证算法
            可用的认证算法通过下面的数组来描述, 
            包含NULL, MD5, SHA1, SHA256, RIPEMD160等认证算法:
            static struct xfrm_algo_desc aalg_list[] =
            {
                ......
                {
                    .name = "hmac(sha1)",
                    .compat = "sha1",
                    .uinfo = {
                        .auth = {
                            .icv_truncbits = 96,// 96位截断
                            .icv_fullbits = 160, // 总共160位
                        }
                    },
                    .desc = { // 这是对SHA1认证算法的标准描述参数
                        .sadb_alg_id = SADB_AALG_SHA1HMAC, // 算法ID值
                        .sadb_alg_ivlen = 0,
                        .sadb_alg_minbits = 160,
                        .sadb_alg_maxbits = 160
                    }
                },
                ......
            }
            相关操作函数:
                // 通过算法ID查找认证算法
                struct xfrm_algo_desc *xfrm_aalg_get_byid(int alg_id)
                {
                    int i;
                    // 遍历认证数组
                    for (i = 0; i < aalg_entries(); i++)
                    {
                        // 查找和指定算法ID相同的算法
                        if (aalg_list[i].desc.sadb_alg_id == alg_id)
                        {
                            // 检查该算法是否可用
                            if (aalg_list[i].available)
                                return &aalg_list[i];
                            else
                                break;
                        }
                    }
                    return NULL;
                }
                EXPORT_SYMBOL_GPL(xfrm_aalg_get_byid);
                // 统计可用的认证算法数量, 就是available的认证算法数量累加
                int xfrm_count_auth_supported(void)
                {
                    int i, n;
                    for (i = 0, n = 0; i < aalg_entries(); i++)
                        if (aalg_list[i].available)
                            n++;
                    return n;
                }
                EXPORT_SYMBOL_GPL(xfrm_count_auth_supported);
        6.2.2 加密算法
            可用的认证算法通过下面的数组来描述, 
            包含NULL, DES, 3DES, CAST, AES, BLOWFISH, TWOFISH, SERPENT等加密算法:
            static struct xfrm_algo_desc ealg_list[] = {
                ......
                {
                    .name = "cbc(des3_ede)",
                    .compat = "des3_ede",
                    .uinfo = {
                        .encr = {
                            .blockbits = 64,
                            .defkeybits = 192,
                        }
                    },
                    .desc = {
                        .sadb_alg_id = SADB_EALG_3DESCBC,
                        .sadb_alg_ivlen = 8,
                        .sadb_alg_minbits = 192,
                        .sadb_alg_maxbits = 192
                    }
                },
                ......
            }
            相关操作函数:
                // 通过算法ID查找加密算法, 和认证算法查找类似
                struct xfrm_algo_desc *xfrm_ealg_get_byid(int alg_id)
                {
                    int i;
                    for (i = 0; i < ealg_entries(); i++)
                    {
                        if (ealg_list[i].desc.sadb_alg_id == alg_id)
                        {
                            if (ealg_list[i].available)
                                return &ealg_list[i];
                            else
                                break;
                        }
                    }
                    return NULL;
                }
                EXPORT_SYMBOL_GPL(xfrm_ealg_get_byid);
                // 统计可用的加密算法数量, 就是available的加密算法数量累加
                int xfrm_count_enc_supported(void)
                {
                    int i, n;
                    for (i = 0, n = 0; i < ealg_entries(); i++)
                        if (ealg_list[i].available)
                            n++;
                    return n;
                }
                EXPORT_SYMBOL_GPL(xfrm_count_enc_supported);
        6.2.3 压缩算法
            可用的压缩算法通过下面的数组来描述, 包含DELFATE, LZS, LZJH等压缩算法:
            static struct xfrm_algo_desc calg_list[] = {
                ......
                {
                    .name = "lzs",
                    .uinfo = {
                        .comp = {
                            .threshold = 90,
                        }
                    },
                    .desc = { .sadb_alg_id = SADB_X_CALG_LZS }
                },
                ......
            }
            相关操作函数:
                // 通过算法ID查找加密算法, 和认证算法查找类似
                struct xfrm_algo_desc *xfrm_calg_get_byid(int alg_id)
                {
                    int i;
                    for (i = 0; i < calg_entries(); i++)
                    {
                        if (calg_list[i].desc.sadb_alg_id == alg_id)
                        {
                            if (calg_list[i].available)
                                return &calg_list[i];
                            else
                                break;
                        }
                    }
                    return NULL;
                }
                EXPORT_SYMBOL_GPL(xfrm_calg_get_byid);
        6.2.4 通过名称查找算法
            // 输入参数为算法数组, 数组元素个数, 类型, 掩码, 名称和是否探测在内核中存在
            static struct xfrm_algo_desc *xfrm_get_byname(struct xfrm_algo_desc *list,
                    int entries, u32 type, u32 mask,
                    char *name, int probe)
            {
                int i, status;
                if (!name)
                    return NULL;
                // 遍历数组
                for (i = 0; i < entries; i++)
                {
                    // 比较算法名称或缩写名称是否和指定名称相同
                    if (strcmp(name, list[i].name) &&
                            (!list[i].compat || strcmp(name, list[i].compat)))
                        continue;
                    // 找到算法结构
                    // 检查算法是否在内核可用, 可用的话成功返回
                    if (list[i].available)
                        return &list[i];
                    // 如果不需要探测, 将返回空
                    if (!probe)
                        break;
                    // 需要探测算法算法存在内核, 调用crypto_has_alg()函数探测
                    // 返回0表示失败, 非0表示成功
                    status = crypto_has_alg(name, type, mask | CRYPTO_ALG_ASYNC);
                    if (!status)
                        break;
                    // 算法可用, 返回
                    list[i].available = status;
                    return &list[i];
                }
                return NULL;
            }
            /* crypto/api.c */
            // 算法探测
            int crypto_has_alg(const char *name, u32 type, u32 mask)
            {
                int ret = 0;
                // 根据名称, 类型和掩码探测算法模块
                struct crypto_alg *alg = crypto_alg_mod_lookup(name, type, mask);
                // 正确返回找到
                if (!IS_ERR(alg))
                {
                // 减少模块计数, 返回1
                    crypto_mod_put(alg);
                    ret = 1;
                }
                return ret;
            }
            有了xfrm_get_byname()这个通用基本函数, 具体类型的算法查找函数就很简单了:
            // 通过名称查找认证算法
            struct xfrm_algo_desc *xfrm_aalg_get_byname(char *name, int probe)
            {
                return xfrm_get_byname(aalg_list, aalg_entries(),
                                       CRYPTO_ALG_TYPE_HASH, CRYPTO_ALG_TYPE_HASH_MASK,
                                       name, probe);
            }
            EXPORT_SYMBOL_GPL(xfrm_aalg_get_byname);
            // 通过名称查找加密算法
            struct xfrm_algo_desc *xfrm_ealg_get_byname(char *name, int probe)
            {
                return xfrm_get_byname(ealg_list, ealg_entries(),
                                       CRYPTO_ALG_TYPE_BLKCIPHER, CRYPTO_ALG_TYPE_MASK,
                                       name, probe);
            }
            EXPORT_SYMBOL_GPL(xfrm_ealg_get_byname);
            // 通过名称查找压缩算法
            struct xfrm_algo_desc *xfrm_calg_get_byname(char *name, int probe)
            {
                return xfrm_get_byname(calg_list, calg_entries(),
                                       CRYPTO_ALG_TYPE_COMPRESS, CRYPTO_ALG_TYPE_MASK,
                                       name, probe);
            }
            EXPORT_SYMBOL_GPL(xfrm_calg_get_byname);
            以下是通过索引号来查找算法, 就是直接返回相应数组指定位置的算法:
            struct xfrm_algo_desc *xfrm_aalg_get_byidx(unsigned int idx)
            {
                if (idx >= aalg_entries())
                    return NULL;
                return &aalg_list[idx];
            }
            EXPORT_SYMBOL_GPL(xfrm_aalg_get_byidx);
            struct xfrm_algo_desc *xfrm_ealg_get_byidx(unsigned int idx)
            {
                if (idx >= ealg_entries())
                    return NULL;
                return &ealg_list[idx];
            }
            EXPORT_SYMBOL_GPL(xfrm_ealg_get_byidx);
        6.2.5 xfrm算法探测
            该函数在SA进行调整时会调用来查看当前内核中支持的各种算法
            /*
            * Probe for the availability of crypto algorithms, and set the available
            * flag for any algorithms found on the system.  This is typically called by
            * pfkey during userspace SA add, update or register.
            */
            void xfrm_probe_algs(void)
            {
                // 内核必须定义CRYPTO选项, 否则就是空函数了
                #ifdef CONFIG_CRYPTO
                int i, status;
                BUG_ON(in_softirq());
                // 遍历认证算法数组
                for (i = 0; i < aalg_entries(); i++)
                {
                    // 根据算法名称确定该HASH算法是否存在, 返回0不存在, 非0存在
                    status = crypto_has_hash(aalg_list[i].name, 0,
                                             CRYPTO_ALG_ASYNC);
                    // 如果状态和原来的状态不同, 更改
                    if (aalg_list[i].available != status)
                        aalg_list[i].available = status;
                }
                // 遍历加密算法数组
                for (i = 0; i < ealg_entries(); i++)
                {
                    // 根据算法名称确定该加密算法是否存在, 返回0不存在, 非0存在
                    status = crypto_has_blkcipher(ealg_list[i].name, 0,
                                                  CRYPTO_ALG_ASYNC);
                    // 如果状态和原来的状态不同, 更改
                    if (ealg_list[i].available != status)
                        ealg_list[i].available = status;
                }
                // 遍历压缩算法数组
                for (i = 0; i < calg_entries(); i++)
                {
                    // 根据算法名称确定该压缩算法是否存在, 返回0不存在, 非0存在
                    status = crypto_has_comp(calg_list[i].name, 0,
                                             CRYPTO_ALG_ASYNC);
                    // 如果状态和原来的状态不同, 更改
                    if (calg_list[i].available != status)
                        calg_list[i].available = status;
                }
                #endif
            }
            EXPORT_SYMBOL_GPL(xfrm_probe_algs);
    6.3 通过netlink套接口访问xfrm
        通过netlink套接口访问xfrm的处理函数在net/xfrm/xfrm_user.c中, 
        提供了Linux特色的非标准PF_KEY接口的SA, SP控制方法, 
        能完成和PF_KEY一样控制功能, 
        目前iproute2中的ip工具中新增加的xfrm命令就是通过这种netlink接口来完成的,
        因为netlink操作以前已经介绍过, 
        xfrm的操作又都是一样的, 因此本文不再分析其实现过程.
    6.4 xfrm_input
        在net/xfrm/xfrm_input.c文件中定义了关于安全路径(struct sec_path)的几个处理函数, 
        用于对输入的IPSEC包进行解析构造安全路径使用.
        // 释放安全路径
        void __secpath_destroy(struct sec_path *sp)
        {
            int i;
            // 减少安全路径中所有SA的使用计数
            for (i = 0; i < sp->len; i++)
                xfrm_state_put(sp->xvec[i]);
            // 释放安全路径空间
            kmem_cache_free(secpath_cachep, sp);
        }
        EXPORT_SYMBOL(__secpath_destroy);
        // 安全路径复制
        struct sec_path *secpath_dup(struct sec_path *src)
        {
            struct sec_path *sp;
            // 先分配安全路径结构
            sp = kmem_cache_alloc(secpath_cachep, SLAB_ATOMIC);
            if (!sp)
                return NULL;
            sp->len = 0;
            if (src)
            {
                int i;
                // 如果源安全路径结构非空, 将其全部复制到新结构中
                memcpy(sp, src, sizeof(*sp));
                // 增加安全路径中所有SA的使用计数
                for (i = 0; i < sp->len; i++)
                    xfrm_state_hold(sp->xvec[i]);
            }
            // 设置该引用计数初始值位1
            atomic_set(&sp->refcnt, 1);
            return sp;
        }
        EXPORT_SYMBOL(secpath_dup);
        /* Fetch spi and seq from ipsec header */
        // 从数据包中解析SPI和序号, 返回值是网络序的
        int xfrm_parse_spi(struct sk_buff *skb, u8 nexthdr, __be32 *spi, __be32 *seq)
        {
            int offset, offset_seq;
            // 通过nexthdr参数来判断协议类型, nexthdr是IPV6里的说法,
            // 在IPV4中就是IP头里的协议字段
            // 根据不同协议确定数据中SPI和序列号相对数据起始点的偏移
            switch (nexthdr)
            {
            case IPPROTO_AH:
                offset = offsetof(struct ip_auth_hdr, spi);
                offset_seq = offsetof(struct ip_auth_hdr, seq_no);
                break;
            case IPPROTO_ESP:
                offset = offsetof(struct ip_esp_hdr, spi);
                offset_seq = offsetof(struct ip_esp_hdr, seq_no);
                break;
            case IPPROTO_COMP:
                // 对应压缩协议单独处理
                // 数据头准备出IP压缩头结构长度
                if (!pskb_may_pull(skb, sizeof(struct ip_comp_hdr)))
                    return -EINVAL;
                // SPI值取第3,4字节的数据, 序号为0
                *spi = htonl(ntohs(*(__be16*)(skb->h.raw + 2)));
                *seq = 0;
                return 0;
            default:
                return 1;
            }
            // 数据头准备16字节空间, 这是ip_auth_hdr和ip_esp_hdr结构最小长度
            if (!pskb_may_pull(skb, 16))
                return -EINVAL;
            // 根据偏移获取SPI和序号, 注意是网络序的值
            *spi = *(__be32*)(skb->h.raw + offset);
            *seq = *(__be32*)(skb->h.raw + offset_seq);
            return 0;
        }
        EXPORT_SYMBOL(xfrm_parse_spi);         
7. IPV4下的xfrm支持处理
    在xfrm中各种和地址相关的操作是和协议族相关的,
    因此这部分的具体实现就放在相关的协议族实现中,
    然后通过状态和策略信息结构来指引到实际的操作中，
    完成对普通数据包的IPSEC包装或对IPSEC包的解封装。
    7.1 IPV4下的xfrm策略
        IPV4下的xfrm策略在net/ipv4/xfrm4_policy.c文件中定义, 主要是定义IPV4的策略信息结构:
        static struct xfrm_policy_afinfo xfrm4_policy_afinfo =
        {
            .family =   AF_INET,
            .dst_ops =  &xfrm4_dst_ops,
            .dst_lookup =  xfrm4_dst_lookup,
            .get_saddr =  xfrm4_get_saddr,
            .find_bundle =   __xfrm4_find_bundle,
            .bundle_create = __xfrm4_bundle_create,
            .decode_session = _decode_session4,
        };
        在xfrm_policy_register_afinfo()函数中, 
        还定义了struct xfrm_policy_afinfo结构的其他几个成员函数,
        因为这几个函数是和协议无关的, 所以在登记函数中定义了:
                afinfo->garbage_collect = __xfrm_garbage_collect;
        该函数已经在本系列的第3篇中介绍过了.
        以下是结构中几个函数的定义:
        // IPV4的路由查找, 就是普通是路由查找方法
        // 返回0成功
        static int xfrm4_dst_lookup(struct xfrm_dst **dst, struct flowi *fl)
        {
            return __ip_route_output_key((struct rtable**)dst, fl);
        }
        // 查找地址, 这个函数是在通道模式下, 源地址没明确指定时调用的,查找获取
        // 外部头中的源地址
        static int xfrm4_get_saddr(xfrm_address_t *saddr, xfrm_address_t *daddr)
        {
            struct rtable *rt;
            // 通道的流结构定义,用于查找路由
            struct flowi fl_tunnel =
            {
                .nl_u = {
                    .ip4_u = {
                        .daddr = daddr->a4,
                    },
                },
            };
            // 根据目的地址找路由
            if (!xfrm4_dst_lookup((struct xfrm_dst **)&rt, &fl_tunnel))
            {
                // 将找到的路由项中的源地址作为通道模式下的外部源地址
                saddr->a4 = rt->rt_src;
                dst_release(&rt->u.dst);
                return 0;
            }
            return -EHOSTUNREACH;
        }
        // 查找策略中的安全路由, 查找条件是流结构的定义的参数
        static struct dst_entry *
        __xfrm4_find_bundle(struct flowi *fl, struct xfrm_policy *policy)
        {
            struct dst_entry *dst;
            read_lock_bh(&policy->lock);
            // 遍历策略的安全路由链表
            for (dst = policy->bundles; dst; dst = dst->next)
            {
                struct xfrm_dst *xdst = (struct xfrm_dst*)dst;
                // 比较网卡位置, 目的地址, 源地址, TOS值是否匹配
                // 同时检查该安全路由是否可用
                if (xdst->u.rt.fl.oif == fl->oif && /*XXX*/
                        xdst->u.rt.fl.fl4_dst == fl->fl4_dst &&
                        xdst->u.rt.fl.fl4_src == fl->fl4_src &&
                        xdst->u.rt.fl.fl4_tos == fl->fl4_tos &&
                        xfrm_bundle_ok(policy, xdst, fl, AF_INET, 0))
                {
                    dst_clone(dst);
                    break;
                }
            }
            read_unlock_bh(&policy->lock);
            return dst;
        }
        // 解码skb数据, 填充流结构
        static void
        _decode_session4(struct sk_buff *skb, struct flowi *fl)
        {
            struct iphdr *iph = skb->nh.iph;
            // xprth是IP头后的上层协议头起始
            u8 *xprth = skb->nh.raw + iph->ihl*4;
            // 先将流结构清零
            memset(fl, 0, sizeof(struct flowi));
            // 数据包必须不是分片包
            if (!(iph->frag_off & htons(IP_MF | IP_OFFSET)))
            {
                switch (iph->protocol)
                {
                // 对UDP(17), TCP(6), SCTP(132)和DCCP(33)协议, 要提取源端口和目的端口
                // 头4字节是源端口和目的端口
                case IPPROTO_UDP:
                case IPPROTO_TCP:
                case IPPROTO_SCTP:
                case IPPROTO_DCCP:
                    // 要让skb预留出IP头长度加4字节的长度, 在IP层data应该指向最外面的IP头
                    if (pskb_may_pull(skb, xprth + 4 - skb->data))
                    {
                        u16 *ports = (u16 *)xprth;
                        // 提取端口参数
                        fl->fl_ip_sport = ports[0];
                        fl->fl_ip_dport = ports[1];
                    }
                    break;
                case IPPROTO_ICMP:
                    // 对ICMP(1)协议要提取ICMP包的类型和编码, 2字节
                    if (pskb_may_pull(skb, xprth + 2 - skb->data))
                    {
                        u8 *icmp = xprth;
                        fl->fl_icmp_type = icmp[0];
                        fl->fl_icmp_code = icmp[1];
                    }
                    break;
                case IPPROTO_ESP:
                    // 对于ESP(50)协议要提取其中的SPI值, 4字节
                    if (pskb_may_pull(skb, xprth + 4 - skb->data))
                    {
                        __be32 *ehdr = (__be32 *)xprth;
                        fl->fl_ipsec_spi = ehdr[0];
                    }
                    break;
                case IPPROTO_AH:
                    // 对于AH(51)协议要提取其中的SPI值, 4字节
                    if (pskb_may_pull(skb, xprth + 8 - skb->data))
                    {
                        __be32 *ah_hdr = (__be32*)xprth;
                        fl->fl_ipsec_spi = ah_hdr[1];
                    }
                    break;
                case IPPROTO_COMP:
                    // 对于COMP(108)协议要提取其中CPI值作为SPI值, 2字节
                    if (pskb_may_pull(skb, xprth + 4 - skb->data))
                    {
                        __be16 *ipcomp_hdr = (__be16 *)xprth;
                        fl->fl_ipsec_spi = htonl(ntohs(ipcomp_hdr[1]));
                    }
                    break;
                default:
                    fl->fl_ipsec_spi = 0;
                    break;
                };
            }
            // 填充协议,源地址,目的地址, TOS参数
            fl->proto = iph->protocol;
            fl->fl4_dst = iph->daddr;
            fl->fl4_src = iph->saddr;
            fl->fl4_tos = iph->tos;
        }
        /* Allocate chain of dst_entry's, attach known xfrm's, calculate
         * all the metrics... Shortly, bundle a bundle.
         */
        // 创建安全路由
        static int
        __xfrm4_bundle_create(struct xfrm_policy *policy, struct xfrm_state **xfrm, int nx,
                              struct flowi *fl, struct dst_entry **dst_p)
        {
            struct dst_entry *dst, *dst_prev;
            struct rtable *rt0 = (struct rtable*)(*dst_p);
            struct rtable *rt = rt0;
            u32 remote = fl->fl4_dst;
            u32 local  = fl->fl4_src;
            struct flowi fl_tunnel =
            {
                .nl_u = {
                    .ip4_u = {
                        .saddr = local,
                        .daddr = remote,
                        .tos = fl->fl4_tos
                    }
                }
            };
            int i;
            int err;
            int header_len = 0;
            int trailer_len = 0;
            dst = dst_prev = NULL;
            dst_hold(&rt->u.dst);
            // 循环次数为策略中SA的数量, 每个SA对应一个安全路由, 一个安全路由对应对数据包的一个
            // 操作: 如压缩, ESP封装, AH封装等
            for (i = 0; i < nx; i++)
            {
                // 分配安全路由, 安全路由的操作结构是xfrm4_dst_ops
                // 因为定义了很多不同类型的路由, 每种路由都有各自的操作结构, 这样在上层可用
                // 统一的接口进行路由处理
                struct dst_entry *dst1 = dst_alloc(&xfrm4_dst_ops);
                struct xfrm_dst *xdst;
                int tunnel = 0;
                if (unlikely(dst1 == NULL))
                {
                    err = -ENOBUFS;
                    dst_release(&rt->u.dst);
                    goto error;
                }
                if (!dst)
                    // 第一次循环
                    dst = dst1;
                else
                {
                    // 将新分配的安全路由作为前一个路由的child
                    dst_prev->child = dst1;
                    dst1->flags |= DST_NOHASH;
                    dst_clone(dst1);
                }
                xdst = (struct xfrm_dst *)dst1;
                // 安全路由中保留相应的普通路由
                xdst->route = &rt->u.dst;
                xdst->genid = xfrm[i]->genid;
                // 新节点的next是老节点
                dst1->next = dst_prev;
                // 现在prev节点位新节点
                dst_prev = dst1;
                if (xfrm[i]->props.mode != XFRM_MODE_TRANSPORT)
                {
                    remote = xfrm[i]->id.daddr.a4;
                    local  = xfrm[i]->props.saddr.a4;
                    tunnel = 1;
                }
                header_len += xfrm[i]->props.header_len;
                trailer_len += xfrm[i]->props.trailer_len;
                // 如果是通道模式, 需要重新包裹外部IP头, 需要重新寻找外部IP头的路由
                if (tunnel)
                {
                    fl_tunnel.fl4_src = local;
                    fl_tunnel.fl4_dst = remote;
                    err = xfrm_dst_lookup((struct xfrm_dst **)&rt,
                                          &fl_tunnel, AF_INET);
                    if (err)
                        goto error;
                }
                else
                    dst_hold(&rt->u.dst);
            }
            // 将最新节点的child指向最后的普通路由
            dst_prev->child = &rt->u.dst;
            // 最老一个安全路由的path指向最后的普通路由
            dst->path = &rt->u.dst;
            // 将最老安全路由点作为要返回的路由节点链表头
            *dst_p = dst;
            // dst现在是最新节点
            dst = dst_prev;
            // prev现在指向最老安全节点
            dst_prev = *dst_p;
            i = 0;
            /*
             为更好理解上面的操作, 用图来表示. 以上循环形成了下图水平方向的一个链表,
             链表中的最左边的路由项节点dst为最老的安全路由项, 
             新分配的安全路由项通过child链接成链表, child通过next指向老节点, 
             最后一项是数据包封装完后的最后普通路由项. 
             垂直方向的链表是在xfrm_lookup()中形成的, 是多个策略同时起作用的情况,
             一般情况下就只有一个策略, 本文中可不考虑多策略的情况.
                             rt0.u.dst        rt.u.dst            rt.u.dst
                                 ^               ^                   ^
                           route |         route |             route |
                                 |     child     |    child          |
                      bundle  +-----+  -----> +-----+ ----->      +-----+ child
              policy -------> | dst |  <----- | dst | <----- ...  | dst | -----> rt.u.dst
                              +-----+   next  +-----+  next       +-----+
                                 |
                                 |next
                                 |
                                 V     child          child
                              +-----+  -----> +-----+ ----->      +-----+ child
                              | dst |  <----- | dst | <----- ...  | dst | -----> rt.u.dst
                              +-----+   next  +-----+  next       +-----+
                                 |
                                 |next
                                 |
                                 V
                                ....
            */
            // 对新生成的每个安全路由项填充结构参数
            for (; dst_prev != &rt->u.dst; dst_prev = dst_prev->child)
            {
                struct xfrm_dst *x = (struct xfrm_dst*)dst_prev;
                x->u.rt.fl = *fl;
                dst_prev->xfrm = xfrm[i++];
                dst_prev->dev = rt->u.dst.dev;
                if (rt->u.dst.dev)
                    dev_hold(rt->u.dst.dev);
                dst_prev->obsolete = -1;
                dst_prev->flags        |= DST_HOST;
                dst_prev->lastuse = jiffies;
                dst_prev->header_len = header_len;
                dst_prev->nfheader_len = 0;
                dst_prev->trailer_len = trailer_len;
                memcpy(&dst_prev->metrics, &x->route->metrics, sizeof(dst_prev->metrics));
                /* Copy neighbout for reachability confirmation */
                dst_prev->neighbour = neigh_clone(rt->u.dst.neighbour);
                dst_prev->input  = rt->u.dst.input;
                // 注意安全路由的输出函数是xfrm4_output, 在以后分析路由过程时要用到
                dst_prev->output = xfrm4_output;
                if (rt->peer)
                    atomic_inc(&rt->peer->refcnt);
                x->u.rt.peer = rt->peer;
                /* Sheit... I remember I did this right. Apparently,
                 * it was magically lost, so this code needs audit */
                x->u.rt.rt_flags = rt0->rt_flags&(RTCF_BROADCAST|RTCF_MULTICAST|RTCF_LOCAL);
                x->u.rt.rt_type = rt->rt_type;
                x->u.rt.rt_src = rt0->rt_src;
                x->u.rt.rt_dst = rt0->rt_dst;
                x->u.rt.rt_gateway = rt->rt_gateway;
                x->u.rt.rt_spec_dst = rt0->rt_spec_dst;
                x->u.rt.idev = rt0->idev;
                in_dev_hold(rt0->idev);
                header_len -= x->u.dst.xfrm->props.header_len;
                trailer_len -= x->u.dst.xfrm->props.trailer_len;
            }
            // 初始化路由项的MTU值
            xfrm_init_pmtu(dst);
            return 0;
            error:
                if (dst)
                    dst_free(dst);
                return err;
        }
        7.1.1 小结
            IPV4的策略信息结构中的相关成员函数的被调用关系可如下简单表示:
            xfrm_lookup: find xfrm_dst for the skb, create dst_list
                -> xfrm_find_bundle
                    -> afinfo->find_bundle() == __xfrm4_find_bundle
                -> xfrm_tmpl_resolve
                    -> xfrm_tmpl_resolve_one
                        -> xfrm_get_saddr
                            -> afinfo->get_saddr == xfrm4_get_saddr
                                -> xfrm4_dst_lookup
                -> xfrm_bundle_create
                    -> afinfo->bundle_create() == __xfrm4_bundle_create
                        -> xfrm_dst_lookup()
                            -> afinfo->dst_lookup() == xfrm4_dst_lookup
                
            xfrm4_policy_check
                -> xfrm_policy_check
                    -> __xfrm_policy_check
                        -> xfrm_decode_session
                            -> afinfo->decode_session() == _decode_session4
    7.2 IPV4安全路由操作
        路由操作是针对每种类型的路由定义的一个操作结构, 对上层隐藏了不同路由处理内部的处理方法, 
        对于IPSEC的IPV4安全路由(xfrm_dst)的操作结构定义如下:
        /* net/ipv4/xfrm4_policy.c */
        static struct dst_ops xfrm4_dst_ops =
        {
            .family =  AF_INET,
            .protocol =  __constant_htons(ETH_P_IP),
            .gc =   xfrm4_garbage_collect,
            .update_pmtu =  xfrm4_update_pmtu,
            .destroy =  xfrm4_dst_destroy,
            .ifdown =  xfrm4_dst_ifdown,
            .gc_thresh =  1024,
            .entry_size =  sizeof(struct xfrm_dst),
        };
        在xfrm_policy_register_afinfo()函数中, 还定义了安全路由操作结构的其他几个成员函数,
        因为这几个函数是和协议无关的, 所以在登记函数中定义了:
        dst_ops->kmem_cachep = xfrm_dst_cache;
        dst_ops->check = xfrm_dst_check;
        dst_ops->negative_advice = xfrm_negative_advice;
        dst_ops->link_failure = xfrm_link_failure;
        // 安全路由垃圾搜集, 就是调用安全策略信息结构的垃圾搜集函数
        static inline int xfrm4_garbage_collect(void)
        {
            xfrm4_policy_afinfo.garbage_collect();
            return (atomic_read(&xfrm4_dst_ops.entries) > xfrm4_dst_ops.gc_thresh*2);
        }
        // 更新路由的MTU
        static void xfrm4_update_pmtu(struct dst_entry *dst, u32 mtu)
        {
            struct xfrm_dst *xdst = (struct xfrm_dst *)dst;
            struct dst_entry *path = xdst->route;
            // 调用的是安全路由的原始普通路由的MTU更新操作
            path->ops->update_pmtu(path, mtu);
        }
        // 释放安全路由
        static void xfrm4_dst_destroy(struct dst_entry *dst)
        {
            struct xfrm_dst *xdst = (struct xfrm_dst *)dst;
            // 释放inet网卡引用
            if (likely(xdst->u.rt.idev))
                in_dev_put(xdst->u.rt.idev);
            // 释放对方IP的引用
            if (likely(xdst->u.rt.peer))
                inet_putpeer(xdst->u.rt.peer);
            // 释放安全路由
            xfrm_dst_destroy(xdst);
        }
        static inline void xfrm_dst_destroy(struct xfrm_dst *xdst)
        {
            // 释放和安全路由相关的普通路由
            dst_release(xdst->route);
            // 释放SA
            if (likely(xdst->u.dst.xfrm))
                xfrm_state_put(xdst->u.dst.xfrm);
        }
        // 网卡down时的回调操作
        static void xfrm4_dst_ifdown(struct dst_entry *dst, struct net_device *dev,
                                     int unregister)
        {
            struct xfrm_dst *xdst;
            if (!unregister)
                return;
            xdst = (struct xfrm_dst *)dst;
            // 该安全路由对应的网卡是当前停掉的网卡
            if (xdst->u.rt.idev->dev == dev)
            {
                struct in_device *loopback_idev = in_dev_get(&loopback_dev);
                BUG_ON(!loopback_idev);
                do
                {
                    // 释放安全路由网卡
                    in_dev_put(xdst->u.rt.idev);
                    // 安全路由网卡采用自身的回环网卡
                    xdst->u.rt.idev = loopback_idev;
                    in_dev_hold(loopback_idev);
                    // 子路由
                    xdst = (struct xfrm_dst *)xdst->u.dst.child;
                }
                while (xdst->u.dst.xfrm);
                __in_dev_put(loopback_idev);
            }
            xfrm_dst_ifdown(dst, dev);
        }
    7.3 IPV4下的xfrm状态
        IPV4下的xfrm状态在net/ipv4/xfrm4_state.c文件中定义, 主要是定义IPV4的状态信息结构:
        static struct xfrm_state_afinfo xfrm4_state_afinfo =
        {
            .family   = AF_INET,
            .init_flags  = xfrm4_init_flags,
            .init_tempsel  = __xfrm4_init_tempsel,
        };
        该结构中在IPV4下只定义了两个处理函数:
        // 初始化状态标志
        static int xfrm4_init_flags(struct xfrm_state *x)
        {
            if (ipv4_config.no_pmtu_disc)
                x->props.flags |= XFRM_STATE_NOPMTUDISC;
            return 0;
        }
        // 初始化模板选择子
        static void
        __xfrm4_init_tempsel(struct xfrm_state *x, struct flowi *fl,
                             struct xfrm_tmpl *tmpl,
                             xfrm_address_t *daddr, xfrm_address_t *saddr)
        {
            // 填写选择子信息
            // 源地址
            x->sel.daddr.a4 = fl->fl4_dst;
            // 目的地址
            x->sel.saddr.a4 = fl->fl4_src;
            // 目的端口, 掩码
            x->sel.dport = xfrm_flowi_dport(fl);
            x->sel.dport_mask = htons(0xffff);
            // 源端口掩码
            x->sel.sport = xfrm_flowi_sport(fl);
            x->sel.sport_mask = htons(0xffff);
            // 源目的地址长度
            x->sel.prefixlen_d = 32;
            x->sel.prefixlen_s = 32;
            // 协议
            x->sel.proto = fl->proto;
            // 网卡位置
            x->sel.ifindex = fl->oif;
            // 状态ID值
            x->id = tmpl->id;
            if (x->id.daddr.a4 == 0)
                x->id.daddr.a4 = daddr->a4;
            // 支持结构中的参数
            // 源地址
            x->props.saddr = tmpl->saddr;
            if (x->props.saddr.a4 == 0)
                x->props.saddr.a4 = saddr->a4;
            // 模式
            x->props.mode = tmpl->mode;
            // 请求ID
            x->props.reqid = tmpl->reqid;
            // 协议族
            x->props.family = AF_INET;
        }
        7.3.1 小结
            IPV4的状态信息结构中的相关成员函数的被调用关系可如下简单表示:
            xfrm_init_state()
                -> afinfo->init_flags() == xfrm4_init_flags
            xfrm_state_find()
                -> xfrm_init_tempsel()
                    -> afinfo->init_tempsel() == __xfrm4_init_tempsel
    7.4 模式
        xfrm4支持3种模式:
        通道, 传输和BEET模式, 分别在xfrm4_mode_tunnel.c, xfrm4_mode_transport.c和xfrm4_mode_beet.c中定义.
        每个模式都通过结构struct xfrm_mode定义:
            struct xfrm_mode
            {
                int (*input)(struct xfrm_state *x, struct sk_buff *skb);
                int (*output)(struct xfrm_state *x,struct sk_buff *skb);
                struct module *owner;
                unsigned int encap;
            };
        其中input函数在数据接收时调用, output函数数据发出时调用, encap参数表示是否封装.
        7.4.1 通道
            通道模式通过以下结构定义:
            /* net/ipv4/xfrm4_mode_transport.c */
            static struct xfrm_mode xfrm4_tunnel_mode =
            {
                .input = xfrm4_tunnel_input,
                .output = xfrm4_tunnel_output,
                .owner = THIS_MODULE,
                .encap = XFRM_MODE_TUNNEL,
            };
            // 通道模式下的接收函数, 解封装
            static int xfrm4_tunnel_input(struct xfrm_state *x, struct sk_buff *skb)
            {
                struct iphdr *iph = skb->nh.iph;
                int err = -EINVAL;
                // IP协议为IPPROTO_IPIP(4)
                if (iph->protocol != IPPROTO_IPIP)
                    goto out;
                // 需要在skb头留出IP头的长度(20字节)
                if (!pskb_may_pull(skb, sizeof(struct iphdr)))
                    goto out;
                // 如果是clone包,重新拷贝一个
                if (skb_cloned(skb) &&
                        (err = pskb_expand_head(skb, 0, 0, GFP_ATOMIC)))
                    goto out;
                // 复制dscp字段
                if (x->props.flags & XFRM_STATE_DECAP_DSCP)
                    ipv4_copy_dscp(iph, skb->h.ipiph);
                // 非XFRM_STATE_NOECN时进行ECN解封装
                if (!(x->props.flags & XFRM_STATE_NOECN))
                    ipip_ecn_decapsulate(skb);
                // 将硬件地址挪到数据包缓冲区前
                skb->mac.raw = memmove(skb->data - skb->mac_len,
                                       skb->mac.raw, skb->mac_len);
                // 网络部分数据头
                skb->nh.raw = skb->data;
                err = 0;
                out:
                    return err;
            }
            // 通道模式下的数据发出函数, 进行封装
            static int xfrm4_tunnel_output(struct xfrm_state *x, struct sk_buff *skb)
            {
                struct dst_entry *dst = skb->dst;
                struct iphdr *iph, *top_iph;
                int flags;
                iph = skb->nh.iph;
                skb->h.ipiph = iph;
                // 数据头部增加外部IP头的长度
                skb->nh.raw = skb_push(skb, x->props.header_len);
                top_iph = skb->nh.iph;
                // 填写外部IP头参数
                top_iph->ihl = 5;
                top_iph->version = 4;
                /* DS disclosed */
                // 重新计算TOS
                top_iph->tos = INET_ECN_encapsulate(iph->tos, iph->tos);
                flags = x->props.flags;
                if (flags & XFRM_STATE_NOECN)
                    IP_ECN_clear(top_iph);
                // 处理分片包情况
                top_iph->frag_off = (flags & XFRM_STATE_NOPMTUDISC) ?
                                    0 : (iph->frag_off & htons(IP_DF));
                if (!top_iph->frag_off)
                    __ip_select_ident(top_iph, dst->child, 0);
                // TTL
                top_iph->ttl = dst_metric(dst->child, RTAX_HOPLIMIT);
                // 外部源地址用proposal中的源地址
                top_iph->saddr = x->props.saddr.a4;
                // 外部目的地址是SA中的目的地址
                top_iph->daddr = x->id.daddr.a4;
                // 外部IP头内的协议号为IPIP(4)
                top_iph->protocol = IPPROTO_IPIP;
                // IP选项部分设置为0
                memset(&(IPCB(skb)->opt), 0, sizeof(struct ip_options));
                return 0;
            }
        7.4.2 传输
            传输模式下不添加新的IP头, 其实几乎什么都不用做, 老点的2.6内核中就没有专门为传输模式定义.
            传输模式结构定义为:
            /* net/ipv4/xfrm4_mode_transport.c */
            static struct xfrm_mode xfrm4_transport_mode =
            {
                .input = xfrm4_transport_input,
                .output = xfrm4_transport_output,
                .owner = THIS_MODULE,
                .encap = XFRM_MODE_TRANSPORT,
            };
            /* Remove encapsulation header.
             *
             * The IP header will be moved over the top of the encapsulation header.
             *
             * On entry, skb->h shall point to where the IP header should be and skb->nh
             * shall be set to where the IP header currently is.  skb->data shall point
             * to the start of the payload.
             */
            // 传输模式下的数据输入函数
            static int xfrm4_transport_input(struct xfrm_state *x, struct sk_buff *skb)
            {
                // data指向负载头, h指向IP头, 但很多情况下两者相同
                int ihl = skb->data - skb->h.raw;
                // 如果h和nh不同, 将nh所指向IP头部分移动到h处
                if (skb->h.raw != skb->nh.raw)
                    skb->nh.raw = memmove(skb->h.raw, skb->nh.raw, ihl);
                // 增加数据包长度, 重新对数据包长度赋值
                skb->nh.iph->tot_len = htons(skb->len + ihl);
                skb->h.raw = skb->data;
                return 0;
            }
            /* Add encapsulation header.
             *
             * The IP header will be moved forward to make space for the encapsulation
             * header.
             *
             * On exit, skb->h will be set to the start of the payload to be processed
             * by x->type->output and skb->nh will be set to the top IP header.
             */
            // 传输模式下的数据发出函数
            static int xfrm4_transport_output(struct xfrm_state *x, struct sk_buff *skb)
            {
                struct iphdr *iph;
                int ihl;
                // nh和赋值给h
                iph = skb->nh.iph;
                skb->h.ipiph = iph;
                // ip头长度
                ihl = iph->ihl * 4;
                // 重新计算h位置
                skb->h.raw += ihl;
                // 重新计算新的nh位置,增加proposal中的头长度, 拷贝原来的IP头数据
                skb->nh.raw = memmove(skb_push(skb, x->props.header_len), iph, ihl);
                return 0;
            }
        7.4.3 BEET
            封装成BEETPH(94)包, 非标准IPSEC, 略.
        7.4.4 小结
            和xfrm_mode相关的xfrm函数有:
            登记:
            int xfrm_register_mode(struct xfrm_mode *mode, int family);
            撤销:
            int xfrm_unregister_mode(struct xfrm_mode *mode, int family)
            获取:
            struct xfrm_mode *xfrm_get_mode(unsigned int encap, int family)
            释放: void xfrm_put_mode(struct xfrm_mode *mode)
            xfrm_mode的输入输出函数调用:
            xfrm4_rcv_encap()
            -> x->mode->input
            xfrm4_output_one()
            -> x->mode->output
    7.5 数据接收
        IPV4的IPSEC数据接收处理在net/ipv4/xfrm4_input.c中定义, 作为AH和ESP协议数据接收处理函数.
        /* net/ipv4/xfrm4_input.c */
        int xfrm4_rcv(struct sk_buff *skb)
        {
            return xfrm4_rcv_encap(skb, 0);
        }
        实际就是xfrm4_rcv_encap，封装类型参数设置为0,在NAT-T时IPSEC数据被封装在UDP包中时, 该参数才非0.
        int xfrm4_rcv_encap(struct sk_buff *skb, __u16 encap_type)
        {
            int err;
            __be32 spi, seq;
            struct xfrm_state *xfrm_vec[XFRM_MAX_DEPTH];
            struct xfrm_state *x;
            int xfrm_nr = 0;
            int decaps = 0;
            // 获取skb中的spi和序列号信息
            if ((err = xfrm4_parse_spi(skb, skb->nh.iph->protocol, &spi, &seq)) != 0)
                goto drop;
            // 进入循环进行解包操作
            do
            {
                struct iphdr *iph = skb->nh.iph;
                // 循环解包次数太深的话放弃
                if (xfrm_nr == XFRM_MAX_DEPTH)
                    goto drop;
                // 根据地址, SPI和协议查找SA
                x = xfrm_state_lookup((xfrm_address_t *)&iph->daddr, spi, iph->protocol, AF_INET);
                if (x == NULL)
                    goto drop;
                // 以下根据SA定义的操作对数据解码
                spin_lock(&x->lock);
                if (unlikely(x->km.state != XFRM_STATE_VALID))
                    goto drop_unlock;
                // 检查由SA指定的封装类型是否和函数指定的封装类型相同
                if ((x->encap ? x->encap->encap_type : 0) != encap_type)
                    goto drop_unlock;
                // SA重放窗口检查
                if (x->props.replay_window && xfrm_replay_check(x, seq))
                    goto drop_unlock;
                // SA生存期检查
                if (xfrm_state_check_expire(x))
                    goto drop_unlock;
                // type可为esp,ah,ipcomp, ipip等, 对输入数据解密
                if (x->type->input(x, skb))
                    goto drop_unlock;
                /* only the first xfrm gets the encap type */
                encap_type = 0;
                // 更新重放窗口
                if (x->props.replay_window)
                    xfrm_replay_advance(x, seq);
                // 包数,字节数统计
                x->curlft.bytes += skb->len;
                x->curlft.packets++;
                spin_unlock(&x->lock);
                // 保存数据解封用的SA, 增加SA数量计数
                xfrm_vec[xfrm_nr++] = x;
                // mode可为通道,传输等模式, 对输入数据解封装
                if (x->mode->input(x, skb))
                    goto drop;
                // 如果是IPSEC通道模式，将decaps参数置1，否则表示是传输模式
                if (x->props.mode == XFRM_MODE_TUNNEL)
                {
                    decaps = 1;
                    break;
                }
                // 看内层协议是否还要继续解包, 不需要解时返回1, 需要解时返回0, 错误返回负数
                // 协议类型可以多层封装的,比如用AH封装ESP, 就得先解完AH再解ESP
                if ((err = xfrm_parse_spi(skb, skb->nh.iph->protocol, &spi, &seq)) < 0)
                    goto drop;
            }
            while (!err);
            /* Allocate new secpath or COW existing one. */
            // 为skb包建立新的安全路径(struct sec_path)
            if (!skb->sp || atomic_read(&skb->sp->refcnt) != 1)
            {
                struct sec_path *sp;
                sp = secpath_dup(skb->sp);
                if (!sp)
                    goto drop;
                if (skb->sp)
                    secpath_put(skb->sp);
                skb->sp = sp;
            }
            if (xfrm_nr + skb->sp->len > XFRM_MAX_DEPTH)
                goto drop;
            // 将刚才循环解包用到的SA拷贝到安全路径
            // 因此检查一个数据包是否是普通明文包还是解密后的明文包就看skb->sp参数是否为空
            memcpy(skb->sp->xvec + skb->sp->len, xfrm_vec,
                   xfrm_nr * sizeof(xfrm_vec[0]));
            skb->sp->len += xfrm_nr;
            nf_reset(skb);
            if (decaps)
            {
                // 通道模式
                if (!(skb->dev->flags&IFF_LOOPBACK))
                {
                    dst_release(skb->dst);
                    skb->dst = NULL;
                }
                // 重新进入网卡接收函数
                netif_rx(skb);
                return 0;
            }
            else
            {
                // 传输模式
                    #ifdef CONFIG_NETFILTER
                    // 如果定义NETFILTER, 进入PRE_ROUTING链处理,然后进入路由选择处理
                    // 其实现在已经处于INPUT点, 但解码后需要将该包作为一个新包看待
                    // 可能需要进行目的NAT操作, 这时候可能目的地址就会改变不是到自身
                    // 的了, 因此需要将其相当于是放回PRE_PROUTING点去操作, 重新找路由
                    // 这也说明可以制定针对解码后明文包的NAT规则,在还是加密包的时候不匹配
                    // 但解码后能匹配上
                    __skb_push(skb, skb->data - skb->nh.raw);
                    skb->nh.iph->tot_len = htons(skb->len);
                    ip_send_check(skb->nh.iph);
                    NF_HOOK(PF_INET, NF_IP_PRE_ROUTING, skb, skb->dev, NULL,
                            xfrm4_rcv_encap_finish);
                    return 0;
                #else
                    // 内核不支持NETFILTER, 该包肯定就是到自身的了
                    // 返回IP协议的负值, 表示重新进行IP层协议的处理
                    // 用解码后的内层协议来处理数据
                    return -skb->nh.iph->protocol;
                #endif
            }
            drop_unlock:
                spin_unlock(&x->lock);
                xfrm_state_put(x);
            drop:
                while (--xfrm_nr >= 0)
                    xfrm_state_put(xfrm_vec[xfrm_nr]);
                kfree_skb(skb);
                return 0;
        }
        // 解析AH,ESP数据包中的SPI和序号
        static int xfrm4_parse_spi(struct sk_buff *skb, u8 nexthdr, __be32 *spi, __be32 *seq)
        {
            switch (nexthdr)
            {
                // 如果只是普通的IPIP包, SPI为源地址, 序号位0
                case IPPROTO_IPIP:
                    *spi = skb->nh.iph->saddr;
                    *seq = 0;
                    return 0;
            }
            // 否则解析AH/ESP/COMP协议头中的SPI和序号
            return xfrm_parse_spi(skb, nexthdr, spi, seq);
        }
        // 接收封装完成处理函数
        static inline int xfrm4_rcv_encap_finish(struct sk_buff *skb)
        {
            struct iphdr *iph = skb->nh.iph;
            // 如果没有路由, 重新查找路由
            if (skb->dst == NULL)
            {
                if (ip_route_input(skb, iph->daddr, iph->saddr, iph->tos,
                                   skb->dev))
                    goto drop;
            }
            // 调用相关的路由输入函数
            return dst_input(skb);
            drop:
                kfree_skb(skb);
                return NET_RX_DROP;
        }
        调用关系:
        ip_rcv
            -> (AH/ESP) net_protocol->handler == xfrm4_rcv
                -> xfrm4_rcv_encap
                    -> xfrm4_parse_spi
                        -> xfrm_parse_spi
                    -> xfrm4_rcv_encap_finish
    7.6 数据发送
        IPV4的IPSEC数据发送处理在net/ipv4/xfrm4_output.c中定义,作为安全路由的输出函数:
        int xfrm4_output(struct sk_buff *skb)
        {
            // 就是一个条件HOOK, 当skb包不带IPSKB_REROUTED标志时进入POSTROUTING点的NAT操作
            // 这是数据在xfrm策略中多个bundle时会多次调用, 也就是数据在封装完成前可以进行
            // 源NAT操作
            // HOOK出口函数为xfrm4_output_finish
            return NF_HOOK_COND(PF_INET, NF_IP_POST_ROUTING, skb, NULL, skb->dst->dev,
                                xfrm4_output_finish,
                                !(IPCB(skb)->flags & IPSKB_REROUTED));
        }
        // 发送结束处理
        static int xfrm4_output_finish(struct sk_buff *skb)
        {
            struct sk_buff *segs;
            #ifdef CONFIG_NETFILTER
                // 如果内核定义了NETFILTER, 当到达最后一个路由(普通路由)时, 设置IPSKB_REROUTED
                // 标志, 进行普通路由发出函数(ip_output), 设置该标志后不进行源NAT操作
                if (!skb->dst->xfrm)
                {
                    IPCB(skb)->flags |= IPSKB_REROUTED;
                    return dst_output(skb);
                }
            #endif
            // 如果skb包不是是gso, 转xfrm4_output_finish2
            // gso是什么意思现在还不知道, 以后再仔细分析
            if (!skb_is_gso(skb))
                return xfrm4_output_finish2(skb);
            // 处理gso数据包, 最终也是使用xfrm4_output_finish2处理数据包
            skb->protocol = htons(ETH_P_IP);
            segs = skb_gso_segment(skb, 0);
            kfree_skb(skb);
            if (unlikely(IS_ERR(segs)))
                return PTR_ERR(segs);
            do
            {
                struct sk_buff *nskb = segs->next;
                int err;
                segs->next = NULL;
                err = xfrm4_output_finish2(segs);
                if (unlikely(err))
                {
                    while ((segs = nskb))
                    {
                        nskb = segs->next;
                        segs->next = NULL;
                        kfree_skb(segs);
                    }
                    return err;
                }
                segs = nskb;
            }
            while (segs);
            return 0;
        }
        // 第2级发送结束处理
        static int xfrm4_output_finish2(struct sk_buff *skb)
        {
            int err;
            // 根据安全路由包装要发送数据
            while (likely((err = xfrm4_output_one(skb)) == 0))
            {
                // 处理成功
                // 释放skb中的netfilter信息
                nf_reset(skb);
                // 重新将该包作为初始发送包, 进入OUTPUT点处理, 注意这是个函数而不是宏
                // 如果内核没定义NETFILTER, 该函数只是个空函数
                // 返回1表示NF_ACCEPT
                err = nf_hook(PF_INET, NF_IP_LOCAL_OUT, &skb, NULL,
                              skb->dst->dev, dst_output);
                if (unlikely(err != 1))
                    break;
                // 如果已经没有SA, 就只是个普通包了, 路由发送(ip_output)返回, 退出循环
                if (!skb->dst->xfrm)
                    return dst_output(skb);
                // 如果还有SA, 目前还只是中间状态, 还可以进行SNAT操作, 进入POSTROUTING点处理
                err = nf_hook(PF_INET, NF_IP_POST_ROUTING, &skb, NULL,
                              skb->dst->dev, xfrm4_output_finish2);
                if (unlikely(err != 1))
                    break;
            }
            return err;
        }
        // 按安全路由链表的安全路由处理数据, 该链表反映了多个SA对数据包进行处理
        // 链表是在__xfrm4_bundle_create函数中建立的
        static int xfrm4_output_one(struct sk_buff *skb)
        {
            // 安全路由
            struct dst_entry *dst = skb->dst;
            // 相关SA
            struct xfrm_state *x = dst->xfrm;
            int err;
            // skb包校验和 检查
            if (skb->ip_summed == CHECKSUM_PARTIAL)
            {
                err = skb_checksum_help(skb);
                if (err)
                    goto error_nolock;
            }
            // 如果是通道模式, 检查skb数据长度, 并进行相关处理, 通道模式下封装后的数据包长度可能
            // 会超过1500字节的
            if (x->props.mode == XFRM_MODE_TUNNEL)
            {
                err = xfrm4_tunnel_check_size(skb);
                if (err)
                    goto error_nolock;
            }
            do
            {
                spin_lock_bh(&x->lock);
                // SA合法性检查
                err = xfrm_state_check(x, skb);
                if (err)
                    goto error;
                // 调用模式输出函数, 如通道封装, 此时外部IP头协议为IPIP
                err = x->mode->output(x, skb);
                if (err)
                    goto error;
                // 调用协议输出, 如对应ESP协议来说是esp4_output, 此时外部IP头协议会改为ESP
                err = x->type->output(x, skb);
                if (err)
                    goto error;
                // 更新SA中的当前生命期结构中的包和字节计数
                x->curlft.bytes += skb->len;
                x->curlft.packets++;
                spin_unlock_bh(&x->lock);
                // 转移到下一个子路由
                if (!(skb->dst = dst_pop(dst)))
                {
                    err = -EHOSTUNREACH;
                    goto error_nolock;
                }
                // dst和x参数更新为子路由中的安全路由和SA
                dst = skb->dst;
                x = dst->xfrm;
                // 循环条件是SA非空, 而且SA提议模式不是通道模式
            }
            while (x && (x->props.mode != XFRM_MODE_TUNNEL));
            // skb中设置IPSKB_XFRM_TRANSFORMED标志
            // 有该标志的数据包将NAT操作后将不进行一些特殊检查
            IPCB(skb)->flags |= IPSKB_XFRM_TRANSFORMED;
            err = 0;
            out_exit:
                return err;
            error:
                spin_unlock_bh(&x->lock);
            error_nolock:
                kfree_skb(skb);
                goto out_exit;
        }
        IPSEC输出函数调用关系:
        dst_output
        -> xfrm_dst->output == xfrm4_output
        -> NF_HOOK(POSTROUTING)
        -> xfrm4_output_finish
        -> xfrm4_output_finish2
        -> xfrm4_output_one
    7.7 NAT-T支持
        在支持NAT穿越的IPSEC处理中，是通过UDP数据包来封装IPSEC数据(ESP数据包)，
        因此在对UDP处理时需要进行特殊处理。
        由于IKE同样是用UDP处理的, 区分是IKE包还是封装的ESP包就看数据头部头4字节表示的SPI值, 
        SPI为0表示是IKE包, 由IKE用户空间程序接收进行处理, SPI非0表示是UDP封装的ESP包, 需进行ESP解封。
    7.7.1 接收数据
        被UDP封装的IPSEC包在接收时会先按普通UDP包接收，在UDP处理中再解开该包后进行IPSEC处理
        /* net/ipv4/udp.c */
        // 正常接收的UDP包都将进入该函数
        static int udp_queue_rcv_skb(struct sock * sk, struct sk_buff *skb)
        {
            struct udp_sock *up = udp_sk(sk);
            int rc;
            /*
             * Charge it to the socket, dropping if the queue is full.
             */
            // 检查针对该sock，skb包的输入方法上的是否有安全策略
            if (!xfrm4_policy_check(sk, XFRM_POLICY_IN, skb))
            {
                kfree_skb(skb);
                return -1;
            }
            nf_reset(skb);
            // 检查该SOCK是否是IPSEC封装的，该参数通过setsockopt系统调用的UDP_ENCAP选项设置
            // 一般是IKE程序在打开UDP4500端口时设置的
            if (up->encap_type)
            {
                /*
                 * This is an encapsulation socket, so let's see if this is
                 * an encapsulated packet.
                 * If it's a keepalive packet, then just eat it.
                 * If it's an encapsulateed packet, then pass it to the
                 * IPsec xfrm input and return the response
                 * appropriately.  Otherwise, just fall through and
                 * pass this up the UDP socket.
                 */
                int ret;
                // 进入UDP封装接收, 判断是否是ESP包
                // 返回值小于0表示是IPSEC包, 大于0表示是普通UDP包, 等于0表示是错误包
                ret = udp_encap_rcv(sk, skb);
                if (ret == 0)
                {
                    /* Eat the packet .. */
                    kfree_skb(skb);
                    return 0;
                }
                if (ret < 0)
                {
                    // 进行IPSEC接收处理
                    /* process the ESP packet */
                    ret = xfrm4_rcv_encap(skb, up->encap_type);
                    UDP_INC_STATS_BH(UDP_MIB_INDATAGRAMS);
                    return -ret;
                }
                /* FALLTHROUGH -- it's a UDP Packet */
            }
            // 以下按普通UDP包接收处理, 分析略
            if (sk->sk_filter && skb->ip_summed != CHECKSUM_UNNECESSARY)
            {
                if (__udp_checksum_complete(skb))
                {
                    UDP_INC_STATS_BH(UDP_MIB_INERRORS);
                    kfree_skb(skb);
                    return -1;
                }
                skb->ip_summed = CHECKSUM_UNNECESSARY;
            }
            if ((rc = sock_queue_rcv_skb(sk,skb)) < 0)
            {
                /* Note that an ENOMEM error is charged twice */
                if (rc == -ENOMEM)
                    UDP_INC_STATS_BH(UDP_MIB_RCVBUFERRORS);
                UDP_INC_STATS_BH(UDP_MIB_INERRORS);
                kfree_skb(skb);
                return -1;
            }
            UDP_INC_STATS_BH(UDP_MIB_INDATAGRAMS);
            return 0;
        }
        /* return:
         *  1  if the the UDP system should process it
         * 0  if we should drop this packet
         *  -1 if it should get processed by xfrm4_rcv_encap
         */
        static int udp_encap_rcv(struct sock * sk, struct sk_buff *skb)
        {
            #ifndef CONFIG_XFRM
            // 在内核不支持IPSEC情况下直接返回1
                return 1;
            #else
                struct udp_sock *up = udp_sk(sk);
                struct udphdr *uh;
                struct iphdr *iph;
                int iphlen, len;
                __u8 *udpdata;
                __be32 *udpdata32;
                // sock的封装标志值
                __u16 encap_type = up->encap_type;
                /* if we're overly short, let UDP handle it */
                // UDP数据包中数据部分的长度
                len = skb->len - sizeof(struct udphdr);
                if (len <= 0)
                    return 1;
                /* if this is not encapsulated socket, then just return now */
                // 没定义封装处理, 返回1, 普通处理
                if (!encap_type)
                    return 1;
                /* If this is a paged skb, make sure we pull up
                 * whatever data we need to look at. */
                if (!pskb_may_pull(skb, sizeof(struct udphdr) + min(len, 8)))
                    return 1;
                /* Now we can get the pointers */
                uh = skb->h.uh;
                udpdata = (__u8 *)uh + sizeof(struct udphdr);
                udpdata32 = (__be32 *)udpdata;
                switch (encap_type)
                {
                default:
                // 在UDP中封装ESP
                case UDP_ENCAP_ESPINUDP:
                    /* Check if this is a keepalive packet.  If so, eat it. */
                    if (len == 1 && udpdata[0] == 0xff)
                    {
                        // 只是普通UDP的IPSEC通道保活包, 直接丢弃
                        return 0;
                    }
                    else if (len > sizeof(struct ip_esp_hdr) && udpdata32[0] != 0 )
                    {
                        // 头4字节非零, ESP包，需要下一步解析
                        /* ESP Packet without Non-ESP header */
                        len = sizeof(struct udphdr);
                    }
                    else
                        // 这是IKE包，按普通UDP接收处理
                        /* Must be an IKE packet.. pass it through */
                        return 1;
                    break;
                case UDP_ENCAP_ESPINUDP_NON_IKE:
                    /* Check if this is a keepalive packet.  If so, eat it. */
                    if (len == 1 && udpdata[0] == 0xff)
                    {
                        // IPSEC通道保活包, 丢弃
                        return 0;
                    }
                    else if (len > 2 * sizeof(u32) + sizeof(struct ip_esp_hdr) &&
                             udpdata32[0] == 0 && udpdata32[1] == 0)
                    {
                        // 头4字节非零, ESP包，需要下一步解析
                        /* ESP Packet with Non-IKE marker */
                        len = sizeof(struct udphdr) + 2 * sizeof(u32);
                    }
                    else
                        // 这是IKE数据包,由
                        /* Must be an IKE packet.. pass it through */
                        return 1;
                    break;
                }
                /* At this point we are sure that this is an ESPinUDP packet,
                 * so we need to remove 'len' bytes from the packet (the UDP
                 * header and optional ESP marker bytes) and then modify the
                 * protocol to ESP, and then call into the transform receiver.
                 */
                // 如果是clone包需要复制成独立包
                if (skb_cloned(skb) && pskb_expand_head(skb, 0, 0, GFP_ATOMIC))
                    return 0;
                // 检查数据长度
                /* Now we can update and verify the packet length... */
                iph = skb->nh.iph;
                iphlen = iph->ihl << 2;
                iph->tot_len = htons(ntohs(iph->tot_len) - len);
                if (skb->len < iphlen + len)
                {
                    /* packet is too small!?! */
                    return 0;
                }
                /* pull the data buffer up to the ESP header and set the
                 * transport header to point to ESP.  Keep UDP on the stack
                 * for later.
                 */
                // 修改IP上层头位置
                skb->h.raw = skb_pull(skb, len);
                // 更改IP头协议类型为ESP包, 返回-1
                /* modify the protocol (it's ESP!) */
                iph->protocol = IPPROTO_ESP;
                /* and let the caller know to send this into the ESP processor... */
                return -1;
            #endif
        }
        函数调用关系：
        udp_rcv
        ->udp_queue_rcv_skb
        -> udp_encap_rcv
        -> xfrm4_policy_check
        -> xfrm_policy_check
        -> __xfrm_policy_check
    7.7.2 ESP包的UDP封装
        对于ESP包的UDP封装处理, 在下一节ESP协议数据包的输出处理中介绍.        
8. 安全协议
    与IPSEC相关的安全协议是AH(51)和ESP(50), IPSEC使用这两个协议对普通数据包进行封装, 
    AH只认证不加密, ESP既加密又认证, 当ESP和AH同时使用时, 一般都是先进行ESP封装, 
    再进行AH封装, 因为AH是对整个IP包进行验证的, 而ESP只验证负载部分.
    在IPV4下的AH和ESP的协议实现在net/ipv4/ah4.c和net/ipv4/esp4.c中, 
    每个协议实现实际是要完成两个结构:
    struct net_protocol和struct xfrm_type, 
    前者用于处理接收的该协议类型的IP包, 后者则是IPSEC协议处理.
    8.1 AH
        8.1.1 初始化
            /* net/ipv4/ah4.c */
            static int __init ah4_init(void)
            {
                // 登记AH协议的xfrm协议处理结构
                if (xfrm_register_type(&ah_type, AF_INET) < 0)
                {
                    printk(KERN_INFO "ip ah init: can't add xfrm type\n");
                    return -EAGAIN;
                }
                // 登记AH协议到IP协议
                if (inet_add_protocol(&ah4_protocol, IPPROTO_AH) < 0)
                {
                    printk(KERN_INFO "ip ah init: can't add protocol\n");
                    xfrm_unregister_type(&ah_type, AF_INET);
                    return -EAGAIN;
                }
                return 0;
            }
        8.1.2 IPV4下的AH协议处理结构
            // AH协议处理结构, 接收到IPV4包后, 系统根据IP头中的protocol字段选择相应的上层协议处理
            // 函数, 当IP协议号是51时, 数据包将调用该结构的handler处理函数:
            static struct net_protocol ah4_protocol =
            {
                .handler = xfrm4_rcv,
                .err_handler = ah4_err,
                .no_policy = 1,
            };
            AH协议结构的handler函数为xfrm4_rcv, 在net/ipv4/xfrm4_input.c 中定义, 在上一篇中进行了介绍.
            // 错误处理, 收到ICMP错误包时的处理情况, 此时的skb包是ICMP包
            static void ah4_err(struct sk_buff *skb, u32 info)
            {
                // 应用层, data指向ICMP错误包里的内部IP头
                struct iphdr *iph = (struct iphdr*)skb->data;
                // AH头
                struct ip_auth_hdr *ah = (struct ip_auth_hdr*)(skb->data+(iph->ihl<<2));
                struct xfrm_state *x;
                // ICMP错误类型检查, 本处理函数只处理"目的不可达"和"需要分片"两种错误
                if (skb->h.icmph->type != ICMP_DEST_UNREACH ||
                        skb->h.icmph->code != ICMP_FRAG_NEEDED)
                    return;
                // 重新查找SA
                x = xfrm_state_lookup((xfrm_address_t *)&iph->daddr, ah->spi, IPPROTO_AH, AF_INET);
                if (!x)
                    return;
                printk(KERN_DEBUG "pmtu discovery on SA AH/%08x/%08x\n",
                       ntohl(ah->spi), ntohl(iph->daddr));
                xfrm_state_put(x);
            }
        8.1.3 AH4协议的IPSEC处理结构
            // AH4的xfrm协议处理结构
            static struct xfrm_type ah_type =
            {
                .description = "AH4",
                .owner  = THIS_MODULE,
                .proto       = IPPROTO_AH,
                // 状态初始化
                .init_state = ah_init_state,
                // 协议释放
                .destructor = ah_destroy,
                // 协议输入
                .input  = ah_input,
                // 协议输出
                .output  = ah_output
            };
            结构的重点是input和ouput函数
            8.1.3.1 状态初始化
                ah_data数据结构:
                /* include/net/ah.h */
                struct ah_data
                {
                    // 密钥指针
                    u8   *key;
                    // 密钥长度
                    int   key_len;
                    // 工作初始化向量
                    u8   *work_icv;
                    // 初始化向量完整长度
                    int   icv_full_len;
                    // 初始化向量截断长度
                    int   icv_trunc_len;
                    // HASH算法
                    struct crypto_hash *tfm;
                };
                // 该函数被xfrm状态(SA)初始化函数xfrm_init_state调用
                // 用来生成SA中所用的AH数据处理结构相关信息
                static int ah_init_state(struct xfrm_state *x)
                {
                    struct ah_data *ahp = NULL;
                    struct xfrm_algo_desc *aalg_desc;
                    struct crypto_hash *tfm;
                    // 对AH协议的SA, 认证算法是必须的, 否则就没法进行AH认证了
                    if (!x->aalg)
                        goto error;
                    /* null auth can use a zero length key */
                    // 认证算法密钥长度要大于512
                    if (x->aalg->alg_key_len > 512)
                        goto error;
                    // 如果要进行UDP封装(进行NAT穿越), 错误, 因为AH是不支持NAT的
                    if (x->encap)
                        goto error;
                    // 分配ah_data数据结构空间
                    ahp = kzalloc(sizeof(*ahp), GFP_KERNEL);
                    if (ahp == NULL)
                        return -ENOMEM;
                    // 设置AH数据结构的密钥和长度
                    ahp->key = x->aalg->alg_key;
                    ahp->key_len = (x->aalg->alg_key_len+7)/8;
                    // 分配认证算法HASH结构指针并赋值给AH数据结构
                    // 算法是固定相同的, 但在每个应用使用算法时的上下文是不同的, 该结构就是描述具体应用
                    // 时的相关处理的上下文数据的
                    tfm = crypto_alloc_hash(x->aalg->alg_name, 0, CRYPTO_ALG_ASYNC);
                    if (IS_ERR(tfm))
                        goto error;
                    ahp->tfm = tfm;
                    // 设置认证算法密钥
                    if (crypto_hash_setkey(tfm, ahp->key, ahp->key_len))
                        goto error;
                    /*
                    * Lookup the algorithm description maintained by xfrm_algo,
                    * verify crypto transform properties, and store information
                    * we need for AH processing.  This lookup cannot fail here
                    * after a successful crypto_alloc_hash().
                    */
                    // 分配算法描述结构
                    aalg_desc = xfrm_aalg_get_byname(x->aalg->alg_name, 0);
                    BUG_ON(!aalg_desc);
                    if (aalg_desc->uinfo.auth.icv_fullbits/8 !=
                            crypto_hash_digestsize(tfm))
                    {
                        printk(KERN_INFO "AH: %s digestsize %u != %hu\n",
                               x->aalg->alg_name, crypto_hash_digestsize(tfm),
                               aalg_desc->uinfo.auth.icv_fullbits/8);
                        goto error;
                    }
                    // AH数据结构的初始化向量的总长和截断长度的赋值
                    ahp->icv_full_len = aalg_desc->uinfo.auth.icv_fullbits/8;
                    ahp->icv_trunc_len = aalg_desc->uinfo.auth.icv_truncbits/8;
                    BUG_ON(ahp->icv_trunc_len > MAX_AH_AUTH_LEN);
                    // 分配初始化向量空间, 没对其赋值, 其初始值就是随机值, 这也是初始化向量所需要的
                    ahp->work_icv = kmalloc(ahp->icv_full_len, GFP_KERNEL);
                    if (!ahp->work_icv)
                        goto error;
                    // AH类型SA中AH头长度: ip_auth_hdr结构和初始化向量长度, 按8字节对齐
                    // 反映在AH封装操作时要将数据包增加的长度
                    x->props.header_len = XFRM_ALIGN8(sizeof(struct ip_auth_hdr) + ahp->icv_trunc_len);
                    // 如果是通道模式, 增加IP头长度
                    if (x->props.mode == XFRM_MODE_TUNNEL)
                        x->props.header_len += sizeof(struct iphdr);
                    // SA数据指向AH数据结构
                    x->data = ahp;
                    return 0;
                    error:
                        if (ahp)
                        {
                            kfree(ahp->work_icv);
                            crypto_free_hash(ahp->tfm);
                            kfree(ahp);
                        }
                        return -EINVAL;
                }
            8.1.3.2 协议释放
                // 该函数被xfrm状态(SA)释放函数xfrm_state_gc_destroy()调用
                static void ah_destroy(struct xfrm_state *x)
                {
                    struct ah_data *ahp = x->data;
                    if (!ahp)
                        return;
                    // 释放初始化向量空间
                    kfree(ahp->work_icv);
                    ahp->work_icv = NULL;
                    // 算法描述释放
                    crypto_free_hash(ahp->tfm);
                    ahp->tfm = NULL;
                    // AH数据结构释放
                    kfree(ahp);
                }
            8.1.3.3 协议输入
                // 接收数据处理, 在xfrm4_rcv_encap()函数中调用
                // 进行AH认证, 剥离AH头
                static int ah_input(struct xfrm_state *x, struct sk_buff *skb)
                {
                    int ah_hlen;
                    int ihl;
                    int err = -EINVAL;
                    struct iphdr *iph;
                    struct ip_auth_hdr *ah;
                    struct ah_data *ahp;
                    // IP头备份空间
                    char work_buf[60];
                    // skb数据包要准备留出AH头空间
                    if (!pskb_may_pull(skb, sizeof(struct ip_auth_hdr)))
                        goto out;
                    // IP上层数据为AH数据
                    ah = (struct ip_auth_hdr*)skb->data;
                    // SA相关的AH处理数据
                    ahp = x->data;
                    ah_hlen = (ah->hdrlen + 2) << 2;
                    // AH头部长度合法性检查
                    if (ah_hlen != XFRM_ALIGN8(sizeof(struct ip_auth_hdr) + ahp->icv_full_len) &&
                            ah_hlen != XFRM_ALIGN8(sizeof(struct ip_auth_hdr) + ahp->icv_trunc_len))
                        goto out;
                    // skb数据包要准备留出实际AH头空间
                    if (!pskb_may_pull(skb, ah_hlen))
                        goto out;
                    /* We are going to _remove_ AH header to keep sockets happy,
                    * so... Later this can change. */
                    // 对于clone的包要复制成独立包
                    if (skb_cloned(skb) &&
                            pskb_expand_head(skb, 0, 0, GFP_ATOMIC))
                        goto out;
                    skb->ip_summed = CHECKSUM_NONE;
                    // 可能包已经进行了复制, 所以对ah重新赋值
                    ah = (struct ip_auth_hdr*)skb->data;
                    iph = skb->nh.iph;
                    // IP头长度
                    ihl = skb->data - skb->nh.raw;
                    // 备份外部IP头数据
                    memcpy(work_buf, iph, ihl);
                    // 将IP头中的一些参数清零, 这些参数不进行认证
                    iph->ttl = 0;
                    iph->tos = 0;
                    iph->frag_off = 0;
                    iph->check = 0;
                    // IP头长度超过20字节时,处理IP选项参数
                    if (ihl > sizeof(*iph))
                    {
                        u32 dummy;
                        if (ip_clear_mutable_options(iph, &dummy))
                            goto out;
                    }
                    {
                    // 认证数据缓冲区
                        u8 auth_data[MAX_AH_AUTH_LEN];
                    // 拷贝数据包中的认证数据到缓冲区
                        memcpy(auth_data, ah->auth_data, ahp->icv_trunc_len);
                    // 包括IP头部分数据
                        skb_push(skb, ihl);
                    // 计算认证值是否匹配, 非0表示出错
                        err = ah_mac_digest(ahp, skb, ah->auth_data);
                    // 认证失败返回错误
                        if (err)
                            goto out;
                        err = -EINVAL;
                    // 复制一定长度的认证数据作为初始化向量
                        if (memcmp(ahp->work_icv, auth_data, ahp->icv_trunc_len))
                        {
                            x->stats.integrity_failed++;
                            goto out;
                        }
                    }
                    // 将备份的IP头缓冲区中的协议改为AH内部包裹的协议
                    ((struct iphdr*)work_buf)->protocol = ah->nexthdr;
                    // 将原来IP头数据拷贝到原来AH头后面作为新IP头
                    skb->h.raw = memcpy(skb->nh.raw += ah_hlen, work_buf, ihl);
                    // skb包缩减原来的IP头和AH头, 以新IP头作为数据开始
                    __skb_pull(skb, ah_hlen + ihl);
                    return 0;
                    out:
                        return err;
                }
            8.1.3.4 协议输出
                // 发送数据处理, 在xfrm4_output_one()中调用
                // 计算AH认证值, 添加AH头
                static int ah_output(struct xfrm_state *x, struct sk_buff *skb)
                {
                    int err;
                    struct iphdr *iph, *top_iph;
                    struct ip_auth_hdr *ah;
                    struct ah_data *ahp;
                    // 临时IP头缓冲区, 最大IP头60字节
                    union
                    {
                        struct iphdr iph;
                        char   buf[60];
                    } tmp_iph;
                    // 当前的IP头将作为最外部IP头
                    top_iph = skb->nh.iph;
                    // 临时IP头,用于临时保存IP头内部分字段数据
                    iph = &tmp_iph.iph;
                    // 将当前IP头中不进行认证的字段数据复制到临时IP头
                    iph->tos = top_iph->tos;
                    iph->ttl = top_iph->ttl;
                    iph->frag_off = top_iph->frag_off;
                    // 如果有IP选项, 处理IP选项
                    if (top_iph->ihl != 5)
                    {
                        iph->daddr = top_iph->daddr;
                        memcpy(iph+1, top_iph+1, top_iph->ihl*4 - sizeof(struct iphdr));
                        err = ip_clear_mutable_options(top_iph, &top_iph->daddr);
                        if (err)
                            goto error;
                    }
                    // AH头定位在外部IP头后面, skb缓冲中已经预留出AH头的数据部分了,
                    // 这是通过mode->output函数预留的, 通常调用type->output前要调用mode->oputput
                    ah = (struct ip_auth_hdr *)((char *)top_iph+top_iph->ihl*4);
                    // AH中的下一个头用原来的外部IP头中的协议
                    ah->nexthdr = top_iph->protocol;
                    // 将外部IP头的不进行认证计算的部分字段清零
                    top_iph->tos = 0;
                    top_iph->tot_len = htons(skb->len);
                    top_iph->frag_off = 0;
                    top_iph->ttl = 0;
                    // IP协议改为AH
                    top_iph->protocol = IPPROTO_AH;
                    top_iph->check = 0;
                    // AH数据处理结构
                    ahp = x->data;
                    // AH头长度对齐
                    ah->hdrlen  = (XFRM_ALIGN8(sizeof(struct ip_auth_hdr) +
                                               ahp->icv_trunc_len) >> 2) - 2;
                    // AH头参数赋值
                    ah->reserved = 0;
                    // SPI值
                    ah->spi = x->id.spi;
                    // 序列号
                    ah->seq_no = htonl(++x->replay.oseq);
                    // 通知防止重放***处理, 更新序列号
                    xfrm_aevent_doreplay(x);
                    // 对skb进行AH认证值的计算
                    err = ah_mac_digest(ahp, skb, ah->auth_data);
                    if (err)
                        goto error;
                    // 赋值初始化向量值到认证数据部分
                    memcpy(ah->auth_data, ahp->work_icv, ahp->icv_trunc_len);
                    // 恢复原来IP头的的不认证部分的值
                    top_iph->tos = iph->tos;
                    top_iph->ttl = iph->ttl;
                    top_iph->frag_off = iph->frag_off;
                    if (top_iph->ihl != 5)
                    {
                        top_iph->daddr = iph->daddr;
                        memcpy(top_iph+1, iph+1, top_iph->ihl*4 - sizeof(struct iphdr));
                    }
                    // 重新计算IP头的认证值
                    ip_send_check(top_iph);
                    err = 0;
                    error:
                        return err;
                }
    8.2 ESP
        8.2.1 初始化
            /* net/ipv4/esp4.c */
            static int __init esp4_init(void)
            {
                // 登记ESP协议的xfrm协议处理结构
                if (xfrm_register_type(&esp_type, AF_INET) < 0)
                {
                    printk(KERN_INFO "ip esp init: can't add xfrm type\n");
                    return -EAGAIN;
                }
                // 登记ESP协议到IP协议
                if (inet_add_protocol(&esp4_protocol, IPPROTO_ESP) < 0)
                {
                    printk(KERN_INFO "ip esp init: can't add protocol\n");
                    xfrm_unregister_type(&esp_type, AF_INET);
                    return -EAGAIN;
                }
                return 0;
            }
        8.2.2 IPV4下的ESP协议处理结构
            // ESP协议处理结构, 接收到IPV4包后, 系统根据IP头中的protocol
            // 字段选择相应的上层协议处理函数, 当IP协议号是50时, 数据包将
            // 调用该结构的handler处理函数:
            static struct net_protocol esp4_protocol =
            {
                .handler = xfrm4_rcv,
                .err_handler = esp4_err,
                .no_policy = 1,
            };
            ESP协议结构的handler函数也是xfrm4_rcv, 
            在net/ipv4/xfrm4_input.c 中定义,
            在上一篇中进行了介绍.
            // 错误处理, 收到ICMP错误包时的处理情况, 此时的skb包是ICMP包
            static void esp4_err(struct sk_buff *skb, u32 info)
            {
                // 应用层, data指向ICMP错误包里的内部IP头
                struct iphdr *iph = (struct iphdr*)skb->data;
                // ESP头
                struct ip_esp_hdr *esph = (struct ip_esp_hdr*)(skb->data+(iph->ihl<<2));
                struct xfrm_state *x;
                // ICMP错误类型检查, 本处理函数只处理"目的不可达"和"需要分片"两种错误
                if (skb->h.icmph->type != ICMP_DEST_UNREACH ||
                        skb->h.icmph->code != ICMP_FRAG_NEEDED)
                    return;
                // 重新查找SA
                x = xfrm_state_lookup((xfrm_address_t *)&iph->daddr, esph->spi, IPPROTO_ESP, AF_INET);
                if (!x)
                    return;
                NETDEBUG(KERN_DEBUG "pmtu discovery on SA ESP/%08x/%08x\n",
                         ntohl(esph->spi), ntohl(iph->daddr));
                xfrm_state_put(x);
            }
        8.2.3 ESP4协议的IPSEC处理结构
            static struct xfrm_type esp_type =
            {
                .description = "ESP4",
                .owner  = THIS_MODULE,
                .proto       = IPPROTO_ESP,
                // 状态初始化
                .init_state = esp_init_state,
                // 协议释放
                .destructor = esp_destroy,
                // 计算最大长度
                .get_max_size = esp4_get_max_size,
                // 协议输入
                .input  = esp_input,
                // 协议输出
                .output  = esp_output
            };
            8.2.3.1 状态初始化
                esp_data数据结构:
                /* include/net/esp.h */
                struct esp_data
                {
                    struct scatterlist  sgbuf[ESP_NUM_FAST_SG];
                    /* Confidentiality */
                    // 加密使用的相关数据
                    struct
                    {
                        // 密钥
                        u8   *key;  /* Key */
                        // 密钥长度
                        int   key_len; /* Key length */
                        // 填充长度
                        int   padlen;  /* 0..255 */
                        /* ivlen is offset from enc_data, where encrypted data start.
                        * It is logically different of crypto_tfm_alg_ivsize(tfm).
                        * We assume that it is either zero (no ivec), or
                        * >= crypto_tfm_alg_ivsize(tfm). */
                        // 初始化向量长度
                        int   ivlen;
                        // 初始化向量是否初始化标志
                        int   ivinitted;
                        // 初始化向量
                        u8   *ivec;  /* ivec buffer */
                        // 加密算法
                        struct crypto_blkcipher *tfm;  /* crypto handle */
                    } conf;
                    /* Integrity. It is active when icv_full_len != 0 */
                    // 认证使用的相关数据
                    struct
                    {
                        // 密钥
                        u8   *key;  /* Key */
                        // 密钥长度
                        int   key_len; /* Length of the key */
                        // 初始化向量
                        u8   *work_icv;
                        // 初始化向量全长
                        int   icv_full_len;
                        // 初始化向量截断长度
                        int   icv_trunc_len;
                        // 初始化向量更新函数, 好象没用
                        void   (*icv)(struct esp_data*,
                                      struct sk_buff *skb,
                                      int offset, int len, u8 *icv);
                        // HASH算法
                        struct crypto_hash *tfm;
                    } auth;
                };
                // ESP的esp_data数据结构初始化
                static int esp_init_state(struct xfrm_state *x)
                {
                    struct esp_data *esp = NULL;
                    struct crypto_blkcipher *tfm;
                    /* null auth and encryption can have zero length keys */
                    // 如果有认证算法, 密钥至少512, ESP的认证处理是可选的, 但在实际中都会使用认证
                    if (x->aalg)
                    {
                        if (x->aalg->alg_key_len > 512)
                            goto error;
                    }
                    // ESP加密算法是必须的
                    if (x->ealg == NULL)
                        goto error;
                    // 分配esp_data数据结构空间
                    esp = kzalloc(sizeof(*esp), GFP_KERNEL);
                    if (esp == NULL)
                        return -ENOMEM;
                    // 如果定义了认证算法, 初始化认证算法参数, 和AH类似
                    if (x->aalg)
                    {
                        struct xfrm_algo_desc *aalg_desc;
                        struct crypto_hash *hash;
                        // 认证密钥和长度设置
                        esp->auth.key = x->aalg->alg_key;
                        esp->auth.key_len = (x->aalg->alg_key_len+7)/8;
                        // 分配HASH算法的实现
                        hash = crypto_alloc_hash(x->aalg->alg_name, 0,
                                                 CRYPTO_ALG_ASYNC);
                        if (IS_ERR(hash))
                            goto error;
                        esp->auth.tfm = hash;
                        // 设置HASH算法密钥
                        if (crypto_hash_setkey(hash, esp->auth.key, esp->auth.key_len))
                            goto error;
                        // 找到算法描述
                        aalg_desc = xfrm_aalg_get_byname(x->aalg->alg_name, 0);
                        BUG_ON(!aalg_desc);
                        // 检查算法初始化向量长度合法性
                        if (aalg_desc->uinfo.auth.icv_fullbits/8 !=
                                crypto_hash_digestsize(hash))
                        {
                            NETDEBUG(KERN_INFO "ESP: %s digestsize %u != %hu\n",
                                     x->aalg->alg_name,
                                     crypto_hash_digestsize(hash),
                                     aalg_desc->uinfo.auth.icv_fullbits/8);
                            goto error;
                        }
                        // 初始化向量的全长和截断长度
                        esp->auth.icv_full_len = aalg_desc->uinfo.auth.icv_fullbits/8;
                        esp->auth.icv_trunc_len = aalg_desc->uinfo.auth.icv_truncbits/8;
                        // 分配全长度的初始化向量空间
                        esp->auth.work_icv = kmalloc(esp->auth.icv_full_len, GFP_KERNEL);
                        if (!esp->auth.work_icv)
                            goto error;
                    }
                    // 初始化加密算法相关参数, ESP使用的加密算法都是对称块加密算法, 不可能用非对称算法的
                    // 加密密钥
                    esp->conf.key = x->ealg->alg_key;
                    // 加密密钥长度
                    esp->conf.key_len = (x->ealg->alg_key_len+7)/8;
                    // 分配加密算法的具体实现结构
                    tfm = crypto_alloc_blkcipher(x->ealg->alg_name, 0, CRYPTO_ALG_ASYNC);
                    if (IS_ERR(tfm))
                        goto error;
                    esp->conf.tfm = tfm;
                    // 初始化向量大小
                    esp->conf.ivlen = crypto_blkcipher_ivsize(tfm);
                    // 填充数据长度初始化为0
                    esp->conf.padlen = 0;
                    // 初始化向量长度非0, 分配具体的初始化向量空间
                    if (esp->conf.ivlen)
                    {
                        esp->conf.ivec = kmalloc(esp->conf.ivlen, GFP_KERNEL);
                        if (unlikely(esp->conf.ivec == NULL))
                            goto error;
                        esp->conf.ivinitted = 0;
                    }
                    // 设置加密算法密钥
                    if (crypto_blkcipher_setkey(tfm, esp->conf.key, esp->conf.key_len))
                        goto error;
                    // 定义SA中ESP头部长度: ESP头加初始化向量长度
                    // 反映在ESP封装操作时要将数据包增加的长度
                    x->props.header_len = sizeof(struct ip_esp_hdr) + esp->conf.ivlen;
                    // 如果是通道模式, 还需要增加IP头长度
                    if (x->props.mode == XFRM_MODE_TUNNEL)
                        x->props.header_len += sizeof(struct iphdr);
                    // 如果要进行UDP封装
                    if (x->encap)
                    {
                        struct xfrm_encap_tmpl *encap = x->encap;
                        switch (encap->encap_type)
                        {
                        default:
                            goto error;
                        case UDP_ENCAP_ESPINUDP:
                            // 该类型封装增加UDP头长度
                            x->props.header_len += sizeof(struct udphdr);
                            break;
                        case UDP_ENCAP_ESPINUDP_NON_IKE:
                            // 该类型封装增加UDP头长度外加加8字节
                            x->props.header_len += sizeof(struct udphdr) + 2 * sizeof(u32);
                            break;
                        }
                    }
                    // 将esp_data作为SA的data指针
                    x->data = esp;
                    // 追踪长度, 最大增加长度和当前的计算的增加长度的差值,在路由时会用到
                    // 对于AH, 由于没有定义get_max_size(), 该值位0
                    x->props.trailer_len = esp4_get_max_size(x, 0) - x->props.header_len;
                    return 0;
                    error:
                        x->data = esp;
                        esp_destroy(x);
                        x->data = NULL;
                        return -EINVAL;
                }
            8.2.3.2 协议释放
                // 该函数被xfrm状态(SA)释放函数xfrm_state_gc_destroy()调用
                static void esp_destroy(struct xfrm_state *x)
                {
                    struct esp_data *esp = x->data;
                    if (!esp)
                        return;
                    // 释放加密算法
                    crypto_free_blkcipher(esp->conf.tfm);
                    esp->conf.tfm = NULL;
                    // 释放加密初始化向量
                    kfree(esp->conf.ivec);
                    esp->conf.ivec = NULL;
                    // 释放认证算法
                    crypto_free_hash(esp->auth.tfm);
                    esp->auth.tfm = NULL;
                    // 释放认证初始化向量
                    kfree(esp->auth.work_icv);
                    esp->auth.work_icv = NULL;
                    // 释放esp_data
                    kfree(esp);
                }
            8.2.3.3 计算最大长度
                // 在xfrm_state_mtu()函数中调用, 计算最大增加的数据长度
                // AH中没有该函数, 增加的长度使用x->props.header_len
                static u32 esp4_get_max_size(struct xfrm_state *x, int mtu)
                {
                    struct esp_data *esp = x->data;
                    // 加密块长度, 按4字节对齐
                    u32 blksize = ALIGN(crypto_blkcipher_blocksize(esp->conf.tfm), 4);
                    int enclen = 0;
                    switch (x->props.mode)
                    {
                    case XFRM_MODE_TUNNEL:
                        // 通道模式下的MTU, 按加密块大小对齐, +2是要包括2字节数据长度
                        mtu = ALIGN(mtu +2, blksize);
                        break;
                    default:
                    case XFRM_MODE_TRANSPORT:
                        /* The worst case */
                        // 传输模式下, MTU先按4字节对齐, 再加块长度减4
                        mtu = ALIGN(mtu + 2, 4) + blksize - 4;
                        break;
                    case XFRM_MODE_BEET:
                        /* The worst case. */
                        enclen = IPV4_BEET_PHMAXLEN;
                        mtu = ALIGN(mtu + enclen + 2, blksize);
                        break;
                    }
                    // 如果加密算法中定义了填充长度, MTU也要按填充长度对齐
                    if (esp->conf.padlen)
                        mtu = ALIGN(mtu, esp->conf.padlen);
                    // 返回MTU加提议中需要增加的头部长度和认证初始化向量的截断长度
                    // enclen只在BEET模式下非0, 在通道和传输模式下都是0
                    return mtu + x->props.header_len + esp->auth.icv_trunc_len - enclen;
                }
            8.2.3.4 协议输入
                struct scatterlist结构说明:
                /* include/asm-i386/scatterlist.h */
                struct scatterlist
                {
                    struct page  *page;
                    unsigned int offset;
                    dma_addr_t  dma_address;
                    unsigned int length;
                };
                /*
                * Note: detecting truncated vs. non-truncated authentication data is very
                * expensive, so we only support truncated data, which is the recommended
                * and common case.
                */
                // 接收数据处理, 在xfrm4_rcv_encap()函数中调用
                // 进行ESP认证解密, 剥离ESP头, 解密成普通数据包, 数据包长度减少
                // 输入的数据包是ESP包
                static int esp_input(struct xfrm_state *x, struct sk_buff *skb)
                {
                    struct iphdr *iph;
                    struct ip_esp_hdr *esph;
                    struct esp_data *esp = x->data;
                    struct crypto_blkcipher *tfm = esp->conf.tfm;
                    struct blkcipher_desc desc = { .tfm = tfm };
                    struct sk_buff *trailer;
                    int blksize = ALIGN(crypto_blkcipher_blocksize(tfm), 4);
                    // 认证初始化向量截断长度
                    int alen = esp->auth.icv_trunc_len;
                    // 需要加密的数据长度: 总长减ESP头, 加密初始化向量长度, 认证初始化向量长度
                    int elen = skb->len - sizeof(struct ip_esp_hdr) - esp->conf.ivlen - alen;
                    int nfrags;
                    int ihl;
                    u8 nexthdr[2];
                    struct scatterlist *sg;
                    int padlen;
                    int err;
                    // 在skb头留出ESP头的空间
                    if (!pskb_may_pull(skb, sizeof(struct ip_esp_hdr)))
                        goto out;
                    // 检查需要加密的数据长度, 必须大于0而且按块大小对齐的
                    if (elen <= 0 || (elen & (blksize-1)))
                        goto out;
                    /* If integrity check is required, do this. */
                    // 认证计算处理
                    if (esp->auth.icv_full_len)
                    {
                        u8 sum[alen];
                        // 计算认证值, 认证值保存在esp_data结构中
                        err = esp_mac_digest(esp, skb, 0, skb->len - alen);
                        if (err)
                            goto out;
                        // 将skb中的认证初始化向量部分数据拷贝到缓冲区sum中
                        if (skb_copy_bits(skb, skb->len - alen, sum, alen))
                            BUG();
                        // 比较sum中的向量值和认证算法结构中的向量值是否匹配, 数据包正常情况下应该是相同的
                        if (unlikely(memcmp(esp->auth.work_icv, sum, alen)))
                        {
                            x->stats.integrity_failed++;
                            goto out;
                        }
                    }
                    // 使数据包是可写的
                    if ((nfrags = skb_cow_data(skb, 0, &trailer)) < 0)
                        goto out;
                    skb->ip_summed = CHECKSUM_NONE;
                    // 定位在数据包中的ESP头位置, 为当前的data位置
                    esph = (struct ip_esp_hdr*)skb->data;
                    /* Get ivec. This can be wrong, check against another impls. */
                    // 设置加密算法的初始化向量
                    if (esp->conf.ivlen)
                        crypto_blkcipher_set_iv(tfm, esph->enc_data, esp->conf.ivlen);
                    sg = &esp->sgbuf[0];
                    if (unlikely(nfrags > ESP_NUM_FAST_SG))
                    {
                        sg = kmalloc(sizeof(struct scatterlist)*nfrags, GFP_ATOMIC);
                        if (!sg)
                            goto out;
                    }
                    skb_to_sgvec(skb, sg, sizeof(struct ip_esp_hdr) + esp->conf.ivlen, elen);
                    // 解密操作, 返回非0表示失败
                    err = crypto_blkcipher_decrypt(&desc, sg, sg, elen);
                    if (unlikely(sg != &esp->sgbuf[0]))
                        kfree(sg);
                    // 解密失败返回
                    if (unlikely(err))
                        return err;
                    // 拷贝两字节数据
                    if (skb_copy_bits(skb, skb->len-alen-2, nexthdr, 2))
                        BUG();
                    padlen = nexthdr[0];
                    if (padlen+2 >= elen)
                        goto out;
                    /* ... check padding bits here. Silly. :-) */
                    // 新的IP头
                    iph = skb->nh.iph;
                    ihl = iph->ihl * 4;
                    // 如果是NAT穿越情况, 进行一些处理
                    if (x->encap)
                    {
                        // xfrm封装模板
                        struct xfrm_encap_tmpl *encap = x->encap;
                        // 定位UDP数据头位置, 在IP头之后
                        struct udphdr *uh = (void *)(skb->nh.raw + ihl);
                        /*
                        * 1) if the NAT-T peer's IP or port changed then
                        *    advertize the change to the keying daemon.
                        *    This is an inbound SA, so just compare
                        *    SRC ports.
                        */
                        // 如果IP头源地址和SA提议中的源地址不同或源端口不同
                        if (iph->saddr != x->props.saddr.a4 ||
                                uh->source != encap->encap_sport)
                        {
                            xfrm_address_t ipaddr;
                            // 保存当前IP头源地址
                            ipaddr.a4 = iph->saddr;
                            // 进行NAT通知回调处理
                            km_new_mapping(x, &ipaddr, uh->source);
                            /* XXX: perhaps add an extra
                            * policy check here, to see
                            * if we should allow or
                            * reject a packet from a
                            * different source
                            * address/port.
                            */
                        }
                        /*
                        * 2) ignore UDP/TCP checksums in case
                        *    of NAT-T in Transport Mode, or
                        *    perform other post-processing fixes
                        *    as per draft-ietf-ipsec-udp-encaps-06,
                        *    section 3.1.2
                        */
                        // 如果是传输模式或BEET模式, 设置不需要计算校验和
                        if (x->props.mode == XFRM_MODE_TRANSPORT ||
                                x->props.mode == XFRM_MODE_BEET)
                            skb->ip_summed = CHECKSUM_UNNECESSARY;
                    }
                    // 新IP头中协议
                    iph->protocol = nexthdr[1];
                    // 缩减skb数据包长度
                    pskb_trim(skb, skb->len - alen - padlen - 2);
                    // 重新定位IP上层数据头位置
                    skb->h.raw = __skb_pull(skb, sizeof(*esph) + esp->conf.ivlen) - ihl;
                    return 0;
                    out:
                        return -EINVAL;
                }
            8.2.3.5 协议输出
                // 发送数据处理, 在xfrm4_output_one()中调用
                // 添加ESP头, 对数据包进行加密和认证处理, 数据包长度扩大
                // 在NAT穿越情况下会封装为UDP数据
                static int esp_output(struct xfrm_state *x, struct sk_buff *skb)
                {
                    int err;
                    struct iphdr *top_iph;
                    struct ip_esp_hdr *esph;
                    struct crypto_blkcipher *tfm;
                    struct blkcipher_desc desc;
                    struct esp_data *esp;
                    struct sk_buff *trailer;
                    int blksize;
                    int clen;
                    int alen;
                    int nfrags;
                    /* Strip IP+ESP header. */
                    // 缩减skb数据, 减去IP头和ESP头, 剩下的数据就是要进行加密和认证的部分
                    __skb_pull(skb, skb->h.raw - skb->data);
                    /* Now skb is pure payload to encrypt */
                    err = -ENOMEM;
                    /* Round to block size */
                    // 加密块的初始值
                    clen = skb->len;
                    // 获取SA的esp_data数据结构
                    esp = x->data;
                    // 认证初始化向量截断长度
                    alen = esp->auth.icv_trunc_len;
                    // 加密算法
                    tfm = esp->conf.tfm;
                    // 给块加密算法描述结构赋值
                    desc.tfm = tfm;
                    desc.flags = 0;
                    // 每个加密块大小
                    blksize = ALIGN(crypto_blkcipher_blocksize(tfm), 4);
                    // 对齐要加密的数据总长
                    clen = ALIGN(clen + 2, blksize);
                    // 如果要考虑填充, 继续对齐
                    if (esp->conf.padlen)
                        clen = ALIGN(clen, esp->conf.padlen);
                    // 使数据包可写
                    if ((nfrags = skb_cow_data(skb, clen-skb->len+alen, &trailer)) < 0)
                        goto error;
                    /* Fill padding... */
                    // 长度对齐后填充多余长度部分内容
                    do
                    {
                        int i;
                        for (i=0; i<clen-skb->len - 2; i++)
                            *(u8*)(trailer->tail + i) = i+1;
                    }
                    while (0);
                    // 最后两字节表示填充数据的长度
                    *(u8*)(trailer->tail + clen-skb->len - 2) = (clen - skb->len)-2;
                    pskb_put(skb, trailer, clen - skb->len);
                    // 在将IP头部分扩展回来
                    __skb_push(skb, skb->data - skb->nh.raw);
                    // 现在的IP头作为外部IP头
                    top_iph = skb->nh.iph;
                    // esp头跟在IP头后
                    esph = (struct ip_esp_hdr *)(skb->nh.raw + top_iph->ihl*4);
                    // 数据总长增加认证部分长度
                    top_iph->tot_len = htons(skb->len + alen);
                    *(u8*)(trailer->tail - 1) = top_iph->protocol;
                    /* this is non-NULL only with UDP Encapsulation */
                    if (x->encap)
                    {
                        // NAT穿越情况下要将数据封装为UDP包
                        struct xfrm_encap_tmpl *encap = x->encap;
                        struct udphdr *uh;
                        u32 *udpdata32;
                        // IP头后改为UDP头
                        uh = (struct udphdr *)esph;
                        // 填充UDP头参数, 源端口, 目的端口, UDP数据长度
                        uh->source = encap->encap_sport;
                        uh->dest = encap->encap_dport;
                        uh->len = htons(skb->len + alen - top_iph->ihl*4);
                        // 校验和为0, 表示不需要计算校验和, ESP本身就进行认证了
                        uh->check = 0;
                        switch (encap->encap_type)
                        {
                        default:
                        case UDP_ENCAP_ESPINUDP:
                            // 在该模式下ESP头跟在UDP头后面
                            esph = (struct ip_esp_hdr *)(uh + 1);
                            break;
                        case UDP_ENCAP_ESPINUDP_NON_IKE:
                            // 在该模式下ESP头跟在UDP头后面8字节处
                            udpdata32 = (u32 *)(uh + 1);
                            udpdata32[0] = udpdata32[1] = 0;
                            esph = (struct ip_esp_hdr *)(udpdata32 + 2);
                            break;
                        }
                        // 外部IP头协议是UDP
                        top_iph->protocol = IPPROTO_UDP;
                    }
                    else
                    // 非NAT穿越情况下, 外部IP头中的协议是ESP
                        top_iph->protocol = IPPROTO_ESP;
                    // 填充ESP头中的SPI和序列号
                    esph->spi = x->id.spi;
                    esph->seq_no = htonl(++x->replay.oseq);
                    // 序列号更新通知回调
                    xfrm_aevent_doreplay(x);
                    // 如果加密初始化向量长度非零, 设置加密算法中的初始化向量
                    if (esp->conf.ivlen)
                    {
                        if (unlikely(!esp->conf.ivinitted))
                        {
                            get_random_bytes(esp->conf.ivec, esp->conf.ivlen);
                            esp->conf.ivinitted = 1;
                        }
                        crypto_blkcipher_set_iv(tfm, esp->conf.ivec, esp->conf.ivlen);
                    }
                    // 加密操作
                    do
                    {
                        struct scatterlist *sg = &esp->sgbuf[0];
                        if (unlikely(nfrags > ESP_NUM_FAST_SG))
                        {
                            sg = kmalloc(sizeof(struct scatterlist)*nfrags, GFP_ATOMIC);
                            if (!sg)
                                goto error;
                        }
                        skb_to_sgvec(skb, sg, esph->enc_data+esp->conf.ivlen-skb->data, clen);
                        // 对数据加密
                        err = crypto_blkcipher_encrypt(&desc, sg, sg, clen);
                        if (unlikely(sg != &esp->sgbuf[0]))
                            kfree(sg);
                    }
                    while (0);
                    if (unlikely(err))
                        goto error;
                    // 将加密算法初始化向量拷贝到数据包
                    if (esp->conf.ivlen)
                    {
                        memcpy(esph->enc_data, esp->conf.ivec, esp->conf.ivlen);
                        crypto_blkcipher_get_iv(tfm, esp->conf.ivec, esp->conf.ivlen);
                    }
                    // 认证计算, 计算出HASH值并拷贝到数据包中
                    if (esp->auth.icv_full_len)
                    {
                        err = esp_mac_digest(esp, skb, (u8 *)esph - skb->data,
                                             sizeof(*esph) + esp->conf.ivlen + clen);
                        memcpy(pskb_put(skb, trailer, alen), esp->auth.work_icv, alen);
                    }
                    // 重新计算外部IP头校验和
                    ip_send_check(top_iph);
                    error:
                        return err;
                }
9. IPSEC封装流程
    IPSEC数据包的封装过程是在数据包发出前完成的, 是和路由选择密切相关的, 
    根据前面的发出分析可知封装是通过对数据设置安全路由链表来实现的, 
    因此对数据包的IPSEC封装流程可以简单描述如下:
    1) 对于进入的数据包, 进行路由选择, 如果是转发的, 进入路由输入, 
       然后查找安全策略检查是否需要IPSEC封装, 如果需要封装, 就查找和创建相关的安全路由, 
       进入路由输出处理, 在路由输出时即按照安全路由一层层地封装数据包最后得到IPSEC包发出;
    2) 对于自身发出的数据包, 需要进行路由选择, 选定路由后进入路由输入, 
       查找安全策略进行处理, 以后和转发的数据包IPSEC封装就是完全相同了。
    9.1 转发包的封装
        数据的转发入口点函数是ip_forward, 进入该函数的数据包还是普通数据包，数据包的路由也是普通路由：
        /* net/ipv4/ip_forward.c */
        int ip_forward(struct sk_buff *skb)
        {
            struct iphdr *iph; /* Our header */
            struct rtable *rt; /* Route we use */
            struct ip_options * opt = &(IPCB(skb)-<opt);
            // 对转发的数据包进行安全策略检查, 检查失败的话丢包
            if (!xfrm4_policy_check(NULL, XFRM_POLICY_FWD, skb))
                goto drop;
            if (IPCB(skb)-<opt.router_alert && ip_call_ra_chain(skb))
                return NET_RX_SUCCESS;
            // 转发包也是到自身的包, 不是的话丢包
            if (skb-<pkt_type != PACKET_HOST)
                goto drop;
            skb-<ip_summed = CHECKSUM_NONE;
            /*
             * According to the RFC, we must first decrease the TTL field. If
             * that reaches zero, we must reply an ICMP control message telling
             * that the packet's lifetime expired.
             */
            // TTL到头了, 丢包
            if (skb->nh.iph->ttl <= 1)              
                goto too_many_hops;
            // 进入安全路由选路和转发处理, 在此函数中构造数据包的安全路由
            if (!xfrm4_route_forward(skb))
                goto drop;
            // 以下是一些常规的路由和TTL处理
            rt = (struct rtable*)skb-<dst;
            if (opt-<is_strictroute && rt-<rt_dst != rt-<rt_gateway)
                goto sr_failed;
            /* We are about to mangle packet. Copy it! */
            if (skb_cow(skb, LL_RESERVED_SPACE(rt-<u.dst.dev)+rt-<u.dst.header_len))
                goto drop;
            iph = skb-<nh.iph;
            /* Decrease ttl after skb cow done */
            ip_decrease_ttl(iph);
            /*
             * We now generate an ICMP HOST REDIRECT giving the route
             * we calculated.
             */
            if (rt-<rt_flags&RTCF_DOREDIRECT && !opt-<srr)
                ip_rt_send_redirect(skb);
                skb-<priority = rt_tos2priority(iph-<tos);
                // 进行FORWARD点过滤, 过滤后进入ip_forward_finish函数
                return NF_HOOK(PF_INET, NF_IP_FORWARD, skb, skb-<dev, 
                               rt-<u.dst.dev,  ip_forward_finish);
            sr_failed:
                /*
                   * Strict routing permits no gatewaying
                   */
                icmp_send(skb, ICMP_DEST_UNREACH, ICMP_SR_FAILED, 0);
                goto drop;
            too_many_hops:
                /* Tell the sender its packet died... */
                IP_INC_STATS_BH(IPSTATS_MIB_INHDRERRORS);
                icmp_send(skb, ICMP_TIME_EXCEEDED, ICMP_EXC_TTL, 0);
            drop:
                kfree_skb(skb);
                return NET_RX_DROP;
        }
        // ip_forward_finish函数主要就是调用dst_output函数
        static inline int ip_forward_finish(struct sk_buff *skb)
        {
            struct ip_options * opt = &(IPCB(skb)-<opt);
            IP_INC_STATS_BH(IPSTATS_MIB_OUTFORWDATAGRAMS);
            if (unlikely(opt-<optlen))
                ip_forward_options(skb);
            return dst_output(skb);
        }
        核心函数是xfrm4_route_forward函数
        /* include/net/xfrm.h */
        static inline int xfrm4_route_forward(struct sk_buff *skb)
        {
            return xfrm_route_forward(skb, AF_INET);
        }
        static inline int xfrm_route_forward(struct sk_buff *skb, unsigned short family)
        {
            // 如果没有发出方向的安全策略的话返回
            return !xfrm_policy_count[XFRM_POLICY_OUT] ||
                   // 如果路由标志专门设置不进行IPSEC封装的话也返回
                   (skb-<dst-<flags & DST_NOXFRM) ||
                   __xfrm_route_forward(skb, family);
        }
        /* net/xfrm/xfrm_policy.c */
        int __xfrm_route_forward(struct sk_buff *skb, unsigned short family)
        {
            struct flowi fl;
            // 路由解码, 填充流结构参数,
            // 对IPV4实际调用的是_decode_session4(net/ipv4/xfrm4_policy.c)函数
            if (xfrm_decode_session(skb, &fl, family) < 0 br style='font-size:12px;font-style:normal;font-weight:400;color:#666;' />  return 0;
                    // 根据流结构查找安全路由, 没找到的话创建新的安全路由, 最后形成安全路由链表
                    // 见前几节中的分析
                    return xfrm_lookup(&skb-<dst, &fl, NULL, 0) == 0;
        }
        
        因此数据进行转发处理后, 最终进入dst_output函数处理
        转发函数流程小结:
        ip_forward
          -> xfrm4_route_forward (net/xfrm.h, get xfrm_dst)
            -> xfrm_route_forward
              -> __xfrm_route_forward
                -> xfrm_lookup
                  -> xfrm_find_bundle
                    -> afinfo->find_bundle == __xfrm4_find_bundle
                  -> xfrm_bundle_create
                    -> afinfo->bundle_create == __xfrm4_bundle_create
                      tunnel mode
                      -> xfrm_dst_lookup
                        -> afinfo->dst_lookup == xfrm4_dst_lookup
                          -> __ip_route_output_key
                  -> dst_list: dst->list=policy_bundles, policy->bundles = dst
          -> NF_HOOK(NF_FORWARD)
          -> ip_forward_finish
          -> dst_output
    9.2 自身数据发出
        对于IPv4包的发出, 通常出口函数是ip_queue_xmit或ip_push_pending_frames, 
        如果是后者, 数据包是已经经过了路由选择的, 而前者还没有进行路由选择, 
        两者最后都会调用dst_output()函数进行数据的发出.
        /* net/ipv4/ip_output.c */
        int ip_queue_xmit(struct sk_buff *skb, int ipfragok)
        {
            struct sock *sk = skb-<sk;
            struct inet_sock *inet = inet_sk(sk);
            struct ip_options *opt = inet-<opt;
            struct rtable *rt;
            struct iphdr *iph;
            /* Skip all of this if the packet is already routed,
             * f.e. by something like SCTP.
             */
            // 已经路由过的数据跳过路由查找过程
            rt = (struct rtable *) skb-<dst;
            if (rt != NULL)
                goto packet_routed;
            /* Make sure we can route this packet. */
            rt = (struct rtable *)__sk_dst_check(sk, 0);
            if (rt == NULL)
            {
                __be32 daddr;
                /* Use correct destination address if we have options. */
                daddr = inet-<daddr;
                if(opt && opt-<srr)
                    daddr = opt-<faddr;
                {
                    struct flowi fl = { .oif = sk-<sk_bound_dev_if,
                        .nl_u = { .ip4_u =
                        {
                            .daddr = daddr,
                            .saddr = inet-<saddr,
                            .tos = RT_CONN_FLAGS(sk)
                        }
                                },
                                .proto = sk-<sk_protocol,
                                 .uli_u = { .ports =
                        {
                            .sport = inet-<sport,
                            .dport = inet-<dport
                        }
                                          }
                                      };
                    /* If this fails, retransmit mechanism of transport layer will
                     * keep trying until route appears or the connection times
                     * itself out.
                     */
                    security_sk_classify_flow(sk, &fl);
                    if (ip_route_output_flow(&rt, &fl, sk, 0))
                        goto no_route;
                }
                sk_setup_caps(sk, &rt-<u.dst);
            }
            skb-<dst = dst_clone(&rt-<u.dst);
            packet_routed:
                if (opt && opt-<is_strictroute && rt-<rt_dst != rt-<rt_gateway)
                    goto no_route;
                /* OK, we know where to send it, allocate and build IP header. */
                iph = (struct iphdr *) skb_push(skb, sizeof(struct iphdr) + (opt ? opt-<optlen : 0));
                *((__u16 *)iph) = htons((4 < inet->tos & 0xff));
                iph-<tot_len = htons(skb-<len);
                if (ip_dont_fragment(sk, &rt-<u.dst) && !ipfragok)
                    iph-<frag_off = htons(IP_DF);
                else
                    iph-<frag_off = 0;
                iph-<ttl      = ip_select_ttl(inet, &rt-<u.dst);
                iph-<protocol = sk-<sk_protocol;
                iph-<saddr    = rt-<rt_src;
                iph-<daddr    = rt-<rt_dst;
                skb-<nh.iph   = iph;
                /* Transport layer set skb-<h.foo itself. */
                if (opt && opt-<optlen)
                {
                    iph-<ihl += opt-<optlen << 2;
                    ip_options_build(skb, opt, inet-<daddr, rt, 0);
                }
                ip_select_ident_more(iph, &rt-<u.dst, sk,
                                     (skb_shinfo(skb)-<gso_segs ?: 1) - 1);
                /* Add an IP checksum. */
                ip_send_check(iph);
                skb-<priority = sk-<sk_priority;
                // 进入OUTPUT点进行过滤, 过滤完成后进入dst_output()函数
                return NF_HOOK(PF_INET, NF_IP_LOCAL_OUT, skb, NULL, rt-<u.dst.dev,
                               dst_output);
            no_route:
                IP_INC_STATS(IPSTATS_MIB_OUTNOROUTES);
                kfree_skb(skb);
                return -EHOSTUNREACH;
        }
        // 路由查找函数
        int ip_route_output_flow(struct rtable **rp, struct flowi *flp, struct sock *sk, int flags)
        {
            int err;
            // 普通的路由查找过程, 此过程不是本文重点, 分析略
            if ((err = __ip_route_output_key(rp, flp)) != 0)
                return err;
            // 如果流结构协议非0(基本是肯定的)进行xfrm路由查找
            if (flp-<proto)
            {
                // 指定流结构的源地址和目的地址
                if (!flp-<fl4_src)
                    flp-<fl4_src = (*rp)-<rt_src;
                if (!flp-<fl4_dst)
                    flp-<fl4_dst = (*rp)-<rt_dst;
                // 根据流结构查找安全路由, 没找到的话创建新的安全路由, 最后形成安全路由链表
                // 见前几节中的分析
                return xfrm_lookup((struct dst_entry **)rp, flp, sk, flags);
            }
            return 0;
        }
        对于不是进入ip_queue_xmit()发送的数据包, 
        在发送前必然也是经过ip_route_output_flow()函数的路由选择处理, 
        因此如果需要IPSEC封装的话, 也就设置了相关的安全路由链表.
        这样, 对于自身发出的数据包, 最终也是进入dst_output()函数进行发送, 
        转发和自身发出的数据殊途同归了, 以后的处理过程就都是相同的了
        函数流程小结:
        ip_queue_xmit
          -> ip_route_output_flow
            -> xfrm_lookup
              -> xfrm_find_bundle
                -> bundle_create
                  -> afinfo->bundle_create == __xfrm4_bundle_create
                    -> xfrm_dst_lookup
                      -> afinfo->dst_lookup == xfrm4_dst_lookup
                        -> __ip_route_output_key
                -> dst_list
                -> dst->list=policy_bundles, policy->bundles = dst
          -> NF_HOOK(NF_OUTPUT)
          -> dst_output
            -> dst->output
    9.3 dst_output
        /* include/net/dst.h */
        /* Output packet to network from transport.  */
        static inline int dst_output(struct sk_buff *skb)
        {
            return skb-<dst-<output(skb);
        }
        dst_output()函数就是调用路由项的输出函数, 对于安全路由, 
        该函数是xfrm4_output()函数, 对于普通路由, 是ip_output()函数
        对于xfrm4_output()函数的分析见7.6, 执行完所有安全路由的输出函数, 
        每执行一个安全路由输出函数就是一次IPSEC封装处理过程, 
        封装结束后的数据包会设置IPSKB_REROUTED标志, 到路由链表的最后一项是普通路由, 
        进入普通路由的输出函数ip_output:
        int ip_output(struct sk_buff *skb)
        {
            struct net_device *dev = skb-<dst-<dev;
            IP_INC_STATS(IPSTATS_MIB_OUTREQUESTS);
            skb-<dev = dev;
            skb-<protocol = htons(ETH_P_IP);
        // 如果是带IPSKB_REROUTED标志的数据包, 不进入POSTROUTING的SNAT处理, 直接执行
        // ip_finish_output函数
            return NF_HOOK_COND(PF_INET, NF_IP_POST_ROUTING, skb, NULL, dev,
                                ip_finish_output,
                                !(IPCB(skb)-<flags & IPSKB_REROUTED));
        }
        因此对于封装的数据包而言, 在封装过程中可以进行OUTPUT点的过滤和POSTROUTING点的SNAT处理, 
        但一旦封装完成, 就不会再进行SNAT操作了.
    函数调用小结:
        xfrm_lookup: find xfrm_dst for the skb, create dst_list
          -> xfrm_sk_policy_lookup
          -> flow_cache_lookup
          -> xfrm_find_bundle
          -> xfrm_policy_lookup_bytype
          -> xfrm_tmpl_resolve
            -> xfrm_tmpl_resolve_one
              -> xfrm_get_saddr
                -> afinfo->get_saddr == xfrm4_get_saddr
                  -> xfrm4_dst_lookup
              -> xfrm_state_find
                -> __xfrm_state_lookup
                -> xfrm_state_alloc
                -> km_query
                  -> km->acquire (pfkey_acquire, xfrm_send_acquire)
            -> xfrm_state_sort
              -> afinfo->state_sort == NULL
          -> km_wait_queue
          -> xfrm_bundle_create
         
        dst_output: loop dst_list
          -> dst->output == xfrm4_output 
            -> NF_HOOK(POSTROUTING)
              -> xfrm4_output_finish
                -> gso ?
                -> xfrm4_output_finish2
                  -> xfrm4_output_one
                    -> mode->output
                    -> type->output
                    -> skb->dst=dst_pop(skb->dst)
                  -> nf_hook(NF_OUTPUT)
                    -> !dst->xfrm
                      -> dst_output
                  -> nf_hook(POSTROUTING)
          -> dst->output == ip_output
            -> NF_HOOK(POSTROUTING)
              -> ip_finish_output
                -> ip_finish_output2
                  -> hh_output == dev_queue_xmit
10. 总结
    Linux自带的native ipsec实现xfrm是通过路由来实现IPSEC封装处理的, 这和freeswan是类似的, 
    只不过freeswan构造了虚拟的ipsec*网卡设备, 
    这样就可以通过标准的网络工具如iproute2等通过配置路由和ip rule等实现安全策略, 
    进入该虚拟网卡的数据包就进行IPSEC解封, 从虚拟网卡发出的包就是进行IPSEC封装，
    因此实现比较独立，除了NAT-T需要修改udp.c源码外，其他基本不需要修改内核源码，
    对于进入的IPSEC包在物理网卡上可以抓到原始的IPSEC包，
    而从虚拟网卡上可以抓到解密后的数据包。
    而xfrm没有定义虚拟网卡，都是在路由查找过程中自动查找安全策略实现ipsec的解封或封装，
    因此该实现是必须和内核网络代码耦合在一起的，
    对于进入的IPSEC包，能在物理网卡抓到两次包，一次是IPSEC原始包，一次是解密后的包。
    由于还是需要根据路由来进行封装，所以本质还不是基于策略的IPSEC，
    不过可以通过定义策略路由方式来实现基于策略IPSEC，
    要是能把IPSEC封装作为一个netfilter的target就好了，
    这样就可以进行标准的基于策略的IPSEC了。
    xfrm和网络代码耦合，这样进行路由或netfilter过滤时都可以通过相关标志进行处理或旁路，
    如经过IPSEC处理后的数据包是自动不会进行SNAT操作的，而freeswan的实现就不能保证，
    如果设置SNAT规则不对，是有可能对封装好的包进行SNAT操作而造成错误。
    但两个实现对于封装前的数据包都是可以进行SNAT操作的，
    因此那种实现同网段VPN的特殊NAT可以在xfrm下实现。
    在RFC2367中只定义了SA相关操作的消息类型，而没有定义SP的操作类型，
    也没有定义其他扩展的IPSEC功能的相关消息类型，如NAT-T相关的类型，
    那些SADB_X_*的消息类型就是非标准的，
    这就造成各种IPSEC实现只能自己定义这些消息类型，
    因此可能会造成不兼容的现象，应该尽快出新的RFC来更新2367了。