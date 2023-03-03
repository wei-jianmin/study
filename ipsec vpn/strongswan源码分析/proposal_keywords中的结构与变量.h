/**
 * Class representing a proposal（建议、提议） token.
 * 记录一个算法（主要目的是将一个算法跟一个容易记忆的名字--令牌名关联起来）
 */
struct proposal_token_t {

	/**
	 * The name of the token.
	 */
	char *name;  //令牌名

	/**
	 * The type of transform in the token.
	 */
	transform_type_t type;  //transform.h

	/**
	 * The IKE id of the algorithm.  ike算法id
	 */
	uint16_t algorithm;

	/**
	 * The key size associated with the specific algorithm.
	 */
	uint16_t keysize;
};

/**
 * Class to manage proposal keywords
 * 管理 proposal_token 结构（链表维护），提供注册和检索功能，使用注册的外部算法进行检索
 */
struct proposal_keywords_t {

	/**
	 * Returns the proposal token for the specified string if a token exists.
	 *
	 * @param str		the string containing the name of the token
	 * @return			proposal_token if found, NULL otherwise
	 */
	const proposal_token_t *(*get_token)(proposal_keywords_t *this,
										 const char *str);

	/**
	 * Register a new proposal token for an algorithm.
	 *
	 * @param name		the string containing the name of the token
	 * @param type		the transform_type_t for the token
	 * @param algorithm	the IKE id of the algorithm
	 * @param keysize	the key size associated with the specific algorithm
	 */
	void (*register_token)(proposal_keywords_t *this, const char *name,
						   transform_type_t type, uint16_t algorithm,
						   uint16_t keysize);

	/**
	 * Register an algorithm name parser.
	 *
	 * It is meant to parse an algorithm name into a proposal token in a
	 * generic, user defined way.
	 *
	 * @param parser	a pointer to the parser function
	 */
	void (*register_algname_parser)(proposal_keywords_t *this,
									proposal_algname_parser_t parser);

	/**
	 * Destroy a proposal_keywords_t instance.
	 */
	void (*destroy)(proposal_keywords_t *this);
};

==================================================================

struct private_proposal_keywords_t {

	/**
	 * public interface
	 */
	proposal_keywords_t public;

	/**
	 * registered tokens, as proposal_token_t
	 */
	linked_list_t * tokens;

	/**
	 * registered algname parsers, as proposal_algname_parser_t
	 */
	linked_list_t *parsers;

	/**
	 * rwlock to lock access to modules
	 */
	rwlock_t *lock;
};