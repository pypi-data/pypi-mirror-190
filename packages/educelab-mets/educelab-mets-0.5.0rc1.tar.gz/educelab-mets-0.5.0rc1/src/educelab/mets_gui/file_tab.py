# sets up a file section tab for mets gui
from PySide6.QtCore import Qt, QItemSelectionModel
from PySide6.QtGui import QStandardItem, QIcon, QStandardItemModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QFrame, QStyle, QTreeView, \
    QLabel, QFormLayout

from educelab.mets_gui import constants
from educelab.mets_gui.dialogs import AddFileSecItemDialog
from educelab.mets_gui.utils import (LabelWithTooltip, create_form_row_items,
                                     InputLine, make_item)


class FileTab(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        label = LabelWithTooltip(constants.Labels.FILE_SEC.value,
                                 constants.ElementTooltips.FILE_SEC.value)
        main_layout.addWidget(label)

        # form layout for attribs belonging to the main file section element
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

        tree_label = QLabel(constants.Labels.FILE_SEC_TREE.value)
        main_layout.addWidget(tree_label)

        # creation of gui buttons and connection of event listeners to functions
        tree_button_layout = QHBoxLayout()
        self.tree_new_button = QPushButton(constants.ButtonText.ADD.value)
        self.tree_new_button.setIcon(QIcon(constants.Resources.ICON_ADD.value))
        self.tree_new_button.clicked.connect(self.add_tree_item)
        self.tree_new_child_button = QPushButton(
            constants.ButtonText.ADD_CHILD.value)
        self.tree_new_child_button.setIcon(
            QIcon(constants.Resources.ICON_CHILD_ADD.value))
        self.tree_new_child_button.clicked.connect(self.add_tree_child)
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
        self.tree_up_button = QPushButton(constants.ButtonText.UP.value)
        self.tree_up_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp))
        self.tree_up_button.clicked.connect(
            lambda checked,
                   direction=self.tree_up_button.text(): self.move_tree_item(
                direction))
        self.tree_up_button.setEnabled(False)
        self.tree_down_button = QPushButton(constants.ButtonText.DOWN.value)
        self.tree_down_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
        self.tree_down_button.clicked.connect(
            lambda checked,
                   direction=self.tree_down_button.text(): self.move_tree_item(
                direction))
        self.tree_down_button.setEnabled(False)
        tree_button_layout.addWidget(self.tree_new_button)
        tree_button_layout.addWidget(self.tree_new_child_button)
        tree_button_layout.addWidget(self.tree_edit_button)
        tree_button_layout.addWidget(self.tree_remove_button)
        tree_button_layout.addWidget(self.tree_up_button)
        tree_button_layout.addWidget(self.tree_down_button)
        main_layout.addLayout(tree_button_layout)

        # tree view for file section elements
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(QStandardItemModel())
        self.tree_view.header().setVisible(False)
        self.tree_view.setSortingEnabled(False)
        self.tree_view.doubleClicked.connect(self.edit_tree_item)
        self.tree_view.selectionModel().currentChanged.connect(
            self.tree_item_change)

        main_layout.addWidget(self.tree_view)
        # main_layout.addStretch(1)

        self.setLayout(main_layout)

        return

    # creates a new window for adding an item into a tree view
    def add_tree_item(self):
        first_addition = False
        index = self.tree_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            parent = item.parent()
            if parent is None:
                dialog = AddFileSecItemDialog(parent)
                parent = self.tree_view.model().invisibleRootItem()
            else:
                dialog = AddFileSecItemDialog(parent)
        else:
            parent = self.tree_view.model().invisibleRootItem()
            dialog = AddFileSecItemDialog(None)
            first_addition = True
        if dialog.exec():
            data = dialog.values
            new_item = make_item(data)
            parent.appendRow(new_item)
            if first_addition:  # activates gui buttons after adding a first entry
                ind = new_item.index()
                self.tree_view.selectionModel().setCurrentIndex(ind,
                                                                QItemSelectionModel.SelectionFlag.SelectCurrent)
                self.tree_edit_button.setEnabled(True)
                self.tree_remove_button.setEnabled(True)
                self.tree_up_button.setEnabled(True)
                self.tree_down_button.setEnabled(True)

        return

    # removes selected item from a tree view
    def remove_tree_item(self):
        index = self.tree_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            parent = item.parent()
            if parent is None:
                parent = self.tree_view.model().invisibleRootItem()
            parent.removeRow(index[0].row())
        return

    # listener function for change of currently selected item
    # enables/disables gui buttons based on the type of selected element
    def tree_item_change(self, current, previous):
        if current.model():
            item = current.model().itemFromIndex(current)
            if item.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value] in \
                    [constants.ElementTags.FILE_LOCATION.value,
                     constants.ElementTags.FILE_CONTENT.value,
                     constants.ElementTags.STREAM.value,
                     constants.ElementTags.TRANSFORM_FILE.value]:
                self.tree_new_child_button.setDisabled(True)
            else:
                self.tree_new_child_button.setDisabled(False)
        else:
            self.tree_new_child_button.setDisabled(True)
            self.tree_edit_button.setDisabled(True)
            self.tree_remove_button.setDisabled(True)
            self.tree_up_button.setDisabled(True)
            self.tree_down_button.setDisabled(True)
        return

    # creates a new window for adding a child item into a tree view
    def add_tree_child(self):
        index = self.tree_view.selectedIndexes()
        if index:
            parent = index[0].model().itemFromIndex(index[0])
            dialog = AddFileSecItemDialog(parent)
        else:
            parent = self.tree_view.model().invisibleRootItem()
            dialog = AddFileSecItemDialog(None)
        if dialog.exec():
            data = dialog.values
            new_item = make_item(data)
            parent.appendRow(new_item)

        return

    # opens a window for editing information about a selected item
    def edit_tree_item(self):
        index = self.tree_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            dialog = AddFileSecItemDialog(item.parent(),
                                          item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                data = dialog.values
                item = make_item(data, item)
        return

    # function for moving tree items within the tree hierarchy
    # used for changing order of elements without having to delete items above or below
    def move_tree_item(self, direction):
        index = self.tree_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            parent = item.parent()
            if not parent:
                parent = self.tree_view.model().invisibleRootItem()
            row = index[0].row()
            if direction == constants.ButtonText.UP.value:
                if row != 0:
                    item_above = parent.takeRow(row - 1)
                    parent.insertRow(row, item_above)
            elif direction == constants.ButtonText.DOWN.value:
                if row != parent.rowCount() - 1:
                    item_below = parent.takeRow(row + 1)
                    parent.insertRow(row, item_below)
        return

    # function for loading data into tab
    # clears previous data and adds newly loaded information
    # resets gui buttons
    def load_data(self, values, items):
        if values:
            for i in range(1, self.main_form_layout.count(), 2):
                item = self.main_form_layout.itemAt(i).widget()
                if type(item) == InputLine:
                    item.setText(values[item.key])
        if items:
            for row in items:
                self.tree_view.model().appendRow(row)
        return

    # packages current gui information for convertor function
    def save_data(self) -> tuple[dict, list[QStandardItem]]:
        values = {}
        for i in range(1, self.main_form_layout.count(), 2):
            values.update(self.main_form_layout.itemAt(i).widget().data())

        items = []
        for i in range(0, self.tree_view.model().rowCount()):
            items.append(self.tree_view.model().invisibleRootItem().child(i))

        return values, items
