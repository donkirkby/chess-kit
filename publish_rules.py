import logging
import os
import typing
from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter
from csv import DictReader
from datetime import datetime
from functools import partial
from logging import getLogger, basicConfig
from pathlib import Path
from subprocess import call
from textwrap import wrap, dedent

# noinspection PyPackageRequirements
from PIL import Image
from reportlab.graphics.shapes import Image as ReportLabImage, Drawing
from reportlab.lib import pagesizes
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.platypus.flowables import Spacer, KeepTogether, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet, ListStyle, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus.tableofcontents import TableOfContents
# noinspection PyUnresolvedReferences
from reportlab.rl_config import defaultPageSize
from space_tracer import LivePillowImage

from diagram import Diagram
from diagram_differ import LiveSvg, DiagramDiffer
from font_set import register_fonts
from footer import FooterCanvas
from book_parser import parse, Styles

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]

logger = getLogger(__file__)


def parse_args():
    default_markdown = str(Path(__file__).parent / 'raw_rules' / 'rules.md')
    # noinspection PyTypeChecker
    parser = ArgumentParser(description='Convert rules markdown into a PDF.',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--booklet',
                        action='store_true',
                        help='Use smaller pages for a booklet.')
    parser.add_argument('--no-merge',
                        action='store_true',
                        help="Don't write merged markdown, only PDF.")
    parser.add_argument('markdown',
                        type=FileType(),
                        nargs='?',
                        default=default_markdown,
                        help='markdown source file to convert')
    return parser.parse_args()


class DiagramWriter:
    def __init__(self,
                 target_folder: Path,
                 images_folder: Path,
                 is_disabled=False):
        self.diagram_count = 0
        self.target_folder = target_folder
        self.images_folder = images_folder
        self.diagram_differ = DiagramDiffer()
        self.diagram_differ.tolerance = 10
        self.is_disabled = is_disabled
        self.unused_images = set(images_folder.glob('diagram*.png'))

    def add_diagram(self, diagram: Diagram) -> Path:
        if self.is_disabled:
            return Path(os.devnull)

        self.diagram_count += 1
        svg_diagram = diagram.build()
        image = LiveSvg(svg_diagram)
        file_name = f'diagram{self.diagram_count}.png'
        target_path = self.images_folder / file_name
        relative_path = target_path.relative_to(self.target_folder)
        self.unused_images.remove(target_path)
        try:
            old_image = LivePillowImage(Image.open(target_path))
            self.diagram_differ.compare(old_image, image)
            if self.diagram_differ.diff_count == 0:
                return relative_path
        except IOError:
            pass
        image.write_png(target_path)
        return relative_path

    def remove_unused_images(self) -> None:
        for image_path in self.unused_images:
            image_path.unlink()


