LIGHT_BACKGROUND = "#f1f3f6"
LIGHT_WIDGET_BACKGROUND = "#f8f9fa"
DARK_BACKGROUND = "#2c313a"
DARK_WIDGET_BACKGROUND = "#373c47"

LIGHT_STYLE = f"""
QWidget {{
    font-family: Verdana, sans-serif;
    font-size: 10pt;
    color: #212529;
}}
QMainWindow, QFrame#left_panel, QFrame#right_panel {{
    background-color: {LIGHT_BACKGROUND};
}}
QLabel#title {{
    font-weight: bold;
    font-size: 11pt;
}}
QLineEdit, QTextEdit, QComboBox, QScrollArea#tags_scroll_area {{
    background-color: {LIGHT_WIDGET_BACKGROUND};
    border: 1px solid #ced4da;
    border-radius: 8px;
    padding: 5px;
    color: #212529;
}}
QTextEdit {{
    font-family: "Courier New", monospace;
}}
QPushButton {{
    background-color: #e9ecef;
    border: 1px solid #ced4da;
    border-radius: 8px;
    padding: 6px 12px;
}}
QPushButton:hover {{
    background-color: #dee2e6;
    border-color: #adb5bd;
}}
QPushButton#copy_button {{
    background-color: #007bff;
    color: white;
    font-weight: bold;
}}
QPushButton#copy_button:hover {{
    background-color: #0069d9;
}}
QComboBox QAbstractItemView {{
    background-color: {LIGHT_WIDGET_BACKGROUND};
    border: 1px solid #ced4da;
    selection-background-color: #007bff;
    color: #212529;
}}
QScrollBar:vertical {{
    border: none;
    background: #e9ecef;
    width: 10px;
}}
QScrollBar::handle:vertical {{
    background: #ced4da;
    min-height: 20px;
    border-radius: 5px;
}}
/* Estilo específico para as tags no modo claro */
QLabel[objectName="tag_label"] {{
    background-color: #e9ecef;
    border-radius: 8px;
    padding: 4px 8px;
    color: #212529; /* Adicionado para garantir o contraste */
}}
QPushButton[objectName="tag_remove_button"] {{
    background-color: #dee2e6;
    border-radius: 10px;
}}
QPushButton[objectName="suggestion_button"] {{
    background-color: {LIGHT_WIDGET_BACKGROUND};
    border: 1px solid #ced4da;
}}
"""

DARK_STYLE = f"""
QWidget {{
    font-family: Verdana, sans-serif;
    font-size: 10pt;
    color: #f8f9fa;
}}
QMainWindow, QFrame#left_panel, QFrame#right_panel {{
    background-color: {DARK_BACKGROUND};
}}
QLabel#title {{
    font-weight: bold;
    font-size: 11pt;
}}
QLineEdit, QTextEdit, QComboBox, QScrollArea#tags_scroll_area {{
    background-color: {DARK_WIDGET_BACKGROUND};
    border: 1px solid #495057;
    border-radius: 8px;
    padding: 5px;
    color: #f8f9fa;
}}
QTextEdit {{
    font-family: "Courier New", monospace;
}}
QPushButton {{
    background-color: #495057;
    border: 1px solid #6c757d;
    border-radius: 8px;
    padding: 6px 12px;
    color: #f8f9fa;
}}
QPushButton:hover {{
    background-color: #6c757d;
    border-color: #adb5bd;
}}
QPushButton#copy_button {{
    background-color: #0d6efd;
    color: white;
    font-weight: bold;
}}
QPushButton#copy_button:hover {{
    background-color: #0b5ed7;
}}
QComboBox QAbstractItemView {{
    background-color: {DARK_WIDGET_BACKGROUND};
    border: 1px solid #6c757d;
    selection-background-color: #0d6efd;
    color: #f8f9fa;
}}
QScrollBar:vertical {{
    border: none;
    background: {DARK_WIDGET_BACKGROUND};
    width: 10px;
}}
QScrollBar::handle:vertical {{
    background: #6c757d;
    min-height: 20px;
    border-radius: 5px;
}}
/* Estilo específico para as tags no modo escuro */
QLabel[objectName="tag_label"] {{
    background-color: #6c757d;
    border-radius: 8px;
    padding: 4px 8px;
    color: #f8f9fa; /* <<< CORREÇÃO AQUI */
}}
QPushButton[objectName="tag_remove_button"] {{
    background-color: #495057;
    border-radius: 10px;
}}
QPushButton[objectName="suggestion_button"] {{
    background-color: {DARK_WIDGET_BACKGROUND};
    border: 1px solid #6c757d;
}}
"""