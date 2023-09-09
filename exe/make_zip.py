if __name__ == '__main__':
    import os
    import sys
    from zipfile import ZIP_LZMA, ZipFile

    import destiny2autofishing
    from destiny2autofishing import predefined

    name = destiny2autofishing.__name__
    predefined_dir = predefined.__path__[0]
    dist = sys.argv[1]
    config_dir = 'configs'

    with ZipFile(f'{dist}/{name}.zip', 'w', ZIP_LZMA) as z:
        z.write(f'{dist}/{name}.exe', f'{name}.exe')
        z.mkdir(config_dir)
        for name in os.listdir(predefined_dir):
            if name.endswith(('.png', '.toml')):
                z.write(f'{predefined_dir}/{name}', f'{config_dir}/{name}')