class RulesDocTemplate(SimpleDocTemplate):
    def __init__(self,
                 *args,
                 contents_descriptions: typing.Dict[str, str] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.contents_descriptions = contents_descriptions or {}
        self.bookmarks = {}  # {heading_text: key}
        self.first_headings = set()
        self.before_contents = True

    def create_link(self, heading_text):
        new_link = f'section{len(self.bookmarks)}'
        linked_text = heading_text + f'<a name="{new_link}"/>'
        self.bookmarks[heading_text] = new_link
        return linked_text

    def afterFlowable(self, flowable):
        if not isinstance(flowable, Paragraph):
            return
        if not flowable.style.name.startswith('Heading'):
            return
        heading_level = int(flowable.style.name[-1])
        if heading_level > 2:
            return
        heading_text = flowable.getPlainText()
        if heading_text == 'Table of Contents':
            self.before_contents = False
            return
        if self.before_contents or heading_text in self.first_headings:
            self.first_headings.add(heading_text)
            return
        description = self.contents_descriptions.get(heading_text)
        key = self.bookmarks.get(heading_text)
        if description:
            heading_text += ' '
            heading_text += description
        self.notify('TOCEntry',
                    (heading_level - 1, heading_text, self.page, key))


def load_contents_descriptions(contents_path: Path) -> typing.Dict[str, str]:
    if not contents_path.exists():
        return {}
    with contents_path.open() as f:
        reader = DictReader(f)
        # noinspection PyTypeChecker
        return {row['heading']: row['description']
                for row in reader}


def slug(heading: str) -> str:
    return heading.lower().replace(" ", "-")


def format_contents_markdown(
        contents_descriptions: typing.Dict[str, str]) -> str:
    display = '\n'.join(
        '\n    '.join(wrap(f'* [{heading}][{slug(heading)}] '
                           f'{description}',
                           break_on_hyphens=False))
        for heading, description in contents_descriptions.items())
    links = '\n'.join(f'[{slug(heading)}]: #{slug(heading)}'
                      for heading in contents_descriptions)
    return f'{display}\n\n{links}\n\n'


def main():
    basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s:%(name)s:%(message)s")
    args = parse_args()
    logger.info('Start.')
    markdown_path = Path(args.markdown.name)
    rules_stem = markdown_path.stem
    pdf_stem = 'chess-kit' if rules_stem == 'rules' else rules_stem
    source_path = Path(__file__).parent
    pdf_path = source_path / 'docs' / (pdf_stem + '.pdf')
    merged_path = pdf_path.parent / (rules_stem + '.md')
    images_path = pdf_path.parent / 'images' / rules_stem
    if not args.no_merge:
        images_path.mkdir(parents=True, exist_ok=True)
    contents_path = markdown_path.parent / (rules_stem + '_contents.csv')
    contents_descriptions = load_contents_descriptions(contents_path)
    unlinked_section_names = set(contents_descriptions)
    register_fonts()

    with args.markdown:
        states = parse(args.markdown.read())
    diagram_writer = DiagramWriter(pdf_path.parent,
                                   images_path,
                                   is_disabled=args.no_merge)
    if args.booklet:
        page_size = (4.25 * inch, 6.875 * inch)
        vertical_margin = 0.3 * inch
        side_margin = 0.5 * inch
    else:
        page_size = pagesizes.letter
        vertical_margin = 0.625 * inch
        side_margin = inch

    doc = RulesDocTemplate(str(pdf_path),
                           author='Don Kirkby',
                           pagesize=page_size,
                           leftMargin=side_margin,
                           rightMargin=side_margin,
                           topMargin=vertical_margin,
                           bottomMargin=vertical_margin,
                           contents_descriptions=contents_descriptions)
    styles = getSampleStyleSheet()
    for style in styles.byName.values():
        if hasattr(style, 'fontSize'):
            if style.name.startswith('Heading'):
                scale = 1.5
                style.fontName = 'Heading'
            else:
                scale = 2
                style.fontName = 'Body'
            if False and args.booklet:
                style.fontSize *= scale
                style.leading *= scale
    paragraph_style = styles[Styles.Normal]
    numbered_list_style = ListStyle('default_list',
                                    bulletFontName='Body',
                                    bulletFontSize=paragraph_style.fontSize,
                                    leftIndent=paragraph_style.fontSize * 1.5,
                                    bulletFormat='%s.')
    bulleted_list_style = ListStyle('default_list',
                                    bulletFontName='Body',
                                    bulletFontSize=paragraph_style.fontSize,
                                    leftIndent=paragraph_style.fontSize * 1.5)
    centred_style = ParagraphStyle('Author',
                                   parent=paragraph_style,
                                   alignment=TA_CENTER)
    story = []
    group = []
    bulleted = []
    headings = []
    first_bullet = None
    image_width = 800
    image_height = 600
    toc = TableOfContents(dotsMinLevel=0)
    toc.levelStyles = [ParagraphStyle('toc',
                                      parent=paragraph_style,
                                      leftIndent=10,
                                      firstLineIndent=-10,
                                      leading=16),
                       ParagraphStyle('toc',
                                      parent=paragraph_style,
                                      leftIndent=20,
                                      firstLineIndent=-10,
                                      leading=16)]
    cc_aspect = 88 / 31
    cc_width = page_size[0] * 0.1
    padding = 6
    cc_height = cc_width / cc_aspect
    cc_drawing = Drawing(doc.width, cc_height * 2)
    cc_drawing.add(ReportLabImage(
        (doc.width - cc_width) / 2 - padding, 0,
        cc_width, cc_height,
        'docs/images/cc-by-sa.png'))
    for state in states:
        if state.style == Styles.Metadata:
            doc.title = state.text
            title_text = state.text
            subtitle_text = state.subtitle
            if title_text == 'The Rules of Chess Kit':
                title_text = 'Chess Kit'
                subtitle_text = 'Lighthearted New Games for Your Chess Set'
            if args.booklet:
                story.append(Spacer(0, page_size[1] * 0.3))
            title_style = ParagraphStyle('MainTitle',
                                         parent=styles['Heading1'],
                                         alignment=TA_CENTER)
            story.append(Paragraph(title_text, title_style))
            if subtitle_text:
                subtitle_style = ParagraphStyle('Subtitle',
                                                parent=paragraph_style,
                                                alignment=TA_CENTER,
                                                fontName='Body-Italic')
                story.append(Paragraph(subtitle_text, subtitle_style))
            if args.booklet:
                story.append(Spacer(0, page_size[1] * 0.15))
                story.append(Paragraph('Don Kirkby', centred_style))
                story.append(Spacer(0, page_size[1] * 0.15))
                story.append(Paragraph('???-?-????-????-?', centred_style))
                story.append(Paragraph('Imprint: Lulu.com', centred_style))
                story.append(cc_drawing)
                story.append(Paragraph(f'{datetime.now().year}', centred_style))
                story.append(PageBreak())
            continue
        elif state.style == Styles.Diagram:
            flowable = Diagram(doc.width,
                               doc.height,
                               state.text).build().to_reportlab()
            state.image_path = diagram_writer.add_diagram(Diagram(
                image_width,
                image_height,
                state.text))
        else:
            flowable = Paragraph(state.text,
                                 styles[state.style])
        if state.style.startswith(Styles.Heading):
            heading_level = int(state.style[-1])
            if heading_level < 3:
                logger.info(state.text)
            linked_text = doc.create_link(state.text)
            flowable = Paragraph(linked_text, styles[state.style])
            unlinked_section_names.discard(state.text)
            if bulleted:
                create_list_flowable(bulleted,
                                     group,
                                     story,
                                     first_bullet,
                                     bulleted_list_style,
                                     numbered_list_style)
                group = []
                bulleted = []
                first_bullet = None
            if heading_level < 3 and not group:
                story.append(PageBreak())
            group.append(flowable)
            headings = headings[:heading_level]
            while len(headings) < heading_level:
                headings.append(None)
            headings[heading_level - 1] = state.text
            if state.text == 'Table of Contents':
                state.extra_markdown = format_contents_markdown(
                    contents_descriptions)
                story.append(KeepTogether(group))
                story.append(toc)
                group = []
        elif state.bullet:
            bulleted.append(flowable)
            first_bullet = first_bullet or state.bullet
        else:
            if bulleted:
                create_list_flowable(bulleted,
                                     group,
                                     story,
                                     first_bullet,
                                     bulleted_list_style,
                                     numbered_list_style)
                group = []
                bulleted = []
                first_bullet = None
                story.append(Spacer(1, 0.055 * inch))
            if not group:
                story.append(flowable)
            else:
                group.append(flowable)
                story.append(KeepTogether(group))
                group = []
            story.append(Spacer(1, 0.055 * inch))
    if bulleted:
        create_list_flowable(bulleted,
                             group,
                             story,
                             first_bullet,
                             bulleted_list_style,
                             numbered_list_style)
    diagram_writer.remove_unused_images()
    if not args.booklet:
        story.append(cc_drawing)
        story.append(Paragraph(
            f'<a href="https://creativecommons.org/licenses/by-sa/4.0/">'
            f'{datetime.now().year}</a>',
            centred_style))
    if unlinked_section_names:
        if len(unlinked_section_names) > 1:
            suffix = 's'
        else:
            suffix = ''
        unknown_section_message = (f'Unknown section{suffix} in contents: ' +
                                   ', '.join(unlinked_section_names))
        raise ValueError(unknown_section_message)
    doc.multiBuild(story, canvasmaker=partial(FooterCanvas,
                                              font_name='Body',
                                              is_booklet=args.booklet))
    if not args.no_merge:
        with merged_path.open('w') as merged_file:
            for state in states:
                state.write_markdown(merged_file)
            merged_file.write(dedent('''\

                [![cc-logo]][cc-by-sa]

                [cc-logo]: images/cc-by-sa.png
                [cc-by-sa]: https://creativecommons.org/licenses/by-sa/4.0/
                '''))

    logger.info('Done.')
    call(["evince", pdf_path])


def create_list_flowable(bulleted,
                         group,
                         story,
                         first_bullet,
                         bulleted_list_style,
                         numbered_list_style):
    if first_bullet == '*':
        bullet_type = 'bullet'
        first_bullet = None
        list_style = bulleted_list_style
    else:
        bullet_type = '1'
        list_style = numbered_list_style
    group.append(ListFlowable(bulleted[:1],
                              style=list_style,
                              bulletType=bullet_type,
                              start=first_bullet))
    story.append(KeepTogether(group))
    bulleted = bulleted[1:]
    if bulleted:
        if first_bullet is not None:
            next_bullet = int(first_bullet) + 1
        else:
            next_bullet = first_bullet
        story.append(ListFlowable(bulleted,
                                  style=list_style,
                                  bulletType=bullet_type,
                                  start=next_bullet))


if __name__ == '__main__':
    main()
