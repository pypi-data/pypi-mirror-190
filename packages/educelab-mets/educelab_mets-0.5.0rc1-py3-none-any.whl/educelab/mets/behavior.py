from __future__ import annotations

import datetime
from abc import abstractmethod
from typing import Union

from lxml import etree

from .constants import ElementTags, AttributeTags, XlinkAttributes, \
    LocatorTypes, XlinkActuateTypes, XlinkShowTypes
from .exceptions import ParseError
from .generic import METSElement
from .utils import _get_element_list, _add_attribute_to_tree, \
    _add_namespace_attribute_to_tree, _get_string_value, \
    _get_datetime_value, _check_tag, _add_mets_class, _add_enum_value


class BehaviorSection(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value,
        AttributeTags.CREATED.value,
        AttributeTags.LABEL.value
    ]

    def __init__(self, element_id: str,
                 created: Union[datetime.datetime, str] = None,
                 label: str = None,
                 content: Union[BehaviorSection, Behavior, list[
                     Union[BehaviorSection, Behavior]]] = None,
                 other_attribs: dict[str, str] = None) -> None:
        self.id = element_id
        self.created = created
        self.label = label

        self.content = content
        self.behavior_sections = None
        self.behaviors = None

        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.BEHAVIOR_SECTION.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(BehaviorSection.NAMESPACE,
                           ElementTags.BEHAVIOR_SECTION.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.CREATED, self.created)
        _add_attribute_to_tree(tree, AttributeTags.LABEL, self.label)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        if self.behavior_sections is not None:
            for item in self.behavior_sections:
                tree.append(item.generate_tree())

        if self.behaviors is not None:
            for item in self.behaviors:
                tree.append(item.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> BehaviorSection:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Behavior Section Element cant be parsed.')

        content = []
        for child in tree:
            if child.tag == BehaviorSection.tag():
                content.append(BehaviorSection.from_tree(child))
            elif child.tag == Behavior.tag():
                content.append(Behavior.from_tree(child))

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        beh_sec = BehaviorSection(element_id=tree.get(AttributeTags.ID.value),
                                  created=tree.get(AttributeTags.CREATED.value),
                                  label=tree.get(AttributeTags.LABEL.value),
                                  content=content,
                                  other_attribs=other)

        return beh_sec

    @property
    def content(self) -> tuple[BehaviorSection, Behavior]:
        return self.behavior_sections + self.behaviors

    @content.setter
    def content(self, content: Union[
        BehaviorSection, Behavior, list[BehaviorSection, Behavior]]) -> None:
        result = _get_element_list(content, (BehaviorSection, Behavior))
        self._behavior_sections = \
            [item for item in result if item.tag() == BehaviorSection.tag()][0]
        self._behaviors = [item for item in result if
                           item.tag() == Behavior.tag()]
        return

    @property
    def behavior_sections(self) -> tuple[BehaviorSection]:
        return tuple(self._behavior_sections)

    @behavior_sections.setter
    def behavior_sections(self, behavior_sections: Union[
        BehaviorSection, list[BehaviorSection]]) -> None:
        self._behavior_sections = _get_element_list(behavior_sections,
                                                    BehaviorSection)
        return

    @property
    def behaviors(self) -> tuple[Behavior]:
        return tuple(self._behaviors)

    @behaviors.setter
    def behaviors(self, behaviors: Union[Behavior, list[Behavior]]) -> None:
        self._behaviors = _get_element_list(behaviors, Behavior)
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
    def other_attribs(self) -> dict[str, str]:
        return self._other_attribs

    @other_attribs.setter
    def other_attribs(self, other_attribs: dict[str, str]) -> None:
        if other_attribs is not None:
            self._other_attribs = other_attribs
        else:
            self._other_attribs = {}
        return


class Behavior(METSElement):

    def __init__(self, mechanism: ExecutableMechanism, element_id: str = None,
                 struct_id: str = None, btype: str = None,
                 created: Union[datetime.datetime, str] = None,
                 label: str = None, group_id: str = None,
                 admid: str = None,
                 interface_def: InterfaceDefinition = None) -> None:

        self.mechanism = mechanism

        self.id = element_id
        self.struct_id = struct_id
        self.btype = btype
        self.created = created
        self.label = label
        self.group_id = group_id
        self.admid = admid
        self.interface_def = interface_def

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.BEHAVIOR.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(Behavior.NAMESPACE, ElementTags.BEHAVIOR.value)

    def verify(self) -> bool:
        if self.mechanism is not None:
            return True
        else:
            return False

    def generate_tree(self) -> etree:
        if self.verify():
            tree = etree.Element(self.qname())

            tree.append(self.mechanism.generate_tree())

            _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
            _add_attribute_to_tree(tree, AttributeTags.STRUCT_ID,
                                   self.struct_id)
            _add_attribute_to_tree(tree, AttributeTags.BTYPE, self.btype)
            _add_attribute_to_tree(tree, AttributeTags.CREATED, self.created)
            _add_attribute_to_tree(tree, AttributeTags.LABEL, self.label)
            _add_attribute_to_tree(tree, AttributeTags.GROUP_ID, self.group_id)
            _add_attribute_to_tree(tree, AttributeTags.ADMID, self.admid)

            if self.interface_def is not None:
                tree.append(self.interface_def.generate_tree())

            return tree
        else:
            print(self.tag() + ' Element failed verification check.')
            return None

    @classmethod
    def from_tree(cls, tree: etree) -> Behavior:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Behavior Element cant be parsed.')

        mechanism = None
        interface = None
        for child in tree:
            if child.tag == ExecutableMechanism.tag():
                mechanism = ExecutableMechanism.from_tree(child)
            elif child.tag == InterfaceDefinition.tag():
                interface = InterfaceDefinition.from_tree(child)

        beh = Behavior(mechanism=mechanism,
                       element_id=tree.get(AttributeTags.ID.value),
                       struct_id=tree.get(AttributeTags.STRUCT_ID.value),
                       btype=tree.get(AttributeTags.BTYPE.value),
                       created=tree.get(AttributeTags.CREATED.value),
                       label=tree.get(AttributeTags.LABEL.value),
                       group_id=tree.get(AttributeTags.GROUP_ID.value),
                       admid=tree.get(AttributeTags.ADMID.value),
                       interface_def=interface)

        return beh

    @property
    def admid(self) -> str:
        return self._admid

    @admid.setter
    def admid(self, admid: str) -> None:
        self._admid = _get_string_value(admid)
        return

    @property
    def btype(self) -> str:
        return self._btype

    @btype.setter
    def btype(self, btype: str) -> None:
        self._btype = _get_string_value(btype)
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
        self._id = _get_string_value(element_id)
        return

    @property
    def interface_def(self) -> InterfaceDefinition:
        return self._interface_def

    @interface_def.setter
    def interface_def(self, interface_def: InterfaceDefinition) -> None:
        self._interface_def = _add_mets_class(interface_def,
                                              InterfaceDefinition)
        return

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str) -> None:
        self._label = _get_string_value(label)
        return

    @property
    def mechanism(self) -> ExecutableMechanism:
        return self._mechanism

    @mechanism.setter
    def mechanism(self, mechanism: ExecutableMechanism) -> None:
        self._mechanism = _add_mets_class(mechanism, ExecutableMechanism, False)
        return

    @property
    def struct_id(self) -> str:
        return self._struct_id

    @struct_id.setter
    def struct_id(self, struct_id: str) -> None:
        self._struct_id = _get_string_value(struct_id)
        return


