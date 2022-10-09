from typing import List, Optional

from PyPDF2 import PdfReader

from api.processor.extractor import Extractor, ExtractedModel


DEFAULT_FOOTER_MARKER_THRESHOLD = 50


class PDFProcessor:
    """
        PDFReader implementation via PyPDF2 python library. Splits raw text from pdf file into list of strings.
        Example:
            >>> pdf_reader = PDFProcessor('filename.pdf')
            >>> for text in pdf_reader.iter_content():
            >>>     print(text)
            # todo: Merge logically set up strings into sentences for easier context management.
        Can also handle footer/header via "smart" markers (pypdf2 feature): when reading raw text from pdf file
        we start with 0 Y offset and assume next Y jump would be start of the content and if next Y jump
        is greated than `_footer_marker_y` then we assume that Y to be footer offset.
    """
    def __init__(self, file_uri: str,
                 footer_marker_threshold: Optional[int] = DEFAULT_FOOTER_MARKER_THRESHOLD):
        self._reader: PdfReader = PdfReader(file_uri)
        self.header_y: int = 0
        self._text_wrapper: List[str] = []
        self._can_read_less_y: int = 0
        self._can_read_more_y: int = 0
        self._footer_marker_y: int = footer_marker_threshold or DEFAULT_FOOTER_MARKER_THRESHOLD

    @property
    def reader(self) -> PdfReader:
        return self._reader

    def _make_smart_read_visitor(self):
        """
            Creates visitor function to filter any raw text out of header/footer bounds.
            Read results are stored in `self._text_wrapper`
        """
        def reader_visitor(text, cm, tm, font_dict, font_size):
            y = tm[5]
            x = tm[4]
            if not self._can_read_more_y and 0 < y < self._footer_marker_y:
                self._can_read_more_y = y
            if not self._can_read_less_y and (y - self._can_read_more_y) > self._footer_marker_y:
                self._can_read_less_y = y
                self._can_read_less_x = x
            if self._can_read_more_y < y:
                if text and text != '\n':
                    self._text_wrapper.append(text)
        return reader_visitor

    def iter_content(self):
        for page in self.reader.pages:
            page.extract_text(visitor_text=self._make_smart_read_visitor())
            yield self._text_wrapper
            self._text_wrapper = []

    def run_extractor(self, extractor: Extractor) -> List[ExtractedModel]:
        """
            Runs any extractor on a raw text and combines results of extractor into a list of `ExtractedModel` class.
        :param extractor: Extractor interface implementor
        :return: list of extracted models: extracted_data and context.
        """
        result = []
        # First we try to fetch document info from PDF metadata
        created_at = self.get_created_at_extracted_model()
        if created_at:
            result.append(created_at)
        for page in self.iter_content():
            for detected_sentence in page:
                for extracted_model in extractor.extract(detected_sentence):
                    if extracted_model not in result:
                        result.append(extracted_model)
        for form, form_value in self.reader.get_form_text_fields().items():
            for extracted_model in extractor.extract(form_value):
                if extracted_model not in result:
                    result.append(extracted_model)
        return result

    def get_created_at_extracted_model(self) -> Optional[ExtractedModel]:
        if self.reader.documentInfo:
            try:
                created_date = self.reader.documentInfo.creation_date
                if created_date:
                    return ExtractedModel(str(created_date), 'Created at')
            except Exception as e:
                return None
