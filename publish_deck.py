from pathlib import Path
from subprocess import run, Popen
from xml.etree import ElementTree as ET  # noqa

from reportlab.lib import pagesizes
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfdoc import PDFInfo
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

import publish_rules
from chess_deck import SvgCardBack, SvgCard, SvgGrid
from font_set import register_fonts
from svg_diagram import SvgDiagram
from svg_page import SvgPage


def generate_card_images(card: SvgCard, base_filename: Path) -> None:
    output_width = 750
    output_height = 1125
    for suffix, bleed in (('.svg', 0), ('.png', 0.04)):
        page = SvgPage(output_width, output_height)
        page.append(ET.Element('rect', dict(fill='white',
                                            width=str(output_width),
                                            height=str(output_height))))
        y_margin = page.height * bleed
        card.scale = (page.height - 2 * y_margin) / card.rect_height
        card.x = (page.width - card.rect_width * card.scale) / 2
        card.y = (page.height - card.rect_height * card.scale) / 2
        page.append(card.to_element())
        diagram_svg = page.to_svg()
        filename = base_filename.with_suffix(suffix)
        if suffix == '.svg':
            filename.write_text(diagram_svg)
        else:
            diagram = SvgDiagram(diagram_svg)
            diagram.to_cairo(filename,
                             output_width=output_width,
                             output_height=output_height)


def generate_images():
    image_folder = Path(__file__).parent / 'deck'
    image_folder.mkdir(exist_ok=True)
    card_back = SvgCardBack()
    generate_card_images(card_back, image_folder / 'back')
    for symbol in 'K Q R B N P k q r b n p C4 C7 C8 C9 c4 c7 c8 c9'.split():
        filename = image_folder / f'card-{symbol}'
        card = SvgCard(symbol, has_border=False)
        generate_card_images(card, filename)


def main() -> None:
    generate_images()
    page_size = pagesizes.letter
    top_margin = 0.85 * inch
    bottom_margin = 0.1 * inch
    side_margin = 0.6 * inch
    register_fonts()
    styles = getSampleStyleSheet()

    pdf_path = Path(__file__).parent / 'docs' / 'chess-deck.pdf'
    doc = SimpleDocTemplate(str(pdf_path),
                            title='Chess Deck',
                            author='Don Kirkby',
                            subject='Playing cards to match the 32 chess pieces',
                            keywords=['chess',
                                      'games',
                                      'card-games',
                                      'board-games',
                                      'puzzles'],
                            creator=PDFInfo.creator,
                            pagesize=page_size,
                            leftMargin=side_margin,
                            rightMargin=side_margin,
                            topMargin=top_margin,
                            bottomMargin=bottom_margin)
    title_style = styles['Title']
    title_style.fontName = 'Heading'
    body_style = styles['Normal']
    body_style.fontName = 'Body'
    centred_style = ParagraphStyle('Centred',
                                   parent=body_style,
                                   alignment=TA_CENTER)
    flowables = [
        Paragraph('Chess Deck', title_style),
        Paragraph('Designed by Don Kirkby. Find game rules at '
                  '<a href="https://donkirkby.github.io/chess-kit/">donkirkby.github.io/chess-kit</a>.',
                  body_style),
        Spacer(0, 0.125*inch)]
    symbol_pages = [['rnbq', 'pppp'],
                    ['kbnr', 'pppp'],
                    ['PPPP', 'RNBQ'],
                    ['PPPP', 'KBNR'],
                    [['C4', 'C7', 'C8', 'C9'], ['c4', 'c7', 'c8', 'c9']]]
    for symbol_page in symbol_pages:
        svg_page = SvgPage(7.5 * inch, 9 * inch)
        grid = SvgGrid(symbol_page)
        grid.rotation = 90
        grid.x = 7*inch
        grid.scale = 7*inch / grid.base_height
        svg_page.append(grid.to_element())
        diagram = SvgDiagram(svg_page.to_svg()).to_reportlab()
        flowables.append(diagram)
    flowables.extend(publish_rules.create_cc_section(doc, centred_style))
    doc.build(flowables)
    try:
        run(['pdfsizeopt', '--v=30', pdf_path, pdf_path])
    except FileNotFoundError:
        print('pdfsizeopt not installed, so PDF is not optimized.')
    try:
        Popen(["evince", pdf_path])
    except FileNotFoundError:
        print('PDF viewer evince is not installed.')
    print('Done.')


if __name__ == '__main__':
    main()
