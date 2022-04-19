from grayscale_image import GrayscaleImage


def analyze_pic(path):
    """
    Analyzes the compression using lzw
    """
    image = GrayscaleImage.from_file(path)
    compressed_len = len(image.lzw_compression())
    uncompressed_len = (image.width() + 1) * image.height()
    print(f"Uncompressed image at {path} requires at least "
          f"{uncompressed_len} amount of bytes "
          f"(only values of pixels and next row symbols)\n"
          f"Compressed image requires at least "
          f"{compressed_len} amount of bytes "
          f"(to be fair each symbol might be more then byte)\n"
          f"So, overall result, LZW deflated "
          f"{100 * (1 - compressed_len/uncompressed_len)}%")


if __name__ == '__main__':
    analyze_pic(input("Enter a path to a picture:\n>>> "))
