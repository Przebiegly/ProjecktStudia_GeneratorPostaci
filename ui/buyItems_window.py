from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QListWidget,
    QLineEdit,
)
from PyQt6.QtCore import Qt
from logic.character_buy_items import get_categorized_items, buy_item
from .styles import MAIN_WINDOW_STYLE


class BuyItemsWindow(QMainWindow):
    def __init__(self, connector):
        super().__init__()
        self.connector = connector
        self.categorized_items = get_categorized_items()

        self.setWindowTitle("Sklep")
        self.setMinimumSize(1200, 800)
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
        top_layout = QVBoxLayout(main_widget)
        top_layout.setContentsMargins(15, 15, 15, 15)
        columns_layout = QHBoxLayout()

        self.gold_label = QLabel("Twoje Złoto: 0 ZK")
        self.gold_label.setObjectName("HeaderLabel")
        self.gold_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.gold_label)

        category_box = QGroupBox("Kategorie")
        category_layout = QVBoxLayout(category_box)
        self.category_list = QListWidget()
        category_layout.addWidget(self.category_list)
        columns_layout.addWidget(category_box, 1)

        item_box = QGroupBox("Przedmioty")
        item_layout = QVBoxLayout(item_box)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Wyszukaj w tej kategorii...")
        self.search_input.textChanged.connect(self._filter_items)

        self.item_table = QTableWidget()
        self.item_table.setColumnCount(2)
        self.item_table.setHorizontalHeaderLabels(["Przedmiot", "Koszt (Złota)"])
        self.item_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.item_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.item_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        header = self.item_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        self.buy_button = QPushButton("Kup Wybrany Przedmiot")

        item_layout.addWidget(self.search_input)
        item_layout.addWidget(self.item_table)
        item_layout.addWidget(self.buy_button)
        columns_layout.addWidget(item_box, 3)

        top_layout.addLayout(columns_layout)

        self.category_list.currentItemChanged.connect(self._display_items_for_category)
        self.item_table.itemSelectionChanged.connect(self._update_buy_button_state)
        self.buy_button.clicked.connect(self._buy_selected_item)

    def populate_data(self):
        character = self.connector.current_character
        if not character:
            self.close()
            return

        self.gold_label.setText(f"Twoje Złoto: <b>{character.gold:.2f}</b> Złoto")
        self.category_list.clear()
        self.category_list.addItems(self.categorized_items.keys())

        if self.category_list.count() > 0:
            self.category_list.setCurrentRow(0)
        self._update_buy_button_state()

    def _display_items_for_category(self, current_item, previous_item):
        self.search_input.clear()
        self._filter_items()

    def _filter_items(self):
        current_category_item = self.category_list.currentItem()
        if not current_category_item:
            return

        category_name = current_category_item.text()
        search_text = self.search_input.text().lower()

        items_in_category = self.categorized_items.get(category_name, [])

        self.item_table.setRowCount(0)
        for item_data in items_in_category:
            if search_text in item_data["name"].lower():
                row_position = self.item_table.rowCount()
                self.item_table.insertRow(row_position)

                name_item = QTableWidgetItem(item_data["name"])
                cost_item = QTableWidgetItem(f"{item_data[ 'cost' ]:.2f}")
                cost_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.item_table.setItem(row_position, 0, name_item)
                self.item_table.setItem(row_position, 1, cost_item)

        self._update_buy_button_state()

    def _update_buy_button_state(self):
        character = self.connector.current_character
        if not character or not self.item_table.selectedItems():
            self.buy_button.setEnabled(False)
            return

        selected_row = self.item_table.currentRow()
        cost_text = self.item_table.item(selected_row, 1).text()
        item_cost = float(cost_text)

        self.buy_button.setEnabled(character.gold >= item_cost)

    def _buy_selected_item(self):
        character = self.connector.current_character
        selected_row = self.item_table.currentRow()
        if not character or selected_row < 0:
            return

        item_name = self.item_table.item(selected_row, 0).text()
        item_cost = float(self.item_table.item(selected_row, 1).text())

        if buy_item(character, item_name, item_cost):
            self.gold_label.setText(f"Twoje Złoto: <b>{character.gold:.2f}</b> Złoto")
            self._update_buy_button_state()
            self.connector.update_character_data()

    def showEvent(self, event):
        self.populate_data()
        super().showEvent(event)
