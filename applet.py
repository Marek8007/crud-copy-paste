#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

from PySide6.QtCore import QPoint, Qt, QTimer, QSize
from PySide6.QtGui import QAction, QClipboard, QCursor, QGuiApplication, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSystemTrayIcon,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QMenu,
)


APP_ICON_PATH = Path("/usr/share/icons/breeze/emotes/22/drink-beer.svg")
TEXTS_FILE = Path(__file__).resolve().with_name("applety_texts.json")

DEFAULT_TEXT_ITEMS = [
    ("Texto 1", "superadmin@elhadepilacionlaser.com"),
    ("Texto 2", "*AntDa2014##19"),
    ("Texto 3", "🎷🦐")
]


class PopupWindow(QDialog):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Applety")
        self.setWindowFlags(
            Qt.Tool
            | Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setMinimumWidth(340)
        self.setFixedSize(560, 620)

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(14, 14, 14, 14)
        card_layout.setSpacing(12)

        title = QLabel("Accesos rápidos")
        title.setObjectName("title")
        card_layout.addWidget(title)
        self.title = title

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("scrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.list_host = QWidget()
        self.list_host.setObjectName("listHost")
        self.list_host.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.list_layout = QVBoxLayout(self.list_host)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)
        self.list_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.list_host)
        card_layout.addWidget(self.scroll_area, 1)

        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 6, 0, 0)
        footer_layout.setSpacing(8)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        footer_layout.addWidget(spacer, 1)

        add_button = QPushButton("Añadir")
        add_button.clicked.connect(self.add_item)
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.hide)
        footer_layout.addWidget(add_button)
        footer_layout.addWidget(close_button)

        card_layout.addWidget(footer)
        self.footer = footer
        root.addWidget(card)

        self.refresh_items()

        self.setStyleSheet(
            """
            QDialog {
                background: #1f232a;
                color: #f5f7fa;
                border: 1px solid #3a404a;
                border-radius: 12px;
            }
            QFrame#card {
                background: transparent;
            }
            QScrollArea#scrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea#scrollArea QWidget#listHost {
                background: transparent;
            }
            QLabel#title {
                font-size: 16px;
                font-weight: 700;
                color: #ffffff;
            }
            QLabel#caption {
                font-size: 11px;
                color: #a9b4c0;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QLabel#text {
                font-size: 13px;
                color: #edf2f7;
            }
            QFrame#itemCard {
                background: #20262f;
                border: 1px solid #343c47;
                border-radius: 10px;
            }
            QLabel#itemLabel {
                font-size: 11px;
                color: #b7c0cb;
                text-transform: uppercase;
                letter-spacing: 0.4px;
            }
            QPushButton {
                background: #2f6fed;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 7px 12px;
                font-weight: 600;
                min-width: 66px;
            }
            QPushButton[iconButton="true"] {
                min-width: 40px;
                min-height: 40px;
                max-width: 40px;
                max-height: 40px;
                padding: 0px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #3f7ef0;
            }
            QPushButton:pressed {
                background: #255fd0;
            }
            QPushButton[text="Añadir"] {
                background: #2f8f4e;
            }
            QPushButton[text="Añadir"]:hover {
                background: #36a75b;
            }
            QPushButton[text="Añadir"]:pressed {
                background: #267a43;
            }
            QPushButton[text="Cerrar"] {
                background: #3d4652;
                min-width: 78px;
            }
            QPushButton[text="Cerrar"]:hover {
                background: #495463;
            }
            QPushButton#deleteButton {
                background: #8a3b3b;
                min-width: 40px;
                padding-left: 0px;
                padding-right: 0px;
            }
            QPushButton#deleteButton:hover {
                background: #a14545;
            }
            QPushButton#editButton {
                background: #b28d2f;
            }
            QPushButton#editButton:hover {
                background: #c4a13a;
            }
            QPushButton#editButton:pressed {
                background: #987724;
            }
            QPushButton#copyButton {
                background: #2f6fed;
            }
            QPushButton#copyButton:hover {
                background: #3f7ef0;
            }
            """
        )

    def copy_text(self, text: str) -> None:
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text, QClipboard.Clipboard)
        if clipboard.supportsSelection():
            clipboard.setText(text, QClipboard.Selection)

    def copy_text_with_feedback(self, button: QPushButton, text: str) -> None:
        self.copy_text(text)

        original_icon = button.icon()
        tick_icon = QIcon.fromTheme("dialog-ok-apply")
        if tick_icon.isNull():
            tick_icon = QIcon.fromTheme("emblem-ok")
        if tick_icon.isNull():
            tick_icon = self.style().standardIcon(self.style().SP_DialogApplyButton)

        button.setIcon(tick_icon)

        def restore_icon() -> None:
            if button is not None:
                button.setIcon(original_icon)

        QTimer.singleShot(1000, restore_icon)

    def clear_items(self) -> None:
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def refresh_items(self) -> None:
        self.clear_items()

        for index, (label_text, value) in enumerate(self.controller.text_items):
            row = QFrame()
            row.setObjectName("itemCard")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(12, 10, 24, 10)
            row_layout.setSpacing(10)

            text_label = QLabel(value)
            text_label.setWordWrap(True)
            text_label.setObjectName("text")
            text_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

            copy_button = QPushButton()
            copy_button.setCursor(Qt.PointingHandCursor)
            copy_icon = QIcon.fromTheme("edit-copy")
            if copy_icon.isNull():
                copy_icon = QIcon.fromTheme("edit-copy-symbolic")
            if copy_icon.isNull():
                copy_icon = self.style().standardIcon(self.style().SP_DialogOpenButton)
            copy_button.setToolTip("Copiar")
            copy_button.setIcon(copy_icon)
            copy_button.setIconSize(QSize(16, 16))
            copy_button.setFixedSize(40, 40)
            copy_button.setObjectName("copyButton")
            copy_button.setProperty("iconButton", True)
            copy_button.clicked.connect(
                lambda _checked=False, btn=copy_button, text=value: self.copy_text_with_feedback(btn, text)
            )

            edit_button = QPushButton()
            edit_icon = QIcon.fromTheme("document-edit")
            if edit_icon.isNull():
                edit_icon = QIcon.fromTheme("edit-find")
            if edit_icon.isNull():
                edit_icon = self.style().standardIcon(self.style().SP_FileDialogDetailedView)
            edit_button.setToolTip("Editar")
            edit_button.setIcon(edit_icon)
            edit_button.setIconSize(QSize(16, 16))
            edit_button.setFixedSize(40, 40)
            edit_button.setObjectName("editButton")
            edit_button.setProperty("iconButton", True)
            edit_button.clicked.connect(lambda _checked=False, idx=index: self.edit_item(idx))

            delete_button = QPushButton()
            delete_icon = QIcon.fromTheme("user-trash")
            if delete_icon.isNull():
                delete_icon = QIcon.fromTheme("edit-delete")
            if delete_icon.isNull():
                delete_icon = self.style().standardIcon(self.style().SP_TrashIcon)
            delete_button.setToolTip("Eliminar")
            delete_button.setIcon(delete_icon)
            delete_button.setIconSize(QSize(16, 16))
            delete_button.setFixedSize(40, 40)
            delete_button.setObjectName("deleteButton")
            delete_button.setProperty("iconButton", True)
            delete_button.clicked.connect(lambda _checked=False, idx=index: self.delete_item(idx))

            column = QVBoxLayout()
            column.setContentsMargins(0, 0, 0, 0)
            column.setSpacing(4)

            caption = QLabel(label_text)
            caption.setObjectName("itemLabel")
            column.addWidget(caption)
            column.addWidget(text_label)

            wrapper = QWidget()
            wrapper.setLayout(column)

            row_layout.addWidget(wrapper, 1)
            row_layout.addWidget(copy_button, 0, Qt.AlignVCenter)
            row_layout.addWidget(edit_button, 0, Qt.AlignVCenter)
            row_layout.addWidget(delete_button, 0, Qt.AlignVCenter)
            self.list_layout.addWidget(row)

        self.list_host.adjustSize()
        self.scroll_area.updateGeometry()

    def update_window_size(self) -> None:
        return

    def add_item(self) -> None:
        self.open_item_dialog(
            title_text="Añadir texto",
            header_text="Nuevo acceso rápido",
            initial_label=f"Texto {len(self.controller.text_items) + 1}",
            initial_value="",
        )

    def edit_item(self, index: int) -> None:
        if not (0 <= index < len(self.controller.text_items)):
            return

        label, value = self.controller.text_items[index]
        self.open_item_dialog(
            title_text="Editar texto",
            header_text="Editar acceso rápido",
            initial_label=label,
            initial_value=value,
            index=index,
        )

    def open_item_dialog(
        self,
        *,
        title_text: str,
        header_text: str,
        initial_label: str,
        initial_value: str,
        index: int | None = None,
    ) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle(title_text)
        dialog.setModal(True)
        dialog.setMinimumWidth(360)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel(header_text)
        title.setObjectName("title")
        layout.addWidget(title)

        label_input = QLineEdit()
        label_input.setPlaceholderText("Nombre del texto")
        label_input.setText(initial_label)
        layout.addWidget(label_input)

        value_input = QLineEdit()
        value_input.setPlaceholderText("Texto a copiar")
        value_input.setText(initial_value)
        layout.addWidget(value_input)

        buttons = QWidget()
        buttons_layout = QHBoxLayout(buttons)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(8)

        buttons_spacer = QWidget()
        buttons_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        buttons_layout.addWidget(buttons_spacer, 1)

        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("cancelButton")
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        layout.addWidget(buttons)

        dialog.setStyleSheet(
            """
            QDialog {
                background: #1f232a;
                color: #f5f7fa;
                border: 1px solid #3a404a;
                border-radius: 12px;
            }
            QLineEdit {
                background: #20262f;
                color: #edf2f7;
                border: 1px solid #343c47;
                border-radius: 8px;
                padding: 8px 10px;
            }
            QPushButton#cancelButton {
                background: #3d4652;
                min-width: 86px;
            }
            QPushButton#cancelButton:hover {
                background: #495463;
            }
            """
        )

        def accept_dialog() -> None:
            dialog.accept()

        def reject_dialog() -> None:
            dialog.reject()

        ok_button.clicked.connect(accept_dialog)
        cancel_button.clicked.connect(reject_dialog)
        value_input.returnPressed.connect(accept_dialog)
        label_input.returnPressed.connect(value_input.setFocus)

        if dialog.exec() != QDialog.Accepted:
            return

        label = label_input.text().strip() or initial_label
        value = value_input.text().strip()
        if not value:
            return

        if index is None:
            self.controller.text_items.append((label, value))
        else:
            self.controller.text_items[index] = (label, value)
        self.controller.save_text_items()
        self.refresh_items()

    def delete_item(self, index: int) -> None:
        if 0 <= index < len(self.controller.text_items):
            del self.controller.text_items[index]
            self.controller.save_text_items()
            self.refresh_items()

    def show_near_cursor(self) -> None:
        self.adjustSize()
        cursor_pos = QCursor.pos()
        x = cursor_pos.x() - self.width() // 2
        y = cursor_pos.y() - self.height() - 18

        available = QGuiApplication.primaryScreen().availableGeometry()
        x = max(available.left() + 10, min(x, available.right() - self.width() - 10))
        y = max(available.top() + 10, min(y, available.bottom() - self.height() - 10))
        self.move(QPoint(x, y))
        self.show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event) -> None:
        event.ignore()
        self.hide()


