from __future__ import annotations

import datetime
from typing import Union

from lxml import etree

from .constants import ElementTags, AttributeTags, XlinkAttributes, \
    LocatorTypes, FileBeginEndTypes, \
    TransformTypes, ChecksumTypes, XlinkShowTypes, XlinkActuateTypes
from .exceptions import ParseError, METSLibError
from .generic import METSElement, XMLData, BinData
from .utils import _get_element_list, _add_attribute_to_tree, \
    _add_namespace_attribute_to_tree, _add_enum_value, \
    _get_string_value, _check_tag, _get_datetime_value, _get_integer_value, \
    _add_mets_class


class FileSection(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value
    ]

    def __init__(self, file_groups: Union[FileGroup, list[FileGroup]],
                 element_id: str = None,
                 other_attribs: dict[str, str] = None) -> None:

        self.id = element_id
        self.file_groups = file_groups

        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.FILE_SECTION.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(FileSection.NAMESPACE,
                           ElementTags.FILE_SECTION.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        for item in self.file_groups:
            tree.append(item.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> FileSection:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('File Section Element cant be parsed.')

        file_groups = []
        for child in tree:
            if child.tag == FileGroup.tag() or child.tag == str(
                    FileGroup.qname()):
                file_groups.append(FileGroup.from_tree(child))

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        f_section = FileSection(file_groups=file_groups,
                                element_id=tree.get(AttributeTags.ID.value),
                                other_attribs=other)

        return f_section

    @property
    def file_groups(self) -> list[FileGroup]:
        return self._file_groups

    @file_groups.setter
    def file_groups(self,
                    file_groups: Union[FileGroup, list[FileGroup]]) -> None:
        self._file_groups = _get_element_list(file_groups, FileGroup, False)
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


class FileGroup(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value,
        AttributeTags.VERSDATE.value,
        AttributeTags.ADMID.value,
        AttributeTags.USE.value
    ]

    def __init__(self, content: Union[FileGroup, File, list[FileGroup, File]],
                 element_id: str = None,
                 versdate: Union[datetime.datetime, str] = None,
                 admid: str = None, use: str = None,
                 other_attribs: dict[str, str] = None) -> None:

        self.id = element_id
        self.versdate = versdate
        self.admid = admid
        self.use = use

        self.content = content

        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.FILE_GROUP.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(FileGroup.NAMESPACE, ElementTags.FILE_GROUP.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.VERSDATE, self.versdate)
        _add_attribute_to_tree(tree, AttributeTags.ADMID, self.admid)
        _add_attribute_to_tree(tree, AttributeTags.USE, self.use)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        for item in self.content:
            tree.append(item.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> FileGroup:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('File Group Element cant be parsed.')

        content = []
        for child in tree:
            if child.tag == FileGroup.tag() or child.tag == str(
                    FileGroup.qname()):
                content.append(FileGroup.from_tree(child))
            elif child.tag == File.tag() or child.tag == str(File.qname()):
                content.append(File.from_tree(child))

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        file_group = FileGroup(content=content,
                               element_id=tree.get(AttributeTags.ID.value),
                               versdate=tree.get(AttributeTags.VERSDATE.value),
                               admid=tree.get(AttributeTags.ADMID.value),
                               use=tree.get(AttributeTags.USE.value),
                               other_attribs=other)

        return file_group

    @property
    def admid(self) -> str:
        return self._admid

    @admid.setter
    def admid(self, admid: str) -> None:
        self._admid = _get_string_value(admid)
        return

    @property
    def content(self) -> Union[list[FileGroup], list[File]]:
        return self._content

    @content.setter
    def content(self, content: Union[
        FileGroup, File, list[FileGroup], list[File]]) -> None:
        self._content = _get_element_list(content, (FileGroup, File), False)
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

    @property
    def use(self) -> str:
        return self._use

    @use.setter
    def use(self, use: str) -> None:
        self._use = _get_string_value(use)
        return

    @property
    def versdate(self) -> str:
        return self._versdate

    @versdate.setter
    def versdate(self, versdate: Union[str, datetime.datetime]) -> None:
        self._versdate = _get_datetime_value(versdate)
        return


class File(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value,
        AttributeTags.SEQUENCE.value,
        AttributeTags.MIMETYPE.value,
        AttributeTags.SIZE.value,
        AttributeTags.CREATED.value,
        AttributeTags.CHECKSUM.value,
        AttributeTags.CHECKSUM_TYPE.value,
        AttributeTags.OWNER_ID.value,
        AttributeTags.ADMID.value,
        AttributeTags.DMDID.value,
        AttributeTags.GROUP_ID.value,
        AttributeTags.USE.value,
        AttributeTags.BEGIN.value,
        AttributeTags.END.value,
        AttributeTags.BETYPE.value
    ]

    def __init__(self, element_id: str,
                 content: Union[
                     FileLocation, FileContent, Stream, TransformFile, File,
                     list[
                         FileLocation, FileContent, Stream, TransformFile, File]] = None,
                 sequence: int = None, mimetype: str = None, size: int = None,
                 created: Union[datetime.datetime, str] = None,
                 checksum: str = None, checksum_type: str = None,
                 owner_id: str = None, admid: str = None, dmdid: str = None,
                 group_id: str = None, use: str = None,
                 begin: str = None, end: str = None, betype: str = None,
                 other_attribs: dict[str, str] = None) -> None:

        self.id = element_id
        self.sequence = sequence
        self.mimetype = mimetype
        self.size = size
        self.created = created
        self.checksum = checksum
        self.checksum_type = checksum_type
        self.owner_id = owner_id
        self.admid = admid
        self.dmdid = dmdid
        self.group_id = group_id
        self.use = use
        self.begin = begin
        self.end = end
        self.betype = betype

        self.file_content = None
        self.file_locations = None
        self.files = None
        self.streams = None
        self.transforms = None
        self.content = content

        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.FILE.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(File.NAMESPACE, ElementTags.FILE.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(etree.QName(self.NAMESPACE, self.tag()))

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.SEQUENCE, self.sequence)
        _add_attribute_to_tree(tree, AttributeTags.MIMETYPE, self.mimetype)
        _add_attribute_to_tree(tree, AttributeTags.SIZE, self.size)
        _add_attribute_to_tree(tree, AttributeTags.CREATED, self.created)
        _add_attribute_to_tree(tree, AttributeTags.CHECKSUM, self.checksum)
        _add_attribute_to_tree(tree, AttributeTags.CHECKSUM_TYPE,
                               self.checksum_type)
        _add_attribute_to_tree(tree, AttributeTags.OWNER_ID, self.owner_id)
        _add_attribute_to_tree(tree, AttributeTags.ADMID, self.admid)
        _add_attribute_to_tree(tree, AttributeTags.DMDID, self.dmdid)
        _add_attribute_to_tree(tree, AttributeTags.GROUP_ID, self.group_id)
        _add_attribute_to_tree(tree, AttributeTags.USE, self.use)
        _add_attribute_to_tree(tree, AttributeTags.BEGIN, self.begin)
        _add_attribute_to_tree(tree, AttributeTags.END, self.end)
        _add_attribute_to_tree(tree, AttributeTags.BETYPE, self.betype)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        for item in self.file_locations:
            tree.append(item.generate_tree())
        if self.file_content is not None:
            tree.append(self.file_content.generate_tree())
        for item in self.streams:
            tree.append(item.generate_tree())
        for item in self.transforms:
            tree.append(item.generate_tree())
        for item in self.files:
            tree.append(item.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> File:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('File Element cant be parsed.')

        content = []

        for child in tree:
            if child.tag == FileLocation.tag() or child.tag == str(
                    FileLocation.qname()):
                content.append(FileLocation.from_tree(child))
            elif child.tag == FileContent.tag() or child.tag == str(
                    FileContent.qname()):
                content.append(FileContent.from_tree(child))
            elif child.tag == Stream.tag() or child.tag == str(Stream.qname()):
                content.append(Stream.from_tree(child))
            elif child.tag == TransformFile.tag() or child.tag == str(
                    TransformFile.qname()):
                content.append(TransformFile.from_tree(child))
            elif child.tag == File.tag() or child.tag == str(File.qname()):
                content.append(File.from_tree(child))

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        file = File(element_id=tree.get(AttributeTags.ID.value),
                    sequence=tree.get(AttributeTags.SEQUENCE.value),
                    content=content,
                    mimetype=tree.get(AttributeTags.MIMETYPE.value),
                    size=tree.get(AttributeTags.SIZE.value),
                    created=tree.get(AttributeTags.CREATED.value),
                    checksum=tree.get(AttributeTags.CHECKSUM.value),
                    checksum_type=tree.get(AttributeTags.CHECKSUM_TYPE.value),
                    owner_id=tree.get(AttributeTags.OWNER_ID.value),
                    admid=tree.get(AttributeTags.ADMID.value),
                    dmdid=tree.get(AttributeTags.DMDID.value),
                    group_id=tree.get(AttributeTags.GROUP_ID.value),
                    use=tree.get(AttributeTags.USE.value),
                    begin=tree.get(AttributeTags.BEGIN.value),
                    end=tree.get(AttributeTags.END.value),
                    betype=tree.get(AttributeTags.BETYPE.value),
                    other_attribs=other)
        return file

    @property
    def admid(self) -> str:
        return self._admid

    @admid.setter
    def admid(self, admid: str) -> None:
        self._admid = _get_string_value(admid)
        return

    @property
    def begin(self) -> str:
        return self._begin

    @begin.setter
    def begin(self, begin: str) -> None:
        self._begin = _get_string_value(begin)
        return

    @property
    def betype(self) -> str:
        return self._betype

    @betype.setter
    def betype(self, betype: str) -> None:
        self._betype = _add_enum_value(betype, FileBeginEndTypes)
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
    def dmdid(self) -> str:
        return self._dmdid

    @dmdid.setter
    def dmdid(self, dmdid: str) -> None:
        self._dmdid = _get_string_value(dmdid)
        return

    @property
    def end(self) -> str:
        return self._end

    @end.setter
    def end(self, end: str) -> None:
        self._end = _get_string_value(end)
        return

    @property
    def content(self) -> tuple[
        FileContent, FileLocation, File, Stream, TransformFile]:
        result = self.file_locations + self.files + self.streams + self.transforms
        if self.file_content:
            result += self.file_content
        return result

    @content.setter
    def content(self, content: Union[
        FileLocation, FileContent, Stream, TransformFile, File,
        list[FileLocation, FileContent, Stream, TransformFile, File]]) -> None:
        result = _get_element_list(content, (
            FileLocation, FileContent, Stream, TransformFile, File))
        fcontent = [item for item in result if item.tag() == FileContent.tag()]
        if len(fcontent) > 1:
            raise METSLibError(
                'Only one File Content element can be present in a File')
        else:
            if fcontent:
                self._file_content = \
                    [item for item in result if
                     item.tag() == FileContent.tag()][0]
            self._file_locations = [item for item in result if
                                    item.tag() == FileLocation.tag()]
            self._files = [item for item in result if item.tag() == File.tag()]
            self._streams = [item for item in result if
                             item.tag() == Stream.tag()]
            self._transforms = [item for item in result if
                                item.tag() == TransformFile.tag()]
        return

    @property
    def file_content(self) -> FileContent:
        return self._file_content

    @file_content.setter
    def file_content(self, file_content: FileContent) -> None:
        self._file_content = _add_mets_class(file_content, FileContent)
        return

    @property
    def file_locations(self) -> tuple[FileLocation]:
        return tuple(self._file_locations)

    @file_locations.setter
    def file_locations(self, file_locations: Union[
        FileLocation, list[FileLocation]]) -> None:
        self._file_locations = _get_element_list(file_locations, FileLocation)
        return

    @property
    def files(self) -> tuple[File]:
        return tuple(self._files)

    @files.setter
    def files(self, files: Union[File, list[File]]) -> None:
        self._files = _get_element_list(files, File)
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
        self._id = _get_string_value(element_id)
        return

    @property
    def mimetype(self) -> str:
        return self._mimetype

    @mimetype.setter
    def mimetype(self, mimetype: str) -> None:
        self._mimetype = _get_string_value(mimetype)
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
    def owner_id(self) -> str:
        return self._owner_id

    @owner_id.setter
    def owner_id(self, owner_id: str) -> None:
        self._owner_id = _get_string_value(owner_id)
        return

    @property
    def sequence(self) -> int:
        return self._sequence

    @sequence.setter
    def sequence(self, sequence: int) -> None:
        self._sequence = _get_integer_value(sequence)
        return

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, size: int) -> None:
        self._size = _get_integer_value(size)
        return

    @property
    def streams(self) -> tuple[Stream]:
        return tuple(self._streams)

    @streams.setter
    def streams(self, streams: Union[Stream, list[Stream]]) -> None:
        self._streams = _get_element_list(streams, Stream)
        return

    @property
    def transforms(self) -> tuple[TransformFile]:
        return tuple(self._transforms)

    @transforms.setter
    def transforms(self, transforms: Union[
        TransformFile, list[TransformFile]]) -> None:
        self._transforms = _get_element_list(transforms, TransformFile)
        return

    @property
    def use(self) -> str:
        return self._use

    @use.setter
    def use(self, use: str) -> None:
        self._use = _get_string_value(use)
        return


class FileLocation(METSElement):
    def __init__(self, loctype: str, xlink_href: str, element_id: str = None,
                 use: str = None,
                 other_loctype: str = None, xlink_role: str = None,
                 xlink_arcrole: str = None, xlink_title: str = None,
                 xlink_show: str = None, xlink_actuate: str = None) -> None:
        self.loctype = loctype
        self.xlink_href = xlink_href

        self.id = element_id
        self.use = use
        self.other_loctype = other_loctype
        self.xlink_role = xlink_role
        self.xlink_arcrole = xlink_arcrole
        self.xlink_title = xlink_title

        self.xlink_show = xlink_show
        self.xlink_actuate = xlink_actuate

    @staticmethod
    def tag() -> str:
        return ElementTags.FILE_LOCATION.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(FileLocation.NAMESPACE,
                           ElementTags.FILE_LOCATION.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.USE, self.use)
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

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> FileLocation:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('File Location Element cant be parsed.')

        file_loc = FileLocation(loctype=tree.get(AttributeTags.LOCTYPE.value),
                                xlink_href=tree.get(
                                    str(XlinkAttributes.HREF.value)),
                                element_id=tree.get(AttributeTags.ID.value),
                                use=tree.get(AttributeTags.USE.value),
                                other_loctype=tree.get(
                                    AttributeTags.LOCTYPE_OTHER.value),
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

        return file_loc

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
        return

    @property
    def loctype(self) -> str:
        return self._loctype

    @loctype.setter
    def loctype(self, loctype: str) -> None:
        self._loctype = _add_enum_value(loctype, LocatorTypes, False)
        return

    @property
    def other_loctype(self) -> str:
        return self._other_loctype

    @other_loctype.setter
    def other_loctype(self, other_loctype: str) -> None:
        self._other_loctype = _get_string_value(other_loctype)
        return

    @property
    def use(self) -> str:
        return self._use

    @use.setter
    def use(self, use: str) -> None:
        self._use = _get_string_value(use)
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
        self._xlink_href = _get_string_value(xlink_href)
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


class FileContent(METSElement):

    def __init__(self, content: Union[XMLData, BinData], element_id: str = None,
                 use: str = None) -> None:
        self.id = element_id
        self.use = use
        self.content = content

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.FILE_CONTENT.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(FileContent.NAMESPACE,
                           ElementTags.FILE_CONTENT.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        tree.append(self.content.generate_tree())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.USE, self.use)

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> FileContent:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('File Content Element cant be parsed.')

        content = None
        for child in tree:
            if child.tag == XMLData.tag() or child.tag == str(XMLData.qname()):
                content = XMLData.from_tree(child)
            elif child.tag == BinData.tag() or child.tag == str(
                    BinData.qname()):
                content = BinData.from_tree(child)

        file_content = FileContent(content=content,
                                   element_id=tree.get(AttributeTags.ID.value),
                                   use=tree.get(AttributeTags.USE.value))

        return file_content

    @property
    def content(self) -> Union[XMLData, BinData]:
        return self._content

    @content.setter
    def content(self, content: Union[XMLData, BinData]) -> None:
        self._content = _add_mets_class(content, (XMLData, BinData), False)
        return

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
        return

    @property
    def use(self) -> str:
        return self._use

    @use.setter
    def use(self, use: str) -> None:
        self._use = _get_string_value(use)
        return


class Stream(METSElement):

    def __init__(self, element_id: str = None, stream_type: str = None,
                 owner_id: str = None, admid: str = None,
                 dmdid: str = None, begin: str = None, end: str = None,
                 betype: str = None) -> None:
        self.id = element_id
        self.stream_type = stream_type
        self.owner_id = owner_id
        self.admid = admid
        self.dmdid = dmdid
        self.begin = begin
        self.end = end
        self.betype = betype

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.COMPONENT_BYTE_STREAM.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(Stream.NAMESPACE,
                           ElementTags.COMPONENT_BYTE_STREAM.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.STREAM_TYPE,
                               self.stream_type)
        _add_attribute_to_tree(tree, AttributeTags.OWNER_ID, self.owner_id)
        _add_attribute_to_tree(tree, AttributeTags.ADMID, self.admid)
        _add_attribute_to_tree(tree, AttributeTags.DMDID, self.dmdid)
        _add_attribute_to_tree(tree, AttributeTags.BEGIN, self.begin)
        _add_attribute_to_tree(tree, AttributeTags.END, self.end)
        _add_attribute_to_tree(tree, AttributeTags.BETYPE, self.betype)

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> Stream:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Stream Element cant be parsed.')

        stream = Stream(element_id=tree.get(AttributeTags.ID.value),
                        stream_type=tree.get(AttributeTags.STREAM_TYPE.value),
                        owner_id=tree.get(AttributeTags.OWNER_ID.value),
                        admid=tree.get(AttributeTags.ADMID.value),
                        dmdid=tree.get(AttributeTags.DMDID.value),
                        begin=tree.get(AttributeTags.BEGIN.value),
                        end=tree.get(AttributeTags.END.value),
                        betype=tree.get(AttributeTags.BETYPE.value))

        return stream

    @property
    def admid(self) -> str:
        return self._admid

    @admid.setter
    def admid(self, admid: str) -> None:
        self._admid = _get_string_value(admid)
        return

    @property
    def begin(self) -> str:
        return self._begin

    @begin.setter
    def begin(self, begin: str) -> None:
        self._begin = _get_string_value(begin)
        return

    @property
    def betype(self) -> str:
        return self._betype

    @betype.setter
    def betype(self, betype: str) -> None:
        self._betype = _add_enum_value(betype, FileBeginEndTypes)
        return

    @property
    def dmdid(self) -> str:
        return self._dmdid

    @dmdid.setter
    def dmdid(self, dmdid: str) -> None:
        self._dmdid = _get_string_value(dmdid)
        return

    @property
    def end(self) -> str:
        return self._end

    @end.setter
    def end(self, end: str) -> None:
        self._end = _get_string_value(end)
        return

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
        return

    @property
    def owner_id(self) -> str:
        return self._owner_id

    @owner_id.setter
    def owner_id(self, owner_id: str) -> None:
        self._owner_id = _get_string_value(owner_id)
        return

    @property
    def stream_type(self) -> str:
        return self._stream_type

    @stream_type.setter
    def stream_type(self, stream_type: str) -> None:
        self._stream_type = _get_string_value(stream_type)
        return


class TransformFile(METSElement):

    def __init__(self, transform_type: str, algorithm: str, order: int,
                 element_id: str = None, key: str = None,
                 behavior: str = None) -> None:

        self.transform_type = transform_type
        self.algorithm = algorithm
        self.order = order

        self.id = element_id
        self.key = key
        self.behavior = behavior

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.TRANSFORM_FILE.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(TransformFile.NAMESPACE,
                           ElementTags.TRANSFORM_FILE.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.TRANSFORM_TYPE,
                               self.transform_type)
        _add_attribute_to_tree(tree, AttributeTags.TRANSFORM_ALGORITHM,
                               self.algorithm)
        _add_attribute_to_tree(tree, AttributeTags.TRANSFORM_KEY, self.key)
        _add_attribute_to_tree(tree, AttributeTags.TRANSFORM_BEHAVIOR,
                               self.behavior)
        _add_attribute_to_tree(tree, AttributeTags.TRANSFORM_ORDER, self.order)

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> TransformFile:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Transform File Element cant be parsed.')

        transform = TransformFile(
            transform_type=tree.get(AttributeTags.TRANSFORM_TYPE.value),
            algorithm=tree.get(AttributeTags.TRANSFORM_ALGORITHM.value),
            order=tree.get(AttributeTags.TRANSFORM_ORDER.value),
            element_id=tree.get(AttributeTags.ID.value),
            key=tree.get(AttributeTags.TRANSFORM_KEY.value),
            behavior=tree.get(AttributeTags.TRANSFORM_BEHAVIOR.value))

        return transform

    @property
    def algorithm(self) -> str:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm: str) -> None:
        self._algorithm = _get_string_value(algorithm, False)
        return

    @property
    def behavior(self) -> str:
        return self._behavior

    @behavior.setter
    def behavior(self, behavior: str) -> None:
        self._behavior = _get_string_value(behavior)
        return

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
        return

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, key: str) -> None:
        self._key = _get_string_value(key)
        return

    @property
    def order(self) -> int:
        return self._order

    @order.setter
    def order(self, order: int) -> None:
        self._order = _get_integer_value(order, False)
        if self._order < 1:
            raise ValueError('Transform Order value must be positive.')
        return

    @property
    def transform_type(self) -> str:
        return self._transform_type

    @transform_type.setter
    def transform_type(self, transform_type: str) -> None:
        self._transform_type = _add_enum_value(transform_type, TransformTypes,
                                               False)
        return
