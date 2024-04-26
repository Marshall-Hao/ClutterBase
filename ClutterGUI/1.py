# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ClutterUI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ClutterUI(object):
    def setupUi(self, ClutterUI):
        if not ClutterUI.objectName():
            ClutterUI.setObjectName(u"ClutterUI")
        ClutterUI.resize(745, 584)
        self.gridLayout = QGridLayout(ClutterUI)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(ClutterUI)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.load_db = QPushButton(self.groupBox)
        self.load_db.setObjectName(u"load_db")

        self.horizontalLayout.addWidget(self.load_db)


        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)

        self.db_view = QGroupBox(ClutterUI)
        self.db_view.setObjectName(u"db_view")
        self.db_layout = QVBoxLayout(self.db_view)
        self.db_layout.setObjectName(u"db_layout")

        self.gridLayout.addWidget(self.db_view, 0, 0, 1, 1)


        self.retranslateUi(ClutterUI)

        QMetaObject.connectSlotsByName(ClutterUI)
    # setupUi

    def retranslateUi(self, ClutterUI):
        ClutterUI.setWindowTitle(QCoreApplication.translate("ClutterUI", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("ClutterUI", u"DB Controls", None))
        self.load_db.setText(QCoreApplication.translate("ClutterUI", u"Load DB", None))
        self.db_view.setTitle(QCoreApplication.translate("ClutterUI", u"Database View", None))
    # retranslateUi

