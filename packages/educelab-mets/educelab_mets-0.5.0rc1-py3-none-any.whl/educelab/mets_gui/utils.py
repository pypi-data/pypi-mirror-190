from typing import Dict, Union

from PySide6.QtCore import Qt, QDateTime, QDate
from PySide6.QtGui import QPixmap, QStandardItemModel, QIcon, QStandardItem
from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget, QLineEdit, \
    QListWidgetItem, \
    QPushButton, QComboBox, QDateTimeEdit, QCheckBox, QTextEdit, QListWidget, \
    QVBoxLayout, QMessageBox, \
    QDialogButtonBox, QFormLayout, QDialog, QFrame

from educelab.mets_gui import constants, storage


# custom class to create a label with an icon that displayes a tooltip on cursor hover
class LabelWithTooltip(QWidget):
    def __init__(self, label: str, tooltip: str, required: bool = False,
                 stretch: bool = True):
        """
        :param label: text for the label
        :param tooltip: text for the tooltip
        :param required: whether the element/attribute the label represents is required by
                         the mets schema - creates a red asterisk if it is so
        :param stretch: whether add a stretch widget at the end - used for labels that
                        do not have another widgets next to them
        """
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0,
                                  0)  # remove basic margins from layout
        qlabel = QLabel(label)  # create requested label
        layout.addWidget(qlabel)
        if required:  # add extra red asterisk after the text if it is required
            req_label = QLabel('*')
            req_label.setStyleSheet('color: red')
            layout.addWidget(req_label)
        if tooltip:  # if tooltip text was provided, add a tooltip icon and attach tooltip
            qlabel_tooltip = QLabel()
            qlabel_tooltip.setPixmap(
                QPixmap(constants.Resources.ICON_INFO.value).scaledToWidth(20))
            qlabel_tooltip.setToolTip(tooltip)
            layout.addWidget(qlabel_tooltip)
        if stretch:
            layout.addStretch()
        self.setLayout(layout)


# custom class for use when short text user input is required
class InputLine(QLineEdit):
    def __init__(self, key, required=False):
        """
        :param key: identifier for the data that will be inserted by the user
        :param required: whether the element/attribute the label represents is required by
                         the mets schema - used for checking whether the input can be emtpy
        """
        super().__init__()
        self.key = key
        self.required = required

    # function for getting the user input
    # returns a text mapped to the supplied key value
    def data(self) -> Dict[str, str]:
        return {self.key: self.text()}


# custom class for use when multiline text user input is required
class InputText(QTextEdit):
    def __init__(self, key, required=False):
        """
        :param key: identifier for the data that will be inserted by the user
        :param required: whether the element/attribute the label represents is required by
                         the mets schema - used for checking whether the input can be emtpy
        """
        super().__init__()
        self.key = key
        self.required = required
        self.setAcceptRichText(False)

    # function for getting the user input
    # returns a text mapped to the supplied key value
    def data(self) -> Dict[str, str]:
        return {self.key: self.toPlainText()}


# custom class for use when multiple options are provided for user
class InputChoice(QComboBox):
    def __init__(self, key, choices, required=False):
        """
        :param key: identifier for the data that will be inserted by the user
        :param required: whether the element/attribute the label represents is required by
                         the mets schema - creates an empty option
        """
        super().__init__()
        self.key = key
        self.required = required

        if not required:
            self.addItem('')
        for choice in choices:
            self.addItem(choice.value)

    # function for getting the user input
    # returns a text mapped to the supplied key value
    def data(self) -> Dict[str, str]:
        return {self.key: self.currentText()}


