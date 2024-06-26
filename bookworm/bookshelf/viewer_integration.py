# coding: utf-8


from enum import IntEnum

import wx

from bookworm.commandline_handler import run_subcommand_in_a_new_process
from bookworm.concurrency import call_threaded, threaded_worker
from bookworm.document import DocumentIOError
from bookworm.gui.settings import ReconciliationStrategies, SettingsPanel
from bookworm.logger import logger
from bookworm.signals import reader_book_loaded

from .local_bookshelf.dialogs import EditDocumentClassificationDialog
from .local_bookshelf.models import Document
from .local_bookshelf.tasks import issue_add_document_request
from .window import BookshelfWindow

log = logger.getChild(__name__)


class StatefulBookshelfMenuIds(IntEnum):
    add_current_book_to_shelf = 25001


class StatelessBookshelfMenuIds(IntEnum):
    open_bookshelf = 25100


class BookshelfSettingsPanel(SettingsPanel):
    config_section = "bookshelf"

    def addControls(self):
        # Translators: the label of a group of controls in the bookshelf page in the preferences dialog
        static_box = self.make_static_box(_("Local Bookshelf"))
        wx.CheckBox(
            static_box,
            -1,
            # Translators: the label of a checkbox
            _("Automatically add opened books to the local bookshelf"),
            name="bookshelf.auto_add_opened_documents_to_bookshelf",
        )


class BookshelfMenu(wx.Menu):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.view = service.view
        self.Append(
            StatelessBookshelfMenuIds.open_bookshelf,
            # Translators: the label of an item in the application menubar
            _("&Open Bookshelf"),
            # Translators: the help text of an item in the application menubar
            _("Open your bookshelf"),
        )
        self.Append(
            StatefulBookshelfMenuIds.add_current_book_to_shelf,
            # Translators: the label of an item in the application menubar
            _("&Add to local bookshelf..."),
            # Translators: the help text of an item in the application menubar
            _("Add the current book to the local bookshelf"),
        )
        # EventHandlers
        self.view.Bind(
            wx.EVT_MENU,
            self.onOpenBookshelf,
            id=StatelessBookshelfMenuIds.open_bookshelf,
        )
        self.view.Bind(
            wx.EVT_MENU,
            self.onAddDocumentToLocalBookshelf,
            id=StatefulBookshelfMenuIds.add_current_book_to_shelf,
        )
        reader_book_loaded.connect(
            self._on_reader_loaded, sender=self.view.reader, weak=False
        )

    def onOpenBookshelf(self, event):
        run_subcommand_in_a_new_process(
            [
                "bookshelf",
            ]
        )

    def onAddDocumentToLocalBookshelf(self, event):
        try:
            self.view.reader.document.get_file_system_path()
        except DocumentIOError:
            wx.MessageBox(
                # Translators: content of a message indicating failure to add the current document to the bookshelf
                _(
                    "You can not add this document to Bookshelf.\nThe document should exist locally in your computer."
                ),
                # Translators: title of a message indicating failure to add the current document to the bookshelf
                _("Can not add document"),
                style=wx.ICON_WARNING,
            )
            return
        dialog = EditDocumentClassificationDialog(
            self.view,
            # Translators: title of a dialog to select reading list and collections for a document when adding it to the bookshelf
            _("Reading list and collections"),
        )
        with dialog:
            retval = dialog.ShowModal()
        if retval is not None:
            category_name, tags_names, should_add_to_fts = retval
            threaded_worker.submit(
                issue_add_document_request,
                document_uri=self.view.reader.document.uri,
                category_name=category_name,
                tags_names=tags_names,
                should_add_to_fts=should_add_to_fts,
            )
            wx.CallAfter(
                self.Enable, StatefulBookshelfMenuIds.add_current_book_to_shelf, False
            )

    @call_threaded
    def _on_reader_loaded(self, sender):
        wx.CallAfter(
            self.Enable,
            StatefulBookshelfMenuIds.add_current_book_to_shelf,
            not Document.select().where(Document.uri == sender.document.uri).count(),
        )
