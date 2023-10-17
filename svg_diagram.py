from io import BytesIO, StringIO

import reportlab.graphics.shapes as reportlab_shapes
from cairosvg import svg2png
from svglib.svglib import svg2rlg


class SvgDiagram:
    def __init__(self, svg_text: str):
        self.svg_text = svg_text

    def to_reportlab(self) -> reportlab_shapes.Drawing:
        svg_bytes = self.svg_text.encode()
        drawing = svg2rlg(BytesIO(svg_bytes))
        return drawing

    def to_cairo(self, png_file: str):
        svg2png(file_obj=StringIO(self.svg_text),
                write_to=png_file,
                background_color='transparent')
