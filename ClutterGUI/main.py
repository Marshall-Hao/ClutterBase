#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
import sys

# from PySide2.QtWidgets import QApplication
from PySide2 import QtCore, QtSql, QtUiTools, QtWidgets
from PySide2.QtSql import QSqlQueryModel
from PySide2.QtCore import Qt

from PySide2.QtGui import *
from PySide2.QtWidgets import *


class ImageDateModel(QSqlQueryModel) :
    def __init__(self,parent=None) :
        super().__init__(parent)
    def data(self,index,role=0) :

        if index.column() in [2,3,4,5] :
           if role == Qt.ItemDataRole.DecorationRole :
               variant = QSqlQueryModel.data(self,index,Qt.ItemDataRole.DisplayRole)
               pixmap = QPixmap()
               pixmap.loadFromData(variant)
               return pixmap
        else :
            value=QSqlQueryModel.data(self,index,role)
            return value



class ClutterDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ClutterDialog, self).__init__()
        self.setWindowTitle("Clutter Dialog")
        self.resize(800,400)
        self.grid_layout = QGridLayout()
        self.grid_layout.setObjectName("GridLayout")
        db_view_gb = QGroupBox("Clutter Base")
        self.grid_layout.addWidget(db_view_gb,0,0)

        self.create_db_controls()

        self.setLayout(self.grid_layout)
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db_view_layout = QVBoxLayout()
        db_view_gb.setLayout(db_view_layout)
        self.database_view = QtWidgets.QTableView(db_view_gb)
        db_view_layout.addWidget(self.database_view)

    def create_db_controls(self) :
        db_controls = QGroupBox("DB Controls")
        self.grid_layout.addWidget(db_controls,1,0)

        db_controls_layout = QGridLayout()
        db_controls.setLayout(db_controls_layout)
        load_db = QPushButton("Load DB")
        load_db.clicked.connect(self.load_db_pressed)
        row=0
        db_controls_layout.addWidget(load_db,row,0)
        row+=1
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
            self, "Select DB File", "./", "Clutter Base Files (*.db)"
        )
        if file_name[0] != "":
            self.load_db(file_name[0])

    def resizeEvent(self,size) :
        ...
#        print("resize")
        self.database_view.resizeRowsToContents()
        self.database_view.resizeColumnsToContents()


    def load_db(self, file_name: str) -> None:
        self.db.setDatabaseName(file_name)
        self.connected = self.db.open()
        if not "Meshes" in self.db.tables():
            QtWidgets.QMessageBox.critical(
                self,
                "Critical Error",
                "Not a Clutter basefile",
                QtWidgets.QMessageBox.StandardButton.Abort,
            )
        query = ImageDateModel()
        queryColumns = "name,mesh_type,front_image,side_image,top_image,persp_image"
        query.setQuery(f"select {queryColumns} from Meshes;")
        self.database_view.setModel(query)
        self.database_view.resizeRowsToContents()
        self.database_view.resizeColumnsToContents()
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    # ...
    dialog = ClutterDialog()
    dialog.show()
    sys.exit(app.exec_())
