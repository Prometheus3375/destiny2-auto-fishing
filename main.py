from argparse import ArgumentParser
from collections import defaultdict
from collections.abc import Iterable

from predefined.image import *

DEFAULT_FISH_LIMIT = 50

if __name__ == '__main__':
    def group_by_name(available: Iterable[str], /) -> Iterable[str]:
        data = defaultdict(set)
        for name_resolution in available:
            name, _, resolution = name_resolution.partition('_')
            data[name].add(resolution)

        for name, resolutions in data.items():
            resolutions_str = ', '.join(resolutions)
            yield f'{name!r} ({resolutions_str})'


    def main():
        localizations_str = ', '.join(group_by_name(available_localizations))
        keys_str = ', '.join(group_by_name(available_keys))

        parser = ArgumentParser(description='A script for automatic fishing in Destiny 2')
        parser.add_argument('screen_width', type=int, help='the width of your screen in pixels')
        parser.add_argument('screen_height', type=int, help='the height of your screen in pixels')
        parser.add_argument(
            'localization',
            help='the localization you use in Destiny 2; case insensitive. '
                 f'Supported localizations with resolutions: {localizations_str}',
            )
        parser.add_argument(
            'interact_key',
            help='the interaction key you use in Destiny 2; case insensitive. '
                 f'Supported keys with resolutions: {keys_str}',
            )
        parser.add_argument(
            'fish_limit',
            nargs='?',
            default=50,
            type=float,
            help='the maximum number of fish this script is allowed to catch. '
                 'People reported that fish can disappear if there is around 60 uncollected fish. '
                 f"Defaults to {DEFAULT_FISH_LIMIT}. Put 'inf' to remove limit",
            )
        parser.add_argument(
            '--skip_initial_cast',
            '-sic',
            action='store_false',
            help='if present then the script will not cast fishing rod for the first time',
            )

        args = parser.parse_args()

        from fisher import start_fishing
        from methods.image import ImageMethod

        start_fishing(
            ImageMethod.from_predefined(
                screen_width=args.screen_width,
                screen_height=args.screen_height,
                localization=args.localization,
                key=args.interact_key,
                ),
            fish_limit=args.fish_limit,
            do_initial_cast=args.skip_initial_cast,
            )


    main()
