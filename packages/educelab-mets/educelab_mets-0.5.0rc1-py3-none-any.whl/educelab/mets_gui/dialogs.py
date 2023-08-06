# defines all dialog windows for adding/editting new elements and attributes
# base class for all dialogs is CustomDialog - defined in utils.py

from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QComboBox, QLabel

from educelab import mets
from educelab.mets_gui import constants
from educelab.mets_gui.utils import (LabelWithTooltip,
                                     combo_box_other_type_enable,
                                     create_form_row_items,
                                     xml_warning_text_change, CustomDialog,
                                     OtherAttributeList, create_separator)


# structural map creation dialog
class AddStructMapDialog(CustomDialog):
    def fill_form_layout(self):
        self.setWindowTitle(constants.Labels.DIALOG_ADD_STRUCT_MAP.value)
        layout = self.form_layout
        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.ID.value,
            constants.AttributeTooltips.ID.value)
        layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.TYPE.value,
            constants.AttributeTooltips.STRUCT_MAP_TYPE.value)
        layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.LABEL.value,
            constants.AttributeTooltips.STRUCT_MAP_LABEL.value)
        layout.addRow(label, form_input)

        label = LabelWithTooltip(constants.Labels.OTHER_ATTRIBS.value,
                                 constants.AttributeTooltips.OTHER_ATTRIBS.value)
        layout.addRow(label, OtherAttributeList(verbose=False))

        return

    def fill_tag_data(self):
        self.values[
            constants.Labels.TAG.value] = constants.ElementTags.STRUCT_MAP.value
        return

    def load_data(self, data):
        self.setWindowTitle(constants.Labels.DIALOG_EDIT_STRUCT_MAP.value)
        super().load_data(data)
        return


# structural map child elements creation dialog
class AddStructMapItemDialog(CustomDialog):
    def __init__(self, parent, data=None):
        self.parent = parent
        super().__init__(data)
        self.setWindowTitle(
            constants.Labels.DIALOG_ADD_STRUCT_MAP_ELEMENT.value)

    def fill_upper_layout(self):
        layout = self.upper_layout
        label = LabelWithTooltip(constants.Labels.ELEMENT_TYPE.value,
                                 constants.ElementTooltips.STRUCT_MAP_TREE.value,
                                 True)
        layout.addWidget(label)
        self.element_type = QComboBox(self)
        i = 0
        for item in constants.StructMapElements:
            self.element_type.addItem(item.value)
            self.element_type.model().item(i).setToolTip(
                constants.ElementTooltips[item.name].value)
            i += 1

        self.element_type.currentIndexChanged.connect(self.element_type_change)
        layout.addWidget(self.element_type)
        layout.addWidget(create_separator())
        return

    def fill_form_layout(self):
        self.restrict_element_types()

    def restrict_element_types(self):
        model = self.element_type.model()
        if self.parent is None:
            model.item(1).setEnabled(False)
            model.item(2).setEnabled(False)
            model.item(3).setEnabled(False)
            model.item(4).setEnabled(False)
            model.item(5).setEnabled(False)
            self.element_type.setCurrentIndex(1)
            self.element_type.setCurrentIndex(0)
        else:
            parent_type = self.parent.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value]
            if parent_type == constants.ElementTags.DIV.value:
                model.item(3).setEnabled(False)
                model.item(4).setEnabled(False)
                model.item(5).setEnabled(False)
                self.element_type.setCurrentIndex(1)
                self.element_type.setCurrentIndex(0)
            elif parent_type == constants.ElementTags.FPTR.value:
                model.item(0).setEnabled(False)
                model.item(1).setEnabled(False)
                model.item(2).setEnabled(False)
                self.element_type.setCurrentIndex(3)
            elif parent_type == constants.ElementTags.SEQ.value:
                model.item(0).setEnabled(False)
                model.item(1).setEnabled(False)
                model.item(2).setEnabled(False)
                model.item(4).setEnabled(False)
                self.element_type.setCurrentIndex(3)
            elif parent_type == constants.ElementTags.PAR.value:
                model.item(0).setEnabled(False)
                model.item(1).setEnabled(False)
                model.item(2).setEnabled(False)
                model.item(5).setEnabled(False)
                self.element_type.setCurrentIndex(3)
        return

    def element_type_change(self):
        tag_type = self.element_type.currentText()
        layout = self.form_layout
        for i in reversed(
                range(
                    layout.count())):  # delete previous widgets when switching element types
            layout.itemAt(i).widget().setParent(None)
        if tag_type == constants.StructMapElements.DIV.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.TYPE.value,
                constants.AttributeTooltips.DIV_TYPE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.LABEL.value,
                constants.AttributeTooltips.DIV_LABEL.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.DMDID.value,
                constants.AttributeTooltips.DMDID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ADMID.value,
                constants.AttributeTooltips.ADMID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ORDER.value,
                constants.AttributeTooltips.ORDER.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ORDER_LABEL.value,
                constants.AttributeTooltips.ORDER_LABEL.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.CONTENT_IDS.value,
                constants.AttributeTooltips.CONTENT_IDS.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_LABEL.value,
                constants.AttributeTooltips.XLINK_LABEL.value)
            layout.addRow(label, form_input)

        elif tag_type == constants.StructMapElements.MPTR.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input_box = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.LOCTYPE.value,
                constants.AttributeTooltips.LOCTYPE.value,
                True,
                mets.constants.LocatorTypes)
            layout.addRow(label, form_input_box)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.OTHER_LOCTYPE.value,
                constants.AttributeTooltips.OTHER_LOCTYPE.value)

            form_input.setEnabled(False)
            layout.addRow(label, form_input)

            form_input_box.currentIndexChanged.connect(
                lambda idx, box=form_input_box,
                       inpt=form_input: combo_box_other_type_enable(box, inpt))

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.CONTENT_IDS.value,
                constants.AttributeTooltips.CONTENT_IDS.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_HREF.value,
                constants.AttributeTooltips.XLINK_HREF.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ROLE.value,
                constants.AttributeTooltips.XLINK_ROLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ARCROLE.value,
                constants.AttributeTooltips.XLINK_ARCROLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_TITLE.value,
                constants.AttributeTooltips.XLINK_TITLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_SHOW.value,
                constants.AttributeTooltips.XLINK_SHOW.value,
                data=mets.constants.XlinkShowTypes)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_ACTUATE.value,
                constants.AttributeTooltips.XLINK_ACTUATE.value,
                data=mets.constants.XlinkActuateTypes)
            layout.addRow(label, form_input)

        elif tag_type == constants.StructMapElements.FPTR.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.FILE_ID.value,
                constants.AttributeTooltips.FILE_ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.CONTENT_IDS.value,
                constants.AttributeTooltips.CONTENT_IDS.value)
            layout.addRow(label, form_input)

        elif tag_type == constants.StructMapElements.SEQ.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

        elif tag_type == constants.StructMapElements.AREA.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.FILE_ID.value,
                constants.AttributeTooltips.FILE_ID.value,
                True)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.SHAPE.value,
                constants.AttributeTooltips.SHAPE.value,
                data=mets.constants.ShapeTypes)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.COORDS.value,
                constants.AttributeTooltips.COORDS.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.BEGIN.value,
                constants.AttributeTooltips.BEGIN.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.END.value,
                constants.AttributeTooltips.END.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.BETYPE.value,
                constants.AttributeTooltips.BETYPE.value,
                data=mets.constants.AreaBeginEndTypes)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.EXTEND.value,
                constants.AttributeTooltips.EXTEND.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.EXT_TYPE.value,
                constants.AttributeTooltips.EXT_TYPE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ADMID.value,
                constants.AttributeTooltips.ADMID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.CONTENT_IDS.value,
                constants.AttributeTooltips.CONTENT_IDS.value)
            layout.addRow(label, form_input)

        elif tag_type == constants.StructMapElements.PAR.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)
        self.adjustSize()
        return

    def load_data(self, data):
        self.setWindowTitle(
            constants.Labels.DIALOG_EDIT_STRUCT_MAP_ELEMENT.value)
        index = self.element_type.findText(
            constants.StructMapElements[constants.ElementTags(
                data[constants.Labels.TAG.value]).name].value)
        self.element_type.setCurrentIndex(index)
        super().load_data(data)

    def fill_tag_data(self):
        element_type = self.element_type.currentText()
        if element_type == constants.StructMapElements.DIV.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.DIV.value
        elif element_type == constants.StructMapElements.MPTR.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.MPTR.value
        elif element_type == constants.StructMapElements.FPTR.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.FPTR.value
        elif element_type == constants.StructMapElements.SEQ.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.SEQ.value
        elif element_type == constants.StructMapElements.AREA.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.AREA.value
        elif element_type == constants.StructMapElements.PAR.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.PAR.value
        return


