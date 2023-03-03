struct command_t {
	/** Function implementing the command */
	int (*call)(vici_conn_t *conn);
	/** short option character */
	char op;
	/** long option string */
	char *cmd;
	/** description of the command */
	char *description;
	/** usage summary of the command */
	char *line[MAX_LINES];
	/** list of options the command accepts */
	command_option_t options[MAX_OPTIONS];
};


struct command_option_t {
	/** long option string of the option */
	char *name;
	/** short option character of the option */
	char op;
	/** expected argument to option, no/req/opt_argument */
	int arg;
	/** description of the option */
	char *desc;
};

=======================================================

static command_t cmds[26];    //Registered commands.
static int active = 0;      //active command.
static int registered = 0;  //number of registered commands
static int help_idx;        //help command index
static char *uri = NULL;    //Uri to connect to
static int argc;
static char **argv;
static options_t *options;
static struct option command_opts[34];  //Global options used by all subcommands
static char command_optstring[34*3];    //Global optstring used by all subcommands

/*
struct option
{
  const char *name;
  int has_arg;
  int *flag;
  int val;
};
*/