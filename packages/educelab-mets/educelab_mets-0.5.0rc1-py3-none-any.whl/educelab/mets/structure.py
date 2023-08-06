from __future__ import annotations

from typing import Union

from lxml import etree

from .constants import ElementTags, AttributeTags, XlinkAttributes, NAMESPACES, \
    XlinkShowTypes, XlinkActuateTypes, \
    ArclinkOrderTypes, LocatorTypes, AreaBeginEndTypes, ExtentTypes
from .exceptions import METSLibError, ParseError
from .generic import METSElement
from .utils import _get_element_list, _add_attribute_to_tree, \
    _add_namespace_attribute_to_tree, _add_enum_value, \
    _add_mets_class, _get_string_value, _check_tag, _get_integer_value


class StructuralMap(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value,
        AttributeTags.LABEL.value,
        AttributeTags.TYPE.value
    ]

    def __init__(self, div: Division, element_id: str = None, label: str = None,
                 struct_map_type: str = None,
                 other_attribs: dict[str, str] = None) -> None:

        self.div = div

        self.id = element_id
        self.label = label
        self.type = struct_map_type
        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.STRUCTURAL_MAP.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(StructuralMap.NAMESPACE,
                           ElementTags.STRUCTURAL_MAP.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.TYPE, self.type)
        _add_attribute_to_tree(tree, AttributeTags.LABEL, self.label)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        tree.append(self.div.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> StructuralMap:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Structural Map Element cant be parsed.')

        div = None
        for child in tree:
            if child.tag == Division.tag() or child.tag == str(
                    Division.qname()):
                div = Division.from_tree(child)

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        struct_map = StructuralMap(div=div,
                                   element_id=tree.get(AttributeTags.ID.value),
                                   label=tree.get(AttributeTags.LABEL.value),
                                   struct_map_type=tree.get(
                                       AttributeTags.TYPE.value),
                                   other_attribs=other)

        return struct_map

    @property
    def div(self) -> Division:
        return self._div

    @div.setter
    def div(self, div: Division) -> None:
        self._div = _add_mets_class(div, Division, False)
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
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, element_type: str) -> None:
        self._type = _get_string_value(element_type)
        return


class Division(METSElement):

    def __init__(self, content: list[METSPointer, FilePointer, Division] = None,
                 element_id: str = None,
                 order: int = None, order_label: str = None, label: str = None,
                 dmdid: str = None, admid: str = None,
                 div_type: str = None, content_ids: str = None,
                 xlink_label: str = None) -> None:

        self.content = content

        self.id = element_id
        self.order = order
        self.order_label = order_label
        self.label = label
        self.dmdid = dmdid
        self.admid = admid
        self.type = div_type
        self.content_ids = content_ids
        self.xlink_label = xlink_label

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.DIVISION.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(Division.NAMESPACE, ElementTags.DIVISION.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.ORDER, self.order)
        _add_attribute_to_tree(tree, AttributeTags.ORDER_LABEL,
                               self.order_label)
        _add_attribute_to_tree(tree, AttributeTags.LABEL, self.label)
        _add_attribute_to_tree(tree, AttributeTags.DMDID, self.dmdid)
        _add_attribute_to_tree(tree, AttributeTags.ADMID, self.admid)
        _add_attribute_to_tree(tree, AttributeTags.TYPE, self.type)
        _add_attribute_to_tree(tree, AttributeTags.CONTENT_IDS,
                               self.content_ids)

        _add_namespace_attribute_to_tree(tree, XlinkAttributes.LABEL.value,
                                         self.xlink_label)

        if self.content is not None:
            for item in self.content:
                tree.append(item.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> Division:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Division Element cant be parsed.')

        content = []
        for child in tree:
            if child.tag == Division.tag() or child.tag == str(
                    Division.qname()):
                content.append(Division.from_tree(child))
            elif child.tag == FilePointer.tag() or child.tag == str(
                    FilePointer.qname()):
                content.append(FilePointer.from_tree(child))
            elif child.tag == METSPointer.tag() or child.tag == str(
                    METSPointer.qname()):
                content.append(METSPointer.from_tree(child))

        division = Division(content=content,
                            element_id=tree.get(AttributeTags.ID.value),
                            order=tree.get(AttributeTags.ORDER.value),
                            order_label=tree.get(
                                AttributeTags.ORDER_LABEL.value),
                            label=tree.get(AttributeTags.LABEL.value),
                            dmdid=tree.get(AttributeTags.DMDID.value),
                            admid=tree.get(AttributeTags.ADMID.value),
                            div_type=tree.get(AttributeTags.TYPE.value),
                            content_ids=tree.get(
                                AttributeTags.CONTENT_IDS.value),
                            xlink_label=tree.get(
                                str(XlinkAttributes.LABEL.value)))

        return division

    @property
    def admid(self) -> str:
        return self._amdid

    @admid.setter
    def admid(self, amdid: str) -> None:
        self._amdid = _get_string_value(amdid)
        return

    @property
    def content(self) -> list[Division, FilePointer, METSPointer]:
        return self._content

    @content.setter
    def content(self,
                content: list[Division, FilePointer, METSPointer]) -> None:
        self._content = _get_element_list(content,
                                          (Division, FilePointer, METSPointer))
        return

    @property
    def content_ids(self) -> str:
        return self._content_ids

    @content_ids.setter
    def content_ids(self, content_ids: str) -> None:
        self._content_ids = _get_string_value(content_ids)
        return

    @property
    def dmdid(self) -> str:
        return self._dmdid

    @dmdid.setter
    def dmdid(self, dmdid: str) -> None:
        self._dmdid = _get_string_value(dmdid)
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
    def order(self) -> int:
        return self._order

    @order.setter
    def order(self, order: int) -> None:
        self._order = _get_integer_value(order)
        return

    @property
    def order_label(self) -> str:
        return self._order_label

    @order_label.setter
    def order_label(self, order_label: str) -> None:
        self._order_label = _get_string_value(order_label)
        return

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, element_type: str) -> None:
        self._type = _get_string_value(element_type)
        return

    @property
    def xlink_label(self) -> str:
        return self._xlink_label

    @xlink_label.setter
    def xlink_label(self, xlink_label: str) -> None:
        self._xlink_label = _get_string_value(xlink_label)
        return


