import typing
from collections import Counter
from random import shuffle, choices
# noinspection PyPep8Naming
from xml.etree import ElementTree as ET

from svg_page import SvgGroup


def shade_to_colour(shade: int) -> str:
    return f'#{shade:02x}{shade:02x}{shade:02x}'

class SvgLetter(SvgGroup):
    def __init__(self, letter: str = '?', shade: int = 0) -> None:
        """ Initialize the SvgSquare.

        :param letter: The letter to display in the corners.
        :param shade: Background colour from 0 to 255.
        """
        super().__init__()
        self.letter = letter
        self.shade = shade
        self.base_size = 100

    def to_element(self) -> ET.Element:
        group = super().to_element()
        text = ET.Element('text', attrib={
        'x': '0',
        'y': '35',
        'text-anchor': 'middle',
        'font-family': 'FredokaOne',
        'font-size': '100',
        'fill': shade_to_colour(self.shade)})
        text.text = self.letter
        group.append(text)

        return group


class SvgSquare(SvgGroup):
    BASE_SIZE = 150
    def __init__(self,
                 letters: str = '?',
                 shade: int = 0) -> None:
        """ Initialize the SvgSquare.

        :param letters: The letter(s) to display in the corners.
        :param shade: Background colour from 0 to 255.
        """
        super().__init__()
        self.letters = letters
        self.shade = shade

    def to_element(self) -> ET.Element:
        group = super().to_element()
        border_shade = 128
        border_width = 2
        rect_size = full_size = 150
        rect_offset = 0
        rect_count = 4
        for rect_num in range(rect_count):
            rect_shade = border_shade + round(
                (rect_num / rect_count) * (self.shade - border_shade))
            fill_shade = border_shade + round(
                ((rect_num + 1) / rect_count) * (self.shade - border_shade))
            rect_colour = shade_to_colour(rect_shade)
            fill_colour = shade_to_colour(fill_shade)
            group.append(ET.Element('rect', {
                'fill': fill_colour,
                'x': str(rect_offset),
                'y': str(rect_offset),
                'width': str(rect_size),
                'height': str(rect_size),
                'stroke': rect_colour,
                'stroke-width': str(border_width)}))
            rect_size -= border_width * 2
            rect_offset = (full_size - rect_size) // 2
            border_width = 2
        for i, letter in enumerate(self.letters):
            top_letter = SvgLetter(letter, shade=255-self.shade)
            top_letter.x = 20 + 110 * i
            top_letter.y = 25
            top_letter.scale = 0.3
            top_letter.rotation = 180
            group.append(top_letter.to_element())
            bottom_letter = SvgLetter(letter, shade=255-self.shade)
            bottom_letter.x = 130 - 110 * i
            bottom_letter.y = 125
            bottom_letter.scale = 0.3
            group.append(bottom_letter.to_element())

        return group


class SvgPlank(SvgGroup):
    def __init__(self,
                 letters: typing.Sequence[str] = ('?', '?'),
                 shade: int = 0) -> None:
        super().__init__()
        self.letters = letters
        self.shade = shade

    def to_element(self) -> ET.Element:
        group = super().to_element()
        for i, square_letters in enumerate(self.letters):
            if i % 2:
                shade = 255 - self.shade
            else:
                shade = self.shade
            square = SvgSquare(square_letters, shade)
            square.x = i * 150
            group.append(square.to_element())
        return group


class SvgSheet(SvgGroup):
    def __init__(self,
                 lines: typing.Sequence[typing.Sequence[str]] = (('?', '?'),),
                 shade: int = 0) -> None:
        super().__init__()
        self.lines = lines
        self.shade = shade

    def to_element(self) -> ET.Element:
        group = super().to_element()
        for i, line in enumerate(self.lines):
            if i % 2:
                shade = 255 - self.shade
            else:
                shade = self.shade
            plank = SvgPlank(line, shade)
            plank.y = i * 150
            group.append(plank.to_element())

        return group

def make_lines(letter_counts: Counter[str],
               line_count: int,
               line_width: int) -> list[list[str]]:
    consonant_counts = Counter(letter_counts)
    vowel_counts = Counter()
    for vowel in 'AEIOUYaeiouy':
        try:
            vowel_counts[vowel] = consonant_counts.pop(vowel)
        except KeyError:
            pass
    lines = []
    for i in range(line_count):
        line = []
        line_consonant_counts = Counter(consonant_counts)
        line_vowel_counts = Counter(vowel_counts)
        remaining_lines = line_count - i
        vowel_count = vowel_counts.total() // remaining_lines
        consonant_count = line_width - vowel_count
        while vowel_count:
            weights = list(line_vowel_counts.values())
            population = list(line_vowel_counts)
            vowel = choices(population, weights)[0]

            line.append(vowel)
            vowel_counts[vowel] -= 1
            line_vowel_counts[vowel] /= 1000
            vowel_count -= 1
        while consonant_count:
            weights = list(line_consonant_counts.values())
            population = list(line_consonant_counts)
            consonant = choices(population, weights)[0]

            line.append(consonant)
            consonant_counts[consonant] -= 1
            line_consonant_counts[consonant] /= 1000
            consonant_count -= 1
        shuffle(line)
        lines.append(line)

    return lines
