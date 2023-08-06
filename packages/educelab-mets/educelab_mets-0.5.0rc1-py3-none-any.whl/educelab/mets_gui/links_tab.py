# sets up a structural links tab for mets gui
from PySide6.QtCore import Qt, QItemSelectionModel
from PySide6.QtGui import QStandardItem, QIcon, QStandardItemModel, QBrush
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QFrame, QTreeView, \
    QLabel, QFormLayout

from educelab.mets_gui import constants
from educelab.mets_gui.dialogs import AddLinkDialog
from educelab.mets_gui.utils import (LabelWithTooltip, create_form_row_items,
                                     InterruptException, make_item)


class LinksTab(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        label = LabelWithTooltip(constants.Labels.STRUCT_LINK_SEC.value,
                                 constants.ElementTooltips.STRUCT_LINK_SEC.value)
        main_layout.addWidget(label)

        # form layout for attribs belonging to the main struct link element
        self.main_form_layout = QFormLayout()

        label, form_input = create_form_row_items(
            constants.InputTypes.LINE_EDIT.value,
            constants.Attributes.ID.value,
            constants.AttributeTooltips.ID.value)
        self.main_form_layout.addRow(label, form_input)

        main_layout.addLayout(self.main_form_layout)

        # separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        label = QLabel(constants.Labels.STRUCT_LINK_ELEMENTS.value)
        main_layout.addWidget(label)

        self.link_view = QTreeView(self)
        self.link_view.setModel(QStandardItemModel())
        self.link_view.header().setVisible(False)
        self.link_view.setSortingEnabled(False)
        self.link_view.selectionModel().currentChanged.connect(
            self.link_item_change)
        self.link_view.model().rowsInserted.connect(self.check_link_groups)
        self.link_view.model().dataChanged.connect(self.check_link_groups)
        self.link_view.doubleClicked.connect(self.edit_link)

        # creation of gui buttons and connection of event listeners to functions
        link_layout = QVBoxLayout()
        link_button_layout = QHBoxLayout()
        link_new_button = QPushButton(constants.ButtonText.ADD.value)
        link_new_button.setIcon(QIcon(constants.Resources.ICON_ADD.value))
        link_new_button.clicked.connect(self.add_link)
        self.link_new_child_button = QPushButton(
            constants.ButtonText.ADD_CHILD.value)
        self.link_new_child_button.setIcon(
            QIcon(constants.Resources.ICON_CHILD_ADD.value))
        self.link_new_child_button.clicked.connect(self.add_link_child)
        self.link_new_child_button.setEnabled(False)
        self.link_remove_button = QPushButton(constants.ButtonText.REMOVE.value)
        self.link_remove_button.setIcon(
            QIcon(constants.Resources.ICON_REMOVE.value))
        self.link_remove_button.clicked.connect(self.remove_link)
        self.link_remove_button.setEnabled(False)
        self.link_edit_button = QPushButton(constants.ButtonText.EDIT.value)
        self.link_edit_button.setIcon(
            QIcon(constants.Resources.ICON_EDIT.value))
        self.link_edit_button.clicked.connect(self.edit_link)
        self.link_edit_button.setEnabled(False)

        link_button_layout.addWidget(link_new_button)
        link_button_layout.addWidget(self.link_new_child_button)
        link_button_layout.addWidget(self.link_edit_button)
        link_button_layout.addWidget(self.link_remove_button)
        link_layout.addLayout(link_button_layout)
        link_layout.addWidget(self.link_view)

        main_layout.addLayout(link_layout)

        self.warning_label = QLabel(constants.Labels.STRUCT_GROUP_WARNING.value)
        self.warning_label.setHidden(True)
        self.warning_label.setStyleSheet('color: red')
        main_layout.addWidget(self.warning_label)

        self.setLayout(main_layout)

        return

    # creates a new window for adding a child item into an item view
    def add_link(self):
        first_addition = False
        index = self.link_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            parent = item.parent()
            if parent is None:
                dialog = AddLinkDialog(parent)
                parent = self.link_view.model().invisibleRootItem()
            else:
                dialog = AddLinkDialog(parent)
        else:
            parent = self.link_view.model().invisibleRootItem()
            dialog = AddLinkDialog(None)
            first_addition = True
        if dialog.exec():
            data = dialog.values
            new_item = make_item(data)
            parent.appendRow(new_item)
            if first_addition:
                ind = new_item.index()
                self.link_view.selectionModel().setCurrentIndex(ind,
                                                                QItemSelectionModel.SelectionFlag.SelectCurrent)
                self.link_edit_button.setEnabled(True)
                self.link_remove_button.setEnabled(True)

        return

    # removes selected item from an item view
    def remove_link(self):
        index = self.link_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            parent = item.parent()
            if parent is None:
                parent = self.link_view.model().invisibleRootItem()
            parent.removeRow(index[0].row())

        return

    # opens a window for editing information about a selected item
    def edit_link(self):
        index = self.link_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            dialog = AddLinkDialog(item.parent(),
                                   item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                values = dialog.values
                item = make_item(values, item)

        return

    # event listener function for enabling/disabling gui buttons based
    # on status of item view
    def link_item_change(self, current, previous):
        if current.model():
            item = current.model().itemFromIndex(current)
            if item.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value] in \
                    [constants.ElementTags.LOCATOR_LINK.value,
                     constants.ElementTags.ARC_LINK.value,
                     constants.ElementTags.STRUCT_LINK.value]:
                self.link_new_child_button.setDisabled(True)
            else:
                self.link_new_child_button.setDisabled(False)
        else:
            self.link_new_child_button.setDisabled(True)
            self.link_edit_button.setDisabled(True)
            self.link_remove_button.setDisabled(True)
        return

    # creates a new window for adding a child item into an item view
    def add_link_child(self):
        index = self.link_view.selectedIndexes()
        if index:
            parent = index[0].model().itemFromIndex(index[0])
            dialog = AddLinkDialog(parent)
        else:
            parent = self.link_view.model().invisibleRootItem()
            dialog = AddLinkDialog(None)
        if dialog.exec():
            data = dialog.values
            new_item = make_item(data)
            parent.appendRow(new_item)

        return

    # function for validating individual items in the item view
    # if any item is missing required parts, a warning will be displayed
    def check_link_groups(self):
        model = self.link_view.model()
        rows = model.rowCount()
        valid = True
        for i in range(0, rows):
            item = model.itemFromIndex(model.index(i, 0))
            if item.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value] == \
                    constants.ElementTags.STRUCT_LINK_GROUP.value:
                locator_count = 0
                arc_count = 0
                for j in range(item.rowCount()):
                    child = item.child(j)
                    if child.data(Qt.ItemDataRole.UserRole)[
                        constants.Labels.TAG.value] == \
                            constants.ElementTags.LOCATOR_LINK.value:
                        locator_count += 1
                    elif child.data(Qt.ItemDataRole.UserRole)[
                        constants.Labels.TAG.value] == \
                            constants.ElementTags.ARC_LINK.value:
                        arc_count += 1
                if locator_count > 1 and arc_count > 0:
                    self.warning_label.setHidden(True)
                    item.setBackground(QBrush(Qt.GlobalColor.white))
                else:
                    self.warning_label.setHidden(False)
                    item.setBackground(QBrush(Qt.GlobalColor.red))
                    valid = False

        return valid

    # function for loading data into tab
    # clears previous data and adds newly loaded information
    # resets gui buttons
    def load_data(self, values, links):
        layout = self.main_form_layout
        for i in range(1, layout.count(), 2):
            item = layout.itemAt(i).widget()
            item.setText(values[item.key])

        self.link_view.clear()
        if links:
            for link in links:
                self.link_view.addItem(link)

            self.link_edit_button.setEnabled(True)
            self.link_remove_button.setEnabled(True)
            self.link_new_child_button.setEnabled(True)
            self.link_view.setCurrentRow(0)
        else:
            self.link_edit_button.setEnabled(False)
            self.link_remove_button.setEnabled(False)
            self.link_new_child_button.setEnabled(False)
        return

    # packages current gui information for convertor function
    def save_data(self) -> tuple[dict, list[QStandardItem]]:
        if self.check_link_groups():
            values = {}
            for i in range(1, self.main_form_layout.count(), 2):
                values.update(self.main_form_layout.itemAt(i).widget().data())

            items = []
            for i in range(0, self.link_view.model().rowCount()):
                items.append(
                    self.link_view.model().invisibleRootItem().child(i))

            return values, items

        else:
            raise InterruptException(
                constants.Labels.STRUCT_GROUP_WARNING.value)
