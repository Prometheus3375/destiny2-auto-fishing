from argparse import ArgumentParser

from PIL.Image import open as open_image

from methods.image.functions import *

if __name__ == '__main__':
    def main():
        parser = ArgumentParser(
            description='Takes a path to an image file, '
                        'converts it to grayscale and evaluates '
                        'average color for every row and column.\n'
                        'If two paths are given, then converts both images to grayscale '
                        'and evaluates absolute difference between '
                        'their average values for every row and colum '
                        'and minimum required tolerance',
            )

        parser.add_argument('image_file_path', help='a path to an image file')
        parser.add_argument(
            'second_image_file_path',
            nargs='?',
            default=None,
            help='a path to an image file',
            )

        args = parser.parse_args()

        if args.second_image_file_path is None:
            with open_image(args.image_file_path) as image:
                avg_x, avg_y = calculate_averages(image.convert('L'))
                x_averages = list(avg_x)
                y_averages = list(avg_y)
                print(f'{x_averages=!r}')
                print(f'{y_averages=!r}')
        else:
            with (open_image(args.image_file_path) as im1,
                  open_image(args.second_image_file_path) as im2):
                diff_x, diff_y = calculate_difference(im1, im2)
                diff_x = list(diff_x)
                diff_y = list(diff_y)
                tolerance = max(*diff_x, *diff_y) + 1
                print(f'{diff_x=!r}')
                print(f'{diff_y=!r}')
                print(f'{tolerance=!r}')


    main()
