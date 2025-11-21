import sys
from PyQt6 import QtWidgets

from main_window import MainWindow
from app_view_model import AppsViewModel

def main():
    """
    Función principal para iniciar la aplicación.
    """
    app = QtWidgets.QApplication(sys.argv)

    # Crear una instancia del ViewModel y la Vista
    view_model = AppsViewModel()
    main_window = MainWindow(view_model)

    # Mostrar la ventana y ejecutar el bucle de eventos
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

