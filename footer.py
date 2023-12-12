from reportlab.pdfgen import canvas


class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, is_booklet=False, font_name='Times-Roman', **kwargs):
        super().__init__(*args, **kwargs)
        self.is_booklet = is_booklet
        self.font_name = font_name
        self.previous_bottom = 0

    def showPage(self):
        self.draw_canvas()
        super().showPage()

    def draw_canvas(self):
        x = 30
        width, height = self._pagesize

        template = getattr(self, '_doctemplate', None)
        if template is None:
            bottom = self.previous_bottom
        else:
            bottom = self.previous_bottom = template.bottomMargin

        self.saveState()
        self.setFont(self.font_name, 8 if self.is_booklet else 9)
        if self._pageNumber % 2:
            self.drawRightString(width-x, bottom, str(self._pageNumber))
        else:
            self.drawString(x, bottom, str(self._pageNumber))
        if self._pageNumber == 1:
            self.drawCentredString(width / 2,
                                   bottom,
                                   "https://donkirkby.github.io/chess-kit")
        self.restoreState()


class ZineCanvas(FooterCanvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        while len(self.pages) % 8 != 0:
            self.showPage()
        original_pages = self.pages[:]
        reordered_pages = []
        while original_pages:
            reordered_pages.append(original_pages.pop(1))
            reordered_pages.append(original_pages.pop(-2))
            reordered_pages.append(original_pages.pop(2))
            reordered_pages.append(original_pages.pop(-3))
            reordered_pages.append(original_pages.pop(-1))
            reordered_pages.append(original_pages.pop(0))
            reordered_pages.append(original_pages.pop(-1))
            reordered_pages.append(original_pages.pop(0))
        for page in reordered_pages:
            self.__dict__.update(page)
            super().showPage()
        super().save()
