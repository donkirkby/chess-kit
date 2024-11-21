from copy import deepcopy
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
from chess_deck import SvgCardBack, SvgCard, SvgGrid, parse_player_aids, SvgAid
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


def generate_images(aid_cards: dict[str, SvgCard]):
    image_folder = Path(__file__).parent / 'deck'
    image_folder.mkdir(exist_ok=True)
    card_back = SvgCardBack()
    generate_card_images(card_back, image_folder / 'back')
    for symbol in 'K Q R B N P k q r b n p C4 C7 C8 C9 c4 c7 c8 c9'.split():
        filename = image_folder / f'card-{symbol}'
        card = SvgCard(symbol, has_border=False)
        generate_card_images(card, filename)
    for game_name, aid_card in aid_cards.items():
        filename = (image_folder /
                    f'aid-{game_name.lower().replace(" ", "-")}')
        aid_card.has_border = False
        generate_card_images(aid_card, filename)


def main() -> None:
    page_size = pagesizes.letter
    top_margin = 0.25 * inch
    bottom_margin = 0.1 * inch
    side_margin = 0.675 * inch
    page_width, page_height = page_size
    content_width = page_width - side_margin*2
    register_fonts()
    styles = getSampleStyleSheet()
    image_cards = {}  # {name: SvgCard}

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
    title_paragraph = Paragraph('Chess Deck', title_style)
    subtitle_paragraph = Paragraph(
        'Designed by Don Kirkby. Find game rules at '
        '<a href="https://donkirkby.github.io/chess-kit/">'
        'donkirkby.github.io/chess-kit</a>.',
        body_style)
    title_paragraph.wrap(content_width, page_height)
    subtitle_paragraph.wrap(content_width, page_height)
    first_header_space = 0.125 * inch
    other_header_space = (title_paragraph.height +
                          title_paragraph.getSpaceAfter() +
                          subtitle_paragraph.height +
                          subtitle_paragraph.getSpaceAfter() +
                          first_header_space)
    cc_section = publish_rules.create_cc_section(doc, centred_style)
    footer_height = other_header_space / 2
    flowables = [title_paragraph,
                 subtitle_paragraph,
                 Spacer(0, first_header_space)]
    symbol_pages = [['rnbq', 'pppp'],
                    ['kbnr', 'pppp'],
                    ['PPPP', 'RNBQ'],
                    ['PPPP', 'KBNR'],
                    [['C4', 'C7', 'C8', 'C9'], ['c4', 'c7', 'c8', 'c9']]]
    page_grids = []
    for symbol_page in symbol_pages:
        grid = SvgGrid(symbol_page)
        page_grids.append(grid)

    player_aid_path = Path(__file__).parent / 'raw_rules' / 'player_aids.md'
    player_aid_markdown = player_aid_path.read_text()
    player_aid_groups = parse_player_aids(player_aid_markdown)
    player_aid_cards = []
    for game_name, markdown_states in player_aid_groups:
        aid = SvgAid(game_name, markdown_states)
        if game_name in image_cards:
            game_name += ' back'
        image_cards[game_name] = deepcopy(aid)
        player_aid_cards.append(aid)
    while player_aid_cards:
        symbol_pages.append([player_aid_cards[:4], player_aid_cards[4:8]])
        player_aid_cards = player_aid_cards[8:]
    for i, symbol_page in enumerate(symbol_pages):
        svg_page = SvgPage(7.5 * inch, 9 * inch)
        grid = SvgGrid(symbol_page)
        grid.scale = 7*inch / grid.base_height
        if i in (len(symbol_pages) - 3, len(symbol_pages) - 1):
            grid.rotation = 270
            grid.x = -0.075 * inch
            grid.y = grid.base_width * grid.scale
        else:
            grid.rotation = 90
            grid.x = 7*inch
        svg_page.append(grid.to_element())
        diagram = SvgDiagram(svg_page.to_svg()).to_reportlab()
        if i > 0:
            flowables.append(Spacer(0, other_header_space))
        flowables.append(diagram)
        if i < len(symbol_pages) - 1:
            flowables.append(Spacer(0, footer_height))
    flowables.extend(cc_section)
    doc.build(flowables)
    generate_images(image_cards)
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
