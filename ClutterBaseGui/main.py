# This Python file uses the following encoding: utf-8
import sys
#from PySide2 import QtWidgets, QtUiTools, QtCore
from PySide2 import QtSql
from PySide2.QtSql import QSqlQueryModel
from PySide2.QtCore import Qt
from PySide2 import QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class ImageDataModel(QSqlQueryModel):
    def __init__(self, parent=None):
       super().__init__(parent)
    def data(self,index,role=0):
        if index.column() in [2,3,4,5]:
            if role == Qt.ItemDataRole.DecorationRole :
                variant = QSqlQueryModel.data(self,index,Qt.ItemDataRole.DisplayRole)
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(variant)
                return pixmap
        else :
            value = QSqlQueryModel.data(self,index,role)
            return value

class ClutterDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ClutterDialog, self).__init__()
        self.setWindowTitle("Clutter Dialog")
        self.resize(800,400)
        self.grid_layout = QGridLayout()
        self.grid_layout.setObjectName("GridLayout")
        db_view_gb = QGroupBox("db_view")
        db_view_gb.setTitle("Database View")
        self.grid_layout.addWidget(db_view_gb,0,0)

#        db_controls = QGroupBox("DB Controls")
#        self.grid_layout.addWidget(db_controls,1,0)

#        db_controls_layout = QGridLayout()
#        db_controls.setLayout(db_controls_layout)
#        load_db = QPushButton("Load DB")
#        load_db.clicked.connect(self.load_db_pressed)
#        db_controls_layout.addWidget(load_db)

        self.create_db_control()

        self.setLayout(self.grid_layout)
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db_view_layout = QVBoxLayout()
        db_view_gb.setLayout(db_view_layout)
        self.database_view = QtWidgets.QTableView(db_view_gb)
        db_view_layout.addWidget(self.database_view)

#        layout = QtWidgets.QVBoxLayout()
#        loader = QtUiTools.QUiLoader()
#        ui_file = QtCore.QFile("cl.ui")
#        ui_file.open(QtCore.QFile.ReadOnly)
#        self.ui = loader.load(ui_file, self)
#        ui_file.close()
#        self.ui.load_db.clicked.connect(self.load_db_pressed)
#        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
#        self.database_view = QtWidgets.QTableView(self)
#        self.ui.db_layout.addWidget(self.database_view)

    def create_db_control(self):
        db_controls = QGroupBox("DB Controls")
        self.grid_layout.addWidget(db_controls,1,0)

        db_controls_layout = QGridLayout()
        db_controls.setLayout(db_controls_layout)
        load_db = QPushButton("Load DB")
        load_db.clicked.connect(self.load_db_pressed)
        row = 0
        db_controls_layout.addWidget(load_db, row, 0)
        row += 1
        self.query_text = QLineEdit()
        db_controls_layout.addWidget(self.query_text,row,0)
        run_query = QPushButton("Run Query")
        db_controls_layout.addWidget(run_query,row,1)
        run_query.clicked.connect(self.run_query)

    def run_query(self) :
        print(f"running query {self.query_text.text()}")


    def load_db_pressed(self):
        print("load db pressed")
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select DB file", "./", "Clutter Base Files(*.db)"
        )
        if file_name[0] != "":
            self.load_db(file_name[0])

    def resizeEvent(self,size):
       ...

    def load_db(self, file_name: str) -> None:
        self.db.setDatabaseName(file_name)
        self.connected = self.db.open()
        if not "Meshes" in self.db.tables():
            QtWidgets.QMessageBox.Critical(
                self,
                "Critical Error",
                "Not a Clutter Basefile",
                QtWidgets.QMessageBox.StandardButton.Abort,
            )
        query = ImageDataModel()
        queryColumns = "name,mesh_type, front_image, side_image, top_image, persp_image"
        query.setQuery(f"select {queryColumns} from Meshes;")
        self.database_view.setModel(query)
        self.database_view.resizeColumnToContents()
        self.database_view.resizeRowToContents()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # ...
    dialog = ClutterDialog()
    dialog.show()
    sys.exit(app.exec_())
