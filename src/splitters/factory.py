from typing import Any

from ..interfaces import ISplitter
from .character import CharacterSplitter
from .recursive_char import RecursiveSplitter
from .semantic import SemanticSplitter
from .sentence import SentenceSplitter
from .token import TokenSplitter

SPLITTER_MAP = {
    "character": CharacterSplitter,
    "recursive": RecursiveSplitter,
    "semantic": SemanticSplitter,
    "sentence": SentenceSplitter,
    "token": TokenSplitter,
}


def get_splitter(splitter_type: str, **kwargs: Any) -> ISplitter:
    splitter_class = SPLITTER_MAP.get(splitter_type)
    if not splitter_class:
        raise ValueError(f"Splitter type '{splitter_type}' is not supported.")
    return splitter_class(**kwargs)
