# coding: utf-8

"""Provides the definition for different features related to documents."""


from enum import IntEnum, IntFlag, auto


class DocumentCapability(IntFlag):
    """Represents feature flags for a document."""

    NULL_CAPABILITY = auto()
    """Placeholder for abstract classes."""
    ASYNC_READ = auto()
    """Does this document needs to be opened asynchronously."""
    TOC_TREE = auto()
    """Does this document provide a table-of-content?"""
    METADATA = auto()
    """Does this document provide metadata about its author and pub date?"""
    STRUCTURED_NAVIGATION = auto()
    """Does this document provide symantic information about its content?"""
    TEXT_STYLE = auto()
    """Does this document provide style information about its content?"""
    GRAPHICAL_RENDERING = auto()
    """Does this document provide graphical rendition of its pages?"""
    SINGLE_PAGE = auto()
    """Is this a single page document."""
    IMAGE_EXTRACTION = auto()
    """Does this document supports extracting images out of pages?"""
    PAGE_LABELS = auto()
    """Does this document supports the notion of page labels?"""
    LINKS = auto()
    """
    Does this document support external links.
    Note: literal URLs can be deducted from the text using regexs.
    We refer to links that are masked by textual labels.
    """
    INTERNAL_ANCHORS = auto()
    """Does this document support internal links."""


class ReadingMode(IntEnum):
    DEFAULT = 0
    READING_ORDER = 1
    PHYSICAL = 2
    PAGINATION_BASED = 3
    CHAPTER_BASED = 4
    CLEAN_VIEW = 5
    FULL_TEXT_VIEW = 6


READING_MODE_LABELS = {
    ReadingMode.DEFAULT: _("Default reading mode"),
    ReadingMode.READING_ORDER: _("Reading order"),
    ReadingMode.PHYSICAL: _("Physical layout"),
    ReadingMode.PAGINATION_BASED: _("Paginated"),
    ReadingMode.CHAPTER_BASED: _("Chapter by chapter"),
    ReadingMode.CLEAN_VIEW: _("Clean text"),
    ReadingMode.FULL_TEXT_VIEW: _("Full text"),
}
