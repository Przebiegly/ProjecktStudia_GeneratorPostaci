from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QFrame,
    QScrollArea,
    QComboBox,
)
from PyQt6.QtCore import Qt
from logic.character_auto_generator import load_data
from logic.character_develop import (
    purchase_advance,
    are_all_advances_purchased,
    change_character_profession,
    get_profession_preview_data,
    get_profession_details,
)
from .styles import MAIN_WINDOW_STYLE


class DevelopCharacterWindow(QMainWindow):
    def __init__(self, connector):
        super().__init__()
        self.connector = connector
        self.game_data = load_data()
        self.setWindowTitle("Rozwój Postaci")
        self.setMinimumSize(1200, 800)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
        )

        self.setStyleSheet(MAIN_WINDOW_STYLE)

        self.skill_choice_combos = []
        self.talent_choice_combos = []
        self.equipment_choice_combos = []

        self._setup_ui()

    def _setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.xp_label = QLabel("Dostępne Punkty Doświadczenia: <b>0</b>")
        self.xp_label.setObjectName("HeaderLabel")
        self.xp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.xp_label)

        advances_box = QGroupBox("Dostępne Rozwinięcia (Koszt: 100 PD)")
        self.advances_layout = QGridLayout(advances_box)
        main_layout.addWidget(advances_box)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setObjectName("HorizontalDivider")
        main_layout.addWidget(divider)

        self.profession_box = self._create_profession_change_box()
        main_layout.addWidget(self.profession_box)

        main_layout.addStretch()

    def _create_profession_change_box(self):
        p_box = QGroupBox("Zmiana Profesji (Koszt: 500 PD)")
        prof_main_layout = QHBoxLayout(p_box)

        left_column = QWidget()
        choices_layout = QVBoxLayout(left_column)
        choices_layout.setContentsMargins(0, 0, 0, 0)
        self.prof_choice_list = QListWidget()
        self.prof_change_button = QPushButton("Zmień Profesję")
        choices_layout.addWidget(QLabel("Wybierz Profesję:"))
        choices_layout.addWidget(self.prof_choice_list)
        choices_layout.addWidget(self.prof_change_button)

        preview_box = QGroupBox("Podgląd Zysków")
        preview_outer_layout = QVBoxLayout(preview_box)
        self._create_preview_panel(preview_outer_layout)

        prof_main_layout.addWidget(left_column, 2)
        prof_main_layout.addWidget(preview_box, 5)

        self.prof_choice_list.currentItemChanged.connect(
            self._update_profession_preview
        )
        self.prof_change_button.clicked.connect(self.change_profession)

        return p_box

    def _create_preview_panel(self, parent_layout):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content_widget = QWidget()
        self.preview_content_layout = QVBoxLayout(scroll_content_widget)
        self.preview_content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_area.setWidget(scroll_content_widget)
        parent_layout.addWidget(scroll_area)

        stats_box = QGroupBox("Premie do Cech")
        stats_grid = QGridLayout(stats_box)
        self.preview_stats_labels = {}
        all_stats = [
            "WW",
            "US",
            "K",
            "Odp",
            "Zr",
            "Int",
            "SW",
            "Ogd",
            "A",
            "Żyw",
            "S",
            "Wt",
            "Sz",
            "Mag",
            "PO",
            "PP",
        ]
        for i, stat in enumerate(all_stats):
            row, col = divmod(i, 8)
            stat_label = QLabel(f"<b>{stat}</b>")
            stat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_label = QLabel("-")
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.preview_stats_labels[stat] = value_label
            stats_grid.addWidget(stat_label, row * 2, col)
            stats_grid.addWidget(value_label, row * 2 + 1, col)
        self.preview_content_layout.addWidget(stats_box)

        self.skills_preview_box = QGroupBox("Nowe Umiejętności")
        self.skills_preview_layout = QVBoxLayout(self.skills_preview_box)
        self.preview_content_layout.addWidget(self.skills_preview_box)

        self.talents_preview_box = QGroupBox("Nowe Zdolności")
        self.talents_preview_layout = QVBoxLayout(self.talents_preview_box)
        self.preview_content_layout.addWidget(self.talents_preview_box)

        self.equipment_preview_box = QGroupBox("Nowy Ekwipunek")
        self.equipment_preview_layout = QVBoxLayout(self.equipment_preview_box)
        self.preview_content_layout.addWidget(self.equipment_preview_box)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def populate_data(self):
        character = self.connector.current_character
        if not character:
            return

        self.xp_label.setText(f"Dostępne Punkty Doświadczenia: <b>{character.xp}</b>")

        self._clear_layout(self.advances_layout)

        row, col = 0, 0
        for stat, values in character.schemat_rozwoju.items():
            purchased_count = character.purchased_advances.get(stat, 0)
            stat_label = QLabel(f"<b>{stat}</b> ({purchased_count}/{len(values)})")
            buy_button = QPushButton(
                f"Kup (+{values[purchased_count] if purchased_count < len(values) else 0})"
            )
            buy_button.clicked.connect(lambda _, s=stat: self.buy_advance(s))

            if purchased_count >= len(values) or character.xp < 100:
                buy_button.setEnabled(False)
                if purchased_count >= len(values):
                    buy_button.setText("Wykupione")

            self.advances_layout.addWidget(stat_label, row, col * 2)
            self.advances_layout.addWidget(buy_button, row, col * 2 + 1)

            col += 1
            if col > 3:
                col = 0
                row += 1

        self.update_profession_change_section()

    def buy_advance(self, stat_key):
        if purchase_advance(self.connector.current_character, stat_key):
            self.connector.update_character_data()
            self.populate_data()

    def update_profession_change_section(self):
        character = self.connector.current_character
        all_purchased = are_all_advances_purchased(character)

        current_prof_details = get_profession_details(
            character.profesja, self.game_data
        )
        exit_professions = current_prof_details.get("profesja_wyjsciowa", [])

        if all_purchased and exit_professions:
            self.profession_box.setVisible(True)
            self.prof_choice_list.clear()
            self.prof_choice_list.addItems(exit_professions)
            if self.prof_choice_list.count() > 0:
                self.prof_choice_list.setCurrentRow(0)
        else:
            self.profession_box.setVisible(False)

    def _update_profession_preview(self, current_item, previous_item=None):
        self._clear_profession_preview()
        character = self.connector.current_character
        if not current_item or not character:
            self.prof_change_button.setEnabled(False)
            return

        preview = get_profession_preview_data(
            character, current_item.text(), self.game_data
        )

        advances = preview.get("total_advances", {})
        for stat, label in self.preview_stats_labels.items():
            value = advances.get(stat) or advances.get(stat.replace("PO", "Po"))
            label.setText(f"+{value}" if value is not None else "-")

        self._populate_preview_section(
            self.skills_preview_layout,
            self.skill_choice_combos,
            preview.get("new_base_skills", []),
            preview.get("new_skill_choices", []),
            "Brak nowych umiejętności.",
        )
        self._populate_preview_section(
            self.talents_preview_layout,
            self.talent_choice_combos,
            preview.get("new_base_talents", []),
            preview.get("new_talent_choices", []),
            "Brak nowych zdolności.",
        )
        self._populate_preview_section(
            self.equipment_preview_layout,
            self.equipment_choice_combos,
            preview.get("new_base_equipment", []),
            preview.get("new_equipment_choices", []),
            "Brak nowego ekwipunku.",
        )

        self.prof_change_button.setEnabled(character.xp >= 500)

    def _populate_preview_section(
        self, layout, combo_list, base_items, choice_groups, empty_text
    ):
        has_content = False
        if base_items:
            for item in base_items:
                layout.addWidget(QLabel(f"• {item}"))
            has_content = True

        if choice_groups:
            for group in choice_groups:
                if group:
                    combo = QComboBox()
                    combo.addItems(group)
                    layout.addWidget(combo)
                    combo_list.append(combo)
            has_content = True

        if not has_content:
            layout.addWidget(QLabel(empty_text))

    def _clear_profession_preview(self):
        self._clear_layout(self.skills_preview_layout)
        self._clear_layout(self.talents_preview_layout)
        self._clear_layout(self.equipment_preview_layout)
        self.skill_choice_combos.clear()
        self.talent_choice_combos.clear()
        self.equipment_choice_combos.clear()
        for label in self.preview_stats_labels.values():
            label.setText("-")

    def change_profession(self):
        selected_item = self.prof_choice_list.currentItem()
        if not selected_item:
            return

        choices = {
            "skills": [combo.currentText() for combo in self.skill_choice_combos],
            "talents": [combo.currentText() for combo in self.talent_choice_combos],
            "equipment": [
                combo.currentText() for combo in self.equipment_choice_combos
            ],
        }

        if change_character_profession(
            self.connector.current_character,
            selected_item.text(),
            self.game_data,
            choices,
        ):
            self.connector.update_character_data()
            self.close()

    def showEvent(self, event):
        self.populate_data()
        self.profession_box.setVisible(False)
        self.update_profession_change_section()
        super().showEvent(event)
