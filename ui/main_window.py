import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QGroupBox,
    QApplication,
    QFileDialog,
    QScrollArea,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ImageLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(1, 1)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._pixmap = None

    def setPixmap(self, pixmap: QPixmap | None):
        self._pixmap = pixmap
        self._rescale_pixmap()

    def resizeEvent(self, event):
        self._rescale_pixmap()
        super().resizeEvent(event)

    def clear(self):
        self.setPixmap(None)

    def _rescale_pixmap(self):
        if self._pixmap:
            scaled_pixmap = self._pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.IgnoreAspectRatio,  # <--- TUTAJ JEST ZMIANA
                Qt.TransformationMode.SmoothTransformation,
            )
            super().setPixmap(scaled_pixmap)
        else:
            super().clear()


class InventoryItemWidget(QWidget):
    def __init__(self, item_data: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("InventoryItem")
        self.item_data = item_data

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        self.icon_label = ImageLabel("Dodaj ikonę")
        self.icon_label.setFixedSize(80, 80)
        self.icon_label.mousePressEvent = self.open_image_dialog
        self.icon_label.setObjectName("ItemIcon")
        self.name_label = QLabel(self.item_data.get("name", "Błąd"))
        self.name_label.setObjectName("ItemName")
        layout.addWidget(self.icon_label)
        layout.addWidget(self.name_label, 1)
        self.setLayout(layout)

    def open_image_dialog(self, event):
        filters = "Pliki obrazów (*.png *.jpg *.jpeg *.bmp)"
        filename, _ = QFileDialog.getOpenFileName(
            self, "Wybierz ikonę przedmiotu", "", filters
        )
        if filename:
            self.icon_label.setPixmap(QPixmap(filename))
            self.item_data["icon_path"] = filename


class MainWindow(QWidget):
    def __init__(self, connector: "WindowConnector"):
        super().__init__()
        self.connector = connector
        self._setup_ui()
        self.update_display(None)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        title_label = QLabel("Generator Postaci Warhammer by Lauer")
        title_label.setObjectName("TitleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        columns_layout = QHBoxLayout()
        main_layout.addLayout(columns_layout)
        col1_layout = self._create_identity_column()
        col2_layout = self._create_main_stats_skills_column()
        col3_layout = self._create_secondary_stats_talents_column()
        col4_layout = self._create_equipment_column()
        columns_layout.addLayout(col1_layout, 3)
        columns_layout.addLayout(col2_layout, 4)
        columns_layout.addLayout(col3_layout, 4)
        columns_layout.addLayout(col4_layout, 4)
        bottom_bar_layout = self._create_bottom_bar()
        main_layout.addLayout(bottom_bar_layout)
        self.setLayout(main_layout)

    def _create_identity_column(self):
        layout = QVBoxLayout()
        self.portrait_label = ImageLabel("Kliknij, aby dodać portret")
        self.portrait_label.setObjectName("Portrait")
        self.portrait_label.mousePressEvent = self.open_image_dialog
        identity_box = QGroupBox("Tożsamość i Wygląd")
        form_layout = QFormLayout()
        self.name_label = QLabel("...")
        self.race_label = QLabel("...")
        self.profession_label = QLabel("...")
        self.gender_label = QLabel("...")
        self.age_label = QLabel("...")
        self.height_label = QLabel("...")
        self.weight_label = QLabel("...")
        self.hair_label = QLabel("...")
        self.eyes_label = QLabel("...")
        self.star_sign_label = QLabel("...")
        self.siblings_label = QLabel("...")
        self.birthplace_label = QLabel("...")
        self.marks_label = QLabel("...")
        form_layout.addRow("Imię:", self.name_label)
        form_layout.addRow("Rasa:", self.race_label)
        form_layout.addRow("Profesja:", self.profession_label)
        form_layout.addRow("Płeć:", self.gender_label)
        form_layout.addRow("Wiek:", self.age_label)
        form_layout.addRow("Wzrost:", self.height_label)
        form_layout.addRow("Waga:", self.weight_label)
        form_layout.addRow("Kolor włosów:", self.hair_label)
        form_layout.addRow("Kolor oczu:", self.eyes_label)
        form_layout.addRow("Znak Gwiezdny:", self.star_sign_label)
        form_layout.addRow("Rodzeństwo:", self.siblings_label)
        form_layout.addRow("Miejsce urodzenia:", self.birthplace_label)
        form_layout.addRow("Znak szczególny:", self.marks_label)
        identity_box.setLayout(form_layout)
        resources_box = QGroupBox("Zasoby")
        res_layout = QFormLayout()
        self.gold_label = QLabel("0")
        self.xp_label = QLabel("0")
        res_layout.addRow("Złoto:", self.gold_label)
        res_layout.addRow("PD:", self.xp_label)
        resources_box.setLayout(res_layout)
        layout.addWidget(self.portrait_label, 5)
        layout.addWidget(identity_box, 4)
        layout.addWidget(resources_box, 1)
        return layout

    def _create_main_stats_skills_column(self):
        layout = QVBoxLayout()
        main_stats_box = QGroupBox("Cechy Główne")
        ms_layout = QGridLayout()
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
        main_stats_box.setLayout(ms_layout)
        skills_box = QGroupBox("Umiejętności")
        skills_layout = QVBoxLayout()
        self.skills_list = QListWidget()
        skills_layout.addWidget(self.skills_list)
        skills_box.setLayout(skills_layout)
        layout.addWidget(main_stats_box)
        layout.addWidget(skills_box)
        return layout

    def _create_secondary_stats_talents_column(self):
        layout = QVBoxLayout()
        sec_stats_box = QGroupBox("Cechy Drugorzędne")
        ss_layout = QGridLayout()
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
        sec_stats_box.setLayout(ss_layout)
        talents_box = QGroupBox("Zdolności")
        talents_layout = QVBoxLayout()
        self.talents_list = QListWidget()
        talents_layout.addWidget(self.talents_list)
        talents_box.setLayout(talents_layout)
        layout.addWidget(sec_stats_box)
        layout.addWidget(talents_box)
        return layout

    def _create_equipment_column(self):
        layout = QVBoxLayout()
        equipment_box = QGroupBox("Ekwipunek")
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("EquipmentScrollArea")
        self.equipment_content_widget = QWidget()
        self.equipment_layout = QVBoxLayout(self.equipment_content_widget)
        self.equipment_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_area.setWidget(self.equipment_content_widget)
        box_layout = QVBoxLayout()
        box_layout.addWidget(scroll_area)
        equipment_box.setLayout(box_layout)
        layout.addWidget(equipment_box)
        return layout

    def _create_bottom_bar(self):
        layout = QHBoxLayout()
        btn_add = QPushButton("Dodaj PD i Złoto")
        btn_dev = QPushButton("Rozwiń Postać")
        btn_learn = QPushButton("Nauka")
        btn_buy = QPushButton("Kup Ekwipunek")
        btn_save = QPushButton("Zapisz Postać")
        btn_load = QPushButton("Wczytaj / Nowa")
        btn_add.clicked.connect(self.connector.show_add_xp_gold_window)
        btn_buy.clicked.connect(self.connector.show_buy_items_window)
        btn_dev.clicked.connect(self.connector.show_develop_window)
        btn_learn.clicked.connect(self.connector.show_learn_skill_talent_window)
        btn_save.clicked.connect(self.connector.show_save_window)
        btn_load.clicked.connect(self.connector.show_load_window)
        buttons = [btn_add, btn_dev, btn_learn, btn_buy, btn_save, btn_load]
        for btn in buttons:
            layout.addWidget(btn)
        return layout

    def open_image_dialog(self, event):
        if not self.connector.current_character:
            return
        filters = "Pliki obrazów (*.png *.jpg *.jpeg *.bmp)"
        filename, _ = QFileDialog.getOpenFileName(self, "Wybierz portret", "", filters)
        if filename:
            self.portrait_label.setPixmap(QPixmap(filename))
            self.connector.current_character.portrait_path = filename

    def update_display(self, character: "Character"):
        while self.equipment_layout.count():
            child = self.equipment_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not character:
            self.portrait_label.clear()
            self.portrait_label.setText("Kliknij, aby dodać portret")
            labels_to_reset = [
                self.name_label,
                self.race_label,
                self.profession_label,
                self.gender_label,
                self.age_label,
                self.height_label,
                self.weight_label,
                self.hair_label,
                self.eyes_label,
                self.star_sign_label,
                self.siblings_label,
                self.birthplace_label,
                self.marks_label,
            ]
            for label in labels_to_reset:
                label.setText("...")
            self.gold_label.setText("0")
            self.xp_label.setText("0")
            for label in self.main_stats_labels.values():
                label.setText("0")
            for label in self.sec_stats_labels.values():
                label.setText("0")
            self.skills_list.clear()
            self.talents_list.clear()
            return

        self.portrait_label.clear()
        if character.portrait_path and os.path.exists(character.portrait_path):
            self.portrait_label.setPixmap(QPixmap(character.portrait_path))
        else:
            self.portrait_label.setText("Kliknij, aby dodać portret")

        self.name_label.setText(character.imie)
        self.race_label.setText(character.rasa)
        self.profession_label.setText(character.profesja)
        self.gender_label.setText(character.plec)
        self.age_label.setText(str(character.wiek))
        self.height_label.setText(f"{character.wyglad.get('wzrost', 0)} cm")
        self.weight_label.setText(f"{character.wyglad.get('waga', 0)} kg")
        self.hair_label.setText(character.wyglad.get("kolor_wlosow", "..."))
        self.eyes_label.setText(character.wyglad.get("kolor_oczu", "..."))
        self.star_sign_label.setText(
            character.szczegoly_osobiste.get("znak_gwiezdny", "...")
        )
        self.siblings_label.setText(
            str(character.szczegoly_osobiste.get("liczba_rodzenstwa", 0))
        )
        self.birthplace_label.setText(
            character.szczegoly_osobiste.get("miejsce_urodzenia", "...")
        )
        self.marks_label.setText(character.wyglad.get("znak_szczegolny", "..."))
        self.gold_label.setText(str(character.gold))
        self.xp_label.setText(str(character.xp))

        for stat, label in self.main_stats_labels.items():
            label.setText(str(character.cechy_glowne.get(stat, 0)))
        for stat, label in self.sec_stats_labels.items():
            val = character.cechy_drugorzedne.get(stat)
            if val is None:
                val = character.cechy_drugorzedne.get(stat.replace("PO", "Po"), 0)
            label.setText(str(val))

        self.skills_list.clear()
        self.skills_list.addItems(character.umiejetnosci)
        self.talents_list.clear()
        self.talents_list.addItems(character.zdolnosci)

        for item_dict in character.ekwipunek:
            item_widget = InventoryItemWidget(item_dict)
            icon_path = item_dict.get("icon_path")
            if icon_path and os.path.exists(icon_path):
                item_widget.icon_label.setPixmap(QPixmap(icon_path))
            self.equipment_layout.addWidget(item_widget)
