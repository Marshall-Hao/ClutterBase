# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cl.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1064, 811)
        self.db_view = QGroupBox(Form)
        self.db_view.setObjectName(u"db_view")
        self.db_view.setGeometry(QRect(40, 10, 951, 411))
        self.db_layout = QVBoxLayout(self.db_view)
        self.db_layout.setObjectName(u"db_layout")
        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(40, 420, 951, 65))
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(838, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.load_db = QPushButton(self.groupBox_2)
        self.load_db.setObjectName(u"load_db")

        self.horizontalLayout.addWidget(self.load_db)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.db_view.setTitle(QCoreApplication.translate("Form", u"Database View", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"DB Controls", None))
        self.load_db.setText(QCoreApplication.translate("Form", u"Load DB", None))
    # retranslateUi

