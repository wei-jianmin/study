https://blog.csdn.net/it_hue/category_7462826.html
1. ǰ��
    ��Linux2.6�ں����Դ���IPSEC��ʵ��,�����Ͳ�����2.4�����򲹶���ʵ����
    ��ʵ�ְ������¼�������:
        PF_KEY�����׽ӿ�, �����ṩ���û���ռ����PF_KEYͨ�ţ�������net/keyĿ¼�£�
        ��ע������������netlinkͨ�ŷ�ʽ��
        ��ȫ����SA�Ͱ�ȫ����SP������ʹ��xfrm����ʵ�ֵģ�������net/xfrm/Ŀ¼�¶���
        ESP��AH��Э��ʵ�֣���net/ipv4(6)�¶���
        ������֤�㷨�⣬��cryptoĿ¼�¶��壬��Щ�㷨���Ǳ�׼������
    ��ϵ��������Ҫ����XFRM���ʵ���Լ���IPV4�����Э��Ĵ�����, IPV6�ĺ��ԡ�
    3 �����ݽṹ��
        ����(xfrm policy)
        ģ��(template)
        ״̬(xfrm state)
    ����Linux�ں˴���汾Ϊ2.6.19.2
    xfrm���ں��б仯�Ƚϴ�Ĳ���,ÿ���汾�ж��в�С�Ĳ���, ͬʱҲ˵���˸�ģ��Ĳ�������
    ��net/xfrmĿ¼�µĸ��ļ����¹���˵������
        xfrm_state.c    : xfrm״̬����
        xfrm_policy.c   : xfrm���Թ���
        xfrm_algo.c     : �㷨����
        xfrm_hash.c     : HASH���㺯��
        xfrm_input.c    : ��ȫ·��(sec_path)����,���ڽ����ipsec��
        xfrm_user.c     :  netlink�ӿڵ�SA��SP����
    ��net/ipv4Ŀ¼�µĺ�ipsec��ظ��ļ����¹���˵������:
        ah4.c               : IPV4��AHЭ�鴦��
        esp4.c              : IPV4��ESPЭ�鴦��
        ipcomp.c            : IPѹ��Э�鴦��
        xfrm4_input         : ���յ�IPV4��IPSEC������
        xfrm4_output        : ������IPV4��IPSEC������
        xfrm4_state         : IPV4��SA����
        xfrm4_policy        : IPV4�Ĳ��Դ���
        xfrm4_tunnel        : IPV4��ͨ������
        xfrm4_mode_transport: ����ģʽ
        xfrm4_mode_tunnel   : ͨ��ģʽ
        xfrm4_mode_beet     : BEETģʽ
2. ���ݽṹ
    �ں�SA�Ķ�����xfrm_state�ṹ���壬SP��xfrm_policy�ṹ���壬
    ��include/net/xfrm.h�ж���
    2.1 ״̬(SA)
        xfrm_state״̬�ṹ��������SA���ں��еľ���ʵ��:
        struct xfrm_state
        {
            /* Note: bydst is re-used during gc */
            // ÿ��״̬�ṹ�ҽӵ�����HASH������
            struct hlist_node bydst; // ��Ŀ�ĵ�ַHASH
            struct hlist_node bysrc; // ��Դ��ַHASH
            struct hlist_node byspi; // ��SPIֵHASH
            atomic_t  refcnt; // ����ʹ�ü���
            spinlock_t  lock;   // ״̬��
            struct xfrm_id  id; // ID�ṹ�� ��Ŀ�ĵ�ַ��SPI��Э����Ԫ��
            struct xfrm_selector sel; // ״̬ѡ����
            u32   genid; // ״̬�ı�־ֵ, ��ֹ������ײ
            /* Key manger bits */
            struct {
                u8  state;
                u8  dying;
                u32  seq;
            } km;  // KEY�ص�������ṹ����
            /* Parameters of this state. */
            struct {
                u32  reqid; // ����ID
                u8  mode;  // ģʽ: ����/ͨ��
                u8  replay_window; // �طŴ���
                u8  aalgo, ealgo, calgo; // ��֤,����,ѹ���㷨IDֵ
                u8  flags; // һЩ��׼
                u16  family; // Э����
                xfrm_address_t saddr;  // Դ��ַ
                int  header_len;  // ��ӵ�Э��ͷ����
                int  trailer_len; //
            } props; // SA��ز����ṹ
            struct xfrm_lifetime_cfg lft; // ����ʱ������
            /* Data for transformer */
            struct xfrm_algo *aalg; // hash�㷨
            struct xfrm_algo *ealg; // �����㷨
            struct xfrm_algo *calg; // ѹ���㷨
            /* Data for encapsulator */
            struct xfrm_encap_tmpl *encap; // NAT-T��װ��Ϣ
            /* Data for care-of address */
            xfrm_address_t *coaddr;
            /* IPComp needs an IPIP tunnel for handling uncompressed packets */
            struct xfrm_state *tunnel;  // ͨ��, ʵ������һ��SA
            /* If a tunnel, number of users + 1 */
            atomic_t  tunnel_users; // ͨ����ʹ����
            /* State for replay detection */
            struct xfrm_replay_state replay; // �طż��ṹ,�����������к��������Ϣ
            /* Replay detection state at the time we sent the last notification */
            struct xfrm_replay_state preplay; // �ϴεĻطż�¼ֵ
            /* internal flag that only holds state for delayed aevent at the moment */
            u32   xflags; // ��־
            /* Replay detection notification settings */
            u32   replay_maxage; // �ط����ʱ����
            u32   replay_maxdiff; // �ط�����ֵ
            /* Replay detection notification timer */
            struct timer_list rtimer; // �طż�ⶨʱ��
            /* Statistics */
            struct xfrm_stats stats; // ͳ��ֵ
            struct xfrm_lifetime_cur curlft; // ��ǰʱ�������
            struct timer_list timer;  // SA��ʱ��
            /* Last used time */
            u64   lastused; // �ϴ�ʹ��ʱ��
            /* Reference to data common to all the instances of this transformer */
            struct xfrm_type *type;  // Э��, ESP/AH/IPCOMP
            struct xfrm_mode *mode;  // ģʽ, ͨ������
            /* Security context */
            struct xfrm_sec_ctx *security; // ��ȫ������, ����ʱʹ��
            /* Private data of this transformer, format is opaque,
            * interpreted by xfrm_type methods. */
            void   *data; // �ڲ�����
        };
    2.2 ��ȫ����(SP)
        xfrm_policy�ṹ��������SP���ں��ڲ��ľ���ʵ��:
        struct xfrm_policy
        {
            struct xfrm_policy *next; // ��һ������
            struct hlist_node bydst; // ��Ŀ�ĵ�ַHASH������
            struct hlist_node byidx; // ��������HASH������
            /* This lock only affects elements except for entry. */
            rwlock_t  lock;  // ���Խṹ��
            atomic_t  refcnt; // ���ô���
            struct timer_list timer; // ���Զ�ʱ��
            u8   type;     // ����
            u32   priority; // �������ȼ�
            u32   index;    // ����������
            struct xfrm_selector selector; // ѡ����
            struct xfrm_lifetime_cfg lft;     // ����������
            struct xfrm_lifetime_cur curlft;  // ��ǰ������������
            struct dst_entry       *bundles;  // ·������
            __u16   family;   // Э����
            __u8   action;   // ���Զ���, ����/����/����...
            __u8   flags;    // ��־
            __u8   dead;     // ����������־
            __u8   xfrm_nr;  // ʹ�õ�xfrm_vec������
            struct xfrm_sec_ctx *security; // ��ȫ������
            struct xfrm_tmpl        xfrm_vec[XFRM_MAX_DEPTH]; // ״̬ģ��
        };
        xfrmģ��ṹ, ����״̬�Ͳ��ԵĲ�ѯ:
        struct xfrm_tmpl
        {
            /* id in template is interpreted as:
            * daddr - destination of tunnel, may be zero for transport mode.
            * spi   - zero to acquire spi. Not zero if spi is static, then
            *    daddr must be fixed too.
            * proto - AH/ESP/IPCOMP
            */
            // SA��Ԫ��, Ŀ�ĵ�ַ, Э��, SOI
            struct xfrm_id  id;
            /* Source address of tunnel. Ignored, if it is not a tunnel. */
            // Դ��ַ
            xfrm_address_t  saddr;
            // ����ID
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
    2.3 Э��ṹ
        ��ESP, AH, IPCOMP��Э���������ͨ��xfrm_type�ṹ��������, 
        ���Э��ķ�װ���ǿ����Э��ṹ�γɵ�������ʵ��:
        struct xfrm_type
        {
            char   *description; // �����ַ���
            struct module  *owner; // Э��ģ��
            __u8   proto;  // Э��ֵ
            __u8   flags;  // ��־
            #define XFRM_TYPE_NON_FRAGMENT 1
            // ��ʼ��״̬
            int   (*init_state)(struct xfrm_state *x);
            // ��������
            void   (*destructor)(struct xfrm_state *);
            // �������뺯��
            int   (*input)(struct xfrm_state *, struct sk_buff *skb);
            // �����������
            int   (*output)(struct xfrm_state *, struct sk_buff *pskb);
            // �ܾ�����
            int   (*reject)(struct xfrm_state *, struct sk_buff *, struct flowi *);
            // ͷ��ƫ��
            int   (*hdr_offset)(struct xfrm_state *, struct sk_buff *, u8 **);
            // ���ص�ַ
            xfrm_address_t  *(*local_addr)(struct xfrm_state *, xfrm_address_t *);
            // Զ�̵�ַ
            xfrm_address_t  *(*remote_addr)(struct xfrm_state *, xfrm_address_t *);
            /* Estimate maximal size of result of transformation of a dgram */
            // ������ݱ�����
            u32   (*get_max_size)(struct xfrm_state *, int size);
        };
        �����Э��ṹ��������, ͨ��ֻ�����ʼ��,����,���������ĸ���Ա����:
        AHЭ�鶨��
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
        ESPЭ�鶨��:
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
        IPѹ��Э�鶨��:
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
        IPIPЭ�鶨��:
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
    2.4 ģʽ�ṹ
        ģʽ�ṹ��������IPSEC��������, ��Ϊͨ��ģʽ����ģʽ����:
        struct xfrm_mode {
            // �������뺯��
            int (*input)(struct xfrm_state *x, struct sk_buff *skb);
            // �����������
            int (*output)(struct xfrm_state *x,struct sk_buff *skb);
            // ģ��ָ��
            struct module *owner;
            // ��װ
            unsigned int encap;
        };
        ͨ��ģʽ�ṹ����:
            /* net/ipv4/xfrm4_mode_tunnel.c */
            static struct xfrm_mode xfrm4_tunnel_mode = {
                .input = xfrm4_tunnel_input,
                .output = xfrm4_tunnel_output,
                .owner = THIS_MODULE,
                .encap = XFRM_MODE_TUNNEL,
            };
        ����ģʽ�ṹ����:
            /* net/ipv4/xfrm4_mode_transport.c */
            static struct xfrm_mode xfrm4_transport_mode = {
                .input = xfrm4_transport_input,
                .output = xfrm4_transport_output,
                .owner = THIS_MODULE,
                .encap = XFRM_MODE_TRANSPORT,
            };
        beetģʽ, ��֪��������
            /* net/ipv4/xfrm4_mode_beet.c */
            static struct xfrm_mode xfrm4_beet_mode = {
                .input = xfrm4_beet_input,
                .output = xfrm4_beet_output,
                .owner = THIS_MODULE,
                .encap = XFRM_MODE_BEET,
            };
    2.5 ���Ե����Э�鴦��ṹ
        ���½ṹ������������Э�����µĵĲ��Դ���:
        struct xfrm_policy_afinfo {
            // Э����
            unsigned short  family;
            // Э������
            struct xfrm_type *type_map[IPPROTO_MAX];
            // ģʽ
            struct xfrm_mode *mode_map[XFRM_MODE_MAX];
            // Ŀ�Ĳ����ṹ
            struct dst_ops  *dst_ops;
            // �����Ѽ�
            void   (*garbage_collect)(void);
            // ·��ѡ��
            int   (*dst_lookup)(struct xfrm_dst **dst, struct flowi *fl);
            // ��ȡԴ��ַ
            int   (*get_saddr)(xfrm_address_t *saddr, xfrm_address_t *daddr);
            // ����·����
            struct dst_entry *(*find_bundle)(struct flowi *fl, struct xfrm_policy *policy);
            // ������·����
            int   (*bundle_create)(struct xfrm_policy *policy, 
            struct xfrm_state **xfrm, 
            int nx,
            struct flowi *fl, 
            struct dst_entry **dst_p);
            // ����Ự
            void   (*decode_session)(struct sk_buff *skb,
            struct flowi *fl);
        };
        IPV4�Ĳ���Э����ش���ṹ��������:
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
    2.6 ״̬�����Э�鴦��ṹ
        ���½ṹ������������Э�����µĵ�״̬����:
        struct xfrm_state_afinfo {
            // Э����
            unsigned short  family;
            // ��ʼ����־
            int   (*init_flags)(struct xfrm_state *x);
            // ��ʼ��ģ��ѡ��
            void   (*init_tempsel)(struct xfrm_state *x, struct flowi *fl,
            struct xfrm_tmpl *tmpl,
            xfrm_address_t *daddr, xfrm_address_t *saddr);
            // ģ������
            int   (*tmpl_sort)(struct xfrm_tmpl **dst, struct xfrm_tmpl **src, int n);
            // ״̬����
            int   (*state_sort)(struct xfrm_state **dst, struct xfrm_state **src, int n);
        };
        IPV4��״̬���Э�鴦��ṹ
        /* net/ipv4/xfrm4_state.c */
        static struct xfrm_state_afinfo xfrm4_state_afinfo = {
            .family   = AF_INET,
            .init_flags  = xfrm4_init_flags,
            .init_tempsel  = __xfrm4_init_tempsel,
        };
    2.7 �ص�֪ͨ��Ϣ�ṹ
        struct xfrm_mgr
        {
            struct list_head list;
            char   *id;
            // ״̬֪ͨ
            int   (*notify)(struct xfrm_state *x, struct km_event *c);
            // ��ȡ, ���ȡSA
            int   (*acquire)(struct xfrm_state *x, struct xfrm_tmpl *, struct xfrm_policy *xp, int dir);
            // �������
            struct xfrm_policy *(*compile_policy)(struct sock *sk, int opt, u8 *data, int len, int *dir);
            // ӳ��
            int   (*new_mapping)(struct xfrm_state *x, xfrm_address_t *ipaddr, u16 sport);
            // ����֪ͨ
            int   (*notify_policy)(struct xfrm_policy *x, int dir, struct km_event *c);
            // ����
            int   (*report)(u8 proto, struct xfrm_selector *sel, xfrm_address_t *addr);
        };
        ��net/key/pf_key.c�ж�����pkeyv2_mgr�ṹ:
        static struct xfrm_mgr pfkeyv2_mgr =
        {
            .id  = "pfkeyv2",
            .notify  = pfkey_send_notify,
            .acquire = pfkey_send_acquire,
            .compile_policy = pfkey_compile_policy,
            .new_mapping = pfkey_send_new_mapping,
            .notify_policy = pfkey_send_policy_notify,
        };
3. ��ʼ��
    xfrm��ʼ����������״̬, ���Ժ����봦�������ʼ������
        /* net/xfrm/xfrm_policy.c */
        // xfrm�ǲ�֧��ģ�鷽ʽ��
        void __init xfrm_init(void)
        {
            xfrm_state_init();
            xfrm_policy_init();
            xfrm_input_init();
        }
    3.1 xfrm״̬��ʼ��
        /* net/xfrm/xfrm_state.c */
        void __init xfrm_state_init(void)
        {
            unsigned int sz;
            // ��ʼHASH����, ÿ��HASH�г�ʼ��Ϊ8������, ������״̬����������
            // �ᶯ̬����HASH������
            sz = sizeof(struct hlist_head) * 8;
            // ����3��HASH, �ֱ�SA��Դ��ַ, Ŀ�ĵ�ַ��SPIֵ
            xfrm_state_bydst = xfrm_hash_alloc(sz);
            xfrm_state_bysrc = xfrm_hash_alloc(sz);
            xfrm_state_byspi = xfrm_hash_alloc(sz);
            if (!xfrm_state_bydst || !xfrm_state_bysrc || !xfrm_state_byspi)
                panic("XFRM: Cannot allocate bydst/bysrc/byspi hashes.");
            // xfrm_state_hmask��ʼֵΪ=7, �������HASHֵ���ֵ�����õ������
            xfrm_state_hmask = ((sz / sizeof(struct hlist_head)) - 1);
            // ��ʼ����������work_queue, ��ɶ�״̬�������Ѽ����ͷ�
            INIT_WORK(&xfrm_state_gc_work, xfrm_state_gc_task, NULL);
        }
    3.2 ���Գ�ʼ��
        static void __init xfrm_policy_init(void)
        {
            unsigned int hmask, sz;
            int dir;
            // ����һ���ں�cache, ���ڷ���xfrm_dst�ṹ()
            xfrm_dst_cache = kmem_cache_create("xfrm_dst_cache",
                                                sizeof(struct xfrm_dst),
                                                0, SLAB_HWCACHE_ALIGN|SLAB_PANIC,
                                                NULL, NULL);
            // ����״̬HASH��, ��ʼ��8��HASH����,�Ժ����Ų�������������
            // �ᶯ̬����HASH�������
            hmask = 8 - 1;
            sz = (hmask+1) * sizeof(struct hlist_head);
            // ��HASH���ǰ����Ե�index��������������
            xfrm_policy_byidx = xfrm_hash_alloc(sz);
            xfrm_idx_hmask = hmask;
            if (!xfrm_policy_byidx)
            panic("XFRM: failed to allocate byidx hash\n");
            // ����, ���, ת�����������, ˫��
            for (dir = 0; dir < XFRM_POLICY_MAX * 2; dir++) {
                struct xfrm_policy_hash *htab;
                // ��ʼ��inexact����ͷ, inexact����ѡ������س��Ȳ��Ǳ�׼ֵ��һЩ�ر����
                INIT_HLIST_HEAD(&xfrm_policy_inexact[dir]);
                // ���䰴��ַHASH��HASH��
                htab = &xfrm_policy_bydst[dir];
                htab->table = xfrm_hash_alloc(sz);
                htab->hmask = hmask;
                if (!htab->table)
                panic("XFRM: failed to allocate bydst hash\n");
            }
            // ��ʼ�����������Ѽ��Ĺ�������, ��ɶԲ����������Ѽ����ͷ�
            INIT_WORK(&xfrm_policy_gc_work, xfrm_policy_gc_task, NULL);
            // �Ǽ�����֪ͨ
            register_netdevice_notifier(&xfrm_dev_notifier);
        }
        xfrm������֪ͨ�ص��ṹ
        static struct notifier_block xfrm_dev_notifier = {
            xfrm_dev_event,
            NULL,
            0
        };
        // ����֪ͨ�ص�����
        static int xfrm_dev_event(struct notifier_block *this, unsigned long event, void *ptr)
        {
            switch (event) {
                // �������down���Ļ�, �����ص����е�xfrm·����
                case NETDEV_DOWN:
                xfrm_flush_bundles();
            }
            return NOTIFY_DONE;
        }
        // �����ص����е�xfrm·����
        static int xfrm_flush_bundles(void)
        {
            // �����õ�·����ɾ��
            xfrm_prune_bundles(stale_bundle);
            return 0;
        }       
    3.3 �����ʼ��
        /* net/xfrm/xfrm_input.c */
        void __init xfrm_input_init(void)
        {
            // ����һ���ں�cache, ���ڷ���sec_path�ṹ(��ȫ·��)
            secpath_cachep = kmem_cache_create("secpath_cache",
                                                sizeof(struct sec_path),
                                                0, SLAB_HWCACHE_ALIGN|SLAB_PANIC,
                                                NULL, NULL);
        }
        struct sec_path�ṹ�Ƕ�����ļ��ܰ����в�����Ĵ���, 
        ��sk_buff���иýṹ��ָ��sp, ���sp�ǿձ�ʾ���Ǹ�IPSEC���ܺ�İ���
4. ״̬(xfrm_state)����
    ���������ܵĺ�������net/xfrm/xfrm_state.c�ж��塣
    4.1 ״̬����
        ״̬���亯��Ϊxfrm_state_alloc(), �ú�����pfkey_msg2xfrm_state()��������, 
        pfkey_msg2xfrm_state()�����ǽ���׼��pfkey_msg(SA�ṹ)ת��Ϊxfrm״̬,
        ͬʱ�ú���Ҳ������״̬����������.
        struct xfrm_state *xfrm_state_alloc(void)
        {
            struct xfrm_state *x;
            // ����ռ�
            x = kzalloc(sizeof(struct xfrm_state), GFP_ATOMIC);
            if (x) {
                // ʹ������ʼ��Ϊ1
                atomic_set(&x->refcnt, 1);
                // ��0��ipsecͨ��ʹ��
                atomic_set(&x->tunnel_users, 0);
                // ��ʼ������ڵ�, ״̬�ɰ�Ŀ�ĵ�ַ, Դ��ַ��SPI�ҽӵ���ͬ����
                INIT_HLIST_NODE(&x->bydst);
                INIT_HLIST_NODE(&x->bysrc);
                INIT_HLIST_NODE(&x->byspi);
                // ״̬��ʱ��
                init_timer(&x->timer);
                // ��ʱ��������
                x->timer.function = xfrm_timer_handler;
                x->timer.data  = (unsigned long)x;
                // �طż�ⶨʱ��
                init_timer(&x->rtimer);
                // �طŶ�ʱ��������
                x->rtimer.function = xfrm_replay_timer_handler;
                x->rtimer.data     = (unsigned long)x;
                x->curlft.add_time = (unsigned long)xtime.tv_sec;
                // SA�����ڲ���
                x->lft.soft_byte_limit = XFRM_INF;
                x->lft.soft_packet_limit = XFRM_INF;
                x->lft.hard_byte_limit = XFRM_INF;
                x->lft.hard_packet_limit = XFRM_INF;
                // �طŴ������
                x->replay_maxage = 0;
                x->replay_maxdiff = 0;
                // ��ʼ��״̬��
                spin_lock_init(&x->lock);
            }
            return x;
        }
        EXPORT_SYMBOL(xfrm_state_alloc);
        // ״̬��ʱ����ʱ������
        static void xfrm_timer_handler(unsigned long data)
        {
            struct xfrm_state *x = (struct xfrm_state*)data;
            unsigned long now = (unsigned long)xtime.tv_sec;
            long next = LONG_MAX;
            int warn = 0;
            spin_lock(&x->lock);
            // �����xfrm״̬�Ѿ���������״̬, ���Է�����
            if (x->km.state == XFRM_STATE_DEAD)
                goto out;
            // ������������ڵ���״̬, ת���ڴ���
            if (x->km.state == XFRM_STATE_EXPIRED)
                goto expired;
            // ��������˻�Ҫǿ��Ҫ����һЩʱ��
            if (x->lft.hard_add_expires_seconds) {
                // ����ǿ�����ӵĳ�ʱʱ��
                long tmo = x->lft.hard_add_expires_seconds +
                x->curlft.add_time - now;
                // û�����ӳ�ʱ��, ����
                if (tmo <= 0)
                goto expired;
                if (tmo < next)
                next = tmo;
            }
            // ��������˻�Ҫǿ��Ҫ���ӵ�ʹ��ʱ��
            if (x->lft.hard_use_expires_seconds) {
                // ����ǿ�����ӵ�ʹ��ʱ��
                long tmo = x->lft.hard_use_expires_seconds +
                (x->curlft.use_time ? : now) - now;
                // û�����ӳ�ʱ��, ����
                if (tmo <= 0)
                goto expired;
                if (tmo < next)
                next = tmo;
            }
            // dying��ʾ�������ӳ�ʱ�Ѿ�������
            if (x->km.dying)
                goto resched;
            // ��������˻�Ҫ����Ҫ����һЩʱ��
            if (x->lft.soft_add_expires_seconds) {
                // �����������ӵ�ʱ��
                long tmo = x->lft.soft_add_expires_seconds +
                x->curlft.add_time - now;
                // �������ӳ�ʱ��������
                if (tmo <= 0)
                warn = 1;
                else if (tmo < next)
                next = tmo;
            }
            // ��������˻�Ҫ����Ҫ���ӵ�ʹ��ʱ��
            if (x->lft.soft_use_expires_seconds) {
                // �����������ӵ�ʹ��ʱ��
                long tmo = x->lft.soft_use_expires_seconds +
                (x->curlft.use_time ? : now) - now;
                // �������ӳ�ʱ��������
                if (tmo <= 0)
                warn = 1;
                else if (tmo < next)
                next = tmo;
            }
            // dying��Ϊ�������ӳ�ʱ�Ƿ���ñ�־
            x->km.dying = warn;
            // �������ӳ�ʱ�ѱȲ�����, ����״̬�ĳ�ʱ����֪ͨ
            if (warn)
                km_state_expired(x, 0, 0);
            resched:
                // ������ӵĳ�ʱ��Ч, �޸Ķ�ʱ����ʱʱ��
                if (next != LONG_MAX)
                    mod_timer(&x->timer, jiffies + make_jiffies(next));
                goto out;
            expired:
                // ״̬����
                if (x->km.state == XFRM_STATE_ACQ && x->id.spi == 0) {
                // ������״̬��ACQ����״̬(�����û��ռ�����������״̬,�����ں˸��ݲ�������Ҫ��
                // �û��ռ����IKEЭ�̽�����״̬)
                // ״̬����Ϊ����
                x->km.state = XFRM_STATE_EXPIRED;
                // ���ѵȴ�����׼�����������Ѽ�����
                wake_up(&km_waitq);
                next = 2;
                goto resched;
                }
                // ɾ��״̬, ����״̬�ĵ���֪ͨ
                if (!__xfrm_state_delete(x) && x->id.spi)
                // 1��ʾ��Ӳ�Ե�����
                km_state_expired(x, 1, 0);
            out:
                spin_unlock(&x->lock);
        }
        // �طŶ�ʱ����ʱ�ص�����
        static void xfrm_replay_timer_handler(unsigned long data)
        {
            struct xfrm_state *x = (struct xfrm_state*)data;
            spin_lock(&x->lock);
            // ֻ��״̬Ϊ��Чʱ�ż��
            if (x->km.state == XFRM_STATE_VALID) {
                // �Ƿ���NETLINK�ļ�����
                if (xfrm_aevent_is_on())
                    // ֪ͨ�طų�ʱ�¼�
                    xfrm_replay_notify(x, XFRM_REPLAY_TIMEOUT);
                else
                    // ����֪ͨ�Ƴٱ�־
                    x->xflags |= XFRM_TIME_DEFER;
            }
            spin_unlock(&x->lock);
        }
        ״̬��ʼ��:
        int xfrm_init_state(struct xfrm_state *x)
        {
            struct xfrm_state_afinfo *afinfo;
            int family = x->props.family;
            int err;
            err = -EAFNOSUPPORT;
            // ��ȡЭ������Ϣ�ṹ
            afinfo = xfrm_state_get_afinfo(family);
            if (!afinfo)
                goto error;
            err = 0;
            // Э������Ϣ��ʼ��
            if (afinfo->init_flags)
                err = afinfo->init_flags(x);
            xfrm_state_put_afinfo(afinfo);
            if (err)
                goto error;
            err = -EPROTONOSUPPORT;
            // ��ȡ����Э��(ah, esp, ipcomp, ip)
            x->type = xfrm_get_type(x->id.proto, family);
            if (x->type == NULL)
                goto error;
            err = x->type->init_state(x);
            if (err)
                goto error;
            // ��ȡ����ģʽ(transport, tunnel)
            x->mode = xfrm_get_mode(x->props.mode, family);
            if (x->mode == NULL)
                goto error;
            // ״̬����ΪVALID
            x->km.state = XFRM_STATE_VALID;
            error:
                return err;
        }
        EXPORT_SYMBOL(xfrm_init_state);
    4.2 ״̬ɾ��
        ״̬ɾ������Ϊxfrm_state_delete(), �ú�����pfkey_delete��������.
        // �������ֻ��__xfrm_state_delete()�����İ�������
        int xfrm_state_delete(struct xfrm_state *x)
        {
            int err;
            spin_lock_bh(&x->lock);
            err = __xfrm_state_delete(x);
            spin_unlock_bh(&x->lock);
            return err;
        }
        EXPORT_SYMBOL(xfrm_state_delete);
        // ʵ�ʵ���ͬɾ����������, ���뱣֤��x->lock����״̬��ִ��
        int __xfrm_state_delete(struct xfrm_state *x)
        {
            int err = -ESRCH;
            // ���״̬�Ѿ���DEAD�Ͳ�������
            if (x->km.state != XFRM_STATE_DEAD) {
                // ����״̬ΪDEAD
                x->km.state = XFRM_STATE_DEAD;
                // xfrm_state_lock��ȫ�ֵ�״̬���������
                spin_lock(&xfrm_state_lock);
                // ��Ŀ�ĵ�ַ�����������жϿ�
                hlist_del(&x->bydst);
                // ��Դ��ַ�����������жϿ�
                hlist_del(&x->bysrc);
                // ��SPI�����������жϿ�
                if (x->id.spi)
                    hlist_del(&x->byspi);
                // xfrm״̬������һ
                xfrm_state_num--;
                spin_unlock(&xfrm_state_lock);
                /* All xfrm_state objects are created by xfrm_state_alloc.
                * The xfrm_state_alloc call gives a reference, and that
                * is what we are dropping here.
                */
                // ���ٸ�״̬���ü���
                __xfrm_state_put(x);
                err = 0;
            }
            return err;
        }
        EXPORT_SYMBOL(__xfrm_state_delete);
    4.3 ɾ��ȫ��״̬
        ɾ��ȫ��״̬����Ϊxfrm_state_flush(), �ú�����pfkey_flush��������.
        // ɾ��ĳ��Э��proto������״̬
        void xfrm_state_flush(u8 proto)
        {
            int i;
            spin_lock_bh(&xfrm_state_lock);
            // ѭ������HASH����
            for (i = 0; i <= xfrm_state_hmask; i++) {
                struct hlist_node *entry;
                struct xfrm_state *x;
                restart:
                    // �ڰ�Ŀ�ĵ�ַ����������������ѭ����֧����Ƕ��������
                    hlist_for_each_entry(x, entry, xfrm_state_bydst+i, bydst) 
                    {
                        // Ҫ������������:
                        // �����ڱ�ipsecͨ��ʹ�õ�״̬; Э������ƥ��
                        if (!xfrm_state_kern(x) &&
                            xfrm_id_proto_match(x->id.proto, proto)) 
                        {
                            // ��holdס״̬,��ֹ�ڽ⿪xfrm_state_lock��, 
                            // ��û������xfrm_state_delete()ǰ
                            // ������ɾ����, �˴����ǵñȽ���ϸ
                            xfrm_state_hold(x);
                            // �Ƚ⿪xfrm_state_lock, ��xfrm_state_delete()��Ҫ��������
                            spin_unlock_bh(&xfrm_state_lock);
                            // ɾ��״̬
                            xfrm_state_delete(x);
                            // ���ٸղŵ����ü���
                            xfrm_state_put(x);
                            // ���¼���, ѭ��
                            spin_lock_bh(&xfrm_state_lock);
                            goto restart;
                        }
                    }
            }
            spin_unlock_bh(&xfrm_state_lock);
            wake_up(&km_waitq);
        }
        EXPORT_SYMBOL(xfrm_state_flush);
    4.4 ״̬���ӻ����
        ״̬���Ӻ���Ϊxfrm_state_add(), ״̬���º���Ϊxfrm_state_update(),
        ��������������pfkey_add��������.
        // ���xfrm״̬
        int xfrm_state_add(struct xfrm_state *x)
        {
            struct xfrm_state *x1;
            int family;
            int err;
            // ��Э��ΪΪESP, AH, COMP�Լ�ANYʱΪ��, ����Ϊ��
            int use_spi = xfrm_id_proto_match(x->id.proto, IPSEC_PROTO_ANY);
            family = x->props.family;
            spin_lock_bh(&xfrm_state_lock);
            // ����xfrm�ĵ�ַ, SPI, Э��, Э�������Ϣ�����ں����Ƿ��Ѿ�������ͬ��xfrm
            x1 = __xfrm_state_locate(x, use_spi, family);
            if (x1) {
                // ȷʵ�Ѿ�����, ���ش���
                xfrm_state_put(x1);
                x1 = NULL;
                err = -EEXIST;
                goto out;
            }
            if (use_spi && x->km.seq) {
                // ������к���Ч, �������кŲ����ں����Ƿ��Ѿ�������ͬ��xfrm
                x1 = __xfrm_find_acq_byseq(x->km.seq);
                // �ҵ�, �����Ŀ�ĵ�ַ�����ϵĻ�, ����Ϊû�ҵ�
                if (x1 && xfrm_addr_cmp(&x1->id.daddr, &x->id.daddr, family)) {
                    xfrm_state_put(x1);
                    x1 = NULL;
                }
            }
            // ���û�ҵ�x1, ���ݸ�����Ϣ�ٲ���xfrm
            if (use_spi && !x1)
                x1 = __find_acq_core(family, x->props.mode, x->props.reqid,
                                     x->id.proto,
                                     &x->id.daddr, &x->props.saddr, 0);
            // ���x�������ں��е�xfrmƥ��Ļ�Ϊx����genid����
            // ���õ�һ����̬���ļ�ȫ�ֱ���: xfrm_state_genid
            __xfrm_state_bump_genids(x);
            // ����xfrm�����ں˵ĸ�xfrm��, ��Щ������HASH����ʽʵ�ֵ�, �ֱ����
            // Դ��ַ, Ŀ�ĵ�ַ�γ�����HASH��
            __xfrm_state_insert(x);
            err = 0;
            out:
                spin_unlock_bh(&xfrm_state_lock);
                // ����������������ҵ�x1, ɾ��֮, ��״̬����Ҫ��
                if (x1) {
                    // ���ҵ���x1��������ɾ��,
                    xfrm_state_delete(x1);
                    // �ͷ�x1
                    xfrm_state_put(x1);
                }
            return err;
        }
        EXPORT_SYMBOL(xfrm_state_add);
        // ����xfrm״̬
        int xfrm_state_update(struct xfrm_state *x)
        {
            struct xfrm_state *x1;
            int err;
            int use_spi = xfrm_id_proto_match(x->id.proto, IPSEC_PROTO_ANY);
            spin_lock_bh(&xfrm_state_lock);
            // �����ں�����Ӧ��xfrm, �Ҳ����Ļ�����
            x1 = __xfrm_state_locate(x, use_spi, x->props.family);
            err = -ESRCH;
            if (!x1)
                goto out;
            // �����xfrm���ڱ�IPSECͨ��ʹ��, ���ش���
            if (xfrm_state_kern(x1)) {
                xfrm_state_put(x1);
                err = -EEXIST;
                goto out;
            }
            // �ҵ���x1����������acquire״̬, ֱ�ӽ�x����ϵͳxfrm�������
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
                    // ���ҵ���acquire״̬��xfrmɾ��, ��ȷ����
                    xfrm_state_delete(x1);
                    xfrm_state_put(x1);
                    return 0;
                }
            // �ҵ���x1, ״̬Ҳ����acquire, �����������ĸ���x1�е�����Ϊx������
            err = -EINVAL;
            spin_lock_bh(&x1->lock);
            if (likely(x1->km.state == XFRM_STATE_VALID)) {
                // ������װ����
                if (x->encap && x1->encap)
                    memcpy(x1->encap, x->encap, sizeof(*x1->encap));
                // ����care of�ĵ�ַ
                if (x->coaddr && x1->coaddr) {
                    memcpy(x1->coaddr, x->coaddr, sizeof(*x1->coaddr));
                }
                // û��SPIʱ����ѡ����
                if (!use_spi && memcmp(&x1->sel, &x->sel, sizeof(x1->sel)))
                    memcpy(&x1->sel, &x->sel, sizeof(x1->sel));
                // ����������
                memcpy(&x1->lft, &x->lft, sizeof(x1->lft));
                x1->km.dying = 0;
                // 1���ӵĳ�ʱ
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
    4.5 ״̬����
        ״̬���뺯��Ϊxfrm_state_insert(), �ú�����ipcomp_tunnel_attach()����(net/ipv4/ipcomp.c)����
        // xfrm_state_insertֻ�Ǹ���������, ��xfrm_state_lock�������__xfrm_state_bump_genids��
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
        // ��ײ���, ���Ƿ��ж������״̬, Ҫ��������
        static void __xfrm_state_bump_genids(struct xfrm_state *xnew)
        {
            unsigned short family = xnew->props.family;
            u32 reqid = xnew->props.reqid;
            struct xfrm_state *x;
            struct hlist_node *entry;
            unsigned int h;
            // ����״̬HASHֵ�����������
            h = xfrm_dst_hash(&xnew->id.daddr, &xnew->props.saddr, reqid, family);
            hlist_for_each_entry(x, entry, xfrm_state_bydst+h, bydst)
            {
                // ����Ѿ��������е�״̬��Э����, ����ID, Դ��ַ, Ŀ�ĵ�ַ������״̬ƥ��
                if (x->props.family == family && x->props.reqid == reqid &&
                    !xfrm_addr_cmp(&x->id.daddr, &xnew->id.daddr, family) &&
                    !xfrm_addr_cmp(&x->props.saddr, &xnew->props.saddr, family))
                    // ����Щ״̬��genid��������Ϊ��ǰxfrm_state_genid(ȫ�ֱ���)
                    x->genid = xfrm_state_genid;
            }
        }
        static void __xfrm_state_insert(struct xfrm_state *x)
        {
            unsigned int h;
            // ����״̬��genid����Ϊ��ǰxfrm_state_genidֵ��һ,��������ײ��״̬���ֿ�
            x->genid = ++xfrm_state_genid;
            // ��ӵ���Ŀ�ĵ�ַHASH������
            h = xfrm_dst_hash(&x->id.daddr, &x->props.saddr,
            x->props.reqid, x->props.family);
            hlist_add_head(&x->bydst, xfrm_state_bydst+h);
            // ��ӵ���Դ��ַHASH������
            h = xfrm_src_hash(&x->id.daddr, &x->props.saddr, x->props.family);
            hlist_add_head(&x->bysrc, xfrm_state_bysrc+h);
            if (x->id.spi) {
                // ��ӵ���SPI����HASH������
                h = xfrm_spi_hash(&x->id.daddr, x->id.spi, x->id.proto,
                x->props.family);
                hlist_add_head(&x->byspi, xfrm_state_byspi+h);
            }
            // �޸Ķ�ʱ��, ��ʱ��1��
            mod_timer(&x->timer, jiffies + HZ);
            // ��������˻ط����ʱ����, ��ʱ��Ϊ��ֵ
            if (x->replay_maxage)
                mod_timer(&x->rtimer, jiffies + x->replay_maxage);
            // ���ѵȴ�����
            wake_up(&km_waitq);
            // ״̬������1
            xfrm_state_num++;
            // HASH������, ����Ƿ���Ҫ��չHASH������
            xfrm_hash_grow_check(x->bydst.next != NULL);
        }
    4.6 ״̬����
        ״̬���Һ����кü���, �ֱ𰴲�ͬ����������״̬, ע���ҵ�״̬��, ��������״̬�����ü���.
        4.6.1 xfrm_state_lookup
            // ֻ��__xfrm_state_lookup�İ��������� �Ǹ���SPI����HASH�����
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
                // ����SPI����HASH
                unsigned int h = xfrm_spi_hash(daddr, spi, proto, family);
                struct xfrm_state *x;
                struct hlist_node *entry;
                // ѭ����Ӧ��SPI����
                hlist_for_each_entry(x, entry, xfrm_state_byspi+h, byspi) 
                {
                    // �Ƚ�Э����, SPI, ��Э���Ƿ���ͬ
                    if (x->props.family != family ||
                        x->id.spi       != spi ||
                        x->id.proto     != proto)
                        continue;
                    // �Ƚ�Ŀ�ĵ�ַ�Ƿ���ͬ
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
                    // �ҵ�, ����״̬���ü���, ����
                    xfrm_state_hold(x);
                    return x;
                }
                return NULL;
            }
        4.6.2 ����ַ����״̬
            // ֻ��__xfrm_state_lookup_byaddr�İ����������Ǹ���Ŀ�ĵ�ַ����HASH�����
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
                // ����Ŀ�ĵ�ַ����HASHֵ
                unsigned int h = xfrm_src_hash(daddr, saddr, family);
                struct xfrm_state *x;
                struct hlist_node *entry;
                // ѭ����Ӧ��Դ��ַ����
                hlist_for_each_entry(x, entry, xfrm_state_bysrc+h, bysrc) 
                {
                    // �Ƚ�Э�����Э���Ƿ���ͬ
                    if (x->props.family != family ||
                        x->id.proto     != proto)
                        continue;
                    // �Ƚ�Դ��ַ��Ŀ�ĵ�ַ�Ƿ���ͬ
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
                    // �ҵ�, ����״̬���ü���, ����
                    xfrm_state_hold(x);
                    return x;
                }
                return NULL;
            }
        4.6.3 __xfrm_state_locate
            �������ֻ��__xfrm_state_lookup��__xfrm_state_lookup_byaddr����Ϻ���
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
        4.6.4 ����ACQUIRE���͵�״̬
            ACQUIRE���͵�SA�Ĳ������ں˷���������Ҫ���б���, ��ȴû���ҵ���ص�SA, �����û��ռ��IKEЭ�̳�����ACQUIRE����, ������һ��ACQUIRE���͵�SA, ����û��ռ�Э��Э�̳ɹ������ɺ��ʵ�SA���ں�, �ں˾ͻ��滻��ACQUIRE��SA, ���ACQUIRE�����������õ�SA, ֻ�Ǳ�ʾ�д�SA������, �ȴ��û��ռ����Э�̽����
            // ֻ��__find_acq_core�İ�������
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
                // ����Դ��ַ��Ŀ�ĵ�ַ,����ID����Ŀ�ĵ�ַ����HASH
                unsigned int h = xfrm_dst_hash(daddr, saddr, reqid, family);
                struct hlist_node *entry;
                struct xfrm_state *x;
                hlist_for_each_entry(x, entry, xfrm_state_bydst+h, bydst) 
                {
                    // �Ƚ�����ID������ģʽ��Э����
                    // Ҫ��״̬������ΪXFRM_STATE_ACQ��SPIֵΪ0
                    if (x->props.reqid  != reqid ||
                        x->props.mode   != mode ||
                        x->props.family != family ||
                        x->km.state     != XFRM_STATE_ACQ ||
                        x->id.spi       != 0)
                        continue;
                    // �ٱȽ�Դ��ַ��Ŀ�ĵ�ַ�Ƿ���ͬ
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
                    // �ҵ�, ����״̬���ü���, ����
                    xfrm_state_hold(x);
                    return x;
                }
                // û�ҵ�
                // �������Ҫ����, ����NULL
                if (!create)
                    return NULL;
                // ����ACQ���͵�xfrm_state
                // ����ռ�
                x = xfrm_state_alloc();
                if (likely(x)) {
                    // ��д�����ַ��������
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
                    // ״̬��������ΪXFRM_STATE_ACQ
                    x->km.state = XFRM_STATE_ACQ;
                    // ״̬����������ֵ
                    x->id.proto = proto;
                    x->props.family = family;
                    x->props.mode = mode;
                    x->props.reqid = reqid;
                    // Ӳ�Կ����ӵĳ�ʱ
                    x->lft.hard_add_expires_seconds = XFRM_ACQ_EXPIRES;
                    xfrm_state_hold(x);
                    // ��ʱXFRM_ACQ_EXPIRES��
                    x->timer.expires = jiffies + XFRM_ACQ_EXPIRES*HZ;
                    add_timer(&x->timer);
                    // ��ӵ�Ŀ��HASH����
                    hlist_add_head(&x->bydst, xfrm_state_bydst+h);
                    // ��ӵ�Դ��ַHASH����
                    h = xfrm_src_hash(daddr, saddr, family);
                    hlist_add_head(&x->bysrc, xfrm_state_bysrc+h);
                    wake_up(&km_waitq);
                    // ����״̬����     
                }
            }
    ע��list_for_each_entry�÷�
        https://blog.csdn.net/u012503639/article/details/77771814
        ��Linux�ں�Դ���У�����Ҫ��������в���������һ������Ҫ��'��'��list_for_each_entry��
        ��˼��������
             ��ʵ������һ�� for ѭ�������ô���� pos ��Ϊѭ��������
             �ӱ�ͷ head ��ʼ���������next �����ƶ� pos��ֱ���ֻ�head
             �ڳ����е�ʹ�����£�
                var pos;
                list_for_each_entry��pos , head,member��
                {       
                    ������������
                    addr =    pos;  
                    //�Է���ֵpos�Ĳ���������������ȥ���list_for_each_entry��
                    //���԰�������for()ѭ��
                    ������������
                }
        ��list_for_each_entry��ʵ�֣�
            #define list_for_each_entry(pos, head, member)				    \
            for (pos = list_entry((head)->next, typeof(*pos), member);	\
                   prefetch(pos->member.next), &pos->member != (head); 	    \
                   pos = list_entry(pos->member.next, typeof(*pos), member)
                  )
            1. pos = list_entry((head)->next, typeof(*pos), member)
                pos�൱��ѭ���з��ص�ѭ��������������Ƿ���һ���ṹ��ָ��
                #define list_entry container_of
                ���������������:
                   ����һ���ṹ������е�һ�����Ա������ָ��
                   ����ȡָ�������ṹ�������ָ�롣
                #define container_of(ptr, type, member) ({               \
                   const typeof(((type *)0)->member)*__mptr = (ptr);   \
                   (type *)((char *)__mptr - offsetof(type, member)); })
                ����list_entry()������Ϊ��
                    ͨ����֪��ָ��member�����ָ�룬��������ṹ���ָ�루��ַ��
            2. prefetch(pos->member.next),&pos->member!= (head);  
                refetch�ĺ����Ǹ���cpu��ЩԪ���п������Ͼ�Ҫ�õ���
                ����cpuԤȡһ�£�������������ٶȣ�����Ԥȡ����߱����ٶȣ�
                &pos->member !=(head)  ������ж�ѭ��������
            3. pos= list_entry(pos->member.next, typeof(*pos), member)) 
                �͵ڣ�1��ʵ�����ƣ������������next �����ƶ� pos��
