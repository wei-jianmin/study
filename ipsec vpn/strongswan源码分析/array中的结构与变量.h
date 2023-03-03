#ifndef HAVE_QSORT_R
	/* store data to replicate qsort_r in thread local storage */
	static thread_value_t *sort_data;
#endif

struct array_t {
	/** number of elements currently in array (not counting head/tail) */
	uint32_t count;
	/** size of each element, 0 for a pointer based array */
	uint16_t esize;
	/** allocated but unused elements at array front */
	uint8_t head;
	/** allocated but unused elements at array end */
	uint8_t tail;
	/** array elements */
	void *data;
};