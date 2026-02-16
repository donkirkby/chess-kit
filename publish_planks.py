from pathlib import Path
from random import seed
from subprocess import run, Popen
from xml.etree import ElementTree as ET  # noqa

from reportlab.lib import pagesizes
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfdoc import PDFInfo
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable

import publish_rules
from font_set import register_fonts
from letter_board import SvgSheet, SvgSquare, make_lines
from svg_diagram import SvgDiagram
from svg_page import SvgPage
from word_stats import WordCounter


def main() -> None:
    page_size = pagesizes.letter
    top_margin = 0.25 * inch
    bottom_margin = 0.1 * inch
    side_margin = 0.675 * inch
    page_width, page_height = page_size
    content_width = page_width - side_margin*2
    register_fonts()
    styles = getSampleStyleSheet()

    pdf_path = Path(__file__).parent / 'docs' / 'chess-planks.pdf'
    doc = SimpleDocTemplate(str(pdf_path),
                            title='Chess Planks',
                            author='Don Kirkby',
                            subject='Letter planks to make a chess board',
                            keywords=['chess',
                                      'games',
                                      'card-games',
                                      'board-games',
                                      'word-games'],
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
    # noinspection PyTypeChecker
    centred_style = ParagraphStyle('Centred',
                                   parent=body_style,
                                   alignment=TA_CENTER)
    title_paragraph = Paragraph('Chess Planks', title_style)
    subtitle_paragraph = Paragraph(
        'Designed by Don Kirkby. Find the rules for Secret Chesswords at '
        '<a href="https://donkirkby.github.io/chess-kit/new_rules.html#secret-chesswords">'
        'donkirkby.github.io/chess-kit/new_rules</a>.',
        body_style)
    title_paragraph.wrap(content_width, page_height)
    subtitle_paragraph.wrap(content_width, page_height)
    first_header_space = 0.125 * inch
    other_header_space = (title_paragraph.height +
                          title_paragraph.getSpaceAfter() +
                          subtitle_paragraph.height +
                          subtitle_paragraph.getSpaceAfter() +
                          first_header_space)
    footer_height = other_header_space / 2
    cc_section = publish_rules.create_cc_section(doc, centred_style)
    flowables: list[Flowable] = [title_paragraph,
                                 subtitle_paragraph,
                                 Spacer(0, first_header_space)]
    word_counter = WordCounter()
    word_path = Path(__file__).parent.parent / 'ludiverbia' / 'src' / "rawWords.csv"
    word_counter.count(word_path)
    seed(0)
    line_length = 6
    line_count = line_length*2
    total_squares = line_count * line_length
    letter_counts = word_counter.choose_letters('min', total_squares)
    sheet_lines = make_lines(letter_counts, line_count, line_length).splitlines()

    for i in range(2):
        if i % 2:
            shade = 255
        else:
            shade = 0
        sheet_letters = '\n'.join(sheet_lines[i * 6:(i + 1) * 6]).upper()
        svg_page = SvgPage(7.5 * inch, 9 * inch)
        sheet = SvgSheet(sheet_letters, shade)
        sheet.scale = 7 * inch / (SvgSquare.BASE_SIZE * 6)
        sheet.x = -0.075 * inch
        sheet.y = SvgSquare.BASE_SIZE * 0.1 * sheet.scale
        svg_page.append(sheet.to_element())
        diagram = SvgDiagram(svg_page.to_svg()).to_reportlab()
        flowables.append(diagram)
        if i == 0:
            flowables.append(Spacer(0, footer_height))
            flowables.append(Spacer(0, other_header_space))
    flowables.extend(cc_section)
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