# agent element creation dialog
class AddAgentDialog(CustomDialog):
    def fill_form_layout(self):
        self.setWindowTitle(constants.Labels.DIALOG_ADD_AGENT.value)
        layout = self.form_layout
        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.NAME.value,
            constants.ElementTooltips.NAME.value,
            True)
        layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.ID.value,
            constants.AttributeTooltips.ID.value)
        layout.addRow(label, form_input)

        label, form_input_box = create_form_row_items(
            constants.InputTypes.COMBO_BOX.value,
            constants.Attributes.ROLE.value,
            constants.AttributeTooltips.ROLE.value,
            required=True,
            data=mets.constants.AgentRoles)
        layout.addRow(label, form_input_box)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.OTHER_ROLE.value,
            constants.AttributeTooltips.AGENT_OTHER_TYPE.value)
        layout.addRow(label, form_input)
        form_input.setEnabled(False)
        form_input_box.currentIndexChanged.connect(
            lambda idx, box=form_input_box,
                   inpt=form_input: combo_box_other_type_enable(box, inpt))

        label, form_input_box = create_form_row_items(
            constants.InputTypes.COMBO_BOX.value,
            constants.Attributes.TYPE.value,
            constants.AttributeTooltips.AGENT_TYPE.value,
            data=mets.constants.AgentTypes)
        layout.addRow(label, form_input_box)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.OTHER_TYPE.value,
            constants.AttributeTooltips.AGENT_OTHER_TYPE.value)
        layout.addRow(label, form_input)
        form_input.setEnabled(False)
        form_input_box.currentIndexChanged.connect(
            lambda idx, box=form_input_box,
                   inpt=form_input: combo_box_other_type_enable(box, inpt))

        label, form_input = create_form_row_items(
            constants.InputTypes.LIST.value,
            constants.Attributes.NOTE.value,
            constants.ElementTooltips.NOTE.value,
            dialog=AddNoteDialog)
        layout.addRow(label, form_input)
        return

    def fill_tag_data(self):
        self.values[
            constants.Labels.TAG.value] = constants.ElementTags.AGENT.value
        return

    def load_data(self, data):
        self.setWindowTitle(constants.Labels.DIALOG_EDIT_AGENT.value)
        super().load_data(data)


# note element creation dialog
class AddNoteDialog(CustomDialog):
    def fill_form_layout(self):
        self.setWindowTitle(constants.Labels.DIALOG_ADD_NOTE.value)
        layout = self.form_layout
        label, form_input = create_form_row_items(
            constants.InputTypes.TEXT_EDIT.value,
            constants.Labels.VALUE.value,
            constants.ElementTooltips.NOTE.value,
            True)
        layout.addRow(label, form_input)

        return

    def fill_tag_data(self):
        self.values[
            constants.Labels.TAG.value] = constants.ElementTags.NOTE.value
        self.values[constants.Attributes.ID.value] = ''
        return

    def load_data(self, data):
        self.setWindowTitle(constants.Labels.DIALOG_EDIT_NOTE.value)
        super().load_data(data)


