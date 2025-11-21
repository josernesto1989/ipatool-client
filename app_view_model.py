# Este módulo actúa como el "pegamento" entre la Vista y el Modelo.
# Maneja la lógica de la UI y los datos de la aplicación.
from PyQt6.QtCore import QObject, QStringListModel, pyqtSignal, Qt, QAbstractItemModel
import ipatool_helper


class AppsViewModel(QAbstractItemModel):
    """
    El ViewModel de la aplicación.
    Gestiona la lógica de la UI, los modelos de datos y se comunica con el ExcelProcessor.
    """
    resumeCompleted = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self._apps_dict = {}
        self._header_labels = ["name", "version", "bundleID", "price", "id"]
        
        
    def update_apps(self, apps_dict):
        """
        Actualiza el diccionario de aplicaciones y notifica a la UI.
        """
        self._apps_dict = apps_dict
        self.resumeCompleted.emit()
    
    def index(self, row, column, parent=None):
        return self.createIndex(row, column)
    
    def rowCount(self, parent=None):
        return len(self._apps_dict)
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._apps_dict[index.row()][self._header_labels[index.column()]]            
        return None
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._header_labels[section]
        return None
    
    def columnCount(self, parent=None):
        return 5  # Por ejemplo, Nombre y Versión
    
    def search_apps(self, name):    
        self._apps_dict=ipatool_helper.find_app_by_name(name)
        self.layoutChanged.emit()