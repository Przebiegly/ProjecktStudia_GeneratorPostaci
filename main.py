import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont
from ui.window_connector import WindowConnector


def main():
    app = QApplication(sys.argv)


    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'MedievalSharp-Regular.ttf')
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
    else:
        print(f"BŁĄD: Nie udało się załadować czcionki z {font_path}. Upewnij się, że plik istnieje.")
    connector = WindowConnector()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()