class FilePointer(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value,
        AttributeTags.FILE_ID.value,
        AttributeTags.CONTENT_IDS.value
    ]

    def __init__(self,
                 content: Union[Area, ParallelFiles, SequenceOfFiles] = None,
                 element_id: str = None,
                 file_id: str = None, content_ids: str = None,
                 other_attribs: dict[str, str] = None) -> None:

        self.content = content

        self.id = element_id
        self.file_id = file_id
        self.content_ids = content_ids
        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.FILE_POINTER.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(FilePointer.NAMESPACE,
                           ElementTags.FILE_POINTER.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.FILE_ID, self.file_id)
        _add_attribute_to_tree(tree, AttributeTags.LABEL, self.content_ids)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        if self.content is not None:
            tree.append(self.content.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> FilePointer:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('File Pointer Element cant be parsed.')

        content = None
        for child in tree:
            if child.tag == Area.tag() or child.tag == str(Area.qname()):
                content = Area.from_tree(child)
            elif child.tag == ParallelFiles.tag() or child.tag == str(
                    ParallelFiles.qname()):
                content = ParallelFiles.from_tree(child)
            elif child.tag == SequenceOfFiles.tag() or child.tag == str(
                    SequenceOfFiles.qname()):
                content = SequenceOfFiles.from_tree(child)

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        fpt = FilePointer(content=content,
                          element_id=tree.get(AttributeTags.ID.value),
                          file_id=tree.get(AttributeTags.FILE_ID.value),
                          content_ids=tree.get(AttributeTags.CONTENT_IDS.value),
                          other_attribs=other)

        return fpt

    @property
    def content(self) -> Union[Area, ParallelFiles, SequenceOfFiles]:
        return self._content

    @content.setter
    def content(self,
                content: Union[Area, ParallelFiles, SequenceOfFiles]) -> None:
        self._content = _add_mets_class(content,
                                        (Area, ParallelFiles, SequenceOfFiles))
        return

    @property
    def content_ids(self) -> str:
        return self._content_ids

    @content_ids.setter
    def content_ids(self, content_ids: str) -> None:
        self._content_ids = _get_string_value(content_ids)
        return

    @property
    def file_id(self) -> str:
        return self._file_id

    @file_id.setter
    def file_id(self, file_id: str) -> None:
        self._file_id = _get_string_value(file_id)
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


class Area(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value,
        AttributeTags.FILE_ID.value,
        AttributeTags.SHAPE.value,
        AttributeTags.COORDS.value,
        AttributeTags.BEGIN.value,
        AttributeTags.END.value,
        AttributeTags.BETYPE.value,
        AttributeTags.EXTENT.value,
        AttributeTags.EXTENT_TYPE.value,
        AttributeTags.ADMID.value,
        AttributeTags.CONTENT_IDS.value,
        AttributeTags.LABEL.value,
        AttributeTags.ORDER.value,
        AttributeTags.ORDER_LABEL.value
    ]

    def __init__(self, file_id: str, element_id: str = None, shape: str = None,
                 coords: str = None, begin: str = None,
                 end: str = None, betype: str = None, extent: str = None,
                 extent_type: str = None, admid: str = None,
                 content_ids: str = None, label: str = None, order: int = None,
                 order_label: str = None,
                 other_attribs: dict[str, str] = None):

        self.file_id = file_id
        self.id = element_id
        self.shape = shape
        self.coords = coords
        self.begin = begin
        self.end = end
        self.extent = extent
        self.admid = admid
        self.content_ids = content_ids
        self.label = label
        self.order = order
        self.order_label = order_label

        self.betype = betype
        self.extent_type = extent_type

        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.AREA.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(Area.NAMESPACE, ElementTags.AREA.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.FILE_ID, self.file_id)
        _add_attribute_to_tree(tree, AttributeTags.SHAPE, self.shape)
        _add_attribute_to_tree(tree, AttributeTags.COORDS, self.coords)
        _add_attribute_to_tree(tree, AttributeTags.BEGIN, self.begin)
        _add_attribute_to_tree(tree, AttributeTags.END, self.end)
        _add_attribute_to_tree(tree, AttributeTags.EXTENT, self.extent)
        _add_attribute_to_tree(tree, AttributeTags.ADMID, self.admid)
        _add_attribute_to_tree(tree, AttributeTags.CONTENT_IDS,
                               self.content_ids)
        _add_attribute_to_tree(tree, AttributeTags.BETYPE, self.betype)
        _add_attribute_to_tree(tree, AttributeTags.EXTENT_TYPE,
                               self.extent_type)
        _add_attribute_to_tree(tree, AttributeTags.LABEL, self.label)
        _add_attribute_to_tree(tree, AttributeTags.ORDER, self.order)
        _add_attribute_to_tree(tree, AttributeTags.ORDER_LABEL,
                               self.order_label)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> Area:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Area Element cant be parsed.')

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        area = Area(file_id=tree.get(AttributeTags.FILE_ID.value),
                    element_id=tree.get(AttributeTags.ID.value),
                    shape=tree.get(AttributeTags.SHAPE.value),
                    coords=tree.get(AttributeTags.COORDS.value),
                    begin=tree.get(AttributeTags.BEGIN.value),
                    end=tree.get(AttributeTags.END.value),
                    betype=tree.get(AttributeTags.BETYPE.value),
                    extent=tree.get(AttributeTags.EXTENT.value),
                    extent_type=tree.get(AttributeTags.EXTENT_TYPE.value),
                    admid=tree.get(AttributeTags.ADMID.value),
                    content_ids=tree.get(AttributeTags.CONTENT_IDS.value),
                    label=tree.get(AttributeTags.LABEL.value),
                    order=tree.get(AttributeTags.ORDER.value),
                    order_label=tree.get(AttributeTags.ORDER_LABEL.value),
                    other_attribs=other)
        return area

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
        self._betype = _add_enum_value(betype, AreaBeginEndTypes)
        return

    @property
    def content_ids(self) -> str:
        return self._content_ids

    @content_ids.setter
    def content_ids(self, content_ids: str) -> None:
        self._content_ids = _get_string_value(content_ids)
        return

    @property
    def coords(self) -> str:
        return self._coords

    @coords.setter
    def coords(self, coords: str) -> None:
        self._coords = _get_string_value(coords)
        return

    @property
    def end(self) -> str:
        return self._end

    @end.setter
    def end(self, end: str) -> None:
        self._end = _get_string_value(end)
        return

    @property
    def extent(self) -> str:
        return self._extent

    @extent.setter
    def extent(self, extent: str) -> None:
        self._extent = _get_string_value(extent)
        return

    @property
    def extent_type(self) -> str:
        return self._extent_type

    @extent_type.setter
    def extent_type(self, extent_type: str) -> None:
        self._extent_type = _add_enum_value(extent_type, ExtentTypes)
        return

    @property
    def file_id(self) -> str:
        return self._file_id

    @file_id.setter
    def file_id(self, file_id: str) -> None:
        self._file_id = _get_string_value(file_id)
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
    def order(self) -> int:
        return self._order

    @order.setter
    def order(self, order: int) -> None:
        self._order = _get_integer_value(order)
        return

    @property
    def order_label(self) -> str:
        return self._order_label

    @order_label.setter
    def order_label(self, order_label: str) -> None:
        self._order_label = _get_string_value(order_label)
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
    def shape(self) -> str:
        return self._shape

    @shape.setter
    def shape(self, shape: str) -> None:
        self._shape = _get_string_value(shape)
        return


class SequenceOfFiles(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value,
        AttributeTags.LABEL.value,
        AttributeTags.ORDER.value,
        AttributeTags.ORDER_LABEL.value
    ]

    def __init__(self, content: Union[
        Area, ParallelFiles, list[Union[Area, ParallelFiles]]] = None,
                 element_id: str = None, label: str = None, order: int = None,
                 order_label: str = None,
                 other_attribs: dict[str, str] = None) -> None:

        self.id = element_id
        self.label = label
        self.order = order
        self.order_label = order_label
        self.content = content
        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.SEQUENCE_OF_FILES.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(SequenceOfFiles.NAMESPACE,
                           ElementTags.SEQUENCE_OF_FILES.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.LABEL, self.label)
        _add_attribute_to_tree(tree, AttributeTags.ORDER, self.order)
        _add_attribute_to_tree(tree, AttributeTags.ORDER_LABEL,
                               self.order_label)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        for item in self.content:
            tree.append(item.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> SequenceOfFiles:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Sequence Of Files Element cant be parsed.')

        content = None
        for child in tree:
            if child.tag == Area.tag() or child.tag == str(Area.qname()):
                content = Area.from_tree(child)
            elif child.tag == ParallelFiles.tag() or child.tag == str(
                    ParallelFiles.qname()):
                content = ParallelFiles.from_tree(child)

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        seq = SequenceOfFiles(content=content,
                              element_id=tree.get(AttributeTags.ID.value),
                              label=tree.get(AttributeTags.LABEL.value),
                              order=tree.get(AttributeTags.ORDER.value),
                              order_label=tree.get(
                                  AttributeTags.ORDER_LABEL.value),
                              other_attribs=other)

        return seq

    @property
    def content(self) -> list[Union[Area, ParallelFiles]]:
        return self._content

    @content.setter
    def content(self, content: Union[
        Area, ParallelFiles, list[Union[Area, ParallelFiles]]]) -> None:
        self._content = _get_element_list(content, (Area, ParallelFiles))
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
    def order(self) -> int:
        return self._order

    @order.setter
    def order(self, order: int) -> None:
        self._order = _get_integer_value(order)
        return

    @property
    def order_label(self) -> str:
        return self._order_label

    @order_label.setter
    def order_label(self, order_label: str) -> None:
        self._order_label = _get_string_value(order_label)
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


class ParallelFiles(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value,
        AttributeTags.LABEL.value,
        AttributeTags.ORDER.value,
        AttributeTags.ORDER_LABEL.value
    ]

    def __init__(self, content: Union[
        Area, SequenceOfFiles, list[Union[Area, SequenceOfFiles]]] = None,
                 element_id: str = None, label: str = None, order: int = None,
                 order_label: str = None,
                 other_attribs: dict[str, str] = None) -> None:

        self.id = element_id
        self.label = label
        self.order = order
        self.order_label = order_label
        self.content = content
        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.PARALLEL_FILES.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(ParallelFiles.NAMESPACE,
                           ElementTags.PARALLEL_FILES.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.LABEL, self.label)
        _add_attribute_to_tree(tree, AttributeTags.ORDER, self.order)
        _add_attribute_to_tree(tree, AttributeTags.ORDER_LABEL,
                               self.order_label)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        for item in self.content:
            tree.append(item.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> ParallelFiles:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Parallel Files Element cant be parsed.')

        content = None
        for child in tree:
            if child.tag == Area.tag() or child.tag == str(Area.qname()):
                content = Area.from_tree(child)
            elif child.tag == SequenceOfFiles.tag() or child.tag == str(
                    SequenceOfFiles.qname()):
                content = SequenceOfFiles.from_tree(child)

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        par = ParallelFiles(content=content,
                            element_id=tree.get(AttributeTags.ID.value),
                            label=tree.get(AttributeTags.LABEL.value),
                            order=tree.get(AttributeTags.ORDER.value),
                            order_label=tree.get(
                                AttributeTags.ORDER_LABEL.value),
                            other_attribs=other)

        return par

    @property
    def content(self) -> list[Union[Area, SequenceOfFiles]]:
        return self._content

    @content.setter
    def content(self, content: Union[
        Area, SequenceOfFiles, list[Union[Area, SequenceOfFiles]]]) -> None:
        self._content = _get_element_list(content, (Area, SequenceOfFiles))
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
    def order(self) -> int:
        return self._order

    @order.setter
    def order(self, order: int) -> None:
        self._order = _get_integer_value(order)
        return

    @property
    def order_label(self) -> str:
        return self._order_label

    @order_label.setter
    def order_label(self, order_label: str) -> None:
        self._order_label = _get_string_value(order_label)
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


class METSPointer(METSElement):

    def __init__(self, loctype: str, element_id: str = None,
                 other_loctype: str = None, content_ids: str = None,
                 xlink_actuate: str = None, xlink_arcrole: str = None,
                 xlink_href: str = None, xlink_role: str = None,
                 xlink_show: str = None, xlink_title: str = None) -> None:
        self.loctype = loctype

        self.id = element_id
        self.other_loctype = other_loctype
        self.content_ids = content_ids
        self.xlink_href = xlink_href
        self.xlink_role = xlink_role
        self.xlink_arcrole = xlink_arcrole
        self.xlink_title = xlink_title
        self.xlink_show = xlink_show
        self.xlink_actuate = xlink_actuate

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.METS_POINTER.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(METSPointer.NAMESPACE,
                           ElementTags.METS_POINTER.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.LOCTYPE, self.loctype)
        _add_attribute_to_tree(tree, AttributeTags.LOCTYPE_OTHER,
                               self.other_loctype)
        _add_attribute_to_tree(tree, AttributeTags.CONTENT_IDS,
                               self.content_ids)

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
    def from_tree(cls, tree: etree) -> METSPointer:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('METS Pointer Element cant be parsed.')

        ptr = METSPointer(loctype=tree.get(AttributeTags.LOCTYPE.value),
                          element_id=tree.get(AttributeTags.ID.value),
                          other_loctype=tree.get(
                              AttributeTags.LOCTYPE_OTHER.value),
                          content_ids=tree.get(AttributeTags.CONTENT_IDS.value),
                          xlink_actuate=tree.get(
                              str(XlinkAttributes.ACTUATE.value)),
                          xlink_arcrole=tree.get(
                              str(XlinkAttributes.ARCROLE.value)),
                          xlink_href=tree.get(str(XlinkAttributes.HREF.value)),
                          xlink_role=tree.get(str(XlinkAttributes.ROLE.value)),
                          xlink_show=tree.get(str(XlinkAttributes.SHOW.value)),
                          xlink_title=tree.get(
                              str(XlinkAttributes.TITLE.value)))

        return ptr

    @property
    def content_ids(self) -> str:
        return self._content_ids

    @content_ids.setter
    def content_ids(self, content_ids: str) -> None:
        self._content_ids = _get_string_value(content_ids)
        return

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


class StructuralLink(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value
    ]

    def __init__(self, element_id: str = None,
                 struct_map_links: Union[
                     StructuralMapLink, list[StructuralMapLink]] = None,
                 struct_map_link_groups: Union[StructuralMapLinkGroup, list[
                     StructuralMapLinkGroup]] = None,
                 other_attribs: dict[str, str] = None) -> None:

        self.id = element_id
        self.struct_map_links = struct_map_links
        self.struct_map_link_groups = struct_map_link_groups
        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.STRUCTURAL_LINK.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(StructuralLink.NAMESPACE,
                           ElementTags.STRUCTURAL_LINK.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        for item in self.struct_map_links:
            tree.append(item.generate_tree())

        for item in self.struct_map_link_groups:
            tree.append(item.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> StructuralLink:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Structural Link Element cant be parsed.')

        struct_map_links = []
        struct_map_link_groups = []
        for child in tree:
            if child.tag == StructuralMapLink.tag() or child.tag == str(
                    StructuralMapLink.qname()):
                struct_map_links.append(StructuralMapLink.from_tree(child))
            elif child.tag == StructuralMapLinkGroup.tag() or child.tag == str(
                    StructuralMapLinkGroup.qname()):
                struct_map_link_groups.append(
                    StructuralMapLinkGroup.from_tree(child))

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        struct_link = StructuralLink(
            element_id=tree.get(AttributeTags.ID.value),
            struct_map_links=struct_map_links,
            struct_map_link_groups=struct_map_link_groups,
            other_attribs=other)

        return struct_link

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
    def struct_map_link_groups(self) -> list[StructuralMapLinkGroup]:
        return self._struct_map_link_groups

    @struct_map_link_groups.setter
    def struct_map_link_groups(self, struct_map_link_groups: Union[
        StructuralMapLinkGroup,
        list[StructuralMapLinkGroup]]) -> None:
        self._struct_map_link_groups = _get_element_list(struct_map_link_groups,
                                                         StructuralMapLinkGroup)
        return

    @property
    def struct_map_links(self) -> list[StructuralMapLink]:
        return self._struct_map_links

    @struct_map_links.setter
    def struct_map_links(self, struct_map_links: Union[
        StructuralMapLink, list[StructuralMapLink]]) -> None:
        self._struct_map_links = _get_element_list(struct_map_links,
                                                   StructuralMapLink)
        return


class StructuralMapLink(METSElement):

    def __init__(self, xlink_from: str, xlink_to: str, element_id: str = None,
                 xlink_arcrole: str = None,
                 xlink_title: str = None, xlink_show: str = None,
                 xlink_actuate: str = None) -> None:
        self.xlink_to = xlink_to
        self.xlink_from = xlink_from

        self.id = element_id
        self.xlink_arcrole = xlink_arcrole
        self.xlink_title = xlink_title
        self.xlink_show = xlink_show
        self.xlink_actuate = xlink_actuate

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.STRUCTURAL_MAP_LINK.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(StructuralMapLink.NAMESPACE,
                           ElementTags.STRUCTURAL_MAP_LINK.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())
        _add_namespace_attribute_to_tree(tree, XlinkAttributes.TO.value,
                                         self.xlink_to)
        _add_namespace_attribute_to_tree(tree, XlinkAttributes.FROM.value,
                                         self.xlink_from)

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
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
    def from_tree(cls, tree: etree) -> StructuralMapLink:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Structural Map Link Element cant be parsed.')

        sml = StructuralMapLink(
            xlink_from=tree.get(str(XlinkAttributes.FROM.value)),
            xlink_to=tree.get(str(XlinkAttributes.TO.value)),
            element_id=tree.get(AttributeTags.ID.value),
            xlink_arcrole=tree.get(str(XlinkAttributes.ARCROLE.value)),
            xlink_title=tree.get(str(XlinkAttributes.TITLE.value)),
            xlink_show=tree.get(str(XlinkAttributes.SHOW.value)),
            xlink_actuate=tree.get(str(XlinkAttributes.ACTUATE.value)))

        return sml

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
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
    def xlink_from(self) -> str:
        return self._xlink_from

    @xlink_from.setter
    def xlink_from(self, xlink_from: str) -> None:
        self._xlink_from = _get_string_value(xlink_from, False)
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
    def xlink_to(self) -> str:
        return self._xlink_to

    @xlink_to.setter
    def xlink_to(self, xlink_to: str) -> None:
        self._xlink_to = _get_string_value(xlink_to, False)
        return


class StructuralMapLinkGroup(METSElement):

    def __init__(self, locator_links: list[StructuralMapLocatorLink],
                 arclinks: Union[
                     StructuralMapArcLink, list[StructuralMapArcLink]],
                 element_id: str = None,
                 arclink_order: str = None, xlink_role: str = None,
                 xlink_title: str = None) -> None:

        self.locator_links = locator_links
        self.arclinks = arclinks

        self.arclink_order = arclink_order
        self.id = element_id
        self.xlink_role = xlink_role
        self.xlink_title = xlink_title

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.STRUCTURAL_MAP_LINK.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(StructuralMapLink.NAMESPACE,
                           ElementTags.STRUCTURAL_MAP_LINK.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())
        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.ARCLINK_ORDER,
                               self.arclink_order)

        _add_namespace_attribute_to_tree(tree, etree.QName(NAMESPACES['xlink'],
                                                           XlinkAttributes.ROLE.value),
                                         self.xlink_role)
        _add_namespace_attribute_to_tree(tree, etree.QName(NAMESPACES['xlink'],
                                                           XlinkAttributes.TITLE.value),
                                         self.xlink_title)

        for item in self.locator_links:
            tree.append(item.generate_tree())

        for item in self.arclinks:
            tree.append(item.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> StructuralMapLinkGroup:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError(
                'Structural Map Link Group Element cant be parsed.')

        locator_links = []
        arclinks = []
        for child in tree:
            if child.tag == StructuralMapLocatorLink.tag() or child.tag == str(
                    StructuralMapLocatorLink.qname()):
                locator_links = StructuralMapLocatorLink.from_tree(child)
            elif child.tag == StructuralMapArcLink.tag() or child.tag == str(
                    StructuralMapArcLink.qname()):
                arclinks = StructuralMapArcLink.from_tree(child)

        smlg = StructuralMapLinkGroup(locator_links=locator_links,
                                      arclinks=arclinks,
                                      element_id=tree.get(
                                          AttributeTags.ID.value),
                                      arclink_order=tree.get(
                                          AttributeTags.ARCLINK_ORDER.value),
                                      xlink_role=tree.get(
                                          XlinkAttributes.ROLE.value),
                                      xlink_title=tree.get(
                                          XlinkAttributes.TITLE.value))

        return smlg

    @property
    def arclink_order(self) -> str:
        return self._arclink_order

    @arclink_order.setter
    def arclink_order(self, arclink_order: str) -> None:
        if arclink_order is not None:
            self._arclink_order = _add_enum_value(arclink_order,
                                                  ArclinkOrderTypes)
        else:
            self._arclink_order = 'unordered'
        return

    @property
    def arclinks(self) -> list[StructuralMapArcLink]:
        return self._arclinks

    @arclinks.setter
    def arclinks(self, arclinks: Union[
        StructuralMapArcLink, list[StructuralMapArcLink]]) -> None:
        self._arclinks = _get_element_list(arclinks, StructuralMapArcLink,
                                           False)
        return

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
        return

    @property
    def locator_links(self) -> list[StructuralMapLocatorLink]:
        return self._locator_links

    @locator_links.setter
    def locator_links(self, locator_links: Union[
        StructuralMapLocatorLink, list[StructuralMapLocatorLink]]) -> None:
        self._locator_links = _get_element_list(locator_links,
                                                StructuralMapLocatorLink, False)
        if len(self.locator_links) < 2:
            raise METSLibError(
                'At least two Locator Links must be present in Structural Map Link Group Element')
        return

    @property
    def xlink_role(self) -> str:
        return self._xlink_role

    @xlink_role.setter
    def xlink_role(self, xlink_role: str) -> None:
        self._xlink_role = _get_string_value(xlink_role)
        return

    @property
    def xlink_title(self) -> str:
        return self._xlink_title

    @xlink_title.setter
    def xlink_title(self, xlink_title: str) -> None:
        self._xlink_title = _get_string_value(xlink_title)
        return


class StructuralMapLocatorLink(METSElement):

    def __init__(self, xlink_href: str, element_id: str = None,
                 xlink_label: str = None, xlink_role: str = None,
                 xlink_title: str = None) -> None:
        self.xlink_href = xlink_href

        self.id = element_id
        self.xlink_label = xlink_label
        self.xlink_role = xlink_role
        self.xlink_title = xlink_title

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.STRUCTURAL_MAP_LOCATOR_LINK.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(StructuralMapLink.NAMESPACE,
                           ElementTags.STRUCTURAL_MAP_LOCATOR_LINK.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)

        _add_namespace_attribute_to_tree(tree, XlinkAttributes.HREF.value,
                                         self.xlink_href)
        _add_namespace_attribute_to_tree(tree, XlinkAttributes.LABEL.value,
                                         self.xlink_label)
        _add_namespace_attribute_to_tree(tree, XlinkAttributes.ROLE.value,
                                         self.xlink_role)
        _add_namespace_attribute_to_tree(tree, XlinkAttributes.TITLE.value,
                                         self.xlink_title)

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> StructuralMapLocatorLink:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError(
                'Structural Map Locator Link Element cant be parsed.')

        smll = StructuralMapLocatorLink(
            xlink_href=tree.get(str(XlinkAttributes.HREF.value)),
            element_id=tree.get(AttributeTags.ID.value),
            xlink_label=tree.get(str(XlinkAttributes.LABEL.value)),
            xlink_role=tree.get(str(XlinkAttributes.ROLE.value)),
            xlink_title=tree.get(str(XlinkAttributes.TITLE.value)))

        return smll

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = self.id = _get_string_value(element_id)
        return

    @property
    def xlink_href(self) -> str:
        return self._xlink_href

    @xlink_href.setter
    def xlink_href(self, xlink_href: str) -> None:
        self._xlink_href = _get_string_value(xlink_href, False)
        return

    @property
    def xlink_label(self) -> str:
        return self._xlink_label

    @xlink_label.setter
    def xlink_label(self, xlink_label: str) -> None:
        self._xlink_label = _get_string_value(xlink_label)
        return

    @property
    def xlink_role(self) -> str:
        return self._xlink_role

    @xlink_role.setter
    def xlink_role(self, xlink_role: str) -> None:
        self._xlink_role = _get_string_value(xlink_role)
        return

    @property
    def xlink_title(self) -> str:
        return self._xlink_title

    @xlink_title.setter
    def xlink_title(self, xlink_title: str) -> None:
        self._xlink_title = _get_string_value(xlink_title)
        return


class StructuralMapArcLink(METSElement):

    def __init__(self, element_id: str = None, admid: str = None,
                 arctype: str = None, xlink_arcrole: str = None,
                 xlink_title: str = None, xlink_from: str = None,
                 xlink_to: str = None, xlink_show: str = None,
                 xlink_actuate: str = None) -> None:
        self.id = element_id
        self.admid = admid
        self.arctype = arctype
        self.xlink_arcrole = xlink_arcrole
        self.xlink_title = xlink_title
        self.xlink_from = xlink_from
        self.xlink_to = xlink_to
        self.xlink_show = xlink_show
        self.xlink_actuate = xlink_actuate

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.STRUCTURAL_MAP_ARCLINK.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(StructuralMapLink.NAMESPACE,
                           ElementTags.STRUCTURAL_MAP_ARCLINK.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())
        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.ADMID, self.admid)
        _add_attribute_to_tree(tree, AttributeTags.ARCTYPE, self.arctype)

        _add_namespace_attribute_to_tree(tree, XlinkAttributes.TO.value,
                                         self.xlink_to)
        _add_namespace_attribute_to_tree(tree, XlinkAttributes.FROM.value,
                                         self.xlink_from)
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
    def from_tree(cls, tree: etree) -> StructuralMapArcLink:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Structural Map Arc Link Element cant be parsed.')

        smal = StructuralMapArcLink(element_id=tree.get(AttributeTags.ID.value),
                                    admid=tree.get(AttributeTags.ADMID.value),
                                    arctype=tree.get(
                                        AttributeTags.ARCTYPE.value),
                                    xlink_arcrole=tree.get(
                                        str(XlinkAttributes.ARCROLE.value)),
                                    xlink_title=tree.get(
                                        str(XlinkAttributes.TITLE.value)),
                                    xlink_from=tree.get(
                                        str(XlinkAttributes.FROM.value)),
                                    xlink_to=tree.get(
                                        str(XlinkAttributes.TO.value)),
                                    xlink_show=tree.get(
                                        str(XlinkAttributes.SHOW.value)),
                                    xlink_actuate=tree.get(
                                        str(XlinkAttributes.ACTUATE.value)))

        return smal

    @property
    def admid(self) -> str:
        return self._admid

    @admid.setter
    def admid(self, admid: str) -> None:
        self._admid = _get_string_value(admid)
        return

    @property
    def arctype(self) -> str:
        return self._arctype

    @arctype.setter
    def arctype(self, arctype: str) -> None:
        self._arctype = _get_string_value(arctype)
        return

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
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
    def xlink_from(self) -> str:
        return self._xlink_from

    @xlink_from.setter
    def xlink_from(self, xlink_from: str) -> None:
        self._xlink_from = _get_string_value(xlink_from)
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
    def xlink_to(self) -> str:
        return self._xlink_to

    @xlink_to.setter
    def xlink_to(self, xlink_to: str) -> None:
        self._xlink_to = _get_string_value(xlink_to)
        return
