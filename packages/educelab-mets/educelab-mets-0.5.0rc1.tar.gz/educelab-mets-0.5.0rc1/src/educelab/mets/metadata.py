from __future__ import annotations

import datetime
from abc import abstractmethod
from typing import Union

from .constants import *
from .exceptions import ParseError
from .generic import METSElement, XMLData, BinData
from .utils import _add_attribute_to_tree, _add_namespace_attribute_to_tree, \
    _add_mets_class, _get_string_value, \
    _get_datetime_value, _check_tag, _add_enum_value, _get_integer_value, \
    _get_element_list


class GenericMetadataElement(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value,
        AttributeTags.GROUP_ID.value,
        AttributeTags.ADMID.value,
        AttributeTags.CREATED.value,
        AttributeTags.STATUS.value
    ]

    def __init__(self, element_id: str, group_id: str = None, admid: str = None,
                 created: Union[datetime.datetime, str] = None,
                 status: str = None, mdref: MetadataReference = None,
                 mdwrap: MetadataWrapper = None,
                 other_attribs: dict[str, str] = None) -> None:
        self.id = element_id
        self.group_id = group_id
        self.admid = admid
        self.created = created
        self.status = status

        self.mdref = mdref
        self.mdwrap = mdwrap

        self.other_attribs = other_attribs

        return

    @staticmethod
    @abstractmethod
    def tag():
        pass

    @staticmethod
    @abstractmethod
    def qname():
        pass

    def generate_tree(self) -> etree:
        tree = etree.Element(etree.QName(self.NAMESPACE, self.tag()))

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.GROUP_ID, self.group_id)
        _add_attribute_to_tree(tree, AttributeTags.ADMID, self.admid)
        _add_attribute_to_tree(tree, AttributeTags.CREATED, self.created)
        _add_attribute_to_tree(tree, AttributeTags.STATUS, self.status)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        if self.mdref is not None:
            tree.append(self.mdref.generate_tree())

        if self.mdwrap is not None:
            tree.append(self.mdwrap.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree):
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Element cant be parsed.')

        mdref = mdwrap = None
        for child in tree:
            if child.tag == MetadataReference.tag() or child.tag == str(
                    MetadataReference.qname()):
                mdref = MetadataReference.from_tree(child)
            elif child.tag == MetadataWrapper.tag() or child.tag == str(
                    MetadataWrapper.qname()):
                mdwrap = MetadataWrapper.from_tree(child)

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        element = cls(element_id=tree.get(AttributeTags.ID.value),
                      group_id=tree.get(AttributeTags.GROUP_ID.value),
                      admid=tree.get(AttributeTags.ADMID.value),
                      created=tree.get(AttributeTags.CREATED.value),
                      status=tree.get(AttributeTags.STATUS.value), mdref=mdref,
                      mdwrap=mdwrap, other_attribs=other)

        return element

    @property
    def admid(self) -> str:
        return self._admid

    @admid.setter
    def admid(self, admid: str) -> None:
        self._admid = _get_string_value(admid)
        return

    @property
    def created(self) -> str:
        return self._created

    @created.setter
    def created(self, created: Union[str, datetime.datetime]) -> None:
        self._created = _get_datetime_value(created)
        return

    @property
    def group_id(self) -> str:
        return self._group_id

    @group_id.setter
    def group_id(self, group_id: str) -> None:
        self._group_id = _get_string_value(group_id)
        return

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id, False)
        return

    @property
    def mdref(self) -> MetadataReference:
        return self._mdref

    @mdref.setter
    def mdref(self, mdref: MetadataReference) -> None:
        self._mdref = _add_mets_class(mdref, MetadataReference)
        return

    @property
    def mdwrap(self) -> MetadataWrapper:
        return self._mdwrap

    @mdwrap.setter
    def mdwrap(self, mdwrap: MetadataWrapper) -> None:
        self._mdwrap = _add_mets_class(mdwrap, MetadataWrapper)
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
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        self._status = _get_string_value(status)
        return


