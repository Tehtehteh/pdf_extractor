from typing import Protocol, List

from api.processor.model import ExtractedModel


class Extractor(Protocol):
    def extract(self, data: str) -> List[ExtractedModel]:
        ...
