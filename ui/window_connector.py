import os
from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from ui.main_window import MainWindow
from ui.generateCharacter_window import GenerateCharacterWindow
from ui.addGoldAndXp_Window import AddGoldAndXpWindow
from ui.buyItems_window import BuyItemsWindow
from ui.developCharacter_window import DevelopCharacterWindow
from ui.learn_skill_talent_window import LearnSkillTalentWindow
from ui.save_character_window import SaveCharacterWindow
from ui.load_character_window import LoadCharacterWindow

from logic.character_auto_generator import create_character
from logic import save_load_logic
from Character import Character
from .styles import MAIN_WINDOW_STYLE


class WindowConnector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_character = None

        self.setWindowTitle("Generator Postaci Warhammer by Lauer")
        self.setGeometry(100, 100, 1600, 900)
        self.setStyleSheet(MAIN_WINDOW_STYLE)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_view = MainWindow(self)
        self.gen_view = GenerateCharacterWindow(self)
        self.load_view = LoadCharacterWindow(self)

        self.add_xp_gold_window = AddGoldAndXpWindow(self)
        self.buy_items_window = BuyItemsWindow(self)
        self.dev_char_window = DevelopCharacterWindow(self)
        self.learn_skill_talent_window = LearnSkillTalentWindow(self)
        self.save_view = SaveCharacterWindow(self)

        self.stacked_widget.addWidget(self.gen_view)
        self.stacked_widget.addWidget(self.main_view)
        self.stacked_widget.addWidget(self.load_view)

        self.stacked_widget.setCurrentWidget(self.gen_view)
        self.showMaximized()

    def generate_and_set_random_character(self):
        character_data = create_character()
        if character_data:
            self.set_new_character(Character(character_data))

    def set_new_character(self, character_object):
        self.current_character = character_object
        self.main_view.update_display(self.current_character)
        self.stacked_widget.setCurrentWidget(self.main_view)

    def update_character_data(self):
        if self.current_character:
            self.main_view.update_display(self.current_character)

    def show_generate_window(self):
        self.stacked_widget.setCurrentWidget(self.gen_view)

    def show_main_window(self):
        self.stacked_widget.setCurrentWidget(self.main_view)

    def show_add_xp_gold_window(self):
        if self.current_character:
            self.add_xp_gold_window.show()

    def show_buy_items_window(self):
        if self.current_character:
            self.buy_items_window.show()

    def show_develop_window(self):
        if self.current_character:
            self.dev_char_window.show()

    def show_learn_skill_talent_window(self):
        if self.current_character:
            self.learn_skill_talent_window.show()

    def show_load_window(self):
        self.stacked_widget.setCurrentWidget(self.load_view)

    def show_save_window(self):
        if self.current_character:
            self.save_view.show()

    def save_current_character(self, filename: str) -> bool:
        if self.current_character:
            char_data = self.current_character.to_dict()
            return save_load_logic.save_character(char_data, filename)
        return False

    def load_character_from_file(self, filename: str):
        char_data = save_load_logic.load_character_data(filename)
        if char_data:
            self.set_new_character(Character(char_data))

    def get_save_list(self) -> list[dict]:
        return save_load_logic.list_saves()

    def delete_character_save(self, filename: str) -> bool:
        return save_load_logic.delete_save(filename)
