from __future__ import annotations

import logging
from importlib import resources
from typing import Union

from lxml import etree

# noinspection PyUnresolvedReferences
from . import schemas
from .behavior import BehaviorSection
from .constants import ElementTags, AttributeTags, NAMESPACES, \
    METS_SCHEMA_VERSION
from .exceptions import ParseError
from .file_sec import FileSection
from .generic import METSElement
from .header import Header
from .metadata import DescriptiveMetadataSection, AdministrativeMetadataSection
from .structure import StructuralMap, StructuralLink
from .utils import _get_element_list, _add_attribute_to_tree, _get_string_value, \
    _add_mets_class, _check_tag


class METSDocument(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value,
        AttributeTags.OBJID.value,
        AttributeTags.LABEL.value,
        AttributeTags.TYPE.value,
        AttributeTags.PROFILE.value
    ]

    # TODO: add check for uri values?
    def __init__(self, struct_map: Union[StructuralMap, list[StructuralMap]],
                 header: Header = None,
                 amd: Union[AdministrativeMetadataSection, list[
                     AdministrativeMetadataSection]] = None,
                 dmd: Union[DescriptiveMetadataSection, list[
                     DescriptiveMetadataSection]] = None,
                 file_sec: FileSection = None,
                 struct_link: StructuralLink = None,
                 behavior: Union[BehaviorSection, list[BehaviorSection]] = None,
                 element_id: str = None,
                 objid: str = None, label: str = None, mets_type: str = None,
                 profile: str = None,
                 other_attribs: dict[str, str] = None) -> None:
        self.struct_map = struct_map
        self.header = header
        self.amd = amd
        self.dmd = dmd
        self.file_sec = file_sec
        self.struct_link = struct_link
        self.behavior = behavior
        self.id = element_id
        self.objid = objid
        self.label = label
        self.type = mets_type
        self.profile = profile
        self._namespaces = NAMESPACES

        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.METS.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(METSDocument.NAMESPACE, ElementTags.METS.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname(),
                             nsmap=self._namespaces)  # Needs to be changed for custom ns on creation

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.OBJID, self.objid)
        _add_attribute_to_tree(tree, AttributeTags.LABEL, self.label)
        _add_attribute_to_tree(tree, AttributeTags.TYPE, self.type)
        _add_attribute_to_tree(tree, AttributeTags.PROFILE, self.profile)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        if self.header is not None:
            tree.append(self.header.generate_tree())
        if self.dmd is not None:
            for item in self.dmd:
                tree.append(item.generate_tree())
        if self.amd is not None:
            for item in self.amd:
                tree.append(item.generate_tree())
        if self.file_sec is not None:
            tree.append(self.file_sec.generate_tree())
        for item in self.struct_map:
            tree.append(item.generate_tree())
        if self.struct_link is not None:
            tree.append(self.struct_link.generate_tree())
        for item in self.behavior:
            tree.append(item.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> METSDocument:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Only METS element can be parsed.')

        header = file_sec = struct_link = None
        dmd = []
        amd = []
        struct_map = []
        beh_sec = []
        for child in tree:
            if child.tag == Header.tag() or child.tag == str(Header.qname()):
                header = Header.from_tree(child)
            elif child.tag == DescriptiveMetadataSection.tag() or child.tag == str(
                    DescriptiveMetadataSection.qname()):
                dmd.append(DescriptiveMetadataSection.from_tree(child))
            elif child.tag == AdministrativeMetadataSection.tag() or \
                    child.tag == str(AdministrativeMetadataSection.qname()):
                amd.append(AdministrativeMetadataSection.from_tree(child))
            elif child.tag == FileSection.tag() or child.tag == str(
                    FileSection.qname()):
                file_sec = FileSection.from_tree(child)
            elif child.tag == StructuralMap.tag() or child.tag == str(
                    StructuralMap.qname()):
                struct_map.append(StructuralMap.from_tree(child))
            elif child.tag == StructuralLink.tag() or child.tag == str(
                    StructuralLink.qname()):
                struct_link = StructuralLink.from_tree(child)
            elif child.tag == BehaviorSection.tag() or child.tag == str(
                    BehaviorSection.qname()):
                beh_sec.append(BehaviorSection.from_tree(child))

        other = {}
        for key in tree.keys():
            if key not in METSDocument._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        doc = METSDocument(struct_map, header=header, dmd=dmd, amd=amd,
                           file_sec=file_sec, struct_link=struct_link,
                           behavior=beh_sec,
                           element_id=tree.get(AttributeTags.ID.value),
                           objid=tree.get(AttributeTags.OBJID.value),
                           label=tree.get(AttributeTags.LABEL.value),
                           mets_type=tree.get(AttributeTags.TYPE.value),
                           profile=tree.get(AttributeTags.PROFILE.value),
                           other_attribs=other)

        doc._namespaces = tree.nsmap

        return doc

    @classmethod
    def validation(cls, tree: etree) -> bool:
        logger = logging.getLogger(__name__)
        schema_file = f'mets-{METS_SCHEMA_VERSION}.xsd'
        resource_path = resources.files('educelab.mets.schemas')
        xsd_path = resource_path / schema_file
        logger.debug(f'Loading schema: {xsd_path}')
        xmlschema = etree.XMLSchema(file=xsd_path)
        if not xmlschema.validate(tree):
            log = xmlschema.error_log
            print('Failed to validate against METS schema')
            print(log)
            return False
        else:
            return True

    @classmethod
    def from_file(cls, file: str) -> METSDocument:
        logger = logging.getLogger(__name__)
        logger.debug('Creating parser')
        parser = etree.XMLParser(remove_comments=True,
                                 remove_blank_text=True)
        logger.debug(f'Loading file: {file}')
        tree = etree.parse(file, parser=parser).getroot()

        logger.debug('Validating tree')
        if cls.validation(tree):
            logger.debug('Converting tree to METS doc')
            doc = cls.from_tree(tree)
            return doc
        else:
            raise ParseError('File does not adhere to the METS schema')

    def write_to_file(self, file: str) -> None:
        tree = self.generate_tree()
        if METSDocument.validation(tree):
            try:
                root = etree.ElementTree(tree)
                root.write(file, pretty_print=True, xml_declaration=True,
                           encoding="utf-8")
            except Exception as e:
                raise OSError(
                    'Could not write to file ' + str(file) + '/nReason: ' + str(
                        e))
        else:
            print(
                'Error has occured. Generated file does not adhere to METS schema')

        return

    def generate_string(self) -> str:
        tree = self.generate_tree()
        string = etree.tostring(tree, pretty_print=True).decode('UTF-8')
        return string

    @property
    def amd(self) -> list[AdministrativeMetadataSection]:
        return self._amd

    @amd.setter
    def amd(self, amd: Union[AdministrativeMetadataSection, list[
        AdministrativeMetadataSection]]) -> None:
        self._amd = _get_element_list(amd, AdministrativeMetadataSection)
        return

    @property
    def behavior(self) -> list[BehaviorSection]:
        return self._behavior

    @behavior.setter
    def behavior(self, behavior: Union[
        BehaviorSection, list[BehaviorSection]]) -> None:
        self._behavior = _get_element_list(behavior, BehaviorSection)
        return

    @property
    def dmd(self) -> list[DescriptiveMetadataSection]:
        return self._dmd

    @dmd.setter
    def dmd(self, dmd: Union[
        DescriptiveMetadataSection, list[DescriptiveMetadataSection]]) -> None:
        self._dmd = _get_element_list(dmd, DescriptiveMetadataSection)
        return

    @property
    def file_sec(self) -> FileSection:
        return self._file_sec

    @file_sec.setter
    def file_sec(self, file_sec: FileSection) -> None:
        self._file_sec = _add_mets_class(file_sec, FileSection)
        return

    @property
    def header(self) -> Header:
        return self._header

    @header.setter
    def header(self, header: Header) -> None:
        self._header = _add_mets_class(header, Header)
        return

    @property
    def struct_link(self) -> StructuralLink:
        return self._struct_link

    @struct_link.setter
    def struct_link(self, struct_link: StructuralLink) -> None:
        self._struct_link = _add_mets_class(struct_link, StructuralLink)
        return

    @property
    def struct_map(self) -> list[StructuralMap]:
        return self._struct_map

    @struct_map.setter
    def struct_map(self, struct_map: Union[
        StructuralMap, list[StructuralMap]]) -> None:
        self._struct_map = _get_element_list(struct_map, StructuralMap, False)
        return

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, mets_id: str) -> None:
        self._id = _get_string_value(mets_id)
        return

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str) -> None:
        self._label = _get_string_value(label)
        return

    @property
    def objid(self) -> str:
        return self._objid

    @objid.setter
    def objid(self, objid: str) -> None:
        self._objid = _get_string_value(objid)
        return

    @property
    def other_attribs(self) -> dict[str, str]:
        return self._other_attribs

    @other_attribs.setter
    def other_attribs(self, other_attribs: dict[str, str]) -> None:
        if other_attribs is not None:
            self._other_attribs = other_attribs
        else:
            self._other_attribs = {}
        return

    @property
    def profile(self) -> str:
        return self._profile

    @profile.setter
    def profile(self, profile: str) -> None:
        self._profile = _get_string_value(profile)
        return

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, mets_type: str) -> None:
        self._type = _get_string_value(mets_type)
        return
