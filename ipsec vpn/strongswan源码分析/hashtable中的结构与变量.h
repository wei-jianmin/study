/**
 * Class implementing a hash table.
 *
 * General purpose hash table. This hash table is not synchronized.
 */
struct hashtable_t {

	/**
	 * Create an enumerator over the hash table key/value pairs.
	 *
	 * @return			enumerator over (void *key, void *value)
	 */
	enumerator_t *(*create_enumerator) (hashtable_t *this);

	/**
	 * Adds the given value with the given key to the hash table, if there
	 * exists no entry with that key. NULL is returned in this case.
	 * Otherwise the existing value is replaced and the function returns the
	 * old value.
	 *
	 * @param key		the key to store
	 * @param value		the value to store
	 * @return			NULL if no item was replaced, the old value otherwise
	 */
	void *(*put) (hashtable_t *this, const void *key, void *value);

	/**
	 * Returns the value with the given key, if the hash table contains such an
	 * entry, otherwise NULL is returned.
	 *
	 * @param key		the key of the requested value
	 * @return			the value, NULL if not found
	 */
	void *(*get) (hashtable_t *this, const void *key);

	/**
	 * Returns the value with a matching key, if the hash table contains such an
	 * entry, otherwise NULL is returned.
	 *
	 * Compared to get() the given match function is used to compare the keys
	 * for equality.  The hash function does have to be deviced properly in
	 * order to make this work if the match function compares keys differently
	 * than the equals function provided to the constructor.  This basically
	 * allows to enumerate all entries with the same hash value.
	 *
	 * @param key		the key to match against
	 * @param match		match function to be used when comparing keys
	 * @return			the value, NULL if not found
	 */
	void *(*get_match) (hashtable_t *this, const void *key,
						hashtable_equals_t match);

	/**
	 * Removes the value with the given key from the hash table and returns the
	 * removed value (or NULL if no such value existed).
	 *
	 * @param key		the key of the value to remove
	 * @return			the removed value, NULL if not found
	 */
	void *(*remove) (hashtable_t *this, const void *key);

	/**
	 * Removes the key and value pair from the hash table at which the given
	 * enumerator currently points.
	 *
	 * @param enumerator	enumerator, from create_enumerator
	 */
	void (*remove_at) (hashtable_t *this, enumerator_t *enumerator);

	/**
	 * Gets the number of items in the hash table.
	 *
	 * @return			number of items
	 */
	u_int (*get_count) (hashtable_t *this);

	/**
	 * Destroys a hash table object.
	 */
	void (*destroy) (hashtable_t *this);

	/**
	 * Destroys a hash table object and calls the given function for each
	 * item and its key in the hash table.
	 *
	 * @param function	function to call on each item and key
	 */
	void (*destroy_function)(hashtable_t *this,
							 void (*)(void *val, const void *key));
};

===========================================================================


/**
 * This pair holds a pointer to the key and value it represents.
 */
struct pair_t {
	/**
	 * Key of a hash table item.
	 */
	const void *key;

	/**
	 * Value of a hash table item.
	 */
	void *value;

	/**
	 * Cached hash (used in case of a resize).
	 */
	u_int hash;

	/**
	 * Next pair in an overflow list.
	 */
	pair_t *next;
};

/**
 * Private data of a hashtable_t object.
 *
 */
struct private_hashtable_t {
	/**
	 * Public part of hash table.
	 */
	hashtable_t public;

	/**
	 * The number of items in the hash table.
	 */
	u_int count;

	/**
	 * The current capacity of the hash table (always a power of 2).
	 */
	u_int capacity;

	/**
	 * The current mask to calculate the row index (capacity - 1).
	 */
	u_int mask;

	/**
	 * The load factor.
	 */
	float load_factor;

	/**
	 * The actual table.
	 */
	pair_t **table;

	/**
	 * The hashing function.
	 */
	hashtable_hash_t hash;

	/**
	 * The equality function.
	 */
	hashtable_equals_t equals;
};

/**
 * hash table enumerator implementation
 */
struct private_enumerator_t {

	/**
	 * implements enumerator interface
	 */
	enumerator_t enumerator;

	/**
	 * associated hash table
	 */
	private_hashtable_t *table;

	/**
	 * current row index
	 */
	u_int row;

	/**
	 * number of remaining items in hashtable
	 */
	u_int count;

	/**
	 * current pair
	 */
	pair_t *current;

	/**
	 * previous pair (used by remove_at)
	 */
	pair_t *prev;
};