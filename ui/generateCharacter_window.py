from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QGroupBox,
    QScrollArea,
    QListWidget,
    QGridLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
import random

from Character import Character
from logic.character_manual_generator import (
    get_race_options,
    get_professions_for_race,
    get_names_for_race_and_gender,
    get_list_options_for_race,
    get_general_options,
    finalize_character,
    get_combined_data_for_ui,
)
from logic.character_auto_generator import (
    create_character,
    load_data,
    roll_2d10,
    find_in_range_table,
    roll_d10,
)


class GenerateCharacterWindow(QWidget):
    def __init__(self, connector):
        super().__init__()
        self.connector = connector
        self.game_data = load_data()
        self.general_options = get_general_options()

        self.skill_choice_combos = []
        self.talent_choice_combos = []
        self.equipment_choice_combos = []
        self.rolled_main_stats = {}
        self.rolled_secondary_stats = {}

        self._setup_ui()
        self.update_character_preview()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        container = QWidget()
        scroll_area.setWidget(container)
        form_layout = QFormLayout(container)

        self.race_combo = QComboBox()
        self.race_combo.addItems(["-- Wybierz Rasę --"] + get_race_options())
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Mężczyzna", "Kobieta"])
        self.profession_combo = QComboBox()
        self.name_combo = QComboBox()
        self.name_combo.setEditable(True)
        self.name_combo.lineEdit().setPlaceholderText("Wybierz lub wpisz imię")

        self.combos = {
            "age": QComboBox(),
            "height": QComboBox(),
            "weight": QComboBox(),
            "siblings": QComboBox(),
            "eye_color": QComboBox(),
            "hair_color": QComboBox(),
            "birthplace": QComboBox(),
            "star_sign": QComboBox(),
            "marks": QComboBox(),
        }
        self.combos["birthplace"].setEditable(True)
        self.combos["birthplace"].lineEdit().setPlaceholderText(
            "Wybierz lub wpisz miejsce"
        )

        self.combos["star_sign"].addItems(self.general_options.get("star_signs", []))
        self.combos["marks"].addItems(
            self.general_options.get("distinguishing_marks", [])
        )

        form_layout.addRow("Rasa:", self.race_combo)
        form_layout.addRow("Płeć:", self.gender_combo)
        form_layout.addRow("Imię:", self.name_combo)
        form_layout.addRow("Profesja:", self.profession_combo)
        form_layout.addRow("Wiek:", self.combos["age"])
        form_layout.addRow("Wzrost (cm):", self.combos["height"])
        form_layout.addRow("Waga (kg):", self.combos["weight"])
        form_layout.addRow("Kolor oczu:", self.combos["eye_color"])
        form_layout.addRow("Kolor włosów:", self.combos["hair_color"])
        form_layout.addRow("Miejsce urodzenia:", self.combos["birthplace"])
        form_layout.addRow("Znak gwiezdny:", self.combos["star_sign"])
        form_layout.addRow("Liczba rodzeństwa:", self.combos["siblings"])
        form_layout.addRow("Znak szczególny:", self.combos["marks"])

        stats_layout = QHBoxLayout()
        # ### POPRAWKA ###: Usunięto "(Finalne)" z tytułu
        main_stats_box = QGroupBox("Cechy Główne")
        ms_layout = QGridLayout(main_stats_box)
        self.main_stats_labels = {
            "WW": QLabel("0"),
            "US": QLabel("0"),
            "K": QLabel("0"),
            "Odp": QLabel("0"),
            "Zr": QLabel("0"),
            "Int": QLabel("0"),
            "SW": QLabel("0"),
            "Ogd": QLabel("0"),
        }
        positions = [
            ("WW", 0, 0),
            ("K", 0, 1),
            ("Zr", 0, 2),
            ("SW", 0, 3),
            ("US", 2, 0),
            ("Odp", 2, 1),
            ("Int", 2, 2),
            ("Ogd", 2, 3),
        ]
        for name, row, col in positions:
            name_label = QLabel(name)
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ms_layout.addWidget(name_label, row, col)
            value_label = self.main_stats_labels[name]
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ms_layout.addWidget(value_label, row + 1, col)

        sec_stats_box = QGroupBox("Cechy Drugorzędne")
        ss_layout = QGridLayout(sec_stats_box)
        self.sec_stats_labels = {
            "A": QLabel("0"),
            "Żyw": QLabel("0"),
            "S": QLabel("0"),
            "Wt": QLabel("0"),
            "Sz": QLabel("0"),
            "Mag": QLabel("0"),
            "PO": QLabel("0"),
            "PP": QLabel("0"),
        }
        positions_sec = [
            ("A", 0, 0),
            ("S", 0, 1),
            ("Sz", 0, 2),
            ("PO", 0, 3),
            ("Żyw", 2, 0),
            ("Wt", 2, 1),
            ("Mag", 2, 2),
            ("PP", 2, 3),
        ]
        for name, row, col in positions_sec:
            name_label = QLabel(name)
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ss_layout.addWidget(name_label, row, col)
            value_label = self.sec_stats_labels[name]
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ss_layout.addWidget(value_label, row + 1, col)

        stats_layout.addWidget(main_stats_box)
        stats_layout.addWidget(sec_stats_box)
        form_layout.addRow(stats_layout)

        self.skills_box = QGroupBox("Umiejętności")
        self.skills_layout = QVBoxLayout(self.skills_box)
        self.skills_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.talents_box = QGroupBox("Zdolności")
        self.talents_layout = QVBoxLayout(self.talents_box)
        self.talents_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.equipment_box = QGroupBox("Ekwipunek")
        self.equipment_layout = QVBoxLayout(self.equipment_box)
        self.equipment_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        abilities_layout = QHBoxLayout()
        abilities_layout.addWidget(self.skills_box)
        abilities_layout.addWidget(self.talents_box)
        abilities_layout.addWidget(self.equipment_box)
        form_layout.addRow(abilities_layout)

        self.manual_generate_button = QPushButton("Stwórz Postać")
        self.random_generate_button = QPushButton("Wygeneruj w Pełni Losową Postać")
        self.load_character_button = QPushButton("Wczytaj Postać")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_character_button)
        button_layout.addWidget(self.random_generate_button)
        button_layout.addWidget(self.manual_generate_button)
        main_layout.addLayout(button_layout)

        self.race_combo.currentTextChanged.connect(self.update_character_preview)
        self.gender_combo.currentTextChanged.connect(self.update_character_preview)
        self.profession_combo.currentTextChanged.connect(self.update_character_preview)
        self.manual_generate_button.clicked.connect(self.finalize_and_create_character)
        self.random_generate_button.clicked.connect(self.generate_random_character)
        self.load_character_button.clicked.connect(self.connector.show_load_window)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self._clear_layout(item.layout())

    def update_character_preview(self):
        race_name = self.race_combo.currentText()
        gender = self.gender_combo.currentText()
        is_major_update = self.sender() in [self.race_combo, self.gender_combo, None]

        if is_major_update:
            if race_name != "-- Wybierz Rasę --" and gender:
                self.name_combo.clear()
                self.name_combo.addItems(
                    get_names_for_race_and_gender(race_name, gender)
                )
                list_options = get_list_options_for_race(race_name, gender)
                for key, combo in self.combos.items():
                    if key in list_options:
                        combo.clear()
                        combo.addItems(list_options.get(key, []))

                race_data = self.game_data["races"][race_name]
                self.rolled_main_stats = {
                    stat: base + roll_2d10()
                    for stat, base in race_data["base_stats"].items()
                }
                self.rolled_secondary_stats = race_data["secondary_stats"].copy()
                self.rolled_secondary_stats["Żyw"] = find_in_range_table(
                    race_data["vitality_table"], roll_d10()
                )["value"]
                self.rolled_secondary_stats["PP"] = find_in_range_table(
                    race_data["destination_points_table"], roll_d10()
                )["value"]
                self.rolled_secondary_stats["S"] = self.rolled_main_stats["K"] // 10
                self.rolled_secondary_stats["Wt"] = self.rolled_main_stats["Odp"] // 10

            if self.sender() == self.race_combo or self.sender() is None:
                self.profession_combo.currentTextChanged.disconnect(
                    self.update_character_preview
                )
                self.profession_combo.clear()
                if race_name != "-- Wybierz Rasę --":
                    self.profession_combo.addItems(
                        ["-- Wybierz Profesję --"] + get_professions_for_race(race_name)
                    )
                self.profession_combo.currentTextChanged.connect(
                    self.update_character_preview
                )

        profession_name = self.profession_combo.currentText()
        self._clear_layout(self.skills_layout)
        self._clear_layout(self.talents_layout)
        self._clear_layout(self.equipment_layout)
        self.skill_choice_combos.clear()
        self.talent_choice_combos.clear()
        self.equipment_choice_combos.clear()

        if race_name == "-- Wybierz Rasę --" or not self.rolled_main_stats:
            for label in self.main_stats_labels.values():
                label.setText("0")
            for label in self.sec_stats_labels.values():
                label.setText("0")
            return

        display_main_stats = self.rolled_main_stats.copy()
        display_sec_stats = self.rolled_secondary_stats.copy()
        if profession_name and profession_name != "-- Wybierz Profesję --":
            prof_advances = self.game_data["base_class"][profession_name].get(
                "advances", {}
            )
            for stat, value_list in prof_advances.items():
                value = sum(value_list)
                if stat in display_main_stats:
                    display_main_stats[stat] += value
                elif stat in display_sec_stats:
                    display_sec_stats[stat] += value

        if "Po" in display_sec_stats:
            display_sec_stats["PO"] = display_sec_stats.pop("Po")

        for stat, value in display_main_stats.items():
            self.main_stats_labels[stat].setText(str(value))
        for stat, value in display_sec_stats.items():
            if stat in self.sec_stats_labels:
                self.sec_stats_labels[stat].setText(str(value))

        preview_data = get_combined_data_for_ui(
            race_name,
            profession_name if profession_name != "-- Wybierz Profesję --" else None,
        )
        for skill in preview_data.get("base_skills", []):
            self.skills_layout.addWidget(QLabel(f"• {skill}"))
        for choice in preview_data.get("skill_choices", []):
            combo = QComboBox()
            combo.addItems(choice)
            self.skills_layout.addWidget(combo)
            self.skill_choice_combos.append(combo)
        for talent in preview_data.get("base_talents", []):
            self.talents_layout.addWidget(QLabel(f"• {talent}"))
        for choice in preview_data.get("talent_choices", []):
            combo = QComboBox()
            combo.addItems(choice)
            self.talents_layout.addWidget(combo)
            self.talent_choice_combos.append(combo)
        for item in preview_data.get("base_equipment", []):
            self.equipment_layout.addWidget(QLabel(f"• {item}"))
        for choice in preview_data.get("equipment_choices", []):
            combo = QComboBox()
            combo.addItems(choice)
            self.equipment_layout.addWidget(combo)
            self.equipment_choice_combos.append(combo)

    def generate_random_character(self):
        character_data = create_character()
        if character_data:
            self.connector.set_new_character(Character(character_data))

    def finalize_and_create_character(self):
        chosen_skills = [combo.currentText() for combo in self.skill_choice_combos]
        chosen_talents = [combo.currentText() for combo in self.talent_choice_combos]
        chosen_equipment = [
            combo.currentText() for combo in self.equipment_choice_combos
        ]

        # ### POPRAWKA ###: Ujednolicenie "PO" przy tworzeniu postaci
        sec_stats_final = {k: int(v.text()) for k, v in self.sec_stats_labels.items()}
        if "PO" in sec_stats_final:
            sec_stats_final["Po"] = sec_stats_final.pop("PO")

        user_selections = {
            "rasa": self.race_combo.currentText(),
            "plec": self.gender_combo.currentText(),
            "profesja": self.profession_combo.currentText(),
            "imie": self.name_combo.currentText(),
            "wiek": int(self.combos["age"].currentText() or 0),
            "wzrost": int(self.combos["height"].currentText() or 0),
            "waga": int(self.combos["weight"].currentText() or 0),
            "rodzenstwo": int(self.combos["siblings"].currentText() or 0),
            "kolor_oczu": self.combos["eye_color"].currentText(),
            "kolor_wlosow": self.combos["hair_color"].currentText(),
            "miejsce_urodzenia": self.combos["birthplace"].currentText(),
            "znak_gwiezdny": self.combos["star_sign"].currentText(),
            "znak_szczegolny": self.combos["marks"].currentText(),
            "cechy_glowne": {
                k: int(v.text()) for k, v in self.main_stats_labels.items()
            },
            "cechy_drugorzedne": sec_stats_final,
            "chosen_skills": chosen_skills,
            "chosen_talents": chosen_talents,
            "chosen_equipment": chosen_equipment,
        }
        final_character_data = finalize_character(user_selections)
        if final_character_data:
            self.connector.set_new_character(Character(final_character_data))
