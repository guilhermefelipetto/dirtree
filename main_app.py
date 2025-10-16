import os
import sys

from PyQt5.QtCore import (QEasingCurve, QPropertyAnimation, Qt, QThread,
                          QTimer, pyqtSignal)
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QComboBox, QFileDialog, QFrame,
                             QGraphicsOpacityEffect, QHBoxLayout, QLabel,
                             QLineEdit, QMainWindow, QPushButton, QScrollArea,
                             QSplitter, QTextEdit, QVBoxLayout, QWidget)

from draw_structure_logic import draw_tree
from styles import DARK_STYLE, LIGHT_STYLE


class Worker(QThread):
    finished = pyqtSignal(str)
    def __init__(self, path, params):
        super().__init__()
        self.path = path
        self.params = params
    def run(self):
        if not self.path or not os.path.isdir(self.path):
            self.finished.emit("")
            return
        base_name = os.path.basename(os.path.normpath(self.path))
        header = f"{base_name}/\n"
        try:
            tree_structure = draw_tree(self.path, **self.params, is_root=True)
            self.finished.emit(header + tree_structure)
        except Exception as e:
            self.finished.emit(f"Ocorreu um erro: {e}")

class TagWidget(QWidget):
    removed = pyqtSignal(str)
    def __init__(self, text):
        super().__init__()
        self.text = text
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        self.label = QLabel(text)
        self.label.setObjectName("tag_label")
        self.remove_button = QPushButton("x")
        self.remove_button.setObjectName("tag_remove_button")
        self.remove_button.setFixedSize(20, 20)
        self.remove_button.clicked.connect(self.emit_removed)
        layout.addWidget(self.label)
        layout.addWidget(self.remove_button)
    def emit_removed(self):
        self.removed.emit(self.text)
        self.deleteLater()

