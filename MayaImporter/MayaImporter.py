import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
from shiboken2 import wrapInstance

from PySide2 import QtWidgets, QtUiTools, QtCore, QtSql, QtGui
from PySide2.QtSql import QSqlQueryModel
from PySide2.QtCore import Qt

from PySide2.QtGui import *
from PySide2.QtWidgets import *
import tempfile


def get_main_window() :
    # not api1 code here
    window = maya.OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(window), QtWidgets.QDialog)


class ImageDataModel(QSqlQueryModel) :
    def __init__(self, parent=get_main_window()) :
        super().__init__(parent)
    def data(self,index,role=0) :
        if index.column() in [3, 4, 5, 6] :

            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole :
                return None

            if role == Qt.ItemDataRole.DecorationRole :
                variant = QSqlQueryModel.data(self, index, Qt.ItemDataRole.DisplayRole)
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(variant)
                return pixmap
        else :
            value = QSqlQueryModel.data(self, index, role)
            return value


class ClutterDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ClutterDialog, self).__init__()
        self.setWindowTitle("ClutterDialog")
        self.resize(800, 400)
        self.grid_layout = QGridLayout()
        self.grid_layout.setObjectName("GridLayout")
        db_view_gb = QGroupBox("db_view")
        db_view_gb.setTitle("Database")
        self.grid_layout.addWidget(db_view_gb, 0, 0)

        self.create_db_controls()

        self.setLayout(self.grid_layout)
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db_view_layout = QVBoxLayout()
        db_view_gb.setLayout(db_view_layout)
        self.database_view = QtWidgets.QTableView(db_view_gb)
        db_view_layout.addWidget(self.database_view)

        self.database_view.doubleClicked.connect(self.load_mesh)

    def load_mesh(self, index) :
        print("loading mesh")
        model = self.database_view.model()
        mesh_id = model.data(model.index(index.row(), 0))
        print(f"{mesh_id}")
        #query = """Select mesh_data, mesh_type from Meshes where ID = ?;"""
        query = QtSql.QSqlQuery()
        result = query.exec_(f"Select mesh_data, mesh_type from Meshes where ID = {mesh_id};")
        if result :
            print("got result")
            import_type = {'obj' : 'OBJ', 'usd' : 'USD Import', 'fbx' : 'FBX'}
            query.next()
            mesh_data = query.value(0)
            mesh_type = query.value(1)
            with tempfile.TemporaryDirectory() as temp_dir :
                out_name = f"{temp_dir}/mesh.{mesh_type}"
                with open(out_name, "wb") as file :
                    file.write(mesh_data)
                cmds.file(out_name, gr=True, i=True, groupName="ClutterbaseImport", type=import_type[mesh_type])

    def create_db_controls(self) :
        db_controls = QGroupBox("DB Controls")
        self.grid_layout.addWidget(db_controls, 1, 0)
        db_controls_layout = QGridLayout()
        db_controls.setLayout(db_controls_layout)
        load_db = QPushButton("Load DB")
        load_db.clicked.connect(self.load_db_pressed)
        row = 0
        db_controls_layout.addWidget(load_db, row, 0)
        row += 1
        self.query_text = QLineEdit()
        db_controls_layout.addWidget(self.query_text, row, 0)
        run_query = QPushButton("Run Query")
        db_controls_layout.addWidget(run_query, row, 1)
        run_query.clicked.connect(self.run_query)

    def run_query(self) :
        print(f"running query {self.query_text.text()}")

    def load_db_pressed(self):
        print("load db pressed")
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select DB File", "../", "Clutter Base Files (*.db)"
        )
        if file_name[0] != "":
            self.load_db(file_name[0])

    def resizeEvent(self, size) :
        self.database_view.resizeRowsToContents()
        self.database_view.resizeColumnsToContents()

    def load_db(self, file_name: str):
        self.db.setDatabaseName(file_name)
        self.connected = self.db.open()
        if not "Meshes" in self.db.tables():
            QtWidgets.QMessageBox.critical(
                self,
                "Critical Error",
                "Not a Clutter basefile",
                QtWidgets.QMessageBox.StandardButton.Abort,
            )
        model = ImageDataModel()
        queryColumns = "id, name, mesh_type, front_image, side_image, top_image, persp_image"
        model.setQuery(f"select {queryColumns} from Meshes")
        self.database_view.setModel(model)
        self.database_view.resizeRowsToContents()
        self.database_view.resizeColumnsToContents()


if __name__ == "__main__" :
    # see if the dialogue is already open
    try :
        clutterbase_dialogue.close()
        clutterbase_dialogue.deleteLater()
    except :
        pass
    
    clutterbase_dialogue = ClutterDialog()
    clutterbase_dialogue.show()