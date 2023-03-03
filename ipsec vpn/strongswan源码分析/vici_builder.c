/**
 * Build helper for vici message
 */
struct vici_builder_t {

	/**
	 * Append a generic message element to message.
	 *
	 * The additional arguments are type specific, it may be nothing, a string,
	 * a chunk value or both.
	 *
	 * @param type	element type to add
	 * @param ...	additional type specific arguments
	 */
	void (*add)(vici_builder_t *this, vici_type_t type, ...);

	/**
	 * Append a key/value element using a format string.
	 *
	 * Instead of passing the type specific value as a chunk, this method
	 * takes a printf() style format string followed by its arguments. The
	 * key name for a key/value type is still a fixed string.
	 *
	 * @param key	key name of the key/value to add
	 * @param fmt	value format string
	 * @param ...	arguments to value format string
	 */
	void (*add_kv)(vici_builder_t *this, char *key, char *fmt, ...);

	/**
	 * Append a message element using a format string and va_list.
	 *
	 * Instead of passing the type specific value as a chunk, this method
	 * takes a printf() style format string followed by its arguments. The
	 * key name for a key/value type is still a fixed string.
	 *
	 * @param key	key name of the key/value to add
	 * @param fmt	value format string
	 * @param args	arguments to value format string
	 */
	void (*vadd_kv)(vici_builder_t *this, char *key, char *fmt, va_list args);

	/**
	 * Append a list item element using a format string.
	 *
	 * Instead of passing the type specific value as a chunk, this method
	 * takes a printf() style format string followed by its arguments.
	 *
	 * @param fmt	value format string
	 * @param ...	arguments to value format string
	 */
	void (*add_li)(vici_builder_t *this, char *fmt, ...);

	/**
	 * Append a list item element using a format string and va_list.
	 *
	 * Instead of passing the type specific value as a chunk, this method
	 * takes a printf() style format string followed by its arguments.
	 *
	 * @param fmt	value format string
	 * @param args	arguments to value format string
	 */
	void (*vadd_li)(vici_builder_t *this, char *fmt, va_list args);

	/**
	 * Begin a new section.
	 *
	 * @param name	name of section to begin
	 */
	void (*begin_section)(vici_builder_t *this, char *name);

	/**
	 * End the currently open section.
	 */
	void (*end_section)(vici_builder_t *this);

	/**
	 * Begin a new list.
	 *
	 * @param name	name of list to begin
	 */
	void (*begin_list)(vici_builder_t *this, char *name);

	/**
	 * End the currently open list.
	 */
	void (*end_list)(vici_builder_t *this);

	/**
	 * Finalize a vici message with all added elements, destroy builder.
	 *
	 * @return		vici message, NULL on error
	 */
	vici_message_t* (*finalize)(vici_builder_t *this);

	/**
	 * Destroy a vici builder without finalization.
	 *
	 * Note that finalize() already destroys the message, and calling destroy()
	 * is required only if the message does not get finalize()d.
	 */
	void (*destroy)(vici_builder_t *this);
};

====================================================

struct private_vici_builder_t {

	/**
	 * Public vici_builder_t interface.
	 */
	vici_builder_t public;

	/**
	 * Writer for elements
	 */
	bio_writer_t *writer;

	/**
	 * Errors encountered
	 */
	u_int error;

	/**
	 * Section nesting level
	 */
	u_int section;

	/**
	 * In list element?
	 */
	bool list;
};