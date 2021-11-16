"""copy file or folder to a zip file"""
import argparse
import os
import zipfile


def get_args():
    """
    Get args specified in the cmd
    :return: Namespace object with all arguments
    """
    parser = argparse.ArgumentParser(
        description='Copy file or folder to a zip file'
    )
    parser.add_argument(
        'src',
        type=str,
        help='source of files',
        metavar='src'
    )
    parser.add_argument(
        'dst',
        type=str,
        help='path to save new zip file',
        metavar='dst'
    )
    return parser.parse_args()


def copy_files(src: str, dst: str):
    """
    Copies files from <src> to a zip file at <dst>
    :param src: source to copy from
    :param dst: zip file to write in
    :return: None
    """
    try:
        with zipfile.ZipFile(dst, 'w') as zip_file:
            if os.path.normpath(src) != os.path.normpath(dst) and \
                    os.path.isfile(src):
                zip_file.write(src)
            elif os.path.isdir(src):
                for subdir, _, files in os.walk(src):
                    for file in files:
                        path = os.path.join(subdir, file)
                        if os.path.abspath(path) == os.path.abspath(dst):
                            continue
                        zip_file.write(path, os.path.relpath(path, src))
    except OSError as e:
        print(e)


def main():
    """
    A main function
    :return: None
    """
    args = get_args()
    copy_files(args.src, args.dst)


if __name__ == '__main__':
    main()