# custom class for use when datetime user input is required
class InputDateTime(QWidget):
    def __init__(self, key, required=False):
        """
        :param key: identifier for the data that will be inserted by the user
        :param required: whether the element/attribute the label represents is required by
                         the mets schema - creates a check box to turn widget on/off
        """
        super().__init__()
        self.key = key
        self.required = required

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.input_datetime = QDateTimeEdit()
        self.input_datetime.setDateTime(
            QDateTime.currentDateTime())  # insert current datetime
        layout.addWidget(self.input_datetime, stretch=2)
        if not required:  # create a checkbox to turn the field on if not required
            self.toggle = QCheckBox(constants.Labels.LEAVE_EMPTY.value)
            self.toggle.stateChanged.connect(self.toggled)
            layout.addWidget(self.toggle, stretch=1)
        self.setLayout(layout)
        self.toggle.toggle()

    # function for getting the user input
    # returns a datetime string mapped to the supplied key value if turned on
    def data(self):
        if self.toggle.isChecked():
            return {self.key: ''}

        return {self.key: self.input_datetime.dateTime().toString(
            Qt.DateFormat.ISODate)}

    # event handler for checkbox to turn date input on/off
    def toggled(self, state):
        if state == Qt.CheckState.Checked.value:
            self.input_datetime.setEnabled(False)
        else:
            self.input_datetime.setEnabled(True)
        return

    # function for uploading data from mets document to the widget
    def load_data(self, value: str):
        if not value:
            self.toggle.setChecked(True)
        else:
            self.toggle.setChecked(False)
            self.input_datetime.setDate(
                QDate.fromString(value, Qt.DateFormat.ISODate))
        return


