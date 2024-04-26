import sys

from PySide2.QtGui import QCloseEvent

import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import pymel.core as pm
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel,QSql
from pathlib import Path
from shiboken2 import wrapInstance
import tempfile
import pymel.core as pm


def get_main_window():
    """this returns the maya main window for parenting"""
    window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(window), QDialog)


class ClutterBaseExporter(QDialog):
    def __init__(self, parent=get_main_window()):
        """init the class and setup dialog"""
        super().__init__(parent)
        self.database = QSqlDatabase.addDatabase("QSQLITE")

        # Set the GUI components and layout
        self.setWindowTitle("ClutterBase Exporter")
        self.resize(800, 200)
        grid_layout = QGridLayout(self)

        row = 0
        # set export options
        db_controls_row = 0
        export_gb = QGroupBox("Export Options")
        export_gb_layout = QGridLayout()
        export_gb.setLayout(export_gb_layout)
        grid_layout.addWidget(export_gb, row, 0)
        label = QLabel("Export Type", export_gb)
        export_gb_layout.addWidget(label, db_controls_row, 0, 1, 1)
        self.export_type = QComboBox(export_gb)
        self.export_type.addItem("OBJ")
        self.export_type.addItem("USD")
        self.export_type.addItem("FBX")
        export_gb_layout.addWidget(self.export_type, db_controls_row, 1, 1, 1)
        db_controls_row+=1
        self.image_width = QSpinBox(export_gb)
        self.image_width.setRange(32, 1024)
        self.image_width.setValue(256)
        label = QLabel("Image Width", export_gb)
        export_gb_layout.addWidget(label, db_controls_row, 0, 1, 1)
        export_gb_layout.addWidget(self.image_width, db_controls_row, 1, 1, 1)
        self.image_height = QSpinBox(export_gb)
        self.image_height.setRange(32, 1024)
        self.image_height.setValue(256)
        label = QLabel("Image Height", export_gb)
        export_gb_layout.addWidget(label, db_controls_row, 2, 1, 1)
        export_gb_layout.addWidget(self.image_height, db_controls_row, 3, 1, 1)

        db_controls_row+=1
        import_selection = QPushButton("add selection to db", export_gb)
        import_selection.clicked.connect(self.import_selection_clicked)
        export_gb_layout.addWidget(import_selection, db_controls_row, 1, 1, 1)

    
        # Add the database controls
        row+=1
        controls_gb = QGroupBox("DB Controls")
        controls_gb_layout = QGridLayout()
        controls_gb.setLayout(controls_gb_layout)
        grid_layout.addWidget(controls_gb,row,0) 

        load_db_button = QPushButton("Load Database", controls_gb)
        load_db_button.clicked.connect(self.load_db_clicked)
        controls_gb_layout.addWidget(load_db_button,row,0)
        new_db_button = QPushButton("New Database", controls_gb)
        new_db_button.clicked.connect(self.new_db_clicked)
        controls_gb_layout.addWidget(new_db_button,row,1)

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        self.database.close()
        return super().closeEvent(arg__1)
    
    def import_selection_clicked(self) :
        # Get the selected Objects
        current_view = cmds.getPanel( withFocus = True)
        objects = cmds.ls(sl=True)
        if len(objects) == 0 :
            cmds.warning("No objects selected")
            return
        temp_dir = tempfile.mkdtemp()
        cmds.hide( all=True )
        # iterate for each of the object
        for obj in objects :
            cmds.group(empty=True, world=True, name="exportGRP")
            # duplicate
            cmds.showHidden("exportGRP")
            for item in cmds.listRelatives(obj, f=True):
                # note the rr flag here to avoid name clashes on export
                dup_name=cmds.duplicate(item,rr=True)
                cmds.parent(dup_name, "exportGRP")

            cmds.select("exportGRP")
            cmds.CenterPivot()
            cmds.move(0, 0, 0, "exportGRP", rotatePivotRelative=True)
            self._save_screenshots(temp_dir,obj)
            # export
            if self.export_type.currentText() == "OBJ" :                
                cmds.file(temp_dir+"/obj.obj",pr=1,typ="OBJexport",exportSelected=1,
                            op="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1",force=True)
                export_file_name = temp_dir + "/obj.obj"

            elif self.export_type.currentText() == "USD" :
                cmds.file(temp_dir+"/usd",pr=1,typ="USD Export",exportSelected=1,
                          op="defaultUSDFormat=usda;mergeTransformAndShape=1;exportDisplayColor=1;exportDisplayColor=1;exportDisplayOpacity=1;exportUVs=1;exportNormals=1;exportMaterialAssignments=1;exportVisibility=1;exportCameras=1;exportLights=1;shadingMode=useRegistry")
                export_file_name = temp_dir + "/usd.usd"
            elif self.export_type.currentText() == "FBX" :
                cmds.file(temp_dir+"/fbx.fbx",pr=1,typ="FBX export",exportSelected=1)
                export_file_name = temp_dir + "/fbx.fbx"
                
            cmds.delete("exportGRP")
            query = QSqlQuery()
            query.prepare("""INSERT into Meshes (name,mesh_data,mesh_type,front_image,side_image,top_image,persp_image) VALUES(?,?,?,?,?,?,?)""")
            
            obj_data=self._loadBlob(export_file_name)
            persp = self._loadBlob(f"{temp_dir}/Persp.png")
            side = self._loadBlob(f"{temp_dir}/Side.png")
            front = self._loadBlob(f"{temp_dir}/Front.png")
            top = self._loadBlob(f"{temp_dir}/Top.png")

            query.bindValue(0,obj)
            query.bindValue(1,obj_data,QSql.In | QSql.Binary)
            mesh_type = self.export_type.currentText().lower()
            query.bindValue(2,mesh_type)
            query.bindValue(3,front,QSql.In | QSql.Binary)
            query.bindValue(4,side,QSql.In | QSql.Binary)
            query.bindValue(5,top,QSql.In | QSql.Binary)
            query.bindValue(6,persp,QSql.In | QSql.Binary)
            query.exec_()
            self.database.commit()
        # clean up
        cmds.showHidden( all=True )
        # clean up the temp directory
        # removed all files in temp dir
        for file in Path(temp_dir).iterdir() :
            file.unlink()
        Path(temp_dir).rmdir()



    def _loadBlob(self,name : str) :
        with open(name,'rb') as file :
            blob_data = file.read()
        print(f"loaded blob {len(blob_data)} bytes")
        return QByteArray(blob_data)

    def load_db_clicked(self) :
        project_directory = cmds.workspace(q=True, rd=True)
        db_name=QFileDialog.getOpenFileName(self,"Open Database File",project_directory,"Databases (*.db *.sqlite)")        

        if db_name is not None :
            self.database.setDatabaseName(db_name[0])
            self.database.open()
            # check to see if it is a valid database
            if not "Meshes" in self.database.tables():
                QMessageBox.critical(
                    self,
                    "CRITICAL ERROR",
                    "Not a valid ClutterBase File",
                    QMessageBox.StandardButton.Abort,
                )
                return

    def new_db_clicked(self) :
        project_directory = cmds.workspace(q=True, rd=True)
        db_name=QFileDialog.getSaveFileName(self,"New Database File",project_directory,"*.db;*.sqlite")        

        print(db_name[0])
        if db_name is not None :
            self.database.setDatabaseName(db_name[0])
            self.database.open()
            print(f"{self.database.isOpen()}")
            query = QSqlQuery()
            query.exec_("""DROP TABLE IF EXISTS Meshes""")
            query.exec_("""Create table Meshes (
        id integer PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL,
        mesh_data BLOB NOT NULL,
        mesh_type TEXT CHECK(mesh_type IN('obj','usd','fbx')),
        front_image BLOB,
        side_image BLOB,
        top_image BLOB,
        persp_image BLOB)""")
        self.database.commit()
    
    def get_yes_no(self,message) :
        msgBox = QMessageBox()
        msgBox.setText("Warning")
        msgBox.setInformativeText(message);
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No )
        msgBox.setDefaultButton(QMessageBox.No)
        return msgBox.exec_()
    
    def _save_screenshots(self,path,text):
        """This does all the work"""
        # We evaluate these commands to set the view
        # for the screen shot
        views = [
            "cmds.viewSet(p=True, fit=True)",
            "cmds.viewSet(t=True, fit=True)",
            "cmds.viewSet(s=True, fit=True)",
            "cmds.viewSet(f=True, fit=True)",
        ]
        
        # loop for each view
        for i in range(0, 4):
            # is if it should be exported
        
            # Set the active view
            eval(views[i])
            # grab the view from maya
            view = OpenMayaUI.M3dView.active3dView()
            # need to set focus for the frame command
            panel = cmds.getPanel(visiblePanels=True)
            cmds.setFocus(panel[0])

            #if self.frame_all.isChecked():
            pm.viewFit()
            # now dump to MImage
            image = OpenMaya.MImage()
            view.refresh()
            cmds.viewManip(v=False)
            view.readColorBuffer(image, True)
            # resize to selected size
            image.resize(
                self.image_width.value(), self.image_height.value(), preserveAspectRatio=True
            )
            name = ["Persp", "Top", "Side", "Front"]
            # write
            image.writeToFile(
                f"{path}/{name[i]}.png",
                outputFormat="png",
            )




if __name__ == "__main__":

    # If we have a dialog open already close
    try:
        clutter_base_dialog.close()
        clutter_base_dialog.deleteLater()
    except:
        pass

    clutter_base_dialog = ClutterBaseExporter()
    clutter_base_dialog.show()
