import re
from typing import List, Optional, Pattern
from dateutil import parser

from api.processor.extractor import Extractor, ExtractedModel

# List of known date matchers
# Note: this is suboptimal, probably best to keep these in a config
_default_date_matchers: List[Pattern] = [
    re.compile(r'([^0]\d{1,2}\s?[a-zA-z]+\s?\d{4})'),
    re.compile(r'.*(\d{1,2}/\d{1,2}/\d{4})'),
    re.compile(r'.*([^0]\d{1,2}\.\d{1,2}\.\d{4})'),
    re.compile(r'.*([^0]\d{1,2}\s*([Jj]anuary|[Ff]ebruary|[Mm]arch|[Aa]pril|'
               r'[Mm]ay|[Jj]une|[Jj]uly|[Aa]ugust|[Ss]eptember|[Oo]ctober|[Nn]ovember|[Dd]ecember)\s*\d{4})'),
    re.compile(r'.*(([Jj]anuary|[Ff]ebruary|[Mm]arch|[Aa]pril|[Mm]ay|'
               r'[Jj]une|[Jj]uly|[Aa]ugust|[Ss]eptember|[Oo]ctober|[Nn]ovember|[Dd]ecember)\s*\d{1,2}[\s,]*\d{4})'),
]


class DateExtractor(Extractor):
    """
        Class for extracting date information from input string.
        Example usage:
        >>> date_extractor = DateExtractor()
        >>> extracted_date = date_extractor.extract("10 June 1995 - I was born")
    """
    def __init__(self, matchers: Optional[List[Pattern]] = None):
        self.matchers = matchers or _default_date_matchers
        self.start_str_marker: str = '.'

    def extract(self, data: Optional[str]) -> List[ExtractedModel]:
        """
            Runs input string through regex matchers and extracts date as well as context.
            In this case context would be whole string.
        """
        result: List[ExtractedModel] = []
        if not data:
            return []
        for matcher in self.matchers:
            if match := matcher.match(data):
                matched_str = match.group(1)
                if matched_str.startswith(' '):
                    matched_str = matched_str.strip()
                parsed_date = parser.parse(matched_str)
                result.append(ExtractedModel(str(parsed_date), self._sanitize_data(data)))
        return result

    def _sanitize_data(self, data_str: str) -> str:
        """
            Strips input string to a last sentence. Probably not a best idea for when extracted date
            is in a middle of an input string.
        """
        idx = data_str.rfind(self.start_str_marker)
        if idx + 1 == len(data_str):
            idx = data_str[:idx-1].rfind(self.start_str_marker)
        return data_str[idx + 1:]
