if __name__ == '__main__':
    from argparse import ArgumentParser
    from os import listdir
    from os.path import join
    from destiny2autofishing.methods.image.functions import *


    def main():
        parser = ArgumentParser(
            description='Evaluates matrix difference between the main image and other ones '
                        'and proposes minimum required tolerance value. Supports PNG format only.',
            )

        parser.add_argument('main_image_file_path', help='path to the main image')
        parser.add_argument(
            'image_file_paths',
            nargs='*',
            help='space separated paths to image files',
            )

        parser.add_argument(
            '--dir',
            '-d',
            nargs='?',
            default=None,
            help='path to the directory with images',
            )

        args = parser.parse_args()

        with open_image(args.main_image_file_path) as im:
            main_matrix = image_matrix(im)

        other_images: list[str] = args.image_file_paths
        if args.dir:
            other_images.extend(
                join(args.dir, file)
                for file in listdir(args.dir)
                if file.endswith('.png')
                )

        for path in other_images:
            with open_image(path) as im:
                tolerance = difference_matrix_image(main_matrix, im)
                print(f'Tolerance for {path!r}:')
                print(f'{tolerance=!r}')
                print('-' * 20)


    main()
