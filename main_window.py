# Este módulo define la ventana principal (la Vista).
# Se encarga de la interfaz de usuario y la comunicación con el ViewModel.
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QUrl, Qt, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence
import ipatool_helper
import threading
from auth_window import AuthWindow

class MainWindow(QtWidgets.QMainWindow):
    """
    La ventana principal de la aplicación.
    Carga el diseño de Qt Designer y maneja los eventos de la UI.
    """
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        # Cargar el diseño de la UI desde el archivo .ui generado por Qt Designer.
        try:
            uic.loadUi('mainwindow.ui', self)
        except FileNotFoundError:
            # En caso de que el archivo .ui no exista, se crea una interfaz básica.
            # Este es un buen fallback, pero el usuario debe crear el archivo .ui
            # para una experiencia completa.
            self.setWindowTitle("Ipatool-Cli")
            self.setGeometry(100, 100, 800, 600)

            # Widgets de la interfaz básica
            self.dropLabel = QtWidgets.QLabel("Arrastra y suelta tus archivos aquí", self)
            self.dropLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.fileListView = QtWidgets.QListView(self)
            self.loadFilesButton = QtWidgets.QPushButton("Cargar Archivos", self)

            # Diseño de la interfaz básica
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(self.dropLabel)
            layout.addWidget(self.fileListView)
            layout.addWidget(self.loadFilesButton)

            central_widget = QtWidgets.QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)
        
        self.lineEdit_Search.textChanged.connect(self.on_search_text_changed)
        self.pushButton_search.clicked.connect(self.on_search_clicked)
        self.tableView_search_results.setModel(self.view_model)
        self.pushButton_download.clicked.connect(self.on_download_clicked)
        self.tableView_search_results.doubleClicked.connect(self.on_download_clicked)
        self.actionAutenticar_usuario_sin_2FA.triggered.connect(self.on_authenticate_user)  

    def on_search_text_changed(self, text):
        self.pushButton_search.setEnabled(len(text.strip()) > 3)
        
    def on_search_clicked(self):
        search_text = self.lineEdit_Search.text()
        # Aquí deberías llamar a un método del view_model para realizar la búsqueda
        # Por ejemplo: self.view_model.search_apps(search_text)
        self.view_model.search_apps(search_text)

    def showFinishMessage(self):
        """
        Muestra un mensaje de información al usuario.
        """
        QtWidgets.QMessageBox.information(self, "Completado", "El proceso de resumen ha finalizado.")

    def on_download_clicked(self):
        selected_indexes = self.tableView_search_results.selectionModel().selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            app_id = self.view_model._apps_dict[row]["bundleID"]
            print(f"Descargando app con ID: {app_id}")
            threading.Thread(target=ipatool_helper.download_app_by_id, args=(app_id,None)).start()
    
    def download_finished_callback(self,message="Descarga completada"):
        QtWidgets.QMessageBox.information(self, "Descarga", message)
        
    def on_authenticate_user(self):
        auth_window = AuthWindow(self)
        if auth_window.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            username, password = auth_window.get_credentials()
            stdout, stderr = ipatool_helper.authenticate_user(username, password)
            # print(f'error:{len(stderr)}')
            # print(f'stdout:{stdout}')
            # print(f'stderr:{stderr}')
            message =stdout if len(stderr)==0 else "Autenticación fallida"
            QtWidgets.QMessageBox.information(self, "Autenticación", message)
           