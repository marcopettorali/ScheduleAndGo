# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/main_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(441, 789)
        mainWindow.setAutoFillBackground(False)
        mainWindow.setStyleSheet("#mainWindow{background-color:white}")
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.currentTask = QtWidgets.QScrollArea(self.centralwidget)
        self.currentTask.setMinimumSize(QtCore.QSize(0, 150))
        self.currentTask.setMaximumSize(QtCore.QSize(16777215, 150))
        self.currentTask.setAutoFillBackground(True)
        self.currentTask.setStyleSheet("")
        self.currentTask.setWidgetResizable(True)
        self.currentTask.setObjectName("currentTask")
        self.currentTaskContents = QtWidgets.QWidget()
        self.currentTaskContents.setGeometry(QtCore.QRect(0, 0, 418, 148))
        self.currentTaskContents.setObjectName("currentTaskContents")
        self.currentTaskElem = QtWidgets.QGridLayout(self.currentTaskContents)
        self.currentTaskElem.setObjectName("currentTaskElem")
        self.currentTask.setWidget(self.currentTaskContents)
        self.gridLayout.addWidget(self.currentTask, 7, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 6, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.timeLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeLabel.setObjectName("timeLabel")
        self.horizontalLayout.addWidget(self.timeLabel)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 9, 0, 1, 1)
        self.taskList = QtWidgets.QScrollArea(self.centralwidget)
        self.taskList.setAutoFillBackground(True)
        self.taskList.setWidgetResizable(True)
        self.taskList.setObjectName("taskList")
        self.taskListContents = QtWidgets.QWidget()
        self.taskListContents.setGeometry(QtCore.QRect(0, 0, 423, 299))
        self.taskListContents.setObjectName("taskListContents")
        self.taskListElems = QtWidgets.QVBoxLayout(self.taskListContents)
        self.taskListElems.setObjectName("taskListElems")
        self.taskList.setWidget(self.taskListContents)
        self.gridLayout.addWidget(self.taskList, 11, 0, 1, 2)
        self.currentPositionImage = QtWidgets.QLabel(self.centralwidget)
        self.currentPositionImage.setMinimumSize(QtCore.QSize(200, 200))
        self.currentPositionImage.setText("")
        self.currentPositionImage.setScaledContents(False)
        self.currentPositionImage.setAlignment(QtCore.Qt.AlignCenter)
        self.currentPositionImage.setObjectName("currentPositionImage")
        self.gridLayout.addWidget(self.currentPositionImage, 2, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 441, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.actionClose = QtWidgets.QAction(mainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionAboutScheduleAndGo = QtWidgets.QAction(mainWindow)
        self.actionAboutScheduleAndGo.setObjectName("actionAboutScheduleAndGo")
        self.menuFile.addAction(self.actionClose)
        self.menu.addAction(self.actionAboutScheduleAndGo)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(mainWindow)
        self.actionClose.triggered.connect(mainWindow.close)
        self.actionAboutScheduleAndGo.triggered.connect(mainWindow.on_help)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "ScheduleAndGo"))
        self.label.setText(_translate("mainWindow", "Current task:"))
        self.label_3.setText(_translate("mainWindow", "Current time:"))
        self.timeLabel.setText(_translate("mainWindow", "time"))
        self.label_2.setText(_translate("mainWindow", "Next tasks:"))
        self.menuFile.setTitle(_translate("mainWindow", "File"))
        self.menu.setTitle(_translate("mainWindow", "?"))
        self.actionClose.setText(_translate("mainWindow", "Close"))
        self.actionAboutScheduleAndGo.setText(_translate("mainWindow", "AboutScheduleAndGo"))
