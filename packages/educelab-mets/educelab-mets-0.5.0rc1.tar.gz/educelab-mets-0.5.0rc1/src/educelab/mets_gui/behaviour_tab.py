# sets up a behaviour tab for mets gui

from PySide6.QtCore import Qt, QItemSelectionModel
from PySide6.QtGui import QStandardItem, QIcon, QBrush, QStandardItemModel
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
                               QTreeView, QLabel)

from educelab.mets_gui import constants
from educelab.mets_gui.dialogs import AddBehaviourDialog
from educelab.mets_gui.utils import (LabelWithTooltip, make_item,
                                     iterate_item_model, InterruptException)


class BehaviourTab(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        label = LabelWithTooltip(constants.Labels.BEHAVIOUR_SECTION.value,
                                 constants.ElementTooltips.BEHAVIOUR_SEC.value)
        main_layout.addWidget(label)

        tree_layout = QVBoxLayout()
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(QStandardItemModel())
        self.tree_view.header().setVisible(False)
        self.tree_view.setSortingEnabled(False)

        # connecting event listeners to functions
        self.tree_view.selectionModel().currentChanged.connect(
            self.tree_item_change)
        self.tree_view.model().rowsInserted.connect(self.check_behaviour)
        self.tree_view.doubleClicked.connect(self.edit_item)

        # creation of gui buttons
        button_layout = QHBoxLayout()
        self.new_button = QPushButton(constants.ButtonText.ADD.value)
        self.new_button.setIcon(QIcon(constants.Resources.ICON_ADD.value))
        self.new_button.clicked.connect(self.add_item)
        self.new_child_button = QPushButton(
            constants.ButtonText.ADD_CHILD.value)
        self.new_child_button.setIcon(
            QIcon(constants.Resources.ICON_CHILD_ADD.value))
        self.new_child_button.clicked.connect(self.add_child)
        self.new_child_button.setEnabled(False)
        self.remove_button = QPushButton(constants.ButtonText.REMOVE.value)
        self.remove_button.setIcon(QIcon(constants.Resources.ICON_REMOVE.value))
        self.remove_button.clicked.connect(self.remove_item)
        self.remove_button.setEnabled(False)
        self.edit_button = QPushButton(constants.ButtonText.EDIT.value)
        self.edit_button.setIcon(QIcon(constants.Resources.ICON_EDIT.value))
        self.edit_button.clicked.connect(self.edit_item)
        self.edit_button.setEnabled(False)

        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.new_child_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.remove_button)
        tree_layout.addLayout(button_layout)
        tree_layout.addWidget(self.tree_view)

        main_layout.addLayout(tree_layout)

        # warning label layout
        # informs users when elements are missing required components
        self.warning_label = QLabel(constants.Labels.BEHAVIOUR_WARNING.value)
        self.warning_label.setHidden(True)
        self.warning_label.setStyleSheet('color: red')
        main_layout.addWidget(self.warning_label)

        self.setLayout(main_layout)

        return

    # creates a new window for adding an item into an item view
    def add_item(self) -> None:
        first_addition = False
        index = self.tree_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            parent = item.parent()
            if parent is None:
                dialog = AddBehaviourDialog(parent)
                parent = self.tree_view.model().invisibleRootItem()
            else:
                dialog = AddBehaviourDialog(parent)
        else:
            parent = self.tree_view.model().invisibleRootItem()
            dialog = AddBehaviourDialog(None)
            first_addition = True
        if dialog.exec():
            data = dialog.values
            new_item = make_item(data)
            parent.appendRow(new_item)
            if first_addition:
                ind = new_item.index()
                self.tree_view.selectionModel().setCurrentIndex(ind,
                                                                QItemSelectionModel.SelectionFlag.SelectCurrent)
                self.edit_button.setEnabled(True)
                self.remove_button.setEnabled(True)

            self.tree_item_change(self.tree_view.selectedIndexes()[0], None)
        return

    # removes selected item from an item view
    def remove_item(self) -> None:
        index = self.tree_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            parent = item.parent()
            if parent is None:
                parent = self.tree_view.model().invisibleRootItem()
            parent.removeRow(index[0].row())

        return

    # opens a window for editing information about a selected item
    def edit_item(self) -> None:
        index = self.tree_view.selectedIndexes()
        if index:
            item = index[0].model().itemFromIndex(index[0])
            dialog = AddBehaviourDialog(item.parent(),
                                        item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                values = dialog.values
                item = make_item(values, item)

        return

    # event listener function for enabling/disabling gui buttons based
    # on status of item view
    def tree_item_change(self, current, previous) -> None:
        if current.model():
            item = current.model().itemFromIndex(current)
            if item.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value] == constants.ElementTags.BEHAVIOUR.value:
                if item.rowCount() == 2:
                    self.new_child_button.setDisabled(True)
                else:
                    self.new_child_button.setDisabled(False)
                self.new_button.setDisabled(False)
            elif item.data(Qt.ItemDataRole.UserRole)[constants.Labels.TAG.value] \
                    in [constants.ElementTags.MECHANISM.value,
                        constants.ElementTags.INTERFACE_DEFINITION.value]:
                self.new_child_button.setDisabled(True)
                if item.parent().rowCount() == 2:
                    self.new_button.setDisabled(True)
                else:
                    self.new_button.setDisabled(False)
            else:
                self.new_button.setDisabled(False)
                self.new_child_button.setDisabled(False)
        else:
            self.new_child_button.setDisabled(True)
            self.edit_button.setDisabled(True)
            self.remove_button.setDisabled(True)
        return

    # creates a new window for adding a child item into an item view
    def add_child(self) -> None:
        index = self.tree_view.selectedIndexes()
        if index:
            parent = index[0].model().itemFromIndex(index[0])
            dialog = AddBehaviourDialog(parent)
        else:
            parent = self.tree_view.model().invisibleRootItem()
            dialog = AddBehaviourDialog(None)
        if dialog.exec():
            data = dialog.values
            new_item = make_item(data)
            parent.appendRow(new_item)

            self.tree_item_change(self.tree_view.selectedIndexes()[0], None)

        return

    # function for validating individual items in the item view
    # if any item is missing required parts, a warning will be displayed
    def check_behaviour(self) -> None:
        model = self.tree_view.model()
        valid = True

        for item in iterate_item_model(model.invisibleRootItem()):
            if item.data(Qt.ItemDataRole.UserRole)[
                constants.Labels.TAG.value] == \
                    constants.ElementTags.BEHAVIOUR.value:
                mechanism = 0
                for j in range(item.rowCount()):
                    child = item.child(j)
                    if child.data(Qt.ItemDataRole.UserRole)[
                        constants.Labels.TAG.value] == \
                            constants.ElementTags.MECHANISM.value:
                        mechanism += 1
                if mechanism == 1:
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
    def load_data(self, items: list[QStandardItem]) -> None:
        self.tree_view.clear()
        if items:
            for item in items:
                self.tree_view.addItem(item)

            self.edit_button.setEnabled(True)
            self.remove_button.setEnabled(True)
            self.new_child_button.setEnabled(True)
            self.tree_view.setCurrentRow(0)
        else:
            self.edit_button.setEnabled(False)
            self.remove_button.setEnabled(False)
            self.new_child_button.setEnabled(False)
        return

    # packages current gui information for convertor function
    def save_data(self) -> list[QStandardItem]:
        if self.check_behaviour():
            items = []
            for i in range(0, self.tree_view.model().rowCount()):
                items.append(
                    self.tree_view.model().invisibleRootItem().child(i))
        else:
            raise InterruptException(constants.Labels.BEHAVIOUR_WARNING.value)
        return items
