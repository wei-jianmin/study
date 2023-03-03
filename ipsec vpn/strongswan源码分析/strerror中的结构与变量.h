/**
 * Thread specific strerror buffer, as char*
 */
static thread_value_t *strerror_buf;

#ifndef HAVE_STRERROR_R
/**
 * Lock to access strerror() safely
 */
static spinlock_t *strerror_lock;
#endif /* HAVE_STRERROR_R */