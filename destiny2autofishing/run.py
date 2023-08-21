from argparse import ArgumentParser, RawTextHelpFormatter
from os.path import exists, isfile


def from_command_line(include_predefined: bool, /):
    """
    Starts fishing from command line arguments.
    :param include_predefined: If ``True``, then command line arguments will include
      an argument to specify a predefined configuration;
      this argument will be mutually exclusive with argument for config file.
    """
    import destiny2autofishing

    parser = ArgumentParser(
        prog=f'python -m {destiny2autofishing.__name__}',
        description='A script for automatic fishing in Destiny 2',
        formatter_class=RawTextHelpFormatter,
        add_help=False,
        )

    parser.add_argument(
        '-h',
        '--help',
        action='help',
        help='If specified, the script shows this help message and exits.',
        )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'{destiny2autofishing.__name__} {destiny2autofishing.version}',
        help='If specified, the script prints its version and exits.',
        )

    config_file_arg_kw = dict(
        help='Path to the configuration file.\n'
             'If it exists, the script starts fishing with this configuration.\n'
             'Otherwise, the script generates a sample '
             'configuration file at the specified path and exists;\n'
             'any other argument is ignored in this case.',
        metavar='CONFIG_FILE_PATH',
        )

    if include_predefined:
        from destiny2autofishing.predefined import available_configs

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-c', '--config-file', **config_file_arg_kw)

        predefined_names = '\n  '.join(map(repr, available_configs))
        group.add_argument(
            '-p',
            '--predefined-config',
            choices=available_configs,
            help='Name of the predefined configuration to use for fishing.\n'
                 f'Available configurations:\n  {predefined_names}',
            metavar='PREDEFINED_CONFIG_NAME',
            )
    else:
        parser.add_argument('config_file', **config_file_arg_kw)
        # Define this variable to supress error about unreferenced variable
        available_configs = None

    parser.add_argument(
        'fish_limit',
        nargs='?',
        default=None,
        type=float,
        help='The maximum number of fish this script is allowed to catch.\n'
             'People reported that fish can disappear if there is ~60 uncollected fish.\n'
             "Put 'inf' to disable the limit.",
        )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--no-initial-cast',
        action='store_const',
        const=False,
        dest='do_initial_cast',
        help='If specified, the fishing rod will not be cast at the start of the script.',
        )
    group.add_argument(
        '--do-initial-cast',
        action='store_const',
        const=True,
        dest='do_initial_cast',
        help='If specified, the fishing rod will be cast at the start of the script.',
        )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--disable-anti-afk',
        action='store_const',
        const=False,
        dest='enable_anti_afk',
        help='If specified, the script will not perform anti-AKF actions.',
        )
    group.add_argument(
        '--enable-anti-afk',
        action='store_const',
        const=True,
        dest='enable_anti_afk',
        help='If specified, the script will perform anti-AKF actions.',
        )

    args = parser.parse_args()
    overwritten = dict(
        enable_anti_afk=getattr(args, 'enable_anti_afk', None),
        do_initial_cast=getattr(args, 'do_initial_cast', None),
        fish_limit=args.fish_limit,
        )

    from destiny2autofishing.configurator import Config, generate_config

    if predefined_specified := getattr(args, 'predefined_config', None):
        config_file = available_configs[predefined_specified]
    else:
        config_file = args.config_file
        if not exists(config_file):
            generate_config(config_file)
            return

        if not isfile(config_file):
            raise OSError('Configuration file must be a .toml file, not a directory')

    config = Config(config_file)
    for k, v in overwritten.items():
        if v is not None:
            config.params[k] = v

    from destiny2autofishing.fisher import Fisher

    Fisher.from_config(config).start()


__all__ = 'from_command_line',