class TagInputWidget(QWidget):
    tags_changed = pyqtSignal()
    def __init__(self, title, suggestions=None):
        super().__init__()
        self.all_tags = set()
        self.suggestions = suggestions or []
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        title_label = QLabel(title)
        title_label.setObjectName("title")
        main_layout.addWidget(title_label)
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Digite um valor e pressione Enter...")
        self.entry.returnPressed.connect(self.add_tag_from_entry)
        main_layout.addWidget(self.entry)
        if self.suggestions:
            self.suggestions_widget = QWidget()
            self.suggestions_layout = QHBoxLayout(self.suggestions_widget)
            self.suggestions_layout.setContentsMargins(0, 0, 0, 0)
            self.suggestions_layout.setSpacing(5)
            self.suggestions_layout.setAlignment(Qt.AlignLeft)
            main_layout.addWidget(self.suggestions_widget)
            self.update_suggestions()
        self.tags_area = QWidget()
        self.tags_layout = QHBoxLayout(self.tags_area)
        self.tags_layout.setContentsMargins(0, 0, 0, 0)
        self.tags_layout.setAlignment(Qt.AlignLeft)
        scroll = QScrollArea()
        scroll.setObjectName("tags_scroll_area")
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.tags_area)
        scroll.setFixedHeight(60)
        main_layout.addWidget(scroll)
    def add_tag(self, tag_text):
        if tag_text and tag_text not in self.all_tags:
            self.all_tags.add(tag_text)
            tag_widget = TagWidget(tag_text)
            tag_widget.removed.connect(self.remove_tag)
            self.tags_layout.addWidget(tag_widget)
            self.update_suggestions()
            self.tags_changed.emit()
    def add_tag_from_entry(self):
        text = self.entry.text().strip()
        self.add_tag(text)
        self.entry.clear()
    def remove_tag(self, tag_text):
        if tag_text in self.all_tags:
            self.all_tags.remove(tag_text)
            self.update_suggestions()
            self.tags_changed.emit()
    def update_suggestions(self):
        if not hasattr(self, 'suggestions_layout'): return
        for i in reversed(range(self.suggestions_layout.count())): 
            self.suggestions_layout.itemAt(i).widget().setParent(None)
        for suggestion in self.suggestions:
            if suggestion not in self.all_tags:
                btn = QPushButton(suggestion)
                btn.setObjectName("suggestion_button")
                btn.setCursor(Qt.PointingHandCursor)
                btn.clicked.connect(lambda _, s=suggestion: self.add_tag(s))
                self.suggestions_layout.addWidget(btn)
    def get_tags(self):
        return list(self.all_tags)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Estrutura de Diretórios")
        self.setGeometry(100, 100, 1200, 700)
        self.is_dark_mode = False
        self.pending_text_update = ""

        self.splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.splitter)

        left_panel = QFrame()
        left_panel.setObjectName("left_panel")
        left_panel.setFixedWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)
        left_layout.setContentsMargins(20, 20, 20, 20)
        dir_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Selecione um diretório...")
        self.path_edit.textChanged.connect(self.trigger_tree_generation)
        dir_button = QPushButton("Procurar...")
        dir_button.clicked.connect(self.select_directory)
        dir_layout.addWidget(self.path_edit)
        dir_layout.addWidget(dir_button)
        left_layout.addLayout(dir_layout)
        self.ignore_folders = TagInputWidget("Ignorar Pastas:", suggestions=["__pycache__", ".git", "node_modules", "venv"])
        self.ignore_files = TagInputWidget("Ignorar Arquivos:", suggestions=[".DS_Store"])
        self.ignore_extensions = TagInputWidget("Ignorar Extensões:", suggestions=[".log", ".tmp", ".bak", ".pdf", ".pyc"])
        self.always_include = TagInputWidget("Sempre Incluir:")
        self.ignore_folders.tags_changed.connect(self.trigger_tree_generation)
        self.ignore_files.tags_changed.connect(self.trigger_tree_generation)
        self.ignore_extensions.tags_changed.connect(self.trigger_tree_generation)
        self.always_include.tags_changed.connect(self.trigger_tree_generation)
        left_layout.addWidget(self.ignore_folders)
        left_layout.addWidget(self.ignore_files)
        left_layout.addWidget(self.ignore_extensions)
        left_layout.addWidget(self.always_include)
        sort_layout = QVBoxLayout()
        sort_layout.setSpacing(5)
        sort_label = QLabel("Opções de Ordenação")
        sort_label.setObjectName("title")
        sort_layout.addWidget(sort_label)
        self.root_sort_combo = self.create_sort_combobox()
        self.subdir_sort_combo = self.create_sort_combobox()
        self.root_sort_combo.currentIndexChanged.connect(self.trigger_tree_generation)
        self.subdir_sort_combo.currentIndexChanged.connect(self.trigger_tree_generation)
        sort_layout.addWidget(QLabel("Diretório Raiz:"))
        sort_layout.addWidget(self.root_sort_combo)
        sort_layout.addWidget(QLabel("Subdiretórios:"))
        sort_layout.addWidget(self.subdir_sort_combo)
        left_layout.addLayout(sort_layout)
        left_layout.addStretch()
        self.theme_button = QPushButton()
        self.theme_button.setCursor(Qt.PointingHandCursor)
        self.theme_button.clicked.connect(self.toggle_theme)
        left_layout.addWidget(self.theme_button)

        right_panel = QFrame()
        right_panel.setObjectName("right_panel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)

        self.tree_output = QTextEdit()
        self.tree_output.setReadOnly(True)
        
        self.opacity_effect = QGraphicsOpacityEffect(self.tree_output)
        self.tree_output.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.copy_button = QPushButton("Copiar")
        self.copy_button.setObjectName("copy_button")
        self.copy_button.setFixedSize(90, 30)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        
        self.copy_feedback_timer = QTimer(self)
        self.copy_feedback_timer.setSingleShot(True)
        self.copy_feedback_timer.timeout.connect(self._revert_copy_button_style)
        
        top_right_layout = QHBoxLayout()
        top_right_layout.addStretch()
        top_right_layout.addWidget(self.copy_button)
        right_layout.addLayout(top_right_layout)
        right_layout.addWidget(self.tree_output)

        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([400, 800])

        self.toggle_theme()

    def create_sort_combobox(self):
        combo = QComboBox()
        combo.addItem("Diretórios primeiro (A-Z)", "dirs_first_az")
        combo.addItem("Diretórios primeiro (Z-A)", "dirs_first_za")
        combo.addItem("Arquivos primeiro (A-Z)", "files_first_az")
        combo.addItem("Arquivos primeiro (Z-A)", "files_first_za")
        return combo

    def select_directory(self):
        path = QFileDialog.getExistingDirectory(self, "Selecione o Diretório Raiz")
        if path:
            self.path_edit.setText(path)

    def trigger_tree_generation(self):
        if not self.path_edit.text():
            self.update_output("")
            return
        params = {
            "ignore_folders": self.ignore_folders.get_tags(),
            "ignore_files": self.ignore_files.get_tags(),
            "ignore_extensions": self.ignore_extensions.get_tags(),
            "always_include": self.always_include.get_tags(),
            "root_sort_key": self.root_sort_combo.currentData(),
            "subdir_sort_key": self.subdir_sort_combo.currentData(),
        }
        path = self.path_edit.text()
        self.update_output("Processando...")
        self.worker = Worker(path, params)
        self.worker.finished.connect(self.update_output)
        self.worker.start()

    def update_output(self, result):
        self.pending_text_update = result
        if self.animation.state() == QPropertyAnimation.Running:
            self.animation.stop()
        self.animation.setStartValue(self.opacity_effect.opacity())
        self.animation.setEndValue(0.0)
        try: self.animation.finished.disconnect()
        except TypeError: pass
        self.animation.finished.connect(self._on_fade_out_finished)
        self.animation.start()

    def _on_fade_out_finished(self):
        self.tree_output.setPlainText(self.pending_text_update)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        try: self.animation.finished.disconnect()
        except TypeError: pass
        self.animation.start()

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.tree_output.toPlainText())
        
        self.copy_button.setText("Copiado!")
        self.copy_button.setStyleSheet("background-color: #28a745; color: white; font-weight: bold;")
        self.copy_button.setEnabled(False)
        
        self.copy_feedback_timer.start(1500)

    def _revert_copy_button_style(self):
        self.copy_button.setText("Copiar")
        self.copy_button.setStyleSheet("") 
        self.copy_button.setEnabled(True)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            app.setStyleSheet(DARK_STYLE)
            self.theme_button.setText("Modo Claro")
        else:
            app.setStyleSheet(LIGHT_STYLE)
            self.theme_button.setText("Modo Escuro")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
