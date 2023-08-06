from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QFrame, QFormLayout, QListWidget, QListWidgetItem

from educelab.mets_gui import constants
from educelab.mets_gui.dialogs import AddNamespaceDialog
from educelab.mets_gui.utils import (LabelWithTooltip, create_form_row_items,
                                     OtherAttributeList, make_item,
                                     create_separator)


class METSTab(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        main_layout.addWidget(LabelWithTooltip(constants.Labels.METS.value,
                                               constants.ElementTooltips.METS.value))

        main_form_layout = QFormLayout()

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.ID.value,
            constants.AttributeTooltips.ID.value)
        main_form_layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.OBJID.value,
            constants.AttributeTooltips.OBJID.value)
        main_form_layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.LABEL.value,
            constants.AttributeTooltips.METS_LABEL.value)
        main_form_layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.TYPE.value,
            constants.AttributeTooltips.TYPE.value)
        main_form_layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.PROFILE.value,
            constants.AttributeTooltips.PROFILE.value)
        main_form_layout.addRow(label, form_input)

        self.main_form_layout = main_form_layout
        main_layout.addLayout(main_form_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        sub_layout = QHBoxLayout()
        schemas_layout = QVBoxLayout()
        label = LabelWithTooltip(constants.Labels.NAMESPACES.value,
                                 constants.AttributeTooltips.NAMESPACES.value)
        schemas_layout.addWidget(label)
        namespace_button_layout = QHBoxLayout()

        namespace_new_button = QPushButton(constants.ButtonText.ADD.value)
        namespace_new_button.setIcon(QIcon(constants.Resources.ICON_ADD.value))
        namespace_new_button.clicked.connect(self.add_schema)
        self.namespace_remove_button = QPushButton(
            constants.ButtonText.REMOVE.value)
        self.namespace_remove_button.setIcon(
            QIcon(constants.Resources.ICON_REMOVE.value))
        self.namespace_remove_button.clicked.connect(self.remove_namespace)
        self.namespace_remove_button.setEnabled(False)
        self.namespace_edit_button = QPushButton(
            constants.ButtonText.EDIT.value)
        self.namespace_edit_button.setIcon(
            QIcon(constants.Resources.ICON_EDIT.value))
        self.namespace_edit_button.clicked.connect(self.edit_namespace)
        self.namespace_edit_button.setEnabled(False)

        namespace_button_layout.addWidget(namespace_new_button)
        namespace_button_layout.addWidget(self.namespace_edit_button)
        namespace_button_layout.addWidget(self.namespace_remove_button)

        self.namespace_list = QListWidget()
        self.namespace_list.currentItemChanged.connect(
            self.namespace_item_change)
        self.namespace_list.doubleClicked.connect(self.edit_namespace)
        schemas_layout.addLayout(namespace_button_layout)
        schemas_layout.addWidget(self.namespace_list)
        sub_layout.addLayout(schemas_layout)

        sub_layout.addWidget(
            create_separator(constants.SeparatorTypes.VERTICAL.value))

        self.other_attribs_list = OtherAttributeList()
        sub_layout.addWidget(self.other_attribs_list)

        main_layout.addLayout(sub_layout)

        self.setLayout(main_layout)

    def add_schema(self):
        dialog = AddNamespaceDialog()
        if dialog.exec():
            values = dialog.values
            item = make_item(values)
            self.namespace_list.addItem(item)
            if self.namespace_list.count() == 1:
                self.namespace_list.setCurrentItem(item)
                # workaround for buggy button disable system
                temp = QListWidgetItem()
                self.namespace_list.addItem(temp)
                self.namespace_list.setCurrentItem(temp)
                self.namespace_list.takeItem(self.namespace_list.currentRow())
        return

    def namespace_item_change(self, current, previous):
        if not current:
            self.namespace_edit_button.setEnabled(False)
            self.namespace_remove_button.setEnabled(False)
        if not previous:
            self.namespace_edit_button.setEnabled(True)
            self.namespace_remove_button.setEnabled(True)
        return

    def remove_namespace(self):
        self.namespace_list.takeItem(self.namespace_list.currentRow())
        return

    def edit_namespace(self):
        item = self.namespace_list.currentItem()
        if item:
            dialog = AddNamespaceDialog(item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                values = dialog.values
                item = make_item(values)

        return

    def load_data(self, values, namespaces, other_attribs):
        layout = self.main_form_layout
        for i in range(1, layout.count(), 2):
            item = layout.itemAt(i).widget()
            item.setText(values[item.key])

        self.namespace_list.clear()
        if namespaces:
            for namespace in namespaces:
                self.namespace_list.addItem(make_item(namespace))

            self.namespace_edit_button.setEnabled(True)
            self.namespace_remove_button.setEnabled(True)
            self.namespace_list.setCurrentRow(0)
        else:
            self.namespace_edit_button.setEnabled(False)
            self.namespace_remove_button.setEnabled(False)

        self.other_attribs_list.load_data(other_attribs)

        return

    def save_data(self) -> tuple[dict, list[QListWidgetItem]]:
        values = {}
        for i in range(1, self.main_form_layout.count(), 2):
            values.update(self.main_form_layout.itemAt(i).widget().data())

        namespaces = []
        for i in range(0, self.namespace_list.model().rowCount()):
            namespaces.append(self.namespace_list.item(i))

        values.update(self.other_attribs_list.data())

        return values, namespaces


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