class DescriptiveMetadataSection(GenericMetadataElement):

    @staticmethod
    def tag() -> str:
        return ElementTags.DESCRIPTIVE_METADATA.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(DescriptiveMetadataSection.NAMESPACE,
                           ElementTags.DESCRIPTIVE_METADATA.value)


class AdministrativeMetadataSection(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value
    ]

    def __init__(self, element_id: str = None,
                 content: Union[
                     TechnicalMetadata, PropertyRightsMetadata, SourceMetadata, DigitalProvenanceMetadata,
                     list[
                         TechnicalMetadata, PropertyRightsMetadata, SourceMetadata,
                         DigitalProvenanceMetadata]] = None,
                 other_attribs: dict[str, str] = None) -> None:

        self.id = element_id
        self.content = content

        self.tech_md = None
        self.digiprov_md = None
        self.source_md = None
        self.rights_md = None

        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.ADMINISTRATIVE_METADATA.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(AdministrativeMetadataSection.NAMESPACE,
                           ElementTags.ADMINISTRATIVE_METADATA.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        if self.tech_md:
            for item in self.tech_md:
                tree.append(item.generate_tree())

        if self.rights_md:
            for item in self.rights_md:
                tree.append(item.generate_tree())

        if self.source_md:
            for item in self.source_md:
                tree.append(item.generate_tree())

        if self.digiprov_md:
            for item in self.digiprov_md:
                tree.append(item.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> AdministrativeMetadataSection:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError(
                'Administrative Metadata Section Element cant be parsed.')

        content = []

        for child in tree:
            if child.tag == TechnicalMetadata.tag() or child.tag == str(
                    TechnicalMetadata.qname()):
                content.append(TechnicalMetadata.from_tree(child))
            elif child.tag == PropertyRightsMetadata.tag() or child.tag == str(
                    PropertyRightsMetadata.qname()):
                content.append(PropertyRightsMetadata.from_tree(child))
            elif child.tag == SourceMetadata.tag() or child.tag == str(
                    SourceMetadata.qname()):
                content.append(SourceMetadata.from_tree(child))
            elif child.tag == DigitalProvenanceMetadata.tag() or child.tag == str(
                    DigitalProvenanceMetadata.qname()):
                content.append(DigitalProvenanceMetadata.from_tree(child))

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        amd = AdministrativeMetadataSection(
            element_id=tree.get(AttributeTags.ID.value), content=content,
            other_attribs=other)

        return amd

    @property
    def content(self) -> list[
        TechnicalMetadata, PropertyRightsMetadata, SourceMetadata, DigitalProvenanceMetadata]:
        return self.tech_md + self.digiprov_md + self.source_md + self.rights_md

    @content.setter
    def content(self, content: Union[
        TechnicalMetadata, PropertyRightsMetadata, SourceMetadata,
        DigitalProvenanceMetadata, list[TechnicalMetadata,
        PropertyRightsMetadata,
        SourceMetadata,
        DigitalProvenanceMetadata]]) -> None:
        result = _get_element_list(content, (
            TechnicalMetadata, PropertyRightsMetadata, SourceMetadata,
            DigitalProvenanceMetadata))
        self.tech_md = [item for item in result if
                        item.tag() == TechnicalMetadata.tag()]
        self.digiprov_md = [item for item in result if
                            item.tag() == DigitalProvenanceMetadata.tag()]
        self.source_md = [item for item in result if
                          item.tag() == SourceMetadata.tag()]
        self.rights_md = [item for item in result if
                          item.tag() == PropertyRightsMetadata.tag()]

        return

    @property
    def tech_md(self) -> list[TechnicalMetadata]:
        return self._tech_md

    @tech_md.setter
    def tech_md(self, tech_md: Union[
        TechnicalMetadata, list[TechnicalMetadata]]) -> None:
        self._tech_md = _get_element_list(tech_md, TechnicalMetadata)
        return

    @property
    def digiprov_md(self) -> list[DigitalProvenanceMetadata]:
        return self._digiprov_md

    @digiprov_md.setter
    def digiprov_md(self, digiprov_md: Union[
        DigitalProvenanceMetadata, list[DigitalProvenanceMetadata]]) -> None:
        self._digiprov_md = _get_element_list(digiprov_md,
                                              DigitalProvenanceMetadata)
        return

    @property
    def rights_md(self) -> list[PropertyRightsMetadata]:
        return self._rights_md

    @rights_md.setter
    def rights_md(self, rights_md: Union[
        PropertyRightsMetadata, list[PropertyRightsMetadata]]) -> None:
        self._rights_md = _get_element_list(rights_md, PropertyRightsMetadata)
        return

    @property
    def source_md(self) -> list[SourceMetadata]:
        return self._source_md

    @source_md.setter
    def source_md(self, source_md: Union[
        SourceMetadata, list[SourceMetadata]]) -> None:
        self._source_md = _get_element_list(source_md, SourceMetadata)
        return

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
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


class MetadataWrapper(METSElement):

    def __init__(self, mdtype: str, wrapped_data: Union[XMLData, BinData],
                 element_id: str = None, mimetype: str = None,
                 label: str = None, mdtype_version: str = None,
                 other_mdtype: str = None, size: int = None,
                 created: Union[datetime.datetime, str] = None,
                 checksum: str = None,
                 checksum_type: str = None) -> None:

        self.mdtype = mdtype
        self.wrapped_data = wrapped_data

        self.id = element_id
        self.mimetype = mimetype
        self.label = label
        self.mdtype_version = mdtype_version
        self.other_mdtype = other_mdtype
        self.size = size
        self.created = created
        self.checksum = checksum
        self.checksum_type = checksum_type

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.METADATA_WRAPPER.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(MetadataWrapper.NAMESPACE,
                           ElementTags.METADATA_WRAPPER.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        tree.append(self.wrapped_data.generate_tree())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.MDTYPE, self.mdtype)
        _add_attribute_to_tree(tree, AttributeTags.MDTYPE_OTHER,
                               self.other_mdtype)
        _add_attribute_to_tree(tree, AttributeTags.MDTYPE_VERSION,
                               self.mdtype_version)
        _add_attribute_to_tree(tree, AttributeTags.MIMETYPE, self.mimetype)
        _add_attribute_to_tree(tree, AttributeTags.SIZE, self.size)
        _add_attribute_to_tree(tree, AttributeTags.CREATED, self.created)
        _add_attribute_to_tree(tree, AttributeTags.CHECKSUM, self.checksum)
        _add_attribute_to_tree(tree, AttributeTags.CHECKSUM_TYPE,
                               self.checksum_type)
        _add_attribute_to_tree(tree, AttributeTags.LABEL, self.label)

        return tree

    @classmethod
    def from_tree(cls, tree) -> MetadataWrapper:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError(
                'Administrative Metadata Section Element cant be parsed.')

        wrapped_data = None
        for child in tree:
            if child.tag == XMLData.tag() or child.tag == str(XMLData.qname()):
                wrapped_data = XMLData.from_tree(child)
            elif child.tag == BinData.tag() or child.tag == str(
                    BinData.qname()):
                wrapped_data = BinData.from_tree(child)

        wrapper = MetadataWrapper(mdtype=tree.get(AttributeTags.MDTYPE.value),
                                  wrapped_data=wrapped_data,
                                  element_id=tree.get(AttributeTags.ID.value),
                                  mimetype=tree.get(
                                      AttributeTags.MIMETYPE.value),
                                  label=tree.get(AttributeTags.LABEL.value),
                                  mdtype_version=tree.get(
                                      AttributeTags.MDTYPE_VERSION.value),
                                  other_mdtype=tree.get(
                                      AttributeTags.MDTYPE_OTHER.value),
                                  size=tree.get(AttributeTags.SIZE.value),
                                  created=tree.get(AttributeTags.CREATED.value),
                                  checksum=tree.get(
                                      AttributeTags.CHECKSUM.value),
                                  checksum_type=tree.get(
                                      AttributeTags.CHECKSUM_TYPE.value))
        return wrapper

    @property
    def mdtype(self) -> str:
        return self._mdtype

    @mdtype.setter
    def mdtype(self, mdtype: str) -> None:
        self._mdtype = _add_enum_value(mdtype, MetadataTypes, False)
        return

    @property
    def mdtype_version(self) -> str:
        return self._mdtype_version

    @mdtype_version.setter
    def mdtype_version(self, mdtype_version: str) -> None:
        self._mdtype_version = _get_string_value(mdtype_version)
        return

    @property
    def checksum(self) -> str:
        return self._checksum

    @checksum.setter
    def checksum(self, checksum: str) -> None:
        self._checksum = _get_string_value(checksum)
        return

    @property
    def checksum_type(self) -> str:
        return self._checksum_type

    @checksum_type.setter
    def checksum_type(self, checksum_type: str) -> None:
        self._checksum_type = _add_enum_value(checksum_type, ChecksumTypes)
        return

    @property
    def created(self) -> str:
        return self._created

    @created.setter
    def created(self, created: Union[str, datetime.datetime]) -> None:
        self._created = _get_datetime_value(created)
        return

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
        return

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str) -> None:
        self._label = _get_string_value(label)
        return

    @property
    def mimetype(self) -> str:
        return self._mimetype

    @mimetype.setter
    def mimetype(self, mimetype: str) -> None:
        self._mimetype = _get_string_value(mimetype)
        return

    @property
    def other_mdtype(self) -> str:
        return self._other_mdtype

    @other_mdtype.setter
    def other_mdtype(self, other_mdtype: str) -> None:
        self._other_mdtype = _get_string_value(other_mdtype)
        return

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, size: int) -> None:
        self._size = _get_integer_value(size)
        return

    @property
    def wrapped_data(self) -> Union[XMLData, BinData]:
        return self._wrapped_data

    @wrapped_data.setter
    def wrapped_data(self, wrapped_data: Union[XMLData, BinData]) -> None:
        self._wrapped_data = _add_mets_class(wrapped_data, (XMLData, BinData),
                                             False)
        return