# alternative id element creation dialog
class AddAltIDDialog(CustomDialog):
    def fill_form_layout(self):
        self.setWindowTitle(constants.Labels.DIALOG_ADD_ALT_ID.value)
        layout = self.form_layout
        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Labels.VALUE.value,
            constants.ElementTooltips.ALT_RECORD_ID.value,
            True)
        layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.ID.value,
            constants.AttributeTooltips.ID.value)
        layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.TYPE.value,
            constants.AttributeTooltips.IDENTIFIER_TYPE.value)
        layout.addRow(label, form_input)

        return

    def fill_tag_data(self):
        self.values[
            constants.Labels.TAG.value] = constants.ElementTags.ALT_RECORD_ID.value
        return

    def load_data(self, data):
        self.setWindowTitle(constants.Labels.DIALOG_ADD_ALT_ID.value)
        super().load_data(data)


# file section child element creation dialog
class AddFileSecItemDialog(CustomDialog):
    def __init__(self, parent, data=None):
        self.parent = parent
        super().__init__(data)
        self.setWindowTitle(constants.Labels.DIALOG_ADD_FILE_SEC_ELEMENT.value)

    def fill_upper_layout(self):
        layout = self.upper_layout
        label = LabelWithTooltip(constants.Labels.ELEMENT_TYPE.value,
                                 constants.ElementTooltips.FILE_SEC.value,
                                 True)
        layout.addWidget(label)
        self.element_type = QComboBox(self)
        i = 0
        for item in constants.FileSecElements:
            self.element_type.addItem(item.value)
            self.element_type.model().item(i).setToolTip(
                constants.ElementTooltips[item.name].value)
            i += 1

        self.element_type.currentIndexChanged.connect(self.element_type_change)
        layout.addWidget(self.element_type)
        layout.addWidget(create_separator())
        return

    def fill_form_layout(self):
        self.restrict_element_types()
        return

    def restrict_element_types(self):
        model = self.element_type.model()
        if self.parent is None:
            model.item(1).setEnabled(False)
            model.item(2).setEnabled(False)
            model.item(3).setEnabled(False)
            model.item(4).setEnabled(False)
            model.item(5).setEnabled(False)
            self.element_type.setCurrentIndex(1)
            self.element_type.setCurrentIndex(0)
        else:
            parent_type = self.parent.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value]
            if parent_type == constants.ElementTags.FILE_GROUP.value:
                model.item(2).setEnabled(False)
                model.item(3).setEnabled(False)
                model.item(4).setEnabled(False)
                model.item(5).setEnabled(False)
                if self.parent.rowCount() == 0:
                    self.element_type.setCurrentIndex(1)
                    self.element_type.setCurrentIndex(0)
                else:
                    required_type = \
                        self.parent.child(0).data(Qt.ItemDataRole.UserRole)[
                            constants.Labels.TAG.value]
                    if required_type == constants.ElementTags.FILE_GROUP.value:
                        model.item(1).setEnabled(False)
                        self.element_type.setCurrentIndex(1)
                        self.element_type.setCurrentIndex(0)
                    elif required_type == constants.ElementTags.FILE.value:
                        model.item(0).setEnabled(False)
                        self.element_type.setCurrentIndex(1)
            elif parent_type == constants.ElementTags.FILE.value:
                model.item(0).setEnabled(False)
                self.element_type.setCurrentIndex(1)
                content = False
                if self.parent.rowCount() > 0:
                    for i in range(0, self.parent.rowCount()):
                        if self.parent.child(i).data(Qt.ItemDataRole.UserRole)[
                            constants.Labels.TAG.value] == \
                                constants.ElementTags.FILE_CONTENT.value:
                            content = True
                if content:
                    model.item(3).setEnabled(False)

        return

    def element_type_change(self):
        tag_type = self.element_type.currentText()
        layout = self.form_layout
        for i in reversed(
                range(
                    layout.count())):  # delete previous widgets when switching element types
            layout.itemAt(i).widget().setParent(None)
        if tag_type == constants.FileSecElements.FILE_GROUP.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.DATE_TIME.value,
                constants.Attributes.VERSDATE.value,
                constants.AttributeTooltips.VERSDATE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ADMID.value,
                constants.AttributeTooltips.ADMID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.USE.value,
                constants.AttributeTooltips.USE.value)
            layout.addRow(label, form_input)

        elif tag_type == constants.FileSecElements.FILE.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID_FILE.value,
                required=True)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.SEQ.value,
                constants.AttributeTooltips.SEQ.value)
            form_input.setValidator(
                QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*")))
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.MIMETYPE.value,
                constants.AttributeTooltips.MIME_TYPE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.SIZE.value,
                constants.AttributeTooltips.SIZE.value)
            form_input.setValidator(
                QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*")))
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.DATE_TIME.value,
                constants.Attributes.CREATED.value,
                constants.AttributeTooltips.CREATED.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.CHECKSUM.value,
                constants.AttributeTooltips.CHECKSUM.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.CHECKSUM_TYPE.value,
                constants.AttributeTooltips.CHECKSUM_TYPE.value,
                data=mets.constants.ChecksumTypes)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.OWNER_ID.value,
                constants.AttributeTooltips.OWNER_ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.DMDID.value,
                constants.AttributeTooltips.DMDID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ADMID.value,
                constants.AttributeTooltips.ADMID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.GROUP_ID.value,
                constants.AttributeTooltips.GROUP_ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.USE.value,
                constants.AttributeTooltips.USE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.BEGIN.value,
                constants.AttributeTooltips.BEGIN.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.END.value,
                constants.AttributeTooltips.END.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.BETYPE.value,
                constants.AttributeTooltips.BETYPE.value,
                data=mets.constants.FileBeginEndTypes)
            layout.addRow(label, form_input)

        elif tag_type == constants.FileSecElements.FILE_LOCATION.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input_box = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.LOCTYPE.value,
                constants.AttributeTooltips.LOCTYPE.value,
                True,
                mets.constants.LocatorTypes)
            layout.addRow(label, form_input_box)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.OTHER_LOCTYPE.value,
                constants.AttributeTooltips.OTHER_LOCTYPE.value)

            form_input.setEnabled(False)
            layout.addRow(label, form_input)

            form_input_box.currentIndexChanged.connect(
                lambda idx, box=form_input_box,
                       inpt=form_input: combo_box_other_type_enable(box, inpt))

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.USE.value,
                constants.AttributeTooltips.USE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_HREF.value,
                constants.AttributeTooltips.XLINK_HREF.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ROLE.value,
                constants.AttributeTooltips.XLINK_ROLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ARCROLE.value,
                constants.AttributeTooltips.XLINK_ARCROLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_TITLE.value,
                constants.AttributeTooltips.XLINK_TITLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_SHOW.value,
                constants.AttributeTooltips.XLINK_SHOW.value,
                data=mets.constants.XlinkShowTypes)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_ACTUATE.value,
                constants.AttributeTooltips.XLINK_ACTUATE.value,
                data=mets.constants.XlinkActuateTypes)
            layout.addRow(label, form_input)

        elif tag_type == constants.FileSecElements.FILE_CONTENT.value:
            label, form_input_type = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Labels.ELEMENT_TYPE.value,
                constants.ElementTooltips.FILE_CONTENT.value,
                required=True,
                data=constants.DataContentTypes)
            layout.addRow(label, form_input_type)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.USE.value,
                constants.AttributeTooltips.FCONTENT_USE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.TEXT_EDIT.value,
                constants.Labels.CONTENT.value,
                constants.ElementTooltips.FILE_CONTENT.value,
                required=True)
            layout.addRow(label, form_input)

            label = QLabel(constants.Labels.XML_NAMESPACE_WARNING.value)
            form_input_type.currentIndexChanged.connect(
                lambda idx, box=form_input_type,
                       inpt=label: xml_warning_text_change(box, inpt))
            layout.addRow(None, label)

        elif tag_type == constants.FileSecElements.STREAM.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.STREAM_TYPE.value,
                constants.AttributeTooltips.STREAM_TYPE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.OWNER_ID.value,
                constants.AttributeTooltips.OWNER_ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ADMID.value,
                constants.AttributeTooltips.ADMID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.DMDID.value,
                constants.AttributeTooltips.DMDID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.BEGIN.value,
                constants.AttributeTooltips.BEGIN.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.END.value,
                constants.AttributeTooltips.END.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.BETYPE.value,
                constants.AttributeTooltips.BETYPE.value,
                data=mets.constants.FileBeginEndTypes)
            layout.addRow(label, form_input)

        elif tag_type == constants.FileSecElements.TRANSFORM_FILE.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.TRANSFORM_TYPE.value,
                constants.AttributeTooltips.TRANSFORM_TYPE.value,
                required=True,
                data=mets.constants.TransformTypes)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.TRANSFORM_ALGORITHM.value,
                constants.AttributeTooltips.TRANSFORM_ALGORITHM.value,
                required=True)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.TRANSFORM_KEY.value,
                constants.AttributeTooltips.TRANSFORM_KEY.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.TRANSFORM_BEHAVIOR.value,
                constants.AttributeTooltips.TRANSFORM_BEHAVIOR.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.TRANSFORM_ORDER.value,
                constants.AttributeTooltips.TRANSFORM_ORDER.value,
                required=True)
            form_input.setValidator(
                QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*")))
            layout.addRow(label, form_input)

        return

    def load_data(self, data):
        self.setWindowTitle(constants.Labels.DIALOG_EDIT_FILE_SEC_ELEMENT.value)
        index = self.element_type.findText(
            constants.FileSecElements[constants.ElementTags(
                data[constants.Labels.TAG.value]).name].value)
        self.element_type.setCurrentIndex(index)
        super().load_data(data)

    def fill_tag_data(self):
        element_type = self.element_type.currentText()
        if element_type == constants.FileSecElements.FILE_GROUP.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.FILE_GROUP.value
        elif element_type == constants.FileSecElements.FILE.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.FILE.value
        elif element_type == constants.FileSecElements.FILE_LOCATION.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.FILE_LOCATION.value
        elif element_type == constants.FileSecElements.FILE_CONTENT.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.FILE_CONTENT.value
        elif element_type == constants.FileSecElements.STREAM.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.STREAM.value
        elif element_type == constants.FileSecElements.TRANSFORM_FILE.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.TRANSFORM_FILE.value
        return


# metadata elements creation dialog
class AddMetadataSectionDialog(CustomDialog):
    def fill_upper_layout(self):
        self.setWindowTitle(constants.Labels.DIALOG_ADD_METADATA_SEC.value)
        layout = self.upper_layout
        label = LabelWithTooltip(constants.Labels.METADATA_SECTION_TYPE.value,
                                 '', required=True)
        layout.addWidget(label)
        self.element_type = QComboBox(self)
        i = 0
        for item in constants.MetadataSectionTypes:
            self.element_type.addItem(item.value)
            self.element_type.model().item(i).setToolTip(
                constants.ElementTooltips[item.name].value)
            i += 1

        self.element_type.currentIndexChanged.connect(self.element_type_change)
        layout.addWidget(self.element_type)
        return

    def fill_form_layout(self):
        self.element_type.setCurrentIndex(1)
        self.element_type.setCurrentIndex(0)
        return

    def element_type_change(self):
        tag_type = self.element_type.currentText()
        layout = self.form_layout
        for i in reversed(
                range(
                    layout.count())):  # delete previous widgets when switching element types
            layout.itemAt(i).widget().setParent(None)
        if tag_type == constants.MetadataSectionTypes.DMD_SEC.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.DMD_SEC_ID.value,
                required=True)
            layout.addRow(label, form_input)

        elif tag_type == constants.MetadataSectionTypes.AMD_SEC.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

        return

    def fill_tag_data(self):
        element_type = self.element_type.currentText()
        if element_type == constants.MetadataSectionTypes.DMD_SEC.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.DMD_SEC.value
        elif element_type == constants.MetadataSectionTypes.AMD_SEC.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.AMD_SEC.value
        return

    def load_data(self, data):
        self.setWindowTitle(constants.Labels.DIALOG_EDIT_METADATA_SEC.value)
        index = self.element_type.findText(
            constants.MetadataSectionTypes[constants.ElementTags(
                data[constants.Labels.TAG.value]).name].value)
        self.element_type.setCurrentIndex(index)
        super().load_data(data)


