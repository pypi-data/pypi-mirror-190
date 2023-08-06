import logging
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QSettings, QStandardPaths
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (QMainWindow, QApplication, QMessageBox,
                               QVBoxLayout, QTabWidget, QWidget, QStyle,
                               QFileDialog)

import educelab.mets
from educelab.mets_gui import (constants, convertor)
from educelab.mets_gui.behaviour_tab import BehaviourTab
from educelab.mets_gui.file_tab import FileTab
from educelab.mets_gui.header_tab import HeaderTab
from educelab.mets_gui.links_tab import LinksTab
from educelab.mets_gui.metadata_tab import MetadataTab
from educelab.mets_gui.mets_tab import METSTab
from educelab.mets_gui.structure_tab import StructureTab
from educelab.mets_gui.utils import (InterruptException, create_message_box,
                                     create_separator)


def setup_logging(log_level=logging.INFO):
    app_dir = QStandardPaths.writableLocation(
        QStandardPaths.AppLocalDataLocation)
    log_dir = Path(app_dir) / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'METS Editor_log.txt'

    # Formats
    date_format = '%Y-%m-%d %H:%M:%S UTC'
    line_format = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'

    # Setup formatter
    logger_frmt = logging.Formatter(fmt=line_format, datefmt=date_format)
    logger_frmt.converter = time.gmtime

    # Setup handlers
    handlers = []

    stderr_hndl = logging.StreamHandler()
    stderr_hndl.setLevel(log_level)
    stderr_hndl.setFormatter(logger_frmt)
    handlers.append(stderr_hndl)

    file_hndl = RotatingFileHandler(filename=log_file,
                                    maxBytes=5000000,
                                    backupCount=10)
    file_hndl.setLevel(log_level)
    file_hndl.setFormatter(logger_frmt)
    handlers.append(file_hndl)

    # noinspection PyArgumentList
    logging.basicConfig(format=line_format, level=log_level,
                        datefmt=date_format, handlers=handlers)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(constants.Labels.APP_TITLE.value)
        self.setWindowIcon(QIcon(constants.Resources.ICON_APP.value))

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # center alignment
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

        # status bar
        status = self.statusBar()

        # top menu
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu(constants.ButtonText.OPEN.value)
        # edit_menu = main_menu.addMenu(constants.ButtonText.EDIT.value)
        help_menu = main_menu.addMenu(constants.ButtonText.HELP.value)

        open_button = QAction(constants.ButtonText.OPEN.value, self)
        open_button.setShortcut(constants.Shortcuts.OPEN.value)
        open_button.setStatusTip(constants.ButtonTooltips.OPEN.value)
        open_button.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_DialogOpenButton))
        open_button.triggered.connect(self.open_file)
        file_menu.addAction(open_button)

        save_button = QAction(constants.ButtonText.SAVE.value, self)
        save_button.setShortcut(constants.Shortcuts.SAVE.value)
        save_button.setStatusTip(constants.ButtonTooltips.SAVE.value)
        save_button.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_DialogSaveButton))
        save_button.triggered.connect(self.save_file)
        file_menu.addAction(save_button)

        file_menu.addSeparator()

        exit_button = QAction(constants.ButtonText.EXIT.value, self)
        exit_button.setShortcut(constants.Shortcuts.EXIT.value)
        exit_button.setStatusTip(constants.ButtonTooltips.EXIT.value)
        exit_button.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_DialogCloseButton))
        exit_button.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(exit_button)

        about_button = QAction(constants.ButtonText.ABOUT.value, self)
        about_button.triggered.connect(self.about)
        help_menu.addAction(about_button)

        # tab layout
        tab_widget = QTabWidget()
        self.structure_tab = StructureTab()
        self.file_tab = FileTab()
        self.header_tab = HeaderTab()
        self.metadata_tab = MetadataTab()
        self.mets_tab = METSTab()
        self.links_tab = LinksTab()
        self.behaviour_tab = BehaviourTab()

        tab_widget.addTab(self.structure_tab,
                          constants.TabNames.STRUCTURE.value)
        tab_widget.addTab(self.file_tab, constants.TabNames.FILES.value)
        tab_widget.addTab(self.header_tab, constants.TabNames.HEADER.value)
        tab_widget.addTab(self.metadata_tab, constants.TabNames.METADATA.value)
        tab_widget.addTab(self.mets_tab, constants.TabNames.METS.value)
        tab_widget.addTab(self.links_tab, constants.TabNames.LINKS.value)
        tab_widget.addTab(self.behaviour_tab,
                          constants.TabNames.BEHAVIOUR.value)
        layout.addWidget(tab_widget)

        # separator from status bar
        layout.addWidget(create_separator())

        # Restore state
        self._load_settings()
        self.show()

        return

    # closing of the main window - ask user for confirmation
    def closeEvent(self, event):
        reply = QMessageBox.question(self, constants.Labels.CONFIRMATION.value,
                                     constants.Labels.QUIT_QUESTION.value)
        if reply is QMessageBox.StandardButton.Yes:
            event.accept()
            self._save_settings()
        else:
            event.ignore()
        return

    def _save_settings(self):
        settings = QSettings()
        settings.setValue("mainWin/geometry", self.saveGeometry())
        settings.setValue("mainWin/state", self.saveState())

    def _load_settings(self):
        settings = QSettings()
        if settings.contains("mainWin/geometry"):
            self.restoreGeometry(settings.value("mainWin/geometry"))
        if settings.contains("mainWin/state"):
            self.restoreState(settings.value("mainWin/state"))

    # open mets file and load data into gui
    def open_file(self):
        logger = logging.getLogger('METS Editor')
        file_name = \
            QFileDialog.getOpenFileName(self, constants.Labels.OPEN_FILE.value,
                                        dir=QStandardPaths.writableLocation(
                                            QStandardPaths.HomeLocation),
                                        filter='XML files (*.xml)')[0]

        logger.debug(f'Selected: {file_name}')
        if file_name:
            try:
                mets = educelab.mets.METSDocument.from_file(file_name)
            except Exception as e:
                logger.error(e)
                msg = f'{constants.Labels.FILE_OPEN_ERROR.value}\n\nError: {e}'
                create_message_box(msg)
                return

            # load data from file
            logger.debug('Setting up app from loaded document')
            mets_data = convertor.mets_from_xml(mets)
            struct_maps = convertor.struct_map_from_xml(mets.struct_map)
            file_sec = convertor.file_sec_from_xml(mets.file_sec)
            header = convertor.header_from_xml(mets.header)
            metadata = convertor.metadata_from_xml(mets.amd, mets.dmd)
            links = convertor.links_from_xml(mets.struct_link)
            behaviour = convertor.behaviour_from_xml(mets.behavior)

            # pass loaded data into gui
            self.mets_tab.load_data(mets_data[0], mets_data[1], mets_data[2])
            self.structure_tab.load_data(struct_maps)
            if file_sec:
                self.file_tab.load_data(file_sec[0], file_sec[1])
            if header:
                self.header_tab.load_data(header[0], header[1], header[2],
                                          header[3])
            if metadata:
                self.metadata_tab.load_data(metadata)
            if links:
                self.links_tab.load_data(links[0], links[1])
            if behaviour:
                self.behaviour_tab.load_data(behaviour)

        return

    # save information in gui into a mets file
    def save_file(self):
        save_file = QFileDialog.getSaveFileName(self, 'Save File',
                                                filter='XML files (*.xml)')[0]
        if save_file:
            try:
                # get data from individual tabs and paste them into educelab.mets constructs
                data = self.behaviour_tab.save_data()
                behaviour_sec = convertor.behaviour_to_xml(data)

                data = self.links_tab.save_data()
                link_sec = convertor.links_to_xml(data)

                data = self.metadata_tab.save_data()
                metadata_sec = convertor.metadata_to_xml(data)

                data = self.header_tab.save_data()
                header = convertor.header_to_xml(data)

                data = self.file_tab.save_data()
                file_sec = convertor.file_sec_to_xml(data)

                data = self.structure_tab.save_data()
                structure_sec = convertor.struct_map_to_xml(data)

                mets = convertor.mets_to_xml(self.mets_tab.save_data(),
                                             structure_sec, file_sec, header,
                                             metadata_sec[0], metadata_sec[1],
                                             link_sec, behaviour_sec)
            except InterruptException as e:
                create_message_box(str(e))
                return
            try:
                mets.write_to_file(save_file)
            except Exception as e:
                create_message_box(str(e))

            create_message_box(constants.Labels.SAVE_SUCCESSFUL.value,
                               constants.MessageTypes.INFO.value)

        return

    # popup for about button
    # TODO: think on what information should be displayed here
    def about(self):
        create_message_box(constants.Labels.ABOUT_TEXT.value,
                           constants.MessageTypes.INFO.value)
        return


def main():
    app = QApplication(sys.argv)
    QCoreApplication.setOrganizationName('EduceLab')
    QCoreApplication.setApplicationName('METS Editor')
    QCoreApplication.setApplicationVersion('1.0.0')
    app.setWindowIcon(QIcon(constants.Resources.ICON_APP.value))

    setup_logging(log_level=logging.DEBUG)
    logger = logging.getLogger('METS Editor')
    logger.info(
        f'Launching {QCoreApplication.organizationName()} '
        f'{QCoreApplication.applicationName()} '
        f'v{QCoreApplication.applicationVersion()}')

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
