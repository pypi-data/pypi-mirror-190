# contains all variable strings that is used in mets gui

from enum import Enum

# noinspection PyUnresolvedReferences
import educelab.mets_gui.resources
from educelab import mets


# defines names for individual tabs
class TabNames(Enum):
    STRUCTURE = 'Structure'
    FILES = 'Files'
    HEADER = 'METS Header'
    METADATA = 'Metadata'
    METS = 'METS Document'
    BEHAVIOUR = 'Behaviour'
    LINKS = 'Links'


# defines shortcut key combinations
class Shortcuts(Enum):
    OPEN = 'Ctrl+O'
    EXIT = 'Ctrl+Q'
    SAVE = 'Ctrl+S'


# defines types of error messages used by gui
class MessageTypes(Enum):
    ERROR = 'error'
    INFO = 'info'


# defines types of separator lines used by gui
class SeparatorTypes(Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


# defines text to be used in button labels
class ButtonText(Enum):
    FILE = 'File'
    EDIT = 'Edit'
    HELP = 'Help'
    OPEN = 'Open'
    SAVE = 'Save'
    EXIT = 'Exit'
    ABOUT = 'About'
    ADD = 'Add'
    REMOVE = 'Remove'
    UP = 'Move up'
    DOWN = 'Move down'
    ADD_CHILD = 'Add child element'


# defines text to be used in gui labels
class Labels(Enum):
    OPEN_FILE = 'Open File'
    CONFIRMATION = 'Confirmation'
    QUIT_QUESTION = 'Are you sure you want to quit? Unsaved data will be lost.'
    STRUCT_MAP = 'Structural Maps'
    STRUCT_MAP_TREE = 'Structural Map View'
    BEHAVIOUR_SECTION = 'Behaviour Section'
    BEHAVIOUR_SECTION_VIEW = 'Behaviour Section View'
    APP_TITLE = 'METS Editor'
    DIALOG_ADD_STRUCT_MAP = 'Add Structural Map'
    DIALOG_EDIT_STRUCT_MAP = 'Edit Structural Map'
    DIALOG_ADD_STRUCT_MAP_ELEMENT = 'Add Map Element'
    DIALOG_EDIT_STRUCT_MAP_ELEMENT = 'Edit Map Element'
    DIALOG_ADD_AGENT = 'Add Agent'
    DIALOG_EDIT_AGENT = 'Edit Agent'
    DIALOG_ADD_NOTE = 'Add Note'
    DIALOG_EDIT_NOTE = 'Edit Note'
    DIALOG_ADD_ALT_ID = 'Add Alternative ID'
    DIALOG_EDIT_ALT_ID = 'Edit Alternative ID'
    DIALOG_ADD_FILE_SEC = 'Add File Section'
    DIALOG_EDIT_FILE_SEC = 'Edit File Section'
    DIALOG_ADD_FILE_SEC_ELEMENT = 'Add File Section Element'
    DIALOG_EDIT_FILE_SEC_ELEMENT = 'Edit File Section Element'
    DIALOG_ADD_METADATA_SEC = 'Add Metadata Section'
    DIALOG_EDIT_METADATA_SEC = 'Edit Metadata Section'
    DIALOG_ADD_DMD_ELEMENT = 'Add Metadata Element'
    DIALOG_EDIT_DMD_ELEMENT = 'Edit Metadata Element'
    DIALOG_ADD_AMD_ELEMENT = 'Add Administrative Metadata Element'
    DIALOG_EDIT_AMD_ELEMENT = 'Edit Administrative Metadata Element'
    DIALOG_ADD_STRUCT_LINK = 'Add Structural Link'
    DIALOG_EDIT_STRUCT_LINK = 'Edit Structural Link'
    DIALOG_ADD_NAMESPACE = 'Add XML Namespace'
    DIALOG_EDIT_NAMESPACE = 'Edit XML Namespace'
    DIALOG_ADD_OTHER_ATTRIB = 'Add Other Attribute'
    DIALOG_EDIT_OTHER_ATTRIB = 'Edit Other Attribute'
    DIALOG_ADD_BEHAVIOUR_ELEMENT = 'Add Behaviour Element'
    DIALOG_EDIT_BEHAVIOUR_ELEMENT = 'Edit Behaviour Element'
    ELEMENT_TYPE = 'Element Type'
    TAG = 'Tag'
    AGENT = 'Agents'
    ALT_RECORD_ID = 'Alternative Record IDs'
    LEAVE_EMPTY = 'Leave Empty'
    VALUE = 'Value'
    EMPTY_REQUIRED_FIELD = 'Required field is empty.'
    WARNING = 'Warning'
    ERROR = 'Error'
    FILE_SEC = 'File Section'
    FILE_SEC_TREE = 'File Section View'
    CONTENT = 'Content'
    METADATA_SECTIONS = 'Metadata Sections'
    METADATA_SECTION_TYPE = 'Metadata Section Type'
    DMD_ELEMENTS = 'Descriptive Metadata Elements'
    AMD_ELEMENTS = 'Administrative Metadata Elements'
    XML_NAMESPACE_WARNING = 'Any namespaces used in XML should be declared in the %s tab' % TabNames.METS.value
    METS = 'METS Document Data'
    HEADER = 'Header'
    STRUCT_LINK_SEC = 'Structural Link Section'
    STRUCT_LINK_ELEMENTS = 'Structural Link Elements'
    GENERIC_TAG = '<%s> %s'
    STRUCT_GROUP_WARNING = 'Warning: Every Structural Group Element must contain at least one Arc Link and two ' \
                           'Locator Links '
    DUPLICATE_ID_WARNING = 'ID value already exists within the document.'
    NAMESPACES = 'XML Namespaces'
    OTHER_ATTRIBS = 'Other Attributes'
    FILE_OPEN_ERROR = 'Could not open file.'
    ABOUT = 'About'
    INFO = 'Info'
    ABOUT_TEXT = 'Created as a part of the Living Virtually project.\n' \
                 f'Supported METS Schema version: {mets.METS_SCHEMA_VERSION}'
    CHECKBOX_ENABLE = 'Use Element'
    INTERFACE_DEFINITION = 'Behaviour Interface'
    MECHANISM = 'Behaviour Mechanism'
    BEHAVIOUR_WARNING = 'Every Behaviour Element must contain one Mechanism Element'
    SAVE_SUCCESSFUL = 'File successfully saved.'


# defines text to be used in error message popups
class ErrorMessages(Enum):
    STRUCT_MAP_MISSING = 'At least one Structural Map must exist in METS File'
    STRUCT_MAP_ELEMENT_MISSING = 'At least one Division must be present in a Structural Map'


# defines paths to graphical resources of the gui
class Resources(Enum):
    ICON_APP = ':/res/icon_app'
    ICON_ADD = ':/res/icon_add'
    ICON_REMOVE = ':/res/icon_remove'
    ICON_EDIT = ':/res/icon_edit'
    ICON_CHILD_ADD = ':/res/icon_child_add'
    ICON_INFO = ':/res/icon_info'


# defines text to be used in tooltip bar at the bottom of the gui
class ButtonTooltips(Enum):
    OPEN = 'Open File'
    SAVE = 'Save data into an XML file'
    EXIT = 'Exit application'


# defines internal input types of the gui app
# classes are defined in utils.py
class InputTypes(Enum):
    LINE_EDIT = 'InputLine'
    COMBO_BOX = 'InputChoice'
    DATE_TIME = 'InputDateTime'
    TEXT_EDIT = 'InputText'
    LIST = 'InputList'


# defines names of structural map elements for use as labels/ids
# TODO: switch to educelab.mets definitions
class StructMapElements(Enum):
    DIV = 'Division'
    MPTR = 'METS Pointer'
    FPTR = 'File Pointer'
    AREA = 'Area'
    SEQ = 'Sequence of Files'
    PAR = 'Paralel Files'


# defines names of file section elements for use as labels/ids
# TODO: switch to educelab.mets definitions
class FileSecElements(Enum):
    FILE_GROUP = 'File Group'
    FILE = 'File'
    FILE_LOCATION = 'File Location'
    FILE_CONTENT = 'File Content'
    STREAM = 'Component Byte Stream'
    TRANSFORM_FILE = 'Transform File'


# defines xml labels for all mets elements
# TODO: switch to educelab.mets definitions
class ElementTags(Enum):
    STRUCT_MAP = 'structMap'
    DIV = 'div'
    MPTR = 'mptr'
    FPTR = 'fptr'
    AREA = 'area'
    SEQ = 'seq'
    PAR = 'par'
    AGENT = 'agent'
    NOTE = 'note'
    ALT_RECORD_ID = 'altRecordID'
    FILE_SEC = 'fileSec'
    FILE_GROUP = 'fileGrp'
    FILE = 'file'
    FILE_LOCATION = 'FLocat'
    FILE_CONTENT = 'FContent'
    STREAM = 'stream'
    TRANSFORM_FILE = 'transformFile'
    DMD_SEC = 'dmdSec'
    AMD_SEC = 'amdSec'
    MD_REF = 'mdRef'
    MD_WRAP = 'mdWrap'
    TECH_MD = 'techMD'
    RIGHTS_MD = 'rightsMD'
    SOURCE_MD = 'sourceMD'
    DIGIPROV_MD = 'digiprovMD'
    STRUCT_LINK = 'smLink'
    STRUCT_LINK_GROUP = 'smLinkGrp'
    LOCATOR_LINK = 'smLocatorLink'
    ARC_LINK = 'smArcLink'
    METS_DOCUMENT_ID = 'metsDocumentID'
    BEHAVIOUR_SEC = 'behaviorSec'
    BEHAVIOUR = 'behavior'
    INTERFACE_DEFINITION = 'interfaceDef'
    MECHANISM = 'mechanism'


# defines names of data content elements for use as labels/ids
# TODO: switch to educelab.mets definitions
class DataContentTypes(Enum):
    XML = 'XML data'
    BIN = 'Base64 encoded data'


# defines names of metadata elements for use as labels/ids
# TODO: switch to educelab.mets definitions
class MetadataSectionTypes(Enum):
    DMD_SEC = 'Descriptive metadata'
    AMD_SEC = 'Administrative metadata'


# defines names of descriptive metadata elements for use as labels/ids
# TODO: switch to educelab.mets definitions
class DescriptiveMetadataTypes(Enum):
    MD_REF = 'Reference'
    MD_WRAP = 'Wrapper'


# defines names of structural link elements for use as labels/ids
# TODO: switch to educelab.mets definitions
class StructuralLinkTypes(Enum):
    STRUCT_LINK = 'Structural Link'
    STRUCT_LINK_GROUP = 'Structural Link Group'
    LOCATOR_LINK = 'Locator Link'
    ARC_LINK = 'Arc Link'


# defines names of administrative metadata elements for use as labels/ids
# TODO: switch to educelab.mets definitions
class AdministrativeMetadataTypes(Enum):
    TECH_MD = 'Technical Metadata'
    RIGHTS_MD = 'Intellectual Property Rights Metadata'
    SOURCE_MD = 'Source Metadata'
    DIGIPROV_MD = 'Digital Provenance Metadata'


# defines names of behaviour elements for use as labels/ids
# TODO: switch to educelab.mets definitions
class BehaviourTypes(Enum):
    BEHAVIOUR_SEC = 'Behaviour Section'
    BEHAVIOUR = 'Behaviour'
    INTERFACE_DEFINITION = 'Interface'
    MECHANISM = 'Mechanism'


# defines names of all mets attributes for use as labels/ids
# TODO: switch to educelab.mets definitions
class Attributes(Enum):
    ID = 'ID'
    TYPE = 'Type'
    LABEL = 'Label'
    DMDID = 'Desc. Metadata ID'
    ADMID = 'Adm. Metadata ID'
    ORDER = 'Order'
    ORDER_LABEL = 'Order Label'
    CONTENT_IDS = 'Content IDs'
    XLINK_LABEL = 'Xlink Label'
    FILE_ID = 'File ID'
    LOCTYPE = 'Locator Type'
    OTHER_LOCTYPE = 'Other Locator Type'
    XLINK_HREF = 'URI Link'
    XLINK_ROLE = 'Link Role'
    XLINK_ARCROLE = 'Link Arcrole'
    XLINK_TITLE = 'Link Title'
    XLINK_SHOW = 'Link Behaviour'
    XLINK_ACTUATE = 'Link Actuation'
    XLINK_TO = 'Link to'
    XLINK_FROM = 'Link from'
    SHAPE = 'Shape'
    COORDS = 'Coordinates'
    BEGIN = 'Content Begin'
    END = 'Content End'
    BETYPE = 'Begin/End Type'
    EXTEND = 'Extend'
    EXT_TYPE = 'Extend Type'
    CREATE_DATE = 'Created'
    LAST_MOD_DATE = 'Last Modified'
    RECORD_STATUS = 'Record Status'
    ROLE = 'Role'
    OTHER_ROLE = 'Other Role'
    OTHER_TYPE = 'Other Type'
    NAME = 'Name'
    NOTE = 'Note'
    METS_DOCUMENT_ID = 'METS Document ID'
    USE = 'Use'
    VERSDATE = 'Version Date'
    TRANSFORM_TYPE = 'Transform Type'
    TRANSFORM_ALGORITHM = 'Transform Algorithm'
    TRANSFORM_KEY = 'Transform Key'
    TRANSFORM_BEHAVIOR = 'Transform Behavior'
    TRANSFORM_ORDER = 'Transform Order'
    STREAM_TYPE = 'Stream Type'
    OWNER_ID = 'Owner ID'
    SEQ = 'Sequence'
    MIMETYPE = 'MIME Type'
    SIZE = 'Size'
    CREATED = 'Created'
    CHECKSUM = 'Checksum'
    CHECKSUM_TYPE = 'Checksum Type'
    GROUP_ID = 'Group ID'
    STATUS = 'Status'
    MD_TYPE = 'Metadata Type'
    MD_TYPE_OTHER = 'Other Metadata Type'
    MD_TYPE_VERSION = 'Metadata Type Version'
    XPTR = 'XPointer Reference'
    OBJID = 'Object ID'
    PROFILE = 'Profile'
    ARCLINK_ORDER = 'ArcLink Order'
    LOCATOR_LINK = 'Locator Link'
    ARC_LINK = 'Arc Link'
    XLINK_TYPE = 'Link Type'
    ARC_TYPE = 'Arc Type'
    BTYPE = 'Behavior type'
    STRUCTID = 'Structure ID'


# text of tooltips shown for all attributes available in gui
# taken from mets schema annotations
class AttributeTooltips(Enum):
    ID = 'This attribute uniquely identifies the element within the METS document, and would allow the element to be ' \
         'referenced unambiguously from another element or document via an IDREF or an XPTR.'
    OBJID = 'Is the primary identifier assigned to the METS object as a whole. Although this attribute is not ' \
            'required, it is strongly recommended. This identifier is used to tag the entire METS object to external ' \
            'systems, in contrast with the ID identifier. '
    METS_LABEL = 'Is a simple title string used to identify the object/entity being described in the METS document ' \
                 'for the user. '
    TYPE = 'Specifies the class or type of the object, e.g.: book, journal, stereograph, dataset, video, etc.'
    ADMID = 'Contains the ID attribute values of the <techMD>, <sourceMD>, <rightsMD> and/or <digiprovMD> ' \
            'elements within the <amdSec> of the METS document that contain administrative metadata pertaining ' \
            'to the METS document itself.'
    PROFILE = 'Indicates to which of the registered profile(s) the METS document conforms.'
    CREATE_DATE = 'Records the date/time the METS document was created.'
    LAST_MOD_DATE = 'Is used to indicate the date/time the METS document was last modified.'
    RECORD_STATUS = 'Specifies the status of the METS document. It is used for internal processing purposes.'
    VERSDATE = 'An optional dateTime attribute specifying the date this version/fileGrp of the digital object was ' \
               'created. '
    STRUCT_MAP_LABEL = 'Describes the <structMap> to viewers of the METS document. This would be useful ' \
                       'primarily where more than one <structMap> is provided for a single object. A ' \
                       'descriptive LABEL value, in that case, could clarify to users the purpose of each of the ' \
                       'available structMaps. '
    USE = 'A tagging attribute to indicate the intended use of files within this file group (e.g., master, ' \
          'reference, thumbnails for image files). A USE attribute can be expressed at the&lt;fileGrp&gt; level, ' \
          'the &lt;file&gt; level, the &lt;FLocat&gt; level and/or the &lt;FContent&gt; level.  A USE attribute ' \
          'value at the &lt;fileGrp&gt; level should pertain to all of the files in the &lt;fileGrp&gt;.  A USE ' \
          'attribute at the &lt;file&gt; level should pertain to all copies of the file as represented by ' \
          'subsidiary &lt;FLocat&gt; and/or &lt;FContent&gt; elements.  A USE attribute at the &lt;FLocat&gt; or ' \
          '&lt;FContent&gt; level pertains to the particular copy of the file that is either referenced (' \
          '&lt;FLocat&gt;) or wrapped (&lt;FContent&gt;). '
    CONTENT_IDS = 'Content IDs for the content represented by the &lt;div&gt; (equivalent to DIDL DII or Digital ' \
                  'Item Identifier, a unique external ID). '
    DMDID = 'Contains the ID attribute values identifying the &lt;dmdSec&gt;, elements in the METS document that ' \
            'contain or link to descriptive metadata pertaining to the structural division represented by the ' \
            'current &lt;div&gt; element.'
    ORDER = "A representation of the element's order among its siblings (e.g., its absolute, numeric sequence). " \
            "For an example, and clarification of the distinction between ORDER and ORDERLABEL, " \
            "see the description of the ORDERLABEL attribute. "
    ORDER_LABEL = "A representation of the element's order among its siblings (e.g., “xii”), or of any " \
                  "non-integer native numbering system. It is presumed that this value will still be machine " \
                  "actionable (e.g., it would support ‘go to page ___’ function), and it should not be used as a " \
                  "replacement/substitute for the LABEL attribute. To understand the differences between ORDER, " \
                  "ORDERLABEL and LABEL, imagine a text with 10 roman numbered pages followed by 10 arabic " \
                  "numbered pages. Page iii would have an ORDER of “3”, an ORDERLABEL of “iii” and a LABEL of " \
                  "“Page iii”, while page 3 would have an ORDER of “13”, an ORDERLABEL of “3” and a LABEL of “Page 3”."
    DIV_LABEL = 'An attribute used, for example, to identify a &lt;div&gt; to an end user viewing the document. ' \
                'Thus a hierarchical arrangement of the &lt;div&gt; LABEL values could provide a table of ' \
                'contents to the digital content represented by a METS document and facilitate the users’ ' \
                'navigation of the digital object. Note that a &lt;div&gt; LABEL should be specific to its level ' \
                'in the structural map. In the case of a book with chapters, the book &lt;div&gt; LABEL should ' \
                'have the book title and the chapter &lt;div&gt;; LABELs should have the individual chapter ' \
                'titles, rather than having the chapter &lt;div&gt; LABELs combine both book title and chapter ' \
                'title . For further of the distinction between LABEL and ORDERLABEL see the description of the ' \
                'ORDERLABEL attribute. '
    XLINK_LABEL = 'An xlink label to be referred to by an smLink element'
    XLINK_HREF = 'This attribute gives the URI of where the METS document represented by the <mptr> is located. The ' \
                 'xlink:href should always be present in this context if the <mptr> is t o have any meaning or use. '
    XLINK_ROLE = 'An attribute that serves a semantic purpose. If present, it specifies the URI of a resource that ' \
                 'describes the role or function of the xlink:href link. This attribute is defined as part of the ' \
                 'xlink:simpleLink attribute group. It must be referenced as defined in IETF RFC 2396, except that, ' \
                 'if the URI except that, if the URI scheme used is allowed to have absolute and relative forms, ' \
                 'the URI portion must be absolute. '
    XLINK_ARCROLE = 'An attribute that serves a semantic purpose. If present it specifies the URI of a resource that ' \
                    'describes the pertinent arcrole. While more likely to be used in arcLinks than simpleLinks, ' \
                    'this attribute is nonetheless defined as part of the xlink:simpleLink attribute group. This URI ' \
                    'reference i s defined in IETF RFC 2396, except if the URI scheme used is allowed to have ' \
                    'absolute and relative forms, the URI portion must be absolute. '
    XLINK_TITLE = 'An attribute that serves a semantic purpose. It is used to describe the meaning of a link or ' \
                  'resource in a human readable fashion. '
    XLINK_SHOW = 'An attribute that specifies behavior within a simpleLink. It signals behavior intentions for ' \
                 'traversal to the simpleLink’s single remote ending resource.'
    XLINK_ACTUATE = 'An attribute that specifies behavior. Within a simpleLin k it signals behavior intentions for ' \
                    'traversal to the simpleLink’s single remote ending resource.'
    XLINK_TO = 'The value of the label for the element in the structMap you are linking to.'
    XLINK_FROM = 'The value of the label for the element in the structMap you are linking from.'
    FILE_ID = 'An optional attribute that provides the XML ID identifying the &lt;file&gt; element that links to ' \
              'and/or contains the digital content represented by the &lt;fptr&gt;. A &lt;fptr&gt; element should ' \
              'only have a FILEID attribute value if it does not have a child &lt;area&gt;, &lt;par&gt; or ' \
              '&lt;seq&gt; element. If it has a child element, then the responsibility for pointing to the relevant ' \
              'content falls to this child element or its descendants. '
    LOCTYPE = 'Specifies the locator type used in the link attribute.'
    OTHER_LOCTYPE = 'Specifies the locator type when the value OTHER is used in the LOCTYPE attribute. Although ' \
                    'optional, it is strongly recommended when OTHER is used. '
    SHAPE = 'An attribute that can be used as in HTML to define the shape of the relevant area within the content ' \
            'file pointed to by the <area> element. Typically this would be used with image content (still image or ' \
            'video frame) w hen only a portion of an integral image map pertains. If SHAPE is specified then COORDS ' \
            'must also be present (see below). SHAPE should be used in conjunction with COORDS in the manner defined ' \
            'for the shape and coords attributes on an HTML4 <area> element . SHAPE must contain one of the following ' \
            'values: RECT, CIRCLE, POLY '
    COORDS = 'Specifies the coordinates in an image map for the shape of the pertinent area as specified in the SHAPE ' \
             'attribute. While technically optional, SHAPE and COORDS must both appear together to define the ' \
             'relevant area of image content. COORDS should be used in conjunction with SHAPE in the manner defined ' \
             'for the COORDs and SHAPE attributes on an HTML4 &lt;area&gt; element. COORDS must be a comma delimited ' \
             'string of integer value pairs representing coordinates (plus radius in the case of CIRCLE) within an ' \
             'image map. Number of coordinates pairs depends on shape: RECT: x1, y1, x2, y2; CIRC: x1, y1; POLY: x1, ' \
             'y1, x2, y2, x3, y3 . . . '
    BEGIN = 'An attribute that specifies the point in the content file where the relevant section of content begins. ' \
            'It can be used in conjunction with either the END attribute or the EXTENT attribute as a means of ' \
            'defining the relevant portion of the referenced file precisely. It can only be interpreted meaningfully ' \
            'in conjunction with the BETYPE or EXTTYPE, which specify the kind of beginning/ending point values or ' \
            'beginning/extent values that are being used. The BEGIN attribute can be used with or without a companion ' \
            'END or EXTENT element. In this case, the end of the content file is assumed to be the end point. '
    END = 'An attribute that specifies the point in the content file where the relevant section of content ends. It ' \
          'can only be interpreted meaningfully in conjunction with the BETYPE, which specifies the kind of ending ' \
          'point values being used. Typically the END attribute would only appear in conjunction with a BEGIN element. '
    BETYPE = 'An attribute that specifies the kind of BEGIN and/or END values that are being used. For example, ' \
             'if BYTE is specified, then the BEGIN and END point values represent the byte offsets into a file. If ' \
             'IDREF is specified, then the BEGIN element specifies the ID value that identifies the element in a ' \
             'structured text file where the relevant section of the file begins; and the END value (if present) ' \
             'would specify the ID value that identifies the element with which the relevant section of the file ends. '
    EXTEND = 'An attribute that specifies the extent of the relevant section of the content file. Can only be ' \
             'interpreted meaningfully in conjunction with the EXTTYPE which specifies the kind of value that is ' \
             'being used. Typically the EXTENT attribute would only appear in conjunction with a BEGIN element and ' \
             'would not be used if the BEGIN point represents an IDREF. '
    EXT_TYPE = 'An attribute that specifies the kind of EXTENT values that are being used. For example if BYTE is ' \
               'specified then EXTENT would represent a byte count. If TIME is specified the EXTENT would represent a ' \
               'duration of time. '
    ROLE = 'Specifies the function of the agent with respect to the METS record.'
    OTHER_ROLE = 'Denotes a role not contained in the allowed values set if OTHER is indicated in the ROLE attribute.'
    AGENT_TYPE = 'Is used to specify the type of AGENT.'
    AGENT_OTHER_TYPE = 'Specifies the type of agent when the value OTHER is indicated in the TYPE attribute.'
    IDENTIFIER_TYPE = 'A description of the identifier type.'
    DIV_TYPE = 'An attribute that specifies the type of structural division that the &lt;div&gt; element represents. ' \
               'Possible &lt;div&gt; TYPE attribute values include: chapter, article, page, track, segment, ' \
               'section etc. METS places no constraints on the possible TYPE values. Suggestions for controlled ' \
               'vocabularies for TYPE may be found on the METS website. '
    STRUCT_MAP_TYPE = 'Identifies the type of structure represented by the &lt;structMap&gt;. For example, ' \
                      'a &lt;structMap&gt; that represented a purely logical or intellectual structure could be ' \
                      'assigned a TYPE value of “logical” whereas a &lt;structMap&gt; that represented a purely ' \
                      'physical structure could be assigned a TYPE value of “physical”. However, the METS schema ' \
                      'neither defines nor requires a common vocabulary for this attribute. A METS profile, however, ' \
                      'may well constrain the values for the &lt;structMap&gt; TYPE. '
    FCONTENT_USE = 'A tagging attribute to indicate the intended use of the specific copy of the file represented by ' \
                   'the &lt;FContent&gt; element (e.g., service master, archive master). A USE attribute can be ' \
                   'expressed at the&lt;fileGrp&gt; level, the &lt;file&gt; level, the &lt;FLocat&gt; level and/or ' \
                   'the &lt;FContent&gt; level.  A USE attribute value at the &lt;fileGrp&gt; level should pertain to ' \
                   'all of the files in the &lt;fileGrp&gt;.  A USE attribute at the &lt;file&gt; level should ' \
                   'pertain to all copies of the file as represented by subsidiary &lt;FLocat&gt; and/or ' \
                   '&lt;FContent&gt; elements.  A USE attribute at the &lt;FLocat&gt; or &lt;FContent&gt; level ' \
                   'pertains to the particular copy of the file that is either referenced (&lt;FLocat&gt;) or wrapped ' \
                   '(&lt;FContent&gt;). '
    TRANSFORM_TYPE = 'Is used to indicate the type of transformation needed to render content of a file accessible. ' \
                     'This may include unpacking a file into subsidiary files/streams. The controlled value ' \
                     'constraints for this XML string include “decompression” and “decryption”. Decompression is ' \
                     'defined as the action of reversing data compression, i.e., the process of encoding information ' \
                     'using fewer bits than an unencoded representation would use by means of specific encoding ' \
                     'schemas. Decryption is defined as the process of restoring data that has been obscured to make ' \
                     'it unreadable without special knowledge (encrypted data) to its original form. '
    TRANSFORM_ALGORITHM = 'Specifies the decompression or decryption routine used to access the contents of the file. ' \
                          'Algorithms for compression can be either loss-less or lossy. '
    TRANSFORM_KEY = 'A key to be used with the transform algorithm for accessing the file’s contents.'
    TRANSFORM_BEHAVIOR = 'An IDREF to a behavior element for this transformation.'
    TRANSFORM_ORDER = 'The order in which the instructions must be followed in order to unpack or transform the ' \
                      'container file. Signified by a positive integer.'
    STREAM_TYPE = 'The IANA MIME media type for the bytestream.'
    OWNER_ID = 'Used to provide a unique identifier (which could include a URI) assigned to the file. This identifier ' \
               'may differ from the URI used to retrieve the file. '
    ID_FILE = 'This attribute uniquely identifies the element within the METS document, and would allow the element ' \
              'to be referenced unambiguously from another element or document via an IDREF or an XPTR. Typically, ' \
              'the ID attribute value on a &lt;file&gt; element would be referenced from one or more FILEID ' \
              'attributes (which are of type IDREF) on &lt;fptr&gt;and/or &lt;area&gt; elements within the ' \
              '&lt;structMap&gt;.  Such references establish links between  structural divisions (&lt;div&gt; ' \
              'elements) and the specific content files or parts of content files that manifest them. '
    SEQ = 'Indicates the sequence of this &lt;file&gt; relative to the others in its &lt;fileGrp&gt;.'
    MIME_TYPE = 'The IANA MIME media type for the associated file or wrapped content. Some values for this attribute ' \
                'can be found on the IANA website. '
    SIZE = 'Specifies the size in bytes of the associated file or wrapped content.'
    CREATED = 'Specifies the date and time of creation for the associated file or wrapped content.'
    CHECKSUM = 'Provides a checksum value for the associated file or wrapped content.'
    CHECKSUM_TYPE = 'Specifies the checksum algorithm used to produce the value contained in the CHECKSUM attribute.'
    GROUP_ID = 'An identifier that establishes a correspondence between this file and files in other file groups. ' \
               'Typically, this will be used to associate a master file in one file group with the derivative files ' \
               'made from it in other file groups. '
    DMD_SEC_ID = 'This attribute uniquely identifies the element within the METS document, and would allow the ' \
                 'element to be referenced unambiguously from another element or document via an IDREF or an XPTR. ' \
                 'The ID attribute on the &lt;dmdSec&gt;, &lt;techMD&gt;, &lt;sourceMD&gt;, &lt;rightsMD&gt; and ' \
                 '&lt;digiprovMD&gt; elements (which are all of mdSecType) is required, and its value should be ' \
                 'referenced from one or more DMDID attributes (when the ID identifies a &lt;dmdSec&gt; element) or ' \
                 'ADMID attributes (when the ID identifies a &lt;techMD&gt;, &lt;sourceMD&gt;, &lt;rightsMD&gt; or ' \
                 '&lt;digiprovMD&gt; element) that are associated with other elements in the METS document. The ' \
                 'following elements support references to a &lt;dmdSec&gt; via a DMDID attribute: &lt;file&gt;, ' \
                 '&lt;stream&gt;, &lt;div&gt;.  The following elements support references to &lt;techMD&gt;, ' \
                 '&lt;sourceMD&gt;, &lt;rightsMD&gt; and &lt;digiprovMD&gt; elements via an ADMID attribute: ' \
                 '&lt;metsHdr&gt;, &lt;dmdSec&gt;, &lt;techMD&gt;, &lt;sourceMD&gt;, &lt;rightsMD&gt;, ' \
                 '&lt;digiprovMD&gt;, &lt;fileGrp&gt;, &lt;file&gt;, &lt;stream&gt;, &lt;div&gt;, &lt;area&gt;, ' \
                 '&lt;behavior&gt;.'
    GROUP_ID_METADATA = 'This identifier is used to indicate that different metadata sections may be considered as ' \
                        'part of a group. Two metadata sections with the same GROUPID value are to be considered part ' \
                        'of the same group. For example this facility might be used to group changed versions of the ' \
                        'same metadata if previous versions are maintained in a file for tracking purposes. '
    ADMID_DMD_SEC = 'Contains the ID attribute values of the &lt;digiprovMD&gt;, &lt;techMD&gt;, &lt;sourceMD&gt; ' \
                    'and/or &lt;rightsMD&gt; elements within the &lt;amdSec&gt; of the METS document that contain ' \
                    'administrative metadata pertaining to the current mdSecType element. Typically used in this ' \
                    'context to reference preservation metadata (digiprovMD) which applies to the current metadata. '
    CREATED_METADATA = 'Specifies the date and time of creation for the metadata.'
    STATUS = 'Indicates the status of this metadata (e.g., superseded, current, etc.).'
    MD_WRAP_LABEL = 'An optional string attribute providing a label to display to the viewer of the METS document ' \
                    'identifying the metadata. '
    MD_TYPE = 'Is used to indicate the type of the associated metadata.'
    MD_TYPE_OTHER = 'Specifies the form of metadata in use when the value OTHER is indicated in the MDTYPE attribute.'
    MD_TYPE_VERSION = 'Provides a means for recording the version of the type of metadata (as recorded in the MDTYPE ' \
                      'or OTHERMDTYPE attribute) that is being used.  This may represent the version of the ' \
                      'underlying data dictionary or metadata model rather than a schema version. '
    XPTR = 'Locates the point within a file to which the &lt;mdRef&gt; element refers, if applicable.'
    ARCLINK_ORDER = 'ARCLINKORDER is used to indicate whether the order of the smArcLink elements aggregated by the ' \
                    'smLinkGrp element is significant. If the order is significant, then a value of ' \
                    '&quot;ordered&quot; should be supplied.  Value defaults to &quot;unordered&quot; Note that the ' \
                    'ARLINKORDER attribute has no xlink specified meaning. '
    XLINK_TYPE = ''
    ARC_TYPE = 'The ARCTYPE attribute provides a means of specifying the relationship between the &lt;div&gt; ' \
               'elements participating in the arc link, and hence the purpose or role of the link.  While it can be ' \
               'considered analogous to the xlink:arcrole attribute, its type is a simple string, rather than anyURI. ' \
               ' ARCTYPE has no xlink specified meaning, and the xlink:arcrole attribute should be used instead of or ' \
               'in addition to the ARCTYPE attribute when full xlink compliance is desired with respect to specifying ' \
               'the role or purpose of the arc link. '
    OTHER_ATTRIBS = 'ANY attribute from ANY namespace OTHER than http://www.loc.gov/METS/'
    NAMESPACES = 'As permitted by the XML Schema Standard, the processContents attribute value for the metadata in an ' \
                 '<xmlData> is set to “lax”. Therefore, if the source schema and its location are identified by means ' \
                 'of ' \
                 'an XML schemaLocation attribute, then an XML processor will validate the elements for which it can ' \
                 'find declarations. If a source schema is not identified, or cannot be found at the specified ' \
                 'schemaLocation, then an XML validator will check for well-formedness, but otherwise skip over the ' \
                 'elements appearing in the <xmlData> element. '
    LABEL_BEHAVIOUR_SEC = 'A text description of the behavior section.'
    BTYPE = 'The behavior type provides a means of categorizing the related behavior.'
    STRUCTID = 'An XML IDREFS attribute used to link a &lt;behavior&gt;  to one or more &lt;div&gt; elements within a ' \
               '&lt;structMap&gt; in the METS document. The content to which the STRUCTID points is considered input ' \
               'to the executable behavior mechanism defined for the behavior.  If the &lt;behavior&gt; applies to ' \
               'one or more &lt;div&gt; elements, then the STRUCTID attribute must be present. '
    LABEL = 'A text description of the entity represented.'


# text of tooltips shown for all elements available in gui
# taken from mets schema annotations
class ElementTooltips(Enum):
    METS = 'METS is intended to provide a standardized XML format for transmission of complex digital library ' \
           'objects between systems.  As such, it can be seen as filling a role similar to that defined for the ' \
           'Submission Information Package (SIP), Archival Information Package (AIP) and Dissemination ' \
           'Information Package (DIP) in the Reference Model for an Open Archival Information System. The root ' \
           'element <mets> establishes the container for the information being stored and/or transmitted by the ' \
           'standard.'
    HEADER = 'The mets header element <metsHdr> captures metadata about the METS document itself, ' \
             'not the digital object the METS document encodes. Although it records a more limited set of ' \
             'metadata, it is very similar in function and purpose to the headers employed in other schema such ' \
             'as the Text Encoding Initiative (TEI) or in the Encoded Archival Description (EAD).'
    AGENT = 'The agent element <agent> provides for various parties and their roles with respect to the METS ' \
            'record to be documented.'
    ALT_RECORD_ID = 'The alternative record identifier element <altRecordID> allows one to use alternative ' \
                    'record identifier values for the digital object represented by the METS document; the ' \
                    'primary record identifier is stored in the OBJID attribute in the root <mets> element. '
    METS_DOCUMENT_ID = 'The metsDocument identifier element <metsDocumentID> allows a unique identifier to be ' \
                       'assigned to the METS document itself.  This may be different from the OBJID attribute ' \
                       'value in the root <mets> element, which uniquely identifies the entire digital object ' \
                       'represented by the METS document.'
    DMD_SEC = 'A descriptive metadata section <dmdSec> records descriptive metadata pertaining to the METS ' \
              'object as a whole or one of its components. The <dmdSec> element conforms to same generic ' \
              'datatype as the <techMD>, <rightsMD>, <sourceMD> and <digiprovMD> elements, and supports the same ' \
              'sub-elements and attributes. A descriptive metadata element can either wrap the metadata  (' \
              'mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <dmdSec> ' \
              'elements; and descriptive metadata can be associated with any METS element that supports a DMDID ' \
              'attribute.  Descriptive metadata can be expressed according to many current description standards ' \
              '(i.e., MARC, MODS, Dublin Core, TEI Header, EAD, VRA, FGDC, DDI) or a locally produced XML schema.'
    AMD_SEC = 'The administrative metadata section <amdSec> contains the administrative metadata pertaining to ' \
              'the digital object, its components and any original source material from which the digital object ' \
              'is derived. The <amdSec> is separated into four sub-sections that accommodate technical metadata ' \
              '(techMD), intellectual property rights (rightsMD), analog/digital source metadata (sourceMD), ' \
              'and digital provenance metadata (digiprovMD). Each of these subsections can either wrap the ' \
              'metadata  (mdWrap) or reference it in an external location (mdRef) or both. Multiple instances of ' \
              'the <amdSec> element can occur within a METS document and multiple instances of its subsections ' \
              'can occur in one <amdSec> element. This allows considerable flexibility in the structuring of the ' \
              'administrative metadata. METS does not define a vocabulary or syntax for encoding administrative ' \
              'metadata. Administrative metadata can be expressed within the amdSec sub-elements according to ' \
              'many current community defined standards, or locally produced XML schemas.'
    FILE_SEC = 'The overall purpose of the content file section element <fileSec> is to provide an inventory of ' \
               'and the location for the content files that comprise the digital object being described in the ' \
               'METS document.'
    FILE_GROUP = 'A sequence of file group elements <fileGrp> can be used group the digital files ' \
                 'comprising the content of a METS object either into a flat arrangement or, because each file ' \
                 'group element can itself contain one or more  file group elements,  into a nested (' \
                 'hierarchical) arrangement. In the case where the content files are images of different formats ' \
                 'and resolutions, for example, one could group the image content files by format and create a ' \
                 'separate <fileGrp> for each image format/resolution such as:\n-- one <fileGrp> ' \
                 'for the thumbnails of the images\n-- one <fileGrp> for the higher resolution JPEGs of ' \
                 'the image\n-- one <fileGrp> for the master archival TIFFs of the images\nFor a text ' \
                 'resource with a variety of content file types one might group the content files at the highest ' \
                 'level by type,  and then use the <fileGrp> element’s nesting capabilities to subdivide a ' \
                 '<fileGrp> by format within the type, such as:\n-- one <fileGrp> for all of the ' \
                 'page images with nested <fileGrp> elements for each image format/resolution (tiff, jpeg, ' \
                 'gif)\n-- one <fileGrp> for a PDF version of all the pages of the document\n-- one ' \
                 '<fileGrp> for  a TEI encoded XML version of the entire document or each of its pages.\nA ' \
                 '<fileGrp> may contain zero or more <fileGrp> elements and or <file> elements. '
    STRUCT_MAP = 'The structural map section <structMap> is the heart of a METS document. It provides a means for ' \
                 'organizing the digital content represented by the <file> elements in the <fileSec> of the METS ' \
                 'document into a coherent hierarchical structure. Such a hierarchical structure can be presented to ' \
                 'users to facilitate their comprehension and navigation of the digital content. It can further be ' \
                 'applied to any purpose requiring an understanding of the structural relationship of the content ' \
                 'files or parts of the content files. The organization may be specified to any level of granularity ' \
                 '(intellectual and or physical) that is desired. Since the <structMap> element is repeatable, ' \
                 'more than one organization can be applied to the digital content represented by the METS document. '
    STRUCT_MAP_TREE = 'The hierarchical structure specified by a <structMap> is encoded as a tree of nested ' \
                      '<div> elements. A <div> element may directly point to content via child file ' \
                      'pointer <fptr> elements (if the content is represented in the <fileSec>) or child ' \
                      'METS pointer <mptr> elements (if the content is represented by an external METS ' \
                      'document). The <fptr> element may point to a single whole <file> element that ' \
                      'manifests its parent <div>, or to part of a <file> that manifests its <div>. It can also point ' \
                      'to multiple files or parts of files that must be played/displayed either in sequence or in ' \
                      'parallel to reveal its structural division. In addition to providing a means for organizing ' \
                      'content, the <structMap> provides a mechanism for linking content at any hierarchical level ' \
                      'with relevant descriptive and administrative metadata. '
    STRUCT_LINK_SEC = 'The structural link section element &lt;structLink&gt; allows for the specification of ' \
                      'hyperlinks between the different components of a METS structure that are delineated in a ' \
                      'structural map. This element is a container for a single, repeatable element, &lt;smLink&gt; ' \
                      'which indicates a hyperlink between two nodes in the structural map. The &lt;structLink&gt; ' \
                      'section in the METS document is identified using its XML ID attributes.'
    BEHAVIOUR_SEC = 'A behavior section element &lt;behaviorSec&gt; associates executable behaviors with content ' \
                    'in the METS document by means of a repeatable behavior &lt;behavior&gt; element. This ' \
                    'element has an interface definition &lt;interfaceDef&gt; element that represents an ' \
                    'abstract definition of the set of behaviors represented by a particular behavior section. A ' \
                    '&lt;behavior&gt; element also has a &lt;mechanism&gt; element which is used to point to a ' \
                    'module of executable code that implements and runs the behavior defined by the interface ' \
                    'definition. The &lt;behaviorSec&gt; element, which is repeatable as well as nestable, ' \
                    'can be used to group individual behaviors within the structure of the METS document. Such ' \
                    'grouping can be useful for organizing families of behaviors together or to indicate other ' \
                    'relationships between particular behaviors.'
    DIV = "The structural divisions of the hierarchical organization provided by a &lt;structMap&gt; are " \
          "represented by division &lt;div&gt; elements, which can be nested to any depth. Each &lt;div&gt; " \
          "element can represent either an intellectual (logical) division or a physical division. Every " \
          "&lt;div&gt; node in the structural map hierarchy may be connected (via subsidiary &lt;mptr&gt; or " \
          "&lt;fptr&gt; elements) to content files which represent that div's portion of the whole document. "
    MPTR = 'Like the &lt;fptr&gt; element, the METS pointer element &lt;mptr&gt; represents digital content that ' \
           'manifests its parent &lt;div&gt; element. Unlike the &lt;fptr&gt;, which either directly or indirectly ' \
           'points to content represented in the &lt;fileSec&gt; of the parent METS document, the &lt;mptr&gt; ' \
           'element points to content represented by an external METS document. Thus, this element allows multiple ' \
           'discrete and separate METS documents to be organized at a higher level by a separate METS document. For ' \
           'example, METS documents representing the individual issues in the series of a journal could be grouped ' \
           'together and organized by a higher level METS document that represents the entire journal series. Each of ' \
           'the &lt;div&gt; elements in the &lt;structMap&gt; of the METS document representing the journal series ' \
           'would point to a METS document representing an issue.  It would do so via a child &lt;mptr&gt; element. ' \
           'Thus the &lt;mptr&gt; element gives METS users considerable flexibility in managing the depth of the ' \
           '&lt;structMap&gt; hierarchy of individual METS documents. The &lt;mptr&gt; element points to an external ' \
           'METS document by means of an xlink:href attribute and associated XLink attributes. '
    FPTR = 'The &lt;fptr&gt; or file pointer element represents digital content that manifests its parent &lt;div&gt; ' \
           'element. The content represented by an &lt;fptr&gt; element must consist of integral files or parts of ' \
           'files that are represented by &lt;file&gt; elements in the &lt;fileSec&gt;. Via its FILEID attribute,  ' \
           'an &lt;fptr&gt; may point directly to a single integral &lt;file&gt; element that manifests a structural ' \
           'division. However, an &lt;fptr&gt; element may also govern an &lt;area&gt; element,  a &lt;par&gt;, ' \
           'or  a &lt;seq&gt;  which in turn would point to the relevant file or files. A child &lt;area&gt; element ' \
           'can point to part of a &lt;file&gt; that manifests a division, while the &lt;par&gt; and &lt;seq&gt; ' \
           'elements can point to multiple files or parts of files that together manifest a division. More than one ' \
           '&lt;fptr&gt; element can be associated with a &lt;div&gt; element. Typically sibling &lt;fptr&gt; ' \
           'elements represent alternative versions, or manifestations, of the same content '
    AREA = 'The area element &lt;area&gt; typically points to content consisting of just a portion or area of a file ' \
           'represented by a &lt;file&gt; element in the &lt;fileSec&gt;. In some contexts, however, the &lt;area&gt; ' \
           'element can also point to content represented by an integral file. A single &lt;area&gt; element would ' \
           'appear as the direct child of a &lt;fptr&gt; element when only a portion of a &lt;file&gt;, rather than ' \
           'an integral &lt;file&gt;, manifested the digital content represented by the &lt;fptr&gt;. Multiple ' \
           '&lt;area&gt; elements would appear as the direct children of a &lt;par&gt; element or a &lt;seq&gt; ' \
           'element when multiple files or parts of files manifested the digital content represented by an ' \
           '&lt;fptr&gt; element. When used in the context of a &lt;par&gt; or &lt;seq&gt; element an &lt;area&gt; ' \
           'element can point either to an integral file or to a segment of a file as necessary. '
    SEQ = 'The sequence of files element &lt;seq&gt; aggregates pointers to files,  parts of files and/or parallel ' \
          'sets of files or parts of files  that must be played or displayed sequentially to manifest a block of ' \
          'digital content. This might be the case, for example, if the parent &lt;div&gt; element represented a ' \
          'logical division, such as a diary entry, that spanned multiple pages of a diary and, hence, multiple page ' \
          'image files. In this case, a &lt;seq&gt; element would aggregate multiple, sequentially arranged ' \
          '&lt;area&gt; elements, each of which pointed to one of the image files that must be presented sequentially ' \
          'to manifest the entire diary entry. If the diary entry started in the middle of a page, then the first ' \
          '&lt;area&gt; element (representing the page on which the diary entry starts) might be further qualified, ' \
          'via its SHAPE and COORDS attributes, to specify the specific, pertinent area of the associated image file. '
    PAR = 'The &lt;par&gt; or parallel files element aggregates pointers to files, parts of files, and/or sequences ' \
          'of files or parts of files that must be played or displayed simultaneously to manifest a block of digital ' \
          'content represented by an &lt;fptr&gt; element. This might be the case, for example, with multi-media ' \
          'content, where a still image might have an accompanying audio track that comments on the still image. In ' \
          'this case, a &lt;par&gt; element would aggregate two &lt;area&gt; elements, one of which pointed to the ' \
          'image file and one of which pointed to the audio file that must be played in conjunction with the image. ' \
          'The &lt;area&gt; element associated with the image could be further qualified with SHAPE and COORDS ' \
          'attributes if only a portion of the image file was pertinent and the &lt;area&gt; element associated with ' \
          'the audio file could be further qualified with BETYPE, BEGIN, EXTTYPE, and EXTENT attributes if only a ' \
          'portion of the associated audio file should be played in conjunction with the image. '
    TECH_MD = 'A technical metadata element &lt;techMD&gt; records technical metadata about a component of the ' \
              'METS object, such as a digital content file. The &lt;techMD&gt; element conforms to same generic ' \
              'datatype as the &lt;dmdSec&gt;, &lt;rightsMD&gt;, &lt;sourceMD&gt; and &lt;digiprovMD&gt; ' \
              'elements, and supports the same sub-elements and attributes.  A technical metadata element can ' \
              'either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS ' \
              'allows multiple &lt;techMD&gt; elements; and technical metadata can be associated with any METS ' \
              'element that supports an ADMID attribute. Technical metadata can be expressed according to many ' \
              'current technical description standards (such as MIX and textMD) or a locally produced XML schema.'
    RIGHTS_MD = 'An intellectual property rights metadata element &lt;rightsMD&gt; records information about ' \
                'copyright and licensing pertaining to a component of the METS object. The &lt;rightsMD&gt; ' \
                'element conforms to same generic datatype as the &lt;dmdSec&gt;, &lt;techMD>, &lt;sourceMD&gt; ' \
                'and &lt;digiprovMD&gt; elements, and supports the same sub-elements and attributes. A rights ' \
                'metadata element can either wrap the metadata  (mdWrap) or reference it in an external location ' \
                '(mdRef) or both.  METS allows multiple &lt;rightsMD&gt; elements; and rights metadata can be ' \
                'associated with any METS element that supports an ADMID attribute. Rights metadata can be ' \
                'expressed according current rights description standards (such as CopyrightMD and ' \
                'rightsDeclarationMD) or a locally produced XML schema.'
    SOURCE_MD = 'A source metadata element &lt;sourceMD&gt; records descriptive and administrative metadata ' \
                'about the source format or media of a component of the METS object such as a digital content ' \
                'file. It is often used for discovery, data administration or preservation of the digital ' \
                'object. The &lt;sourceMD&gt; element conforms to same generic datatype as the &lt;dmdSec&gt;, ' \
                '&lt;techMD&gt;, &lt;rightsMD&gt;,  and &lt;digiprovMD&gt; elements, and supports the same ' \
                'sub-elements and attributes.  A source metadata element can either wrap the metadata  (mdWrap) ' \
                'or reference it in an external location (mdRef) or both.  METS allows multiple &lt;sourceMD&gt; ' \
                'elements; and source metadata can be associated with any METS element that supports an ADMID ' \
                'attribute. Source metadata can be expressed according to current source description standards (' \
                'such as PREMIS) or a locally produced XML schema.'
    DIGIPROV_MD = 'A digital provenance metadata element &lt;digiprovMD&gt; can be used to record any ' \
                  'preservation-related actions taken on the various files which comprise a digital object (' \
                  'e.g., those subsequent to the initial digitization of the files such as transformation or ' \
                  'migrations) or, in the case of born digital materials, the files’ creation. In short, ' \
                  'digital provenance should be used to record information that allows both archival/library ' \
                  'staff and scholars to understand what modifications have been made to a digital object and/or ' \
                  'its constituent parts during its life cycle. This information can then be used to judge how ' \
                  'those processes might have altered or corrupted the object’s ability to accurately represent ' \
                  'the original item. One might, for example, record master derivative relationships and the ' \
                  'process by which those derivations have been created. Or the &lt;digiprovMD&gt; element could ' \
                  'contain information regarding the migration/transformation of a file from its original ' \
                  'digitization (e.g., OCR, TEI, etc.,)to its current incarnation as a digital object (e.g., ' \
                  'JPEG2000). The &lt;digiprovMD&gt; element conforms to same generic datatype as the ' \
                  '&lt;dmdSec&gt;,  &lt;techMD&gt;, &lt;rightsMD&gt;, and &lt;sourceMD&gt; elements, ' \
                  'and supports the same sub-elements and attributes. A digital provenance metadata element can ' \
                  'either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  ' \
                  'METS allows multiple &lt;digiprovMD> elements; and digital provenance metadata can be ' \
                  'associated with any METS element that supports an ADMID attribute. Digital provenance ' \
                  'metadata can be expressed according to current digital provenance description standards (such ' \
                  'as PREMIS) or a locally produced XML schema.'
    NAME = 'The element <name> can be used to record the full name of the document agent.'
    NOTE = "The <note> element can be used to record any additional information regarding the agent's activities with " \
           "respect to the METS document."
    FILE = 'The file element provides access to content files for a METS object.  A file element may contain one or ' \
           'more FLocat elements, which provide pointers to a content file, and/or an FContent element, which wraps ' \
           'an encoded version of the file. Note that ALL FLocat and FContent elements underneath a single file ' \
           'element should identify/contain identical copies of a single file. '
    FILE_LOCATION = 'The file location element &lt;FLocat&gt; provides a pointer to the location of a content file. ' \
                    'It uses the XLink reference syntax to provide linking information indicating the actual location ' \
                    'of the content file, along with other attributes specifying additional linking information. ' \
                    'NOTE: &lt;FLocat&gt; is an empty element. The location of the resource pointed to MUST be stored ' \
                    'in the xlink:href attribute. '
    FILE_CONTENT = 'The file content element &lt;FContent&gt; is used to identify a content file contained internally ' \
                   'within a METS document. The content file must be either Base64 encoded and contained within the ' \
                   'subsidiary &lt;binData&gt; wrapper element, or consist of XML information and be contained within ' \
                   'the subsidiary &lt;xmlData&gt; wrapper element. '
    STREAM = 'A component byte stream element &lt;stream&gt; may be composed of one or more subsidiary streams. An ' \
             'MPEG4 file, for example, might contain separate audio and video streams, each of which is associated ' \
             'with technical metadata. The repeatable &lt;stream&gt; element provides a mechanism to record the ' \
             'existence of separate data streams within a particular file, and the opportunity to associate ' \
             '&lt;dmdSec&gt; and &lt;amdSec&gt; with those subsidiary data streams if desired. '
    TRANSFORM_FILE = 'The transform file element &lt;transformFile&gt; provides a means to access any subsidiary ' \
                     'files listed below a &lt;file&gt; element by indicating the steps required to "unpack" or ' \
                     'transform the subsidiary files. This element is repeatable and might provide a link to a ' \
                     '&lt;behavior&gt; in the &lt;behaviorSec&gt; that performs the transformation. '
    MD_REF = 'The metadata reference element &lt;mdRef&gt; element is a generic element used throughout the METS ' \
             'schema to provide a pointer to metadata which resides outside the METS document.  NB: &lt;mdRef&gt; is ' \
             'an empty element.  The location of the metadata must be recorded in the xlink:href attribute, ' \
             'supplemented by the XPTR attribute as needed. '
    MD_WRAP = 'A metadata wrapper element &lt;mdWrap&gt; provides a wrapper around metadata embedded within a METS ' \
              'document. The element is repeatable. Such metadata can be in one of two forms:\n1) XML-encoded ' \
              'metadata, with the XML-encoding identifying itself as belonging to a namespace other than the METS ' \
              'document namespace.\n2) Any arbitrary binary or textual form, PROVIDED that the metadata is Base64 ' \
              'encoded and wrapped in a &lt;binData&gt; element within the internal descriptive metadata element. '
    STRUCT_LINK_GROUP = 'The structMap link group element &lt;smLinkGrp&gt; provides an implementation of ' \
                        'xlink:extendLink, and provides xlink compliant mechanisms for establishing xlink:arcLink ' \
                        'type links between 2 or more &lt;div&gt; elements in &lt;structMap&gt; element(s) occurring ' \
                        'within the same METS document or different METS documents.  The smLinkGrp could be used as ' \
                        'an alternative to the &lt;smLink&gt; element to establish a one-to-one link between ' \
                        '&lt;div&gt; elements in the same METS document in a fully xlink compliant manner.  However, ' \
                        'it can also be used to establish one-to-many or many-to-many links between &lt;div&gt; ' \
                        'elements. For example, if a METS document contains two &lt;structMap&gt; elements, ' \
                        'one of which represents a purely logical structure and one of which represents a purely ' \
                        'physical structure, the &lt;smLinkGrp&gt; element would provide a means of mapping a ' \
                        '&lt;div&gt; representing a logical entity (for example, a newspaper article) with multiple ' \
                        '&lt;div&gt; elements in the physical &lt;structMap&gt; representing the physical areas that  ' \
                        'together comprise the logical entity (for example, the &lt;div&gt; elements representing the ' \
                        'page areas that together comprise the newspaper article). '
    STRUCT_LINK = 'The Structural Map Link element &lt;smLink&gt; identifies a hyperlink between two nodes in the ' \
                  'structural map. You would use &lt;smLink&gt;, for instance, to note the existence of hypertext ' \
                  'links between web pages, if you wished to record those links within METS. NOTE: &lt;smLink&gt; is ' \
                  'an empty element. The location of the &lt;smLink&gt; element to which the &lt;smLink&gt; element ' \
                  'is pointing MUST be stored in the xlink:href attribute. '
    LOCATOR_LINK = 'The structMap locator link element <smLocatorLink> is of xlink:type "locator".  It provides a ' \
                   'means of identifying a <div> element that will participate in one or more of the links specified ' \
                   'by means of <smArcLink> elements within the same <smLinkGrp>. The participating <div> element ' \
                   'that is represented by the <smLocatorLink> is identified by means of a URI in the associate ' \
                   'xlink:href attribute.  The lowest level of this xlink:href URI value should be a fragment ' \
                   'identifier that references the ID value that identifies the relevant <div> element.  For example, ' \
                   '"xlink:href=#div20" where "div20" is the ID value that identifies the pertinent <div> in the ' \
                   'current METS document. Although not required by the xlink specification, an <smLocatorLink> ' \
                   'element will typically include an xlink:label attribute in this context, as the <smArcLink> ' \
                   'elements will reference these labels to establish the from and to sides of each arc link. '
    ARC_LINK = 'The structMap arc link element <smArcLink> is of xlink:type "arc" It can be used to establish a ' \
               'traversal link between two <div> elements as identified by <smLocatorLink> elements within the same ' \
               'smLinkGrp element. The associated xlink:from and xlink:to attributes identify the from and to sides ' \
               'of the arc link by referencing the xlink:label attribute values on the participating smLocatorLink ' \
               'elements. '
    BEHAVIOUR = 'A behavior element &lt;behavior&gt; can be used to associate executable behaviors with content in ' \
                'the METS document. This element has an interface definition &lt;interfaceDef&gt; element that ' \
                'represents an abstract definition of a set of behaviors represented by a particular behavior. A ' \
                '&lt;behavior&gt; element also has a behavior mechanism &lt;mechanism&gt; element, a module of ' \
                'executable code that implements and runs the behavior defined abstractly by the interface definition. '
    INTERFACE_DEFINITION = 'The interface definition &lt;interfaceDef&gt; element contains a pointer to an abstract ' \
                           'definition of a single behavior or a set of related behaviors that are associated with ' \
                           'the content of a METS object. The interface definition object to which the ' \
                           '&lt;interfaceDef&gt; element points using xlink:href could be another digital object, ' \
                           'or some other entity, such as a text file which describes the interface or a Web Services ' \
                           'Description Language (WSDL) file. Ideally, an interface definition object contains ' \
                           'metadata that describes a set of behaviors or methods. It may also contain files that ' \
                           'describe the intended usage of the behaviors, and possibly files that represent different ' \
                           'expressions of the interface definition. '
    MECHANISM = 'A mechanism element &lt;mechanism&gt; contains a pointer to an executable code module that ' \
                'implements a set of behaviors defined by an interface definition. The &lt;mechanism&gt; element will ' \
                'be a pointer to another object (a mechanism object). A mechanism object could be another METS ' \
                'object, or some other entity (e.g., a WSDL file). A mechanism object should contain executable code, ' \
                'pointers to executable code, or specifications for binding to network services (e.g., web services). '
