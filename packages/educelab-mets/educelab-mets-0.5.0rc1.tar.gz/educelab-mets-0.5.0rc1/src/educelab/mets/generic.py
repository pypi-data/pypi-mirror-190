from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union

from lxml import etree

from .constants import NAMESPACES, ElementTags
from .exceptions import ParseError
from .utils import _get_string_value, _check_tag


class METSElement(ABC):
    NAMESPACE = NAMESPACES['mets']

    @staticmethod
    @abstractmethod
    def tag():
        pass

    @staticmethod
    @abstractmethod
    def qname():
        pass

    @abstractmethod
    def generate_tree(self):
        pass

    @classmethod
    @abstractmethod
    def from_tree(cls, tree):
        pass


class XMLData(METSElement):
    def __init__(self, xml_data: Union[etree, str]) -> None:
        self.xml_data = xml_data
        return

    @staticmethod
    def tag() -> str:
        return ElementTags.XML_DATA.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(XMLData.NAMESPACE, ElementTags.XML_DATA.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())
        tree.append(self.xml_data)
        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> XMLData:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Only XMLData element can be parsed.')

        xml_data = XMLData(tree[0])

        return xml_data

    @property
    def xml_data(self) -> etree:
        return self._xml_data

    @xml_data.setter
    def xml_data(self, xml_data: Union[etree, str]) -> None:
        if type(xml_data) is str:
            try:
                xml_data = etree.fromstring(xml_data)
            except Exception as e:
                raise ParseError(e)
        self._xml_data = xml_data
        return

    def xml_string(self) -> str:
        return etree.tostring(self._xml_data, pretty_print=True).decode('UTF-8')


class BinData(METSElement):

    def __init__(self, bin_data: str) -> None:
        self.bin_data = _get_string_value(bin_data)
        return

    @staticmethod
    def tag() -> str:
        return ElementTags.BIN_DATA.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(BinData.NAMESPACE, ElementTags.BIN_DATA.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())
        tree.text = self.bin_data
        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> BinData:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Only BinData element can be parsed.')

        bin_data = BinData(tree.text)

        return bin_data

    @property
    def bin_data(self) -> str:
        return self._bin_data

    @bin_data.setter
    def bin_data(self, bin_data: str) -> None:
        self._bin_data = _get_string_value(bin_data)
        return
