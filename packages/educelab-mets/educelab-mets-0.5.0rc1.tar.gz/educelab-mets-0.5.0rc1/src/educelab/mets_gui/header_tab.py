# sets up a header tab for mets gui
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QFrame, QFormLayout, QListWidget, QListWidgetItem, QLabel

from educelab.mets_gui import constants
from educelab.mets_gui.dialogs import AddAgentDialog, AddAltIDDialog
from educelab.mets_gui.utils import (LabelWithTooltip, create_form_row_items,
                                     InputLine, InputText, InputDateTime,
                                     make_item)


class HeaderTab(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        main_layout.addWidget(LabelWithTooltip(constants.Labels.HEADER.value,
                                               constants.ElementTooltips.HEADER.value))

        # form layout for attribs belonging to the main header element
        main_form_layout = QFormLayout()

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.ID.value,
            constants.AttributeTooltips.ID.value)
        main_form_layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.ADMID.value,
            constants.AttributeTooltips.ADMID.value)
        main_form_layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.DATE_TIME.value,
            constants.Attributes.CREATE_DATE.value,
            constants.AttributeTooltips.CREATE_DATE.value)
        main_form_layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.DATE_TIME.value,
            constants.Attributes.LAST_MOD_DATE.value,
            constants.AttributeTooltips.LAST_MOD_DATE.value)
        main_form_layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.RECORD_STATUS.value,
            constants.AttributeTooltips.RECORD_STATUS.value)
        main_form_layout.addRow(label, form_input)

        label = QLabel(constants.Attributes.METS_DOCUMENT_ID.value)
        form_input = METSElementIDWidget()
        main_form_layout.addRow(label, form_input)

        self.main_form_layout = main_form_layout
        main_layout.addLayout(main_form_layout)

        # separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        # layout housing list widgets for agents and alternative ids
        sub_layout = QHBoxLayout()
        agents_layout = QVBoxLayout()
        agents_label = LabelWithTooltip(constants.Labels.AGENT.value,
                                        constants.ElementTooltips.AGENT.value,
                                        stretch=True)
        agents_layout.addWidget(agents_label)
        agents_list_button_layout = QHBoxLayout()

        agents_list_new_button = QPushButton(constants.ButtonText.ADD.value)
        agents_list_new_button.setIcon(
            QIcon(constants.Resources.ICON_ADD.value))
        agents_list_new_button.clicked.connect(self.add_agent)
        self.agents_list_remove_button = QPushButton(
            constants.ButtonText.REMOVE.value)
        self.agents_list_remove_button.setIcon(
            QIcon(constants.Resources.ICON_REMOVE.value))
        self.agents_list_remove_button.clicked.connect(self.remove_agent)
        self.agents_list_remove_button.setEnabled(False)
        self.agents_list_edit_button = QPushButton(
            constants.ButtonText.EDIT.value)
        self.agents_list_edit_button.setIcon(
            QIcon(constants.Resources.ICON_EDIT.value))
        self.agents_list_edit_button.clicked.connect(self.edit_agent)
        self.agents_list_edit_button.setEnabled(False)

        agents_list_button_layout.addWidget(agents_list_new_button)
        agents_list_button_layout.addWidget(self.agents_list_edit_button)
        agents_list_button_layout.addWidget(self.agents_list_remove_button)

        self.agents_list = QListWidget()
        self.agents_list.currentItemChanged.connect(self.agent_item_change)
        self.agents_list.doubleClicked.connect(self.edit_agent)
        agents_layout.addLayout(agents_list_button_layout)
        agents_layout.addWidget(self.agents_list)
        sub_layout.addLayout(agents_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        sub_layout.addWidget(separator)

        alt_id_layout = QVBoxLayout()
        alt_id_label = LabelWithTooltip(constants.Labels.ALT_RECORD_ID.value,
                                        constants.ElementTooltips.ALT_RECORD_ID.value,
                                        stretch=True)
        alt_id_layout.addWidget(alt_id_label)

        alt_id_list_button_layout = QHBoxLayout()

        alt_id_list_new_button = QPushButton(constants.ButtonText.ADD.value)
        alt_id_list_new_button.setIcon(
            QIcon(constants.Resources.ICON_ADD.value))
        alt_id_list_new_button.clicked.connect(self.add_alt_id)
        alt_id_list_remove_button = QPushButton(
            constants.ButtonText.REMOVE.value)
        alt_id_list_remove_button.setIcon(
            QIcon(constants.Resources.ICON_REMOVE.value))
        alt_id_list_remove_button.clicked.connect(self.remove_alt_id)
        alt_id_list_remove_button.setEnabled(False)
        self.alt_id_list_remove_button = alt_id_list_remove_button
        alt_id_list_edit_button = QPushButton(constants.ButtonText.EDIT.value)
        alt_id_list_edit_button.setIcon(
            QIcon(constants.Resources.ICON_EDIT.value))
        alt_id_list_edit_button.clicked.connect(self.edit_alt_id)
        alt_id_list_edit_button.setEnabled(False)
        self.alt_id_list_edit_button = alt_id_list_edit_button

        alt_id_list_button_layout.addWidget(alt_id_list_new_button)
        alt_id_list_button_layout.addWidget(alt_id_list_edit_button)
        alt_id_list_button_layout.addWidget(alt_id_list_remove_button)

        self.alt_id_list = QListWidget()
        self.alt_id_list.currentItemChanged.connect(self.alt_id_item_change)
        self.alt_id_list.doubleClicked.connect(self.edit_alt_id)
        alt_id_layout.addLayout(alt_id_list_button_layout)
        alt_id_layout.addWidget(self.alt_id_list)

        sub_layout.addLayout(alt_id_layout)

        main_layout.addLayout(sub_layout)

        self.setLayout(main_layout)

    def add_agent(self):
        dialog = AddAgentDialog()
        if dialog.exec():
            values = dialog.values
            item = make_item(values)
            self.agents_list.addItem(item)
            if self.agents_list.count() == 1:
                self.agents_list.setCurrentItem(item)
                # workaround for buggy button disable system
                temp = QListWidgetItem()
                self.agents_list.addItem(temp)
                self.agents_list.setCurrentItem(temp)
                self.agents_list.takeItem(self.agents_list.currentRow())
        return

    def agent_item_change(self, current, previous):
        if not current:
            self.agents_list_edit_button.setEnabled(False)
            self.agents_list_remove_button.setEnabled(False)
        if not previous:
            self.agents_list_edit_button.setEnabled(True)
            self.agents_list_remove_button.setEnabled(True)
        return

    def remove_agent(self):
        self.agents_list.takeItem(self.agents_list.currentRow())
        return

    def edit_agent(self):
        item = self.agents_list.currentItem()
        if item:
            dialog = AddAgentDialog(item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                values = dialog.values
                item = make_item(values, item)

        return

    def add_alt_id(self):
        dialog = AddAltIDDialog()
        if dialog.exec():
            values = dialog.values
            item = make_item(values)
            self.alt_id_list.addItem(item)
            if self.alt_id_list.count() == 1:
                self.alt_id_list.setCurrentItem(item)
                # workaround for buggy button disable system
                temp = QListWidgetItem()
                self.alt_id_list.addItem(temp)
                self.alt_id_list.setCurrentItem(temp)
                self.alt_id_list.takeItem(self.alt_id_list.currentRow())

        return

    def alt_id_item_change(self, current, previous):
        if not current:
            self.alt_id_list_edit_button.setEnabled(False)
            self.alt_id_list_remove_button.setEnabled(False)
        if not previous:
            self.alt_id_list_edit_button.setEnabled(True)
            self.alt_id_list_remove_button.setEnabled(True)
        return

    def remove_alt_id(self):
        self.alt_id_list.takeItem(self.alt_id_list.currentRow())
        return

    def edit_alt_id(self):
        item = self.alt_id_list.currentItem()
        if item:
            dialog = AddAltIDDialog(item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                values = dialog.values
                item = make_item(values, item)

        return

    def load_data(self, values, agents, alt_record_ids, mets_document_id):
        layout = self.main_form_layout
        for i in range(1, layout.count(), 2):
            item = layout.itemAt(i).widget()
            if type(item) in [InputLine, InputText]:
                item.setText(values[item.key])
            elif type(item) == METSElementIDWidget:
                if mets_document_id:
                    item.fill_data(mets_document_id)
            elif type(item) == InputDateTime:
                item.load_data(values[item.key])

        self.agents_list.clear()
        if agents:
            for agent in agents:
                self.agents_list.addItem(agent)

            self.agents_list_edit_button.setEnabled(True)
            self.agents_list_remove_button.setEnabled(True)
            self.agents_list.setCurrentRow(0)
        else:
            self.agents_list_edit_button.setEnabled(False)
            self.agents_list_remove_button.setEnabled(False)

        self.alt_id_list.clear()
        if alt_record_ids:
            for alt_record_id in alt_record_ids:
                self.alt_id_list.addItem(alt_record_id)

            self.alt_id_list_edit_button.setEnabled(True)
            self.alt_id_list_remove_button.setEnabled(True)
            self.alt_id_list.setCurrentRow(0)

        else:
            self.alt_id_list_edit_button.setEnabled(False)
            self.alt_id_list_remove_button.setEnabled(False)
        return

    def save_data(self) -> tuple[dict, list[dict], list[dict]]:
        values = {}
        for i in range(1, self.main_form_layout.count(), 2):
            values.update(self.main_form_layout.itemAt(i).widget().data())

        agents = []
        for i in range(0, self.agents_list.model().rowCount()):
            agents.append(
                self.agents_list.item(i).data(Qt.ItemDataRole.UserRole))

        alt_record_ids = []
        for i in range(0, self.alt_id_list.model().rowCount()):
            alt_record_ids.append(
                self.alt_id_list.item(i).data(Qt.ItemDataRole.UserRole))

        return values, agents, alt_record_ids


# mets document id element has multiple parts
# this widget is used to pack them all into one
class METSElementIDWidget(QWidget):
    def __init__(self, data=None):
        super().__init__()
        self.values = {}
        layout = QHBoxLayout()
        label, self.value = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Labels.VALUE.value,
            constants.ElementTooltips.METS_DOCUMENT_ID.value)
        layout.addWidget(label)
        layout.addWidget(self.value)
        label, self.id = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.ID.value,
            constants.AttributeTooltips.ID.value)
        layout.addWidget(label)
        layout.addWidget(self.id)
        label, self.type = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.TYPE.value,
            constants.AttributeTooltips.IDENTIFIER_TYPE.value)
        layout.addWidget(label)
        layout.addWidget(self.type)

        self.setLayout(layout)
        if data:
            self.fill_data(data)

    def data(self):
        self.values = {}
        self.values.update(self.value.data())
        self.values.update(self.id.data())
        self.values.update(self.type.data())
        return {constants.Attributes.METS_DOCUMENT_ID.value: self.values}

    def fill_data(self, data):
        self.value.setText(data[self.value.key])
        self.id.setText(data[self.id.key])
        self.type.setText(data[self.type.key])
        return
