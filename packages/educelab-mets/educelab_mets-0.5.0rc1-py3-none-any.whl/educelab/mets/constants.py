from enum import Enum
from typing import Final

from lxml import etree

METS_SCHEMA_VERSION: Final[str] = '1.12.1'

NAMESPACES = {
    # None: 'http://www.loc.gov/METS/',
    'mets': 'http://www.loc.gov/METS/',
    'xlink': 'http://www.w3.org/1999/xlink'
}

TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
METS_REQUIRED_FUNCTION = 'generate_tree'


class METSEnum(Enum):
    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value

    @classmethod
    def has_value(cls, value: str) -> bool:
        if value in cls._value2member_map_:
            return True
        else:
            return False


class ElementTags(METSEnum):
    METS = 'mets'
    HEADER = 'metsHdr'
    DESCRIPTIVE_METADATA = 'dmdSec'
    ADMINISTRATIVE_METADATA = 'amdSec'
    FILE_SECTION = 'fileSec'
    STRUCTURAL_MAP = 'structMap'
    STRUCTURAL_LINK = 'structLink'
    BEHAVIOR_SECTION = 'behaviorSec'
    AGENT = 'agent'
    ALTERNATIVE_IDENTIFIER = 'altRecordID'
    NAME = 'name'
    NOTE = 'note'
    METS_DOCUMENT_ID = 'metsDocumentID'
    METADATA_REFERENCE = 'mdRef'
    METADATA_WRAPPER = 'mdWrap'
    BIN_DATA = 'binData'
    XML_DATA = 'xmlData'
    TECHNICAL_METADATA = 'techMD'
    PROPERTY_RIGHTS_METADATA = 'rightsMD'
    SOURCE_METADATA = 'sourceMD'
    DIGITAL_PROVENANCE_METADATA = 'digiprovMD'
    BEHAVIOR = 'behavior'
    INTERFACE_DEFINITION = 'interfaceDef'
    EXECUTABLE_MECHANISM = 'mechanism'
    FILE_GROUP = 'fileGrp'
    FILE = 'file'
    FILE_LOCATION = 'FLocat'
    FILE_CONTENT = 'FContent'
    COMPONENT_BYTE_STREAM = 'stream'
    TRANSFORM_FILE = 'transformFile'
    STRUCTURAL_MAP_LINK = 'smLink'
    STRUCTURAL_MAP_LINK_GROUP = 'smLinkGrp'
    STRUCTURAL_MAP_ARCLINK = 'smArcLink'
    STRUCTURAL_MAP_LOCATOR_LINK = 'smLocatorLink'
    DIVISION = 'div'
    METS_POINTER = 'mptr'
    FILE_POINTER = 'fptr'
    AREA = 'area'
    SEQUENCE_OF_FILES = 'seq'
    PARALLEL_FILES = 'par'


class AttributeTags(METSEnum):
    ID = 'ID'
    ADMID = 'ADMID'
    CREATEDATE = 'CREATEDATE'
    LASTMODDATE = 'LASTMODDATE'
    RECORDSTATUS = 'RECORDSTATUS'
    ROLE = 'ROLE'
    ROLE_OTHER = 'OTHER_ROLE'
    TYPE = 'TYPE'
    TYPE_OTHER = 'OTHER_TYPE'
    OBJID = 'OBJID'
    LABEL = 'LABEL'
    PROFILE = 'PROFILE'
    GROUP_ID = 'GROUPID'
    CREATED = 'CREATED'
    STATUS = 'STATUS'
    MDTYPE = 'MDTYPE'
    MDTYPE_OTHER = 'OTHERMDTYPE'
    MDTYPE_VERSION = 'MDTYPEVERSION'
    MIMETYPE = 'MIMETYPE'
    SIZE = 'SIZE'
    CHECKSUM = 'CHECKSUM'
    CHECKSUM_TYPE = 'CHECKSUMTYPE'
    LOCTYPE = 'LOCTYPE'
    LOCTYPE_OTHER = 'OTHERLOCTYPE'
    XPTR = 'XPTR'
    STRUCT_ID = 'STRUCTID'
    BTYPE = 'BTYPE'
    USE = 'USE'
    VERSDATE = 'VERSDATE'
    STREAM_TYPE = 'streamType'
    OWNER_ID = 'OWNERID'
    DMDID = 'DMDID'
    BEGIN = 'BEGIN'
    END = 'END'
    BETYPE = 'BETYPE'
    ARCLINK_ORDER = 'ARCLINKORDER'
    TRANSFORM_TYPE = 'TRANSFORMTYPE'
    TRANSFORM_ALGORITHM = 'TRANSFORMALGORITHM'
    TRANSFORM_KEY = 'TRANSFORMKEY'
    TRANSFORM_BEHAVIOR = 'TRANSFORMBEHAVIOR'
    TRANSFORM_ORDER = 'TRANSFORMORDER'
    SEQUENCE = 'SEQ'
    ARCTYPE = 'ARCTYPE'
    CONTENT_IDS = 'CONTENTIDS'
    ORDER = 'ORDER'
    ORDER_LABEL = 'ORDERLABEL'
    FILE_ID = 'FILEID'
    SHAPE = 'SHAPE'
    COORDS = 'COORDS'
    EXTENT = 'EXTENT'
    EXTENT_TYPE = 'EXTTYPE'