# descriptive metadata child elements creation dialog
class AddDMDElementDialog(CustomDialog):
    def __init__(self, parent, data=None):
        self.parent = parent
        super().__init__(data)
        return

    def fill_upper_layout(self):
        self.setWindowTitle(constants.Labels.DIALOG_ADD_DMD_ELEMENT.value)
        layout = self.upper_layout
        label = LabelWithTooltip(constants.Labels.METADATA_SECTION_TYPE.value,
                                 '', required=True)
        layout.addWidget(label)
        self.element_type = QComboBox(self)
        i = 0
        for item in constants.DescriptiveMetadataTypes:
            self.element_type.addItem(item.value)
            self.element_type.model().item(i).setToolTip(
                constants.ElementTooltips[item.name].value)
            i += 1

        self.element_type.currentIndexChanged.connect(self.element_type_change)
        layout.addWidget(self.element_type)
        return

    def fill_form_layout(self):
        self.restrict_element_types()
        return

    def restrict_element_types(self):
        model = self.element_type.model()
        if self.parent is None:
            self.element_type.setCurrentIndex(1)
            self.element_type.setCurrentIndex(0)
        else:
            if self.parent.rowCount() > 0:
                child = self.parent.child(0).data(Qt.ItemDataRole.UserRole)[
                    constants.Labels.TAG.value]
                if child == constants.ElementTags.MD_REF.value:
                    model.item(0).setEnabled(False)
                    self.element_type.setCurrentIndex(1)
                else:
                    self.element_type.setCurrentIndex(1)
                    self.element_type.setCurrentIndex(0)
                    model.item(1).setEnabled(False)
            else:
                self.element_type.setCurrentIndex(1)
                self.element_type.setCurrentIndex(0)

        return

    def element_type_change(self):
        tag_type = self.element_type.currentText()
        layout = self.form_layout
        for i in reversed(
                range(
                    layout.count())):  # delete previous widgets when switching element types
            layout.itemAt(i).widget().setParent(None)
        if tag_type == constants.DescriptiveMetadataTypes.MD_REF.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.MIMETYPE.value,
                constants.AttributeTooltips.MIME_TYPE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.LABEL.value,
                constants.AttributeTooltips.MD_WRAP_LABEL.value)
            layout.addRow(label, form_input)

            label, form_input_box = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.LOCTYPE.value,
                constants.AttributeTooltips.LOCTYPE.value,
                True,
                mets.constants.LocatorTypes)
            layout.addRow(label, form_input_box)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.OTHER_LOCTYPE.value,
                constants.AttributeTooltips.OTHER_LOCTYPE.value)

            form_input.setEnabled(False)
            layout.addRow(label, form_input)

            form_input_box.currentIndexChanged.connect(
                lambda idx, box=form_input_box,
                       inpt=form_input: combo_box_other_type_enable(box, inpt))

            label, form_input_box = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.MD_TYPE.value,
                constants.AttributeTooltips.MD_TYPE.value,
                required=True,
                data=mets.constants.MetadataTypes)
            layout.addRow(label, form_input_box)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.MD_TYPE_OTHER.value,
                constants.AttributeTooltips.MD_TYPE_OTHER.value)
            layout.addRow(label, form_input)
            form_input.setEnabled(False)
            form_input_box.currentIndexChanged.connect(
                lambda idx, box=form_input_box,
                       inpt=form_input: combo_box_other_type_enable(box, inpt))

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.MD_TYPE_VERSION.value,
                constants.AttributeTooltips.MD_TYPE_VERSION.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.SIZE.value,
                constants.AttributeTooltips.SIZE.value)
            form_input.setValidator(
                QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*")))
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.DATE_TIME.value,
                constants.Attributes.CREATED.value,
                constants.AttributeTooltips.CREATED.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.CHECKSUM.value,
                constants.AttributeTooltips.CHECKSUM.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.CHECKSUM_TYPE.value,
                constants.AttributeTooltips.CHECKSUM_TYPE.value,
                data=mets.constants.ChecksumTypes)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_HREF.value,
                constants.AttributeTooltips.XLINK_HREF.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ROLE.value,
                constants.AttributeTooltips.XLINK_ROLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ARCROLE.value,
                constants.AttributeTooltips.XLINK_ARCROLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_TITLE.value,
                constants.AttributeTooltips.XLINK_TITLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_SHOW.value,
                constants.AttributeTooltips.XLINK_SHOW.value,
                data=mets.constants.XlinkShowTypes)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_ACTUATE.value,
                constants.AttributeTooltips.XLINK_ACTUATE.value,
                data=mets.constants.XlinkActuateTypes)
            layout.addRow(label, form_input)

        elif tag_type == constants.DescriptiveMetadataTypes.MD_WRAP.value:
            label, form_input_type = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.TYPE.value,
                constants.ElementTooltips.MD_WRAP.value,
                required=True,
                data=constants.DataContentTypes)
            layout.addRow(label, form_input_type)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.MIMETYPE.value,
                constants.AttributeTooltips.MIME_TYPE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.LABEL.value,
                constants.AttributeTooltips.MD_WRAP_LABEL.value)
            layout.addRow(label, form_input)

            label, form_input_box = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.MD_TYPE.value,
                constants.AttributeTooltips.MD_TYPE.value,
                required=True,
                data=mets.constants.MetadataTypes)
            layout.addRow(label, form_input_box)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.MD_TYPE_OTHER.value,
                constants.AttributeTooltips.MD_TYPE_OTHER.value)
            layout.addRow(label, form_input)
            form_input.setEnabled(False)
            form_input_box.currentIndexChanged.connect(
                lambda idx, box=form_input_box,
                       inpt=form_input: combo_box_other_type_enable(box, inpt))

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.MD_TYPE_VERSION.value,
                constants.AttributeTooltips.MD_TYPE_VERSION.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.SIZE.value,
                constants.AttributeTooltips.SIZE.value)
            form_input.setValidator(
                QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*")))
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.DATE_TIME.value,
                constants.Attributes.CREATED.value,
                constants.AttributeTooltips.CREATED.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.CHECKSUM.value,
                constants.AttributeTooltips.CHECKSUM.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.CHECKSUM_TYPE.value,
                constants.AttributeTooltips.CHECKSUM_TYPE.value,
                data=mets.constants.ChecksumTypes)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.TEXT_EDIT.value,
                constants.Labels.CONTENT.value,
                constants.ElementTooltips.MD_WRAP.value,
                required=True)
            layout.addRow(label, form_input)

            label = QLabel(constants.Labels.XML_NAMESPACE_WARNING.value)
            form_input_type.currentIndexChanged.connect(
                lambda idx, box=form_input_type,
                       inpt=label: xml_warning_text_change(box, inpt))
            layout.addRow(None, label)

        return

    def fill_tag_data(self):
        element_type = self.element_type.currentText()
        if element_type == constants.DescriptiveMetadataTypes.MD_REF.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.MD_REF.value
        elif element_type == constants.DescriptiveMetadataTypes.MD_WRAP.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.MD_WRAP.value
        return

    def load_data(self, data):
        self.setWindowTitle(constants.Labels.DIALOG_EDIT_DMD_ELEMENT.value)
        index = self.element_type.findText(
            constants.DescriptiveMetadataTypes[constants.ElementTags(
                data[constants.Labels.TAG.value]).name].value)
        self.element_type.setCurrentIndex(index)
        super().load_data(data)


