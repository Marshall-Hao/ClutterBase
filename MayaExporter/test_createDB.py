#!/usr/bin/env python
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
from PySide2 import QtCore
import sys
from PySide2.QtCore import QCoreApplication, QTimer


def create_db():
    # Add your function logic here
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName("test.db")
    database.open()
    query = QSqlQuery()
    query.exec_("DROP TABLE IF EXISTS Meshes;");
    query.exec_("""
        Create table Meshes (id integer PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL,
        mesh_data BLOB NOT NULL,
        mesh_type TEXT CHECK(mesh_type IN('obj','usd','fbx')),
        front_image BLOB,
        side_image BLOB,
        top_image BLOB,
        persp_image BLOB
)""")
    # query.exec_("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)")
    # query.exec_("INSERT INTO test (name) VALUES ('Hello World')")
    # query.exec_("SELECT * FROM test")
    # while query.next():
    #     print(query.value(1))
    database.close()

if __name__ == "__main__":
    app = QtCore.QCoreApplication(sys.argv)

    # Run your function and then quit
    QTimer.singleShot(0, lambda: (create_db(), app.quit()))
   
    sys.exit(app.exec_())