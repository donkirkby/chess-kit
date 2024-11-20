from xml.etree import ElementTree as ET  # noqa

LIGHT_SQUARE = 'transparent'  # transparent or cornsilk
DARK_SQUARE = 'black'  # black or #85440F (dark maple) or #C46316 (light maple)


class SvgPage:
    @staticmethod
    def register_svg():
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

    def __init__(self, width: float, height: float) -> None:
        self.root = ET.XML(f'<svg xmlns="http://www.w3.org/2000/svg" '
                           f'viewBox="0 0 {width} {height}" '
                           f'width="{width}" height="{height}"/>')
        self.width = width
        self.height = height

    def append(self, element: ET.Element) -> None:
        self.root.append(element)

    def append_text(self,
                    text: str,
                    attrib: dict[str, str] = None) -> ET.Element:
        if attrib is None:
            attrib = {}
        element = ET.Element('text', attrib=attrib)
        element.text = text
        self.append(element)
        return element

    def to_svg(self) -> str:
        return ET.tostring(self.root, encoding='unicode')


class SvgGroup:
    def __init__(self) -> None:
        self.scale = 1
        self.rotation = 0
        self.x = self.y = 0

    def to_element(self) -> ET.Element:
        group = ET.Element('g')
        group.set('transform',
                  f'translate({self.x} {self.y}) scale({self.scale}) '
                  f'rotate({self.rotation})')
        return group
