# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 150)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.deadline_lbl = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.deadline_lbl.setFont(font)
        self.deadline_lbl.setObjectName("deadline_lbl")
        self.gridLayout.addWidget(self.deadline_lbl, 1, 1, 1, 1)
        self.action_list = QtWidgets.QVBoxLayout()
        self.action_list.setObjectName("action_list")
        self.gridLayout.addLayout(self.action_list, 2, 1, 1, 1)
        self.img_lbl = QtWidgets.QLabel(Form)
        self.img_lbl.setMaximumSize(QtCore.QSize(150, 150))
        self.img_lbl.setScaledContents(False)
        self.img_lbl.setObjectName("img_lbl")
        self.gridLayout.addWidget(self.img_lbl, 0, 0, 3, 1)
        self.destination_lbl = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.destination_lbl.setFont(font)
        self.destination_lbl.setObjectName("destination_lbl")
        self.gridLayout.addWidget(self.destination_lbl, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.deadline_lbl.setText(_translate("Form", "Deadline"))
        self.img_lbl.setText(_translate("Form", "MAP img"))
        self.destination_lbl.setText(_translate("Form", "DESTINATION"))
