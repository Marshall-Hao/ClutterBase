# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clutter.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QPushButton,
    QSizePolicy, QWidget)

class Ui_Clutter(object):
    def setupUi(self, Clutter):
        if not Clutter.objectName():
            Clutter.setObjectName(u"Clutter")
        Clutter.resize(698, 500)
        self.groupBox = QGroupBox(Clutter)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 250, 631, 231))
        self.load_db = QPushButton(self.groupBox)
        self.load_db.setObjectName(u"load_db")
        self.load_db.setGeometry(QRect(510, 102, 101, 31))
        self.groupBox_2 = QGroupBox(Clutter)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(30, 10, 631, 241))

        self.retranslateUi(Clutter)

        QMetaObject.connectSlotsByName(Clutter)
    # setupUi

    def retranslateUi(self, Clutter):
        Clutter.setWindowTitle(QCoreApplication.translate("Clutter", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Clutter", u"DB Controls", None))
        self.load_db.setText(QCoreApplication.translate("Clutter", u"Load DB", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Clutter", u"Database View", None))
    # retranslateUi

