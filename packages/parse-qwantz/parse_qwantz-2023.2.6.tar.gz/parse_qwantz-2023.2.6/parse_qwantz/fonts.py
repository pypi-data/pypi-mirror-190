import string
from dataclasses import dataclass
from importlib.resources import as_file, files
from itertools import product
from pathlib import Path
from typing import NamedTuple, ContextManager

from PIL import Image

import parse_qwantz
from parse_qwantz.box import Box
from parse_qwantz.pixels import Pixel
from parse_qwantz.simple_image import SimpleImage

PRINTABLE = string.printable.strip()
FORBIDDEN_CHARS = '\\_`|~'

FONT_SIZES = [(13, 'Regular'), (12, 'Condensed'), (11, 'Small'), (9, 'Mini'), (8, 'Tiny')]
SHIFTED_VARIANTS = {
    13: {',': 1, ':': 1, '.': -1},
}


class CharBox(NamedTuple):
    char: str
    box: Box
    is_bold: bool

    def pixels(self, italic_offsets: set[int]):
        if not italic_offsets:
            return [
                (x, y)
                for x in range(self.box.left, self.box.right)
                for y in range(self.box.top, self.box.bottom)
            ]
        else:
            pixels = []
            italic_offset = len(italic_offsets)
            for y in range(self.box.top, self.box.bottom):
                if y - self.box.top in italic_offsets:
                    italic_offset -= 1
                for x in range(self.box.left, self.box.right):
                    pixels.append((x + italic_offset, y))
            return pixels

    @classmethod
    def space(cls, is_bold: bool) -> "CharBox":
        return cls(char=' ', box=Box.dummy(), is_bold=is_bold)


@dataclass
class Font:
    name: str
    width: int
    height: int
    shapes: dict[int, str]
    bold_shapes: dict[int, str]
    italic_offsets: set[int]
    top_pixel: int
    left_pixel: int

    def get_char(
        self,
        pixel: Pixel,
        image: SimpleImage,
        expect_bold: bool = False,
        expect_space: bool = True,
    ) -> CharBox | None:
        if char_box := self.get_char_with_weight(pixel, image, is_bold=expect_bold, expect_space=expect_space):
            return char_box
        return self.get_char_with_weight(pixel, image, is_bold=not expect_bold, expect_space=expect_space)

    def get_char_with_weight(
        self,
        pixel: Pixel,
        image: SimpleImage,
        is_bold: bool,
        expect_space: bool,
    ) -> CharBox | None:
        width = self.width + 1 if is_bold else self.width
        bottom_right = Pixel(pixel.x + width, pixel.y + self.height)
        bitmask = self._get_bitmask(pixel, image, is_bold)
        if char := self._get_char_by_bitmask(bitmask, is_bold):
            return CharBox(char, Box(pixel, bottom_right), is_bold)

        for cut_bottom in range(1, 3):
            cut_bitmask = bitmask & -(1 << (width * cut_bottom))
            if cut_bitmask == 0 or cut_bitmask & -cut_bitmask > (1 << (width * (cut_bottom + 1))):
                if char := self._get_char_by_bitmask(cut_bitmask, is_bold):
                    right, bottom = bottom_right
                    return CharBox(char, Box(pixel, Pixel(right, bottom - cut_bottom)), is_bold)

        for cut_top in range(1, 2):
            cut_bitmask = bitmask & ((1 << (width * (self.height - cut_top))) - 1)
            if cut_bitmask == 0 or cut_bitmask < (1 << (width * (self.height - cut_top - 1))):
                if char := self._get_char_by_bitmask(cut_bitmask, is_bold):
                    return CharBox(char, Box(Pixel(pixel.x, pixel.y + cut_top), bottom_right), is_bold)

        if expect_space:
            right, bottom = bottom_right
            for x, y in product(range(pixel.x, right), range(pixel.y, bottom)):
                if Pixel(x, y) in image.pixels:
                    if x >= right - width // 2 - 1:
                        return CharBox(' ', Box(pixel, Pixel(x, bottom)), is_bold)
                    break

    def _get_bitmask(self, pixel: Pixel, image: SimpleImage, is_bold: bool) -> int:
        width = self.width + 1 if is_bold else self.width
        return get_bitmask(pixel, image, width, self.height, self.italic_offsets)

    def _get_char_by_bitmask(self, bitmask: int, is_bold: bool) -> str | None:
        if bitmask == 0:
            return ' '
        shapes = self.bold_shapes if is_bold else self.shapes
        char = shapes.get(bitmask)
        if char and char not in FORBIDDEN_CHARS:
            return char

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Font(name={self.name}, width={self.width}, height={self.height})"

    @classmethod
    def from_file(
        cls,
        file_path_context_manager: ContextManager[Path],
        name: str,
        italic_offsets: set[int],
        shifted_variants: dict[str, int] | None = None,
    ) -> "Font":
        with file_path_context_manager as file_path:
            image = SimpleImage.from_image(Image.open(file_path))
        width = image.width // len(PRINTABLE)
        height = image.height
        shapes = {}
        for i, char in enumerate(PRINTABLE):
            bitmask = get_bitmask(
                Pixel(width * i, 0), image=image, width=width, height=height, italic_offsets=italic_offsets
            )
            shapes[bitmask] = char
            if shifted_variants and char in shifted_variants:
                shapes[get_shifted_variant(bitmask, width, height, shifted_variants[char])] = char
            cut_bitmask = bitmask & -(1 << width)
            if cut_bitmask != bitmask and char not in 'gq[]':
                shapes[cut_bitmask] = char
        top_pixel = max(get_top_pixel(bitmask, width, height) for bitmask in shapes)
        left_pixel = max(get_left_pixel(bitmask, width, height) for bitmask in shapes)
        return cls(
            name,
            width,
            height,
            shapes,
            get_bold_shapes(width, height, shapes),
            italic_offsets,
            top_pixel,
            left_pixel,
        )