# administrative metadata child elements creation dialog
class AddAMDElementDialog(CustomDialog):
    def fill_upper_layout(self):
        self.setWindowTitle(constants.Labels.DIALOG_ADD_AMD_ELEMENT.value)
        layout = self.upper_layout
        label = LabelWithTooltip(constants.Labels.METADATA_SECTION_TYPE.value,
                                 '', required=True)
        layout.addWidget(label)
        self.element_type = QComboBox(self)
        i = 0
        for item in constants.AdministrativeMetadataTypes:
            self.element_type.addItem(item.value)
            self.element_type.model().item(i).setToolTip(
                constants.ElementTooltips[item.name].value)
            i += 1

        self.element_type.currentIndexChanged.connect(self.element_type_change)
        layout.addWidget(self.element_type)
        return

    def fill_form_layout(self):
        self.element_type.setCurrentIndex(1)
        self.element_type.setCurrentIndex(0)
        return

    def element_type_change(self):
        tag_type = self.element_type.currentText()
        layout = self.form_layout
        for i in reversed(
                range(
                    layout.count())):  # delete previous widgets when switching element types
            layout.itemAt(i).widget().setParent(None)
        if tag_type in [constants.AdministrativeMetadataTypes.TECH_MD.value,
                        constants.AdministrativeMetadataTypes.RIGHTS_MD.value,
                        constants.AdministrativeMetadataTypes.SOURCE_MD.value,
                        constants.AdministrativeMetadataTypes.DIGIPROV_MD.value]:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.GROUP_ID.value,
                constants.AttributeTooltips.GROUP_ID_METADATA.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ADMID.value,
                constants.AttributeTooltips.ADMID_DMD_SEC.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.DATE_TIME.value,
                constants.Attributes.CREATED.value,
                constants.AttributeTooltips.CREATED_METADATA.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.STATUS.value,
                constants.AttributeTooltips.STATUS.value)
            layout.addRow(label, form_input)

        return

    def fill_tag_data(self):
        element_type = self.element_type.currentText()
        if element_type == constants.AdministrativeMetadataTypes.TECH_MD.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.TECH_MD.value
        elif element_type == constants.AdministrativeMetadataTypes.RIGHTS_MD.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.RIGHTS_MD.value
        elif element_type == constants.AdministrativeMetadataTypes.SOURCE_MD.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.SOURCE_MD.value
        elif element_type == constants.AdministrativeMetadataTypes.DIGIPROV_MD.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.DIGIPROV_MD.value
        return

    def load_data(self, data):
        self.setWindowTitle(constants.Labels.DIALOG_EDIT_AMD_ELEMENT.value)
        index = self.element_type.findText(
            constants.AdministrativeMetadataTypes[constants.ElementTags(
                data[constants.Labels.TAG.value]).name].value)
        self.element_type.setCurrentIndex(index)
        super().load_data(data)


