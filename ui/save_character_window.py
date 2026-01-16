from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QGroupBox,
    QFormLayout,
    QMessageBox,
    QMainWindow,
)
from PyQt6.QtCore import Qt
from .styles import MAIN_WINDOW_STYLE


class SaveCharacterWindow(QMainWindow):
    def __init__(self, connector):
        super().__init__()
        self.connector = connector

        self.setWindowTitle("Zapisz Postać")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        self._setup_ui()

    def _setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.addStretch(1)

        save_box = QGroupBox("Zapisz Aktualną Postać")
        save_box.setFixedWidth(500)
        box_layout = QVBoxLayout(save_box)

        form_layout = QFormLayout()
        self.name_label = QLabel("Nazwa zapisu:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Wpisz nazwę dla zapisu...")
        form_layout.addRow(self.name_label, self.name_input)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Zapisz")
        self.cancel_button = QPushButton("Anuluj")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        box_layout.addLayout(form_layout)
        box_layout.addSpacing(15)
        box_layout.addLayout(button_layout)

        main_layout.addWidget(save_box)
        main_layout.addStretch(1)

        self.save_button.clicked.connect(self._save_character)
        self.cancel_button.clicked.connect(self.close)
        self.name_input.returnPressed.connect(self._save_character)

    def _save_character(self):
        save_name = self.name_input.text().strip()
        if save_name:
            self.connector.save_current_character(save_name)
            QMessageBox.information(
                self, "Zapisano Pomyślnie", f"Postać '{save_name}' została zapisana."
            )
            self.close()
        else:
            self.name_input.clear()
            self.name_input.setPlaceholderText("Nazwa nie może być pusta!")
            self.name_input.setStyleSheet("border: 1px solid #D43737;")

    def showEvent(self, event):
        if self.connector.current_character:
            self.name_input.setText(self.connector.current_character.imie)
            self.name_input.selectAll()

        self.name_input.setStyleSheet("")
        self.name_input.setFocus()
        super().showEvent(event)
