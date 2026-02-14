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
    def __init__(self, letter: str = '?', shade: int = 0) -> None:
        """ Initialize the SvgSquare.

        :param letter: The letter to display in the corners.
        :param shade: Background colour from 0 to 255.
        """
        super().__init__()
        self.letter = letter
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
        top_letter = SvgLetter(self.letter, shade=255-self.shade)
        top_letter.x = 30
        top_letter.y = 35
        top_letter.scale = 0.5
        top_letter.rotation = 180
        group.append(top_letter.to_element())
        bottom_letter = SvgLetter(self.letter, shade=255-self.shade)
        bottom_letter.x = 120
        bottom_letter.y = 115
        bottom_letter.scale = 0.5
        group.append(bottom_letter.to_element())

        return group


class SvgPlank(SvgGroup):
    def __init__(self, letters: str = '??', shade: int = 0) -> None:
        super().__init__()
        self.letters = letters
        self.shade = shade

    def to_element(self) -> ET.Element:
        group = super().to_element()
        for i, letter in enumerate(self.letters):
            if i % 2:
                shade = 255 - self.shade
            else:
                shade = self.shade
            square = SvgSquare(letter, shade)
            square.x = i * 150
            group.append(square.to_element())
        return group


class SvgSheet(SvgGroup):
    def __init__(self, letters: str = '??', shade: int = 0) -> None:
        super().__init__()
        self.letters = letters
        self.shade = shade

    def to_element(self) -> ET.Element:
        group = super().to_element()
        lines = self.letters.splitlines()
        for i, line in enumerate(lines):
            if i % 2:
                shade = 255 - self.shade
            else:
                shade = self.shade
            plank = SvgPlank(line, shade)
            plank.y = i * 150
            group.append(plank.to_element())

        return group