class MetadataReference(METSElement):

    def __init__(self, loctype: str, mdtype: str, xlink_href: str,
                 element_id: str = None, mimetype: str = None,
                 label: str = None, xptr: str = None, other_loctype: str = None,
                 mdtype_version: str = None,
                 other_mdtype: str = None, size: int = None,
                 created: Union[datetime.datetime, str] = None,
                 checksum: str = None, checksum_type: str = None,
                 xlink_role: str = None, xlink_arcrole: str = None,
                 xlink_title: str = None, xlink_show: str = None,
                 xlink_actuate: str = None) -> None:
        self.loctype = loctype
        self.mdtype = mdtype

        self.xlink_href = xlink_href

        self.id = element_id
        self.mimetype = mimetype
        self.label = label
        self.xptr = xptr
        self.other_loctype = other_loctype
        self.mdtype_version = mdtype_version
        self.other_mdtype = other_mdtype
        self.size = size
        self.created = created
        self.checksum = checksum
        self.checksum_type = checksum_type

        self.xlink_role = xlink_role
        self.xlink_arcrole = xlink_arcrole
        self.xlink_title = xlink_title
        self.xlink_show = xlink_show
        self.xlink_actuate = xlink_actuate

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.METADATA_REFERENCE.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(MetadataReference.NAMESPACE,
                           ElementTags.METADATA_REFERENCE.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.LOCTYPE, self.loctype)
        _add_attribute_to_tree(tree, AttributeTags.LOCTYPE_OTHER,
                               self.other_loctype)

        _add_namespace_attribute_to_tree(tree, XlinkAttributes.HREF.value,
                                         self.xlink_href)
        _add_namespace_attribute_to_tree(tree, XlinkAttributes.ROLE.value,
                                         self.xlink_role)
        _add_namespace_attribute_to_tree(tree, XlinkAttributes.ARCROLE.value,
                                         self.xlink_arcrole)
        _add_namespace_attribute_to_tree(tree, XlinkAttributes.TITLE.value,
                                         self.xlink_title)
        _add_namespace_attribute_to_tree(tree, XlinkAttributes.SHOW.value,
                                         self.xlink_show)
        _add_namespace_attribute_to_tree(tree, XlinkAttributes.ACTUATE.value,
                                         self.xlink_actuate)

        _add_attribute_to_tree(tree, AttributeTags.MDTYPE, self.mdtype)
        _add_attribute_to_tree(tree, AttributeTags.MDTYPE_OTHER,
                               self.other_mdtype)
        _add_attribute_to_tree(tree, AttributeTags.MDTYPE_VERSION,
                               self.mdtype_version)
        _add_attribute_to_tree(tree, AttributeTags.MIMETYPE, self.mimetype)
        _add_attribute_to_tree(tree, AttributeTags.SIZE, self.size)
        _add_attribute_to_tree(tree, AttributeTags.CREATED, self.created)
        _add_attribute_to_tree(tree, AttributeTags.CHECKSUM, self.checksum)
        _add_attribute_to_tree(tree, AttributeTags.CHECKSUM_TYPE,
                               self.checksum_type)
        _add_attribute_to_tree(tree, AttributeTags.LABEL, self.label)
        _add_attribute_to_tree(tree, AttributeTags.XPTR, self.xptr)

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> MetadataReference:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Metadata Reference Element cant be parsed.')

        mdref = MetadataReference(loctype=tree.get(AttributeTags.LOCTYPE.value),
                                  mdtype=tree.get(AttributeTags.MDTYPE.value),
                                  xlink_href=tree.get(
                                      str(XlinkAttributes.HREF.value)),
                                  element_id=tree.get(AttributeTags.ID.value),
                                  mimetype=tree.get(
                                      AttributeTags.MIMETYPE.value),
                                  label=tree.get(AttributeTags.LABEL.value),
                                  xptr=tree.get(AttributeTags.XPTR.value),
                                  other_loctype=tree.get(
                                      AttributeTags.LOCTYPE_OTHER.value),
                                  mdtype_version=tree.get(
                                      AttributeTags.MDTYPE_VERSION.value),
                                  other_mdtype=tree.get(
                                      AttributeTags.MDTYPE_OTHER.value),
                                  size=tree.get(AttributeTags.SIZE.value),
                                  created=tree.get(AttributeTags.CREATED.value),
                                  checksum=tree.get(
                                      AttributeTags.CHECKSUM.value),
                                  checksum_type=tree.get(
                                      AttributeTags.CHECKSUM_TYPE.value),
                                  xlink_role=tree.get(
                                      str(XlinkAttributes.ROLE.value)),
                                  xlink_arcrole=tree.get(
                                      str(XlinkAttributes.ARCROLE.value)),
                                  xlink_title=tree.get(
                                      str(XlinkAttributes.TITLE.value)),
                                  xlink_show=tree.get(
                                      str(XlinkAttributes.SHOW.value)),
                                  xlink_actuate=tree.get(
                                      str(XlinkAttributes.ACTUATE.value)))

        return mdref

    @property
    def checksum(self) -> str:
        return self._checksum

    @checksum.setter
    def checksum(self, checksum: str) -> None:
        self._checksum = _get_string_value(checksum)
        return

    @property
    def checksum_type(self) -> str:
        return self._checksum_type

    @checksum_type.setter
    def checksum_type(self, checksum_type: str) -> None:
        self._checksum_type = _add_enum_value(checksum_type, ChecksumTypes)
        return

    @property
    def created(self) -> str:
        return self._created

    @created.setter
    def created(self, created: Union[str, datetime.datetime]) -> None:
        self._created = _get_datetime_value(created)
        return

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
        return

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str) -> None:
        self._label = _get_string_value(label)
        return

    @property
    def loctype(self) -> str:
        return self._loctype

    @loctype.setter
    def loctype(self, loctype: str) -> None:
        self._loctype = _add_enum_value(loctype, LocatorTypes, False)
        return

    @property
    def mdtype(self) -> str:
        return self._mdtype

    @mdtype.setter
    def mdtype(self, mdtype: str) -> None:
        self._mdtype = _add_enum_value(mdtype, MetadataTypes, False)
        return

    @property
    def mdtype_version(self) -> str:
        return self._mdtype_version

    @mdtype_version.setter
    def mdtype_version(self, mdtype_version: str) -> None:
        self._mdtype_version = _get_string_value(mdtype_version)
        return

    @property
    def mimetype(self) -> str:
        return self._mimetype

    @mimetype.setter
    def mimetype(self, mimetype: str) -> None:
        self._mimetype = _get_string_value(mimetype)
        return

    @property
    def other_loctype(self) -> str:
        return self._other_loctype

    @other_loctype.setter
    def other_loctype(self, other_loctype: str) -> None:
        self._other_loctype = _get_string_value(other_loctype)
        return

    @property
    def other_mdtype(self) -> str:
        return self._other_mdtype

    @other_mdtype.setter
    def other_mdtype(self, other_mdtype: str) -> None:
        self._other_mdtype = _get_string_value(other_mdtype)
        return

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, size: int) -> None:
        self._size = _get_integer_value(size)
        return

    @property
    def xlink_actuate(self) -> str:
        return self._xlink_actuate

    @xlink_actuate.setter
    def xlink_actuate(self, xlink_actuate: str) -> None:
        self._xlink_actuate = _add_enum_value(xlink_actuate, XlinkActuateTypes)
        return

    @property
    def xlink_arcrole(self) -> str:
        return self._xlink_arcrole

    @xlink_arcrole.setter
    def xlink_arcrole(self, xlink_arcrole: str) -> None:
        self._xlink_arcrole = _get_string_value(xlink_arcrole)
        return

    @property
    def xlink_href(self) -> str:
        return self._xlink_href

    @xlink_href.setter
    def xlink_href(self, xlink_href: str) -> None:
        self._xlink_href = _get_string_value(xlink_href, False)
        return

    @property
    def xlink_role(self) -> str:
        return self._xlink_role

    @xlink_role.setter
    def xlink_role(self, xlink_role: str) -> None:
        self._xlink_role = _get_string_value(xlink_role)
        return

    @property
    def xlink_show(self) -> str:
        return self._xlink_show

    @xlink_show.setter
    def xlink_show(self, xlink_show: str) -> None:
        self._xlink_show = _add_enum_value(xlink_show, XlinkShowTypes)
        return

    @property
    def xlink_title(self) -> str:
        return self._xlink_title

    @xlink_title.setter
    def xlink_title(self, xlink_title: str) -> None:
        self._xlink_title = _get_string_value(xlink_title)
        return

    @property
    def xptr(self) -> str:
        return self._xptr

    @xptr.setter
    def xptr(self, xptr: str) -> None:
        self._xptr = _get_string_value(xptr)
        return


class TechnicalMetadata(GenericMetadataElement):

    @staticmethod
    def tag() -> str:
        return ElementTags.TECHNICAL_METADATA.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(TechnicalMetadata.NAMESPACE,
                           ElementTags.TECHNICAL_METADATA.value)


class PropertyRightsMetadata(GenericMetadataElement):

    @staticmethod
    def tag() -> str:
        return ElementTags.PROPERTY_RIGHTS_METADATA.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(PropertyRightsMetadata.NAMESPACE,
                           ElementTags.PROPERTY_RIGHTS_METADATA.value)


class SourceMetadata(GenericMetadataElement):

    @staticmethod
    def tag() -> str:
        return ElementTags.SOURCE_METADATA.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(SourceMetadata.NAMESPACE,
                           ElementTags.SOURCE_METADATA.value)


class DigitalProvenanceMetadata(GenericMetadataElement):

    @staticmethod
    def tag() -> str:
        return ElementTags.DIGITAL_PROVENANCE_METADATA.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(DigitalProvenanceMetadata.NAMESPACE,
                           ElementTags.DIGITAL_PROVENANCE_METADATA.value)
