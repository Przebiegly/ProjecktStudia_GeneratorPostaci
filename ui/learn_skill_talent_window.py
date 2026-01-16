from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QListWidget,
)
from PyQt6.QtCore import Qt
from logic.character_auto_generator import load_data
from logic.character_learning import get_all_learnable_abilities, learn_ability
from .styles import MAIN_WINDOW_STYLE


class LearnSkillTalentWindow(QMainWindow):
    def __init__(self, connector):
        super().__init__()
        self.connector = connector
        self.game_data = load_data()
        self.all_abilities = get_all_learnable_abilities(self.game_data)

        self.setWindowTitle("Nauka Umiejętności i Zdolności")
        self.setMinimumSize(1000, 700)
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
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.xp_label = QLabel("Dostępne PD: 0")
        self.xp_label.setObjectName("HeaderLabel")
        self.xp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.xp_label)

        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(20)

        skills_box = QGroupBox("Dostępne Umiejętności (Koszt: 100 PD)")
        skills_layout = QVBoxLayout(skills_box)
        self.skills_list = QListWidget()
        self.buy_skill_button = QPushButton("Naucz się Umiejętności")
        self.buy_skill_button.clicked.connect(self._buy_selected_skill)
        skills_layout.addWidget(self.skills_list)
        skills_layout.addWidget(self.buy_skill_button)
        columns_layout.addWidget(skills_box)

        talents_box = QGroupBox("Dostępne Zdolności (Koszt: 100 PD)")
        talents_layout = QVBoxLayout(talents_box)
        self.talents_list = QListWidget()
        self.buy_talent_button = QPushButton("Naucz się Zdolności")
        self.buy_talent_button.clicked.connect(self._buy_selected_talent)
        talents_layout.addWidget(self.talents_list)
        talents_layout.addWidget(self.buy_talent_button)
        columns_layout.addWidget(talents_box)

        main_layout.addLayout(columns_layout)

        self.skills_list.currentItemChanged.connect(self._update_buttons_state)
        self.talents_list.currentItemChanged.connect(self._update_buttons_state)

    def populate_data(self):
        character = self.connector.current_character
        if not character:
            self.close()
            return

        self.xp_label.setText(f"Dostępne Punkty Doświadczenia: <b>{character.xp}</b>")
        self.skills_list.clear()
        learnable_skills = sorted(
            list(set(self.all_abilities["skills"]) - set(character.umiejetnosci))
        )
        self.skills_list.addItems(learnable_skills)

        self.talents_list.clear()
        learnable_talents = sorted(
            list(set(self.all_abilities["talents"]) - set(character.zdolnosci))
        )
        self.talents_list.addItems(learnable_talents)

        self._update_buttons_state()

    def _update_buttons_state(self):
        character = self.connector.current_character
        has_enough_xp = character and character.xp >= 100
        self.buy_skill_button.setEnabled(
            has_enough_xp and self.skills_list.currentItem() is not None
        )
        self.buy_talent_button.setEnabled(
            has_enough_xp and self.talents_list.currentItem() is not None
        )

    def _buy_selected_skill(self):
        selected_item = self.skills_list.currentItem()
        if not selected_item:
            return
        skill_name = selected_item.text()
        if learn_ability(self.connector.current_character, skill_name, "skill"):
            self.populate_data()
            self.connector.update_character_data()

    def _buy_selected_talent(self):
        selected_item = self.talents_list.currentItem()
        if not selected_item:
            return
        talent_name = selected_item.text()
        if learn_ability(self.connector.current_character, talent_name, "talent"):
            self.populate_data()
            self.connector.update_character_data()

    def showEvent(self, event):
        self.populate_data()
        super().showEvent(event)