# custom class that creates an empty qlist that can be filled items
class InputList(QWidget):
    def __init__(self, key, dialog, required=False):
        """
        :param key: identifier for the data that will be inserted by the user
        :param dialog: input dialog that is used for adding new items into the list
        :param required: whether the element/attribute the label represents is required by
                         the mets schema - used for checking whether the list can be empty
        """
        super().__init__()
        self.key = key
        self.required = required
        self.dialog = dialog

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        list_button_layout = QHBoxLayout()

        # create simple add/remove/edit button layout for the list
        list_new_button = QPushButton()
        list_new_button.setIcon(QIcon(constants.Resources.ICON_ADD.value))
        list_new_button.clicked.connect(self.list_add)
        self.list_remove_button = QPushButton()
        self.list_remove_button.setIcon(
            QIcon(constants.Resources.ICON_REMOVE.value))
        self.list_remove_button.clicked.connect(self.list_remove)
        self.list_remove_button.setEnabled(False)
        self.list_edit_button = QPushButton()
        self.list_edit_button.setIcon(
            QIcon(constants.Resources.ICON_EDIT.value))
        self.list_edit_button.clicked.connect(self.list_edit)
        self.list_edit_button.setEnabled(False)

        list_button_layout.addWidget(list_new_button)
        list_button_layout.addWidget(self.list_edit_button)
        list_button_layout.addWidget(self.list_remove_button)

        self.list = QListWidget()
        self.list.doubleClicked.connect(self.list_edit)
        layout.addLayout(list_button_layout)
        layout.addWidget(self.list)

        self.setLayout(layout)

        return

    # function started by add button - creates dialog for adding an item
    # into the list
    def list_add(self):
        d = self.dialog()
        if d.exec():
            values = d.values
            item = QListWidgetItem(constants.Labels.GENERIC_TAG.value % (
                values[constants.Labels.TAG.value],
                values[constants.Labels.VALUE.value]))
            item.setData(Qt.ItemDataRole.UserRole, values)
            self.list.addItem(item)
            if self.list.count() == 1:  # enable rest of the buttons when items are on the list
                self.list_remove_button.setEnabled(True)
                self.list_edit_button.setEnabled(True)
                self.list.setCurrentItem(item)
                # workaround for buggy button disable system
                temp = QListWidgetItem()
                self.list.addItem(temp)
                self.list.setCurrentItem(temp)
                self.list.takeItem(self.list.currentRow())

        return

    # removes items from list - started by REMOVE button
    def list_remove(self):
        self.list.takeItem(self.list.currentRow())
        item = self.list.currentItem()
        if not item:  # disable all buttons but ADD while there is nothing on the list
            self.list_remove_button.setEnabled(False)
            self.list_edit_button.setEnabled(False)
        return

    # opens dialog for editing selected item from the list - started by EDIT button
    def list_edit(self):
        item = self.list.currentItem()
        if item:
            dialog = self.dialog(item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                values = dialog.values
                item.setData(Qt.ItemDataRole.UserRole, values)
                item.setText(constants.Labels.GENERIC_TAG.value % (
                    values[constants.Labels.TAG.value],
                    values[constants.Labels.VALUE.value]))
        return

    # packages data from the list to be sent into converter
    def data(self) -> dict[str, list]:
        data = []
        for i in range(self.list.model().rowCount()):
            item = self.list.item(i)
            data.append(item.data(Qt.ItemDataRole.UserRole))

        return {self.key: data}

    # load data received from mets converter function into the list
    def load_data(self, data):
        if data:
            for values in data:
                item = QListWidgetItem(constants.Labels.GENERIC_TAG.value % (
                    values[constants.Labels.TAG.value],
                    values[constants.Labels.VALUE.value]))
                self.list.addItem(item)
            self.list.setCurrentRow(0)
            self.list_edit_button.setEnabled(True)
            self.list_remove_button.setEnabled(True)
        return


# edit of the regular list item to allow it to have child elements
# used for top level mets elements like structurula maps
class CustomListItem(QListWidgetItem):
    def __init__(self, name):
        super().__init__(name)
        self.model = QStandardItemModel()

    # def setData(self, value: typing.Any, role: int) -> None:
    #    super().setData(role, value)
    #    return


ListTreeItem = Union[QStandardItem, QListWidgetItem, CustomListItem]


# base class for all dialogs in the app
class CustomDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.values = {}  # stores all inputted information
        self.element_type = None  # for element
        self.old_id = None  # for cases when dialog is used for editing and ID value is changed

        self.setWindowIcon(QIcon(constants.Resources.ICON_APP.value))

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()

        upper_widget = QWidget()
        self.upper_layout = QVBoxLayout()
        self.upper_layout.setContentsMargins(0, 0, 0, 0)
        upper_widget.setLayout(self.upper_layout)
        self.fill_upper_layout()
        layout.addWidget(upper_widget)

        form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        form_widget.setLayout(self.form_layout)
        self.fill_form_layout()
        layout.addWidget(form_widget)

        layout.addWidget(button_box)
        layout.addStretch(1)
        self.setLayout(layout)

        if data:
            self.old_id = data.get(constants.Attributes.ID.value)
            self.load_data(data)

        return

    # upper layout is used for combo boxes that change the rest of the layout
    # used by individual dialog implementations to define the type of the combo box
    def fill_upper_layout(self):
        return

    # form layout is used as a space for the main part of the dialog form
    # used by individual dialog implementations to fill in all required input widgets
    def fill_form_layout(self):
        return

    # called when OK dialog button is used
    # checks for required values and collects all information provided by the user
    # stores and checks used ID attributes to maintain unique IDs across document
    def accept(self):
        if not self.required_check():
            create_message_box(constants.Labels.EMPTY_REQUIRED_FIELD.value)
            return

        self.values = {}  # reset value storage
        self.fill_tag_data()  # gather info on element type

        for i in range(1, self.form_layout.count(), 2):  # gather all user input
            self.values.update(self.form_layout.itemAt(i).widget().data())

        new_id = self.values.get(constants.Attributes.ID.value)
        if self.old_id:  # in case of editing existing element
            if new_id == self.old_id:
                super().accept()
                return
            elif not storage.change_id(self.old_id,
                                       new_id):  # if ID has changed, check availability
                create_message_box(constants.Labels.DUPLICATE_ID_WARNING.value)
                return
        elif new_id:  # if new ID entry is made, check its availabilitys
            if not storage.add_id(new_id,
                                  self.values[constants.Labels.TAG.value]):
                create_message_box(constants.Labels.DUPLICATE_ID_WARNING.value)
                return
        super().accept()

    # called during dialog accept function
    # used for storing TAG information into dialog values
    def fill_tag_data(self):
        return

    # fills all input fields in the dialog with provided data
    def load_data(self, data):
        if self.element_type is not None:
            self.element_type.setDisabled(True)
        for i in range(1, self.form_layout.count(), 2):
            item = self.form_layout.itemAt(i).widget()
            if type(item) in [InputLine, InputText]:
                item.setText(data[item.key])
            elif type(item) == InputChoice:
                item_index = item.findText(data[item.key])
                item.setCurrentIndex(item_index)
            elif type(item) == InputDateTime:
                item.load_data(data[item.key])
            elif type(item) == InputList:
                item.load_data(data[item.key])
            elif type(item) == OtherAttributeList:
                item.load_data(data[item.key])
        return

    # checks all input fields - if any field is required and empty,
    # returns false
    def required_check(self) -> bool:
        for i in range(1, self.form_layout.count(), 2):
            item = self.form_layout.itemAt(i).widget()
            if item.required and not list(item.data().values())[0]:
                return False
        return True


# a lot of elements have option to add other attributes
# this widget provides a structure for
class OtherAttributeList(QWidget):
    def __init__(self, verbose: bool = True):

        """
        :param verbose: whether the text part of the widget should be shown or not
        """
        super().__init__()
        self.required = False
        self.key = constants.Labels.OTHER_ATTRIBS.value
        other_attribs_layout = QVBoxLayout()
        other_attribs_layout.setContentsMargins(0, 0, 0, 0)
        label = LabelWithTooltip(constants.Labels.OTHER_ATTRIBS.value,
                                 constants.AttributeTooltips.OTHER_ATTRIBS.value,
                                 stretch=True)
        if verbose:
            other_attribs_layout.addWidget(label)

        other_attribs_button_layout = QHBoxLayout()

        other_attribs_new_button = QPushButton()
        if verbose:
            other_attribs_new_button.setText(constants.ButtonText.ADD.value)
        other_attribs_new_button.setIcon(
            QIcon(constants.Resources.ICON_ADD.value))
        other_attribs_new_button.clicked.connect(self.add_other_attrib)
        other_attribs_remove_button = QPushButton()
        if verbose:
            other_attribs_remove_button.setText(
                constants.ButtonText.REMOVE.value)
        other_attribs_remove_button.setIcon(
            QIcon(constants.Resources.ICON_REMOVE.value))
        other_attribs_remove_button.clicked.connect(self.remove_other_attrib)
        other_attribs_remove_button.setEnabled(False)
        self.other_attribs_remove_button = other_attribs_remove_button
        other_attribs_edit_button = QPushButton()
        if verbose:
            other_attribs_edit_button.setText(constants.ButtonText.EDIT.value)
        other_attribs_edit_button.setIcon(
            QIcon(constants.Resources.ICON_EDIT.value))
        other_attribs_edit_button.clicked.connect(self.edit_other_attrib)
        other_attribs_edit_button.setEnabled(False)
        self.other_attribs_edit_button = other_attribs_edit_button

        other_attribs_button_layout.addWidget(other_attribs_new_button)
        other_attribs_button_layout.addWidget(other_attribs_edit_button)
        other_attribs_button_layout.addWidget(other_attribs_remove_button)

        self.other_attribs_list = QListWidget()
        self.other_attribs_list.currentItemChanged.connect(
            self.other_attribs_item_change)
        self.other_attribs_list.doubleClicked.connect(self.edit_other_attrib)
        other_attribs_layout.addLayout(other_attribs_button_layout)
        other_attribs_layout.addWidget(self.other_attribs_list)

        self.setLayout(other_attribs_layout)

    def add_other_attrib(self):
        dialog = AddOtherAttribDialog()
        if dialog.exec():
            values = dialog.values
            item = make_item(values)
            self.other_attribs_list.addItem(item)
            if self.other_attribs_list.count() == 1:
                self.other_attribs_list.setCurrentItem(item)
                # workaround for buggy button disable system
                temp = QListWidgetItem()
                self.other_attribs_list.addItem(temp)
                self.other_attribs_list.setCurrentItem(temp)
                self.other_attribs_list.takeItem(
                    self.other_attribs_list.currentRow())

        return

    def other_attribs_item_change(self, current, previous):
        if not current:
            self.other_attribs_edit_button.setEnabled(False)
            self.other_attribs_remove_button.setEnabled(False)
        if not previous:
            self.other_attribs_edit_button.setEnabled(True)
            self.other_attribs_remove_button.setEnabled(True)
        return

    def remove_other_attrib(self):
        self.other_attribs_list.takeItem(self.other_attribs_list.currentRow())
        return

    def edit_other_attrib(self):
        item = self.other_attribs_list.currentItem()
        if item:
            dialog = AddOtherAttribDialog(item.data(Qt.ItemDataRole.UserRole))
            if dialog.exec():
                values = dialog.values
                make_item(values, item)
        return

    def load_data(self, other_attribs: list[dict[str, str]]) -> None:
        self.other_attribs_list.clear()
        if other_attribs:
            for attrib in other_attribs:
                item = make_item(attrib)
                self.other_attribs_list.addItem(item)

            self.other_attribs_edit_button.setEnabled(True)
            self.other_attribs_remove_button.setEnabled(True)
            self.other_attribs_list.setCurrentRow(0)

        else:
            self.other_attribs_edit_button.setEnabled(False)
            self.other_attribs_remove_button.setEnabled(False)
        return

    def data(self) -> dict[str: list]:
        result = []
        for i in range(self.other_attribs_list.count()):
            data = self.other_attribs_list.item(i).data(
                Qt.ItemDataRole.UserRole)
            result.append(data)
        return {self.key: result}

    def model(self):
        return self.other_attribs_list.model()


class AddOtherAttribDialog(CustomDialog):
    def fill_form_layout(self):
        self.setWindowTitle(constants.Labels.DIALOG_ADD_OTHER_ATTRIB.value)
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
        self.setWindowTitle(constants.Labels.DIALOG_EDIT_OTHER_ATTRIB.value)
        super().load_data(data)

        return

    def fill_tag_data(self):
        self.values[
            constants.Labels.TAG.value] = constants.Labels.NAMESPACES.value
        self.values[constants.Attributes.ID.value] = ''
        return


# custom exception for interruption of processes within gui app
class InterruptException(Exception):
    def __init__(self, message, *args):
        self.message = message
        super().__init__(args)

    def __str__(self):
        return str(self.message)


def create_form_row_items(item_type, label, tooltip, required=False, data=None,
                          dialog=None):
    """
    creates a label with tooltip and corresponding input field that can be inserted into a form layout
    :param item_type: required type of the input
    :param label: text for the label
    :param tooltip: text for the tooltip
    :param data: set of values for combo box input option
    :param dialog: dialog class for item list input option
    """
    label_item = LabelWithTooltip(label, tooltip, required, False)
    input_item = None
    if item_type == constants.InputTypes.LINE_EDIT.value:
        input_item = InputLine(label, required=required)
    elif item_type == constants.InputTypes.COMBO_BOX.value:
        # TODO raise error for empty data
        input_item = InputChoice(label, data, required=required)
    elif item_type == constants.InputTypes.DATE_TIME.value:
        input_item = InputDateTime(label, required=required)
    elif item_type == constants.InputTypes.TEXT_EDIT.value:
        input_item = InputText(label, required=required)
    elif item_type == constants.InputTypes.LIST.value:
        # TODO raise error for empty dialog
        input_item = InputList(label, dialog, required=required)

    return label_item, input_item


# enables OTHER line input field in dialogs where combo box has option for OTHER
def combo_box_other_type_enable(choice: QComboBox, input_line: QLineEdit):
    if choice.currentText().lower() == 'other':
        input_line.setEnabled(True)
    else:
        input_line.setText('')
        input_line.setEnabled(False)
    return


# shows a warning text within gui
# used when required parts of mets elements are missing
def xml_warning_text_change(combo_box: QComboBox, label: QLabel) -> None:
    if combo_box.currentText() == constants.DataContentTypes.XML.value:
        label.setText(constants.Labels.XML_NAMESPACE_WARNING.value)
    else:
        label.setText('')
    return


# creates item entries for list/tree views
# used to define a way different elements are displayed within gui
# default approach is to use ID if the element
# some elements provide better way of sorting e.g. agent name
# can be modified for custom behaviour for every mets element
def make_item(data: dict[str, str], item: ListTreeItem = None) -> ListTreeItem:
    if data[constants.Labels.TAG.value] in [
        constants.ElementTags.STRUCT_MAP.value,
        constants.ElementTags.DMD_SEC.value,
        constants.ElementTags.AMD_SEC.value
    ]:
        if item:
            new_item = item
            new_item.setText(constants.Labels.GENERIC_TAG.value % (
                data[constants.Labels.TAG.value],
                data[constants.Attributes.ID.value]))
        else:
            new_item = CustomListItem(constants.Labels.GENERIC_TAG.value % (
                data[constants.Labels.TAG.value],
                data[constants.Attributes.ID.value]))
        new_item.setData(Qt.ItemDataRole.UserRole, data)
        storage.add_id(data[constants.Attributes.ID.value],
                       data[constants.Labels.TAG.value])

    elif data[constants.Labels.TAG.value] == constants.ElementTags.AGENT.value:
        if item:
            new_item = item
            new_item.setText(constants.Labels.GENERIC_TAG.value % (
                data[constants.Labels.TAG.value],
                data[constants.Attributes.NAME.value]))
        else:
            new_item = QListWidgetItem(constants.Labels.GENERIC_TAG.value % (
                data[constants.Labels.TAG.value],
                data[constants.Attributes.NAME.value]))
        new_item.setData(Qt.ItemDataRole.UserRole, data)
        storage.add_id(data[constants.Attributes.ID.value],
                       data[constants.Labels.TAG.value])

    elif data[
        constants.Labels.TAG.value] == constants.ElementTags.ALT_RECORD_ID.value:
        if item:
            new_item = item
            new_item.setText(constants.Labels.GENERIC_TAG.value % (
                data[constants.Labels.TAG.value],
                data[constants.Labels.VALUE.value]))
        else:
            new_item = QListWidgetItem(constants.Labels.GENERIC_TAG.value % (
                data[constants.Labels.TAG.value],
                data[constants.Labels.VALUE.value]))
        new_item.setData(data, Qt.ItemDataRole.UserRole)
        storage.add_id(data[constants.Attributes.ID.value],
                       data[constants.Labels.TAG.value])

    elif data[constants.Labels.TAG.value] in [constants.Labels.NAMESPACES.value,
                                              constants.Labels.OTHER_ATTRIBS.value]:
        if item:
            new_item = item
            new_item.setText(': '.join([data[constants.Attributes.NAME.value],
                                        data[constants.Labels.VALUE.value]]))
        else:
            new_item = QListWidgetItem(
                ': '.join([data[constants.Attributes.NAME.value],
                           data[constants.Labels.VALUE.value]]))
        new_item.setData(Qt.ItemDataRole.UserRole, data)

    elif data[constants.Labels.TAG.value] == constants.ElementTags.DIV.value:
        if item:
            new_item = item
            new_item.setText(constants.Labels.GENERIC_TAG.value % (
                data[constants.Labels.TAG.value],
                data[constants.Attributes.LABEL.value]))
        else:
            new_item = QStandardItem(constants.Labels.GENERIC_TAG.value % (
                data[constants.Labels.TAG.value],
                data[constants.Attributes.LABEL.value]))
            new_item.setEditable(False)
        new_item.setData(data, Qt.ItemDataRole.UserRole)

    else:
        if item:
            new_item = item
            new_item.setText(constants.Labels.GENERIC_TAG.value % (
                data[constants.Labels.TAG.value],
                data[constants.Attributes.ID.value]))
        else:
            new_item = QStandardItem(constants.Labels.GENERIC_TAG.value % (
                data[constants.Labels.TAG.value],
                data[constants.Attributes.ID.value]))
            new_item.setEditable(False)
        new_item.setData(data, Qt.ItemDataRole.UserRole)
        storage.add_id(data[constants.Attributes.ID.value],
                       data[constants.Labels.TAG.value])

    return new_item


# creates a different types of graphical separators to be used as gui elements
def create_separator(
        separator_type: str = constants.SeparatorTypes.HORIZONTAL.value) -> QFrame:
    separator = QFrame()
    if separator_type == constants.SeparatorTypes.HORIZONTAL.value:
        separator.setFrameShape(QFrame.Shape.HLine)
    else:
        separator.setFrameShape(QFrame.Shape.VLine)
    separator.setFrameShadow(QFrame.Shadow.Sunken)
    return separator


# creates a specified message box and opens it in the gui
def create_message_box(message: str,
                       message_type: str = constants.MessageTypes.ERROR.value) -> None:
    dlg = QMessageBox()
    dlg.setWindowIcon(QIcon(constants.Resources.ICON_APP.value))
    if message_type == constants.MessageTypes.ERROR.value:
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.setWindowTitle(constants.Labels.ERROR.value)
    elif message_type == constants.MessageTypes.INFO.value:
        dlg.setIcon(QMessageBox.Icon.Information)
        dlg.setWindowTitle(constants.Labels.INFO.value)
    else:
        dlg.setIcon(QMessageBox.Icon.NoIcon)
        dlg.setWindowTitle('')
    dlg.setText(message)
    dlg.exec()
    return


# helper function for iteration through items in a tree view
# used for deleting parts of tree view quickly
def iterate_item_model(root):
    def recurse(parent):
        for row in range(parent.rowCount()):
            for column in range(parent.columnCount()):
                child = parent.child(row, column)
                yield child
                if child.hasChildren():
                    yield from recurse(child)

    if root is not None:
        yield from recurse(root)
