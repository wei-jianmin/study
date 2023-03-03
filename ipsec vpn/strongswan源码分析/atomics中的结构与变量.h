/**
 * Spinlock£¨×ÔĞıËø£© for ref_get/put
 */
static spinlock_t *ref_lock;

/**
 * Spinlock for all compare and swap operations.
 */
static spinlock_t *cas_lock;