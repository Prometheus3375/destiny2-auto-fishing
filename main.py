from fisher import start_fishing
from methods.image import ImageMethod

if __name__ == '__main__':
    start_fishing(
        ImageMethod.from_predefined(
            screen_width=1920,
            screen_height=1080,
            localization='english',
            key='E',
            ),
        # It was reported that fish can disappear if there is around 60 uncollected fish.
        # Putting 50 to be safe.
        fish_limit=50,
        do_initial_cast=True,
        )