class AgentRoles(METSEnum):
    CREATOR = 'CREATOR'
    EDITOR = 'EDITOR'
    ARCHIVIST = 'ARCHIVIST'
    PRESERVATION = 'PRESERVATION'
    DISSEMINATOR = 'DISSEMINATOR'
    CUSTODIAN = 'CUSTODIAN'
    IPOWNER = 'IPOWNER'
    OTHER = 'OTHER'


class AgentTypes(METSEnum):
    INDIVIDUAL = 'INDIVIDUAL'
    ORGANIZATION = 'ORGANIZATION'
    OTHER = 'OTHER'


class MetadataTypes(METSEnum):
    MARC = 'MARC'
    MODS = 'MODS'
    EAD = 'EAD'
    DC = 'DC'
    NISOIMG = 'NISOIMG'
    LC_AV = 'LC-AV'
    VRA = 'VRA'
    TEIHDR = 'TEIHDR'
    DDI = 'DDI'
    FGDC = 'FGDC'
    LOM = 'LOM'
    PREMIS = 'PREMIS'
    PREMIS_OBJECT = 'PREMIS:OBJECT'
    PREMIS_AGENT = 'PREMIS:AGENT'
    PREMIS_RIGHTS = 'PREMIS:RIGHTS'
    PREMIS_EVENT = 'PREMIS:EVENT'
    TEXTMD = 'TEXTMD'
    METSRIGHTS = 'METSRIGHTS'
    ISO_19115_2003_NAP = 'ISO 19115:2003 NAP'
    EAC_CPF = 'EAC-CPF'
    LIDO = 'LIDO'
    OTHER = 'OTHER'


class LocatorTypes(METSEnum):
    ARK = 'ARK'
    URN = 'URN'
    URL = 'URL'
    PURL = 'PURL'
    HANDLE = 'HANDLE'
    DOI = 'DOI'
    OTHER = 'OTHER'


class ChecksumTypes(METSEnum):
    Adler_32 = 'Adler-32'
    CRC32 = 'CRC32'
    HAVAL = 'HAVAL'
    MD5 = 'MD5'
    MNP = 'MNP'
    SHA_1 = 'SHA-1'
    SHA_256 = 'SHA-256'
    SHA_384 = 'SHA-384'
    SHA_512 = 'SHA-512'
    TIGER = 'TIGER'
    WHIRLPOOL = 'WHIRLPOOL'


class XlinkAttributes(METSEnum):
    HREF = etree.QName(NAMESPACES['xlink'], 'href')
    ROLE = etree.QName(NAMESPACES['xlink'], 'role')
    ARCROLE = etree.QName(NAMESPACES['xlink'], 'arcrole')
    TITLE = etree.QName(NAMESPACES['xlink'], 'title')
    SHOW = etree.QName(NAMESPACES['xlink'], 'show')
    ACTUATE = etree.QName(NAMESPACES['xlink'], 'actuate')
    TO = etree.QName(NAMESPACES['xlink'], 'to')
    FROM = etree.QName(NAMESPACES['xlink'], 'from')
    LABEL = etree.QName(NAMESPACES['xlink'], 'label')


class XlinkTypes(METSEnum):
    SIMPLE = 'simple'
    EXTENDED = 'extended'
    LOCATOR = 'locator'
    ARC = 'arc'
    RESOURCE = 'resource'
    TITLE = 'title'
    EMPTY = 'none'


class XlinkShowTypes(METSEnum):
    NEW = 'new'
    REPLACE = 'replace'
    EMBED = 'embed'
    OTHER = 'other'
    NONE = 'none'


class XlinkActuateTypes(METSEnum):
    ONLOAD = 'onLoad'
    ONREQUEST = 'onRequest'
    OTHER = 'other'
    NONE = 'none'


class FileBeginEndTypes(METSEnum):
    BYTE = 'BYTE'


class AreaBeginEndTypes(METSEnum):
    BYTE = 'BYTE'
    IDREF = 'IDREF'
    SMIL = 'SMIL'
    MIDI = 'MIDI'
    SMPTE25 = 'SMPTE-25'
    SMPTE24 = 'SMPTE-24'
    SMPTE_DF30 = 'SMPTE-DF30'
    SMPTE_NDF30 = 'SMPTE-NDF30'
    SMPTE_DF29 = 'SMPTE-DF29.97'
    SMPTE_NDF29 = 'SMPTE-NDF29.97'
    TIME = 'TIME'
    TCF = 'TCF'
    XPTR = 'XPTR'


class TransformTypes(METSEnum):
    DECOMPRESSION = 'decompression'
    DECRYPTION = 'decryption'


class ArclinkOrderTypes(METSEnum):
    ORDERED = 'ordered'
    UNORDERED = 'unordered'


class ExtentTypes(METSEnum):
    BYTE = 'BYTE'
    SMIL = 'SMIL'
    MIDI = 'MIDI'
    SMPTE25 = 'SMPTE-25'
    SMPTE24 = 'SMPTE-24'
    SMPTE_DF30 = 'SMPTE-DF30'
    SMPTE_NDF30 = 'SMPTE-NDF30'
    SMPTE_DF29 = 'SMPTE-DF29.97'
    SMPTE_NDF29 = 'SMPTE-NDF29.97'
    TIME = 'TIME'
    TCF = 'TCF'


class ShapeTypes(METSEnum):
    RECTANGLE = 'RECT'
    CIRCLE = 'CIRCLE'
    POLYGON = 'POLY'
