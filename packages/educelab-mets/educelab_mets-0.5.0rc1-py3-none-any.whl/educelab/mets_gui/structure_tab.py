# sets up a structural map tab for mets gui
from PySide6.QtCore import Qt, QItemSelectionModel
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QPushButton, \
    QHBoxLayout, QFrame, QStyle, QTreeView

from educelab.mets_gui import constants, storage
from educelab.mets_gui.dialogs import AddStructMapDialog, AddStructMapItemDialog
from educelab.mets_gui.utils import (LabelWithTooltip, CustomListItem,
                                     InterruptException, make_item)


class StructureTab(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        struct_map_label = LabelWithTooltip(constants.Labels.STRUCT_MAP.value,
                                            constants.ElementTooltips.STRUCT_MAP.value,
                                            True)
        main_layout.addWidget(struct_map_label)

        self.struct_view = QListWidget(self)
        self.struct_view.setFixedHeight(84)  # get it in-line with buttons
        self.struct_view.currentItemChanged.connect(
            self.struct_view_item_change)
        self.struct_view.doubleClicked.connect(self.edit_struct_map)

        struct_map_layout = QHBoxLayout()
        struct_map_layout.addWidget(self.struct_view)

        struct_map_button_layout = QVBoxLayout()
        struct_map_new_button = QPushButton(constants.ButtonText.ADD.value)
        struct_map_new_button.setIcon(QIcon(constants.Resources.ICON_ADD.value))
        struct_map_new_button.clicked.connect(self.add_struct_map)
        self.struct_map_remove_button = QPushButton(
            constants.ButtonText.REMOVE.value)
        self.struct_map_remove_button.setIcon(
            QIcon(constants.Resources.ICON_REMOVE.value))
        self.struct_map_remove_button.clicked.connect(self.remove_struct_map)
        self.struct_map_remove_button.setEnabled(False)
        self.struct_map_edit_button = QPushButton(
            constants.ButtonText.EDIT.value)
        self.struct_map_edit_button.setIcon(
            QIcon(constants.Resources.ICON_EDIT.value))
        self.struct_map_edit_button.clicked.connect(self.edit_struct_map)
        self.struct_map_edit_button.setEnabled(False)

        struct_map_button_layout.addWidget(struct_map_new_button)
        struct_map_button_layout.addWidget(self.struct_map_edit_button)
        struct_map_button_layout.addWidget(self.struct_map_remove_button)
        # struct_map_button_layout.addStretch(1)
        struct_map_button_layout.addStrut(
            90)  # stop struct map part from being affected by resize of the main window
        struct_map_layout.addLayout(struct_map_button_layout)

        main_layout.addLayout(struct_map_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        tree_label = LabelWithTooltip(constants.Labels.STRUCT_MAP_TREE.value,
                                      constants.ElementTooltips.STRUCT_MAP_TREE.value,
                                      True)
        main_layout.addWidget(tree_label)

        # creation of gui buttons and connection of event listeners to functions
        tree_button_layout = QHBoxLayout()
        self.tree_new_button = QPushButton(constants.ButtonText.ADD.value)
        self.tree_new_button.setIcon(QIcon(constants.Resources.ICON_ADD.value))
        self.tree_new_button.clicked.connect(self.add_tree_item)
        self.tree_new_button.setEnabled(False)
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

        self.tree_view = QTreeView(self)
        self.tree_view.header().setVisible(False)
        self.tree_view.setSortingEnabled(False)
        self.tree_view.doubleClicked.connect(self.edit_tree_item)

        main_layout.addWidget(self.tree_view)
        # main_layout.addStretch(1)

        self.setLayout(main_layout)

        return

    def add_struct_map(self):
        dialog = AddStructMapDialog()
        if dialog.exec():
            values = dialog.values
            item = make_item(values)
            self.struct_view.addItem(item)
            if self.struct_view.count() == 1:
                self.struct_view.setCurrentItem(item)

        return

    def struct_view_item_change(self, current, previous):
        if current:
            self.tree_view.setModel(current.model)
            self.tree_view.selectionModel().currentChanged.connect(
                self.tree_item_change)
            self.tree_new_button.setEnabled(True)
        else:
            self.tree_view.setModel(None)
            self.tree_new_button.setEnabled(False)
            self.tree_new_child_button.setEnabled(False)
            self.tree_edit_button.setEnabled(False)
            self.tree_remove_button.setEnabled(False)
            self.tree_up_button.setEnabled(False)
            self.tree_down_button.setEnabled(False)
            self.struct_map_remove_button.setEnabled(False)
            self.struct_map_edit_button.setEnabled(False)
        if not previous:
            self.struct_map_remove_button.setEnabled(True)
            self.struct_map_edit_button.setEnabled(True)

        return

    def remove_struct_map(self):
        storage.remove_list_item_id(self.struct_view.currentItem())
        self.struct_view.takeItem(self.struct_view.currentRow())
        return

    def edit_struct_map(self):
        item = self.struct_view.currentItem()
        if item:
            dialog = AddStructMapDialog(item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                values = dialog.values
                item = make_item(values, item)

        return

    def add_tree_item(self):
        first_addition = False
        index = self.tree_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            parent = item.parent()
            if parent is None:
                dialog = AddStructMapItemDialog(parent)
                parent = self.tree_view.model().invisibleRootItem()
            else:
                dialog = AddStructMapItemDialog(parent)
        else:
            parent = self.tree_view.model().invisibleRootItem()
            dialog = AddStructMapItemDialog(None)
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
                self.tree_up_button.setEnabled(True)
                self.tree_down_button.setEnabled(True)

            self.tree_item_change(self.tree_view.selectedIndexes()[0], None)

        return

    def remove_tree_item(self):
        index = self.tree_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            parent = item.parent()
            if parent is None:
                parent = self.tree_view.model().invisibleRootItem()
            storage.remove_tree_item_id(item)
            parent.removeRow(index[0].row())

        return

    def tree_item_change(self, current, previous):
        if current.model():
            item = current.model().itemFromIndex(current)
            self.tree_edit_button.setDisabled(False)
            self.tree_remove_button.setDisabled(False)
            self.tree_up_button.setDisabled(False)
            self.tree_down_button.setDisabled(False)
            if item.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value] in \
                    [constants.ElementTags.MPTR.value,
                     constants.ElementTags.AREA.value]:
                self.tree_new_child_button.setDisabled(True)
                self.tree_new_button.setDisabled(False)
            elif item.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value] == constants.ElementTags.FPTR.value:
                if item.rowCount() > 0:
                    self.tree_new_child_button.setDisabled(True)
                    self.tree_new_button.setDisabled(False)
                else:
                    self.tree_new_child_button.setDisabled(False)
                    self.tree_new_button.setDisabled(False)
            elif item.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value] in \
                    [constants.ElementTags.PAR.value,
                     constants.ElementTags.SEQ.value]:
                if item.parent().data(Qt.ItemDataRole.UserRole)[
                    constants.Labels.TAG.value] == \
                        constants.ElementTags.FPTR.value:
                    self.tree_new_button.setDisabled(True)
                    self.tree_new_child_button.setDisabled(False)
            elif item.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value] == constants.ElementTags.DIV.value:
                if item.parent() is None:
                    self.tree_new_button.setDisabled(True)
                    self.tree_new_child_button.setDisabled(False)
                else:
                    self.tree_new_child_button.setDisabled(False)
                    self.tree_new_button.setDisabled(False)
        else:
            self.tree_new_button.setDisabled(False)
            self.tree_new_child_button.setDisabled(True)
            self.tree_edit_button.setDisabled(True)
            self.tree_remove_button.setDisabled(True)
            self.tree_up_button.setDisabled(True)
            self.tree_down_button.setDisabled(True)
        return

    def add_tree_child(self):
        index = self.tree_view.selectedIndexes()
        if index:
            parent = index[0].model().itemFromIndex(index[0])
            dialog = AddStructMapItemDialog(parent)
        else:
            parent = self.tree_view.model().invisibleRootItem()
            dialog = AddStructMapItemDialog(None)
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
            dialog = AddStructMapItemDialog(item.parent(),
                                            item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                data = dialog.values
                item = make_item(data, item)

        return

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

    def load_data(self, data):
        self.struct_view.clear()
        for item in data:
            self.struct_view.addItem(item)
        return

    def save_data(self) -> list[CustomListItem]:
        items = []
        if self.struct_view.model().rowCount() < 1:
            raise InterruptException(
                constants.ErrorMessages.STRUCT_MAP_MISSING.value)
        for i in range(0, self.struct_view.model().rowCount()):
            if self.struct_view.item(i).model.rowCount() < 1:
                raise InterruptException(
                    constants.ErrorMessages.STRUCT_MAP_ELEMENT_MISSING.value)
            items.append(self.struct_view.item(i))
        return items