5. ��ȫ����(xfrm_policy)����
    ���������ܵĺ�������net/xfrm/xfrm_policy.c�ж��塣
    5.1 ���Է���
        ���Է��亯��Ϊxfrm_policy_alloc(), �ú�����pfkey_spdadd()��������
        struct xfrm_policy *xfrm_policy_alloc(gfp_t gfp)
        {
            struct xfrm_policy *policy;
            // ����struct xfrm_policy�ṹ�ռ䲢����
            policy = kzalloc(sizeof(struct xfrm_policy), gfp);
            if (policy)
            {
                // ��ʼ�����ӽڵ�
                INIT_HLIST_NODE(&policy->bydst);
                INIT_HLIST_NODE(&policy->byidx);
                // ��ʼ����
                rwlock_init(&policy->lock);
                // �������ü�����ʼ��Ϊ1
                atomic_set(&policy->refcnt, 1);
                // ��ʼ����ʱ��
                init_timer(&policy->timer);
                policy->timer.data = (unsigned long)policy;
                policy->timer.function = xfrm_policy_timer;
            }
            return policy;
        }
        EXPORT_SYMBOL(xfrm_policy_alloc);
        ��ʱ������:
        static void xfrm_policy_timer(unsigned long data)
        {
            struct xfrm_policy *xp = (struct
                                      xfrm_policy*)data;
            unsigned long now = (unsigned
                                 long)xtime.tv_sec;
            long next = LONG_MAX;
            int warn = 0;
            int dir;
            // ����
            read_lock(&xp->lock);
            // ��������Ѿ�������, �˳�
            if (xp->dead)
                goto out;
            // ���ݲ���������ȷ�����Դ�������ݵķ���, �������ŵĺ�3λ
            dir =
                xfrm_policy_id2dir(xp->index);
            // ��������˻�Ҫǿ��Ҫ����һЩʱ��
            if
            (xp->lft.hard_add_expires_seconds)
            {
                // ����ǿ�����ӵĳ�ʱʱ��
                long tmo = xp->lft.hard_add_expires_seconds +
                           xp->curlft.add_time - now;
                // û�����ӳ�ʱ��, ����
                if (tmo <= 0)
                    goto expired;
                if (tmo < next)
                    next = tmo;
            }
            // ��������˻�Ҫǿ��Ҫ���ӵ�ʹ��ʱ��
            if (xp->lft.hard_use_expires_seconds)
            {
                // ����ǿ�����ӵ�ʹ��ʱ��
                long tmo = xp->lft.hard_use_expires_seconds +
                           (xp->curlft.use_time ? : xp->curlft.add_time) - now;
                // û�����ӳ�ʱ��, ����
                if (tmo <= 0)
                    goto expired;
                if (tmo < next)
                    next = tmo;
            }
            // ��������˻�Ҫ����Ҫ����һЩʱ��
            if (xp->lft.soft_add_expires_seconds)
            {
                // �����������ӵ�ʱ��
                long tmo = xp->lft.soft_add_expires_seconds +
                           xp->curlft.add_time - now;
                // �������ӳ�ʱС��0, ���ñ�����־, ������ʱ����ΪXFRM_KM_TIMEOUT, ����������ͬ
                if (tmo <= 0)
                {
                    warn = 1;
                    tmo = XFRM_KM_TIMEOUT;
                }
                if (tmo < next)
                    next = tmo;
            }
            // ��������˻�Ҫ����Ҫ���ӵ�ʹ��ʱ��
            if (xp->lft.soft_use_expires_seconds)
            {
                // �����������ӵ�ʹ��ʱ��
                long tmo = xp->lft.soft_use_expires_seconds +
                           (xp->curlft.use_time ? : xp->curlft.add_time) - now;
                // �������ӳ�ʱС��0, ���ñ�����־, ������ʱ����ΪXFRM_KM_TIMEOUT, ����������ͬ
                if (tmo <= 0)
                {
                    warn = 1;
                    tmo = XFRM_KM_TIMEOUT;
                }
                if (tmo < next)
                    next = tmo;
            }
            // ��Ҫ����, ���õ��ڻص�
            if (warn)
                km_policy_expired(xp, dir, 0, 0);
            // ������µĳ�ʱֵ��Ч, �޸Ķ�ʱ����ʱ, ���Ӳ���ʹ�ü���
            if (next != LONG_MAX && !mod_timer(&xp->timer, jiffies + make_jiffies(next)))
                xfrm_pol_hold(xp);
            out:
                read_unlock(&xp->lock);
                xfrm_pol_put(xp);
                return;
            expired:
                read_unlock(&xp->lock);
                // ���ȷʵ����, ɾ������
                if (!xfrm_policy_delete(xp, dir))
                    // 1��ʾ��Ӳ�Ե�����
                    km_policy_expired(xp, dir, 1, 0);
                xfrm_pol_put(xp);
        }
    5.2 ���Բ���
        ���Բ��뺯��Ϊxfrm_policy_insert(), �ú�����pfkey_spdadd()��������,
        ע����������ǰ�����Ȩ��С�����������������, ��˲������ʱҪ��������Ȩ�ȽϺ���뵽���ʵ�λ��.
        int xfrm_policy_insert(int dir, struct xfrm_policy *policy, int excl)
        {
            struct xfrm_policy *pol;
            struct xfrm_policy *delpol;
            struct hlist_head *chain;
            struct hlist_node *entry, *newpos, *last;
            struct dst_entry *gc_list;
            write_lock_bh(&xfrm_policy_lock);
            // �ҵ������hash����
            chain = policy_hash_bysel(&policy->selector, policy->family, dir);
            delpol = NULL;
            newpos = NULL;
            last = NULL;
            // ��������, ���������Բ��Ե����ȼ�ֵ�������������, �����Ҫ�����²��Ե����ȼ���С
            // ���²��Բ嵽���ʵ�λ��
            hlist_for_each_entry(pol, entry, chain, bydst)
            {
                // delpolҪΪ��
                if (!delpol &&
                    // �������ͱȽ�
                    pol->type == policy->type
                    &&
                    // ѡ���ӱȽ�
                    !selector_cmp(&pol->selector, &policy->selector)
                    &&
                    // ��ȫ�����ıȽ�
                    xfrm_sec_ctx_match(pol->security, policy->security))
                {
                    // �²��Ժ����е�ĳ����ƥ��
                    if (excl)
                    {
                        // �������������Ӳ���, Ҫ����Ĳ��������ݿ����Ѿ�����, ��������
                        write_unlock_bh(&xfrm_policy_lock);
                        return -EEXIST;
                    }
                    // �����Ҫɾ���Ĳ���λ��
                    delpol = pol;
                    // Ҫ���µĲ������ȼ�ֵ����ԭ�е����ȼ�ֵ, ����ѭ���ҵ����ʵĲ���λ��
                    // ��Ϊ��������������ȼ�ֵ���������, ������
                    // ����delpol�Ѿ��ǿ���,  ǰ��Ĳ��Բ��������Ѿ�������������
                    if (policy->priority > pol->priority)
                        continue;
                }
                else if (policy->priority >= pol->priority)
                {
                    // ����µ����ȼ������ڵ�ǰ�����ȼ�, ���浱ǰ�ڵ�, �������Һ��ʲ���λ��
                    last = &pol->bydst;
                    continue;
                }
                // �����Ǹ����²��Ե����ȼ�ȷ���Ĳ���λ��
                if (!newpos)
                    newpos = &pol->bydst;
                // ����Ѿ��ҵ�Ҫɾ���Ĳ���, �ж�
                if (delpol)
                    break;
                last = &pol->bydst;
            }
            if (!newpos)
                newpos = last;
            // ������Ե���Ŀ�ĵ�ַHASH�������ָ��λ��
            if (newpos)
                hlist_add_after(newpos, &policy->bydst);
            else
                hlist_add_head(&policy->bydst, chain);
            // ���Ӳ������ü���
            xfrm_pol_hold(policy);
            // �÷���Ĳ�������1
            xfrm_policy_count[dir]++;
            atomic_inc(&flow_cache_genid);
            // �������ͬ���ϲ���, Ҫ��Ŀ�ĵ�ַHASH��������HASH����������ɾ��
            if (delpol)
            {
                hlist_del(&delpol->bydst);
                hlist_del(&delpol->byidx);
                xfrm_policy_count[dir]--;
            }
            // ��ȡ����������, ��������HASH����
            policy->index = delpol ?
                            delpol->index :
                            xfrm_gen_index(policy->type, dir);
            hlist_add_head(&policy->byidx,
                           xfrm_policy_byidx+idx_hash(policy->index));
            // ���Բ���ʵ��ʱ��
            policy->curlft.add_time = (unsigned long)xtime.tv_sec;
            policy->curlft.use_time = 0;
            if (!mod_timer(&policy->timer, jiffies + HZ))
                xfrm_pol_hold(policy);
            write_unlock_bh(&xfrm_policy_lock);
            // �ͷ��ϲ���
            if (delpol)
                xfrm_policy_kill(delpol);
            else if (xfrm_bydst_should_resize(dir, NULL))
                schedule_work(&xfrm_hash_work);
            // �����ͷ����в��Ե�ǰ��·��cache
            read_lock_bh(&xfrm_policy_lock);
            gc_list = NULL;
            entry = &policy->bydst;
            // ��������, �Ѽ�����·��cache��������
            hlist_for_each_entry_continue(policy, entry, bydst)
            {
                struct dst_entry *dst;
                write_lock(&policy->lock);
                // ���Ե�·������ͷ
                dst = policy->bundles;
                if (dst)
                {
                    // ֱ�ӽ���������·������ӵ���������ǰ��
                    struct dst_entry *tail = dst;
                    while (tail->next)
                        tail = tail->next;
                    tail->next = gc_list;
                    gc_list = dst;
                    // ��ǰ���Ե�·��Ϊ��
                    policy->bundles = NULL;
                }
                write_unlock(&policy->lock);
            }
            read_unlock_bh(&xfrm_policy_lock);
            // �ͷ�����·��cahce
            while (gc_list)
            {
                struct dst_entry *dst = gc_list;
                gc_list = dst->next;
                dst_free(dst);
            }
            return 0;
        }
        EXPORT_SYMBOL(xfrm_policy_insert);
    5.3  ɾ��ĳ���͵�ȫ����ȫ����
        �ú�����pfkey_spdflush()�Ⱥ�������
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
                    // ����inexact HASH����
                    hlist_for_each_entry(pol, entry,
                                         &xfrm_policy_inexact[dir], bydst)
                    {
                        // �ж�����
                        if (pol->type != type)
                            continue;
                        // �����Դ�bydst�����жϿ�
                        hlist_del(&pol->bydst);
                        // �����Դ�byidt�����жϿ�
                        hlist_del(&pol->byidx);
                        write_unlock_bh(&xfrm_policy_lock);
                        // ������״̬��Ϊdead, ����ӵ�ϵͳ�Ĳ�������������е��ȴ���׼��ɾ��
                        xfrm_policy_kill(pol);
                        killed++;
                        write_lock_bh(&xfrm_policy_lock);
                        goto again1;
                    }
                    // ��������Ŀ��HASH����
                    for (i = xfrm_policy_bydst[dir].hmask; i >= 0; i--)
                    {
                        again2:
                            // ������Ŀ�ĵ�ַHASH������
                            hlist_for_each_entry(pol,
                                                 entry,
                                                 xfrm_policy_bydst[dir].table + i,
                                                 bydst)
                            {
                                if
                                (pol->type != type)
                                    continue;
                                // ���ڵ�������жϿ�
                                hlist_del(&pol->bydst);
                                hlist_del(&pol->byidx);
                                write_unlock_bh(&xfrm_policy_lock);
                                // �ͷŽڵ�
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
        // �����ͷŵ���������
        static void xfrm_policy_kill(struct xfrm_policy *policy)
        {
            int dead;
            write_lock_bh(&policy->lock);
            // �����ϵ�DEAD��־
            dead = policy->dead;
            // ���ò���DEAD��־
            policy->dead = 1;
            write_unlock_bh(&policy->lock);
            // Ϊʲô����ǰ���ж�DEAD��?
            if (unlikely(dead))
            {
                WARN_ON(1);
                return;
            }
            spin_lock(&xfrm_policy_gc_lock);
            // ���ò��Խڵ�ӵ�ǰ����Ͽ�, ���������������
            hlist_add_head(&policy->bydst,
                           &xfrm_policy_gc_list);
            spin_unlock(&xfrm_policy_gc_lock);
            // ���Ȳ����������Թ����ṹ
            schedule_work(&xfrm_policy_gc_work);
        }
    5.4 ���Բ���
        5.4.1 ���Բ��Ҳ�ɾ��
            ����ѡ���ӺͰ�ȫ�����Ĳ��Ҳ���, �ɲ��Ҳ��Բ�ɾ��, ��pfkey_spddelete()��������
            struct xfrm_policy *xfrm_policy_bysel_ctx(u8 type, int dir,
                                                      struct xfrm_selector *sel,
                                                      struct xfrm_sec_ctx *ctx, int delete)
            {
                struct xfrm_policy *pol, *ret;
                struct hlist_head *chain;
                struct hlist_node *entry;
                write_lock_bh(&xfrm_policy_lock);
                // ��λHASH��
                chain = policy_hash_bysel(sel, sel->family, dir);
                ret = NULL;
                // ��������
                hlist_for_each_entry(pol, entry, chain, bydst)
                {
                    // ��������, ѡ���Ӻ������Ľ���ƥ��
                    if (pol->type == type && !selector_cmp(sel, &pol->selector)
                        && xfrm_sec_ctx_match(ctx, pol->security))
                    {
                        xfrm_pol_hold(pol);
                        if (delete)
                        {
                            // Ҫ��ɾ���������Խڵ��Ŀ�ĵ�ַHASH���������HASH�����жϿ�
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
                    // ����genid
                    atomic_inc(&flow_cache_genid);
                    // ������״̬��Ϊdead, ����ӵ�ϵͳ�Ĳ�������������е��ȴ���׼��ɾ��
                    xfrm_policy_kill(ret);
                }
                return ret;
            }
            EXPORT_SYMBOL(xfrm_policy_bysel_ctx);
        5.4.2 �������Ų��Ҳ�ɾ��
            struct xfrm_policy *xfrm_policy_byid(u8 type, int dir, u32 id, int delete)
            {
                struct xfrm_policy *pol, *ret;
                struct hlist_head *chain;
                struct hlist_node *entry;
                write_lock_bh(&xfrm_policy_lock);
                // ���������Ŷ�λ����
                chain = xfrm_policy_byidx + idx_hash(id);
                ret = NULL;
                // ��������
                hlist_for_each_entry(pol, entry, chain, byidx)
                {
                    // ���Ե����ͺ���������ͬ
                    if (pol->type == type && pol->index == id)
                    {
                        xfrm_pol_hold(pol);
                        // ���Ҫɾ��, �����Խڵ��������ɾ��
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
                    // ����genid
                    atomic_inc(&flow_cache_genid);
                    // ������״̬��Ϊdead, ����ӵ�ϵͳ�Ĳ�������������е��ȴ���׼��ɾ��
                    xfrm_policy_kill(ret);
                }
                return ret;
            }
            EXPORT_SYMBOL(xfrm_policy_byid);
        5.4.3 ����·�ɲ��Ҳ���
            // ����fl��·����صĽṹ, ������·�ɲ�����
            // ע�ⷵ��ֵ������, 0�ɹ�, ��0ʧ��, �ҵ��Ĳ���ͨ������objp���д���
            static int xfrm_policy_lookup(struct flowi *fl, u16 family, u8 dir,
                                          void **objp, atomic_t **obj_refp)
            {
                struct xfrm_policy *pol;
                int err = 0;
                #ifdef CONFIG_XFRM_SUB_POLICY
                    // �Ӳ��Բ���, ����Linux�Լ�����չ����, �Ǳ�׼����
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
                // ����MAIN���͵Ĳ���
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
                // ���ҵ��Ĳ��Ը�ֵ��objp����
                if ((*objp = (void *) pol) != NULL)
                    *obj_refp = &pol->refcnt;
                return err;
            }
            // �����Ͳ��Ҳ���
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
                // �����ṹ��Ŀ�ĺ�Դ��ַ
                daddr = xfrm_flowi_daddr(fl, family);
                saddr = xfrm_flowi_saddr(fl, family);
                if (unlikely(!daddr || !saddr))
                    return NULL;
                read_lock_bh(&xfrm_policy_lock);
                // ���ݵ�ַ��Ϣ����HASH����
                chain = policy_hash_direct(daddr, saddr, family, dir);
                ret = NULL;
                // ѭ��HASH����
                hlist_for_each_entry(pol, entry, chain, bydst)
                {
                    // ������ṹ,���ͺ�Э�����Ƿ�ƥ�����, ����0��ʾƥ��
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
                        // �����ҵ��Ĳ��Ժ����ȼ�
                        ret = pol;
                        priority = ret->priority;
                        break;
                    }
                }
                // ����inexact�����в��Ҳ���, ���Ҳ�ҵ�����, �������ȼ���С,
                // �����ҵ��Ĳ������ǰ���ҵ��Ĳ���
                chain = &xfrm_policy_inexact[dir];
                // ѭ��HASH����
                hlist_for_each_entry(pol, entry, chain, bydst)
                {
                    // ������ṹ,���ͺ�Э�����Ƿ�ƥ�����, ����0��ʾƥ��
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
                        // ������ҵ��Ĳ������ȼ���С, ����ȡ��ԭ���ҵ��Ĳ���
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
            // ���xfrm�����Ƿ��������ƥ��
            // ����0��ʾƥ��ɹ�
            static int xfrm_policy_match(struct xfrm_policy *pol, struct flowi
                                         *fl,
                                         u8 type, u16 family, int dir)
            {
                // ѡ����
                struct xfrm_selector *sel = &pol->selector;
                int match, ret = -ESRCH;
                // ������Э����������Ƿ�ƥ��
                if (pol->family != family || pol->type != type)
                    return ret;
                // ���ѡ�����Ƿ�ƥ��, ���ط�0ֵ��ʾƥ��ɹ�
                match = xfrm_selector_match(sel, fl, family);
                if (match)
                    // ����security�������Բ��ÿ���, ��������0�ĺ�������
                    ret = security_xfrm_policy_lookup(pol, fl->secid, dir);
                return ret;
            }
            // ѡ����ƥ��,�ֱ��IPV4��IPV6Э����Ƚ�
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
            //IPV4Э����ѡ���ӱȽ�
            static inline int
            __xfrm4_selector_match(struct xfrm_selector *sel, struct flowi
                                   *fl)
            {
                // �Ƚ�V4Ŀ�ĵ�ַ, V4Դ��ַ, Ŀ�Ķ˿�, Դ�˿�, Э��, ����������
                return
                    addr_match(&fl->fl4_dst, &sel->daddr, sel->prefixlen_d)
                    && addr_match(&fl->fl4_src, &sel->saddr, sel->prefixlen_s)
                    && !((xfrm_flowi_dport(fl) ^ sel->dport) & sel->dport_mask)
                    && !((xfrm_flowi_sport(fl) ^ sel->sport) & sel->sport_mask)
                    && (fl->proto == sel->proto || !sel->proto)
                    && (fl->oif == sel->ifindex || !sel->ifindex);
            }
            //IPV6Э����ѡ���ӱȽ�
            static inline int
            __xfrm6_selector_match(struct xfrm_selector *sel, struct flowi
                                   *fl)
            {
                // �Ƚ�V6Ŀ�ĵ�ַ, V6Դ��ַ, Ŀ�Ķ˿�, Դ�˿�, Э��, ����������
                return addr_match(&fl->fl6_dst, &sel->daddr, sel->prefixlen_d)
                    && addr_match(&fl->fl6_src, &sel->saddr, sel->prefixlen_s)
                    && !((xfrm_flowi_dport(fl) ^ sel->dport) & sel->dport_mask)
                    && !((xfrm_flowi_sport(fl) ^ sel->sport) &  sel->sport_mask)
                    && (fl->proto == sel->proto || !sel->proto)
                    && (fl->oif == sel->ifindex || !sel->ifindex);
            }
        5.4.4 ���Һ�sock��Ӧ�Ĳ���
            static struct xfrm_policy *xfrm_sk_policy_lookup(struct sock *sk, int dir,
                                                             struct flowi *fl)
            {
                struct xfrm_policy *pol;
                read_lock_bh(&xfrm_policy_lock);
                // sock�ṹ����sk_policy����ָ��˫�����ݵİ�ȫ����
                if ((pol = sk->sk_policy[dir]) != NULL)
                {
                    // ���ò��Ե�ѡ�����Ƿ�����ṹƥ��
                    int match = xfrm_selector_match(&pol->selector,
                                                    fl,
                                                    sk->sk_family);
                    int err = 0;
                    // ���ƥ��Ļ���������Ϊ�������
                    if (match)
                    {
                        // ���security��������Ϊ����0�Ŀպ���
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
    5.5 ������ȫ����
        �ú�����pfkey_spddump()�Ⱥ����е���
        // func��������ָ���Ա����Ĳ��Խ��еĲ���
        // ʵ�ʱ������������в���
        int xfrm_policy_walk(u8 type, 
                             int (*func)(struct xfrm_policy *, int, int, void*),
                             void *data)
        {
            struct xfrm_policy *pol;
            struct hlist_node *entry;
            int dir, count, error;
            read_lock_bh(&xfrm_policy_lock);
            count = 0;
            // ��ͳ�Ʒ������͵Ĳ��Ե�������, ������˫���
            for (dir = 0; dir < 2*XFRM_POLICY_MAX; dir++)
            {
                struct hlist_head *table = xfrm_policy_bydst[dir].table;
                int i;
                // inexact HASH��
                hlist_for_each_entry(pol, entry,
                                     &xfrm_policy_inexact[dir], bydst)
                {
                    if (pol->type == type)
                        count++;
                }
                // ��������ַHASH������
                for (i = xfrm_policy_bydst[dir].hmask; i >= 0; i--)
                {
                    // ��������
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
            // ���±���HASH��, ��ǰ��countֵ��ΪSA�����, ����û��ռ��յ�������ǵݼ���
            for (dir = 0; dir < 2*XFRM_POLICY_MAX; dir++)
            {
                struct hlist_head *table = xfrm_policy_bydst[dir].table;
                int i;
                // ����inexact����
                hlist_for_each_entry(pol, entry,
                                     &xfrm_policy_inexact[dir], bydst)
                {
                    if  (pol->type != type)
                        continue;
                    // �Է������͵Ĳ��Ե���func����
                    error = func(pol, dir % XFRM_POLICY_MAX, --count, data);
                    if (error)
                        goto out;
                }
                // ��������ַHASH������
                for (i = xfrm_policy_bydst[dir].hmask; i >= 0; i--)
                {
                    hlist_for_each_entry(pol, entry, table + i, bydst)
                    {
                        if (pol->type != type)
                            continue;
                        // �Է������͵Ĳ��Ե���func����, ��count�ݼ���0ʱ��ʾ�����һ��������
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
    5.6 ���Լ��
        __xfrm_policy_check����Ҳ��һ���Ƚ���Ҫ�ĺ���, ��xfrm_policy_check()����,
        �ֱ�xfrm4_policy_check()��xfrm6_policy_check()����,
        �������������������������ת��������.
        ����ͨ���ͷ��غϷ�, ��IPSEC���������Ƿ�Ϸ�, �Ƿ��·�ɷ���ƥ��
        // ����1��ʾ�Ϸ�, 0��ʾ���Ϸ�, ���ڸú�������0�����ݰ�ͨ���Ǳ�����
        int __xfrm_policy_check(struct sock *sk, int dir, struct sk_buff
                                *skb, unsigned short family)
        {
            struct xfrm_policy *pol;
            struct xfrm_policy *pols[XFRM_POLICY_TYPE_MAX];
            int npols = 0;
            int xfrm_nr;
            int pi;
            struct flowi fl;
            // �����Է���ת��Ϊ������, ��ʵֵ��һ����
            u8 fl_dir = policy_to_flow_dir(dir);
            int xerr_idx = -1;
            // ����Э�����decode_session()����, ��IPV4��˵����_decode_session4
            // ��skb�еĵ�ַ�˿ڵ���Ϣ�������ṹfl��
            if (xfrm_decode_session(skb, &fl, family) < 0)
                return 0;
            // ����ں�֧��NETFILTER, ������ip_nat_decode_session������дNAT��Ϣ
            // ����Ļ����Ǹ��պ���
            nf_nat_decode_session(skb, &fl, amily);
            if (skb->sp)
            {
                // �ð��ǽ����˽��ܺ��IPSEC��
                int i;
                for (i=skb->sp->len-1; i>=0; i--)
                {
                    // ��ȡ�ð���ص�SA��Ϣ
                    struct xfrm_state *x = skb->sp->xvec[i];
                    // ���SAѡ���Ӻ�������(·��)�Ƿ�ƥ��, ���Ϊ0��ʾ��ƥ��, ��ƥ��Ļ�����
                    if (!xfrm_selector_match(&x->sel, &fl, family))
                        return 0;
                }
            }
            pol = NULL;
            // ���sock�ṹ���в���
            if (sk && sk->sk_policy[dir])
            {
                // �������Ƿ�����ṹƥ��, ƥ��Ļ����ز���
                pol = xfrm_sk_policy_lookup(sk, dir, &fl);
                if (IS_ERR(pol))
                    return 0;
            }
            // ����·����Ϣ, ���û�оʹ���·��, xfrm_policy_lookup()������Ϊ�������ݸ�
            // flow_cache_lookup()����, ���Һ͸�·�ɶ�Ӧ�İ�ȫ����
            if (!pol)
                pol = flow_cache_lookup(&fl, family, fl_dir, xfrm_policy_lookup);
            // ���ҹ����г���,����0
            if (IS_ERR(pol))
                return 0;
            // ���Բ�����
            if (!pol)
            {
                // ����ð���IPSEC�����Ұ�ȫ·���е�SA���Ǵ���ģʽ,
                // ת��ʱ, �����Ѿ���װ�İ�û��Ҫ�ٴη�װ;
                // ����ʱ, �������IPSECͨ�Ű���װ����Ҳ������
                if (skb->sp &&
                    secpath_has_nontransport(skb->sp, 0, &xerr_idx))
                {
                    // �ܾ��ð�ȫ·��, ����0ʧ��
                    xfrm_secpath_reject(xerr_idx, skb, &fl);
                    return 0;
                }
                // ��ͨ������, ��ȫ���Բ�����, ����1
                return 1;
            }
            // �ҵ���ȫ����, �Ըð�Ҫ���ݲ��Խ���IPSEC����
            // ���²��Ե�ǰʹ��ʱ��
            pol->curlft.use_time = (unsigned long)xtime.tv_sec;
            pols[0] = pol;
            npols ++;
            #ifdef CONFIG_XFRM_SUB_POLICY
                // ����������Ӳ��ԵĻ����޲����Ӳ���, ���Ǳ�׼IPSEC��û�����, ���Բ�����
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
            // ���Զ���������ͨ��
            if (pol->action == XFRM_POLICY_ALLOW)
            {
                struct sec_path *sp;
                // ��α�����ȫ·��
                static struct sec_path dummy;
                struct xfrm_tmpl *tp[XFRM_MAX_DEPTH];
                struct xfrm_tmpl *stp[XFRM_MAX_DEPTH];
                struct xfrm_tmpl **tpp = tp;
                int ti = 0;
                int i, k;
                // ������ݰ�û�а�ȫ·��, ·��ָ���ʼ��Ϊα��İ�ȫ·��
                if ((sp = skb->sp) == NULL)
                    sp = &dummy;
                // ������������, ���������Ժ��Ӳ���(�ں�֧���Ӳ��ԵĻ�),һ������¾�һ������
                for (pi = 0; pi
                        < npols; pi++)
                {
                    // ����з�����ͨ����������ȫ����, ����
                    if (pols[pi] != pol && pols[pi]->action != XFRM_POLICY_ALLOW)
                        goto reject;
                    // ������Բ��̫��, ����
                    if (ti + pols[pi]->xfrm_nr >= XFRM_MAX_DEPTH)
                        goto reject_error;
                    // ���ݲ����е�xfrm����ģ��, ti������
                    for (i = 0; i < pols[pi]->xfrm_nr; i++)
                        tpp[ti++] = &pols[pi]->xfrm_vec[i];
                }
                // ��������
                xfrm_nr = ti;
                if (npols > 1)
                {
                    // �������һ������,��������, ֻ�����ں�֧����ϵͳʱ����, ����ֻ�Ƿ��ش���
                    // ���ô�����Ժ���
                    xfrm_tmpl_sort(stp, tpp, xfrm_nr, family);
                    tpp = stp;
                }
                // ����������ģ���Ƿ�OK
                for (i = xfrm_nr-1, k = 0; i >= 0; i--)
                {
                    // ע��k��������, Ҳ�����ֵ, k��ʼ��Ϊ0
                    // ����ֵ���ڵ���0��ʾ���ԺϷ�����
                    k = xfrm_policy_ok(tpp[i], sp, k, family);
                    if (k < 0)
                    {
                        if (k < -1) 
                            xerr_idx = -(2+k);
                        goto reject;
                    }
                }
                // ���ڷǴ���ģʽ�Ĳ���, ����
                if (secpath_has_nontransport(sp, k, &xerr_idx))
                    goto reject;
                xfrm_pols_put(pols, npols);
                return 1;
            }
            // ����, ����0��ʾ��鲻ͨ��
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
                // ����Ǵ���ģʽ, ֱ�ӷ���
                if (tmpl->mode == XFRM_MODE_TRANSPORT)
                    return start;
            }
            else
                start = -1;
            for (; idx < sp->len; idx++)
            {
                // sp->xvec��xfrm״̬
                // �����ȫ·����ģ��ƥ��,��������λ��
                if (xfrm_state_ok(tmpl,
                                  sp->xvec[idx], family))
                    return  ++idx;
                // �����ȫ·���е�SA���Ǵ���ģʽ,���ش���
                if (sp->xvec[idx]->props.mode != XFRM_MODE_TRANSPORT)
                {
                    if (start == -1)
                        start = -2-idx;
                    break;
                }
            }
            return start;
        }
    5.7 ��ȫ����·�ɲ���
        xfrm_lookup�����Ǹ��ǳ���Ҫ�ĺ���, �������ݰ�ȫ���Թ������ݰ���·��������,
        ��·��������ӳ�˶����ݰ�����IPSEC��װ�Ķ��εĴ���, ÿ��װһ��, ������һ��·����.
        �ú�����·�ɲ��Һ���ip_route_output_flow()����, ��Ե���ת���򷢳������ݰ�.
        // ����0��ʾ����, ������ʾʧ��
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
            // ��ʼ���������
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
                // �����sock�ж����˰�ȫ����, ���Ҹ�sock��صĲ���
                // һ��socket�İ�ȫ���Կ�ͨ��setsockopt()����, socketѡ��Ϊ
                // IP_IPSEC_POLICY��IP_XFRM_POLICY(net/ipv4/ip_sockglue.c)
                policy = xfrm_sk_policy_lookup(sk, XFRM_POLICY_OUT, fl);
                if (IS_ERR(policy))
                    return PTR_ERR(policy);
            }
            if (!policy)
            {
                // û�ҵ�sock������İ�ȫ����
                // �����ʼ·���������˷�IPSEC��־��û�з�������İ�ȫ����, ֱ�ӷ���
                if ((dst_orig->flags & DST_NOXFRM) ||
                    !xfrm_policy_count[XFRM_POLICY_OUT])
                    return 0;
                // ����·����Ϣ, ���û�оʹ���·��, xfrm_policy_lookup()������Ϊ�������ݸ�
                // flow_cache_lookup()����, ���Һ͸�·�ɶ�Ӧ�İ�ȫ����
                policy = flow_cache_lookup(fl, dst_orig->ops->family,
                                           dir, xfrm_policy_lookup);
                if (IS_ERR(policy))
                    return PTR_ERR(policy);
            }
            // �Ҳ������ԵĻ�����, ������ͨ����ͨ·����
            if (!policy)
                return 0;
            // �����Ǵ��ڰ�ȫ���Ե����, Ҫ�Ըð�������ȫ·������
            // ��ʼ·�ɵ�Э����
            family = dst_orig->ops->family;
            // ��ȫ�������ʹ��ʱ��
            policy->curlft.use_time = (unsigned long)xtime.tv_sec;
            // ���ҵ��Ĳ�����Ϊ��������ĵ�һ��
            pols[0] = policy;
            npols ++;
            xfrm_nr += pols[0]->xfrm_nr;
            // ���ݲ��Բ������������ش���, ֻ���������: ������ͨ��
            switch (policy->action)
            {
                case XFRM_POLICY_BLOCK:
                    // ���������ݰ�, ���ش���
                    err = -EPERM;
                    goto error;
                case XFRM_POLICY_ALLOW:
                    // ����ð�ͨ��, ������Ҫ�Ըð�����IPSEC����
                    #ifndef CONFIG_XFRM_SUB_POLICY
                        // ���Ӳ��Բ�������
                        if
                        (policy->xfrm_nr == 0)
                        {
                            xfrm_pol_put(policy);
                            return 0;
                        }
                    #endif
                    // �����Ƿ��Ѿ����ڰ�ȫ·��, bundle�������Ϊ������ȫ����İ�ȫ·��, ���ݰ��߸�·��
                    // ���ǽ���ĳ�ְ�ȫ��װ, ����ͨ·����һ��, �ù��İ�ȫ·��Ҳ����������
                    dst = xfrm_find_bundle(fl, policy, family);
                    if (IS_ERR(dst))
                    {
                        err = PTR_ERR(dst);
                        goto error;
                    }
                    // ����ҵ���ȫ·��, �˳�switch
                    if (dst)
                        break;
                    #ifdef CONFIG_XFRM_SUB_POLICY
                        // ���Ӳ��Բ���, �����ǷǱ�׼IPSEC,����
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
                    // û�ҵ���ȫ·��, ׼�������µ�·����
                    // ���ò���, ���Ȳ����������SA(xfrm_state)������xfrm��, nxΪSA����
                    nx = xfrm_tmpl_resolve(pols, npols, fl, xfrm, family);
                    if (unlikely(nx<0))
                    {
                        // nx<0��ʾʧ��, û�ҵ�SA
                        // �������-EAGAIN��ʾ�Ѿ�֪ͨ�û��ռ��IKE����Э���µ�SA��,
                        // Ŀǰֻ������ACQUIRE���͵�xfrm_state
                        err = nx;
                        if (err == -EAGAIN && flags)
                        {
                            // ���̽�������״̬
                            DECLARE_WAITQUEUE(wait, current);
                            add_wait_queue(&km_waitq, &wait);
                            set_current_state(TASK_INTERRUPTIBLE);
                            schedule();
                            set_current_state(TASK_RUNNING);
                            remove_wait_queue(&km_waitq, &wait);
                            // �������, ���½���SA
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
                        // nx==0��ʾ�����ǲ���Ҫ����IPSEC�����, ����
                        xfrm_pols_put(pols, npols);
                        return 0;
                    }
                    // �����ʼ·��
                    dst = dst_orig;
                    // �����µİ�ȫ·��, ����0 ��ʾ�ɹ�, ʧ�ܷ��ظ���
                    // dst�ڳɹ�����ʱ���氲ȫ·����, ÿ��SA�����Ӧһ����ȫ·��, ��Щ��ȫ·��ͨ��
                    // ·�����е�child����Ϊһ������, �����Ϳ��Զ����ݰ����������任, ����ѹ��,
                    // ��ESP��װ, ��AH��װ��.
                    // ·��������Ĺ����Э�������, ���������н��ܾ���Э�����е�ʵ��ʱ����ϸ����
                    // ���������·����ľ���ṹ���
                    err = xfrm_bundle_create(policy, xfrm, nx, fl, &dst, family);
                    if (unlikely(err))
                    {
                        // ʧ�ܵĻ��ͷŸջ�ȡ��SA
                        int i;
                        for (i=0; i<nx; i++) 
                            xfrm_state_put(xfrm[i]);
                        goto error;
                    }
                    // ������в��Ե�dead״̬
                    for (pi = 0; pi < npols; pi++)
                    {
                        read_lock_bh(&pols[pi]->lock);
                        pol_dead |= pols[pi]->dead;
                        read_unlock_bh(&pols[pi]->lock);
                    }
                    write_lock_bh(&policy->lock);
                    // ����в�����dead���ȡ�İ�ȫ·����������, �ͷŰ�ȫ·��
                    if (unlikely(pol_dead ||
                                 stale_bundle(dst)))
                    {
                        write_unlock_bh(&policy->lock);
                        if (dst)
                            dst_free(dst);
                        err = -EHOSTUNREACH;
                        goto error;
                    }
                    // ����ȫ·�ɼ��뵽���Ե�·��������ͷ, ����������NULL��β�ĵ�������
                    // ����һ�������Ӧ��ֻ��һ��Ԫ��
                    dst->next = policy->bundles;
                    policy->bundles = dst;
                    dst_hold(dst);
                    write_unlock_bh(&policy->lock);
            }
            // ����ȫ������Ϊ
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
        ��������xfrm_lookup���õ�������bundle�Ĳ�������:
        ���Һʹ���, ����ʹ���˵�ַ����, �Ǻ�Э������ص�,
        ��˾���ʵ�����ڸ�Э������ʵ�ֵ�, �ں��������н���Э�����е�xfrmʵ��ʱ����ϸ����.
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
        // ���Խ���, ����SA
        static int xfrm_tmpl_resolve( struct xfrm_policy **pols, 
                                      int npols, struct
                                      flowi *fl,
                                      struct
                                      xfrm_state **xfrm,
                                      unsigned
                                      short family)
        {
            struct xfrm_state *tp[XFRM_MAX_DEPTH];
            // npols > 1�Ƕ������Ӳ��Ե����, ��ʱ��tp���鱣���ҵ���SA,
            ��û������ԭ��������
            // ������Ϊʲô��ô��
            struct xfrm_state **tpp = (npols > 1) ? tp : xfrm;
            int cnx = 0;
            int error;
            int ret;
            int i;
            // ��������, һ�������npols��ʵֻ��1
            for (i = 0; i < npols; i++)
            {
                // ��鱣��SA�Ļ������Ƿ񻹹���
                if (cnx + pols[i]->xfrm_nr >= XFRM_MAX_DEPTH)
                {
                    error = -ENOBUFS;
                    goto fail;
                }
                // Э��һ������ģ��
                ret =  xfrm_tmpl_resolve_one(pols[i], fl, &tpp[cnx], family);
                if (ret < 0)
                {
                    error = ret;
                    goto fail;
                }
                else
                    cnx += ret;
            }
            // ������ԵĻ����ҵ���SA����, ��û�����Ӳ��Ե�������Ǹ��պ���
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
            // �����ṹ�л�ȡ��ַ��Ϣ
            xfrm_address_t *daddr = xfrm_flowi_daddr(fl,
                                    family);
            xfrm_address_t *saddr = xfrm_flowi_saddr(fl,
                                    family);
            xfrm_address_t tmp;
            // ���������е�����SA
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
                    // �����ͨ��ģʽ, ������ⲿIPͷ, �ڲ�IPͷ����װ���ڲ�, ��˵�ַ��Ϣʹ���ⲿ��ַ
                    // �����Ե�SAģ���еĵ�ַ��Ϣ
                    remote =
                        &tmpl->id.daddr;
                    local =
                        &tmpl->saddr;
                    // ���local��ַû����, ѡȡ��Դ��ַ��Ϊ���ص�ַ, ѡȡ������Э������ص�
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
                // ���ݵ�ַ,��,���Ե��²���SA(xfrm_state),����Ҳ����ֳɵĻ�֪ͨIKE�������Э��
                // �����µ�SA, �����ɿ���SAǰ�ȷ���ACQUIRE���͵�SA, ��ǰһƪ����
                x = xfrm_state_find(remote, local, fl, tmpl, policy, &error, family);
                if (x && x->km.state == XFRM_STATE_VALID)
                {
                    // ���SA�ǺϷ�, ����
                    xfrm[nx++] = x;
                    daddr = remote;
                    saddr =  local;
                    continue;
                }
                if (x)
                {
                    // x���ڵ�����VALID��, ֻҪ������, Ӧ����ACQUIRE���͵�, ��IKE����Э�̽��, ����-EAGAIN
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
        ����·�ɴ�������ں������IPSEC���ķ�������ʱ�����·�ɴ������, �Ӷ��˽ⰲȫ·�ɵ�����.
    5.8 ���HASH���С
        �ı����״̬�����ͨ������������ʵ�ֵ�, ��xfrm_state����
        ��������:
        static DECLARE_WORK(xfrm_hash_work, xfrm_hash_resize, NULL);
        // ����HASH���С
        static void xfrm_hash_resize(void *__unused)
        {
            int dir, total;
            mutex_lock(&hash_resize_mutex);
            total = 0;
            // ע����Զ���˫���
            for (dir = 0; dir < XFRM_POLICY_MAX * 2; dir++)
            {
                // ��Ŀ�ĵ�ַ����HASH������: �����Ҫ����HASH���С, �޸�֮
                if (xfrm_bydst_should_resize(dir, &total))
                    xfrm_bydst_resize(dir);
            }
            // �������Ž���HASH���������
            if (xfrm_byidx_should_resize(total))
                xfrm_byidx_resize(total);
            mutex_unlock(&hash_resize_mutex);
        }
        // ��鰴Ŀ�ĵ�ַHASH��HASH����
        static inline int xfrm_bydst_should_resize(int dir, int
                *total)
        {
            // �÷����ǲ��Ե�����
            unsigned int cnt = xfrm_policy_count[dir];
            // �÷����ǲ��Ե�����
            unsigned int hmask = xfrm_policy_bydst[dir].hmask;
            // �ۼӲ�������
            if (total)
                *total += cnt;
            // ��������������ڲ���������, ��������
            if ((hmask + 1) < xfrm_policy_hashmax &&
                cnt > hmask)
                return 1;
            // ������
            return 0;
        }
        // ��鰴������HASH��HASH����
        static inline int xfrm_byidx_should_resize(int total)
        {
            unsigned int hmask = xfrm_idx_hmask;
            // ��������������ǰ������������, ��������
            if ((hmask + 1) < xfrm_policy_hashmax &&
                total > hmask)
                return 1;
            return 0;
        }
        // ���İ�Ŀ�ĵ�ַHASH��HASH�����С
        static void xfrm_bydst_resize(int dir)
        {
            // �÷����HASH������(���ֵ, һ����2^N-1)
            unsigned int hmask =
                xfrm_policy_bydst[dir].hmask;
            // ��HASH������(2^(N+1)-1)
            unsigned int nhashmask = xfrm_new_hash_mask(hmask);
            // ��HASH���С
            unsigned int nsize = (nhashmask + 1) *
                                 sizeof(struct hlist_head);
            // ��HAHS��
            struct hlist_head *odst = xfrm_policy_bydst[dir].table;
            // ��HASH��
            struct hlist_head *ndst = xfrm_hash_alloc(nsize);
            int i;
            // ��HASH��ռ���䲻����, ����
            if (!ndst)
                return;
            write_lock_bh(&xfrm_policy_lock);
            // �����в��Խڵ�ת����HASH��
            for (i = hmask; i >= 0; i--)
                xfrm_dst_hash_transfer(odst + i, ndst, nhashmask);
            // ��ȫ�ֱ���ֵ����Ϊ��HASH�����
            xfrm_policy_bydst[dir].table = ndst;
            xfrm_policy_bydst[dir].hmask = nhashmask;
            write_unlock_bh(&xfrm_policy_lock);
            // �ͷ���HASH�����
            xfrm_hash_free(odst, (hmask + 1) * sizeof(struct hlist_head));
        }
        // ���İ�������HASH��HASH�����С, ��������������
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
    5.9 �����Ѽ�
        �����Ѽ����ǲ��õİ�ȫ·����, �Ǻ�Э������ص�
        afinfo->garbage_collect =
            __xfrm_garbage_collect;
        // ����xfrm_prune_bundles()�����İ�װ����,������unused_bundle()��������
        static void __xfrm_garbage_collect(void)
        {
            xfrm_prune_bundles(unused_bundle);
        }
        // ɾ����ȫ·��
        static void xfrm_prune_bundles(int (*func)(struct dst_entry
                                       *))
        {
            // ��������
            struct dst_entry *gc_list = NULL;
            int dir;
            read_lock_bh(&xfrm_policy_lock);
            // ѭ�����з���
            for (dir = 0; dir <
                    XFRM_POLICY_MAX * 2; dir++)
            {
                struct xfrm_policy *pol;
                struct hlist_node *entry;
                struct hlist_head *table;
                int i;
                // ����inexact����
                hlist_for_each_entry(pol,
                                     entry,
                                     &xfrm_policy_inexact[dir], bydst)
                // ����ڵ�����������ɾ���ҽӵ���������
                prune_one_bundle(pol,
                                 func, &gc_list);
                // ����Ŀ�ĵ�ַHASH������
                table =
                    xfrm_policy_bydst[dir].table;
                for (i =
                            xfrm_policy_bydst[dir].hmask; i >= 0; i--)
                {
                    // ����ڵ�����������ɾ���ҽӵ���������
                    hlist_for_each_entry(pol,
                                         entry, table + i, bydst)
                    prune_one_bundle(pol,
                                     func, &gc_list);
                }
            }
            read_unlock_bh(&xfrm_policy_lock);
            // ����Ѽ���������, �ͷŰ�ȫ·��
            while (gc_list)
            {
                struct dst_entry *dst =
                            gc_list;
                gc_list =
                    dst->next;
                dst_free(dst);
            }
        }
        // û�õ�·��, ʹ����Ϊ0
        static int unused_bundle(struct dst_entry *dst)
        {
            return
                !atomic_read(&dst->__refcnt);
        }
        // ɾ������·��
        static void prune_one_bundle(struct xfrm_policy *pol, int
                                     (*func)(struct dst_entry *), struct dst_entry **gc_list_p)
        {
            struct dst_entry *dst, **dstp;
            // ����д��
            write_lock(&pol->lock);
            // ���Ե�·�����������
            dstp =
                &pol->bundles;
            // ��������
            while ((dst=*dstp) != NULL)
            {
                if (func(dst))
                {
                    // �����������, ���ڵ��������ɾ��, ��ӵ���������
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
    5.10 ����
        ��Щ������ǲ��Ե�ֱ�Ӵ�����, ����xfrm��һЩ��ش���, ֻ��Ҳ����xfrm_policy.c����.
        5.10.1 Э�鴦�����ʹ���
            xfrm_type�����������Э�鴦������, ��AH,ESP, IPCOMP, IPIP��
            // �Ǽ�Э�鴦������, ����0�ɹ�, ��0ʧ��
            int xfrm_register_type(struct xfrm_type *type, unsigned short
                                   family)
            {
                // �ҵ�Э������صĲ�����Ϣ�ṹ
                struct xfrm_policy_afinfo *afinfo =
                    xfrm_policy_lock_afinfo(family);
                struct xfrm_type **typemap;
                int err = 0;
                if (unlikely(afinfo == NULL))
                    return -EAFNOSUPPORT;
                // ������Ϣ�ṹ�е���������
                typemap = afinfo->type_map;
                // �����������ӦЭ���ӦԪ�طǿ�, ��ֵ, ����������
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
            // ���Э�鴦������, ����0�ɹ�, ��0ʧ��
            int xfrm_unregister_type(struct xfrm_type *type, unsigned short family)
            {
                // �ҵ�Э������صĲ�����Ϣ�ṹ
                struct xfrm_policy_afinfo *afinfo =
                    xfrm_policy_lock_afinfo(family);
                struct xfrm_type **typemap;
                int err = 0;
                if (unlikely(afinfo == NULL))
                    return -EAFNOSUPPORT;
                // ������Ϣ�ṹ�е���������
                typemap = afinfo->type_map;
                // �����������ӦЭ���ӦԪ�ص���Ҫɾ���Ľṹ, Ԫ�����, ����������
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
            // ����Э��ź�Э�����������
            struct xfrm_type *xfrm_get_type(u8 proto, unsigned short family)
            {
                struct xfrm_policy_afinfo *afinfo;
                struct xfrm_type **typemap;
                struct xfrm_type *type;
                int modload_attempted = 0;
                retry:
                    // �ҵ�Э������صĲ�����Ϣ�ṹ
                    afinfo = xfrm_policy_get_afinfo(family);
                    if (unlikely(afinfo == NULL))
                        return NULL;
                    // ������Ϣ�ṹ�е���������
                    typemap = afinfo->type_map;
                    // �����ж�Ӧָ��Э���Ԫ��
                    type = typemap[proto];
                    // ����typeģ���ʹ�ü���
                    if (unlikely(type
                                 &&
                                 !try_module_get(type->owner)))
                        type = NULL;
                    // �����ǰtypeΪ��, �����type���ں�ģ��, ���²���
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
            // �ͷ�����ģ��ʹ�ü���
            void xfrm_put_type(struct xfrm_type *type)
            {
                module_put(type->owner);
            }
        5.10.2 Э��ģʽ����
            ģʽĿǰ����ͨ���ʹ�������.
            // �Ǽ�ģʽ, ����0�ɹ�, ��0ʧ��
            int xfrm_register_mode(struct xfrm_mode *mode, int family)
            {
                struct xfrm_policy_afinfo *afinfo;
                struct xfrm_mode **modemap;
                int err;
                if (unlikely(mode->encap
                             >= XFRM_MODE_MAX))
                    return -EINVAL;
                // �ҵ�Э������صĲ�����Ϣ�ṹ
                afinfo = xfrm_policy_lock_afinfo(family);
                if (unlikely(afinfo == NULL))
                    return -EAFNOSUPPORT;
                err = -EEXIST;
                // ������Ϣ�ṹ�е�ģʽ����
                modemap = afinfo->mode_map;
                // ����Ԫ�طǿյĻ���ֵ, ���سɹ�
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
            // ���ģʽ, ����0�ɹ�, ��0ʧ��
            int xfrm_unregister_mode(struct xfrm_mode *mode, int family)
            {
                struct xfrm_policy_afinfo *afinfo;
                struct xfrm_mode **modemap;
                int err;
                if (unlikely(mode->encap
                             >= XFRM_MODE_MAX))
                    return -EINVAL;
                // �ҵ�Э������صĲ�����Ϣ�ṹ
                afinfo = xfrm_policy_lock_afinfo(family);
                if (unlikely(afinfo == NULL))
                    return -EAFNOSUPPORT;
                err = -ENOENT;
                // ������Ϣ�ṹ�е�ģʽ����
                modemap = afinfo->mode_map;
                // ����Ԫ�ص���Ҫ�����ģʽ, ���, ���سɹ�
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
            // ����ģʽ
            struct xfrm_mode *xfrm_get_mode(unsigned int encap, int family)
            {
                struct xfrm_policy_afinfo *afinfo;
                struct xfrm_mode *mode;
                int modload_attempted = 0;
                if (unlikely(encap >=
                             XFRM_MODE_MAX))
                    return NULL;
                retry:
                    // �ҵ�Э������صĲ�����Ϣ�ṹ
                    afinfo = xfrm_policy_get_afinfo(family);
                    if (unlikely(afinfo == NULL))
                        return NULL;
                    // ������Ϣ�ṹ�е�ģʽ����
                    mode =
                        afinfo->mode_map[encap];
                    // ����ģʽģ���ʹ�ü���
                    if (unlikely(mode
                                 &&
                                 !try_module_get(mode->owner)))
                        mode = NULL;
                    // �����ǰģʽΪ��, �����ģʽ��Ӧ���ں�ģ��, ���²���
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
            // �ͷ�ģʽģ��ʹ�ü���
            void xfrm_put_mode(struct xfrm_mode *mode)
            {
                module_put(mode->owner);
            }
        5.10.3 Э����Ϣ����
            // �Ǽ�Э����Ϣ�ṹ
            int xfrm_policy_register_afinfo(struct xfrm_policy_afinfo *afinfo)
            {
                int err = 0;
                if (unlikely(afinfo == NULL))
                    return -EINVAL;
                if (unlikely(afinfo->family
                             >= NPROTO))
                    return -EAFNOSUPPORT;
                write_lock_bh(&xfrm_policy_afinfo_lock);
                // �����еĶ�ӦЭ���Э����Ϣ�ṹԪ��Ӧ��Ϊ��
                if
                (unlikely(xfrm_policy_afinfo[afinfo->family] !=
                          NULL))
                    err = -ENOBUFS;
                else
                {
                    // ��ȫ·�ɲ����ṹ
                    struct dst_ops *dst_ops =
                                afinfo->dst_ops;
                    // ��ȫ·�ɲ����ṹ�Ĳ����Ͳ���������ֵ
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
                    // �����еĶ�ӦЭ���Э����Ϣ�ṹԪ����ΪЭ����Ϣ�ṹ
                    xfrm_policy_afinfo[afinfo->family]
                    = afinfo;
                }
                write_unlock_bh(&xfrm_policy_afinfo_lock);
                return err;
            }
            EXPORT_SYMBOL(xfrm_policy_register_afinfo);
            // ���Э����Ϣ�ṹ
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
                    // �����е�Э����Ϣ�ṹ����ָ������Ϣ�ṹ
                    if
                    (unlikely(xfrm_policy_afinfo[afinfo->family] !=
                              afinfo))
                        err =
                            -EINVAL;
                    else
                    {
                        // ���Э����Ϣ����Ԫ�غ�·�ɲ����ṹ����
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
            // ����Э����Ϣ�ṹ, �Ӷ���
            static struct xfrm_policy_afinfo *xfrm_policy_get_afinfo(unsigned short family)
            {
                struct xfrm_policy_afinfo *afinfo;
                if (unlikely(family >=
                             NPROTO))
                    return NULL;
                read_lock(&xfrm_policy_afinfo_lock);
                // ��ȡָ��Э��λ�ô���Э����Ϣ�ṹ
                afinfo = xfrm_policy_afinfo[family];
                // �����Э����Ϣ�ṹ������, ����
                if (unlikely(!afinfo))
                    read_unlock(&xfrm_policy_afinfo_lock);
                return afinfo;
            }
            // �ͷ�Э����Ϣ�ṹ, �����
            static void xfrm_policy_put_afinfo(struct xfrm_policy_afinfo *afinfo)
            {
                read_unlock(&xfrm_policy_afinfo_lock);
            }
            // Э����Ϣ�ṹ��д��, ����ָ����Э����Ϣ�ṹ, ����ʱ����NULL
            static struct xfrm_policy_afinfo *xfrm_policy_lock_afinfo(unsigned int family)
            {
                struct xfrm_policy_afinfo *afinfo;
                if (unlikely(family >=
                             NPROTO))
                    return NULL;
                write_lock_bh(&xfrm_policy_afinfo_lock);
                // ��ȡָ��Э��λ�ô���Э����Ϣ�ṹ
                afinfo = xfrm_policy_afinfo[family];
                // �����Э����Ϣ�ṹ������, ����
                if (unlikely(!afinfo))
                    write_unlock_bh(&xfrm_policy_afinfo_lock);
                return afinfo;
            }
            // Э����Ϣ�ṹ��д��
            static void xfrm_policy_unlock_afinfo(struct xfrm_policy_afinfo *afinfo)
            {
                write_unlock_bh(&xfrm_policy_afinfo_lock);
            }
        5.10.4 �����ص�
            // ����֪ͨ�ṹ
            static struct notifier_block xfrm_dev_notifier =
            {
                xfrm_dev_event,
                NULL,
                0
            };
            // �ص�����
            static int xfrm_dev_event(struct notifier_block *this, unsigned
                                      long event, void *ptr)
            {
                switch (event)
                {
                    // ��ֻ��Ӧ����ͣ�¼�, ɾ����������ص����а�ȫ·����
                case NETDEV_DOWN:
                    xfrm_flush_bundles();
                }
                return NOTIFY_DONE;
            }
            static int xfrm_flush_bundles(void)
            {
                // Ҳ��ʹ��xfrm_prune_bundles()��������ɾ������
                // ����������stale_bundle
                xfrm_prune_bundles(stale_bundle);
                return 0;
            }
            // �жϰ�ȫ·�����Ƿ����
            // ����1��ʾ������, 0��ʾ����
            static int stale_bundle(struct dst_entry *dst)
            {
                return !xfrm_bundle_ok(NULL, (struct xfrm_dst
                                              *)dst, NULL, AF_UNSPEC, 0);
            }
            // ����0��ʾ������, 1��ʾ����
            int xfrm_bundle_ok(struct xfrm_policy *pol, struct xfrm_dst
                               *first,
                               struct flowi *fl, int family,
                               int strict)
            {
                struct dst_entry *dst =
                            &first->u.dst;
                struct xfrm_dst *last;
                u32 mtu;
                // ���·����
                if (!dst_check(dst->path, ((struct
                                            xfrm_dst *)dst)->path_cookie) ||
                        // ��������Ƿ�������
                        (dst->dev &&
                         !netif_running(dst->dev)))
                    return 0;
                last = NULL;
                do
                {
                    // ��ȫ·��
                    struct xfrm_dst *xdst = (struct
                                             xfrm_dst *)dst;
                    // ���SAѡ�����Ƿ�ƥ�����ṹ
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
                    // ���SA״̬�Ƿ�Ϸ�
                    if
                    (dst->xfrm->km.state !=
                            XFRM_STATE_VALID)
                        return
                            0;
                    if (xdst->genid
                            != dst->xfrm->genid)
                        return
                            0;
                    // �ϸ���ʱ, ����ͨ��ģʽ�µ�SA��ַ�����ṹ�����Ƿ�ƥ��
                    if (strict
                            && fl
                            &&
                            dst->xfrm->props.mode !=
                            XFRM_MODE_TUNNEL &&
                            !xfrm_state_addr_flow_check(dst->xfrm, fl,
                                                        family))
                        return
                            0;
                    // ��·�����MTU
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
                    // ͨ��·�ɼ��
                    if
                    (!dst_check(xdst->route,
                                xdst->route_cookie))
                        return
                            0;
                    // ��ȫ·����ص���ͨ·�ɵ�MTU
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
                    // ������ȫ·������
                    dst =
                        dst->child;
                }
                while (dst->xfrm);
                // last�����һ������·�ɺ���ͨ·�ɵ�MTU��ͬ�İ�ȫ·��, һ�㶼����ͬ��
                if (likely(!last))
                    return 1;
                // ������·�����е�MTU
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
    5.11 С��
        xfrm_policy��غ����ĵ��ñ����ù�ϵ�����¼򵥱�ʾ:
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
6. XFRM����������
    6.1 HASH����
        ����HASHֵ�ļ��㷽����Ҫ��net/xfrm/xfrm_hash.h�ж���:
        // IPV4��ַHASH
        static inline unsigned int __xfrm4_addr_hash(xfrm_address_t *addr)
        {
            // ���ǵ�ַ����
            return ntohl(addr->a4);
        }
        // IPV6��ַHASH
        static inline unsigned int __xfrm6_addr_hash(xfrm_address_t *addr)
        {
            // ȡ��2��32λ�����
            return ntohl(addr->a6[2] ^ addr->a6[3]);
        }
        // IPV4Դ,Ŀ�ĵ�ַHASH
        static inline unsigned int __xfrm4_daddr_saddr_hash(xfrm_address_t *daddr, xfrm_address_t *saddr)
        {
            // ��������ַ���
            return ntohl(daddr->a4 ^ saddr->a4);
        }
        // IPV4Դ,Ŀ�ĵ�ַHASH
        static inline unsigned int __xfrm6_daddr_saddr_hash(xfrm_address_t *daddr, xfrm_address_t *saddr)
        {
            // ����V6��ַ��ȡ��2��32λ�����
            return ntohl(daddr->a6[2] ^ daddr->a6[3] ^
                         saddr->a6[2] ^ saddr->a6[3]);
        }
        // Ŀ�ĵ�ַHASH
        static inline unsigned int __xfrm_dst_hash(xfrm_address_t *daddr, xfrm_address_t *saddr,
                                                    u32 reqid, unsigned short family,
                                                    unsigned int hmask)
        {
            // Э���������ID���
            unsigned int h = family ^ reqid;
            switch (family)
            {
            // HASHֵ�ٺ�ԴĿ�ĵ�ַHASH����������
            case AF_INET:
                h ^= __xfrm4_daddr_saddr_hash(daddr, saddr);
                break;
            case AF_INET6:
                h ^= __xfrm6_daddr_saddr_hash(daddr, saddr);
                break;
            }
            // ��HASH����ߵ�16λ�����16λ,��16λ����, Ȼ����HASH��������
            return (h ^ (h >> 16)) & hmask;
        }
        // Դ��ַHASH, ֻ��û������ID��, ����HASH���̺�������ͬ
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
        // ����SPI����HASHֵ
        static inline unsigned int
        __xfrm_spi_hash(xfrm_address_t *daddr, __be32 spi, u8 proto, unsigned short family,
                        unsigned int hmask)
        {
            // �Ƚ�SPI��Э��������
            unsigned int h = (__force u32)spi ^ proto;
            switch (family)
            {
            // HASHֵ�ٺ�Ŀ�ĵ�ַ���е�һ��ַHASHֵ���
            case AF_INET:
                h ^= __xfrm4_addr_hash(daddr);
                break;
            case AF_INET6:
                h ^= __xfrm6_addr_hash(daddr);
                break;
            }
            // HASHֵ�ٺͱ���ĸ�22λ, ��12λ�����ٺ���������
            return (h ^ (h >> 10) ^ (h >> 20)) & hmask;
        }
        // ������HASH
        static inline unsigned int __idx_hash(u32 index, unsigned int hmask)
        {
            // ��24λ�͸�24λ���, ��8λ����, �ٺ���������
            return (index ^ (index >> 8)) & hmask;
        }
        // ѡ����HASH
        static inline unsigned int __sel_hash(struct xfrm_selector *sel, unsigned short family, unsigned int hmask)
        {
            // ��ǰԴ��Ŀ�ĵ�ַ
            xfrm_address_t *daddr = &sel->daddr;
            xfrm_address_t *saddr = &sel->saddr;
            unsigned int h = 0;
            switch (family)
            {
                // ��Դ,Ŀ�ĵ�ַͬʱ����HASH
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
            // ��16λ���16λ���,��16λ����
            h ^= (h >> 16);
            // ����������, ��ʵHASHֵ�в���Э��������, ��Ϊ��ַ����Ͱ�����
            return h & hmask;
        }
        // ��ַHASH
        static inline unsigned int __addr_hash(xfrm_address_t *daddr, xfrm_address_t *saddr, unsigned short family, unsigned int hmask)
        {
            unsigned int h = 0;
            switch (family)
            {
            // ��Դ,Ŀ�ĵ�ַͬʱ����HASH
            case AF_INET:
                h = __xfrm4_daddr_saddr_hash(daddr, saddr);
                break;
            case AF_INET6:
                h = __xfrm6_daddr_saddr_hash(daddr, saddr);
                break;
            };
            // ��16λ���16λ���,��16λ����
            h ^= (h >> 16);
            // ����������
            return h & hmask;
        }
        ��net/xfrm/xfrm_hash.c �ļ��ж�����HASH��ķ�����ͷź���:
        struct hlist_head *xfrm_hash_alloc(unsigned int sz)
        {
            struct hlist_head *n;
            // ����HASH���Сѡ����ʵķ��䷽��
            // ��С������PAGE_SIZE, ��kmalloc����
            if (sz <= PAGE_SIZE)
                n = kmalloc(sz, GFP_KERNEL);
            // �������ں˶���NUMA��IA64����vmalloc����
            else if (hashdist)
                n = __vmalloc(sz, GFP_KERNEL, PAGE_KERNEL);
            else
            // �������͵��ں���get_free_page����
                n = (struct hlist_head *)
                    __get_free_pages(GFP_KERNEL, get_order(sz));
            // �ռ�����
            if (n)
                memset(n, 0, sz);
            return n;
        }
        // �ͷ�HASH��ռ�
        void xfrm_hash_free(struct hlist_head *n, unsigned int sz)
        {
            if (sz <= PAGE_SIZE)
                kfree(n);
            else if (hashdist)
                vfree(n);
            else
                free_pages((unsigned long)n, get_order(sz));
        }
    6.2 �㷨����
        IPSEC�������õ�����֤, ����, ѹ�����㷨����ʵ������cryptoĿ¼��, ����xfrm��ֻ�Ƕ�����Щ�㷨��˵��, ��ʾ������֧����Щ�㷨, ��ʹ��ʱ��̽����Щ�㷨�Ƿ����ں��д��ڴӶ�ȷ����ʹ�õ��㷨.
        �����㷨�����ݽṹ����:
        /* include/net/xfrm.h */
        // ��֤�㷨����
        struct xfrm_algo_auth_info
        {
            u16 icv_truncbits; // ��ʼ�����ض�λ��
            u16 icv_fullbits;  // ��ʼ�����ܵ�λ��
        };
        // �����㷨����
        struct xfrm_algo_encr_info
        {
            u16 blockbits;  // ��λ��
            u16 defkeybits; // ��Կ����λ��
        };
        // ѹ���㷨����
        struct xfrm_algo_comp_info
        {
            u16 threshold;  // ��ֵ
        };
        // xfrm�㷨����
        struct xfrm_algo_desc
        {
            char *name;  // ����
            char *compat; // ������д
            u8 available:1; // �㷨�Ƿ����(�Ƿ����ں���)
            union
            {
                struct xfrm_algo_auth_info auth;
                struct xfrm_algo_encr_info encr;
                struct xfrm_algo_comp_info comp;
            } uinfo; // �㷨��Ϣ����
            struct sadb_alg desc; // ͨ���㷨����
        };
        6.2.1 ��֤�㷨
            ���õ���֤�㷨ͨ�����������������, 
            ����NULL, MD5, SHA1, SHA256, RIPEMD160����֤�㷨:
            static struct xfrm_algo_desc aalg_list[] =
            {
                ......
                {
                    .name = "hmac(sha1)",
                    .compat = "sha1",
                    .uinfo = {
                        .auth = {
                            .icv_truncbits = 96,// 96λ�ض�
                            .icv_fullbits = 160, // �ܹ�160λ
                        }
                    },
                    .desc = { // ���Ƕ�SHA1��֤�㷨�ı�׼��������
                        .sadb_alg_id = SADB_AALG_SHA1HMAC, // �㷨IDֵ
                        .sadb_alg_ivlen = 0,
                        .sadb_alg_minbits = 160,
                        .sadb_alg_maxbits = 160
                    }
                },
                ......
            }
            ��ز�������:
                // ͨ���㷨ID������֤�㷨
                struct xfrm_algo_desc *xfrm_aalg_get_byid(int alg_id)
                {
                    int i;
                    // ������֤����
                    for (i = 0; i < aalg_entries(); i++)
                    {
                        // ���Һ�ָ���㷨ID��ͬ���㷨
                        if (aalg_list[i].desc.sadb_alg_id == alg_id)
                        {
                            // �����㷨�Ƿ����
                            if (aalg_list[i].available)
                                return &aalg_list[i];
                            else
                                break;
                        }
                    }
                    return NULL;
                }
                EXPORT_SYMBOL_GPL(xfrm_aalg_get_byid);
                // ͳ�ƿ��õ���֤�㷨����, ����available����֤�㷨�����ۼ�
                int xfrm_count_auth_supported(void)
                {
                    int i, n;
                    for (i = 0, n = 0; i < aalg_entries(); i++)
                        if (aalg_list[i].available)
                            n++;
                    return n;
                }
                EXPORT_SYMBOL_GPL(xfrm_count_auth_supported);
        6.2.2 �����㷨
            ���õ���֤�㷨ͨ�����������������, 
            ����NULL, DES, 3DES, CAST, AES, BLOWFISH, TWOFISH, SERPENT�ȼ����㷨:
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
            ��ز�������:
                // ͨ���㷨ID���Ҽ����㷨, ����֤�㷨��������
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
                // ͳ�ƿ��õļ����㷨����, ����available�ļ����㷨�����ۼ�
                int xfrm_count_enc_supported(void)
                {
                    int i, n;
                    for (i = 0, n = 0; i < ealg_entries(); i++)
                        if (ealg_list[i].available)
                            n++;
                    return n;
                }
                EXPORT_SYMBOL_GPL(xfrm_count_enc_supported);
        6.2.3 ѹ���㷨
            ���õ�ѹ���㷨ͨ�����������������, ����DELFATE, LZS, LZJH��ѹ���㷨:
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
            ��ز�������:
                // ͨ���㷨ID���Ҽ����㷨, ����֤�㷨��������
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
        6.2.4 ͨ�����Ʋ����㷨
            // �������Ϊ�㷨����, ����Ԫ�ظ���, ����, ����, ���ƺ��Ƿ�̽�����ں��д���
            static struct xfrm_algo_desc *xfrm_get_byname(struct xfrm_algo_desc *list,
                    int entries, u32 type, u32 mask,
                    char *name, int probe)
            {
                int i, status;
                if (!name)
                    return NULL;
                // ��������
                for (i = 0; i < entries; i++)
                {
                    // �Ƚ��㷨���ƻ���д�����Ƿ��ָ��������ͬ
                    if (strcmp(name, list[i].name) &&
                            (!list[i].compat || strcmp(name, list[i].compat)))
                        continue;
                    // �ҵ��㷨�ṹ
                    // ����㷨�Ƿ����ں˿���, ���õĻ��ɹ�����
                    if (list[i].available)
                        return &list[i];
                    // �������Ҫ̽��, �����ؿ�
                    if (!probe)
                        break;
                    // ��Ҫ̽���㷨�㷨�����ں�, ����crypto_has_alg()����̽��
                    // ����0��ʾʧ��, ��0��ʾ�ɹ�
                    status = crypto_has_alg(name, type, mask | CRYPTO_ALG_ASYNC);
                    if (!status)
                        break;
                    // �㷨����, ����
                    list[i].available = status;
                    return &list[i];
                }
                return NULL;
            }
            /* crypto/api.c */
            // �㷨̽��
            int crypto_has_alg(const char *name, u32 type, u32 mask)
            {
                int ret = 0;
                // ��������, ���ͺ�����̽���㷨ģ��
                struct crypto_alg *alg = crypto_alg_mod_lookup(name, type, mask);
                // ��ȷ�����ҵ�
                if (!IS_ERR(alg))
                {
                // ����ģ�����, ����1
                    crypto_mod_put(alg);
                    ret = 1;
                }
                return ret;
            }
            ����xfrm_get_byname()���ͨ�û�������, �������͵��㷨���Һ����ͺܼ���:
            // ͨ�����Ʋ�����֤�㷨
            struct xfrm_algo_desc *xfrm_aalg_get_byname(char *name, int probe)
            {
                return xfrm_get_byname(aalg_list, aalg_entries(),
                                       CRYPTO_ALG_TYPE_HASH, CRYPTO_ALG_TYPE_HASH_MASK,
                                       name, probe);
            }
            EXPORT_SYMBOL_GPL(xfrm_aalg_get_byname);
            // ͨ�����Ʋ��Ҽ����㷨
            struct xfrm_algo_desc *xfrm_ealg_get_byname(char *name, int probe)
            {
                return xfrm_get_byname(ealg_list, ealg_entries(),
                                       CRYPTO_ALG_TYPE_BLKCIPHER, CRYPTO_ALG_TYPE_MASK,
                                       name, probe);
            }
            EXPORT_SYMBOL_GPL(xfrm_ealg_get_byname);
            // ͨ�����Ʋ���ѹ���㷨
            struct xfrm_algo_desc *xfrm_calg_get_byname(char *name, int probe)
            {
                return xfrm_get_byname(calg_list, calg_entries(),
                                       CRYPTO_ALG_TYPE_COMPRESS, CRYPTO_ALG_TYPE_MASK,
                                       name, probe);
            }
            EXPORT_SYMBOL_GPL(xfrm_calg_get_byname);
            ������ͨ���������������㷨, ����ֱ�ӷ�����Ӧ����ָ��λ�õ��㷨:
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
        6.2.5 xfrm�㷨̽��
            �ú�����SA���е���ʱ��������鿴��ǰ�ں���֧�ֵĸ����㷨
            /*
            * Probe for the availability of crypto algorithms, and set the available
            * flag for any algorithms found on the system.  This is typically called by
            * pfkey during userspace SA add, update or register.
            */
            void xfrm_probe_algs(void)
            {
                // �ں˱��붨��CRYPTOѡ��, ������ǿպ�����
                #ifdef CONFIG_CRYPTO
                int i, status;
                BUG_ON(in_softirq());
                // ������֤�㷨����
                for (i = 0; i < aalg_entries(); i++)
                {
                    // �����㷨����ȷ����HASH�㷨�Ƿ����, ����0������, ��0����
                    status = crypto_has_hash(aalg_list[i].name, 0,
                                             CRYPTO_ALG_ASYNC);
                    // ���״̬��ԭ����״̬��ͬ, ����
                    if (aalg_list[i].available != status)
                        aalg_list[i].available = status;
                }
                // ���������㷨����
                for (i = 0; i < ealg_entries(); i++)
                {
                    // �����㷨����ȷ���ü����㷨�Ƿ����, ����0������, ��0����
                    status = crypto_has_blkcipher(ealg_list[i].name, 0,
                                                  CRYPTO_ALG_ASYNC);
                    // ���״̬��ԭ����״̬��ͬ, ����
                    if (ealg_list[i].available != status)
                        ealg_list[i].available = status;
                }
                // ����ѹ���㷨����
                for (i = 0; i < calg_entries(); i++)
                {
                    // �����㷨����ȷ����ѹ���㷨�Ƿ����, ����0������, ��0����
                    status = crypto_has_comp(calg_list[i].name, 0,
                                             CRYPTO_ALG_ASYNC);
                    // ���״̬��ԭ����״̬��ͬ, ����
                    if (calg_list[i].available != status)
                        calg_list[i].available = status;
                }
                #endif
            }
            EXPORT_SYMBOL_GPL(xfrm_probe_algs);
    6.3 ͨ��netlink�׽ӿڷ���xfrm
        ͨ��netlink�׽ӿڷ���xfrm�Ĵ�������net/xfrm/xfrm_user.c��, 
        �ṩ��Linux��ɫ�ķǱ�׼PF_KEY�ӿڵ�SA, SP���Ʒ���, 
        ����ɺ�PF_KEYһ�����ƹ���, 
        Ŀǰiproute2�е�ip�����������ӵ�xfrm�������ͨ������netlink�ӿ�����ɵ�,
        ��Ϊnetlink������ǰ�Ѿ����ܹ�, 
        xfrm�Ĳ����ֶ���һ����, ��˱��Ĳ��ٷ�����ʵ�ֹ���.
    6.4 xfrm_input
        ��net/xfrm/xfrm_input.c�ļ��ж����˹��ڰ�ȫ·��(struct sec_path)�ļ���������, 
        ���ڶ������IPSEC�����н������찲ȫ·��ʹ��.
        // �ͷŰ�ȫ·��
        void __secpath_destroy(struct sec_path *sp)
        {
            int i;
            // ���ٰ�ȫ·��������SA��ʹ�ü���
            for (i = 0; i < sp->len; i++)
                xfrm_state_put(sp->xvec[i]);
            // �ͷŰ�ȫ·���ռ�
            kmem_cache_free(secpath_cachep, sp);
        }
        EXPORT_SYMBOL(__secpath_destroy);
        // ��ȫ·������
        struct sec_path *secpath_dup(struct sec_path *src)
        {
            struct sec_path *sp;
            // �ȷ��䰲ȫ·���ṹ
            sp = kmem_cache_alloc(secpath_cachep, SLAB_ATOMIC);
            if (!sp)
                return NULL;
            sp->len = 0;
            if (src)
            {
                int i;
                // ���Դ��ȫ·���ṹ�ǿ�, ����ȫ�����Ƶ��½ṹ��
                memcpy(sp, src, sizeof(*sp));
                // ���Ӱ�ȫ·��������SA��ʹ�ü���
                for (i = 0; i < sp->len; i++)
                    xfrm_state_hold(sp->xvec[i]);
            }
            // ���ø����ü�����ʼֵλ1
            atomic_set(&sp->refcnt, 1);
            return sp;
        }
        EXPORT_SYMBOL(secpath_dup);
        /* Fetch spi and seq from ipsec header */
        // �����ݰ��н���SPI�����, ����ֵ���������
        int xfrm_parse_spi(struct sk_buff *skb, u8 nexthdr, __be32 *spi, __be32 *seq)
        {
            int offset, offset_seq;
            // ͨ��nexthdr�������ж�Э������, nexthdr��IPV6���˵��,
            // ��IPV4�о���IPͷ���Э���ֶ�
            // ���ݲ�ͬЭ��ȷ��������SPI�����к����������ʼ���ƫ��
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
                // ��Ӧѹ��Э�鵥������
                // ����ͷ׼����IPѹ��ͷ�ṹ����
                if (!pskb_may_pull(skb, sizeof(struct ip_comp_hdr)))
                    return -EINVAL;
                // SPIֵȡ��3,4�ֽڵ�����, ���Ϊ0
                *spi = htonl(ntohs(*(__be16*)(skb->h.raw + 2)));
                *seq = 0;
                return 0;
            default:
                return 1;
            }
            // ����ͷ׼��16�ֽڿռ�, ����ip_auth_hdr��ip_esp_hdr�ṹ��С����
            if (!pskb_may_pull(skb, 16))
                return -EINVAL;
            // ����ƫ�ƻ�ȡSPI�����, ע�����������ֵ
            *spi = *(__be32*)(skb->h.raw + offset);
            *seq = *(__be32*)(skb->h.raw + offset_seq);
            return 0;
        }
        EXPORT_SYMBOL(xfrm_parse_spi);         
7. IPV4�µ�xfrm֧�ִ���
    ��xfrm�и��ֺ͵�ַ��صĲ����Ǻ�Э������ص�,
    ����ⲿ�ֵľ���ʵ�־ͷ�����ص�Э����ʵ����,
    Ȼ��ͨ��״̬�Ͳ�����Ϣ�ṹ��ָ����ʵ�ʵĲ����У�
    ��ɶ���ͨ���ݰ���IPSEC��װ���IPSEC���Ľ��װ��
    7.1 IPV4�µ�xfrm����
        IPV4�µ�xfrm������net/ipv4/xfrm4_policy.c�ļ��ж���, ��Ҫ�Ƕ���IPV4�Ĳ�����Ϣ�ṹ:
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
        ��xfrm_policy_register_afinfo()������, 
        ��������struct xfrm_policy_afinfo�ṹ������������Ա����,
        ��Ϊ�⼸�������Ǻ�Э���޹ص�, �����ڵǼǺ����ж�����:
                afinfo->garbage_collect = __xfrm_garbage_collect;
        �ú����Ѿ��ڱ�ϵ�еĵ�3ƪ�н��ܹ���.
        �����ǽṹ�м��������Ķ���:
        // IPV4��·�ɲ���, ������ͨ��·�ɲ��ҷ���
        // ����0�ɹ�
        static int xfrm4_dst_lookup(struct xfrm_dst **dst, struct flowi *fl)
        {
            return __ip_route_output_key((struct rtable**)dst, fl);
        }
        // ���ҵ�ַ, �����������ͨ��ģʽ��, Դ��ַû��ȷָ��ʱ���õ�,���һ�ȡ
        // �ⲿͷ�е�Դ��ַ
        static int xfrm4_get_saddr(xfrm_address_t *saddr, xfrm_address_t *daddr)
        {
            struct rtable *rt;
            // ͨ�������ṹ����,���ڲ���·��
            struct flowi fl_tunnel =
            {
                .nl_u = {
                    .ip4_u = {
                        .daddr = daddr->a4,
                    },
                },
            };
            // ����Ŀ�ĵ�ַ��·��
            if (!xfrm4_dst_lookup((struct xfrm_dst **)&rt, &fl_tunnel))
            {
                // ���ҵ���·�����е�Դ��ַ��Ϊͨ��ģʽ�µ��ⲿԴ��ַ
                saddr->a4 = rt->rt_src;
                dst_release(&rt->u.dst);
                return 0;
            }
            return -EHOSTUNREACH;
        }
        // ���Ҳ����еİ�ȫ·��, �������������ṹ�Ķ���Ĳ���
        static struct dst_entry *
        __xfrm4_find_bundle(struct flowi *fl, struct xfrm_policy *policy)
        {
            struct dst_entry *dst;
            read_lock_bh(&policy->lock);
            // �������Եİ�ȫ·������
            for (dst = policy->bundles; dst; dst = dst->next)
            {
                struct xfrm_dst *xdst = (struct xfrm_dst*)dst;
                // �Ƚ�����λ��, Ŀ�ĵ�ַ, Դ��ַ, TOSֵ�Ƿ�ƥ��
                // ͬʱ���ð�ȫ·���Ƿ����
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
        // ����skb����, ������ṹ
        static void
        _decode_session4(struct sk_buff *skb, struct flowi *fl)
        {
            struct iphdr *iph = skb->nh.iph;
            // xprth��IPͷ����ϲ�Э��ͷ��ʼ
            u8 *xprth = skb->nh.raw + iph->ihl*4;
            // �Ƚ����ṹ����
            memset(fl, 0, sizeof(struct flowi));
            // ���ݰ����벻�Ƿ�Ƭ��
            if (!(iph->frag_off & htons(IP_MF | IP_OFFSET)))
            {
                switch (iph->protocol)
                {
                // ��UDP(17), TCP(6), SCTP(132)��DCCP(33)Э��, Ҫ��ȡԴ�˿ں�Ŀ�Ķ˿�
                // ͷ4�ֽ���Դ�˿ں�Ŀ�Ķ˿�
                case IPPROTO_UDP:
                case IPPROTO_TCP:
                case IPPROTO_SCTP:
                case IPPROTO_DCCP:
                    // Ҫ��skbԤ����IPͷ���ȼ�4�ֽڵĳ���, ��IP��dataӦ��ָ���������IPͷ
                    if (pskb_may_pull(skb, xprth + 4 - skb->data))
                    {
                        u16 *ports = (u16 *)xprth;
                        // ��ȡ�˿ڲ���
                        fl->fl_ip_sport = ports[0];
                        fl->fl_ip_dport = ports[1];
                    }
                    break;
                case IPPROTO_ICMP:
                    // ��ICMP(1)Э��Ҫ��ȡICMP�������ͺͱ���, 2�ֽ�
                    if (pskb_may_pull(skb, xprth + 2 - skb->data))
                    {
                        u8 *icmp = xprth;
                        fl->fl_icmp_type = icmp[0];
                        fl->fl_icmp_code = icmp[1];
                    }
                    break;
                case IPPROTO_ESP:
                    // ����ESP(50)Э��Ҫ��ȡ���е�SPIֵ, 4�ֽ�
                    if (pskb_may_pull(skb, xprth + 4 - skb->data))
                    {
                        __be32 *ehdr = (__be32 *)xprth;
                        fl->fl_ipsec_spi = ehdr[0];
                    }
                    break;
                case IPPROTO_AH:
                    // ����AH(51)Э��Ҫ��ȡ���е�SPIֵ, 4�ֽ�
                    if (pskb_may_pull(skb, xprth + 8 - skb->data))
                    {
                        __be32 *ah_hdr = (__be32*)xprth;
                        fl->fl_ipsec_spi = ah_hdr[1];
                    }
                    break;
                case IPPROTO_COMP:
                    // ����COMP(108)Э��Ҫ��ȡ����CPIֵ��ΪSPIֵ, 2�ֽ�
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
            // ���Э��,Դ��ַ,Ŀ�ĵ�ַ, TOS����
            fl->proto = iph->protocol;
            fl->fl4_dst = iph->daddr;
            fl->fl4_src = iph->saddr;
            fl->fl4_tos = iph->tos;
        }
        /* Allocate chain of dst_entry's, attach known xfrm's, calculate
         * all the metrics... Shortly, bundle a bundle.
         */
        // ������ȫ·��
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
            // ѭ������Ϊ������SA������, ÿ��SA��Ӧһ����ȫ·��, һ����ȫ·�ɶ�Ӧ�����ݰ���һ��
            // ����: ��ѹ��, ESP��װ, AH��װ��
            for (i = 0; i < nx; i++)
            {
                // ���䰲ȫ·��, ��ȫ·�ɵĲ����ṹ��xfrm4_dst_ops
                // ��Ϊ�����˺ܶ಻ͬ���͵�·��, ÿ��·�ɶ��и��ԵĲ����ṹ, �������ϲ����
                // ͳһ�Ľӿڽ���·�ɴ���
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
                    // ��һ��ѭ��
                    dst = dst1;
                else
                {
                    // ���·���İ�ȫ·����Ϊǰһ��·�ɵ�child
                    dst_prev->child = dst1;
                    dst1->flags |= DST_NOHASH;
                    dst_clone(dst1);
                }
                xdst = (struct xfrm_dst *)dst1;
                // ��ȫ·���б�����Ӧ����ͨ·��
                xdst->route = &rt->u.dst;
                xdst->genid = xfrm[i]->genid;
                // �½ڵ��next���Ͻڵ�
                dst1->next = dst_prev;
                // ����prev�ڵ�λ�½ڵ�
                dst_prev = dst1;
                if (xfrm[i]->props.mode != XFRM_MODE_TRANSPORT)
                {
                    remote = xfrm[i]->id.daddr.a4;
                    local  = xfrm[i]->props.saddr.a4;
                    tunnel = 1;
                }
                header_len += xfrm[i]->props.header_len;
                trailer_len += xfrm[i]->props.trailer_len;
                // �����ͨ��ģʽ, ��Ҫ���°����ⲿIPͷ, ��Ҫ����Ѱ���ⲿIPͷ��·��
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
            // �����½ڵ��childָ��������ͨ·��
            dst_prev->child = &rt->u.dst;
            // ����һ����ȫ·�ɵ�pathָ��������ͨ·��
            dst->path = &rt->u.dst;
            // �����ϰ�ȫ·�ɵ���ΪҪ���ص�·�ɽڵ�����ͷ
            *dst_p = dst;
            // dst���������½ڵ�
            dst = dst_prev;
            // prev����ָ�����ϰ�ȫ�ڵ�
            dst_prev = *dst_p;
            i = 0;
            /*
             Ϊ�����������Ĳ���, ��ͼ����ʾ. ����ѭ���γ�����ͼˮƽ�����һ������,
             �����е�����ߵ�·����ڵ�dstΪ���ϵİ�ȫ·����, 
             �·���İ�ȫ·����ͨ��child���ӳ�����, childͨ��nextָ���Ͻڵ�, 
             ���һ�������ݰ���װ���������ͨ·����. 
             ��ֱ�������������xfrm_lookup()���γɵ�, �Ƕ������ͬʱ�����õ����,
             һ������¾�ֻ��һ������, �����пɲ����Ƕ���Ե����.
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
            // �������ɵ�ÿ����ȫ·�������ṹ����
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
                // ע�ⰲȫ·�ɵ����������xfrm4_output, ���Ժ����·�ɹ���ʱҪ�õ�
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
            // ��ʼ��·�����MTUֵ
            xfrm_init_pmtu(dst);
            return 0;
            error:
                if (dst)
                    dst_free(dst);
                return err;
        }
        7.1.1 С��
            IPV4�Ĳ�����Ϣ�ṹ�е���س�Ա�����ı����ù�ϵ�����¼򵥱�ʾ:
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
    7.2 IPV4��ȫ·�ɲ���
        ·�ɲ��������ÿ�����͵�·�ɶ����һ�������ṹ, ���ϲ������˲�ͬ·�ɴ����ڲ��Ĵ�����, 
        ����IPSEC��IPV4��ȫ·��(xfrm_dst)�Ĳ����ṹ��������:
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
        ��xfrm_policy_register_afinfo()������, �������˰�ȫ·�ɲ����ṹ������������Ա����,
        ��Ϊ�⼸�������Ǻ�Э���޹ص�, �����ڵǼǺ����ж�����:
        dst_ops->kmem_cachep = xfrm_dst_cache;
        dst_ops->check = xfrm_dst_check;
        dst_ops->negative_advice = xfrm_negative_advice;
        dst_ops->link_failure = xfrm_link_failure;
        // ��ȫ·�������Ѽ�, ���ǵ��ð�ȫ������Ϣ�ṹ�������Ѽ�����
        static inline int xfrm4_garbage_collect(void)
        {
            xfrm4_policy_afinfo.garbage_collect();
            return (atomic_read(&xfrm4_dst_ops.entries) > xfrm4_dst_ops.gc_thresh*2);
        }
        // ����·�ɵ�MTU
        static void xfrm4_update_pmtu(struct dst_entry *dst, u32 mtu)
        {
            struct xfrm_dst *xdst = (struct xfrm_dst *)dst;
            struct dst_entry *path = xdst->route;
            // ���õ��ǰ�ȫ·�ɵ�ԭʼ��ͨ·�ɵ�MTU���²���
            path->ops->update_pmtu(path, mtu);
        }
        // �ͷŰ�ȫ·��
        static void xfrm4_dst_destroy(struct dst_entry *dst)
        {
            struct xfrm_dst *xdst = (struct xfrm_dst *)dst;
            // �ͷ�inet��������
            if (likely(xdst->u.rt.idev))
                in_dev_put(xdst->u.rt.idev);
            // �ͷŶԷ�IP������
            if (likely(xdst->u.rt.peer))
                inet_putpeer(xdst->u.rt.peer);
            // �ͷŰ�ȫ·��
            xfrm_dst_destroy(xdst);
        }
        static inline void xfrm_dst_destroy(struct xfrm_dst *xdst)
        {
            // �ͷźͰ�ȫ·����ص���ͨ·��
            dst_release(xdst->route);
            // �ͷ�SA
            if (likely(xdst->u.dst.xfrm))
                xfrm_state_put(xdst->u.dst.xfrm);
        }
        // ����downʱ�Ļص�����
        static void xfrm4_dst_ifdown(struct dst_entry *dst, struct net_device *dev,
                                     int unregister)
        {
            struct xfrm_dst *xdst;
            if (!unregister)
                return;
            xdst = (struct xfrm_dst *)dst;
            // �ð�ȫ·�ɶ�Ӧ�������ǵ�ǰͣ��������
            if (xdst->u.rt.idev->dev == dev)
            {
                struct in_device *loopback_idev = in_dev_get(&loopback_dev);
                BUG_ON(!loopback_idev);
                do
                {
                    // �ͷŰ�ȫ·������
                    in_dev_put(xdst->u.rt.idev);
                    // ��ȫ·��������������Ļػ�����
                    xdst->u.rt.idev = loopback_idev;
                    in_dev_hold(loopback_idev);
                    // ��·��
                    xdst = (struct xfrm_dst *)xdst->u.dst.child;
                }
                while (xdst->u.dst.xfrm);
                __in_dev_put(loopback_idev);
            }
            xfrm_dst_ifdown(dst, dev);
        }
    7.3 IPV4�µ�xfrm״̬
        IPV4�µ�xfrm״̬��net/ipv4/xfrm4_state.c�ļ��ж���, ��Ҫ�Ƕ���IPV4��״̬��Ϣ�ṹ:
        static struct xfrm_state_afinfo xfrm4_state_afinfo =
        {
            .family   = AF_INET,
            .init_flags  = xfrm4_init_flags,
            .init_tempsel  = __xfrm4_init_tempsel,
        };
        �ýṹ����IPV4��ֻ����������������:
        // ��ʼ��״̬��־
        static int xfrm4_init_flags(struct xfrm_state *x)
        {
            if (ipv4_config.no_pmtu_disc)
                x->props.flags |= XFRM_STATE_NOPMTUDISC;
            return 0;
        }
        // ��ʼ��ģ��ѡ����
        static void
        __xfrm4_init_tempsel(struct xfrm_state *x, struct flowi *fl,
                             struct xfrm_tmpl *tmpl,
                             xfrm_address_t *daddr, xfrm_address_t *saddr)
        {
            // ��дѡ������Ϣ
            // Դ��ַ
            x->sel.daddr.a4 = fl->fl4_dst;
            // Ŀ�ĵ�ַ
            x->sel.saddr.a4 = fl->fl4_src;
            // Ŀ�Ķ˿�, ����
            x->sel.dport = xfrm_flowi_dport(fl);
            x->sel.dport_mask = htons(0xffff);
            // Դ�˿�����
            x->sel.sport = xfrm_flowi_sport(fl);
            x->sel.sport_mask = htons(0xffff);
            // ԴĿ�ĵ�ַ����
            x->sel.prefixlen_d = 32;
            x->sel.prefixlen_s = 32;
            // Э��
            x->sel.proto = fl->proto;
            // ����λ��
            x->sel.ifindex = fl->oif;
            // ״̬IDֵ
            x->id = tmpl->id;
            if (x->id.daddr.a4 == 0)
                x->id.daddr.a4 = daddr->a4;
            // ֧�ֽṹ�еĲ���
            // Դ��ַ
            x->props.saddr = tmpl->saddr;
            if (x->props.saddr.a4 == 0)
                x->props.saddr.a4 = saddr->a4;
            // ģʽ
            x->props.mode = tmpl->mode;
            // ����ID
            x->props.reqid = tmpl->reqid;
            // Э����
            x->props.family = AF_INET;
        }
        7.3.1 С��
            IPV4��״̬��Ϣ�ṹ�е���س�Ա�����ı����ù�ϵ�����¼򵥱�ʾ:
            xfrm_init_state()
                -> afinfo->init_flags() == xfrm4_init_flags
            xfrm_state_find()
                -> xfrm_init_tempsel()
                    -> afinfo->init_tempsel() == __xfrm4_init_tempsel
    7.4 ģʽ
        xfrm4֧��3��ģʽ:
        ͨ��, �����BEETģʽ, �ֱ���xfrm4_mode_tunnel.c, xfrm4_mode_transport.c��xfrm4_mode_beet.c�ж���.
        ÿ��ģʽ��ͨ���ṹstruct xfrm_mode����:
            struct xfrm_mode
            {
                int (*input)(struct xfrm_state *x, struct sk_buff *skb);
                int (*output)(struct xfrm_state *x,struct sk_buff *skb);
                struct module *owner;
                unsigned int encap;
            };
        ����input���������ݽ���ʱ����, output�������ݷ���ʱ����, encap������ʾ�Ƿ��װ.
        7.4.1 ͨ��
            ͨ��ģʽͨ�����½ṹ����:
            /* net/ipv4/xfrm4_mode_transport.c */
            static struct xfrm_mode xfrm4_tunnel_mode =
            {
                .input = xfrm4_tunnel_input,
                .output = xfrm4_tunnel_output,
                .owner = THIS_MODULE,
                .encap = XFRM_MODE_TUNNEL,
            };
            // ͨ��ģʽ�µĽ��պ���, ���װ
            static int xfrm4_tunnel_input(struct xfrm_state *x, struct sk_buff *skb)
            {
                struct iphdr *iph = skb->nh.iph;
                int err = -EINVAL;
                // IPЭ��ΪIPPROTO_IPIP(4)
                if (iph->protocol != IPPROTO_IPIP)
                    goto out;
                // ��Ҫ��skbͷ����IPͷ�ĳ���(20�ֽ�)
                if (!pskb_may_pull(skb, sizeof(struct iphdr)))
                    goto out;
                // �����clone��,���¿���һ��
                if (skb_cloned(skb) &&
                        (err = pskb_expand_head(skb, 0, 0, GFP_ATOMIC)))
                    goto out;
                // ����dscp�ֶ�
                if (x->props.flags & XFRM_STATE_DECAP_DSCP)
                    ipv4_copy_dscp(iph, skb->h.ipiph);
                // ��XFRM_STATE_NOECNʱ����ECN���װ
                if (!(x->props.flags & XFRM_STATE_NOECN))
                    ipip_ecn_decapsulate(skb);
                // ��Ӳ����ַŲ�����ݰ�������ǰ
                skb->mac.raw = memmove(skb->data - skb->mac_len,
                                       skb->mac.raw, skb->mac_len);
                // ���粿������ͷ
                skb->nh.raw = skb->data;
                err = 0;
                out:
                    return err;
            }
            // ͨ��ģʽ�µ����ݷ�������, ���з�װ
            static int xfrm4_tunnel_output(struct xfrm_state *x, struct sk_buff *skb)
            {
                struct dst_entry *dst = skb->dst;
                struct iphdr *iph, *top_iph;
                int flags;
                iph = skb->nh.iph;
                skb->h.ipiph = iph;
                // ����ͷ�������ⲿIPͷ�ĳ���
                skb->nh.raw = skb_push(skb, x->props.header_len);
                top_iph = skb->nh.iph;
                // ��д�ⲿIPͷ����
                top_iph->ihl = 5;
                top_iph->version = 4;
                /* DS disclosed */
                // ���¼���TOS
                top_iph->tos = INET_ECN_encapsulate(iph->tos, iph->tos);
                flags = x->props.flags;
                if (flags & XFRM_STATE_NOECN)
                    IP_ECN_clear(top_iph);
                // �����Ƭ�����
                top_iph->frag_off = (flags & XFRM_STATE_NOPMTUDISC) ?
                                    0 : (iph->frag_off & htons(IP_DF));
                if (!top_iph->frag_off)
                    __ip_select_ident(top_iph, dst->child, 0);
                // TTL
                top_iph->ttl = dst_metric(dst->child, RTAX_HOPLIMIT);
                // �ⲿԴ��ַ��proposal�е�Դ��ַ
                top_iph->saddr = x->props.saddr.a4;
                // �ⲿĿ�ĵ�ַ��SA�е�Ŀ�ĵ�ַ
                top_iph->daddr = x->id.daddr.a4;
                // �ⲿIPͷ�ڵ�Э���ΪIPIP(4)
                top_iph->protocol = IPPROTO_IPIP;
                // IPѡ�������Ϊ0
                memset(&(IPCB(skb)->opt), 0, sizeof(struct ip_options));
                return 0;
            }
        7.4.2 ����
            ����ģʽ�²�����µ�IPͷ, ��ʵ����ʲô��������, �ϵ��2.6�ں��о�û��ר��Ϊ����ģʽ����.
            ����ģʽ�ṹ����Ϊ:
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
            // ����ģʽ�µ��������뺯��
            static int xfrm4_transport_input(struct xfrm_state *x, struct sk_buff *skb)
            {
                // dataָ����ͷ, hָ��IPͷ, ���ܶ������������ͬ
                int ihl = skb->data - skb->h.raw;
                // ���h��nh��ͬ, ��nh��ָ��IPͷ�����ƶ���h��
                if (skb->h.raw != skb->nh.raw)
                    skb->nh.raw = memmove(skb->h.raw, skb->nh.raw, ihl);
                // �������ݰ�����, ���¶����ݰ����ȸ�ֵ
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
            // ����ģʽ�µ����ݷ�������
            static int xfrm4_transport_output(struct xfrm_state *x, struct sk_buff *skb)
            {
                struct iphdr *iph;
                int ihl;
                // nh�͸�ֵ��h
                iph = skb->nh.iph;
                skb->h.ipiph = iph;
                // ipͷ����
                ihl = iph->ihl * 4;
                // ���¼���hλ��
                skb->h.raw += ihl;
                // ���¼����µ�nhλ��,����proposal�е�ͷ����, ����ԭ����IPͷ����
                skb->nh.raw = memmove(skb_push(skb, x->props.header_len), iph, ihl);
                return 0;
            }
        7.4.3 BEET
            ��װ��BEETPH(94)��, �Ǳ�׼IPSEC, ��.
        7.4.4 С��
            ��xfrm_mode��ص�xfrm������:
            �Ǽ�:
            int xfrm_register_mode(struct xfrm_mode *mode, int family);
            ����:
            int xfrm_unregister_mode(struct xfrm_mode *mode, int family)
            ��ȡ:
            struct xfrm_mode *xfrm_get_mode(unsigned int encap, int family)
            �ͷ�: void xfrm_put_mode(struct xfrm_mode *mode)
            xfrm_mode�����������������:
            xfrm4_rcv_encap()
            -> x->mode->input
            xfrm4_output_one()
            -> x->mode->output
    7.5 ���ݽ���
        IPV4��IPSEC���ݽ��մ�����net/ipv4/xfrm4_input.c�ж���, ��ΪAH��ESPЭ�����ݽ��մ�����.
        /* net/ipv4/xfrm4_input.c */
        int xfrm4_rcv(struct sk_buff *skb)
        {
            return xfrm4_rcv_encap(skb, 0);
        }
        ʵ�ʾ���xfrm4_rcv_encap����װ���Ͳ�������Ϊ0,��NAT-TʱIPSEC���ݱ���װ��UDP����ʱ, �ò����ŷ�0.
        int xfrm4_rcv_encap(struct sk_buff *skb, __u16 encap_type)
        {
            int err;
            __be32 spi, seq;
            struct xfrm_state *xfrm_vec[XFRM_MAX_DEPTH];
            struct xfrm_state *x;
            int xfrm_nr = 0;
            int decaps = 0;
            // ��ȡskb�е�spi�����к���Ϣ
            if ((err = xfrm4_parse_spi(skb, skb->nh.iph->protocol, &spi, &seq)) != 0)
                goto drop;
            // ����ѭ�����н������
            do
            {
                struct iphdr *iph = skb->nh.iph;
                // ѭ���������̫��Ļ�����
                if (xfrm_nr == XFRM_MAX_DEPTH)
                    goto drop;
                // ���ݵ�ַ, SPI��Э�����SA
                x = xfrm_state_lookup((xfrm_address_t *)&iph->daddr, spi, iph->protocol, AF_INET);
                if (x == NULL)
                    goto drop;
                // ���¸���SA����Ĳ��������ݽ���
                spin_lock(&x->lock);
                if (unlikely(x->km.state != XFRM_STATE_VALID))
                    goto drop_unlock;
                // �����SAָ���ķ�װ�����Ƿ�ͺ���ָ���ķ�װ������ͬ
                if ((x->encap ? x->encap->encap_type : 0) != encap_type)
                    goto drop_unlock;
                // SA�طŴ��ڼ��
                if (x->props.replay_window && xfrm_replay_check(x, seq))
                    goto drop_unlock;
                // SA�����ڼ��
                if (xfrm_state_check_expire(x))
                    goto drop_unlock;
                // type��Ϊesp,ah,ipcomp, ipip��, ���������ݽ���
                if (x->type->input(x, skb))
                    goto drop_unlock;
                /* only the first xfrm gets the encap type */
                encap_type = 0;
                // �����طŴ���
                if (x->props.replay_window)
                    xfrm_replay_advance(x, seq);
                // ����,�ֽ���ͳ��
                x->curlft.bytes += skb->len;
                x->curlft.packets++;
                spin_unlock(&x->lock);
                // �������ݽ���õ�SA, ����SA��������
                xfrm_vec[xfrm_nr++] = x;
                // mode��Ϊͨ��,�����ģʽ, ���������ݽ��װ
                if (x->mode->input(x, skb))
                    goto drop;
                // �����IPSECͨ��ģʽ����decaps������1�������ʾ�Ǵ���ģʽ
                if (x->props.mode == XFRM_MODE_TUNNEL)
                {
                    decaps = 1;
                    break;
                }
                // ���ڲ�Э���Ƿ�Ҫ�������, ����Ҫ��ʱ����1, ��Ҫ��ʱ����0, ���󷵻ظ���
                // Э�����Ϳ��Զ���װ��,������AH��װESP, �͵��Ƚ���AH�ٽ�ESP
                if ((err = xfrm_parse_spi(skb, skb->nh.iph->protocol, &spi, &seq)) < 0)
                    goto drop;
            }
            while (!err);
            /* Allocate new secpath or COW existing one. */
            // Ϊskb�������µİ�ȫ·��(struct sec_path)
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
            // ���ղ�ѭ������õ���SA��������ȫ·��
            // ��˼��һ�����ݰ��Ƿ�����ͨ���İ����ǽ��ܺ�����İ��Ϳ�skb->sp�����Ƿ�Ϊ��
            memcpy(skb->sp->xvec + skb->sp->len, xfrm_vec,
                   xfrm_nr * sizeof(xfrm_vec[0]));
            skb->sp->len += xfrm_nr;
            nf_reset(skb);
            if (decaps)
            {
                // ͨ��ģʽ
                if (!(skb->dev->flags&IFF_LOOPBACK))
                {
                    dst_release(skb->dst);
                    skb->dst = NULL;
                }
                // ���½����������պ���
                netif_rx(skb);
                return 0;
            }
            else
            {
                // ����ģʽ
                    #ifdef CONFIG_NETFILTER
                    // �������NETFILTER, ����PRE_ROUTING������,Ȼ�����·��ѡ����
                    // ��ʵ�����Ѿ�����INPUT��, ���������Ҫ���ð���Ϊһ���°�����
                    // ������Ҫ����Ŀ��NAT����, ��ʱ�����Ŀ�ĵ�ַ�ͻ�ı䲻�ǵ�����
                    // ����, �����Ҫ�����൱���ǷŻ�PRE_PROUTING��ȥ����, ������·��
                    // ��Ҳ˵�������ƶ���Խ�������İ���NAT����,�ڻ��Ǽ��ܰ���ʱ��ƥ��
                    // ���������ƥ����
                    __skb_push(skb, skb->data - skb->nh.raw);
                    skb->nh.iph->tot_len = htons(skb->len);
                    ip_send_check(skb->nh.iph);
                    NF_HOOK(PF_INET, NF_IP_PRE_ROUTING, skb, skb->dev, NULL,
                            xfrm4_rcv_encap_finish);
                    return 0;
                #else
                    // �ں˲�֧��NETFILTER, �ð��϶����ǵ��������
                    // ����IPЭ��ĸ�ֵ, ��ʾ���½���IP��Э��Ĵ���
                    // �ý������ڲ�Э������������
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
        // ����AH,ESP���ݰ��е�SPI�����
        static int xfrm4_parse_spi(struct sk_buff *skb, u8 nexthdr, __be32 *spi, __be32 *seq)
        {
            switch (nexthdr)
            {
                // ���ֻ����ͨ��IPIP��, SPIΪԴ��ַ, ���λ0
                case IPPROTO_IPIP:
                    *spi = skb->nh.iph->saddr;
                    *seq = 0;
                    return 0;
            }
            // �������AH/ESP/COMPЭ��ͷ�е�SPI�����
            return xfrm_parse_spi(skb, nexthdr, spi, seq);
        }
        // ���շ�װ��ɴ�����
        static inline int xfrm4_rcv_encap_finish(struct sk_buff *skb)
        {
            struct iphdr *iph = skb->nh.iph;
            // ���û��·��, ���²���·��
            if (skb->dst == NULL)
            {
                if (ip_route_input(skb, iph->daddr, iph->saddr, iph->tos,
                                   skb->dev))
                    goto drop;
            }
            // ������ص�·�����뺯��
            return dst_input(skb);
            drop:
                kfree_skb(skb);
                return NET_RX_DROP;
        }
        ���ù�ϵ:
        ip_rcv
            -> (AH/ESP) net_protocol->handler == xfrm4_rcv
                -> xfrm4_rcv_encap
                    -> xfrm4_parse_spi
                        -> xfrm_parse_spi
                    -> xfrm4_rcv_encap_finish
    7.6 ���ݷ���
        IPV4��IPSEC���ݷ��ʹ�����net/ipv4/xfrm4_output.c�ж���,��Ϊ��ȫ·�ɵ��������:
        int xfrm4_output(struct sk_buff *skb)
        {
            // ����һ������HOOK, ��skb������IPSKB_REROUTED��־ʱ����POSTROUTING���NAT����
            // ����������xfrm�����ж��bundleʱ���ε���, Ҳ���������ڷ�װ���ǰ���Խ���
            // ԴNAT����
            // HOOK���ں���Ϊxfrm4_output_finish
            return NF_HOOK_COND(PF_INET, NF_IP_POST_ROUTING, skb, NULL, skb->dst->dev,
                                xfrm4_output_finish,
                                !(IPCB(skb)->flags & IPSKB_REROUTED));
        }
        // ���ͽ�������
        static int xfrm4_output_finish(struct sk_buff *skb)
        {
            struct sk_buff *segs;
            #ifdef CONFIG_NETFILTER
                // ����ں˶�����NETFILTER, ���������һ��·��(��ͨ·��)ʱ, ����IPSKB_REROUTED
                // ��־, ������ͨ·�ɷ�������(ip_output), ���øñ�־�󲻽���ԴNAT����
                if (!skb->dst->xfrm)
                {
                    IPCB(skb)->flags |= IPSKB_REROUTED;
                    return dst_output(skb);
                }
            #endif
            // ���skb��������gso, תxfrm4_output_finish2
            // gso��ʲô��˼���ڻ���֪��, �Ժ�����ϸ����
            if (!skb_is_gso(skb))
                return xfrm4_output_finish2(skb);
            // ����gso���ݰ�, ����Ҳ��ʹ��xfrm4_output_finish2�������ݰ�
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
        // ��2�����ͽ�������
        static int xfrm4_output_finish2(struct sk_buff *skb)
        {
            int err;
            // ���ݰ�ȫ·�ɰ�װҪ��������
            while (likely((err = xfrm4_output_one(skb)) == 0))
            {
                // ����ɹ�
                // �ͷ�skb�е�netfilter��Ϣ
                nf_reset(skb);
                // ���½��ð���Ϊ��ʼ���Ͱ�, ����OUTPUT�㴦��, ע�����Ǹ����������Ǻ�
                // ����ں�û����NETFILTER, �ú���ֻ�Ǹ��պ���
                // ����1��ʾNF_ACCEPT
                err = nf_hook(PF_INET, NF_IP_LOCAL_OUT, &skb, NULL,
                              skb->dst->dev, dst_output);
                if (unlikely(err != 1))
                    break;
                // ����Ѿ�û��SA, ��ֻ�Ǹ���ͨ����, ·�ɷ���(ip_output)����, �˳�ѭ��
                if (!skb->dst->xfrm)
                    return dst_output(skb);
                // �������SA, Ŀǰ��ֻ���м�״̬, �����Խ���SNAT����, ����POSTROUTING�㴦��
                err = nf_hook(PF_INET, NF_IP_POST_ROUTING, &skb, NULL,
                              skb->dst->dev, xfrm4_output_finish2);
                if (unlikely(err != 1))
                    break;
            }
            return err;
        }
        // ����ȫ·������İ�ȫ·�ɴ�������, ������ӳ�˶��SA�����ݰ����д���
        // ��������__xfrm4_bundle_create�����н�����
        static int xfrm4_output_one(struct sk_buff *skb)
        {
            // ��ȫ·��
            struct dst_entry *dst = skb->dst;
            // ���SA
            struct xfrm_state *x = dst->xfrm;
            int err;
            // skb��У��� ���
            if (skb->ip_summed == CHECKSUM_PARTIAL)
            {
                err = skb_checksum_help(skb);
                if (err)
                    goto error_nolock;
            }
            // �����ͨ��ģʽ, ���skb���ݳ���, ��������ش���, ͨ��ģʽ�·�װ������ݰ����ȿ���
            // �ᳬ��1500�ֽڵ�
            if (x->props.mode == XFRM_MODE_TUNNEL)
            {
                err = xfrm4_tunnel_check_size(skb);
                if (err)
                    goto error_nolock;
            }
            do
            {
                spin_lock_bh(&x->lock);
                // SA�Ϸ��Լ��
                err = xfrm_state_check(x, skb);
                if (err)
                    goto error;
                // ����ģʽ�������, ��ͨ����װ, ��ʱ�ⲿIPͷЭ��ΪIPIP
                err = x->mode->output(x, skb);
                if (err)
                    goto error;
                // ����Э�����, ���ӦESPЭ����˵��esp4_output, ��ʱ�ⲿIPͷЭ����ΪESP
                err = x->type->output(x, skb);
                if (err)
                    goto error;
                // ����SA�еĵ�ǰ�����ڽṹ�еİ����ֽڼ���
                x->curlft.bytes += skb->len;
                x->curlft.packets++;
                spin_unlock_bh(&x->lock);
                // ת�Ƶ���һ����·��
                if (!(skb->dst = dst_pop(dst)))
                {
                    err = -EHOSTUNREACH;
                    goto error_nolock;
                }
                // dst��x��������Ϊ��·���еİ�ȫ·�ɺ�SA
                dst = skb->dst;
                x = dst->xfrm;
                // ѭ��������SA�ǿ�, ����SA����ģʽ����ͨ��ģʽ
            }
            while (x && (x->props.mode != XFRM_MODE_TUNNEL));
            // skb������IPSKB_XFRM_TRANSFORMED��־
            // �иñ�־�����ݰ���NAT�����󽫲�����һЩ������
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
        IPSEC����������ù�ϵ:
        dst_output
        -> xfrm_dst->output == xfrm4_output
        -> NF_HOOK(POSTROUTING)
        -> xfrm4_output_finish
        -> xfrm4_output_finish2
        -> xfrm4_output_one
    7.7 NAT-T֧��
        ��֧��NAT��Խ��IPSEC�����У���ͨ��UDP���ݰ�����װIPSEC����(ESP���ݰ�)��
        ����ڶ�UDP����ʱ��Ҫ�������⴦��
        ����IKEͬ������UDP�����, ������IKE�����Ƿ�װ��ESP���Ϳ�����ͷ��ͷ4�ֽڱ�ʾ��SPIֵ, 
        SPIΪ0��ʾ��IKE��, ��IKE�û��ռ������ս��д���, SPI��0��ʾ��UDP��װ��ESP��, �����ESP��⡣
    7.7.1 ��������
        ��UDP��װ��IPSEC���ڽ���ʱ���Ȱ���ͨUDP�����գ���UDP�������ٽ⿪�ð������IPSEC����
        /* net/ipv4/udp.c */
        // �������յ�UDP����������ú���
        static int udp_queue_rcv_skb(struct sock * sk, struct sk_buff *skb)
        {
            struct udp_sock *up = udp_sk(sk);
            int rc;
            /*
             * Charge it to the socket, dropping if the queue is full.
             */
            // �����Ը�sock��skb�������뷽���ϵ��Ƿ��а�ȫ����
            if (!xfrm4_policy_check(sk, XFRM_POLICY_IN, skb))
            {
                kfree_skb(skb);
                return -1;
            }
            nf_reset(skb);
            // ����SOCK�Ƿ���IPSEC��װ�ģ��ò���ͨ��setsockoptϵͳ���õ�UDP_ENCAPѡ������
            // һ����IKE�����ڴ�UDP4500�˿�ʱ���õ�
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
                // ����UDP��װ����, �ж��Ƿ���ESP��
                // ����ֵС��0��ʾ��IPSEC��, ����0��ʾ����ͨUDP��, ����0��ʾ�Ǵ����
                ret = udp_encap_rcv(sk, skb);
                if (ret == 0)
                {
                    /* Eat the packet .. */
                    kfree_skb(skb);
                    return 0;
                }
                if (ret < 0)
                {
                    // ����IPSEC���մ���
                    /* process the ESP packet */
                    ret = xfrm4_rcv_encap(skb, up->encap_type);
                    UDP_INC_STATS_BH(UDP_MIB_INDATAGRAMS);
                    return -ret;
                }
                /* FALLTHROUGH -- it's a UDP Packet */
            }
            // ���°���ͨUDP�����մ���, ������
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
            // ���ں˲�֧��IPSEC�����ֱ�ӷ���1
                return 1;
            #else
                struct udp_sock *up = udp_sk(sk);
                struct udphdr *uh;
                struct iphdr *iph;
                int iphlen, len;
                __u8 *udpdata;
                __be32 *udpdata32;
                // sock�ķ�װ��־ֵ
                __u16 encap_type = up->encap_type;
                /* if we're overly short, let UDP handle it */
                // UDP���ݰ������ݲ��ֵĳ���
                len = skb->len - sizeof(struct udphdr);
                if (len <= 0)
                    return 1;
                /* if this is not encapsulated socket, then just return now */
                // û�����װ����, ����1, ��ͨ����
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
                // ��UDP�з�װESP
                case UDP_ENCAP_ESPINUDP:
                    /* Check if this is a keepalive packet.  If so, eat it. */
                    if (len == 1 && udpdata[0] == 0xff)
                    {
                        // ֻ����ͨUDP��IPSECͨ�������, ֱ�Ӷ���
                        return 0;
                    }
                    else if (len > sizeof(struct ip_esp_hdr) && udpdata32[0] != 0 )
                    {
                        // ͷ4�ֽڷ���, ESP������Ҫ��һ������
                        /* ESP Packet without Non-ESP header */
                        len = sizeof(struct udphdr);
                    }
                    else
                        // ����IKE��������ͨUDP���մ���
                        /* Must be an IKE packet.. pass it through */
                        return 1;
                    break;
                case UDP_ENCAP_ESPINUDP_NON_IKE:
                    /* Check if this is a keepalive packet.  If so, eat it. */
                    if (len == 1 && udpdata[0] == 0xff)
                    {
                        // IPSECͨ�������, ����
                        return 0;
                    }
                    else if (len > 2 * sizeof(u32) + sizeof(struct ip_esp_hdr) &&
                             udpdata32[0] == 0 && udpdata32[1] == 0)
                    {
                        // ͷ4�ֽڷ���, ESP������Ҫ��һ������
                        /* ESP Packet with Non-IKE marker */
                        len = sizeof(struct udphdr) + 2 * sizeof(u32);
                    }
                    else
                        // ����IKE���ݰ�,��
                        /* Must be an IKE packet.. pass it through */
                        return 1;
                    break;
                }
                /* At this point we are sure that this is an ESPinUDP packet,
                 * so we need to remove 'len' bytes from the packet (the UDP
                 * header and optional ESP marker bytes) and then modify the
                 * protocol to ESP, and then call into the transform receiver.
                 */
                // �����clone����Ҫ���Ƴɶ�����
                if (skb_cloned(skb) && pskb_expand_head(skb, 0, 0, GFP_ATOMIC))
                    return 0;
                // ������ݳ���
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
                // �޸�IP�ϲ�ͷλ��
                skb->h.raw = skb_pull(skb, len);
                // ����IPͷЭ������ΪESP��, ����-1
                /* modify the protocol (it's ESP!) */
                iph->protocol = IPPROTO_ESP;
                /* and let the caller know to send this into the ESP processor... */
                return -1;
            #endif
        }
        �������ù�ϵ��
        udp_rcv
        ->udp_queue_rcv_skb
        -> udp_encap_rcv
        -> xfrm4_policy_check
        -> xfrm_policy_check
        -> __xfrm_policy_check
    7.7.2 ESP����UDP��װ
        ����ESP����UDP��װ����, ����һ��ESPЭ�����ݰ�����������н���.        
8. ��ȫЭ��
    ��IPSEC��صİ�ȫЭ����AH(51)��ESP(50), IPSECʹ��������Э�����ͨ���ݰ����з�װ, 
    AHֻ��֤������, ESP�ȼ�������֤, ��ESP��AHͬʱʹ��ʱ, һ�㶼���Ƚ���ESP��װ, 
    �ٽ���AH��װ, ��ΪAH�Ƕ�����IP��������֤��, ��ESPֻ��֤���ز���.
    ��IPV4�µ�AH��ESP��Э��ʵ����net/ipv4/ah4.c��net/ipv4/esp4.c��, 
    ÿ��Э��ʵ��ʵ����Ҫ��������ṹ:
    struct net_protocol��struct xfrm_type, 
    ǰ�����ڴ�����յĸ�Э�����͵�IP��, ��������IPSECЭ�鴦��.
    8.1 AH
        8.1.1 ��ʼ��
            /* net/ipv4/ah4.c */
            static int __init ah4_init(void)
            {
                // �Ǽ�AHЭ���xfrmЭ�鴦��ṹ
                if (xfrm_register_type(&ah_type, AF_INET) < 0)
                {
                    printk(KERN_INFO "ip ah init: can't add xfrm type\n");
                    return -EAGAIN;
                }
                // �Ǽ�AHЭ�鵽IPЭ��
                if (inet_add_protocol(&ah4_protocol, IPPROTO_AH) < 0)
                {
                    printk(KERN_INFO "ip ah init: can't add protocol\n");
                    xfrm_unregister_type(&ah_type, AF_INET);
                    return -EAGAIN;
                }
                return 0;
            }
        8.1.2 IPV4�µ�AHЭ�鴦��ṹ
            // AHЭ�鴦��ṹ, ���յ�IPV4����, ϵͳ����IPͷ�е�protocol�ֶ�ѡ����Ӧ���ϲ�Э�鴦��
            // ����, ��IPЭ�����51ʱ, ���ݰ������øýṹ��handler������:
            static struct net_protocol ah4_protocol =
            {
                .handler = xfrm4_rcv,
                .err_handler = ah4_err,
                .no_policy = 1,
            };
            AHЭ��ṹ��handler����Ϊxfrm4_rcv, ��net/ipv4/xfrm4_input.c �ж���, ����һƪ�н����˽���.
            // ������, �յ�ICMP�����ʱ�Ĵ������, ��ʱ��skb����ICMP��
            static void ah4_err(struct sk_buff *skb, u32 info)
            {
                // Ӧ�ò�, dataָ��ICMP���������ڲ�IPͷ
                struct iphdr *iph = (struct iphdr*)skb->data;
                // AHͷ
                struct ip_auth_hdr *ah = (struct ip_auth_hdr*)(skb->data+(iph->ihl<<2));
                struct xfrm_state *x;
                // ICMP�������ͼ��, ��������ֻ����"Ŀ�Ĳ��ɴ�"��"��Ҫ��Ƭ"���ִ���
                if (skb->h.icmph->type != ICMP_DEST_UNREACH ||
                        skb->h.icmph->code != ICMP_FRAG_NEEDED)
                    return;
                // ���²���SA
                x = xfrm_state_lookup((xfrm_address_t *)&iph->daddr, ah->spi, IPPROTO_AH, AF_INET);
                if (!x)
                    return;
                printk(KERN_DEBUG "pmtu discovery on SA AH/%08x/%08x\n",
                       ntohl(ah->spi), ntohl(iph->daddr));
                xfrm_state_put(x);
            }
        8.1.3 AH4Э���IPSEC����ṹ
            // AH4��xfrmЭ�鴦��ṹ
            static struct xfrm_type ah_type =
            {
                .description = "AH4",
                .owner  = THIS_MODULE,
                .proto       = IPPROTO_AH,
                // ״̬��ʼ��
                .init_state = ah_init_state,
                // Э���ͷ�
                .destructor = ah_destroy,
                // Э������
                .input  = ah_input,
                // Э�����
                .output  = ah_output
            };
            �ṹ���ص���input��ouput����
            8.1.3.1 ״̬��ʼ��
                ah_data���ݽṹ:
                /* include/net/ah.h */
                struct ah_data
                {
                    // ��Կָ��
                    u8   *key;
                    // ��Կ����
                    int   key_len;
                    // ������ʼ������
                    u8   *work_icv;
                    // ��ʼ��������������
                    int   icv_full_len;
                    // ��ʼ�������ضϳ���
                    int   icv_trunc_len;
                    // HASH�㷨
                    struct crypto_hash *tfm;
                };
                // �ú�����xfrm״̬(SA)��ʼ������xfrm_init_state����
                // ��������SA�����õ�AH���ݴ���ṹ�����Ϣ
                static int ah_init_state(struct xfrm_state *x)
                {
                    struct ah_data *ahp = NULL;
                    struct xfrm_algo_desc *aalg_desc;
                    struct crypto_hash *tfm;
                    // ��AHЭ���SA, ��֤�㷨�Ǳ����, �����û������AH��֤��
                    if (!x->aalg)
                        goto error;
                    /* null auth can use a zero length key */
                    // ��֤�㷨��Կ����Ҫ����512
                    if (x->aalg->alg_key_len > 512)
                        goto error;
                    // ���Ҫ����UDP��װ(����NAT��Խ), ����, ��ΪAH�ǲ�֧��NAT��
                    if (x->encap)
                        goto error;
                    // ����ah_data���ݽṹ�ռ�
                    ahp = kzalloc(sizeof(*ahp), GFP_KERNEL);
                    if (ahp == NULL)
                        return -ENOMEM;
                    // ����AH���ݽṹ����Կ�ͳ���
                    ahp->key = x->aalg->alg_key;
                    ahp->key_len = (x->aalg->alg_key_len+7)/8;
                    // ������֤�㷨HASH�ṹָ�벢��ֵ��AH���ݽṹ
                    // �㷨�ǹ̶���ͬ��, ����ÿ��Ӧ��ʹ���㷨ʱ���������ǲ�ͬ��, �ýṹ������������Ӧ��
                    // ʱ����ش�������������ݵ�
                    tfm = crypto_alloc_hash(x->aalg->alg_name, 0, CRYPTO_ALG_ASYNC);
                    if (IS_ERR(tfm))
                        goto error;
                    ahp->tfm = tfm;
                    // ������֤�㷨��Կ
                    if (crypto_hash_setkey(tfm, ahp->key, ahp->key_len))
                        goto error;
                    /*
                    * Lookup the algorithm description maintained by xfrm_algo,
                    * verify crypto transform properties, and store information
                    * we need for AH processing.  This lookup cannot fail here
                    * after a successful crypto_alloc_hash().
                    */
                    // �����㷨�����ṹ
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
                    // AH���ݽṹ�ĳ�ʼ���������ܳ��ͽضϳ��ȵĸ�ֵ
                    ahp->icv_full_len = aalg_desc->uinfo.auth.icv_fullbits/8;
                    ahp->icv_trunc_len = aalg_desc->uinfo.auth.icv_truncbits/8;
                    BUG_ON(ahp->icv_trunc_len > MAX_AH_AUTH_LEN);
                    // �����ʼ�������ռ�, û���丳ֵ, ���ʼֵ�������ֵ, ��Ҳ�ǳ�ʼ����������Ҫ��
                    ahp->work_icv = kmalloc(ahp->icv_full_len, GFP_KERNEL);
                    if (!ahp->work_icv)
                        goto error;
                    // AH����SA��AHͷ����: ip_auth_hdr�ṹ�ͳ�ʼ����������, ��8�ֽڶ���
                    // ��ӳ��AH��װ����ʱҪ�����ݰ����ӵĳ���
                    x->props.header_len = XFRM_ALIGN8(sizeof(struct ip_auth_hdr) + ahp->icv_trunc_len);
                    // �����ͨ��ģʽ, ����IPͷ����
                    if (x->props.mode == XFRM_MODE_TUNNEL)
                        x->props.header_len += sizeof(struct iphdr);
                    // SA����ָ��AH���ݽṹ
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
            8.1.3.2 Э���ͷ�
                // �ú�����xfrm״̬(SA)�ͷź���xfrm_state_gc_destroy()����
                static void ah_destroy(struct xfrm_state *x)
                {
                    struct ah_data *ahp = x->data;
                    if (!ahp)
                        return;
                    // �ͷų�ʼ�������ռ�
                    kfree(ahp->work_icv);
                    ahp->work_icv = NULL;
                    // �㷨�����ͷ�
                    crypto_free_hash(ahp->tfm);
                    ahp->tfm = NULL;
                    // AH���ݽṹ�ͷ�
                    kfree(ahp);
                }
            8.1.3.3 Э������
                // �������ݴ���, ��xfrm4_rcv_encap()�����е���
                // ����AH��֤, ����AHͷ
                static int ah_input(struct xfrm_state *x, struct sk_buff *skb)
                {
                    int ah_hlen;
                    int ihl;
                    int err = -EINVAL;
                    struct iphdr *iph;
                    struct ip_auth_hdr *ah;
                    struct ah_data *ahp;
                    // IPͷ���ݿռ�
                    char work_buf[60];
                    // skb���ݰ�Ҫ׼������AHͷ�ռ�
                    if (!pskb_may_pull(skb, sizeof(struct ip_auth_hdr)))
                        goto out;
                    // IP�ϲ�����ΪAH����
                    ah = (struct ip_auth_hdr*)skb->data;
                    // SA��ص�AH��������
                    ahp = x->data;
                    ah_hlen = (ah->hdrlen + 2) << 2;
                    // AHͷ�����ȺϷ��Լ��
                    if (ah_hlen != XFRM_ALIGN8(sizeof(struct ip_auth_hdr) + ahp->icv_full_len) &&
                            ah_hlen != XFRM_ALIGN8(sizeof(struct ip_auth_hdr) + ahp->icv_trunc_len))
                        goto out;
                    // skb���ݰ�Ҫ׼������ʵ��AHͷ�ռ�
                    if (!pskb_may_pull(skb, ah_hlen))
                        goto out;
                    /* We are going to _remove_ AH header to keep sockets happy,
                    * so... Later this can change. */
                    // ����clone�İ�Ҫ���Ƴɶ�����
                    if (skb_cloned(skb) &&
                            pskb_expand_head(skb, 0, 0, GFP_ATOMIC))
                        goto out;
                    skb->ip_summed = CHECKSUM_NONE;
                    // ���ܰ��Ѿ������˸���, ���Զ�ah���¸�ֵ
                    ah = (struct ip_auth_hdr*)skb->data;
                    iph = skb->nh.iph;
                    // IPͷ����
                    ihl = skb->data - skb->nh.raw;
                    // �����ⲿIPͷ����
                    memcpy(work_buf, iph, ihl);
                    // ��IPͷ�е�һЩ��������, ��Щ������������֤
                    iph->ttl = 0;
                    iph->tos = 0;
                    iph->frag_off = 0;
                    iph->check = 0;
                    // IPͷ���ȳ���20�ֽ�ʱ,����IPѡ�����
                    if (ihl > sizeof(*iph))
                    {
                        u32 dummy;
                        if (ip_clear_mutable_options(iph, &dummy))
                            goto out;
                    }
                    {
                    // ��֤���ݻ�����
                        u8 auth_data[MAX_AH_AUTH_LEN];
                    // �������ݰ��е���֤���ݵ�������
                        memcpy(auth_data, ah->auth_data, ahp->icv_trunc_len);
                    // ����IPͷ��������
                        skb_push(skb, ihl);
                    // ������ֵ֤�Ƿ�ƥ��, ��0��ʾ����
                        err = ah_mac_digest(ahp, skb, ah->auth_data);
                    // ��֤ʧ�ܷ��ش���
                        if (err)
                            goto out;
                        err = -EINVAL;
                    // ����һ�����ȵ���֤������Ϊ��ʼ������
                        if (memcmp(ahp->work_icv, auth_data, ahp->icv_trunc_len))
                        {
                            x->stats.integrity_failed++;
                            goto out;
                        }
                    }
                    // �����ݵ�IPͷ�������е�Э���ΪAH�ڲ�������Э��
                    ((struct iphdr*)work_buf)->protocol = ah->nexthdr;
                    // ��ԭ��IPͷ���ݿ�����ԭ��AHͷ������Ϊ��IPͷ
                    skb->h.raw = memcpy(skb->nh.raw += ah_hlen, work_buf, ihl);
                    // skb������ԭ����IPͷ��AHͷ, ����IPͷ��Ϊ���ݿ�ʼ
                    __skb_pull(skb, ah_hlen + ihl);
                    return 0;
                    out:
                        return err;
                }
            8.1.3.4 Э�����
                // �������ݴ���, ��xfrm4_output_one()�е���
                // ����AH��ֵ֤, ���AHͷ
                static int ah_output(struct xfrm_state *x, struct sk_buff *skb)
                {
                    int err;
                    struct iphdr *iph, *top_iph;
                    struct ip_auth_hdr *ah;
                    struct ah_data *ahp;
                    // ��ʱIPͷ������, ���IPͷ60�ֽ�
                    union
                    {
                        struct iphdr iph;
                        char   buf[60];
                    } tmp_iph;
                    // ��ǰ��IPͷ����Ϊ���ⲿIPͷ
                    top_iph = skb->nh.iph;
                    // ��ʱIPͷ,������ʱ����IPͷ�ڲ����ֶ�����
                    iph = &tmp_iph.iph;
                    // ����ǰIPͷ�в�������֤���ֶ����ݸ��Ƶ���ʱIPͷ
                    iph->tos = top_iph->tos;
                    iph->ttl = top_iph->ttl;
                    iph->frag_off = top_iph->frag_off;
                    // �����IPѡ��, ����IPѡ��
                    if (top_iph->ihl != 5)
                    {
                        iph->daddr = top_iph->daddr;
                        memcpy(iph+1, top_iph+1, top_iph->ihl*4 - sizeof(struct iphdr));
                        err = ip_clear_mutable_options(top_iph, &top_iph->daddr);
                        if (err)
                            goto error;
                    }
                    // AHͷ��λ���ⲿIPͷ����, skb�������Ѿ�Ԥ����AHͷ�����ݲ�����,
                    // ����ͨ��mode->output����Ԥ����, ͨ������type->outputǰҪ����mode->oputput
                    ah = (struct ip_auth_hdr *)((char *)top_iph+top_iph->ihl*4);
                    // AH�е���һ��ͷ��ԭ�����ⲿIPͷ�е�Э��
                    ah->nexthdr = top_iph->protocol;
                    // ���ⲿIPͷ�Ĳ�������֤����Ĳ����ֶ�����
                    top_iph->tos = 0;
                    top_iph->tot_len = htons(skb->len);
                    top_iph->frag_off = 0;
                    top_iph->ttl = 0;
                    // IPЭ���ΪAH
                    top_iph->protocol = IPPROTO_AH;
                    top_iph->check = 0;
                    // AH���ݴ���ṹ
                    ahp = x->data;
                    // AHͷ���ȶ���
                    ah->hdrlen  = (XFRM_ALIGN8(sizeof(struct ip_auth_hdr) +
                                               ahp->icv_trunc_len) >> 2) - 2;
                    // AHͷ������ֵ
                    ah->reserved = 0;
                    // SPIֵ
                    ah->spi = x->id.spi;
                    // ���к�
                    ah->seq_no = htonl(++x->replay.oseq);
                    // ֪ͨ��ֹ�ط�***����, �������к�
                    xfrm_aevent_doreplay(x);
                    // ��skb����AH��ֵ֤�ļ���
                    err = ah_mac_digest(ahp, skb, ah->auth_data);
                    if (err)
                        goto error;
                    // ��ֵ��ʼ������ֵ����֤���ݲ���
                    memcpy(ah->auth_data, ahp->work_icv, ahp->icv_trunc_len);
                    // �ָ�ԭ��IPͷ�ĵĲ���֤���ֵ�ֵ
                    top_iph->tos = iph->tos;
                    top_iph->ttl = iph->ttl;
                    top_iph->frag_off = iph->frag_off;
                    if (top_iph->ihl != 5)
                    {
                        top_iph->daddr = iph->daddr;
                        memcpy(top_iph+1, iph+1, top_iph->ihl*4 - sizeof(struct iphdr));
                    }
                    // ���¼���IPͷ����ֵ֤
                    ip_send_check(top_iph);
                    err = 0;
                    error:
                        return err;
                }
    8.2 ESP
        8.2.1 ��ʼ��
            /* net/ipv4/esp4.c */
            static int __init esp4_init(void)
            {
                // �Ǽ�ESPЭ���xfrmЭ�鴦��ṹ
                if (xfrm_register_type(&esp_type, AF_INET) < 0)
                {
                    printk(KERN_INFO "ip esp init: can't add xfrm type\n");
                    return -EAGAIN;
                }
                // �Ǽ�ESPЭ�鵽IPЭ��
                if (inet_add_protocol(&esp4_protocol, IPPROTO_ESP) < 0)
                {
                    printk(KERN_INFO "ip esp init: can't add protocol\n");
                    xfrm_unregister_type(&esp_type, AF_INET);
                    return -EAGAIN;
                }
                return 0;
            }
        8.2.2 IPV4�µ�ESPЭ�鴦��ṹ
            // ESPЭ�鴦��ṹ, ���յ�IPV4����, ϵͳ����IPͷ�е�protocol
            // �ֶ�ѡ����Ӧ���ϲ�Э�鴦����, ��IPЭ�����50ʱ, ���ݰ���
            // ���øýṹ��handler������:
            static struct net_protocol esp4_protocol =
            {
                .handler = xfrm4_rcv,
                .err_handler = esp4_err,
                .no_policy = 1,
            };
            ESPЭ��ṹ��handler����Ҳ��xfrm4_rcv, 
            ��net/ipv4/xfrm4_input.c �ж���,
            ����һƪ�н����˽���.
            // ������, �յ�ICMP�����ʱ�Ĵ������, ��ʱ��skb����ICMP��
            static void esp4_err(struct sk_buff *skb, u32 info)
            {
                // Ӧ�ò�, dataָ��ICMP���������ڲ�IPͷ
                struct iphdr *iph = (struct iphdr*)skb->data;
                // ESPͷ
                struct ip_esp_hdr *esph = (struct ip_esp_hdr*)(skb->data+(iph->ihl<<2));
                struct xfrm_state *x;
                // ICMP�������ͼ��, ��������ֻ����"Ŀ�Ĳ��ɴ�"��"��Ҫ��Ƭ"���ִ���
                if (skb->h.icmph->type != ICMP_DEST_UNREACH ||
                        skb->h.icmph->code != ICMP_FRAG_NEEDED)
                    return;
                // ���²���SA
                x = xfrm_state_lookup((xfrm_address_t *)&iph->daddr, esph->spi, IPPROTO_ESP, AF_INET);
                if (!x)
                    return;
                NETDEBUG(KERN_DEBUG "pmtu discovery on SA ESP/%08x/%08x\n",
                         ntohl(esph->spi), ntohl(iph->daddr));
                xfrm_state_put(x);
            }
        8.2.3 ESP4Э���IPSEC����ṹ
            static struct xfrm_type esp_type =
            {
                .description = "ESP4",
                .owner  = THIS_MODULE,
                .proto       = IPPROTO_ESP,
                // ״̬��ʼ��
                .init_state = esp_init_state,
                // Э���ͷ�
                .destructor = esp_destroy,
                // ������󳤶�
                .get_max_size = esp4_get_max_size,
                // Э������
                .input  = esp_input,
                // Э�����
                .output  = esp_output
            };
            8.2.3.1 ״̬��ʼ��
                esp_data���ݽṹ:
                /* include/net/esp.h */
                struct esp_data
                {
                    struct scatterlist  sgbuf[ESP_NUM_FAST_SG];
                    /* Confidentiality */
                    // ����ʹ�õ��������
                    struct
                    {
                        // ��Կ
                        u8   *key;  /* Key */
                        // ��Կ����
                        int   key_len; /* Key length */
                        // ��䳤��
                        int   padlen;  /* 0..255 */
                        /* ivlen is offset from enc_data, where encrypted data start.
                        * It is logically different of crypto_tfm_alg_ivsize(tfm).
                        * We assume that it is either zero (no ivec), or
                        * >= crypto_tfm_alg_ivsize(tfm). */
                        // ��ʼ����������
                        int   ivlen;
                        // ��ʼ�������Ƿ��ʼ����־
                        int   ivinitted;
                        // ��ʼ������
                        u8   *ivec;  /* ivec buffer */
                        // �����㷨
                        struct crypto_blkcipher *tfm;  /* crypto handle */
                    } conf;
                    /* Integrity. It is active when icv_full_len != 0 */
                    // ��֤ʹ�õ��������
                    struct
                    {
                        // ��Կ
                        u8   *key;  /* Key */
                        // ��Կ����
                        int   key_len; /* Length of the key */
                        // ��ʼ������
                        u8   *work_icv;
                        // ��ʼ������ȫ��
                        int   icv_full_len;
                        // ��ʼ�������ضϳ���
                        int   icv_trunc_len;
                        // ��ʼ���������º���, ����û��
                        void   (*icv)(struct esp_data*,
                                      struct sk_buff *skb,
                                      int offset, int len, u8 *icv);
                        // HASH�㷨
                        struct crypto_hash *tfm;
                    } auth;
                };
                // ESP��esp_data���ݽṹ��ʼ��
                static int esp_init_state(struct xfrm_state *x)
                {
                    struct esp_data *esp = NULL;
                    struct crypto_blkcipher *tfm;
                    /* null auth and encryption can have zero length keys */
                    // �������֤�㷨, ��Կ����512, ESP����֤�����ǿ�ѡ��, ����ʵ���ж���ʹ����֤
                    if (x->aalg)
                    {
                        if (x->aalg->alg_key_len > 512)
                            goto error;
                    }
                    // ESP�����㷨�Ǳ����
                    if (x->ealg == NULL)
                        goto error;
                    // ����esp_data���ݽṹ�ռ�
                    esp = kzalloc(sizeof(*esp), GFP_KERNEL);
                    if (esp == NULL)
                        return -ENOMEM;
                    // �����������֤�㷨, ��ʼ����֤�㷨����, ��AH����
                    if (x->aalg)
                    {
                        struct xfrm_algo_desc *aalg_desc;
                        struct crypto_hash *hash;
                        // ��֤��Կ�ͳ�������
                        esp->auth.key = x->aalg->alg_key;
                        esp->auth.key_len = (x->aalg->alg_key_len+7)/8;
                        // ����HASH�㷨��ʵ��
                        hash = crypto_alloc_hash(x->aalg->alg_name, 0,
                                                 CRYPTO_ALG_ASYNC);
                        if (IS_ERR(hash))
                            goto error;
                        esp->auth.tfm = hash;
                        // ����HASH�㷨��Կ
                        if (crypto_hash_setkey(hash, esp->auth.key, esp->auth.key_len))
                            goto error;
                        // �ҵ��㷨����
                        aalg_desc = xfrm_aalg_get_byname(x->aalg->alg_name, 0);
                        BUG_ON(!aalg_desc);
                        // ����㷨��ʼ���������ȺϷ���
                        if (aalg_desc->uinfo.auth.icv_fullbits/8 !=
                                crypto_hash_digestsize(hash))
                        {
                            NETDEBUG(KERN_INFO "ESP: %s digestsize %u != %hu\n",
                                     x->aalg->alg_name,
                                     crypto_hash_digestsize(hash),
                                     aalg_desc->uinfo.auth.icv_fullbits/8);
                            goto error;
                        }
                        // ��ʼ��������ȫ���ͽضϳ���
                        esp->auth.icv_full_len = aalg_desc->uinfo.auth.icv_fullbits/8;
                        esp->auth.icv_trunc_len = aalg_desc->uinfo.auth.icv_truncbits/8;
                        // ����ȫ���ȵĳ�ʼ�������ռ�
                        esp->auth.work_icv = kmalloc(esp->auth.icv_full_len, GFP_KERNEL);
                        if (!esp->auth.work_icv)
                            goto error;
                    }
                    // ��ʼ�������㷨��ز���, ESPʹ�õļ����㷨���ǶԳƿ�����㷨, �������÷ǶԳ��㷨��
                    // ������Կ
                    esp->conf.key = x->ealg->alg_key;
                    // ������Կ����
                    esp->conf.key_len = (x->ealg->alg_key_len+7)/8;
                    // ��������㷨�ľ���ʵ�ֽṹ
                    tfm = crypto_alloc_blkcipher(x->ealg->alg_name, 0, CRYPTO_ALG_ASYNC);
                    if (IS_ERR(tfm))
                        goto error;
                    esp->conf.tfm = tfm;
                    // ��ʼ��������С
                    esp->conf.ivlen = crypto_blkcipher_ivsize(tfm);
                    // ������ݳ��ȳ�ʼ��Ϊ0
                    esp->conf.padlen = 0;
                    // ��ʼ���������ȷ�0, �������ĳ�ʼ�������ռ�
                    if (esp->conf.ivlen)
                    {
                        esp->conf.ivec = kmalloc(esp->conf.ivlen, GFP_KERNEL);
                        if (unlikely(esp->conf.ivec == NULL))
                            goto error;
                        esp->conf.ivinitted = 0;
                    }
                    // ���ü����㷨��Կ
                    if (crypto_blkcipher_setkey(tfm, esp->conf.key, esp->conf.key_len))
                        goto error;
                    // ����SA��ESPͷ������: ESPͷ�ӳ�ʼ����������
                    // ��ӳ��ESP��װ����ʱҪ�����ݰ����ӵĳ���
                    x->props.header_len = sizeof(struct ip_esp_hdr) + esp->conf.ivlen;
                    // �����ͨ��ģʽ, ����Ҫ����IPͷ����
                    if (x->props.mode == XFRM_MODE_TUNNEL)
                        x->props.header_len += sizeof(struct iphdr);
                    // ���Ҫ����UDP��װ
                    if (x->encap)
                    {
                        struct xfrm_encap_tmpl *encap = x->encap;
                        switch (encap->encap_type)
                        {
                        default:
                            goto error;
                        case UDP_ENCAP_ESPINUDP:
                            // �����ͷ�װ����UDPͷ����
                            x->props.header_len += sizeof(struct udphdr);
                            break;
                        case UDP_ENCAP_ESPINUDP_NON_IKE:
                            // �����ͷ�װ����UDPͷ������Ӽ�8�ֽ�
                            x->props.header_len += sizeof(struct udphdr) + 2 * sizeof(u32);
                            break;
                        }
                    }
                    // ��esp_data��ΪSA��dataָ��
                    x->data = esp;
                    // ׷�ٳ���, ������ӳ��Ⱥ͵�ǰ�ļ�������ӳ��ȵĲ�ֵ,��·��ʱ���õ�
                    // ����AH, ����û�ж���get_max_size(), ��ֵλ0
                    x->props.trailer_len = esp4_get_max_size(x, 0) - x->props.header_len;
                    return 0;
                    error:
                        x->data = esp;
                        esp_destroy(x);
                        x->data = NULL;
                        return -EINVAL;
                }
            8.2.3.2 Э���ͷ�
                // �ú�����xfrm״̬(SA)�ͷź���xfrm_state_gc_destroy()����
                static void esp_destroy(struct xfrm_state *x)
                {
                    struct esp_data *esp = x->data;
                    if (!esp)
                        return;
                    // �ͷż����㷨
                    crypto_free_blkcipher(esp->conf.tfm);
                    esp->conf.tfm = NULL;
                    // �ͷż��ܳ�ʼ������
                    kfree(esp->conf.ivec);
                    esp->conf.ivec = NULL;
                    // �ͷ���֤�㷨
                    crypto_free_hash(esp->auth.tfm);
                    esp->auth.tfm = NULL;
                    // �ͷ���֤��ʼ������
                    kfree(esp->auth.work_icv);
                    esp->auth.work_icv = NULL;
                    // �ͷ�esp_data
                    kfree(esp);
                }
            8.2.3.3 ������󳤶�
                // ��xfrm_state_mtu()�����е���, ����������ӵ����ݳ���
                // AH��û�иú���, ���ӵĳ���ʹ��x->props.header_len
                static u32 esp4_get_max_size(struct xfrm_state *x, int mtu)
                {
                    struct esp_data *esp = x->data;
                    // ���ܿ鳤��, ��4�ֽڶ���
                    u32 blksize = ALIGN(crypto_blkcipher_blocksize(esp->conf.tfm), 4);
                    int enclen = 0;
                    switch (x->props.mode)
                    {
                    case XFRM_MODE_TUNNEL:
                        // ͨ��ģʽ�µ�MTU, �����ܿ��С����, +2��Ҫ����2�ֽ����ݳ���
                        mtu = ALIGN(mtu +2, blksize);
                        break;
                    default:
                    case XFRM_MODE_TRANSPORT:
                        /* The worst case */
                        // ����ģʽ��, MTU�Ȱ�4�ֽڶ���, �ټӿ鳤�ȼ�4
                        mtu = ALIGN(mtu + 2, 4) + blksize - 4;
                        break;
                    case XFRM_MODE_BEET:
                        /* The worst case. */
                        enclen = IPV4_BEET_PHMAXLEN;
                        mtu = ALIGN(mtu + enclen + 2, blksize);
                        break;
                    }
                    // ��������㷨�ж�������䳤��, MTUҲҪ����䳤�ȶ���
                    if (esp->conf.padlen)
                        mtu = ALIGN(mtu, esp->conf.padlen);
                    // ����MTU����������Ҫ���ӵ�ͷ�����Ⱥ���֤��ʼ�������Ľضϳ���
                    // enclenֻ��BEETģʽ�·�0, ��ͨ���ʹ���ģʽ�¶���0
                    return mtu + x->props.header_len + esp->auth.icv_trunc_len - enclen;
                }
            8.2.3.4 Э������
                struct scatterlist�ṹ˵��:
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
                // �������ݴ���, ��xfrm4_rcv_encap()�����е���
                // ����ESP��֤����, ����ESPͷ, ���ܳ���ͨ���ݰ�, ���ݰ����ȼ���
                // ��������ݰ���ESP��
                static int esp_input(struct xfrm_state *x, struct sk_buff *skb)
                {
                    struct iphdr *iph;
                    struct ip_esp_hdr *esph;
                    struct esp_data *esp = x->data;
                    struct crypto_blkcipher *tfm = esp->conf.tfm;
                    struct blkcipher_desc desc = { .tfm = tfm };
                    struct sk_buff *trailer;
                    int blksize = ALIGN(crypto_blkcipher_blocksize(tfm), 4);
                    // ��֤��ʼ�������ضϳ���
                    int alen = esp->auth.icv_trunc_len;
                    // ��Ҫ���ܵ����ݳ���: �ܳ���ESPͷ, ���ܳ�ʼ����������, ��֤��ʼ����������
                    int elen = skb->len - sizeof(struct ip_esp_hdr) - esp->conf.ivlen - alen;
                    int nfrags;
                    int ihl;
                    u8 nexthdr[2];
                    struct scatterlist *sg;
                    int padlen;
                    int err;
                    // ��skbͷ����ESPͷ�Ŀռ�
                    if (!pskb_may_pull(skb, sizeof(struct ip_esp_hdr)))
                        goto out;
                    // �����Ҫ���ܵ����ݳ���, �������0���Ұ����С�����
                    if (elen <= 0 || (elen & (blksize-1)))
                        goto out;
                    /* If integrity check is required, do this. */
                    // ��֤���㴦��
                    if (esp->auth.icv_full_len)
                    {
                        u8 sum[alen];
                        // ������ֵ֤, ��ֵ֤������esp_data�ṹ��
                        err = esp_mac_digest(esp, skb, 0, skb->len - alen);
                        if (err)
                            goto out;
                        // ��skb�е���֤��ʼ�������������ݿ�����������sum��
                        if (skb_copy_bits(skb, skb->len - alen, sum, alen))
                            BUG();
                        // �Ƚ�sum�е�����ֵ����֤�㷨�ṹ�е�����ֵ�Ƿ�ƥ��, ���ݰ����������Ӧ������ͬ��
                        if (unlikely(memcmp(esp->auth.work_icv, sum, alen)))
                        {
                            x->stats.integrity_failed++;
                            goto out;
                        }
                    }
                    // ʹ���ݰ��ǿ�д��
                    if ((nfrags = skb_cow_data(skb, 0, &trailer)) < 0)
                        goto out;
                    skb->ip_summed = CHECKSUM_NONE;
                    // ��λ�����ݰ��е�ESPͷλ��, Ϊ��ǰ��dataλ��
                    esph = (struct ip_esp_hdr*)skb->data;
                    /* Get ivec. This can be wrong, check against another impls. */
                    // ���ü����㷨�ĳ�ʼ������
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
                    // ���ܲ���, ���ط�0��ʾʧ��
                    err = crypto_blkcipher_decrypt(&desc, sg, sg, elen);
                    if (unlikely(sg != &esp->sgbuf[0]))
                        kfree(sg);
                    // ����ʧ�ܷ���
                    if (unlikely(err))
                        return err;
                    // �������ֽ�����
                    if (skb_copy_bits(skb, skb->len-alen-2, nexthdr, 2))
                        BUG();
                    padlen = nexthdr[0];
                    if (padlen+2 >= elen)
                        goto out;
                    /* ... check padding bits here. Silly. :-) */
                    // �µ�IPͷ
                    iph = skb->nh.iph;
                    ihl = iph->ihl * 4;
                    // �����NAT��Խ���, ����һЩ����
                    if (x->encap)
                    {
                        // xfrm��װģ��
                        struct xfrm_encap_tmpl *encap = x->encap;
                        // ��λUDP����ͷλ��, ��IPͷ֮��
                        struct udphdr *uh = (void *)(skb->nh.raw + ihl);
                        /*
                        * 1) if the NAT-T peer's IP or port changed then
                        *    advertize the change to the keying daemon.
                        *    This is an inbound SA, so just compare
                        *    SRC ports.
                        */
                        // ���IPͷԴ��ַ��SA�����е�Դ��ַ��ͬ��Դ�˿ڲ�ͬ
                        if (iph->saddr != x->props.saddr.a4 ||
                                uh->source != encap->encap_sport)
                        {
                            xfrm_address_t ipaddr;
                            // ���浱ǰIPͷԴ��ַ
                            ipaddr.a4 = iph->saddr;
                            // ����NAT֪ͨ�ص�����
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
                        // ����Ǵ���ģʽ��BEETģʽ, ���ò���Ҫ����У���
                        if (x->props.mode == XFRM_MODE_TRANSPORT ||
                                x->props.mode == XFRM_MODE_BEET)
                            skb->ip_summed = CHECKSUM_UNNECESSARY;
                    }
                    // ��IPͷ��Э��
                    iph->protocol = nexthdr[1];
                    // ����skb���ݰ�����
                    pskb_trim(skb, skb->len - alen - padlen - 2);
                    // ���¶�λIP�ϲ�����ͷλ��
                    skb->h.raw = __skb_pull(skb, sizeof(*esph) + esp->conf.ivlen) - ihl;
                    return 0;
                    out:
                        return -EINVAL;
                }
            8.2.3.5 Э�����
                // �������ݴ���, ��xfrm4_output_one()�е���
                // ���ESPͷ, �����ݰ����м��ܺ���֤����, ���ݰ���������
                // ��NAT��Խ����»��װΪUDP����
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
                    // ����skb����, ��ȥIPͷ��ESPͷ, ʣ�µ����ݾ���Ҫ���м��ܺ���֤�Ĳ���
                    __skb_pull(skb, skb->h.raw - skb->data);
                    /* Now skb is pure payload to encrypt */
                    err = -ENOMEM;
                    /* Round to block size */
                    // ���ܿ�ĳ�ʼֵ
                    clen = skb->len;
                    // ��ȡSA��esp_data���ݽṹ
                    esp = x->data;
                    // ��֤��ʼ�������ضϳ���
                    alen = esp->auth.icv_trunc_len;
                    // �����㷨
                    tfm = esp->conf.tfm;
                    // ��������㷨�����ṹ��ֵ
                    desc.tfm = tfm;
                    desc.flags = 0;
                    // ÿ�����ܿ��С
                    blksize = ALIGN(crypto_blkcipher_blocksize(tfm), 4);
                    // ����Ҫ���ܵ������ܳ�
                    clen = ALIGN(clen + 2, blksize);
                    // ���Ҫ�������, ��������
                    if (esp->conf.padlen)
                        clen = ALIGN(clen, esp->conf.padlen);
                    // ʹ���ݰ���д
                    if ((nfrags = skb_cow_data(skb, clen-skb->len+alen, &trailer)) < 0)
                        goto error;
                    /* Fill padding... */
                    // ���ȶ���������೤�Ȳ�������
                    do
                    {
                        int i;
                        for (i=0; i<clen-skb->len - 2; i++)
                            *(u8*)(trailer->tail + i) = i+1;
                    }
                    while (0);
                    // ������ֽڱ�ʾ������ݵĳ���
                    *(u8*)(trailer->tail + clen-skb->len - 2) = (clen - skb->len)-2;
                    pskb_put(skb, trailer, clen - skb->len);
                    // �ڽ�IPͷ������չ����
                    __skb_push(skb, skb->data - skb->nh.raw);
                    // ���ڵ�IPͷ��Ϊ�ⲿIPͷ
                    top_iph = skb->nh.iph;
                    // espͷ����IPͷ��
                    esph = (struct ip_esp_hdr *)(skb->nh.raw + top_iph->ihl*4);
                    // �����ܳ�������֤���ֳ���
                    top_iph->tot_len = htons(skb->len + alen);
                    *(u8*)(trailer->tail - 1) = top_iph->protocol;
                    /* this is non-NULL only with UDP Encapsulation */
                    if (x->encap)
                    {
                        // NAT��Խ�����Ҫ�����ݷ�װΪUDP��
                        struct xfrm_encap_tmpl *encap = x->encap;
                        struct udphdr *uh;
                        u32 *udpdata32;
                        // IPͷ���ΪUDPͷ
                        uh = (struct udphdr *)esph;
                        // ���UDPͷ����, Դ�˿�, Ŀ�Ķ˿�, UDP���ݳ���
                        uh->source = encap->encap_sport;
                        uh->dest = encap->encap_dport;
                        uh->len = htons(skb->len + alen - top_iph->ihl*4);
                        // У���Ϊ0, ��ʾ����Ҫ����У���, ESP����ͽ�����֤��
                        uh->check = 0;
                        switch (encap->encap_type)
                        {
                        default:
                        case UDP_ENCAP_ESPINUDP:
                            // �ڸ�ģʽ��ESPͷ����UDPͷ����
                            esph = (struct ip_esp_hdr *)(uh + 1);
                            break;
                        case UDP_ENCAP_ESPINUDP_NON_IKE:
                            // �ڸ�ģʽ��ESPͷ����UDPͷ����8�ֽڴ�
                            udpdata32 = (u32 *)(uh + 1);
                            udpdata32[0] = udpdata32[1] = 0;
                            esph = (struct ip_esp_hdr *)(udpdata32 + 2);
                            break;
                        }
                        // �ⲿIPͷЭ����UDP
                        top_iph->protocol = IPPROTO_UDP;
                    }
                    else
                    // ��NAT��Խ�����, �ⲿIPͷ�е�Э����ESP
                        top_iph->protocol = IPPROTO_ESP;
                    // ���ESPͷ�е�SPI�����к�
                    esph->spi = x->id.spi;
                    esph->seq_no = htonl(++x->replay.oseq);
                    // ���кŸ���֪ͨ�ص�
                    xfrm_aevent_doreplay(x);
                    // ������ܳ�ʼ���������ȷ���, ���ü����㷨�еĳ�ʼ������
                    if (esp->conf.ivlen)
                    {
                        if (unlikely(!esp->conf.ivinitted))
                        {
                            get_random_bytes(esp->conf.ivec, esp->conf.ivlen);
                            esp->conf.ivinitted = 1;
                        }
                        crypto_blkcipher_set_iv(tfm, esp->conf.ivec, esp->conf.ivlen);
                    }
                    // ���ܲ���
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
                        // �����ݼ���
                        err = crypto_blkcipher_encrypt(&desc, sg, sg, clen);
                        if (unlikely(sg != &esp->sgbuf[0]))
                            kfree(sg);
                    }
                    while (0);
                    if (unlikely(err))
                        goto error;
                    // �������㷨��ʼ���������������ݰ�
                    if (esp->conf.ivlen)
                    {
                        memcpy(esph->enc_data, esp->conf.ivec, esp->conf.ivlen);
                        crypto_blkcipher_get_iv(tfm, esp->conf.ivec, esp->conf.ivlen);
                    }
                    // ��֤����, �����HASHֵ�����������ݰ���
                    if (esp->auth.icv_full_len)
                    {
                        err = esp_mac_digest(esp, skb, (u8 *)esph - skb->data,
                                             sizeof(*esph) + esp->conf.ivlen + clen);
                        memcpy(pskb_put(skb, trailer, alen), esp->auth.work_icv, alen);
                    }
                    // ���¼����ⲿIPͷУ���
                    ip_send_check(top_iph);
                    error:
                        return err;
                }
9. IPSEC��װ����
    IPSEC���ݰ��ķ�װ�����������ݰ�����ǰ��ɵ�, �Ǻ�·��ѡ��������ص�, 
    ����ǰ��ķ���������֪��װ��ͨ�����������ð�ȫ·��������ʵ�ֵ�, 
    ��˶����ݰ���IPSEC��װ���̿��Լ���������:
    1) ���ڽ�������ݰ�, ����·��ѡ��, �����ת����, ����·������, 
       Ȼ����Ұ�ȫ���Լ���Ƿ���ҪIPSEC��װ, �����Ҫ��װ, �Ͳ��Һʹ�����صİ�ȫ·��, 
       ����·���������, ��·�����ʱ�����հ�ȫ·��һ���ط�װ���ݰ����õ�IPSEC������;
    2) ���������������ݰ�, ��Ҫ����·��ѡ��, ѡ��·�ɺ����·������, 
       ���Ұ�ȫ���Խ��д���, �Ժ��ת�������ݰ�IPSEC��װ������ȫ��ͬ�ˡ�
    9.1 ת�����ķ�װ
        ���ݵ�ת����ڵ㺯����ip_forward, ����ú��������ݰ�������ͨ���ݰ������ݰ���·��Ҳ����ͨ·�ɣ�
        /* net/ipv4/ip_forward.c */
        int ip_forward(struct sk_buff *skb)
        {
            struct iphdr *iph; /* Our header */
            struct rtable *rt; /* Route we use */
            struct ip_options * opt = &(IPCB(skb)-<opt);
            // ��ת�������ݰ����а�ȫ���Լ��, ���ʧ�ܵĻ�����
            if (!xfrm4_policy_check(NULL, XFRM_POLICY_FWD, skb))
                goto drop;
            if (IPCB(skb)-<opt.router_alert && ip_call_ra_chain(skb))
                return NET_RX_SUCCESS;
            // ת����Ҳ�ǵ�����İ�, ���ǵĻ�����
            if (skb-<pkt_type != PACKET_HOST)
                goto drop;
            skb-<ip_summed = CHECKSUM_NONE;
            /*
             * According to the RFC, we must first decrease the TTL field. If
             * that reaches zero, we must reply an ICMP control message telling
             * that the packet's lifetime expired.
             */
            // TTL��ͷ��, ����
            if (skb->nh.iph->ttl <= 1)              
                goto too_many_hops;
            // ���밲ȫ·��ѡ·��ת������, �ڴ˺����й������ݰ��İ�ȫ·��
            if (!xfrm4_route_forward(skb))
                goto drop;
            // ������һЩ�����·�ɺ�TTL����
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
                // ����FORWARD�����, ���˺����ip_forward_finish����
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
        // ip_forward_finish������Ҫ���ǵ���dst_output����
        static inline int ip_forward_finish(struct sk_buff *skb)
        {
            struct ip_options * opt = &(IPCB(skb)-<opt);
            IP_INC_STATS_BH(IPSTATS_MIB_OUTFORWDATAGRAMS);
            if (unlikely(opt-<optlen))
                ip_forward_options(skb);
            return dst_output(skb);
        }
        ���ĺ�����xfrm4_route_forward����
        /* include/net/xfrm.h */
        static inline int xfrm4_route_forward(struct sk_buff *skb)
        {
            return xfrm_route_forward(skb, AF_INET);
        }
        static inline int xfrm_route_forward(struct sk_buff *skb, unsigned short family)
        {
            // ���û�з�������İ�ȫ���ԵĻ�����
            return !xfrm_policy_count[XFRM_POLICY_OUT] ||
                   // ���·�ɱ�־ר�����ò�����IPSEC��װ�Ļ�Ҳ����
                   (skb-<dst-<flags & DST_NOXFRM) ||
                   __xfrm_route_forward(skb, family);
        }
        /* net/xfrm/xfrm_policy.c */
        int __xfrm_route_forward(struct sk_buff *skb, unsigned short family)
        {
            struct flowi fl;
            // ·�ɽ���, ������ṹ����,
            // ��IPV4ʵ�ʵ��õ���_decode_session4(net/ipv4/xfrm4_policy.c)����
            if (xfrm_decode_session(skb, &fl, family) < 0 br style='font-size:12px;font-style:normal;font-weight:400;color:#666;' />  return 0;
                    // �������ṹ���Ұ�ȫ·��, û�ҵ��Ļ������µİ�ȫ·��, ����γɰ�ȫ·������
                    // ��ǰ�����еķ���
                    return xfrm_lookup(&skb-<dst, &fl, NULL, 0) == 0;
        }
        
        ������ݽ���ת�������, ���ս���dst_output��������
        ת����������С��:
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
    9.2 �������ݷ���
        ����IPv4���ķ���, ͨ�����ں�����ip_queue_xmit��ip_push_pending_frames, 
        ����Ǻ���, ���ݰ����Ѿ�������·��ѡ���, ��ǰ�߻�û�н���·��ѡ��, 
        ������󶼻����dst_output()�����������ݵķ���.
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
            // �Ѿ�·�ɹ�����������·�ɲ��ҹ���
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
                // ����OUTPUT����й���, ������ɺ����dst_output()����
                return NF_HOOK(PF_INET, NF_IP_LOCAL_OUT, skb, NULL, rt-<u.dst.dev,
                               dst_output);
            no_route:
                IP_INC_STATS(IPSTATS_MIB_OUTNOROUTES);
                kfree_skb(skb);
                return -EHOSTUNREACH;
        }
        // ·�ɲ��Һ���
        int ip_route_output_flow(struct rtable **rp, struct flowi *flp, struct sock *sk, int flags)
        {
            int err;
            // ��ͨ��·�ɲ��ҹ���, �˹��̲��Ǳ����ص�, ������
            if ((err = __ip_route_output_key(rp, flp)) != 0)
                return err;
            // ������ṹЭ���0(�����ǿ϶���)����xfrm·�ɲ���
            if (flp-<proto)
            {
                // ָ�����ṹ��Դ��ַ��Ŀ�ĵ�ַ
                if (!flp-<fl4_src)
                    flp-<fl4_src = (*rp)-<rt_src;
                if (!flp-<fl4_dst)
                    flp-<fl4_dst = (*rp)-<rt_dst;
                // �������ṹ���Ұ�ȫ·��, û�ҵ��Ļ������µİ�ȫ·��, ����γɰ�ȫ·������
                // ��ǰ�����еķ���
                return xfrm_lookup((struct dst_entry **)rp, flp, sk, flags);
            }
            return 0;
        }
        ���ڲ��ǽ���ip_queue_xmit()���͵����ݰ�, 
        �ڷ���ǰ��ȻҲ�Ǿ���ip_route_output_flow()������·��ѡ����, 
        ��������ҪIPSEC��װ�Ļ�, Ҳ����������صİ�ȫ·������.
        ����, ���������������ݰ�, ����Ҳ�ǽ���dst_output()�������з���, 
        ת������������������;ͬ����, �Ժ�Ĵ�����̾Ͷ�����ͬ����
        ��������С��:
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
        dst_output()�������ǵ���·������������, ���ڰ�ȫ·��, 
        �ú�����xfrm4_output()����, ������ͨ·��, ��ip_output()����
        ����xfrm4_output()�����ķ�����7.6, ִ�������а�ȫ·�ɵ��������, 
        ÿִ��һ����ȫ·�������������һ��IPSEC��װ�������, 
        ��װ����������ݰ�������IPSKB_REROUTED��־, ��·����������һ������ͨ·��, 
        ������ͨ·�ɵ��������ip_output:
        int ip_output(struct sk_buff *skb)
        {
            struct net_device *dev = skb-<dst-<dev;
            IP_INC_STATS(IPSTATS_MIB_OUTREQUESTS);
            skb-<dev = dev;
            skb-<protocol = htons(ETH_P_IP);
        // ����Ǵ�IPSKB_REROUTED��־�����ݰ�, ������POSTROUTING��SNAT����, ֱ��ִ��
        // ip_finish_output����
            return NF_HOOK_COND(PF_INET, NF_IP_POST_ROUTING, skb, NULL, dev,
                                ip_finish_output,
                                !(IPCB(skb)-<flags & IPSKB_REROUTED));
        }
        ��˶��ڷ�װ�����ݰ�����, �ڷ�װ�����п��Խ���OUTPUT��Ĺ��˺�POSTROUTING���SNAT����, 
        ��һ����װ���, �Ͳ����ٽ���SNAT������.
    ��������С��:
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
10. �ܽ�
    Linux�Դ���native ipsecʵ��xfrm��ͨ��·����ʵ��IPSEC��װ�����, ���freeswan�����Ƶ�, 
    ֻ����freeswan�����������ipsec*�����豸, 
    �����Ϳ���ͨ����׼�����繤����iproute2��ͨ������·�ɺ�ip rule��ʵ�ְ�ȫ����, 
    ������������������ݰ��ͽ���IPSEC���, ���������������İ����ǽ���IPSEC��װ��
    ���ʵ�ֱȽ϶���������NAT-T��Ҫ�޸�udp.cԴ���⣬������������Ҫ�޸��ں�Դ�룬
    ���ڽ����IPSEC�������������Ͽ���ץ��ԭʼ��IPSEC����
    �������������Ͽ���ץ�����ܺ�����ݰ���
    ��xfrmû�ж�������������������·�ɲ��ҹ������Զ����Ұ�ȫ����ʵ��ipsec�Ľ����װ��
    ��˸�ʵ���Ǳ�����ں�������������һ��ģ�
    ���ڽ����IPSEC����������������ץ�����ΰ���һ����IPSECԭʼ����һ���ǽ��ܺ�İ���
    ���ڻ�����Ҫ����·�������з�װ�����Ա��ʻ����ǻ��ڲ��Ե�IPSEC��
    ��������ͨ���������·�ɷ�ʽ��ʵ�ֻ��ڲ���IPSEC��
    Ҫ���ܰ�IPSEC��װ��Ϊһ��netfilter��target�ͺ��ˣ�
    �����Ϳ��Խ��б�׼�Ļ��ڲ��Ե�IPSEC�ˡ�
    xfrm�����������ϣ���������·�ɻ�netfilter����ʱ������ͨ����ر�־���д������·��
    �羭��IPSEC���������ݰ����Զ��������SNAT�����ģ���freeswan��ʵ�־Ͳ��ܱ�֤��
    �������SNAT���򲻶ԣ����п��ܶԷ�װ�õİ�����SNAT��������ɴ���
    ������ʵ�ֶ��ڷ�װǰ�����ݰ����ǿ��Խ���SNAT�����ģ�
    �������ʵ��ͬ����VPN������NAT������xfrm��ʵ�֡�
    ��RFC2367��ֻ������SA��ز�������Ϣ���ͣ���û�ж���SP�Ĳ������ͣ�
    Ҳû�ж���������չ��IPSEC���ܵ������Ϣ���ͣ���NAT-T��ص����ͣ�
    ��ЩSADB_X_*����Ϣ���;��ǷǱ�׼�ģ�
    �����ɸ���IPSECʵ��ֻ���Լ�������Щ��Ϣ���ͣ�
    ��˿��ܻ���ɲ����ݵ�����Ӧ�þ�����µ�RFC������2367�ˡ