from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QMessageBox,
    QGroupBox,
    QListWidgetItem,
)
from PyQt6.QtCore import Qt
from .styles import MAIN_WINDOW_STYLE


class LoadCharacterWindow(QWidget):
    def __init__(self, connector):
        super().__init__()
        self.connector = connector
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        load_box = QGroupBox("Wczytaj lub Usuń Postać")
        box_layout = QVBoxLayout(load_box)
        box_layout.setSpacing(15)  # Dodanie odstępu między listą a przyciskami

        self.saves_list_widget = QListWidget()
        box_layout.addWidget(self.saves_list_widget)

        button_layout = QHBoxLayout()
        self.load_button = QPushButton("Wczytaj Postać")
        self.delete_button = QPushButton("Usuń Zapis")
        self.back_button = QPushButton("Powrót")

        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.back_button)
        box_layout.addLayout(button_layout)

        main_layout.addWidget(load_box)

        self.load_button.clicked.connect(self._load_selected)
        self.delete_button.clicked.connect(self._delete_selected)
        self.back_button.clicked.connect(self._go_back)
        self.saves_list_widget.itemDoubleClicked.connect(self._load_selected)

        self.load_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.saves_list_widget.currentItemChanged.connect(self._update_button_state)

    def populate_saves(self):
        self.saves_list_widget.clear()
        save_files = self.connector.get_save_list()

        if save_files:
            for save_info in save_files:
                display_text = f"{save_info['name']}  ({save_info['date']})"
                item = QListWidgetItem(display_text)
                item.setData(Qt.ItemDataRole.UserRole, save_info["name"])
                self.saves_list_widget.addItem(item)
        else:
            self.saves_list_widget.addItem("Brak zapisanych postaci.")
            self.saves_list_widget.setEnabled(False)
        self._update_button_state(self.saves_list_widget.currentItem())

    def _update_button_state(self, current_item):
        is_valid_item = (
            current_item is not None
            and current_item.text() != "Brak zapisanych postaci."
        )
        self.load_button.setEnabled(is_valid_item)
        self.delete_button.setEnabled(is_valid_item)

    def _load_selected(self):
        selected_item = self.saves_list_widget.currentItem()
        if selected_item and selected_item.text() != "Brak zapisanych postaci.":
            save_name = selected_item.data(Qt.ItemDataRole.UserRole)
            self.connector.load_character_from_file(save_name)

    def _delete_selected(self):
        selected_item = self.saves_list_widget.currentItem()
        if not selected_item or selected_item.text() == "Brak zapisanych postaci.":
            return

        save_name = selected_item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(
            self,
            "Potwierdzenie Usunięcia",
            f"Czy na pewno chcesz usunąć zapis '{save_name}'?\nTej operacji nie można cofnąć.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            if self.connector.delete_character_save(save_name):
                self.populate_saves()

    def _go_back(self):
        if self.connector.current_character:
            self.connector.show_main_window()
        else:
            self.connector.show_generate_window()

    def showEvent(self, event):
        self.saves_list_widget.setEnabled(True)
        self.populate_saves()
        super().showEvent(event)
