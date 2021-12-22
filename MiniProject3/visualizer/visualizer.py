#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
"""
Module for visualization of filler game
"""
import argparse
from PIL import Image, ImageDraw, ImageFont
from dumpparser import parse

FONT = ImageFont.FreeTypeFont("fonts/FreeMonoBold.ttf", 20)
INFO_WIDTH = 300
BACKGROUND_COLOR = (54, 54, 54)
PLAYER1_COLOR = (201, 58, 45)
PLAYER2_COLOR = (39, 141, 196)


def read_dump_file(path: str) -> str:
    """
    Reads dump file
    """
    with open(path, 'r') as file:
        return file.read()


def generate_gif(path_to_log: str, out_image: str):
    """
    Generates gif from dump file
    """
    history, player1_name, player2_name = parse(read_dump_file(path_to_log))
    images = []
    tile_size = int(500 / len(history[0][0]))
    width = tile_size * len(history[0][0][0]) + INFO_WIDTH
    height = tile_size * len(history[0][0])
    for field, _, _ in history:
        image = Image.new("RGBA", (width, height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(image)
        player1_count = 0
        player2_count = 0

        for row_idx, row in enumerate(field):
            for col_idx, tile in enumerate(row):
                if tile == 1:
                    player1_count += 1
                if tile == 2:
                    player2_count += 1
                color = {0: BACKGROUND_COLOR, 1: PLAYER1_COLOR, 2: PLAYER2_COLOR}[tile]
                box = (col_idx * tile_size, row_idx * tile_size, (col_idx + 1) * tile_size, (row_idx + 1) * tile_size)
                draw.rectangle(box, fill=color)

        player1_text = f"{player1_name}\n\n{player1_count}"
        text_width = draw.multiline_textsize(player1_text, font=FONT)[0]
        pos = (width - text_width - (INFO_WIDTH - text_width) // 2, 20)
        draw.text(pos, player1_text, font=FONT, fill=PLAYER1_COLOR)

        player2_text = f"{player2_name}\n\n{player2_count}"
        text_width = draw.multiline_textsize(player2_text, font=FONT)[0]
        pos = (width - text_width - (INFO_WIDTH - text_width) // 2, height / 2)
        draw.text(pos, player2_text, font=FONT, fill=PLAYER2_COLOR)

        images.append(image)
    images[0].save(out_image, save_all=True, append_images=images[1:], duration=10, loop=1)


def main():
    """
    Filler 42 visualizer
    To run:
    ./filler -f map00 -p1 player1.py -p2 player2.py > dump.txt
    python3.9 visualizer.py -file ../path/to/dump.txt -image ../path/to/image.gif
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-file", help="game log file")
    parser.add_argument("-image", help="out image dest")
    args = parser.parse_args()
    generate_gif(args.file, args.image)


if __name__ == "__main__":
    main()