def get_top_pixel(bitmask: int, width: int, height: int) -> int:
    for j in range(height):
        if bitmask & (((1 << width) - 1) << (width * (height - j - 1))):
            return j
    return 0


def get_left_pixel(bitmask: int, width: int, height: int) -> int:
    mask = sum(1 << (width * j) for j in range(height))
    for j in range(width):
        if bitmask & (mask << (width - j - 1)):
            return j
    return 0


def get_shifted_variant(shape: int, width: int, height: int, offset: int) -> int:
    shifted = 0
    mask = (1 << width) - 1
    for level in range(height):
        line = shape & mask
        if offset >= 0:
            shifted_line = line >> offset
        else:
            shifted_line = line << -offset
        shifted |= shifted_line << (level * width)
        shape >>= width
    return shifted


def get_bold_shapes(width: int, height: int, shapes: dict[int, str]) -> dict[int, str]:
    return {
        regular_shape_to_bold(shape, width, height): char
        for shape, char in shapes.items()
    }


def regular_shape_to_bold(shape: int, width: int, height: int) -> int:
    bold = 0
    mask = (1 << width) - 1
    for level in range(height):
        line = shape & mask
        bold_line = line | (line << 1)
        bold |= bold_line << (level * (width + 1))
        shape >>= width
    return bold


def get_bitmask(
    pixel: Pixel, image: SimpleImage, width: int, height: int, italic_offsets: set[int]
) -> int:
    bitmask = 0
    x0, y0 = pixel
    italic_offset = len(italic_offsets)
    for y in range(y0, y0 + height):
        if y - y0 in italic_offsets:
            italic_offset -= 1
        for x in range(x0, x0 + width):
            bitmask <<= 1
            if (x + italic_offset, y) in image.pixels:
                bitmask += 1
    return bitmask


ALL_FONTS = [
    Font.from_file(
        file_path_context_manager=as_file(files(parse_qwantz).joinpath(f'img/regular{size}.png')),
        name=name,
        italic_offsets=set(),
        shifted_variants=SHIFTED_VARIANTS.get(size, {}),
    )
    for size, name in FONT_SIZES
]

ALL_FONTS.append(
    Font.from_file(
        file_path_context_manager=as_file(files(parse_qwantz).joinpath(f'img/italic13.png')),
        name='Italic',
        italic_offsets={3, 5, 9, 11},
        shifted_variants={},
    )
)
