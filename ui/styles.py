MAIN_WINDOW_STYLE = """
    QMainWindow, QWidget {
        background-color: #262626;
        color: #E0E0E0;
        font-family: "MedievalSharp";
        font-size: 13pt; 
    }

    #TitleLabel {
        font-size: 30pt;
        font-weight: bold;
        padding: 15px;
        color: #D4AF37;
        border-bottom: 1px solid #4A4A4A;
        margin-bottom: 10px;
    }

    QGroupBox {
        border: 1px solid #4A4A4A;
        border-radius: 5px;
        margin-top: 1em;
        padding: 10px 15px; 
        font-size: 14pt;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 10px 25px;
        background-color: #333333;
        color: #D4AF37;
        font-size: 20pt;
        font-weight: bold;
        border: 1px solid #4A4A4A;
        border-radius: 5px;
    }

    #DevelopGroupBox {
        background-color: #2C2C2C;
        border: 1px solid #1E1E1E;
        border-top: 1px solid #5A5A5A;
        border-radius: 6px;
        margin-top: 1.5em;
        padding: 15px;
    }
    
    #DevelopGroupBox::title {
        padding: 5px 20px;
        background-color: #1E1E1E;
        border: 1px solid #5A5A5A;
        border-bottom: 1px solid #D4AF37;
    }
    
    #HeaderLabel {
        font-size: 15pt;
        font-weight: bold;
        color: #E0E0E0;
        padding: 8px;
        background-color: #333333;
        border-radius: 5px;
        border: 1px solid #4A4A4A;
    }
    #HeaderLabel > b {
        color: #D4AF37;
    }
    
    #HorizontalDivider {
        max-height: 2px;
        border-top: 1px solid #1E1E1E;
        border-bottom: 1px solid #5A5A5A;
    }

    QLabel {
        font-size: 13pt;
        padding: 2px;
        background-color: transparent;
    }
    QFormLayout QLabel {
        color: #AAAAAA;
        font-size: 13pt;
        font-weight: normal;
    }

    #Portrait {
        border: 2px solid #4A4A4A;
        background-color: #1E1E1E;
        border-radius: 5px;
    }

    QPushButton {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #5A5A5A, stop: 1 #404040);
        border: 1px solid #D4AF37;
        padding: 8px;
        border-radius: 5px;
        font-size: 13pt;
        color: #D4AF37;
        min-height: 40px;
        min-width: 120px;
    }
    
    QPushButton:hover {
        background-color: #6A6A6A;
        border-color: #F7D872;
    }
    
    QPushButton:pressed {
        background-color: #3A3A3A;
    }
    
    QPushButton:disabled {
        background-color: #383838;
        color: #777;
        border: 1px solid #555;
    }

    QComboBox, QLineEdit {
        background-color: #383838;
        padding: 6px; 
        border: 1px solid #5A5A5A;
        border-radius: 3px;
        font-size: 12pt; 
        color: #E0E0E0;
    }
    QComboBox:hover, QLineEdit:hover { border-color: #D4AF37; }
    QComboBox::drop-down { border: none; }
    QComboBox QAbstractItemView {
        background-color: #383838;
        border: 1px solid #D4AF37;
        selection-background-color: #5A5A5A;
        color: #E0E0E0;
    }

    QListWidget, QTableWidget {
        background-color: #262626;
        border: 1px solid #4A4A4A;
        padding: 5px;
        font-size: 16pt;
        outline: 0px;
    }
    QHeaderView::section {
        background-color: #262626;
        color: #D4AF37;
        padding: 5px;
        border: 1px solid #4A4A4A;
        font-size: 13pt;
        font-weight: bold;
    }

    QListWidget::item:hover, QTableWidget::item:hover {
        background-color: #3E3E3E;
    }
    QListWidget::item:selected, QListWidget::item:selected:!active,
    QTableWidget::item:selected, QTableWidget::item:selected:!active {
        background-color: #4A4A4A;
        color: #FFFFFF;
        border: 1px solid #D4AF37;
        font-weight: bold;
    }

    #InventoryItem {
        background-color: #333333;
        border: 1px solid #4A4A4A;
        border-radius: 4px;
        margin-bottom: 5px;
    }
    #ItemIcon {
        border: 1px dashed #666;
        background-color: #2A2A2A;
        color: #777;
        font-size: 10pt;
    }
    #ItemName {
        font-size: 14pt;
        font-weight: bold;
    }

    QScrollBar:vertical {
        border: 1px solid #4A4A4A; background: #333333; width: 15px; margin: 15px 0 15px 0;
    }
    
    QScrollBar::handle:vertical { background: #5A5A5A; min-height: 20px; border-radius: 3px; }
    QScrollBar::handle:vertical:hover { background: #D4AF37; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
"""
