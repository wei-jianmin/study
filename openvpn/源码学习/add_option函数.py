参： file://openvpn_help.txt

//根据配置参数，设置options的相关项
static void add_option(struct options *options,
                       char *p[],
                       bool is_inline,
                       const char *file,
                       int line,
                       const int level,
                       const int msglevel,
                       const unsigned int permission_mask,
                       unsigned int *option_types_found,
                       struct env_set *es)
{
    struct gc_arena gc = gc_new();
    const bool pull_mode = BOOL_CAST(permission_mask & OPT_P_PULL_MODE);
    int msglevel_fc = msglevel_forward_compatible(options, msglevel);

    ASSERT(MAX_PARMS >= 7);

    /*
     * If directive begins with "setenv opt" prefix, don't raise an error if
     * directive is unrecognized.
     */
    if (streq(p[0], "setenv") && p[1] && streq(p[1], "opt") && !(permission_mask & OPT_P_PULL_MODE))
    {
        if (!p[2])
        {
            p[2] = "setenv opt"; /* will trigger an error that includes setenv opt */
        }
        p += 2;
        msglevel_fc = M_WARN;
    }

    if (!file)
    {
        file = "[CMD-LINE]";
        line = 1;
    }
    if (streq(p[0], "help"))
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        usage();
        if (p[1])
        {
            msg(msglevel, "--help does not accept any parameters");
            goto err;
        }
    }
    if (streq(p[0], "version") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        usage_version();
    }
    else if (streq(p[0], "config") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_CONFIG);

        /* save first config file only in options */
        if (!options->config)
        {
            options->config = p[1];
        }

        read_config_file(options, p[1], level, file, line, msglevel, permission_mask, option_types_found, es);
    }
    #if defined(ENABLE_DEBUG) && !defined(ENABLE_SMALL)
    else if (streq(p[0], "show-gateway") && !p[2])
    {
        struct route_gateway_info rgi;
        struct route_ipv6_gateway_info rgi6;
        struct in6_addr remote = IN6ADDR_ANY_INIT;
        openvpn_net_ctx_t net_ctx;
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (p[1])
        {
            get_ipv6_addr(p[1], &remote, NULL, M_WARN);
        }
        net_ctx_init(NULL, &net_ctx);
        get_default_gateway(&rgi, &net_ctx);
        get_default_gateway_ipv6(&rgi6, &remote, &net_ctx);
        print_default_gateway(M_INFO, &rgi, &rgi6);
        openvpn_exit(OPENVPN_EXIT_STATUS_GOOD); /* exit point */
    }
    #endif
    #if 0
    else if (streq(p[0], "foreign-option") && p[1])
    {
        VERIFY_PERMISSION(OPT_P_IPWIN32);
        foreign_option(options, p, 3, es);
    }
    #endif
    else if (streq(p[0], "echo") || streq(p[0], "parameter"))
    {
        struct buffer string = alloc_buf_gc(OPTION_PARM_SIZE, &gc);
        int j;
        bool good = true;

        VERIFY_PERMISSION(OPT_P_ECHO);

        for (j = 1; j < MAX_PARMS; ++j)
        {
            if (!p[j])
            {
                break;
            }
            if (j > 1)
            {
                good &= buf_printf(&string, " ");
            }
            good &= buf_printf(&string, "%s", p[j]);
        }
        if (good)
        {
            /* only message-related ECHO are logged, since other ECHOs
             * can potentially include security-sensitive strings */
            if (p[1] && strncmp(p[1], "msg", 3) == 0)
            {
                msg(M_INFO, "%s:%s",
                    pull_mode ? "ECHO-PULL" : "ECHO",
                    BSTR(&string));
            }
            #ifdef ENABLE_MANAGEMENT
            if (management)
            {
                management_echo(management, BSTR(&string), pull_mode);
            }
            #endif
        }
        else
        {
            msg(M_WARN, "echo/parameter option overflow");
        }
    }
    #ifdef ENABLE_MANAGEMENT
    else if (streq(p[0], "management") && p[1] && p[2] && !p[4])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (streq(p[2], "unix"))
        {
            #if UNIX_SOCK_SUPPORT
            options->management_flags |= MF_UNIX_SOCK;
            #else
            msg(msglevel, "MANAGEMENT: this platform does not support unix domain sockets");
            goto err;
            #endif
        }

        options->management_addr = p[1];
        options->management_port = p[2];
        if (p[3])
        {
            options->management_user_pass = p[3];
        }
    }
    else if (streq(p[0], "management-client-user") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_client_user = p[1];
    }
    else if (streq(p[0], "management-client-group") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_client_group = p[1];
    }
    else if (streq(p[0], "management-query-passwords") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_flags |= MF_QUERY_PASSWORDS;
    }
    else if (streq(p[0], "management-query-remote") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_flags |= MF_QUERY_REMOTE;
    }
    else if (streq(p[0], "management-query-proxy") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_flags |= MF_QUERY_PROXY;
    }
    else if (streq(p[0], "management-hold") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_flags |= MF_HOLD;
    }
    else if (streq(p[0], "management-signal") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_flags |= MF_SIGNAL;
    }
    else if (streq(p[0], "management-forget-disconnect") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_flags |= MF_FORGET_DISCONNECT;
    }
    else if (streq(p[0], "management-up-down") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_flags |= MF_UP_DOWN;
    }
    else if (streq(p[0], "management-client") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_flags |= MF_CONNECT_AS_CLIENT;
        options->management_write_peer_info_file = p[1];
    }
    #ifdef ENABLE_MANAGEMENT
    else if (streq(p[0], "management-external-key"))
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        for (int j = 1; j < MAX_PARMS && p[j] != NULL; ++j)
        {
            if (streq(p[j], "nopadding"))
            {
                options->management_flags |= MF_EXTERNAL_KEY_NOPADDING;
            }
            else if (streq(p[j], "pkcs1"))
            {
                options->management_flags |= MF_EXTERNAL_KEY_PKCS1PAD;
            }
            else
            {
                msg(msglevel, "Unknown management-external-key flag: %s", p[j]);
            }
        }
        /*
         * When no option is present, assume that only PKCS1
         * padding is supported
         */
        if (!(options->management_flags
              &(MF_EXTERNAL_KEY_NOPADDING | MF_EXTERNAL_KEY_PKCS1PAD)))
        {
            options->management_flags |= MF_EXTERNAL_KEY_PKCS1PAD;
        }
        options->management_flags |= MF_EXTERNAL_KEY;
    }
    else if (streq(p[0], "management-external-cert") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_flags |= MF_EXTERNAL_CERT;
        options->management_certificate = p[1];
    }
    #endif /* ifdef ENABLE_MANAGEMENT */
    #ifdef MANAGEMENT_DEF_AUTH
    else if (streq(p[0], "management-client-auth") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_flags |= MF_CLIENT_AUTH;
    }
    #endif
    #ifdef MANAGEMENT_PF
    else if (streq(p[0], "management-client-pf") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->management_flags |= (MF_CLIENT_PF | MF_CLIENT_AUTH);
    }
    #endif
    else if (streq(p[0], "management-log-cache") && p[1] && !p[2])
    {
        int cache;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        cache = atoi(p[1]);
        if (cache < 1)
        {
            msg(msglevel, "--management-log-cache parameter is out of range");
            goto err;
        }
        options->management_log_history_cache = cache;
    }
    #endif /* ifdef ENABLE_MANAGEMENT */
    #ifdef ENABLE_PLUGIN
    else if (streq(p[0], "plugin") && p[1])
    {
        VERIFY_PERMISSION(OPT_P_PLUGIN);
        if (!options->plugin_list)
        {
            options->plugin_list = plugin_option_list_new(&options->gc);
        }
        if (!plugin_option_list_add(options->plugin_list, &p[1], &options->gc))
        {
            msg(msglevel, "plugin add failed: %s", p[1]);
            goto err;
        }
    }
    #endif
    else if (streq(p[0], "mode") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (streq(p[1], "p2p"))
        {
            options->mode = MODE_POINT_TO_POINT;
        }
        else if (streq(p[1], "server"))
        {
            options->mode = MODE_SERVER;
        }
        else
        {
            msg(msglevel, "Bad --mode parameter: %s", p[1]);
            goto err;
        }
    }
    else if (streq(p[0], "dev") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->dev = p[1];
    }
    else if (streq(p[0], "dev-type") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->dev_type = p[1];
    }
    #ifdef _WIN32
    else if (streq(p[0], "windows-driver") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->windows_driver = parse_windows_driver(p[1], M_FATAL);
    }
    #endif
    else if (streq(p[0], "dev-node") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->dev_node = p[1];
    }
    else if (streq(p[0], "lladdr") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_UP);
        if (mac_addr_safe(p[1])) /* MAC address only */
        {
            options->lladdr = p[1];
        }
        else
        {
            msg(msglevel, "lladdr parm '%s' must be a MAC address", p[1]);
            goto err;
        }
    }
    else if (streq(p[0], "topology") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_UP);
        options->topology = parse_topology(p[1], msglevel);
    }
    else if (streq(p[0], "tun-ipv6") && !p[1])
    {
        if (!pull_mode)
        {
            msg(M_WARN, "Note: option tun-ipv6 is ignored because modern operating systems do not need special IPv6 tun handling anymore.");
        }
    }
    #ifdef ENABLE_IPROUTE
    else if (streq(p[0], "iproute") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        iproute_path = p[1];
    }
    #endif
    else if (streq(p[0], "ifconfig") && p[1] && p[2] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_UP);
        if (ip_or_dns_addr_safe(p[1], options->allow_pull_fqdn) && ip_or_dns_addr_safe(p[2], options->allow_pull_fqdn)) /* FQDN -- may be DNS name */
        {
            options->ifconfig_local = p[1];
            options->ifconfig_remote_netmask = p[2];
        }
        else
        {
            msg(msglevel, "ifconfig parms '%s' and '%s' must be valid addresses", p[1], p[2]);
            goto err;
        }
    }
    else if (streq(p[0], "ifconfig-ipv6") && p[1] && p[2] && !p[3])
    {
        unsigned int netbits;

        VERIFY_PERMISSION(OPT_P_UP);
        if (get_ipv6_addr( p[1], NULL, &netbits, msglevel )
            && ipv6_addr_safe( p[2] ) )
        {
            if (netbits < 64 || netbits > 124)
            {
                msg( msglevel, "ifconfig-ipv6: /netbits must be between 64 and 124, not '/%d'", netbits );
                goto err;
            }

            options->ifconfig_ipv6_local = get_ipv6_addr_no_netbits(p[1], &options->gc);
            options->ifconfig_ipv6_netbits = netbits;
            options->ifconfig_ipv6_remote = p[2];
        }
        else
        {
            msg(msglevel, "ifconfig-ipv6 parms '%s' and '%s' must be valid addresses", p[1], p[2]);
            goto err;
        }
    }
    else if (streq(p[0], "ifconfig-noexec") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_UP);
        options->ifconfig_noexec = true;
    }
    else if (streq(p[0], "ifconfig-nowarn") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_UP);
        options->ifconfig_nowarn = true;
    }
    else if (streq(p[0], "local") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        options->ce.local = p[1];
    }
    else if (streq(p[0], "remote-random") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->remote_random = true;
    }
    else if (streq(p[0], "connection") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INLINE);
        if (is_inline)
        {
            struct options sub;
            struct connection_entry *e;

            init_options(&sub, true);
            sub.ce = options->ce;
            read_config_string("[CONNECTION-OPTIONS]", &sub, p[1], msglevel,
                               OPT_P_CONNECTION, option_types_found, es);
            if (!sub.ce.remote)
            {
                msg(msglevel, "Each 'connection' block must contain exactly one 'remote' directive");
                uninit_options(&sub);
                goto err;
            }

            e = alloc_connection_entry(options, msglevel);
            if (!e)
            {
                uninit_options(&sub);
                goto err;
            }
            *e = sub.ce;
            gc_transfer(&options->gc, &sub.gc);
            uninit_options(&sub);
        }
    }
    else if (streq(p[0], "ignore-unknown-option") && p[1])
    {
        int i;
        int j;
        int numignored = 0;
        const char **ignore;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        /* Find out how many options to be ignored */
        for (i = 1; p[i]; i++)
        {
            numignored++;
        }

        /* add number of options already ignored */
        for (i = 0; options->ignore_unknown_option
             && options->ignore_unknown_option[i]; i++)
        {
            numignored++;
        }

        /* Allocate array */
        ALLOC_ARRAY_GC(ignore, const char *, numignored+1, &options->gc);
        for (i = 0; options->ignore_unknown_option
             && options->ignore_unknown_option[i]; i++)
        {
            ignore[i] = options->ignore_unknown_option[i];
        }

        options->ignore_unknown_option = ignore;

        for (j = 1; p[j]; j++)
        {
            /* Allow the user to specify ignore-unknown-option --opt too */
            if (p[j][0]=='-' && p[j][1]=='-')
            {
                options->ignore_unknown_option[i] = (p[j]+2);
            }
            else
            {
                options->ignore_unknown_option[i] = p[j];
            }
            i++;
        }

        options->ignore_unknown_option[i] = NULL;
    }
    #if ENABLE_MANAGEMENT
    else if (streq(p[0], "http-proxy-override") && p[1] && p[2] && !p[4])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->http_proxy_override = parse_http_proxy_override(p[1], p[2], p[3], msglevel, &options->gc);
        if (!options->http_proxy_override)
        {
            goto err;
        }
    }
    #endif
    else if (streq(p[0], "remote") && p[1] && !p[4])
    {
        struct remote_entry re;
        re.remote = re.remote_port = NULL;
        re.proto = -1;
        re.af = 0;

        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        re.remote = p[1];
        if (p[2])
        {
            re.remote_port = p[2];
            if (p[3])
            {
                const int proto = ascii2proto(p[3]);
                const sa_family_t af = ascii2af(p[3]);
                if (proto < 0)
                {
                    msg(msglevel,
                        "remote: bad protocol associated with host %s: '%s'",
                        p[1], p[3]);
                    goto err;
                }
                re.proto = proto;
                re.af = af;
            }
        }
        if (permission_mask & OPT_P_GENERAL)
        {
            struct remote_entry *e = alloc_remote_entry(options, msglevel);
            if (!e)
            {
                goto err;
            }
            *e = re;
        }
        else if (permission_mask & OPT_P_CONNECTION)
        {
            connection_entry_load_re(&options->ce, &re);
        }
    }
    else if (streq(p[0], "resolv-retry") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (streq(p[1], "infinite"))
        {
            options->resolve_retry_seconds = RESOLV_RETRY_INFINITE;
        }
        else
        {
            options->resolve_retry_seconds = positive_atoi(p[1]);
        }
    }
    else if ((streq(p[0], "preresolve") || streq(p[0], "ip-remote-hint")) && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->resolve_in_advance = true;
        /* Note the ip-remote-hint and the argument p[1] are for
         * backward compatibility */
        if (p[1])
        {
            options->ip_remote_hint = p[1];
        }
    }
    else if (streq(p[0], "connect-retry") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        options->ce.connect_retry_seconds = positive_atoi(p[1]);
        /*
         * Limit the base value of retry wait interval to 16 bits to avoid
         * overflow when scaled up for exponential backoff
         */
        if (options->ce.connect_retry_seconds > 0xFFFF)
        {
            options->ce.connect_retry_seconds = 0xFFFF;
            msg(M_WARN, "connect retry wait interval truncated to %d",
                options->ce.connect_retry_seconds);
        }

        if (p[2])
        {
            options->ce.connect_retry_seconds_max =
                max_int(positive_atoi(p[2]), options->ce.connect_retry_seconds);
        }
    }
    else if ((streq(p[0], "connect-timeout") || streq(p[0], "server-poll-timeout"))
             && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        options->ce.connect_timeout = positive_atoi(p[1]);
    }
    else if (streq(p[0], "connect-retry-max") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        options->connect_retry_max = positive_atoi(p[1]);
    }
    else if (streq(p[0], "ipchange") && p[1])
    {
        VERIFY_PERMISSION(OPT_P_SCRIPT);
        if (!no_more_than_n_args(msglevel, p, 2, NM_QUOTE_HINT))
        {
            goto err;
        }
        set_user_script(options,
                        &options->ipchange,
                        string_substitute(p[1], ',', ' ', &options->gc),
                        "ipchange", true);
    }
    else if (streq(p[0], "float") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        options->ce.remote_float = true;
    }
    #ifdef ENABLE_DEBUG
    else if (streq(p[0], "gremlin") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->gremlin = positive_atoi(p[1]);
    }
    #endif
    else if (streq(p[0], "chroot") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->chroot_dir = p[1];
    }
    else if (streq(p[0], "cd") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (platform_chdir(p[1]))
        {
            msg(M_ERR, "cd to '%s' failed", p[1]);
            goto err;
        }
        options->cd_dir = p[1];
    }
    #ifdef ENABLE_SELINUX
    else if (streq(p[0], "setcon") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->selinux_context = p[1];
    }
    #endif
    else if (streq(p[0], "writepid") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->writepid = p[1];
    }
    else if (streq(p[0], "up") && p[1])
    {
        VERIFY_PERMISSION(OPT_P_SCRIPT);
        if (!no_more_than_n_args(msglevel, p, 2, NM_QUOTE_HINT))
        {
            goto err;
        }
        set_user_script(options, &options->up_script, p[1], "up", false);
    }
    else if (streq(p[0], "down") && p[1])
    {
        VERIFY_PERMISSION(OPT_P_SCRIPT);
        if (!no_more_than_n_args(msglevel, p, 2, NM_QUOTE_HINT))
        {
            goto err;
        }
        set_user_script(options, &options->down_script, p[1], "down", true);
    }
    else if (streq(p[0], "down-pre") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->down_pre = true;
    }
    else if (streq(p[0], "up-delay") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->up_delay = true;
    }
    else if (streq(p[0], "up-restart") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->up_restart = true;
    }
    else if (streq(p[0], "syslog") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        open_syslog(p[1], false);
    }
    else if (streq(p[0], "daemon") && !p[2])
    {
        bool didit = false;
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (!options->daemon)
        {
            options->daemon = didit = true;
            open_syslog(p[1], false);
        }
        if (p[1])
        {
            if (!didit)
            {
                msg(M_WARN, "WARNING: Multiple --daemon directives specified, ignoring --daemon %s. (Note that initscripts sometimes add their own --daemon directive.)", p[1]);
                goto err;
            }
        }
    }
    else if (streq(p[0], "inetd") && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (!options->inetd)
        {
            int z;
            const char *name = NULL;
            const char *opterr = "when --inetd is used with two parameters, one of them must be 'wait' or 'nowait' and the other must be a daemon name to use for system logging";

            options->inetd = -1;

            for (z = 1; z <= 2; ++z)
            {
                if (p[z])
                {
                    if (streq(p[z], "wait"))
                    {
                        if (options->inetd != -1)
                        {
                            msg(msglevel, "%s", opterr);
                            goto err;
                        }
                        else
                        {
                            options->inetd = INETD_WAIT;
                        }
                    }
                    else if (streq(p[z], "nowait"))
                    {
                        if (options->inetd != -1)
                        {
                            msg(msglevel, "%s", opterr);
                            goto err;
                        }
                        else
                        {
                            options->inetd = INETD_NOWAIT;
                        }
                    }
                    else
                    {
                        if (name != NULL)
                        {
                            msg(msglevel, "%s", opterr);
                            goto err;
                        }
                        name = p[z];
                    }
                }
            }

            /* default */
            if (options->inetd == -1)
            {
                options->inetd = INETD_WAIT;
            }

            save_inetd_socket_descriptor();
            open_syslog(name, true);
        }
    }
    else if (streq(p[0], "log") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->log = true;
        redirect_stdout_stderr(p[1], false);
    }
    else if (streq(p[0], "suppress-timestamps") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->suppress_timestamps = true;
        set_suppress_timestamps(true);
    }
    else if (streq(p[0], "machine-readable-output") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->machine_readable_output = true;
        set_machine_readable_output(true);
    }
    else if (streq(p[0], "log-append") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->log = true;
        redirect_stdout_stderr(p[1], true);
    }
    #ifdef ENABLE_MEMSTATS
    else if (streq(p[0], "memstats") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->memstats_fn = p[1];
    }
    #endif
    else if (streq(p[0], "mlock") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->mlock = true;
    }
    #if ENABLE_IP_PKTINFO
    else if (streq(p[0], "multihome") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->sockflags |= SF_USE_IP_PKTINFO;
    }
    #endif
    else if (streq(p[0], "verb") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_MESSAGES);
        options->verbosity = positive_atoi(p[1]);
        if (options->verbosity >= (D_TLS_DEBUG_MED & M_DEBUG_LEVEL))
        {
            /* We pass this flag to the SSL library to avoid
             * mbed TLS always generating debug level logging */
            options->ssl_flags |= SSLF_TLS_DEBUG_ENABLED;
        }
        #if !defined(ENABLE_DEBUG) && !defined(ENABLE_SMALL)
        /* Warn when a debug verbosity is supplied when built without debug support */
        if (options->verbosity >= 7)
        {
            msg(M_WARN, "NOTE: debug verbosity (--verb %d) is enabled but this build lacks debug support.",
                options->verbosity);
        }
        #endif
    }
    else if (streq(p[0], "mute") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_MESSAGES);
        options->mute = positive_atoi(p[1]);
    }
    else if (streq(p[0], "errors-to-stderr") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_MESSAGES);
        errors_to_stderr();
    }
    else if (streq(p[0], "status") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->status_file = p[1];
        if (p[2])
        {
            options->status_file_update_freq = positive_atoi(p[2]);
        }
    }
    else if (streq(p[0], "status-version") && p[1] && !p[2])
    {
        int version;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        version = atoi(p[1]);
        if (version < 1 || version > 3)
        {
            msg(msglevel, "--status-version must be 1 to 3");
            goto err;
        }
        options->status_file_version = version;
    }
    else if (streq(p[0], "remap-usr1") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (streq(p[1], "SIGHUP"))
        {
            options->remap_sigusr1 = SIGHUP;
        }
        else if (streq(p[1], "SIGTERM"))
        {
            options->remap_sigusr1 = SIGTERM;
        }
        else
        {
            msg(msglevel, "--remap-usr1 parm must be 'SIGHUP' or 'SIGTERM'");
            goto err;
        }
    }
    else if ((streq(p[0], "link-mtu") || streq(p[0], "udp-mtu")) && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_MTU|OPT_P_CONNECTION);
        options->ce.link_mtu = positive_atoi(p[1]);
        options->ce.link_mtu_defined = true;
    }
    else if (streq(p[0], "tun-mtu") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_MTU|OPT_P_CONNECTION);
        options->ce.tun_mtu = positive_atoi(p[1]);
        options->ce.tun_mtu_defined = true;
    }
    else if (streq(p[0], "tun-mtu-extra") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_MTU|OPT_P_CONNECTION);
        options->ce.tun_mtu_extra = positive_atoi(p[1]);
        options->ce.tun_mtu_extra_defined = true;
    }
    #ifdef ENABLE_FRAGMENT
    else if (streq(p[0], "mtu-dynamic"))
    {
        VERIFY_PERMISSION(OPT_P_MTU|OPT_P_CONNECTION);
        msg(msglevel, "--mtu-dynamic has been replaced by --fragment");
        goto err;
    }
    else if (streq(p[0], "fragment") && p[1] && !p[2])
    {
        /* VERIFY_PERMISSION (OPT_P_MTU); */
        VERIFY_PERMISSION(OPT_P_MTU|OPT_P_CONNECTION);
        options->ce.fragment = positive_atoi(p[1]);
    }
