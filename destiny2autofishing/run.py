from argparse import ArgumentParser, RawTextHelpFormatter


def from_command_line():
    """
    Starts fishing from command line arguments.
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

    # todo uncomment when version will be added
    # parser.add_argument(
    #     '-V',
    #     '--version',
    #     action='version',
    #     version=f'{destiny2autofishing.__name__} {destiny2autofishing.version}',
    #     help='If specified, the script prints its version and exits.',
    #     )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-c',
        '--config-file',
        help='Path to the configuration file.\n'
             'If it exists, the script starts fishing with this configuration.\n'
             'Otherwise, the script generates a sample '
             'configuration file at the specified path;\n'
             'any other argument is ignored in this case.',
        metavar='CONFIG_FILE_PATH',
        )

    from destiny2autofishing.predefined import available_configs

    predefined_names = '\n  '.join(map(repr, available_configs))
    group.add_argument(
        '-p',
        '--predefined-config',
        choices=available_configs,
        help='Name of the predefined configuration to use for fishing.\n'
             f'Available configurations:\n  {predefined_names}',
        metavar='PREDEFINED_CONFIG_NAME',
        )

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

    if predefined_specified := getattr(args, 'predefined_config', None):
        config_file = available_configs[predefined_specified]
    else:
        config_file = args.config_file

    from destiny2autofishing.configurator import Config

    config = Config(config_file)
    for k, v in overwritten.items():
        if v is not None:
            config.params[k] = v

    from destiny2autofishing.fisher import Fisher

    Fisher.from_config(config).start()


__all__ = 'from_command_line',