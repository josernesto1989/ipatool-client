from PyQt6 import QtWidgets

class AuthWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Autenticación")
        self.setModal(True)
        self.setup_ui()
        self._username = None
        self._password = None

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.label = QtWidgets.QLabel("Por favor, ingresa tus credenciales de Apple ID:")
        layout.addWidget(self.label)
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Apple ID")
        layout.addWidget(self.username_input)
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        self.username_input.textChanged.connect(self.on_change_credentials)
        self.password_input.textChanged.connect(self.on_change_credentials)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        
    def on_change_credentials(self):
        self._username = self.username_input.text()
        self._password = self.password_input.text()
         
    def get_credentials(self):
        return self._username, self._password