class AppController:
    def __init__(self, app: QApplication) -> None:
        self.app = app
        self.app.setQuitOnLastWindowClosed(False)
        self.text_items = self.load_text_items()

        icon = QIcon(str(APP_ICON_PATH))
        if icon.isNull():
            icon = QIcon.fromTheme("edit-paste")
        if icon.isNull():
            icon = self.app.style().standardIcon(self.app.style().SP_FileDialogDetailedView)

        self.tray = QSystemTrayIcon(icon, app)
        self.tray.setToolTip("Applety")

        self.menu = QMenu()
        self.toggle_action = QAction("Mostrar / ocultar", self.menu)
        self.quit_action = QAction("Salir", self.menu)
        self.menu.addAction(self.toggle_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)
        self.tray.setContextMenu(self.menu)

        self.window = PopupWindow(self)

        self.toggle_action.triggered.connect(self.toggle_window)
        self.quit_action.triggered.connect(self.app.quit)
        self.tray.activated.connect(self.on_tray_activated)

        self.tray.show()
        QTimer.singleShot(0, self.window.show_near_cursor)

    def load_text_items(self):
        if not TEXTS_FILE.exists():
            return list(DEFAULT_TEXT_ITEMS)

        try:
            data = json.loads(TEXTS_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return list(DEFAULT_TEXT_ITEMS)

        items = []
        if isinstance(data, list):
            for entry in data:
                if isinstance(entry, dict):
                    label = str(entry.get("label", "")).strip()
                    value = str(entry.get("value", "")).strip()
                elif isinstance(entry, (list, tuple)) and len(entry) == 2:
                    label = str(entry[0]).strip()
                    value = str(entry[1]).strip()
                else:
                    continue

                if label and value:
                    items.append((label, value))

        return items or list(DEFAULT_TEXT_ITEMS)

    def save_text_items(self) -> None:
        payload = [{"label": label, "value": value} for label, value in self.text_items]
        TEXTS_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (
            QSystemTrayIcon.Trigger,
            QSystemTrayIcon.DoubleClick,
            QSystemTrayIcon.MiddleClick,
        ):
            self.toggle_window()

    def toggle_window(self) -> None:
        if self.window.isVisible():
            self.window.hide()
        else:
            self.window.show_near_cursor()


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Applety")
    app.setWindowIcon(QIcon(str(APP_ICON_PATH)))

    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("No hay bandeja del sistema disponible en esta sesión.", file=sys.stderr)
        class _FallbackController:
            text_items = list(DEFAULT_TEXT_ITEMS)

            def save_text_items(self) -> None:
                payload = [{"label": label, "value": value} for label, value in self.text_items]
                TEXTS_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        window = PopupWindow(_FallbackController())
        window.show_near_cursor()
        return app.exec()

    _controller = AppController(app)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
