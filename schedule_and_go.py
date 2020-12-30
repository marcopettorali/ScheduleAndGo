import sys
import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

import UI.main_page as ui
import UI.form as f
import nlp_google
import stt
import tts


class TaskForm(QtWidgets.QWidget, f.Ui_Form):
    def __init__(self, parent=None):
        super(TaskForm, self).__init__(parent)
        self.setupUi(self)


class MainApp(QtWidgets.QMainWindow, ui.Ui_mainWindow):
    add_task_signal = QtCore.pyqtSignal(str, str, list, int)
    pop_task_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)

        # set up GUI
        self.setupUi(self)
        self.taskListElems.setAlignment(QtCore.Qt.AlignTop)
        self.currentTaskElem.setAlignment(QtCore.Qt.AlignTop)
        self.currentTask.setStyleSheet("QScrollArea {background-color:transparent;}");
        self.currentTaskContents.setStyleSheet("background-color:transparent;");
        self.taskList.setStyleSheet("QScrollArea {background-color:transparent;}");
        self.taskListContents.setStyleSheet("background-color:transparent;");
        self.setStyleSheet("#mainWindow{background-color:white;}")

        # connect signals
        self.add_task_signal.connect(self.add_task)
        self.pop_task_signal.connect(self.pop_task)

        # initialize other components
        self.s = stt.SpeechToTextManager("google_key.json")
        self.n = nlp_google.NaturalProcessingLanguageGoogleCloud()
        self.t = tts.TextToSpeechManager()
        th = threading.Thread(target=self.get_task_thread_body, daemon=True)
        th.start()

    def on_help(self):
        print("Lorenzoni Pettorali - (C) 2020")

    def add_task(self, destination, deadline, actions, index=-1):
        frame = QtWidgets.QFrame()
        form = TaskForm(frame)
        form.destination_lbl.setText(destination)
        form.deadline_lbl.setText("Entro le " + deadline)

        for a in actions:
            label = QtWidgets.QLabel(form)
            label.setText("• " + a)
            form.action_list.addWidget(label)

        form.setAttribute(QtCore.Qt.WA_StyledBackground)
        form.setStyleSheet(
            "QWidget#Form{background-color:#e1dfe1;border-style: outset; border-width: 0px; border-radius: 10px; border-color: grey;}")
        form.img_lbl.setPixmap(QtGui.QPixmap("img/location.png").scaled(100, 100, QtCore.Qt.KeepAspectRatio,
                                                                        QtCore.Qt.SmoothTransformation))
        if index < 0:
            self.taskListElems.addWidget(form)
        else:
            self.taskListElems.insertWidget(index, form)

        if self.currentTaskElem.isEmpty():
            self.pop_task()

    def pop_task(self):
        for i in reversed(range(self.currentTaskElem.count())):
            self.currentTaskElem.itemAt(i).widget().setParent(None)
        item = self.taskListElems.itemAt(0)
        if item is not None:
            form = item.widget()
            self.currentTaskElem.addWidget(form)

    def get_task_thread_body(self):
        while True:
            sentence = self.s.listen()
            task = self.n.analyze_task(sentence)
            speech = "Ok, vado a " + task['destination'] + " per il seguente motivo: "
            actions = []
            for k in task['action']:
                actions.append(k + " " + task['action'][k])
                speech += k + " " + task['action'][k] + ", "
            speech += "Entro le " + task['deadline']
            speech += ". Per confermare dire \"OK\""
            self.t.cached_say(speech)

            confirm = self.s.listen()
            if confirm.strip().lower() == "ok":
                # send request to task management system
                self.add_task_signal.emit(task['destination'], task['deadline'], actions, -1)
                self.t.cached_say("Ok, richiesta inviata")
                # get response from task management system
            else:
                self.t.cached_say("Richiesta annullata")


app = QApplication(sys.argv)

form = MainApp()
form.show()
app.exec_()