class AddLinkDialog(CustomDialog):
    def __init__(self, parent, data=None):
        self.parent = parent
        super().__init__(data)
        self.setWindowTitle(constants.Labels.DIALOG_ADD_STRUCT_LINK.value)

    def fill_upper_layout(self):
        layout = self.upper_layout
        label = LabelWithTooltip(constants.Labels.DIALOG_ADD_STRUCT_LINK.value,
                                 '', required=True)
        layout.addWidget(label)
        self.element_type = QComboBox(self)
        i = 0
        for item in constants.StructuralLinkTypes:
            self.element_type.addItem(item.value)
            self.element_type.model().item(i).setToolTip(
                constants.ElementTooltips[item.name].value)
            i += 1

        self.element_type.currentIndexChanged.connect(self.element_type_change)
        layout.addWidget(self.element_type)
        return

    def fill_form_layout(self):
        self.restrict_element_types()
        return

    def element_type_change(self):
        tag_type = self.element_type.currentText()
        layout = self.form_layout
        for i in reversed(
                range(
                    layout.count())):  # delete previous widgets when switching element types
            layout.itemAt(i).widget().setParent(None)
        if tag_type == constants.StructuralLinkTypes.STRUCT_LINK.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_FROM.value,
                constants.AttributeTooltips.XLINK_FROM.value,
                required=True)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_TO.value,
                constants.AttributeTooltips.XLINK_TO.value,
                required=True)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ARCROLE.value,
                constants.AttributeTooltips.XLINK_ARCROLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_TITLE.value,
                constants.AttributeTooltips.XLINK_TITLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_SHOW.value,
                constants.AttributeTooltips.XLINK_SHOW.value,
                data=mets.constants.XlinkShowTypes)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_ACTUATE.value,
                constants.AttributeTooltips.XLINK_ACTUATE.value,
                data=mets.constants.XlinkActuateTypes)
            layout.addRow(label, form_input)

        elif tag_type == constants.StructuralLinkTypes.STRUCT_LINK_GROUP.value:

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.ARCLINK_ORDER.value,
                constants.AttributeTooltips.ARCLINK_ORDER.value,
                required=False,
                data=mets.constants.ArclinkOrderTypes)
            layout.addRow(label, form_input)

        elif tag_type == constants.StructuralLinkTypes.LOCATOR_LINK.value:

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_HREF.value,
                constants.AttributeTooltips.XLINK_HREF.value,
                required=True)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_LABEL.value,
                constants.AttributeTooltips.XLINK_LABEL.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ROLE.value,
                constants.AttributeTooltips.XLINK_ROLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_TITLE.value,
                constants.AttributeTooltips.XLINK_TITLE.value)
            layout.addRow(label, form_input)

        elif tag_type == constants.StructuralLinkTypes.ARC_LINK.value:

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ADMID.value,
                constants.AttributeTooltips.ADMID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ARC_TYPE.value,
                constants.AttributeTooltips.ARC_TYPE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_ACTUATE.value,
                constants.AttributeTooltips.XLINK_ACTUATE.value,
                data=mets.constants.XlinkActuateTypes)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ARCROLE.value,
                constants.AttributeTooltips.XLINK_ARCROLE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_FROM.value,
                constants.AttributeTooltips.XLINK_FROM.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_TO.value,
                constants.AttributeTooltips.XLINK_TO.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_SHOW.value,
                constants.AttributeTooltips.XLINK_SHOW.value,
                data=mets.constants.XlinkShowTypes)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_TITLE.value,
                constants.AttributeTooltips.XLINK_TITLE.value)
            layout.addRow(label, form_input)

        return

    def restrict_element_types(self):
        model = self.element_type.model()
        if self.parent is None:
            model.item(2).setEnabled(False)
            model.item(3).setEnabled(False)
            self.element_type.setCurrentIndex(1)
            self.element_type.setCurrentIndex(0)
        else:
            parent_type = self.parent.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value]
            if parent_type == constants.ElementTags.STRUCT_LINK_GROUP.value:
                model.item(0).setEnabled(False)
                model.item(1).setEnabled(False)
                model.item(2).setEnabled(True)
                model.item(3).setEnabled(True)
                self.element_type.setCurrentIndex(2)

        return

    def fill_tag_data(self):
        element_type = self.element_type.currentText()
        if element_type == constants.StructuralLinkTypes.STRUCT_LINK.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.STRUCT_LINK.value
        elif element_type == constants.StructuralLinkTypes.STRUCT_LINK_GROUP.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.STRUCT_LINK_GROUP.value
        elif element_type == constants.StructuralLinkTypes.LOCATOR_LINK.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.LOCATOR_LINK.value
        elif element_type == constants.StructuralLinkTypes.ARC_LINK.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.ARC_LINK.value

        return

    def load_data(self, data):
        self.setWindowTitle(constants.Labels.DIALOG_EDIT_STRUCT_LINK.value)
        index = self.element_type.findText(
            constants.StructuralLinkTypes[constants.ElementTags(
                data[constants.Labels.TAG.value]).name].value)
        self.element_type.setCurrentIndex(index)
        super().load_data(data)


