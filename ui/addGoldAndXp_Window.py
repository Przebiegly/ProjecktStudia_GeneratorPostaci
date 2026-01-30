from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGroupBox,
    QHBoxLayout,
    QGridLayout,
    QLabel,
)
from PyQt6.QtCore import Qt

from .styles import MAIN_WINDOW_STYLE


class AddGoldAndXpWindow(QMainWindow):
    def __init__(self, connector):
        super().__init__()
        self.connector = connector
        self.setWindowTitle("Zarządzaj Zasobami")

        self.setWindowModality(Qt.WindowModality.ApplicationModal)


        self.setStyleSheet(MAIN_WINDOW_STYLE)
        self._setup_ui()

    def _setup_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)

        gold_box = QGroupBox("Złoto")
        xp_box = QGroupBox("Punkty Doświadczenia")

        gold_layout = QVBoxLayout(gold_box)
        gold_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.gold_label = QLabel("0 Złota")
        self.gold_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gold_label.setObjectName("HeaderLabel")  # Użycie poprawnego stylu nagłówka

        gold_buttons_layout = QGridLayout()
        gold_values = [2, 5, 10, 50, 100, 500]
        positions = [(i, j) for i in range(3) for j in range(2)]

        for position, value in zip(positions, gold_values):
            button = QPushButton(f"+{value} Złota")
            button.clicked.connect(lambda _, v=value: self._add_resource(v, "gold"))
            gold_buttons_layout.addWidget(button, *position)

        gold_layout.addWidget(self.gold_label)
        gold_layout.addLayout(gold_buttons_layout)

        xp_layout = QVBoxLayout(xp_box)
        xp_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.xp_label = QLabel("0 PD")
        self.xp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.xp_label.setObjectName("HeaderLabel")

        xp_buttons_layout = QGridLayout()
        xp_values = [2, 5, 10, 25, 50, 100]
        for position, value in zip(positions, xp_values):
            button = QPushButton(f"+{value} PD")
            button.clicked.connect(lambda _, v=value: self._add_resource(v, "xp"))
            xp_buttons_layout.addWidget(button, *position)

        xp_layout.addWidget(self.xp_label)
        xp_layout.addLayout(xp_buttons_layout)

        main_layout.addWidget(gold_box)
        main_layout.addWidget(xp_box)

        self.setCentralWidget(main_widget)
        self.setFixedSize(self.sizeHint())

    #metoda odpowiada po tym jak klikniesz przycisk (obojetnie jaki) sprawdza obiekt postaci i jaki zasob ma dodac xp czy golda, dodaje i odswieza okna
    def _add_resource(self, value: int, resource_type: str):
        character = self.connector.current_character
        if not character:
            return

        if resource_type == "gold":
            character.gold += value
        elif resource_type == "xp":
            character.xp += value

        self._update_display()
        self.connector.update_character_data()


    def _update_display(self):
        character = self.connector.current_character
        if character:
            self.gold_label.setText(f"<b>{character.gold}</b> Złoto")
            self.xp_label.setText(f"<b>{character.xp}</b> PD")
        else:
            self.gold_label.setText("Brak Postaci")
            self.xp_label.setText("Brak Postaci")

    def showEvent(self, event):
        self._update_display()
        super().showEvent(event)
