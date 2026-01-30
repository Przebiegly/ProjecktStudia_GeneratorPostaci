import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont

from logic.character_auto_generator import resource_path
from ui.window_connector import WindowConnector


def main():
    app = QApplication(sys.argv)
    font_path = resource_path(os.path.join('fonts', 'MedievalSharp-Regular.ttf'))
    font_id = QFontDatabase.addApplicationFont(font_path)
    connector = WindowConnector()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()