# xml namespace creation dialog
class AddNamespaceDialog(CustomDialog):
    def fill_form_layout(self):
        self.setWindowTitle(constants.Labels.DIALOG_ADD_NAMESPACE.value)
        layout = self.form_layout
        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.NAME.value,
            '',
            required=True)
        layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Labels.VALUE.value,
            '',
            required=True)
        layout.addRow(label, form_input)
        return

    def load_data(self, data):
        self.setWindowTitle(constants.Labels.DIALOG_EDIT_NAMESPACE.value)
        super().load_data(data)

    def fill_tag_data(self):
        self.values[
            constants.Labels.TAG.value] = constants.Labels.NAMESPACES.value
        self.values[constants.Attributes.ID.value] = ''
        return


# behaviour child element creation dialog
class AddBehaviourDialog(CustomDialog):
    def __init__(self, parent, data=None):
        self.parent = parent
        super().__init__(data)
        return

    def fill_upper_layout(self):
        self.setWindowTitle(constants.Labels.DIALOG_ADD_BEHAVIOUR_ELEMENT.value)
        layout = self.upper_layout
        label = LabelWithTooltip(constants.Labels.BEHAVIOUR_SECTION.value, '',
                                 required=True)
        layout.addWidget(label)
        self.element_type = QComboBox(self)
        i = 0
        for item in constants.BehaviourTypes:
            self.element_type.addItem(item.value)
            self.element_type.model().item(i).setToolTip(
                constants.ElementTooltips[item.name].value)
            i += 1

        self.element_type.currentIndexChanged.connect(self.element_type_change)
        layout.addWidget(self.element_type)
        return

    def fill_form_layout(self):
        self.restrict_element_types()
        return

    def restrict_element_types(self):
        model = self.element_type.model()
        if self.parent is None:
            model.item(1).setEnabled(False)
            model.item(2).setEnabled(False)
            model.item(3).setEnabled(False)
            self.element_type.setCurrentIndex(1)
            self.element_type.setCurrentIndex(0)
        else:
            parent_type = self.parent.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value]
            if parent_type == constants.ElementTags.BEHAVIOUR_SEC.value:
                model.item(2).setEnabled(False)
                model.item(3).setEnabled(False)
                self.element_type.setCurrentIndex(1)
                self.element_type.setCurrentIndex(0)
            elif parent_type == constants.ElementTags.BEHAVIOUR.value:
                model.item(0).setEnabled(False)
                model.item(1).setEnabled(False)
                self.element_type.setCurrentIndex(2)
                if self.parent.rowCount() > 0:
                    child = self.parent.child(0).data(Qt.ItemDataRole.UserRole)[
                        constants.Labels.TAG.value]
                    if child == constants.ElementTags.INTERFACE_DEFINITION.value:
                        model.item(2).setEnabled(False)
                        self.element_type.setCurrentIndex(3)
                    else:
                        model.item(3).setEnabled(False)

        return

    def element_type_change(self):
        tag_type = self.element_type.currentText()
        layout = self.form_layout
        for i in reversed(
                range(
                    layout.count())):  # delete previous widgets when switching element types
            layout.itemAt(i).widget().setParent(None)
        if tag_type == constants.BehaviourTypes.BEHAVIOUR_SEC.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.DATE_TIME.value,
                constants.Attributes.CREATED.value,
                constants.AttributeTooltips.CREATED.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.LABEL.value,
                constants.AttributeTooltips.LABEL_BEHAVIOUR_SEC.value)
            layout.addRow(label, form_input)

            label = LabelWithTooltip(constants.Labels.OTHER_ATTRIBS.value,
                                     constants.AttributeTooltips.OTHER_ATTRIBS.value)
            layout.addRow(label, OtherAttributeList(verbose=False))

        elif tag_type == constants.BehaviourTypes.BEHAVIOUR.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ADMID.value,
                constants.AttributeTooltips.ADMID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.BTYPE.value,
                constants.AttributeTooltips.BTYPE.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.DATE_TIME.value,
                constants.Attributes.CREATED.value,
                constants.AttributeTooltips.CREATED.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.GROUP_ID.value,
                constants.AttributeTooltips.GROUP_ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.LABEL.value,
                constants.AttributeTooltips.LABEL_BEHAVIOUR_SEC.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.STRUCTID.value,
                constants.AttributeTooltips.STRUCTID.value)
            layout.addRow(label, form_input)

        elif tag_type == constants.BehaviourTypes.INTERFACE_DEFINITION.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.LABEL.value,
                constants.AttributeTooltips.LABEL.value)
            self.form_layout.addRow(label, form_input)

            label, form_input_box = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.LOCTYPE.value,
                constants.AttributeTooltips.ID.value,
                True,
                data=mets.constants.LocatorTypes)
            self.form_layout.addRow(label, form_input_box)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.OTHER_LOCTYPE.value,
                constants.AttributeTooltips.OTHER_LOCTYPE.value)
            self.form_layout.addRow(label, form_input)

            form_input.setEnabled(False)
            form_input_box.currentIndexChanged.connect(
                lambda idx, box=form_input_box,
                       inpt=form_input: combo_box_other_type_enable(box, inpt))

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_HREF.value,
                constants.AttributeTooltips.XLINK_HREF.value)
            self.form_layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ROLE.value,
                constants.AttributeTooltips.XLINK_ROLE.value)
            self.form_layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ARCROLE.value,
                constants.AttributeTooltips.XLINK_ARCROLE.value)
            self.form_layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_TITLE.value,
                constants.AttributeTooltips.XLINK_TITLE.value)
            self.form_layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_SHOW.value,
                constants.AttributeTooltips.XLINK_SHOW.value,
                data=mets.constants.XlinkShowTypes)
            self.form_layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_ACTUATE.value,
                constants.AttributeTooltips.XLINK_ACTUATE.value,
                data=mets.constants.XlinkActuateTypes)
            self.form_layout.addRow(label, form_input)

        elif tag_type == constants.BehaviourTypes.MECHANISM.value:
            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.ID.value,
                constants.AttributeTooltips.ID.value)
            layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.LABEL.value,
                constants.AttributeTooltips.LABEL.value)
            self.form_layout.addRow(label, form_input)

            label, form_input_box = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.LOCTYPE.value,
                constants.AttributeTooltips.ID.value,
                True,
                data=mets.constants.LocatorTypes)
            self.form_layout.addRow(label, form_input_box)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.OTHER_LOCTYPE.value,
                constants.AttributeTooltips.OTHER_LOCTYPE.value)
            self.form_layout.addRow(label, form_input)

            form_input.setEnabled(False)
            form_input_box.currentIndexChanged.connect(
                lambda idx, box=form_input_box,
                       inpt=form_input: combo_box_other_type_enable(box, inpt))

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_HREF.value,
                constants.AttributeTooltips.XLINK_HREF.value)
            self.form_layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ROLE.value,
                constants.AttributeTooltips.XLINK_ROLE.value)
            self.form_layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_ARCROLE.value,
                constants.AttributeTooltips.XLINK_ARCROLE.value)
            self.form_layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.LINE_EDIT.value,
                constants.Attributes.XLINK_TITLE.value,
                constants.AttributeTooltips.XLINK_TITLE.value)
            self.form_layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_SHOW.value,
                constants.AttributeTooltips.XLINK_SHOW.value,
                data=mets.constants.XlinkShowTypes)
            self.form_layout.addRow(label, form_input)

            label, form_input = create_form_row_items(
                constants.InputTypes.COMBO_BOX.value,
                constants.Attributes.XLINK_ACTUATE.value,
                constants.AttributeTooltips.XLINK_ACTUATE.value,
                data=mets.constants.XlinkActuateTypes)
            self.form_layout.addRow(label, form_input)

        return

    def fill_tag_data(self):
        element_type = self.element_type.currentText()
        if element_type == constants.BehaviourTypes.BEHAVIOUR_SEC.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.BEHAVIOUR_SEC.value
        elif element_type == constants.BehaviourTypes.BEHAVIOUR.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.BEHAVIOUR.value
        elif element_type == constants.BehaviourTypes.INTERFACE_DEFINITION.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.INTERFACE_DEFINITION.value
        elif element_type == constants.BehaviourTypes.MECHANISM.value:
            self.values[
                constants.Labels.TAG.value] = constants.ElementTags.MECHANISM.value
        return

    def load_data(self, data):
        self.setWindowTitle(
            constants.Labels.DIALOG_EDIT_BEHAVIOUR_ELEMENT.value)
        index = self.element_type.findText(
            constants.BehaviourTypes[constants.ElementTags(
                data[constants.Labels.TAG.value]).name].value)
        self.element_type.setCurrentIndex(index)
        super().load_data(data)
