from PySide6.QtCore import Qt, QItemSelectionModel, QDate
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QPushButton, \
    QHBoxLayout, QFrame, QTreeView, \
    QLabel, QFormLayout, QListView

from educelab.mets_gui import constants
from educelab.mets_gui.dialogs import AddMetadataSectionDialog, \
    AddDMDElementDialog, AddAMDElementDialog
from educelab.mets_gui.utils import CustomListItem, create_form_row_items, \
    InputLine, InputChoice, InputDateTime, make_item


class MetadataTab(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        metadata_label = QLabel(constants.Labels.METADATA_SECTIONS.value)
        main_layout.addWidget(metadata_label)

        self.metadata_view = QListWidget(self)
        self.metadata_view.setFixedHeight(84)  # get it in-line with buttons
        self.metadata_view.currentItemChanged.connect(self.metadata_item_change)
        self.metadata_view.doubleClicked.connect(self.edit_metadata)

        metadata_layout = QHBoxLayout()
        metadata_layout.addWidget(self.metadata_view)

        metadata_button_layout = QVBoxLayout()
        metadata_new_button = QPushButton(constants.ButtonText.ADD.value)
        metadata_new_button.setIcon(QIcon(constants.Resources.ICON_ADD.value))
        metadata_new_button.clicked.connect(self.add_metadata)
        self.metadata_remove_button = QPushButton(
            constants.ButtonText.REMOVE.value)
        self.metadata_remove_button.setIcon(
            QIcon(constants.Resources.ICON_REMOVE.value))
        self.metadata_remove_button.clicked.connect(self.remove_metadata)
        self.metadata_remove_button.setEnabled(False)
        self.metadata_edit_button = QPushButton(constants.ButtonText.EDIT.value)
        self.metadata_edit_button.setIcon(
            QIcon(constants.Resources.ICON_EDIT.value))
        self.metadata_edit_button.clicked.connect(self.edit_metadata)
        self.metadata_edit_button.setEnabled(False)

        metadata_button_layout.addWidget(metadata_new_button)
        metadata_button_layout.addWidget(self.metadata_edit_button)
        metadata_button_layout.addWidget(self.metadata_remove_button)
        metadata_button_layout.addStrut(
            90)  # stop struct map part from being affected by resize of the main window
        metadata_layout.addLayout(metadata_button_layout)

        main_layout.addLayout(metadata_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        metadata_content = QWidget()
        self.metadata_content_layout = QVBoxLayout()
        metadata_content.setLayout(self.metadata_content_layout)
        self.metadata_content_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(metadata_content, stretch=1)

        self.setLayout(main_layout)

        return

    def add_metadata(self):
        dialog = AddMetadataSectionDialog()
        if dialog.exec():
            values = dialog.values
            item = make_item(values)
            self.metadata_view.addItem(item)
            if self.metadata_view.count() == 1:
                self.metadata_view.setCurrentItem(item)

        return

    def metadata_item_change(self, current, previous):
        child = self.metadata_content_layout.itemAt(0)
        if child:
            child.widget().save_edits()
            child.widget().setParent(None)
        if current:
            mtd_type = current.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value]
            if mtd_type == constants.ElementTags.AMD_SEC.value:
                self.metadata_content_layout.addWidget(AMDWidget(current))
            elif mtd_type == constants.ElementTags.DMD_SEC.value:
                self.metadata_content_layout.addWidget(DMDWidget(current))
        else:
            self.metadata_remove_button.setEnabled(False)
            self.metadata_edit_button.setEnabled(False)
        if not previous:
            self.metadata_remove_button.setEnabled(True)
            self.metadata_edit_button.setEnabled(True)

        return

    def remove_metadata(self):
        self.metadata_view.takeItem(self.metadata_view.currentRow())
        return

    def edit_metadata(self):
        item = self.metadata_view.currentItem()
        if item:
            dialog = AddMetadataSectionDialog(
                item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                values = dialog.values
                item = make_item(values, item)

        return

    def load_data(self, data):
        self.metadata_view.clear()
        if data:
            for item in data:
                self.metadata_view.addItem(item)
            self.metadata_view.setCurrentRow(0)
        return

    def save_data(self) -> list[CustomListItem]:
        data = []
        self.metadata_content_layout.itemAt(0).widget().save_edits()
        for i in range(self.metadata_view.count()):
            data.append(self.metadata_view.item(i))
        return data


class AMDWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        tree_label = QLabel(constants.Labels.AMD_ELEMENTS.value)
        main_layout.addWidget(tree_label)

        tree_button_layout = QHBoxLayout()
        self.tree_new_button = QPushButton(constants.ButtonText.ADD.value)
        self.tree_new_button.setIcon(QIcon(constants.Resources.ICON_ADD.value))
        self.tree_new_button.clicked.connect(self.add_tree_item)
        self.tree_new_child_button = QPushButton(
            constants.ButtonText.ADD_CHILD.value)
        self.tree_new_child_button.setIcon(
            QIcon(constants.Resources.ICON_CHILD_ADD.value))
        self.tree_new_child_button.clicked.connect(self.add_tree_child)
        self.tree_new_child_button.setEnabled(False)
        self.tree_remove_button = QPushButton(constants.ButtonText.REMOVE.value)
        self.tree_remove_button.setIcon(
            QIcon(constants.Resources.ICON_REMOVE.value))
        self.tree_remove_button.clicked.connect(self.remove_tree_item)
        self.tree_remove_button.setEnabled(False)
        self.tree_edit_button = QPushButton(constants.ButtonText.EDIT.value)
        self.tree_edit_button.setIcon(
            QIcon(constants.Resources.ICON_EDIT.value))
        self.tree_edit_button.clicked.connect(self.edit_tree_item)
        self.tree_edit_button.setEnabled(False)

        tree_button_layout.addWidget(self.tree_new_button)
        tree_button_layout.addWidget(self.tree_new_child_button)
        tree_button_layout.addWidget(self.tree_edit_button)
        tree_button_layout.addWidget(self.tree_remove_button)
        main_layout.addLayout(tree_button_layout)

        self.tree_view = QTreeView(self)
        self.tree_view.setModel(parent.model)
        self.tree_view.selectionModel().currentChanged.connect(
            self.tree_item_change)
        self.tree_view.header().setVisible(False)
        self.tree_view.setSortingEnabled(False)
        self.tree_view.doubleClicked.connect(self.edit_tree_item)

        main_layout.addWidget(self.tree_view)

        self.setLayout(main_layout)

    def add_tree_item(self):
        first_addition = False
        index = self.tree_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            parent = item.parent()
            if parent is None:
                dialog = AddAMDElementDialog()
                parent = self.tree_view.model().invisibleRootItem()
            else:
                dialog = AddDMDElementDialog(parent)
        else:
            parent = self.tree_view.model().invisibleRootItem()
            dialog = AddAMDElementDialog(None)
            first_addition = True

        if dialog.exec():
            data = dialog.values
            new_item = make_item(data)
            parent.appendRow(new_item)
            if first_addition:
                ind = new_item.index()
                self.tree_view.selectionModel().setCurrentIndex(ind,
                                                                QItemSelectionModel.SelectionFlag.SelectCurrent)
                self.tree_edit_button.setEnabled(True)
                self.tree_remove_button.setEnabled(True)

            self.tree_item_change(self.tree_view.selectedIndexes()[0], None)

        return

    def remove_tree_item(self):
        index = self.tree_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            parent = item.parent()
            if parent is None:
                parent = self.tree_view.model().invisibleRootItem()
            parent.removeRow(index[0].row())
        return

    def tree_item_change(self, current, previous):
        if current.model():
            item = current.model().itemFromIndex(current)
            if item.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value] in \
                    [constants.ElementTags.MD_REF.value,
                     constants.ElementTags.MD_WRAP.value]:
                self.tree_new_child_button.setDisabled(True)
                if item.parent().rowCount() == 2:
                    self.tree_new_button.setDisabled(True)
                else:
                    self.tree_new_button.setDisabled(False)

            else:
                self.tree_new_button.setDisabled(False)
                self.tree_new_child_button.setDisabled(False)
                if item.rowCount() == 2:
                    self.tree_new_child_button.setDisabled(True)
                else:
                    self.tree_new_child_button.setDisabled(False)
        else:
            self.tree_new_child_button.setDisabled(True)
            self.tree_edit_button.setDisabled(True)
            self.tree_remove_button.setDisabled(True)
        return

    def add_tree_child(self):
        index = self.tree_view.selectedIndexes()
        if index:
            parent = index[0].model().itemFromIndex(index[0])
            dialog = AddDMDElementDialog(parent)
            if dialog.exec():
                data = dialog.values
                new_item = make_item(data)
                parent.appendRow(new_item)

                self.tree_item_change(self.tree_view.selectedIndexes()[0], None)

        return

    def edit_tree_item(self):
        index = self.tree_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            if index[0].parent().column() == 0:
                dialog = AddDMDElementDialog(index[0].parent(), item.data(
                    Qt.ItemDataRole.UserRole))
            else:
                dialog = AddAMDElementDialog(
                    item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                data = dialog.values
                item = make_item(data, item)

        return

    def load_data(self, data):
        return

    def save_data(self):
        return

    def save_edits(self):
        return


class DMDWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_form_layout = QFormLayout()

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.GROUP_ID.value,
            constants.AttributeTooltips.GROUP_ID_METADATA.value)
        main_form_layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.ADMID.value,
            constants.AttributeTooltips.ADMID_DMD_SEC.value)
        main_form_layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.DATE_TIME.value,
            constants.Attributes.CREATED.value,
            constants.AttributeTooltips.CREATED_METADATA.value)
        main_form_layout.addRow(label, form_input)

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.STATUS.value,
            constants.AttributeTooltips.STATUS.value)
        main_form_layout.addRow(label, form_input)

        self.main_form_layout = main_form_layout
        main_layout.addLayout(main_form_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        metadata_label = QLabel(constants.Labels.DMD_ELEMENTS.value)
        main_layout.addWidget(metadata_label)

        self.metadata_view = QListView(self)
        self.metadata_view.setModel(parent.model)
        self.metadata_view.doubleClicked.connect(self.edit_metadata)
        self.metadata_view.selectionModel().currentChanged.connect(
            self.metadata_item_change)

        metadata_layout = QHBoxLayout()
        metadata_layout.addWidget(self.metadata_view)

        metadata_button_layout = QVBoxLayout()
        self.metadata_new_button = QPushButton(constants.ButtonText.ADD.value)
        self.metadata_new_button.setIcon(
            QIcon(constants.Resources.ICON_ADD.value))
        self.metadata_new_button.clicked.connect(self.add_metadata)
        self.metadata_remove_button = QPushButton(
            constants.ButtonText.REMOVE.value)
        self.metadata_remove_button.setIcon(
            QIcon(constants.Resources.ICON_REMOVE.value))
        self.metadata_remove_button.clicked.connect(self.remove_metadata)
        self.metadata_remove_button.setEnabled(False)
        self.metadata_edit_button = QPushButton(constants.ButtonText.EDIT.value)
        self.metadata_edit_button.setIcon(
            QIcon(constants.Resources.ICON_EDIT.value))
        self.metadata_edit_button.clicked.connect(self.edit_metadata)
        self.metadata_edit_button.setEnabled(False)

        metadata_button_layout.addWidget(self.metadata_new_button)
        metadata_button_layout.addWidget(self.metadata_edit_button)
        metadata_button_layout.addWidget(self.metadata_remove_button)
        metadata_button_layout.addStretch()
        metadata_layout.addLayout(metadata_button_layout)

        main_layout.addLayout(metadata_layout)

        self.setLayout(main_layout)

        self.fill_data(parent.data(Qt.ItemDataRole.UserRole))

        return

    def add_metadata(self):
        parent = self.metadata_view.model().invisibleRootItem()
        dialog = AddDMDElementDialog(parent)
        if dialog.exec():
            values = dialog.values
            item = make_item(values)
            parent.appendRow(item)
            if self.metadata_view.model().rowCount() == 1:
                ind = item.index()
                self.metadata_view.setCurrentIndex(ind)
                self.metadata_edit_button.setEnabled(True)
                self.metadata_remove_button.setEnabled(True)
            self.metadata_item_change(self.metadata_view.selectedIndexes()[0],
                                      None)

        return

    def metadata_item_change(self, current, previous):
        if not current:
            self.metadata_remove_button.setEnabled(False)
            self.metadata_edit_button.setEnabled(False)
        if not previous:
            self.metadata_remove_button.setEnabled(True)
            self.metadata_edit_button.setEnabled(True)
        if self.metadata_view.model().invisibleRootItem().rowCount() == 2:
            self.metadata_new_button.setEnabled(False)
        else:
            self.metadata_new_button.setEnabled(True)

        return

    def remove_metadata(self):
        index = self.metadata_view.selectedIndexes()
        if index:
            parent = self.metadata_view.model().invisibleRootItem()
            parent.removeRow(index[0].row())

        if self.metadata_view.model().rowCount() == 0:
            self.metadata_edit_button.setEnabled(False)
            self.metadata_remove_button.setEnabled(False)

        return

    def edit_metadata(self):
        index = self.metadata_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            dialog = AddDMDElementDialog(item.parent(),
                                         item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                values = dialog.values
                item = make_item(values, item)

        return

    def fill_data(self, data):
        for i in range(1, self.main_form_layout.count(), 2):
            item = self.main_form_layout.itemAt(i).widget()
            if item.key in data.keys():
                if type(item) == InputLine:
                    item.setText(data[item.key])
                elif type(item) == InputChoice:
                    item_index = item.findText(data[item.key])
                    item.setCurrentIndex(item_index)
                elif type(item) == InputDateTime:
                    if not data[item.key]:
                        item.toggle.setChecked(True)
                    else:
                        item.input_datetime.setDate(
                            QDate.fromString(data[item.key],
                                             Qt.DateFormat.ISODate))

        return

    def load_data(self, data):
        return

    def save_data(self):
        return

    def save_edits(self):
        data = self.parent.data(Qt.ItemDataRole.UserRole)
        for i in range(1, self.main_form_layout.count(), 2):
            data.update(self.main_form_layout.itemAt(i).widget().data())
        self.parent.setData(Qt.ItemDataRole.UserRole, data)
        return