#   endif
    else if (streq(p[0], "mtu-disc") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_MTU|OPT_P_CONNECTION);
        options->ce.mtu_discover_type = translate_mtu_discover_type_name(p[1]);
    }
    else if (streq(p[0], "mtu-test") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->mtu_test = true;
    }
    else if (streq(p[0], "nice") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_NICE);
        options->nice = atoi(p[1]);
    }
    else if (streq(p[0], "rcvbuf") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_SOCKBUF);
        options->rcvbuf = positive_atoi(p[1]);
    }
    else if (streq(p[0], "sndbuf") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_SOCKBUF);
        options->sndbuf = positive_atoi(p[1]);
    }
    else if (streq(p[0], "mark") && p[1] && !p[2])
    {
        #if defined(TARGET_LINUX) && HAVE_DECL_SO_MARK
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->mark = atoi(p[1]);
        #endif
    }
    else if (streq(p[0], "socket-flags"))
    {
        int j;
        VERIFY_PERMISSION(OPT_P_SOCKFLAGS);
        for (j = 1; j < MAX_PARMS && p[j]; ++j)
        {
            if (streq(p[j], "TCP_NODELAY"))
            {
                options->sockflags |= SF_TCP_NODELAY;
            }
            else
            {
                msg(msglevel, "unknown socket flag: %s", p[j]);
            }
        }
    }
    #ifdef TARGET_LINUX
    else if (streq (p[0], "bind-dev") && p[1])
    {
        VERIFY_PERMISSION (OPT_P_SOCKFLAGS);
        options->bind_dev = p[1];
    }
    #endif
    else if (streq(p[0], "txqueuelen") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        #ifdef TARGET_LINUX
        options->tuntap_options.txqueuelen = positive_atoi(p[1]);
        #else
        msg(msglevel, "--txqueuelen not supported on this OS");
        goto err;
        #endif
    }
    else if (streq(p[0], "shaper") && p[1] && !p[2])
    {
        #ifdef ENABLE_FEATURE_SHAPER
        int shaper;

        VERIFY_PERMISSION(OPT_P_SHAPER);
        shaper = atoi(p[1]);
        if (shaper < SHAPER_MIN || shaper > SHAPER_MAX)
        {
            msg(msglevel, "Bad shaper value, must be between %d and %d",
                SHAPER_MIN, SHAPER_MAX);
            goto err;
        }
        options->shaper = shaper;
        #else /* ENABLE_FEATURE_SHAPER */
        VERIFY_PERMISSION(OPT_P_GENERAL);
        msg(msglevel, "--shaper requires the gettimeofday() function which is missing");
        goto err;
        #endif /* ENABLE_FEATURE_SHAPER */
    }
    else if (streq(p[0], "port") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        options->ce.local_port = options->ce.remote_port = p[1];
    }
    else if (streq(p[0], "lport") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        options->ce.local_port_defined = true;
        options->ce.local_port = p[1];
    }
    else if (streq(p[0], "rport") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        options->ce.remote_port = p[1];
    }
    else if (streq(p[0], "bind") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        options->ce.bind_defined = true;
        if (p[1] && streq(p[1], "ipv6only"))
        {
            options->ce.bind_ipv6_only = true;
        }

    }
    else if (streq(p[0], "nobind") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        options->ce.bind_local = false;
    }
    else if (streq(p[0], "fast-io") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->fast_io = true;
    }
    else if (streq(p[0], "inactive") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_TIMER);
        options->inactivity_timeout = positive_atoi(p[1]);
        if (p[2])
        {
            options->inactivity_minimum_bytes = positive_atoi(p[2]);
        }
    }
    else if (streq(p[0], "proto") && p[1] && !p[2])
    {
        int proto;
        sa_family_t af;
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        proto = ascii2proto(p[1]);
        af = ascii2af(p[1]);
        if (proto < 0)
        {
            msg(msglevel,
                "Bad protocol: '%s'. Allowed protocols with --proto option: %s",
                p[1],
                proto2ascii_all(&gc));
            goto err;
        }
        options->ce.proto = proto;
        options->ce.af = af;
    }
    else if (streq(p[0], "proto-force") && p[1] && !p[2])
    {
        int proto_force;
        VERIFY_PERMISSION(OPT_P_GENERAL);
        proto_force = ascii2proto(p[1]);
        if (proto_force < 0)
        {
            msg(msglevel, "Bad --proto-force protocol: '%s'", p[1]);
            goto err;
        }
        options->proto_force = proto_force;
    }
    else if (streq(p[0], "http-proxy") && p[1] && !p[5])
    {
        struct http_proxy_options *ho;

        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);

        {
            if (!p[2])
            {
                msg(msglevel, "http-proxy port number not defined");
                goto err;
            }

            ho = init_http_proxy_options_once(&options->ce.http_proxy_options, &options->gc);

            ho->server = p[1];
            ho->port = p[2];
        }

        if (p[3])
        {
            /* auto -- try to figure out proxy addr, port, and type automatically */
            /* semiauto -- given proxy addr:port, try to figure out type automatically */
            /* (auto|semiauto)-nct -- disable proxy auth cleartext protocols (i.e. basic auth) */
            if (streq(p[3], "auto"))
            {
                ho->auth_retry = PAR_ALL;
            }
            else if (streq(p[3], "auto-nct"))
            {
                ho->auth_retry = PAR_NCT;
            }
            else
            {
                ho->auth_method_string = "basic";
                ho->auth_file = p[3];

                if (p[4])
                {
                    ho->auth_method_string = p[4];
                }
            }
        }
        else
        {
            ho->auth_method_string = "none";
        }
    }
    else if (streq(p[0], "http-proxy-user-pass") && p[1])
    {
        struct http_proxy_options *ho;
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INLINE);
        ho = init_http_proxy_options_once(&options->ce.http_proxy_options, &options->gc);
        ho->auth_file = p[1];
        ho->inline_creds = is_inline;
    }
    else if (streq(p[0], "http-proxy-retry") || streq(p[0], "socks-proxy-retry"))
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        msg(M_WARN, "DEPRECATED OPTION: http-proxy-retry and socks-proxy-retry: "
            "In tzvpn 1.0 proxy connection retries are handled like regular connections. "
            "Use connect-retry-max 1 to get a similar behavior as before.");
    }
    else if (streq(p[0], "http-proxy-timeout") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        msg(M_WARN, "DEPRECATED OPTION: http-proxy-timeout: In tzvpn 1.0 the timeout until a connection to a "
            "server is established is managed with a single timeout set by connect-timeout");
    }
    else if (streq(p[0], "http-proxy-option") && p[1] && !p[4])
    {
        struct http_proxy_options *ho;

        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        ho = init_http_proxy_options_once(&options->ce.http_proxy_options, &options->gc);

        if (streq(p[1], "VERSION") && p[2] && !p[3])
        {
            ho->http_version = p[2];
        }
        else if (streq(p[1], "AGENT") && p[2] && !p[3])
        {
            ho->user_agent = p[2];
        }
        else if ((streq(p[1], "EXT1") || streq(p[1], "EXT2") || streq(p[1], "CUSTOM-HEADER"))
                 && p[2])
        {
            /* In the wild patched versions use both EXT1/2 and CUSTOM-HEADER
             * with either two argument or one */

            struct http_custom_header *custom_header = NULL;
            int i;
            /* Find the first free header */
            for (i = 0; i < MAX_CUSTOM_HTTP_HEADER; i++)
            {
                if (!ho->custom_headers[i].name)
                {
                    custom_header = &ho->custom_headers[i];
                    break;
                }
            }
            if (!custom_header)
            {
                msg(msglevel, "Cannot use more than %d http-proxy-option CUSTOM-HEADER : '%s'", MAX_CUSTOM_HTTP_HEADER, p[1]);
            }
            else
            {
                /* We will save p[2] and p[3], the proxy code will detect if
                 * p[3] is NULL */
                custom_header->name = p[2];
                custom_header->content = p[3];
            }
        }
        else
        {
            msg(msglevel, "Bad http-proxy-option or missing or extra parameter: '%s'", p[1]);
        }
    }
    else if (streq(p[0], "socks-proxy") && p[1] && !p[4])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);

        if (p[2])
        {
            options->ce.socks_proxy_port = p[2];
        }
        else
        {
            options->ce.socks_proxy_port = "1080";
        }
        options->ce.socks_proxy_server = p[1];
        options->ce.socks_proxy_authfile = p[3]; /* might be NULL */
    }
    else if (streq(p[0], "keepalive") && p[1] && p[2] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->keepalive_ping = atoi(p[1]);
        options->keepalive_timeout = atoi(p[2]);
    }
    else if (streq(p[0], "ping") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_TIMER);
        options->ping_send_timeout = positive_atoi(p[1]);
    }
    else if (streq(p[0], "ping-exit") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_TIMER);
        options->ping_rec_timeout = positive_atoi(p[1]);
        options->ping_rec_timeout_action = PING_EXIT;
    }
    else if (streq(p[0], "ping-restart") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_TIMER);
        options->ping_rec_timeout = positive_atoi(p[1]);
        options->ping_rec_timeout_action = PING_RESTART;
    }
    else if (streq(p[0], "ping-timer-rem") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_TIMER);
        options->ping_timer_remote = true;
    }
    else if (streq(p[0], "explicit-exit-notify") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION|OPT_P_EXPLICIT_NOTIFY);
        if (p[1])
        {
            options->ce.explicit_exit_notification = positive_atoi(p[1]);
        }
        else
        {
            options->ce.explicit_exit_notification = 1;
        }
    }
    else if (streq(p[0], "persist-tun") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_PERSIST);
        options->persist_tun = true;
    }
    else if (streq(p[0], "persist-key") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_PERSIST);
        options->persist_key = true;
    }
    else if (streq(p[0], "persist-local-ip") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_PERSIST_IP);
        options->persist_local_ip = true;
    }
    else if (streq(p[0], "persist-remote-ip") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_PERSIST_IP);
        options->persist_remote_ip = true;
    }
    else if (streq(p[0], "client-nat") && p[1] && p[2] && p[3] && p[4] && !p[5])
    {
        VERIFY_PERMISSION(OPT_P_ROUTE);
        cnol_check_alloc(options);
        add_client_nat_to_option_list(options->client_nat, p[1], p[2], p[3], p[4], msglevel);
    }
    else if (streq(p[0], "route") && p[1] && !p[5])
    {
        VERIFY_PERMISSION(OPT_P_ROUTE);
        rol_check_alloc(options);
        if (pull_mode)
        {
            if (!ip_or_dns_addr_safe(p[1], options->allow_pull_fqdn) && !is_special_addr(p[1])) /* FQDN -- may be DNS name */
            {
                msg(msglevel, "route parameter network/IP '%s' must be a valid address", p[1]);
                goto err;
            }
            if (p[2] && !ip_addr_dotted_quad_safe(p[2])) /* FQDN -- must be IP address */
            {
                msg(msglevel, "route parameter netmask '%s' must be an IP address", p[2]);
                goto err;
            }
            if (p[3] && !ip_or_dns_addr_safe(p[3], options->allow_pull_fqdn) && !is_special_addr(p[3])) /* FQDN -- may be DNS name */
            {
                msg(msglevel, "route parameter gateway '%s' must be a valid address", p[3]);
                goto err;
            }
        }
        add_route_to_option_list(options->routes, p[1], p[2], p[3], p[4]);
    }
    else if (streq(p[0], "route-ipv6") && p[1] && !p[4])
    {
        VERIFY_PERMISSION(OPT_P_ROUTE);
        rol6_check_alloc(options);
        if (pull_mode)
        {
            if (!ipv6_addr_safe_hexplusbits(p[1]))
            {
                msg(msglevel, "route-ipv6 parameter network/IP '%s' must be a valid address", p[1]);
                goto err;
            }
            if (p[2] && !ipv6_addr_safe(p[2]))
            {
                msg(msglevel, "route-ipv6 parameter gateway '%s' must be a valid address", p[2]);
                goto err;
            }
            /* p[3] is metric, if present */
        }
        add_route_ipv6_to_option_list(options->routes_ipv6, p[1], p[2], p[3]);
    }
    else if (streq(p[0], "max-routes") && !p[2])
    {
        msg(M_WARN, "DEPRECATED OPTION: --max-routes option ignored."
            "The number of routes is unlimited as of tzvpn 1.0. "
            "This option will be removed in a future version, "
            "please remove it from your configuration.");
    }
    else if (streq(p[0], "route-gateway") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_ROUTE_EXTRAS);
        if (streq(p[1], "dhcp"))
        {
            options->route_gateway_via_dhcp = true;
        }
        else
        {
            if (ip_or_dns_addr_safe(p[1], options->allow_pull_fqdn) || is_special_addr(p[1])) /* FQDN -- may be DNS name */
            {
                options->route_default_gateway = p[1];
            }
            else
            {
                msg(msglevel, "route-gateway parm '%s' must be a valid address", p[1]);
                goto err;
            }
        }
    }
    else if (streq(p[0], "route-ipv6-gateway") && p[1] && !p[2])
    {
        if (ipv6_addr_safe(p[1]))
        {
            options->route_ipv6_default_gateway = p[1];
        }
        else
        {
            msg(msglevel, "route-ipv6-gateway parm '%s' must be a valid address", p[1]);
            goto err;
        }
    }
    else if (streq(p[0], "route-metric") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_ROUTE);
        options->route_default_metric = positive_atoi(p[1]);
    }
    else if (streq(p[0], "route-delay") && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_ROUTE_EXTRAS);
        options->route_delay_defined = true;
        if (p[1])
        {
            options->route_delay = positive_atoi(p[1]);
            if (p[2])
            {
                options->route_delay_window = positive_atoi(p[2]);
            }
        }
        else
        {
            options->route_delay = 0;
        }
    }
    else if (streq(p[0], "route-up") && p[1])
    {
        VERIFY_PERMISSION(OPT_P_SCRIPT);
        if (!no_more_than_n_args(msglevel, p, 2, NM_QUOTE_HINT))
        {
            goto err;
        }
        set_user_script(options, &options->route_script, p[1], "route-up", false);
    }
    else if (streq(p[0], "route-pre-down") && p[1])
    {
        VERIFY_PERMISSION(OPT_P_SCRIPT);
        if (!no_more_than_n_args(msglevel, p, 2, NM_QUOTE_HINT))
        {
            goto err;
        }
        set_user_script(options,
                        &options->route_predown_script,
                        p[1],
                        "route-pre-down", true);
    }
    else if (streq(p[0], "route-noexec") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_SCRIPT);
        options->route_noexec = true;
    }
    else if (streq(p[0], "route-nopull") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->route_nopull = true;
    }
    else if (streq(p[0], "pull-filter") && p[1] && p[2] && !p[3])
    {
        struct pull_filter *f;
        VERIFY_PERMISSION(OPT_P_GENERAL)
        f = alloc_pull_filter(options, msglevel);

        if (strcmp("accept", p[1]) == 0)
        {
            f->type = PUF_TYPE_ACCEPT;
        }
        else if (strcmp("ignore", p[1]) == 0)
        {
            f->type = PUF_TYPE_IGNORE;
        }
        else if (strcmp("reject", p[1]) == 0)
        {
            f->type = PUF_TYPE_REJECT;
        }
        else
        {
            msg(msglevel, "Unknown --pull-filter type: %s", p[1]);
            goto err;
        }
        f->pattern = p[2];
        f->size = strlen(p[2]);
    }
    else if (streq(p[0], "allow-pull-fqdn") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->allow_pull_fqdn = true;
    }
    else if (streq(p[0], "redirect-gateway") || streq(p[0], "redirect-private"))
    {
        int j;
        VERIFY_PERMISSION(OPT_P_ROUTE);
        rol_check_alloc(options);

        if (options->routes->flags & RG_ENABLE)
        {
            msg(M_WARN,
                "WARNING: You have specified redirect-gateway and "
                "redirect-private at the same time (or the same option "
                "multiple times). This is not well supported and may lead to "
                "unexpected results");
        }

        options->routes->flags |= RG_ENABLE;

        if (streq(p[0], "redirect-gateway"))
        {
            options->routes->flags |= RG_REROUTE_GW;
        }
        for (j = 1; j < MAX_PARMS && p[j] != NULL; ++j)
        {
            if (streq(p[j], "local"))
            {
                options->routes->flags |= RG_LOCAL;
            }
            else if (streq(p[j], "autolocal"))
            {
                options->routes->flags |= RG_AUTO_LOCAL;
            }
            else if (streq(p[j], "def1"))
            {
                options->routes->flags |= RG_DEF1;
            }
            else if (streq(p[j], "bypass-dhcp"))
            {
                options->routes->flags |= RG_BYPASS_DHCP;
            }
            else if (streq(p[j], "bypass-dns"))
            {
                options->routes->flags |= RG_BYPASS_DNS;
            }
            else if (streq(p[j], "block-local"))
            {
                options->routes->flags |= RG_BLOCK_LOCAL;
            }
            else if (streq(p[j], "ipv6"))
            {
                rol6_check_alloc(options);
                options->routes_ipv6->flags |= RG_REROUTE_GW;
            }
            else if (streq(p[j], "!ipv4"))
            {
                options->routes->flags &= ~(RG_REROUTE_GW | RG_ENABLE);
            }
            else
            {
                msg(msglevel, "unknown --%s flag: %s", p[0], p[j]);
                goto err;
            }
        }
        #ifdef _WIN32
        /* we need this here to handle pushed --redirect-gateway */
        remap_redirect_gateway_flags(options);
        #endif
    }
    else if (streq(p[0], "block-ipv6") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_ROUTE);
        options->block_ipv6 = true;
    }
    else if (streq(p[0], "remote-random-hostname") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->sockflags |= SF_HOST_RANDOMIZE;
    }
    else if (streq(p[0], "setenv") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (streq(p[1], "REMOTE_RANDOM_HOSTNAME") && !p[2])
        {
            options->sockflags |= SF_HOST_RANDOMIZE;
        }
        else if (streq(p[1], "GENERIC_CONFIG"))
        {
            msg(msglevel, "this is a generic configuration and cannot directly be used");
            goto err;
        }
        else if (streq(p[1], "PUSH_PEER_INFO") && !p[2])
        {
            options->push_peer_info = true;
        }
        else if (streq(p[1], "SERVER_POLL_TIMEOUT") && p[2])
        {
            options->ce.connect_timeout = positive_atoi(p[2]);
        }
        else
        {
            if (streq(p[1], "FORWARD_COMPATIBLE") && p[2] && streq(p[2], "1"))
            {
                options->forward_compatible = true;
                msglevel_fc = msglevel_forward_compatible(options, msglevel);
            }
            setenv_str(es, p[1], p[2] ? p[2] : "");
        }
    }
    else if (streq(p[0], "setenv-safe") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_SETENV);
        setenv_str_safe(es, p[1], p[2] ? p[2] : "");
    }
    else if (streq(p[0], "script-security") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        script_security_set(atoi(p[1]));
    }
    else if (streq(p[0], "mssfix") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);
        if (p[1])
        {
            options->ce.mssfix = positive_atoi(p[1]);
        }
        else
        {
            options->ce.mssfix_default = true;
        }

    }
    else if (streq(p[0], "disable-occ") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->occ = false;
    }
    #if P2MP
    else if (streq(p[0], "server") && p[1] && p[2] && !p[4])
    {
        const int lev = M_WARN;
        bool error = false;
        in_addr_t network, netmask;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        network = get_ip_addr(p[1], lev, &error);
        netmask = get_ip_addr(p[2], lev, &error);
        if (error || !network || !netmask)
        {
            msg(msglevel, "error parsing --server parameters");
            goto err;
        }
        options->server_defined = true;
        options->server_network = network;
        options->server_netmask = netmask;

        if (p[3])
        {
            if (streq(p[3], "nopool"))
            {
                options->server_flags |= SF_NOPOOL;
            }
            else
            {
                msg(msglevel, "error parsing --server: %s is not a recognized flag", p[3]);
                goto err;
            }
        }
    }
    else if (streq(p[0], "server-ipv6") && p[1] && !p[3])
    {
        const int lev = M_WARN;
        struct in6_addr network;
        unsigned int netbits = 0;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (!get_ipv6_addr(p[1], &network, &netbits, lev) )
        {
            msg(msglevel, "error parsing --server-ipv6 parameter");
            goto err;
        }
        if (netbits < 64 || netbits > 124)
        {
            msg(msglevel,
                "--server-ipv6 settings: network must be between /64 and /124 (not /%d)",
                netbits);

            goto err;
        }
        options->server_ipv6_defined = true;
        options->server_network_ipv6 = network;
        options->server_netbits_ipv6 = netbits;

        if (p[2])       /* no "nopool" options or similar for IPv6 */
        {
            msg(msglevel, "error parsing --server-ipv6: %s is not a recognized flag", p[3]);
            goto err;
        }
    }
    else if (streq(p[0], "server-bridge") && p[1] && p[2] && p[3] && p[4] && !p[5])
    {
        const int lev = M_WARN;
        bool error = false;
        in_addr_t ip, netmask, pool_start, pool_end;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        ip = get_ip_addr(p[1], lev, &error);
        netmask = get_ip_addr(p[2], lev, &error);
        pool_start = get_ip_addr(p[3], lev, &error);
        pool_end = get_ip_addr(p[4], lev, &error);
        if (error || !ip || !netmask || !pool_start || !pool_end)
        {
            msg(msglevel, "error parsing --server-bridge parameters");
            goto err;
        }
        options->server_bridge_defined = true;
        options->server_bridge_ip = ip;
        options->server_bridge_netmask = netmask;
        options->server_bridge_pool_start = pool_start;
        options->server_bridge_pool_end = pool_end;
    }
    else if (streq(p[0], "server-bridge") && p[1] && streq(p[1], "nogw") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->server_bridge_proxy_dhcp = true;
        options->server_flags |= SF_NO_PUSH_ROUTE_GATEWAY;
    }
    else if (streq(p[0], "server-bridge") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->server_bridge_proxy_dhcp = true;
    }
    else if (streq(p[0], "push") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_PUSH);
        push_options(options, &p[1], msglevel, &options->gc);
    }
    else if (streq(p[0], "push-reset") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_INSTANCE);
        push_reset(options);
    }
    else if (streq(p[0], "push-remove") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_INSTANCE);
        msg(D_PUSH, "PUSH_REMOVE '%s'", p[1]);
        push_remove_option(options,p[1]);
    }
    else if (streq(p[0], "ifconfig-pool") && p[1] && p[2] && !p[4])
    {
        const int lev = M_WARN;
        bool error = false;
        in_addr_t start, end, netmask = 0;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        start = get_ip_addr(p[1], lev, &error);
        end = get_ip_addr(p[2], lev, &error);
        if (p[3])
        {
            netmask = get_ip_addr(p[3], lev, &error);
        }
        if (error)
        {
            msg(msglevel, "error parsing --ifconfig-pool parameters");
            goto err;
        }
        if (!ifconfig_pool_verify_range(msglevel, start, end))
        {
            goto err;
        }

        options->ifconfig_pool_defined = true;
        options->ifconfig_pool_start = start;
        options->ifconfig_pool_end = end;
        if (netmask)
        {
            options->ifconfig_pool_netmask = netmask;
        }
    }
    else if (streq(p[0], "ifconfig-pool-persist") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->ifconfig_pool_persist_filename = p[1];
        if (p[2])
        {
            options->ifconfig_pool_persist_refresh_freq = positive_atoi(p[2]);
        }
    }
    else if (streq(p[0], "ifconfig-ipv6-pool") && p[1] && !p[2])
    {
        const int lev = M_WARN;
        struct in6_addr network;
        unsigned int netbits = 0;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (!get_ipv6_addr(p[1], &network, &netbits, lev ) )
        {
            msg(msglevel, "error parsing --ifconfig-ipv6-pool parameters");
            goto err;
        }
        if (netbits < 64 || netbits > 124)
        {
            msg(msglevel,
                "--ifconfig-ipv6-pool settings: network must be between /64 and /124 (not /%d)",
                netbits);
            goto err;
        }

        options->ifconfig_ipv6_pool_defined = true;
        options->ifconfig_ipv6_pool_base = network;
        options->ifconfig_ipv6_pool_netbits = netbits;
    }
    else if (streq(p[0], "hash-size") && p[1] && p[2] && !p[3])
    {
        int real, virtual;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        real = atoi(p[1]);
        virtual = atoi(p[2]);
        if (real < 1 || virtual < 1)
        {
            msg(msglevel, "--hash-size sizes must be >= 1 (preferably a power of 2)");
            goto err;
        }
        options->real_hash_size = real;
        options->virtual_hash_size = real;
    }
    else if (streq(p[0], "connect-freq") && p[1] && p[2] && !p[3])
    {
        int cf_max, cf_per;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        cf_max = atoi(p[1]);
        cf_per = atoi(p[2]);
        if (cf_max < 0 || cf_per < 0)
        {
            msg(msglevel, "--connect-freq parms must be > 0");
            goto err;
        }
        options->cf_max = cf_max;
        options->cf_per = cf_per;
    }
    else if (streq(p[0], "max-clients") && p[1] && !p[2])
    {
        int max_clients;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        max_clients = atoi(p[1]);
        if (max_clients < 0)
        {
            msg(msglevel, "--max-clients must be at least 1");
            goto err;
        }
        if (max_clients >= MAX_PEER_ID) /* max peer-id value */
        {
            msg(msglevel, "--max-clients must be less than %d", MAX_PEER_ID);
            goto err;
        }
        options->max_clients = max_clients;
    }
    else if (streq(p[0], "max-routes-per-client") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_INHERIT);
        options->max_routes_per_client = max_int(atoi(p[1]), 1);
    }
    else if (streq(p[0], "client-cert-not-required") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        msg(M_FATAL, "REMOVED OPTION: --client-cert-not-required, use '--verify-client-cert none' instead");
    }
    else if (streq(p[0], "verify-client-cert") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);

        /* Reset any existing flags */
        options->ssl_flags &= ~SSLF_CLIENT_CERT_OPTIONAL;
        options->ssl_flags &= ~SSLF_CLIENT_CERT_NOT_REQUIRED;
        if (p[1])
        {
            if (streq(p[1], "none"))
            {
                options->ssl_flags |= SSLF_CLIENT_CERT_NOT_REQUIRED;
            }
            else if (streq(p[1], "optional"))
            {
                options->ssl_flags |= SSLF_CLIENT_CERT_OPTIONAL;
            }
            else if (!streq(p[1], "require"))
            {
                msg(msglevel, "parameter to --verify-client-cert must be 'none', 'optional' or 'require'");
                goto err;
            }
        }
    }
    else if (streq(p[0], "username-as-common-name") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->ssl_flags |= SSLF_USERNAME_AS_COMMON_NAME;
    }
    else if (streq(p[0], "auth-user-pass-optional") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->ssl_flags |= SSLF_AUTH_USER_PASS_OPTIONAL;
    }
    else if (streq(p[0], "opt-verify") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->ssl_flags |= SSLF_OPT_VERIFY;
    }
    else if (streq(p[0], "auth-user-pass-verify") && p[1])
    {
        VERIFY_PERMISSION(OPT_P_SCRIPT);
        if (!no_more_than_n_args(msglevel, p, 3, NM_QUOTE_HINT))
        {
            goto err;
        }
        if (p[2])
        {
            if (streq(p[2], "via-env"))
            {
                options->auth_user_pass_verify_script_via_file = false;
            }
            else if (streq(p[2], "via-file"))
            {
                options->auth_user_pass_verify_script_via_file = true;
            }
            else
            {
                msg(msglevel, "second parm to --auth-user-pass-verify must be 'via-env' or 'via-file'");
                goto err;
            }
        }
        else
        {
            msg(msglevel, "--auth-user-pass-verify requires a second parameter ('via-env' or 'via-file')");
            goto err;
        }
        set_user_script(options,
                        &options->auth_user_pass_verify_script,
                        p[1], "auth-user-pass-verify", true);
    }
    else if (streq(p[0], "auth-gen-token") && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->auth_token_generate = true;
        options->auth_token_lifetime = p[1] ? positive_atoi(p[1]) : 0;
        if (p[2])
        {
            if (streq(p[2], "external-auth"))
            {
                options->auth_token_call_auth = true;
            }
            else
            {
                msg(msglevel, "Invalid argument to auth-gen-token: %s", p[2]);
            }
        }

    }
    else if (streq(p[0], "auth-gen-token-secret") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INLINE);
        options->auth_token_secret_file = p[1];
        options->auth_token_secret_file_inline = is_inline;

    }
    else if (streq(p[0], "client-connect") && p[1])
    {
        VERIFY_PERMISSION(OPT_P_SCRIPT);
        if (!no_more_than_n_args(msglevel, p, 2, NM_QUOTE_HINT))
        {
            goto err;
        }
        set_user_script(options, &options->client_connect_script,
                        p[1], "client-connect", true);
    }
    else if (streq(p[0], "client-disconnect") && p[1])
    {
        VERIFY_PERMISSION(OPT_P_SCRIPT);
        if (!no_more_than_n_args(msglevel, p, 2, NM_QUOTE_HINT))
        {
            goto err;
        }
        set_user_script(options, &options->client_disconnect_script,
                        p[1], "client-disconnect", true);
    }
    else if (streq(p[0], "learn-address") && p[1])
    {
        VERIFY_PERMISSION(OPT_P_SCRIPT);
        if (!no_more_than_n_args(msglevel, p, 2, NM_QUOTE_HINT))
        {
            goto err;
        }
        set_user_script(options, &options->learn_address_script,
                        p[1], "learn-address", true);
    }
    else if (streq(p[0], "tmp-dir") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->tmp_dir = p[1];
    }
    else if (streq(p[0], "client-config-dir") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->client_config_dir = p[1];
    }
    else if (streq(p[0], "ccd-exclusive") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->ccd_exclusive = true;
    }
    else if (streq(p[0], "bcast-buffers") && p[1] && !p[2])
    {
        int n_bcast_buf;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        n_bcast_buf = atoi(p[1]);
        if (n_bcast_buf < 1)
        {
            msg(msglevel, "--bcast-buffers parameter must be > 0");
        }
        options->n_bcast_buf = n_bcast_buf;
    }
    else if (streq(p[0], "tcp-queue-limit") && p[1] && !p[2])
    {
        int tcp_queue_limit;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        tcp_queue_limit = atoi(p[1]);
        if (tcp_queue_limit < 1)
        {
            msg(msglevel, "--tcp-queue-limit parameter must be > 0");
        }
        options->tcp_queue_limit = tcp_queue_limit;
    }
    #if PORT_SHARE
    else if (streq(p[0], "port-share") && p[1] && p[2] && !p[4])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->port_share_host = p[1];
        options->port_share_port = p[2];
        options->port_share_journal_dir = p[3];
    }
    #endif
    else if (streq(p[0], "client-to-client") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->enable_c2c = true;
    }
    else if (streq(p[0], "duplicate-cn") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->duplicate_cn = true;
    }
    else if (streq(p[0], "iroute") && p[1] && !p[3])
    {
        const char *netmask = NULL;

        VERIFY_PERMISSION(OPT_P_INSTANCE);
        if (p[2])
        {
            netmask = p[2];
        }
        option_iroute(options, p[1], netmask, msglevel);
    }
    else if (streq(p[0], "iroute-ipv6") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_INSTANCE);
        option_iroute_ipv6(options, p[1], msglevel);
    }
    else if (streq(p[0], "ifconfig-push") && p[1] && p[2] && !p[4])
    {
        in_addr_t local, remote_netmask;

        VERIFY_PERMISSION(OPT_P_INSTANCE);
        local = getaddr(GETADDR_HOST_ORDER|GETADDR_RESOLVE, p[1], 0, NULL, NULL);
        remote_netmask = getaddr(GETADDR_HOST_ORDER|GETADDR_RESOLVE, p[2], 0, NULL, NULL);
        if (local && remote_netmask)
        {
            options->push_ifconfig_defined = true;
            options->push_ifconfig_local = local;
            options->push_ifconfig_remote_netmask = remote_netmask;
            if (p[3])
            {
                options->push_ifconfig_local_alias = getaddr(GETADDR_HOST_ORDER|GETADDR_RESOLVE, p[3], 0, NULL, NULL);
            }
        }
        else
        {
            msg(msglevel, "cannot parse --ifconfig-push addresses");
            goto err;
        }
    }
    else if (streq(p[0], "ifconfig-push-constraint") && p[1] && p[2] && !p[3])
    {
        in_addr_t network, netmask;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        network = getaddr(GETADDR_HOST_ORDER|GETADDR_RESOLVE, p[1], 0, NULL, NULL);
        netmask = getaddr(GETADDR_HOST_ORDER, p[2], 0, NULL, NULL);
        if (network && netmask)
        {
            options->push_ifconfig_constraint_defined = true;
            options->push_ifconfig_constraint_network = network;
            options->push_ifconfig_constraint_netmask = netmask;
        }
        else
        {
            msg(msglevel, "cannot parse --ifconfig-push-constraint addresses");
            goto err;
        }
    }
    else if (streq(p[0], "ifconfig-ipv6-push") && p[1] && !p[3])
    {
        struct in6_addr local, remote;
        unsigned int netbits;

        VERIFY_PERMISSION(OPT_P_INSTANCE);

        if (!get_ipv6_addr( p[1], &local, &netbits, msglevel ) )
        {
            msg(msglevel, "cannot parse --ifconfig-ipv6-push addresses");
            goto err;
        }

        if (p[2])
        {
            if (!get_ipv6_addr( p[2], &remote, NULL, msglevel ) )
            {
                msg( msglevel, "cannot parse --ifconfig-ipv6-push addresses");
                goto err;
            }
        }
        else
        {
            if (!options->ifconfig_ipv6_local
                || !get_ipv6_addr( options->ifconfig_ipv6_local, &remote,
                                   NULL, msglevel ) )
            {
                msg( msglevel, "second argument to --ifconfig-ipv6-push missing and no global --ifconfig-ipv6 address set");
                goto err;
            }
        }

        options->push_ifconfig_ipv6_defined = true;
        options->push_ifconfig_ipv6_local = local;
        options->push_ifconfig_ipv6_netbits = netbits;
        options->push_ifconfig_ipv6_remote = remote;
        options->push_ifconfig_ipv6_blocked = false;
    }
    else if (streq(p[0], "disable") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_INSTANCE);
        options->disable = true;
    }
    else if (streq(p[0], "tcp-nodelay") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->server_flags |= SF_TCP_NODELAY_HELPER;
    }
    else if (streq(p[0], "stale-routes-check") && p[1] && !p[3])
    {
        int ageing_time, check_interval;

        VERIFY_PERMISSION(OPT_P_GENERAL);
        ageing_time = atoi(p[1]);
        if (p[2])
        {
            check_interval = atoi(p[2]);
        }
        else
        {
            check_interval = ageing_time;
        }

        if (ageing_time < 1 || check_interval < 1)
        {
            msg(msglevel, "--stale-routes-check aging time and check interval must be >= 1");
            goto err;
        }
        options->stale_routes_ageing_time  = ageing_time;
        options->stale_routes_check_interval = check_interval;
    }

    else if (streq(p[0], "client") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->client = true;
    }
    else if (streq(p[0], "pull") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->pull = true;
    }
    else if (streq(p[0], "push-continuation") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_PULL_MODE);
        options->push_continuation = atoi(p[1]);
    }
    else if (streq(p[0], "auth-user-pass") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (p[1])
        {
            options->auth_user_pass_file = p[1];
        }
        else
        {
            options->auth_user_pass_file = "stdin";
        }
    }
    else if (streq(p[0], "auth-retry") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        auth_retry_set(msglevel, p[1]);
    }
    #ifdef ENABLE_MANAGEMENT
    else if (streq(p[0], "static-challenge") && p[1] && p[2] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->sc_info.challenge_text = p[1];
        if (atoi(p[2]))
        {
            options->sc_info.flags |= SC_ECHO;
        }
    }
    #endif
    #endif /* if P2MP */
    else if (streq(p[0], "msg-channel") && p[1])
    {
        #ifdef _WIN32
        VERIFY_PERMISSION(OPT_P_GENERAL);
        HANDLE process = GetCurrentProcess();
        HANDLE handle = (HANDLE) atoll(p[1]);
        if (!DuplicateHandle(process, handle, process, &options->msg_channel, 0,
                             FALSE, DUPLICATE_CLOSE_SOURCE | DUPLICATE_SAME_ACCESS))
        {
            msg(msglevel, "could not duplicate service pipe handle");
            goto err;
        }
        options->route_method = ROUTE_METHOD_SERVICE;
        #else  /* ifdef _WIN32 */
        msg(msglevel, "--msg-channel is only supported on Windows");
        goto err;
        #endif
    }
    #ifdef _WIN32
    else if (streq(p[0], "win-sys") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (streq(p[1], "env"))
        {
            msg(M_INFO, "NOTE: --win-sys env is default from tzvpn 1.0.	 "
                "This entry will now be ignored.  "
                "Please remove this entry from your configuration file.");
        }
        else
        {
            set_win_sys_path(p[1], es);
        }
    }
    else if (streq(p[0], "route-method") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_ROUTE_EXTRAS);
        if (streq(p[1], "adaptive"))
        {
            options->route_method = ROUTE_METHOD_ADAPTIVE;
        }
        else if (streq(p[1], "ipapi"))
        {
            options->route_method = ROUTE_METHOD_IPAPI;
        }
        else if (streq(p[1], "exe"))
        {
            options->route_method = ROUTE_METHOD_EXE;
        }
        else
        {
            msg(msglevel, "--route method must be 'adaptive', 'ipapi', or 'exe'");
            goto err;
        }
    }
    else if (streq(p[0], "ip-win32") && p[1] && !p[4])
    {
        const int index = ascii2ipset(p[1]);
        struct tuntap_options *to = &options->tuntap_options;

        VERIFY_PERMISSION(OPT_P_IPWIN32);

        if (index < 0)
        {
            msg(msglevel,
                "Bad --ip-win32 method: '%s'.  Allowed methods: %s",
                p[1],
                ipset2ascii_all(&gc));
            goto err;
        }

        if (index == IPW32_SET_ADAPTIVE)
        {
            options->route_delay_window = IPW32_SET_ADAPTIVE_DELAY_WINDOW;
        }

        if (index == IPW32_SET_DHCP_MASQ)
        {
            if (p[2])
            {
                if (!streq(p[2], "default"))
                {
                    int offset = atoi(p[2]);

                    if (!(offset > -256 && offset < 256))
                    {
                        msg(msglevel, "--ip-win32 dynamic [offset] [lease-time]: offset (%d) must be > -256 and < 256", offset);
                        goto err;
                    }

                    to->dhcp_masq_custom_offset = true;
                    to->dhcp_masq_offset = offset;
                }

                if (p[3])
                {
                    const int min_lease = 30;
                    int lease_time;
                    lease_time = atoi(p[3]);
                    if (lease_time < min_lease)
                    {
                        msg(msglevel, "--ip-win32 dynamic [offset] [lease-time]: lease time parameter (%d) must be at least %d seconds", lease_time, min_lease);
                        goto err;
                    }
                    to->dhcp_lease_time = lease_time;
                }
            }
        }
        to->ip_win32_type = index;
        to->ip_win32_defined = true;
    }
    #endif /* ifdef _WIN32 */
    #if defined(_WIN32) || defined(TARGET_ANDROID)
    else if (streq(p[0], "dhcp-option") && p[1] && !p[3])
    {
        struct tuntap_options *o = &options->tuntap_options;
        VERIFY_PERMISSION(OPT_P_IPWIN32);
        bool ipv6dns = false;

        if ((streq(p[1], "DOMAIN") || streq(p[1], "ADAPTER_DOMAIN_SUFFIX"))
            && p[2])
        {
            o->domain = p[2];
        }
        else if (streq(p[1], "NBS") && p[2])
        {
            o->netbios_scope = p[2];
        }
        else if (streq(p[1], "NBT") && p[2])
        {
            int t;
            t = atoi(p[2]);
            if (!(t == 1 || t == 2 || t == 4 || t == 8))
            {
                msg(msglevel, "--dhcp-option NBT: parameter (%d) must be 1, 2, 4, or 8", t);
                goto err;
            }
            o->netbios_node_type = t;
        }
        else if ((streq(p[1], "DNS") || streq(p[1], "DNS6")) && p[2] && (!strstr(p[2], ":") || ipv6_addr_safe(p[2])))
        {
            if (strstr(p[2], ":"))
            {
                ipv6dns = true;
                foreign_option(options, p, 3, es);
                dhcp_option_dns6_parse(p[2], o->dns6, &o->dns6_len, msglevel);
            }
            else
            {
                dhcp_option_address_parse("DNS", p[2], o->dns, &o->dns_len, msglevel);
            }
        }
        else if (streq(p[1], "WINS") && p[2])
        {
            dhcp_option_address_parse("WINS", p[2], o->wins, &o->wins_len, msglevel);
        }
        else if (streq(p[1], "NTP") && p[2])
        {
            dhcp_option_address_parse("NTP", p[2], o->ntp, &o->ntp_len, msglevel);
        }
        else if (streq(p[1], "NBDD") && p[2])
        {
            dhcp_option_address_parse("NBDD", p[2], o->nbdd, &o->nbdd_len, msglevel);
        }
        else if (streq(p[1], "DOMAIN-SEARCH") && p[2])
        {
            if (o->domain_search_list_len < N_SEARCH_LIST_LEN)
            {
                o->domain_search_list[o->domain_search_list_len++] = p[2];
            }
            else
            {
                msg(msglevel, "--dhcp-option %s: maximum of %d search entries can be specified",
                    p[1], N_SEARCH_LIST_LEN);
            }
        }
        else if (streq(p[1], "DISABLE-NBT") && !p[2])
        {
            o->disable_nbt = 1;
        }
        else
        {
            msg(msglevel, "--dhcp-option: unknown option type '%s' or missing or unknown parameter", p[1]);
            goto err;
        }

        /* flag that we have options to give to the TAP driver's DHCPv4 server
         *  - skipped for "DNS6", as that's not a DHCPv4 option
         */
        if (!ipv6dns)
        {
            o->dhcp_options = true;
        }
    }
    #endif /* if defined(_WIN32) || defined(TARGET_ANDROID) */
    #ifdef _WIN32
    else if (streq(p[0], "show-adapters") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        show_tap_win_adapters(M_INFO|M_NOPREFIX, M_WARN|M_NOPREFIX);
        openvpn_exit(OPENVPN_EXIT_STATUS_GOOD); /* exit point */
    }
    else if (streq(p[0], "show-net") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        show_routes(M_INFO|M_NOPREFIX);
        show_adapters(M_INFO|M_NOPREFIX);
        openvpn_exit(OPENVPN_EXIT_STATUS_GOOD); /* exit point */
    }
    else if (streq(p[0], "show-net-up") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_UP);
        options->show_net_up = true;
    }
    else if (streq(p[0], "tap-sleep") && p[1] && !p[2])
    {
        int s;
        VERIFY_PERMISSION(OPT_P_IPWIN32);
        s = atoi(p[1]);
        if (s < 0 || s >= 256)
        {
            msg(msglevel, "--tap-sleep parameter must be between 0 and 255");
            goto err;
        }
        options->tuntap_options.tap_sleep = s;
    }
    else if (streq(p[0], "dhcp-renew") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_IPWIN32);
        options->tuntap_options.dhcp_renew = true;
    }
    else if (streq(p[0], "dhcp-pre-release") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_IPWIN32);
        options->tuntap_options.dhcp_pre_release = true;
        options->tuntap_options.dhcp_renew = true;
    }
    else if (streq(p[0], "dhcp-release") && !p[1])
    {
        msg(M_WARN, "Obsolete option --dhcp-release detected. This is now on by default");
    }
    else if (streq(p[0], "dhcp-internal") && p[1] && !p[2]) /* standalone method for internal use */
    {
        unsigned int adapter_index;
        VERIFY_PERMISSION(OPT_P_GENERAL);
        set_debug_level(options->verbosity, SDL_CONSTRAIN);
        adapter_index = atou(p[1]);
        sleep(options->tuntap_options.tap_sleep);
        if (options->tuntap_options.dhcp_pre_release)
        {
            dhcp_release_by_adapter_index(adapter_index);
        }
        if (options->tuntap_options.dhcp_renew)
        {
            dhcp_renew_by_adapter_index(adapter_index);
        }
        openvpn_exit(OPENVPN_EXIT_STATUS_GOOD); /* exit point */
    }
    else if (streq(p[0], "register-dns") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_IPWIN32);
        options->tuntap_options.register_dns = true;
    }
    else if (streq(p[0], "block-outside-dns") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_IPWIN32);
        options->block_outside_dns = true;
    }
    else if (streq(p[0], "rdns-internal") && !p[1])
    /* standalone method for internal use
     *
     * (if --register-dns is set, openvpn needs to call itself in a
     *  sub-process to execute the required functions in a non-blocking
     *  way, and uses --rdns-internal to signal that to itself)
     */
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        set_debug_level(options->verbosity, SDL_CONSTRAIN);
        if (options->tuntap_options.register_dns)
        {
            ipconfig_register_dns(NULL);
        }
        openvpn_exit(OPENVPN_EXIT_STATUS_GOOD); /* exit point */
    }
    else if (streq(p[0], "show-valid-subnets") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        show_valid_win32_tun_subnets();
        openvpn_exit(OPENVPN_EXIT_STATUS_GOOD); /* exit point */
    }
    else if (streq(p[0], "pause-exit") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        set_pause_exit_win32();
    }
    else if (streq(p[0], "service") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->exit_event_name = p[1];
        if (p[2])
        {
            options->exit_event_initial_state = (atoi(p[2]) != 0);
        }
    }
    else if (streq(p[0], "allow-nonadmin") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        tap_allow_nonadmin_access(p[1]);
        openvpn_exit(OPENVPN_EXIT_STATUS_GOOD); /* exit point */
    }
    else if (streq(p[0], "user") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        msg(M_WARN, "NOTE: --user option is not implemented on Windows");
    }
    else if (streq(p[0], "group") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        msg(M_WARN, "NOTE: --group option is not implemented on Windows");
    }
    #else  /* ifdef _WIN32 */
    else if (streq(p[0], "user") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->username = p[1];
    }
    else if (streq(p[0], "group") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->groupname = p[1];
    }
    else if (streq(p[0], "dhcp-option") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_IPWIN32);
        foreign_option(options, p, 3, es);
    }
    else if (streq(p[0], "route-method") && p[1] && !p[2]) /* ignore when pushed to non-Windows OS */
    {
        VERIFY_PERMISSION(OPT_P_ROUTE_EXTRAS);
    }
    #endif /* ifdef _WIN32 */
    #if PASSTOS_CAPABILITY
    else if (streq(p[0], "passtos") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->passtos = true;
    }
    #endif
    #if defined(USE_COMP)
    else if (streq(p[0], "allow-compression") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);

        if (streq(p[1], "no"))
        {
            options->comp.flags =
                COMP_F_ALLOW_STUB_ONLY|COMP_F_ADVERTISE_STUBS_ONLY;
            if (comp_non_stub_enabled(&options->comp))
            {
                msg(msglevel, "'--allow-compression no' conflicts with "
                    " enabling compression");
            }
        }
        else if (options->comp.flags & COMP_F_ALLOW_STUB_ONLY)
        {
            /* Also printed on a push to hint at configuration problems */
            msg(msglevel, "Cannot set allow-compression to '%s' "
                "after set to 'no'", p[1]);
            goto err;
        }
        else if (streq(p[1], "asym"))
        {
            options->comp.flags &= ~COMP_F_ALLOW_COMPRESS;
        }
        else if (streq(p[1], "yes"))
        {
            msg(M_WARN, "WARNING: Compression for sending and receiving enabled. Compression has "
                "been used in the past to break encryption. Allowing compression allows "
                "attacks that break encryption. Using \"--allow-compression yes\" is "
                "strongly discouraged for common usage. See --compress in the manual "
                "page for more information ");

            options->comp.flags |= COMP_F_ALLOW_COMPRESS;
        }
        else
        {
            msg(msglevel, "bad allow-compression option: %s -- "
                "must be 'yes', 'no', or 'asym'", p[1]);
            goto err;
        }
    }
    else if (streq(p[0], "comp-lzo") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_COMP);

        /* All lzo variants do not use swap */
        options->comp.flags &= ~COMP_F_SWAP;
        #if defined(ENABLE_LZO)
        if (p[1] && streq(p[1], "no"))
        #endif
        {
            options->comp.alg = COMP_ALG_STUB;
            options->comp.flags &= ~COMP_F_ADAPTIVE;
        }
        #if defined(ENABLE_LZO)
        else if (options->comp.flags & COMP_F_ALLOW_STUB_ONLY)
        {
            /* Also printed on a push to hint at configuration problems */
            msg(msglevel, "Cannot set comp-lzo to '%s', "
                "allow-compression is set to 'no'", p[1]);
            goto err;
        }
        else if (p[1])
        {
            if (streq(p[1], "yes"))
            {
                options->comp.alg = COMP_ALG_LZO;
                options->comp.flags &= ~COMP_F_ADAPTIVE;
            }
            else if (streq(p[1], "adaptive"))
            {
                options->comp.alg = COMP_ALG_LZO;
                options->comp.flags |= COMP_F_ADAPTIVE;
            }
            else
            {
                msg(msglevel, "bad comp-lzo option: %s -- must be 'yes', 'no', or 'adaptive'", p[1]);
                goto err;
            }
        }
        else
        {
            options->comp.alg = COMP_ALG_LZO;
            options->comp.flags |= COMP_F_ADAPTIVE;
        }
        show_compression_warning(&options->comp);
        #endif /* if defined(ENABLE_LZO) */
    }
    else if (streq(p[0], "comp-noadapt") && !p[1])
    {
        /*
         * We do not need to check here if we allow compression since
         * it only modifies a flag if compression is enabled
         */
        VERIFY_PERMISSION(OPT_P_COMP);
        options->comp.flags &= ~COMP_F_ADAPTIVE;
    }
    else if (streq(p[0], "compress") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_COMP);
        if (p[1])
        {
            if (streq(p[1], "stub"))
            {
                options->comp.alg = COMP_ALG_STUB;
                options->comp.flags |= (COMP_F_SWAP|COMP_F_ADVERTISE_STUBS_ONLY);
            }
            else if (streq(p[1], "stub-v2"))
            {
                options->comp.alg = COMP_ALGV2_UNCOMPRESSED;
                options->comp.flags |= COMP_F_ADVERTISE_STUBS_ONLY;
            }
            else if (options->comp.flags & COMP_F_ALLOW_STUB_ONLY)
            {
                /* Also printed on a push to hint at configuration problems */
                msg(msglevel, "Cannot set compress to '%s', "
                    "allow-compression is set to 'no'", p[1]);
                goto err;
            }
            #if defined(ENABLE_LZO)
            else if (streq(p[1], "lzo"))
            {
                options->comp.alg = COMP_ALG_LZO;
                options->comp.flags &= ~(COMP_F_ADAPTIVE | COMP_F_SWAP);
            }
            #endif
            #if defined(ENABLE_LZ4)
            else if (streq(p[1], "lz4"))
            {
                options->comp.alg = COMP_ALG_LZ4;
                options->comp.flags |= COMP_F_SWAP;
            }
            else if (streq(p[1], "lz4-v2"))
            {
                options->comp.alg = COMP_ALGV2_LZ4;
            }
            #endif
            else
            {
                msg(msglevel, "bad comp option: %s", p[1]);
                goto err;
            }
        }
        else
        {
            options->comp.alg = COMP_ALG_STUB;
            options->comp.flags |= COMP_F_SWAP;
        }
        show_compression_warning(&options->comp);
    }
    #endif /* USE_COMP */
    else if (streq(p[0], "show-ciphers") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->show_ciphers = true;
    }
    else if (streq(p[0], "show-digests") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->show_digests = true;
    }
    else if (streq(p[0], "show-engines") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->show_engines = true;
    }
    else if (streq(p[0], "key-direction") && p[1] && !p[2])
    {
        int key_direction;

        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION);

        key_direction = ascii2keydirection(msglevel, p[1]);
        if (key_direction >= 0)
        {
            if (permission_mask & OPT_P_GENERAL)
            {
                options->key_direction = key_direction;
            }
            else if (permission_mask & OPT_P_CONNECTION)
            {
                options->ce.key_direction = key_direction;
            }
        }
        else
        {
            goto err;
        }
    }
    else if (streq(p[0], "secret") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INLINE);
        options->shared_secret_file = p[1];
        options->shared_secret_file_inline = is_inline;
        if (!is_inline && p[2])
        {
            int key_direction;

            key_direction = ascii2keydirection(msglevel, p[2]);
            if (key_direction >= 0)
            {
                options->key_direction = key_direction;
            }
            else
            {
                goto err;
            }
        }
    }
    else if (streq(p[0], "genkey") && !p[4])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->genkey = true;
        if (!p[1])
        {
            options->genkey_type = GENKEY_SECRET;
        }
        else
        {
            if (streq(p[1], "secret") || streq(p[1], "tls-auth")
                || streq(p[1], "tls-crypt"))
            {
                options->genkey_type = GENKEY_SECRET;
            }
            else if (streq(p[1], "tls-crypt-v2-server"))
            {
                options->genkey_type = GENKEY_TLS_CRYPTV2_SERVER;
            }
            else if (streq(p[1], "tls-crypt-v2-client"))
            {
                options->genkey_type = GENKEY_TLS_CRYPTV2_CLIENT;
                if (p[3])
                {
                    options->genkey_extra_data = p[3];
                }
            }
            else if (streq(p[1], "auth-token"))
            {
                options->genkey_type = GENKEY_AUTH_TOKEN;
            }
            else
            {
                msg(msglevel, "unknown --genkey type: %s", p[1]);
            }

        }
        if (p[2])
        {
            options->genkey_filename = p[2];
        }
    }
    else if (streq(p[0], "auth") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->authname = p[1];
    }
    else if (streq(p[0], "cipher") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_NCP|OPT_P_INSTANCE);
        options->ciphername = p[1];
    }
    else if (streq(p[0], "data-ciphers-fallback") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INSTANCE);
        options->ciphername = p[1];
        options->enable_ncp_fallback = true;
    }
    else if ((streq(p[0], "data-ciphers") || streq(p[0], "ncp-ciphers"))
             && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INSTANCE);
        if (streq(p[0], "ncp-ciphers"))
        {
            msg(M_INFO, "Note: Treating option '--ncp-ciphers' as "
                " '--data-ciphers' (renamed in tzvpn 1.0).");
        }
        options->ncp_ciphers = p[1];
    }
    else if (streq(p[0], "ncp-disable") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INSTANCE);
        options->ncp_enabled = false;
        msg(M_WARN, "DEPRECATED OPTION: ncp-disable. Disabling "
            "cipher negotiation is a deprecated debug feature that "
            "will be removed in tzvpn 1.0");
    }
    else if (streq(p[0], "prng") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (streq(p[1], "none"))
        {
            options->prng_hash = NULL;
        }
        else
        {
            options->prng_hash = p[1];
        }
        if (p[2])
        {
            const int sl = atoi(p[2]);
            if (sl >= NONCE_SECRET_LEN_MIN && sl <= NONCE_SECRET_LEN_MAX)
            {
                options->prng_nonce_secret_len = sl;
            }
            else
            {
                msg(msglevel, "prng parameter nonce_secret_len must be between %d and %d",
                    NONCE_SECRET_LEN_MIN, NONCE_SECRET_LEN_MAX);
                goto err;
            }
        }
    }
    else if (streq(p[0], "no-replay") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->replay = false;
    }
    else if (streq(p[0], "replay-window") && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (p[1])
        {
            int replay_window;

            replay_window = atoi(p[1]);
            if (!(MIN_SEQ_BACKTRACK <= replay_window && replay_window <= MAX_SEQ_BACKTRACK))
            {
                msg(msglevel, "replay-window window size parameter (%d) must be between %d and %d",
                    replay_window,
                    MIN_SEQ_BACKTRACK,
                    MAX_SEQ_BACKTRACK);
                goto err;
            }
            options->replay_window = replay_window;

            if (p[2])
            {
                int replay_time;

                replay_time = atoi(p[2]);
                if (!(MIN_TIME_BACKTRACK <= replay_time && replay_time <= MAX_TIME_BACKTRACK))
                {
                    msg(msglevel, "replay-window time window parameter (%d) must be between %d and %d",
                        replay_time,
                        MIN_TIME_BACKTRACK,
                        MAX_TIME_BACKTRACK);
                    goto err;
                }
                options->replay_time = replay_time;
            }
        }
        else
        {
            msg(msglevel, "replay-window option is missing window size parameter");
            goto err;
        }
    }
    else if (streq(p[0], "mute-replay-warnings") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->mute_replay_warnings = true;
    }
    else if (streq(p[0], "replay-persist") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->packet_id_file = p[1];
    }
    else if (streq(p[0], "test-crypto") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->test_crypto = true;
    }
    #ifndef ENABLE_CRYPTO_MBEDTLS
    else if (streq(p[0], "engine") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (p[1])
        {
            options->engine = p[1];
        }
        else
        {
            options->engine = "auto";
        }
    }
    #endif /* ENABLE_CRYPTO_MBEDTLS */
    #ifdef HAVE_EVP_CIPHER_CTX_SET_KEY_LENGTH
    else if (streq(p[0], "keysize") && p[1] && !p[2])
    {
        int keysize;

        VERIFY_PERMISSION(OPT_P_NCP);
        keysize = atoi(p[1]) / 8;
        if (keysize < 0 || keysize > MAX_CIPHER_KEY_LENGTH)
        {
            msg(msglevel, "Bad keysize: %s", p[1]);
            goto err;
        }
        options->keysize = keysize;
    }
    #endif
    #ifdef ENABLE_PREDICTION_RESISTANCE
    else if (streq(p[0], "use-prediction-resistance") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->use_prediction_resistance = true;
    }
    #endif
    else if (streq(p[0], "show-tls") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->show_tls_ciphers = true;
    }
    else if ((streq(p[0], "show-curves") || streq(p[0], "show-groups")) && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->show_curves = true;
    }
    else if (streq(p[0], "ecdh-curve") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        msg(M_WARN, "Consider setting groups/curves preference with "
            "tls-groups instead of forcing a specific curve with "
            "ecdh-curve.");
        options->ecdh_curve = p[1];
    }
    else if (streq(p[0], "tls-server") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->tls_server = true;
    }
    else if (streq(p[0], "tls-client") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->tls_client = true;
    }
    else if (streq(p[0], "ca") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INLINE);
        options->ca_file = p[1];
        options->ca_file_inline = is_inline;
    }
    #ifndef ENABLE_CRYPTO_MBEDTLS
    else if (streq(p[0], "capath") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->ca_path = p[1];
    }
    #endif /* ENABLE_CRYPTO_MBEDTLS */
    else if (streq(p[0], "dh") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INLINE);
        options->dh_file = p[1];
        options->dh_file_inline = is_inline;
    }
    else if (streq(p[0], "cert") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INLINE);
        options->cert_file = p[1];
        options->cert_file_inline = is_inline;
    }
    //add by zhouping 20220414
    else if (streq(p[0], "enc-cert") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL | OPT_P_INLINE);
        options->enc_cert_file = p[1];
        options->enc_cert_file_inline = is_inline;
    }
    // add by zhouping 20220826
    else if (streq(p[0], "cert-bak") && p[1] && !p[2])
    {
	    VERIFY_PERMISSION(OPT_P_GENERAL | OPT_P_INLINE);
	    options->cert_bak = p[1];
	    options->cert_bak_inline = is_inline; 
    }
	// add by zhouping 20220826
	else if (streq(p[0], "enc-cert-bak") && p[1] && !p[2])
	{
	    VERIFY_PERMISSION(OPT_P_GENERAL | OPT_P_INLINE);
	    options->enc_cert_bak = p[1];
	   // options->enc_cert_bak_inline = is_inline;
	}
    
    else if (streq(p[0], "extra-certs") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INLINE);
        options->extra_certs_file = p[1];
        options->extra_certs_file_inline = is_inline;
    }
    else if (streq(p[0], "verify-hash") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);

        if (!p[2] || (p[2] && streq(p[2], "SHA1")))
        {
            options->verify_hash = parse_hash_fingerprint(p[1], SHA_DIGEST_LENGTH, msglevel, &options->gc);
            options->verify_hash_algo = MD_SHA1;
        }
        else if (p[2] && streq(p[2], "SHA256"))
        {
            options->verify_hash = parse_hash_fingerprint(p[1], SHA256_DIGEST_LENGTH, msglevel, &options->gc);
            options->verify_hash_algo = MD_SHA256;
        }
        else
        {
            msg(msglevel, "invalid or unsupported hashing algorithm: %s  (only SHA1 and SHA256 are valid)", p[2]);
            goto err;
        }
    }
    #ifdef ENABLE_CRYPTOAPI
    else if (streq(p[0], "cryptoapicert") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->cryptoapi_cert = p[1];
    }
    #endif
    else if (streq(p[0], "key") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INLINE);
        options->priv_key_file = p[1];
        options->priv_key_file_inline = is_inline;
    }
    //add by zhouping 20220414
    else if (streq(p[0], "enc-key") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL | OPT_P_INLINE);
        options->priv_enc_key_file = p[1];
        options->priv_enc_key_file_inline = is_inline;
    }
	// add by zhouping 20220826
	else if (streq(p[0], "key-bak") && p[1] && !p[2])
	{
	    VERIFY_PERMISSION(OPT_P_GENERAL | OPT_P_INLINE);
	    options->priv_key_bak = p[1];
	    //options->cert_bak_inline = is_inline;
	}
	// add by zhouping 20220826
	else if (streq(p[0], "enc-key-bak") && p[1] && !p[2])
	{
	    VERIFY_PERMISSION(OPT_P_GENERAL | OPT_P_INLINE);
	    options->priv_enc_key_bak = p[1];
	    //options->cert_bak_inline = is_inline;
	}
    else if (streq(p[0], "tls-version-min") && p[1] && !p[3])
    {
        int ver;
        VERIFY_PERMISSION(OPT_P_GENERAL);
        ver = tls_version_parse(p[1], p[2]);
        if (ver == TLS_VER_BAD)
        {
            msg(msglevel, "unknown tls-version-min parameter: %s", p[1]);
            goto err;
        }
        options->ssl_flags &=
            ~(SSLF_TLS_VERSION_MIN_MASK << SSLF_TLS_VERSION_MIN_SHIFT);
        options->ssl_flags |= (ver << SSLF_TLS_VERSION_MIN_SHIFT);
    }
    else if (streq(p[0], "tls-version-max") && p[1] && !p[2])
    {
        int ver;
        VERIFY_PERMISSION(OPT_P_GENERAL);
        ver = tls_version_parse(p[1], NULL);
        if (ver == TLS_VER_BAD)
        {
            msg(msglevel, "unknown tls-version-max parameter: %s", p[1]);
            goto err;
        }
        options->ssl_flags &=
            ~(SSLF_TLS_VERSION_MAX_MASK << SSLF_TLS_VERSION_MAX_SHIFT);
        options->ssl_flags |= (ver << SSLF_TLS_VERSION_MAX_SHIFT);
    }
    #ifndef ENABLE_CRYPTO_MBEDTLS
    else if (streq(p[0], "pkcs12") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INLINE);
        options->pkcs12_file = p[1];
        options->pkcs12_file_inline = is_inline;
    }
    #endif /* ENABLE_CRYPTO_MBEDTLS */
    else if (streq(p[0], "askpass") && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (p[1])
        {
            options->key_pass_file = p[1];
        }
        else
        {
            options->key_pass_file = "stdin";
        }
    }
    else if (streq(p[0], "auth-nocache") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        ssl_set_auth_nocache();
    }
    else if (streq(p[0], "auth-token") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_ECHO);
        ssl_set_auth_token(p[1]);
        #ifdef ENABLE_MANAGEMENT
        if (management)
        {
            management_auth_token(management, p[1]);
        }
        #endif
    }
    else if (streq(p[0], "auth-token-user") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_ECHO);
        ssl_set_auth_token_user(p[1]);
    }
    else if (streq(p[0], "single-session") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->single_session = true;
    }
    else if (streq(p[0], "push-peer-info") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->push_peer_info = true;
    }
    else if (streq(p[0], "tls-exit") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->tls_exit = true;
    }
    else if (streq(p[0], "tls-cipher") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->cipher_list = p[1];
    }
    else if (streq(p[0], "tls-cert-profile") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->tls_cert_profile = p[1];
    }
    else if (streq(p[0], "tls-ciphersuites") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->cipher_list_tls13 = p[1];
    }
    else if (streq(p[0], "tls-groups") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->tls_groups = p[1];
    }
    else if (streq(p[0], "crl-verify") && p[1] && ((p[2] && streq(p[2], "dir"))
                                                   || !p[2]))
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INLINE);
        if (p[2] && streq(p[2], "dir"))
        {
            options->ssl_flags |= SSLF_CRL_VERIFY_DIR;
        }
        options->crl_file = p[1];
        options->crl_file_inline = is_inline;
    }
    else if (streq(p[0], "tls-verify") && p[1])
    {
        VERIFY_PERMISSION(OPT_P_SCRIPT);
        if (!no_more_than_n_args(msglevel, p, 2, NM_QUOTE_HINT))
        {
            goto err;
        }
        set_user_script(options, &options->tls_verify,
                        string_substitute(p[1], ',', ' ', &options->gc),
                        "tls-verify", true);
    }
    #ifndef ENABLE_CRYPTO_MBEDTLS
    else if (streq(p[0], "tls-export-cert") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->tls_export_cert = p[1];
    }
    #endif
    else if (streq(p[0], "compat-names"))
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        msg(msglevel, "--compat-names was removed in tzvpn 1.0. "
            "Update your configuration.");
        goto err;
    }
    else if (streq(p[0], "no-name-remapping") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        msg(msglevel, "--no-name-remapping was removed in tzvpn 1.0. "
            "Update your configuration.");
        goto err;
    }
    else if (streq(p[0], "verify-x509-name") && p[1] && strlen(p[1]) && !p[3])
    {
        int type = VERIFY_X509_SUBJECT_DN;
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (p[2])
        {
            if (streq(p[2], "subject"))
            {
                type = VERIFY_X509_SUBJECT_DN;
            }
            else if (streq(p[2], "name"))
            {
                type = VERIFY_X509_SUBJECT_RDN;
            }
            else if (streq(p[2], "name-prefix"))
            {
                type = VERIFY_X509_SUBJECT_RDN_PREFIX;
            }
            else
            {
                msg(msglevel, "unknown X.509 name type: %s", p[2]);
                goto err;
            }
        }
        options->verify_x509_type = type;
        options->verify_x509_name = p[1];
    }
    else if (streq(p[0], "ns-cert-type") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (streq(p[1], "server"))
        {
            options->ns_cert_type = NS_CERT_CHECK_SERVER;
        }
        else if (streq(p[1], "client"))
        {
            options->ns_cert_type = NS_CERT_CHECK_CLIENT;
        }
        else
        {
            msg(msglevel, "--ns-cert-type must be 'client' or 'server'");
            goto err;
        }
    }
    else if (streq(p[0], "remote-cert-ku"))
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);

        size_t j;
        for (j = 1; j < MAX_PARMS && p[j] != NULL; ++j)
        {
            sscanf(p[j], "%x", &(options->remote_cert_ku[j-1]));
        }
        if (j == 1)
        {
            /* No specific KU required, but require KU to be present */
            options->remote_cert_ku[0] = OPENVPN_KU_REQUIRED;
        }
    }
    else if (streq(p[0], "remote-cert-eku") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->remote_cert_eku = p[1];
    }
    else if (streq(p[0], "remote-cert-tls") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);

        if (streq(p[1], "server"))
        {
            options->remote_cert_ku[0] = OPENVPN_KU_REQUIRED;
            options->remote_cert_eku = "TLS Web Server Authentication";
        }
        else if (streq(p[1], "client"))
        {
            options->remote_cert_ku[0] = OPENVPN_KU_REQUIRED;
            options->remote_cert_eku = "TLS Web Client Authentication";
        }
        else
        {
            msg(msglevel, "--remote-cert-tls must be 'client' or 'server'");
            goto err;
        }
    }
    else if (streq(p[0], "tls-timeout") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_TLS_PARMS);
        options->tls_timeout = positive_atoi(p[1]);
    }
    else if (streq(p[0], "reneg-bytes") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_TLS_PARMS);
        options->renegotiate_bytes = positive_atoi(p[1]);
    }
    else if (streq(p[0], "reneg-pkts") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_TLS_PARMS);
        options->renegotiate_packets = positive_atoi(p[1]);
    }
    else if (streq(p[0], "reneg-sec") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_TLS_PARMS);
        options->renegotiate_seconds = positive_atoi(p[1]);
        if (p[2])
        {
            options->renegotiate_seconds_min = positive_atoi(p[2]);
        }
    }
    else if (streq(p[0], "hand-window") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_TLS_PARMS);
        options->handshake_window = positive_atoi(p[1]);
    }
    else if (streq(p[0], "tran-window") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_TLS_PARMS);
        options->transition_window = positive_atoi(p[1]);
    }
    else if (streq(p[0], "tls-auth") && p[1] && !p[3])
    {
        int key_direction = -1;

        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION|OPT_P_INLINE);

        if (permission_mask & OPT_P_GENERAL)
        {
            options->tls_auth_file = p[1];
            options->tls_auth_file_inline = is_inline;

            if (!is_inline && p[2])
            {
                key_direction = ascii2keydirection(msglevel, p[2]);
                if (key_direction < 0)
                {
                    goto err;
                }
                options->key_direction = key_direction;
            }

        }
        else if (permission_mask & OPT_P_CONNECTION)
        {
            options->ce.tls_auth_file = p[1];
            options->ce.tls_auth_file_inline = is_inline;
            options->ce.key_direction = KEY_DIRECTION_BIDIRECTIONAL;

            if (!is_inline && p[2])
            {
                key_direction = ascii2keydirection(msglevel, p[2]);
                if (key_direction < 0)
                {
                    goto err;
                }
                options->ce.key_direction = key_direction;
            }
        }
    }
    else if (streq(p[0], "tls-crypt") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION|OPT_P_INLINE);
        if (permission_mask & OPT_P_GENERAL)
        {
            options->tls_crypt_file = p[1];
            options->tls_crypt_file_inline = is_inline;
        }
        else if (permission_mask & OPT_P_CONNECTION)
        {
            options->ce.tls_crypt_file = p[1];
            options->ce.tls_crypt_file_inline = is_inline;
        }
    }
    else if (streq(p[0], "tls-crypt-v2") && p[1] && !p[3])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_CONNECTION|OPT_P_INLINE);
        if (permission_mask & OPT_P_GENERAL)
        {
            options->tls_crypt_v2_file = p[1];
            options->tls_crypt_v2_file_inline = is_inline;
        }
        else if (permission_mask & OPT_P_CONNECTION)
        {
            options->ce.tls_crypt_v2_file = p[1];
            options->ce.tls_crypt_v2_file_inline = is_inline;
        }
    }
    else if (streq(p[0], "tls-crypt-v2-verify") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->tls_crypt_v2_verify_script = p[1];
    }
    else if (streq(p[0], "x509-track") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        x509_track_add(&options->x509_track, p[1], msglevel, &options->gc);
    }
    #ifdef ENABLE_X509ALTUSERNAME
    else if (streq(p[0], "x509-username-field") && p[1] && !p[2])
    {
        /* This option used to automatically upcase the fieldname passed as the
         * option argument, e.g., "ou" became "OU". Now, this "helpfulness" is
         * fine-tuned by only upcasing Subject field attribute names which consist
         * of all lower-case characters. Mixed-case attributes such as
         * "emailAddress" are left as-is. An option parameter having the "ext:"
         * prefix for matching X.509v3 extended fields will also remain unchanged.
         */
        char *s = p[1];

        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (strncmp("ext:", s, 4) != 0)
        {
            size_t i = 0;
            while (s[i] && !isupper(s[i]))
            {
                i++;
            }
            if (strlen(s) == i)
            {
                while ((*s = toupper(*s)) != '\0')
                {
                    s++;
                }
                msg(M_WARN, "DEPRECATED FEATURE: automatically upcased the "
                    "--x509-username-field parameter to '%s'; please update your"
                    "configuration", p[1]);
            }
        }
        else if (!x509_username_field_ext_supported(s+4))
        {
            msg(msglevel, "Unsupported x509-username-field extension: %s", s);
        }
        options->x509_username_field = p[1];
    }
    #endif /* ENABLE_X509ALTUSERNAME */
    #ifdef ENABLE_PKCS11
    else if (streq(p[0], "show-pkcs11-ids") && !p[3])
    {
        char *provider =  p[1];
        bool cert_private = (p[2] == NULL ? false : ( atoi(p[2]) != 0 ));

        #ifdef DEFAULT_PKCS11_MODULE
        if (!provider)
        {
            provider = DEFAULT_PKCS11_MODULE;
        }
        else if (!p[2])
        {
            char *endp = NULL;
            int i = strtol(provider, &endp, 10);

            if (*endp == 0)
            {
                /* There was one argument, and it was purely numeric.
                 * Interpret it as the cert_private argument */
                provider = DEFAULT_PKCS11_MODULE;
                cert_private = i;
            }
        }
        #else  /* ifdef DEFAULT_PKCS11_MODULE */
        if (!provider)
        {
            msg(msglevel, "--show-pkcs11-ids requires a provider parameter");
            goto err;
        }
        #endif /* ifdef DEFAULT_PKCS11_MODULE */
        VERIFY_PERMISSION(OPT_P_GENERAL);

        set_debug_level(options->verbosity, SDL_CONSTRAIN);
        show_pkcs11_ids(provider, cert_private);
        openvpn_exit(OPENVPN_EXIT_STATUS_GOOD); /* exit point */
    }
    else if (streq(p[0], "pkcs11-providers") && p[1])
    {
        int j;

        VERIFY_PERMISSION(OPT_P_GENERAL);

        for (j = 1; j < MAX_PARMS && p[j] != NULL; ++j)
        {
            options->pkcs11_providers[j-1] = p[j];
        }
    }
    else if (streq(p[0], "pkcs11-protected-authentication"))
    {
        int j;

        VERIFY_PERMISSION(OPT_P_GENERAL);

        for (j = 1; j < MAX_PARMS && p[j] != NULL; ++j)
        {
            options->pkcs11_protected_authentication[j-1] = atoi(p[j]) != 0 ? 1 : 0;
        }
    }
    else if (streq(p[0], "pkcs11-private-mode") && p[1])
    {
        int j;

        VERIFY_PERMISSION(OPT_P_GENERAL);

        for (j = 1; j < MAX_PARMS && p[j] != NULL; ++j)
        {
            sscanf(p[j], "%x", &(options->pkcs11_private_mode[j-1]));
        }
    }
    else if (streq(p[0], "pkcs11-cert-private"))
    {
        int j;

        VERIFY_PERMISSION(OPT_P_GENERAL);

        for (j = 1; j < MAX_PARMS && p[j] != NULL; ++j)
        {
            options->pkcs11_cert_private[j-1] = atoi(p[j]) != 0 ? 1 : 0;
        }
    }
    else if (streq(p[0], "pkcs11-pin-cache") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->pkcs11_pin_cache_period = atoi(p[1]);
    }
    else if (streq(p[0], "pkcs11-id") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->pkcs11_id = p[1];
    }
    else if (streq(p[0], "pkcs11-id-management") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->pkcs11_id_management = true;
    }
    #endif /* ifdef ENABLE_PKCS11 */
    else if (streq(p[0], "rmtun") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->persist_config = true;
        options->persist_mode = 0;
    }
    else if (streq(p[0], "mktun") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->persist_config = true;
        options->persist_mode = 1;
    }
    else if (streq(p[0], "peer-id") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_PEER_ID);
        options->use_peer_id = true;
        options->peer_id = atoi(p[1]);
    }
    #ifdef HAVE_EXPORT_KEYING_MATERIAL
    else if (streq(p[0], "keying-material-exporter") && p[1] && p[2])
    {
        int ekm_length = positive_atoi(p[2]);

        VERIFY_PERMISSION(OPT_P_GENERAL);

        if (strncmp(p[1], "EXPORTER", 8))
        {
            msg(msglevel, "Keying material exporter label must begin with "
                "\"EXPORTER\"");
            goto err;
        }
        if (ekm_length < 16 || ekm_length > 4095)
        {
            msg(msglevel, "Invalid keying material exporter length");
            goto err;
        }

        options->keying_material_exporter_label = p[1];
        options->keying_material_exporter_length = ekm_length;
    }
    #endif /* HAVE_EXPORT_KEYING_MATERIAL */
    else if (streq(p[0], "allow-recursive-routing") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->allow_recursive_routing = true;
    }
    else if (streq(p[0], "vlan-tagging") && !p[1])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        options->vlan_tagging = true;
    }
    else if (streq(p[0], "vlan-accept") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL);
        if (streq(p[1], "tagged"))
        {
            options->vlan_accept = VLAN_ONLY_TAGGED;
        }
        else if (streq(p[1], "untagged"))
        {
            options->vlan_accept = VLAN_ONLY_UNTAGGED_OR_PRIORITY;
        }
        else if (streq(p[1], "all"))
        {
            options->vlan_accept = VLAN_ALL;
        }
        else
        {
            msg(msglevel, "--vlan-accept must be 'tagged', 'untagged' or 'all'");
            goto err;
        }
    }
    else if (streq(p[0], "vlan-pvid") && p[1] && !p[2])
    {
        VERIFY_PERMISSION(OPT_P_GENERAL|OPT_P_INSTANCE);
        options->vlan_pvid = positive_atoi(p[1]);
        if (options->vlan_pvid < OPENVPN_8021Q_MIN_VID
            || options->vlan_pvid > OPENVPN_8021Q_MAX_VID)
        {
            msg(msglevel,
                "the parameter of --vlan-pvid parameters must be >= %u and <= %u",
                OPENVPN_8021Q_MIN_VID, OPENVPN_8021Q_MAX_VID);
            goto err;
        }
    }
    else
    {
        int i;
        int msglevel = msglecvel_fc;
        /* Check if an option is in --ignore-unknown-option and
         * set warning level to non fatal */
        for (i = 0; options->ignore_unknown_option && options->ignore_unknown_option[i]; i++)
        {
            if (streq(p[0], options->ignore_unknown_option[i]))
            {
                msglevel = M_WARN;
                break;
            }
        }
        if (file)
        {
            msg(msglevel, "Unrecognized option or missing or extra parameter(s) in %s:%d: %s (%s)", file, line, p[0], PACKAGE_VERSION);
        }
        else
        {
            msg(msglevel, "Unrecognized option or missing or extra parameter(s): --%s (%s)", p[0], PACKAGE_VERSION);
        }
    }
err:
    gc_free(&gc);
}
