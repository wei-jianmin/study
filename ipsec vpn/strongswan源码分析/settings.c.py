settings_t *settings_create(char *file)
{
	private_settings_t *this = settings_create_base();
        private_settings_t *this;
            struct private_settings_t {
                settings_t public;
                    char* (*get_str)(settings_t *this, char *key, char *def, ...);
                    bool (*get_bool)(settings_t *this, char *key, int def, ...);
                    int (*get_int)(settings_t *this, char *key, int def, ...);
                    double (*get_double)(settings_t *this, char *key, double def, ...);
                    uint32_t (*get_time)(settings_t *this, char *key, uint32_t def, ...);
                    void (*set_str)(settings_t *this, char *key, char *value, ...);
                    void (*set_bool)(settings_t *this, char *key, int value, ...);
                    void (*set_int)(settings_t *this, char *key, int value, ...);
                    void (*set_double)(settings_t *this, char *key, double value, ...);
                    void (*set_time)(settings_t *this, char *key, uint32_t value, ...);
                    bool (*set_default_str)(settings_t *this, char *key, char *value, ...);
                    enumerator_t* (*create_section_enumerator)(settings_t *this,char *section, ...);
                    enumerator_t* (*create_key_value_enumerator)(settings_t *this,char *section, ...);
                    void (*add_fallback)(settings_t *this, const char *section, const char *fallback, ...);
                    bool (*load_files)(settings_t *this, char *pattern, bool merge);
                    bool (*load_files_section)(settings_t *this, char *pattern, bool merge, char *section, ...);
                    bool (*load_string)(settings_t *this, char *settings, bool merge);
                    bool (*load_string_section)(settings_t *this, char *settings, bool merge, char *section, ...);
                    void (*destroy)(settings_t *this);
                section_t *top;
                    struct section_t {
                        char *name;
                        array_t *references;
                        array_t *sections;
                        array_t *sections_order;
                        array_t *kv;
                        array_t *kv_order;
                    };
                array_t *contents;
                    struct array_t {
                        uint32_t count;
                        uint16_t esize;
                        uint8_t head;
                        uint8_t tail;
                        void *data;
                    };
                rwlock_t *lock;
            };
        INIT(this,
            .public = {
                .get_str = _get_str,
                .get_int = _get_int,
                .get_double = _get_double,
                .get_time = _get_time,
                .get_bool = _get_bool,
                .set_str = _set_str,
                .set_int = _set_int,
                .set_double = _set_double,
                .set_time = _set_time,
                .set_bool = _set_bool,
                .set_default_str = _set_default_str,
                .create_section_enumerator = _create_section_enumerator,
                .create_key_value_enumerator = _create_key_value_enumerator,
                .add_fallback = _add_fallback,
                .load_files = _load_files,
                .load_files_section = _load_files_section,
                .load_string = _load_string,
                .load_string_section = _load_string_section,
                .destroy = _destroy,
            },
            .top = settings_section_create(NULL),
                section_t *this;
                INIT(this,
                    .name = name,
                );
                return this;
            .contents = array_create(0, 0),
                array_t *array_create(u_int esize, uint8_t reserve)
                {
                    array_t *array;
                    初始化array   
                        为array申请内存
                        array.esize = esize
                        array.reserve = reserve
                    if (array->tail)
                        array->data = malloc(get_size(array, array->tail));
                    return array;
                }
            .lock = rwlock_create(RWLOCK_TYPE_DEFAULT),
        );
        return this;
    load_files(this, file, FALSE);
	return &this->public;
}

bool load_files(private_settings_t *this, char *pattern, bool merge)
{
    section_t *section;
    section = load_internal(pattern, FALSE);
    if (!section) return FALSE;
    this->lock->write_lock(this->lock);
    return extend_section(this, this->top, section, merge);
}

static section_t *load_internal(char *pattern, bool string)
{
	section_t *section;
	bool loaded;
	if (pattern == NULL || !pattern[0])
	{
		return settings_section_create(NULL);
	}
	section = settings_section_create(NULL);
	loaded = string ? settings_parser_parse_string(section, pattern) :
					  settings_parser_parse_file(section, pattern);
	if (!loaded)
	{
		settings_section_destroy(section, NULL);
		section = NULL;
	}
	return section;
}

section_t *settings_section_create(char *name)
{
    section_t *this;
    INIT(this, .name = name,);
    return this;
}

static bool extend_section(private_settings_t *this, section_t *parent,
						   section_t *section, bool merge)
{
	if (parent)
	{
		settings_section_extend(parent, section, this->contents, !merge);
	}
	this->lock->unlock(this->lock);
	settings_section_destroy(section, NULL);
	return parent != NULL;
}