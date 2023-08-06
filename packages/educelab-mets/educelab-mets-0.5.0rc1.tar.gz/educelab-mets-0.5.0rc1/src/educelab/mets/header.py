from __future__ import annotations

import datetime
from typing import Union

from lxml import etree

from .constants import ElementTags, AttributeTags, AgentRoles, AgentTypes
from .exceptions import ParseError
from .generic import METSElement
from .utils import _get_element_list, _add_attribute_to_tree, _get_string_value, \
    _get_datetime_value, _add_mets_class, \
    _check_tag, _add_enum_value


class Header(METSElement):
    _ATTRIBUTES = [
        AttributeTags.ID.value,
        AttributeTags.ADMID.value,
        AttributeTags.CREATEDATE.value,
        AttributeTags.LASTMODDATE.value,
        AttributeTags.RECORDSTATUS.value
    ]

    def __init__(self, element_id: str = None, admid: str = None,
                 create_date: Union[datetime.datetime, str] = None,
                 last_mod_date: Union[datetime.datetime, str] = None,
                 record_status: str = None,
                 agents: Union[Agent, list[Agent]] = None,
                 alternative_ids: Union[
                     AlternativeIdentifier, list[AlternativeIdentifier]] = None,
                 document_id: METSDocumentID = None,
                 other_attribs: dict[str, str] = None) -> None:
        self.id = element_id
        self.admid = admid
        self.create_date = create_date
        self.last_mod_date = last_mod_date
        self.record_status = record_status
        self.document_id = document_id
        self.agents = agents
        self.alternative_ids = alternative_ids

        self.other_attribs = other_attribs

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.HEADER.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(Header.NAMESPACE, ElementTags.HEADER.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.ADMID, self.admid)
        _add_attribute_to_tree(tree, AttributeTags.CREATEDATE, self.create_date)
        _add_attribute_to_tree(tree, AttributeTags.LASTMODDATE,
                               self.last_mod_date)
        _add_attribute_to_tree(tree, AttributeTags.RECORDSTATUS,
                               self.record_status)

        for key in self.other_attribs:
            _add_attribute_to_tree(tree, key, self.other_attribs[key])

        for agent in self.agents:
            tree.append(agent.generate_tree())

        for aid in self.alternative_ids:
            tree.append(aid.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> Header:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Only Header element can be parsed.')

        document_id = None
        agents = []
        alternative_ids = []

        for child in tree:
            if child.tag == Agent.tag() or child.tag == str(Agent.qname()):
                agents.append(Agent.from_tree(child))
            elif child.tag == AlternativeIdentifier.tag() or child.tag == str(
                    AlternativeIdentifier.qname()):
                alternative_ids.append(AlternativeIdentifier.from_tree(child))
            elif child.tag == METSDocumentID.tag() or child.tag == str(
                    METSDocumentID.qname()):
                document_id = METSDocumentID.from_tree(child)

        other = {}
        for key in tree.keys():
            if key not in cls._ATTRIBUTES:
                other[str(key)] = str(tree.get(key))

        header = Header(element_id=tree.get(AttributeTags.ID.value),
                        admid=tree.get(AttributeTags.ADMID.value),
                        create_date=tree.get(AttributeTags.CREATEDATE.value),
                        last_mod_date=tree.get(AttributeTags.LASTMODDATE.value),
                        record_status=tree.get(
                            AttributeTags.RECORDSTATUS.value), agents=agents,
                        alternative_ids=alternative_ids,
                        document_id=document_id, other_attribs=other)

        return header

    @property
    def admid(self) -> str:
        return self._admid

    @admid.setter
    def admid(self, admid: str) -> None:
        self._admid = _get_string_value(admid)
        return

    @property
    def agents(self) -> list[Agent]:
        return self._agents

    @agents.setter
    def agents(self, agents: Union[Agent, list[Agent]]) -> None:
        self._agents = _get_element_list(agents, Agent)
        return

    @property
    def alternative_ids(self) -> list[AlternativeIdentifier]:
        return self._alternative_ids

    @alternative_ids.setter
    def alternative_ids(self,
                        alternative_ids: list[AlternativeIdentifier]) -> None:
        self._alternative_ids = _get_element_list(alternative_ids,
                                                  AlternativeIdentifier)
        return

    @property
    def create_date(self) -> str:
        return self._create_date

    @create_date.setter
    def create_date(self, create_date: Union[str, datetime.datetime]) -> None:
        self._create_date = _get_datetime_value(create_date)
        return

    @property
    def document_id(self) -> METSDocumentID:
        return self._document_id

    @document_id.setter
    def document_id(self, document_id: METSDocumentID) -> None:
        self._document_id = _add_mets_class(document_id, METSDocumentID)
        return

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
        return

    @property
    def last_mod_date(self) -> str:
        return self._last_mod_date

    @last_mod_date.setter
    def last_mod_date(self,
                      last_mod_date: Union[str, datetime.datetime]) -> None:
        self._last_mod_date = _get_datetime_value(last_mod_date)
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
    def record_status(self) -> str:
        return self._record_status

    @record_status.setter
    def record_status(self, record_status: str) -> None:
        self._record_status = _get_string_value(record_status)
        return


class Agent(METSElement):

    def __init__(self, name: Name, role: str, element_id: str = None,
                 role_other: str = None, agent_type: str = None,
                 type_other: str = None,
                 notes: Union[list[Note], Note] = None) -> None:

        self.name = name
        self.role = role

        self.type = agent_type
        self.notes = notes
        self.id = element_id
        self.role_other = role_other
        self.type_other = type_other

        return

    @staticmethod
    def tag() -> str:
        return ElementTags.AGENT.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(Agent.NAMESPACE, ElementTags.AGENT.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())
        tree.append(self.name.generate_tree())
        _add_attribute_to_tree(tree, AttributeTags.ROLE, self.role)

        _add_attribute_to_tree(tree, AttributeTags.ROLE_OTHER, self.role_other)
        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.TYPE, self.type)
        _add_attribute_to_tree(tree, AttributeTags.TYPE_OTHER, self.type_other)

        for n in self.notes:
            tree.append(n.generate_tree())

        return tree

    @classmethod
    def from_tree(cls, tree) -> Agent:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Only Agent element can be parsed.')

        name = None
        notes = []

        for child in tree:
            if child.tag == Note.tag() or child.tag == str(Note.qname()):
                notes.append(Note.from_tree(child))
            elif child.tag == Name.tag() or child.tag == str(Name.qname()):
                name = Name.from_tree(child)

        agent = Agent(name=name, role=tree.get(AttributeTags.ROLE.value),
                      element_id=tree.get(AttributeTags.ID.value),
                      role_other=tree.get(AttributeTags.ROLE_OTHER.value),
                      agent_type=tree.get(AttributeTags.TYPE.value),
                      type_other=tree.get(AttributeTags.TYPE_OTHER.value),
                      notes=notes)

        return agent

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
        return

    @property
    def name(self) -> Name:
        return self._name

    @name.setter
    def name(self, name: Name) -> None:
        self._name = _add_mets_class(name, Name, False)
        return

    @property
    def notes(self) -> list[Note]:
        return self._notes

    @notes.setter
    def notes(self, notes: Union[Note, list[Note]]) -> None:
        self._notes = _get_element_list(notes, Note)
        return

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, role: str) -> None:
        self._role = _add_enum_value(role, AgentRoles, False)
        return

    @property
    def role_other(self) -> str:
        return self._role_other

    @role_other.setter
    def role_other(self, role_other: str) -> None:
        self._role_other = _get_string_value(role_other)
        return

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, agent_type: str) -> None:
        self._type = _add_enum_value(agent_type, AgentTypes)
        return

    @property
    def type_other(self) -> str:
        return self._type_other

    @type_other.setter
    def type_other(self, type_other: str) -> None:
        self._type_other = _get_string_value(type_other)
        return


