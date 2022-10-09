from dataclasses import dataclass


@dataclass
class ExtractedModel:
    """
        Generic class for storing any extracted data from PDFReader.
    """
    extracted_data: str
    ctx: str

    def __hash__(self):
        return hash(self.extracted_data)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.extracted_data == other.extracted_data