class GenericBehaviorElement(METSElement):

    def __init__(self, loctype: str, xlink_href: str, element_id: str = None,
                 label: str = None,
                 other_loctype: str = None, xlink_role: str = None,
                 xlink_arcrole: str = None, xlink_title: str = None,
                 xlink_show: str = None, xlink_actuate: str = None) -> None:

        self.loctype = loctype
        self.xlink_href = xlink_href

        self.id = element_id
        self.label = label
        self.other_loctype = other_loctype
        self.xlink_role = xlink_role
        self.xlink_arcrole = xlink_arcrole
        self.xlink_title = xlink_title
        self.xlink_show = xlink_show
        self.xlink_actuate = xlink_actuate

        return

    @staticmethod
    @abstractmethod
    def tag():
        pass

    @staticmethod
    @abstractmethod
    def qname():
        pass

    def verify(self) -> bool:
        if self.loctype is not None and self.xlink_href is not None:
            return True
        else:
            return False

    def generate_tree(self) -> etree:
        if self.verify():
            tree = etree.Element(etree.QName(self.NAMESPACE, self.tag()))

            _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
            _add_attribute_to_tree(tree, AttributeTags.LABEL, self.label)
            _add_attribute_to_tree(tree, AttributeTags.LOCTYPE, self.loctype)
            _add_attribute_to_tree(tree, AttributeTags.LOCTYPE_OTHER,
                                   self.other_loctype)

            _add_namespace_attribute_to_tree(tree, XlinkAttributes.HREF.value,
                                             self.xlink_href)
            _add_namespace_attribute_to_tree(tree, XlinkAttributes.ROLE.value,
                                             self.xlink_role)
            _add_namespace_attribute_to_tree(tree,
                                             XlinkAttributes.ARCROLE.value,
                                             self.xlink_arcrole)
            _add_namespace_attribute_to_tree(tree, XlinkAttributes.TITLE.value,
                                             self.xlink_title)
            _add_namespace_attribute_to_tree(tree, XlinkAttributes.SHOW.value,
                                             self.xlink_show)
            _add_namespace_attribute_to_tree(tree,
                                             XlinkAttributes.ACTUATE.value,
                                             self.xlink_actuate)

            return tree
        else:
            print(self.tag() + ' Element failed verification check.')
            return None

    @classmethod
    def from_tree(cls, tree: etree):
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Behavior Section Element cant be parsed.')

        element = cls(loctype=tree.get(AttributeTags.LOCTYPE.value),
                      xlink_href=tree.get(str(XlinkAttributes.HREF.value)),
                      element_id=tree.get(AttributeTags.ID.value),
                      label=tree.get(AttributeTags.LABEL.value),
                      other_loctype=tree.get(AttributeTags.LOCTYPE_OTHER.value),
                      xlink_role=tree.get(str(XlinkAttributes.ROLE.value)),
                      xlink_arcrole=tree.get(
                          str(XlinkAttributes.ARCROLE.value)),
                      xlink_title=tree.get(str(XlinkAttributes.TITLE.value)),
                      xlink_show=tree.get(str(XlinkAttributes.SHOW.value)),
                      xlink_actuate=tree.get(
                          str(XlinkAttributes.ACTUATE.value)))

        return element

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


class ExecutableMechanism(GenericBehaviorElement):

    @staticmethod
    def tag() -> str:
        return ElementTags.EXECUTABLE_MECHANISM.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(ExecutableMechanism.NAMESPACE,
                           ElementTags.EXECUTABLE_MECHANISM.value)


class InterfaceDefinition(GenericBehaviorElement):

    @staticmethod
    def tag() -> str:
        return ElementTags.INTERFACE_DEFINITION.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(InterfaceDefinition.NAMESPACE,
                           ElementTags.INTERFACE_DEFINITION.value)
