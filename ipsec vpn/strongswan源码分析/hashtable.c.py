//hash，equals是两个算法函数的指针，会创建一个 pair_t 的链表管理类，capacity为链表初始容量
hashtable_t *hashtable_create(hashtable_hash_t hash, hashtable_equals_t equals,
                              u_int capacity)
{
    private_hashtable_t *this;
        struct private_hashtable_t {
            hashtable_t public;
                struct hashtable_t {
                    enumerator_t *(*create_enumerator) (hashtable_t *this);
                    void *(*put) (hashtable_t *this, const void *key, void *value);
                    void *(*get) (hashtable_t *this, const void *key);
                    void *(*get_match) (hashtable_t *this, const void *key, hashtable_equals_t match);
                    void *(*remove) (hashtable_t *this, const void *key);
                    void (*remove_at) (hashtable_t *this, enumerator_t *enumerator);
                    u_int (*get_count) (hashtable_t *this);
                    void (*destroy) (hashtable_t *this);
                    void (*destroy_function)(hashtable_t *this, void (*)(void *val, const void *key));
                };
            u_int count;
            u_int capacity;
            u_int mask;
            float load_factor;
            pair_t **table;
                struct pair_t {
                    const void *key;
                    void *value;
                    u_int hash;
                    pair_t *next;
                };
            hashtable_hash_t hash;
                typedef u_int (*hashtable_hash_t)(const void *key);
            hashtable_equals_t equals;
                typedef bool (*hashtable_equals_t)(const void *key, const void *other_key);
        };
    INIT(this,
        .public = {
            .put = _put,
                void* _put(private_hashtable_t *this, const void *key, void *value)
                    pair = 根据key，定位到 this->table的pair项
                    如果 pair项的key == key，则修改该pair项的value值，返回旧的value值
                    如果找不到匹配的 pair 项，则建立进的pair项，追加到哈希表中
            .get = _get,
            .get_match = _get_match,
            .remove = _remove_,
            .remove_at = (void*)_remove_at,
            .get_count = _get_count,
            .create_enumerator = _create_enumerator,
            .destroy = _destroy,
            .destroy_function = _destroy_function,
        },
        .hash = hash,
        .equals = equals,
    );
    init_hashtable(this, capacity);
        capacity = max(1, min(capacity, MAX_CAPACITY));
        this->capacity = get_nearest_powerof2(capacity);
            返回大于参数的最小的2的幂次，
            如 3 --> 4(2^2), 5 --> 8(2^3), 10 --> 16(2^4)
        this->mask = this->capacity - 1;
        this->load_factor = 0.75;
        this->table = calloc(this->capacity, sizeof(pair_t*));
    return &this->public;
}






