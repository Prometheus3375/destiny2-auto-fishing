VERSION_INFO_TEMPLATE = """
VSVersionInfo(
    ffi=FixedFileInfo(
        filevers={file_version_4_tuple},
        prodvers={product_version_4_tuple},
        ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',
                    [
                        {string_struct_list},
                        ],
                    )
                ]
        ),
        VarFileInfo([VarStruct('Translation', [1033, 1200])]),
        ]
    )
""".lstrip()


def version_string_to_version_tuple(version: str, /) -> tuple[int, int, int, int]:
    """
    Converts a Python version string to a tuple of four integers.
    """
    parts = version.split('.')

    # Drop information about post, dev and pre releases
    last = parts[-1]
    if last.startswith('dev'):
        del parts[-1]
        last = parts[-1]

    if last.startswith('post'):
        del parts[-1]
        last = parts[-1]

    for s in ('a', 'b', 'rc'):
        start_i = last.find(s)
        if start_i > -1:
            parts[-1] = last[:start_i]
            break

    int_parts = [int(s) for s in parts]
    while len(int_parts) < 4:
        int_parts.append(0)

    return int_parts[0], int_parts[1], int_parts[2], int_parts[3]


def make_version_strings(
        out_file: str,
        /,
        *,
        version: str,
        creator: str,
        comments: str | None = None,
        company_name: str | None = None,
        file_description: str | None = None,
        internal_name: str | None = None,
        legal_copyright: str | None = None,
        legal_trademarks: str | None = None,
        original_filename: str | None = None,
        private_build: str | None = None,
        product_name: str | None = None,
        product_version: str | None = None,
        special_build: str | None = None,
        ):
    """
    Generates version information file for PyInstaller from the given keyword arguments.
    If ``product_version`` is unspecified, uses ``version`` for this field.
    """
    product_version = product_version or version
    strings: list[tuple[str, str]] = [
        ("FileVersion", version),
        ("ProductVersion", product_version),
        ("Creator", creator),
        ]

    if comments is not None:
        strings.append(('Comments', comments))
    if company_name is not None:
        strings.append(('CompanyName', company_name))
    if file_description is not None:
        strings.append(('FileDescription', file_description))
    if internal_name is not None:
        strings.append(('InternalName', internal_name))
    if legal_copyright is not None:
        strings.append(('LegalCopyright', legal_copyright))
    if legal_trademarks is not None:
        strings.append(('LegalTrademarks', legal_trademarks))
    if original_filename is not None:
        strings.append(('OriginalFilename', original_filename))
    if private_build is not None:
        strings.append(('PrivateBuild', private_build))
    if product_name is not None:
        strings.append(('ProductName', product_name))
    if special_build is not None:
        strings.append(('SpecialBuild', special_build))

    strings_repr = ',\n                        '.join(
        f'StringStruct({key!r}, {value!r})'
        for key, value in strings
        )

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(
            VERSION_INFO_TEMPLATE.format(
                file_version_4_tuple=version_string_to_version_tuple(version),
                product_version_4_tuple=version_string_to_version_tuple(product_version),
                string_struct_list=strings_repr,
                )
            )


if __name__ == '__main__':
    import destiny2autofishing
    from os.path import dirname, join

    copyright = None
    description = None

    with open('license.md') as f:
        for line in f:
            if line.startswith('Copyright'):
                copyright = line.strip()
                break

    with open('setup.cfg') as f:
        for line in f:
            if line.startswith('description'):
                _, _, value = line.partition('=')
                description = value.strip()
                break

    make_version_strings(
        join(dirname(__file__), 'version-info.py'),
        version=destiny2autofishing.version,
        creator='Prometheus3375',
        file_description=description,
        legal_copyright=copyright,
        original_filename=f'{destiny2autofishing.__name__}.exe',
        product_name='Destiny 2 Automatic Fishing',
        )
