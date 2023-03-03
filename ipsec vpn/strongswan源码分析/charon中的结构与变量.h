static FILE *pidfile = NULL;

// hook in library for debugging messages
extern void (*dbg) (debug_t group, level_t level, char *fmt, ...);