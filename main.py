import os
import re
import sys
import svgutils
from scour import scour


BASE_PATH = '/Users/barisariburnu/Google Drive/Stock/publicdomainvectors/'


def remove_metadata(path):
    sv1 = svgutils.transform.fromfile(path)
    reg = re.compile('(\.\d)(pt)')  # regex to search numbers with "pt"
    svg = sv1.to_str().decode()  # svgutils delivers ascii byte strings.
    svg = reg.sub(r'\1', svg)  # the incorrectly added "pt" unit is removed here

    scour_options = scour.sanitizeOptions(options=None)  # get a clean scour options object
    scour_options.remove_metadata = True  # change any option you like
    clean_svg = scour.scourString(svg, options=scour_options)  # use scour

    return clean_svg


def svg_cleaner(source_path):
    only_files = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f))]

    for f in only_files:
        filename = os.path.splitext(os.path.basename(f))[0]
        extension = os.path.splitext(os.path.basename(f))[1]

        if extension != '.svg':
            continue

        full_path = os.path.join(source_path, f'{filename}{extension}')

        try:
            svg = remove_metadata(full_path)

            print(f'Update file: {full_path}')

            with open(full_path, "w") as fp:
                fp.write(svg)

        except Exception as ex:
            print(f"Error file: {full_path} \nError: {ex}")
            os.remove(full_path)


if __name__ == '__main__':
    path = sys.argv[1]
    if not os.path.exists(path):
        print(f'[ERROR] No such path: "{path}"')
        exit(0)

    svg_cleaner(path)

