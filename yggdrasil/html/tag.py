

from abc import ABC
from dataclasses import dataclass
from typing import Optional, Set
from .base import HTMLComponent

__all__ = ['Tag']

DEFAULT_EMPTY_ELEMENT_TAGS: Set[str] = {
    'image'
    }

DEFAULT_BLOCK_ELEMENTS_TAGS: Set[str] = {
    "div", "article"
    }

DEFAULT_ELEMENT_TAG = set().union(
    DEFAULT_EMPTY_ELEMENT_TAGS,
    DEFAULT_BLOCK_ELEMENTS_TAGS)


class TagComponent(HTMLComponent,ABC):
    pass


def new_inline_tag(
    tag_name: str,
    content: str,
    **kwargs) -> TagComponent:
    ):
        



@dataclass
class InlineTag(TagComponent):
    tag_name: str
    content: str
    kwargs: Optional[dict] = None
    
    def __post_init__(self):
        # validate tag name
        if self.tag_name not in DEFAULT_ELEMENT_TAG:
            raise ValueError(
                f'Invalid tag name: {self.tag_name} to create an HTML tag.' +
                f'Valid tag names are: {DEFAULT_ELEMENT_TAG}')
            
    def render(self):
        attributes = ' '.join([f'{k}="{v}"' for k, v in self.kwargs.items()])
        return self._create_string_block(
            prefix=f'<{self.tag_name} {attributes}>',
            content=self.content,
            suffix=f'</{self.tag_name}>',
            inline=True)
        )
    # tag_name: str
    # children: Optional[list[HTMLComponent]] = None
    # kwargs: Optional[dict] = None
    
    # def __post_init__(self):
    #     # validate tag name
    #     if self.tag_name not in DEFAULT_ELEMENT_TAG:
    #         raise ValueError(
    #             f'Invalid tag name: {self.tag_name} to create an HTML tag.' +
    #             f'Valid tag names are: {DEFAULT_ELEMENT_TAG}')

    #     # TODO : allow string as children


    # def render(self):
    #     attributes = ' '.join([f'{k}="{v}"' for k, v in self.kwargs.items()])
    #     return f'<{self.tag_name} {attributes}>{self.content}</{self.tag_name}>'

    # def get_additional_files(self):
    #     return []




    
    # #: These HTML tags need special treatment so they can be
    # #: represented by a string class.
    # #:
    # #: For some of these tags, it's because the HTML standard defines
    # #: an unusual content model for them. I made this list by going
    # #: through the HTML spec
    # #: (https://html.spec.whatwg.org/#metadata-content) and looking for
    # #: "metadata content" elements that can contain strings.
    # #:
    # #: The Ruby tags (<rt> and <rp>) are here despite being normal
    # #: "phrasing content" tags, because the content they contain is
    # #: qualitatively different from other text in the document, and it
    # #: can be useful to be able to distinguish it.
    # #:
    # #: TODO: Arguably <noscript> could go here but it seems
    # #: qualitatively different from the other tags.
    # # _DEFAULT_STRING_CONTAINERS: Dict[str, Type[NavigableString]] = {
    # #     'rt' : RubyTextString,
    # #     'rp' : RubyParenthesisString,
    # #     'style': Stylesheet,
    # #     'script': Script,
    # #     'template': TemplateString,
    