class Name(METSElement):

    def __init__(self, name: str) -> None:
        self.name = _get_string_value(name, False)
        return

    @staticmethod
    def tag() -> str:
        return ElementTags.NAME.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(Name.NAMESPACE, ElementTags.NAME.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())
        tree.text = self.name
        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> Name:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Only Name element can be parsed.')

        name = Name(tree.text)
        return name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = _get_string_value(name, False)
        return


class Note(METSElement):

    def __init__(self, note: str) -> None:
        self.note = _get_string_value(note, False)
        return

    @staticmethod
    def tag() -> str:
        return ElementTags.NOTE.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(Note.NAMESPACE, ElementTags.NOTE.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())
        tree.text = self.note
        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> Note:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Only Note element can be parsed.')

        note = Note(tree.text)
        return note

    @property
    def note(self) -> str:
        return self._note

    @note.setter
    def note(self, note: str) -> None:
        self._note = _get_string_value(note, False)
        return


class AlternativeIdentifier(METSElement):

    def __init__(self, value: str, element_id: str = None,
                 ai_type: str = None) -> None:
        self.value = value

        self.id = element_id
        self.type = ai_type
        return

    @staticmethod
    def tag() -> str:
        return ElementTags.ALTERNATIVE_IDENTIFIER.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(AlternativeIdentifier.NAMESPACE,
                           ElementTags.ALTERNATIVE_IDENTIFIER.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())
        tree.text = self.value

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.TYPE, self.type)

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> AlternativeIdentifier:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError(
                'Only Alternative Identifier element can be parsed.')

        ai = AlternativeIdentifier(value=tree.text,
                                   element_id=tree.get(AttributeTags.ID.value),
                                   ai_type=tree.get(AttributeTags.TYPE.value))

        return ai

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
        return

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, ai_type: str) -> None:
        self._type = _get_string_value(ai_type)
        return

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = _get_string_value(value, False)
        return


class METSDocumentID(METSElement):

    def __init__(self, value: str, element_id: str = None,
                 id_type: str = None) -> None:
        self.value = value

        self.id = element_id
        self.type = id_type
        return

    @staticmethod
    def tag() -> str:
        return ElementTags.METS_DOCUMENT_ID.value

    @staticmethod
    def qname() -> etree.QName:
        return etree.QName(METSDocumentID.NAMESPACE,
                           ElementTags.METS_DOCUMENT_ID.value)

    def generate_tree(self) -> etree:
        tree = etree.Element(self.qname())
        tree.text = self.value

        _add_attribute_to_tree(tree, AttributeTags.ID, self.id)
        _add_attribute_to_tree(tree, AttributeTags.TYPE, self.type)

        return tree

    @classmethod
    def from_tree(cls, tree: etree) -> METSDocumentID:
        if not _check_tag(tree.tag, cls.tag()):
            raise ParseError('Only Document ID element can be parsed.')

        doc_id = METSDocumentID(value=tree.text,
                                element_id=tree.get(AttributeTags.ID.value),
                                id_type=tree.get(AttributeTags.TYPE.value))

        return doc_id

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, element_id: str) -> None:
        self._id = _get_string_value(element_id)
        return

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, id_type: str) -> None:
        self._type = _get_string_value(id_type)
        return

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = _get_string_value(value, False)
        return
