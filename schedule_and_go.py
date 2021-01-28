import sys
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

import UI.main_page as ui
import UI.form as f

from cloud import stt, nlp, tts
from scheduler.scheduler import Scheduler
from scheduler.timeDaemon import TimeDaemon


class TaskForm(QtWidgets.QWidget, f.Ui_Form):
    def __init__(self, parent=None):
        super(TaskForm, self).__init__(parent)
        self.setupUi(self)


class MainApp(QtWidgets.QMainWindow, ui.Ui_mainWindow):
    add_task_signal = QtCore.pyqtSignal(str, str, list, int)
    pop_task_signal = QtCore.pyqtSignal()
    clear_tasks_signal = QtCore.pyqtSignal()
    update_time_signal = QtCore.pyqtSignal(str)
    update_position_signal = QtCore.pyqtSignal()

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
        self.clear_tasks_signal.connect(self.clear_tasks)
        self.update_time_signal.connect(self.update_time)
        self.update_position_signal.connect(self.update_position)

        # initialize cloud components
        self.stt = stt.SpeechToTextManager("google_key.json")
        self.nlp = nlp.NaturalProcessingLanguageGoogleCloud()
        self.tts = tts.TextToSpeechManager()
        th = threading.Thread(target=self.get_task_thread_body, daemon=True)
        th.start()

        # initialize scheduler
        self.time_daemon = TimeDaemon(min_every_sec=1, update_time_signal=self.update_time_signal)
        threading.Thread(target=self.time_daemon.run, args=()).start()
        # need to set current GPS position here
        self.scheduler = Scheduler(current_position="Cecina", time_daemon=self.time_daemon, polling_sec=5,
                                   task_finished_signal=self.pop_task_signal,
                                   update_position_signal=self.update_position_signal)

    def on_help(self):
        print("Lorenzoni Pettorali - (C) 2020")

    def add_task(self, destination, deadline, actions, index=-1):
        frame = QtWidgets.QFrame()
        form = TaskForm(frame)
        form.destination_lbl.setText(destination)
        form.deadline_lbl.setText("Arrivo previsto alle " + deadline)

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

        if self.currentTaskElem.count() == 0:
            self.pop_task()

    def pop_task(self):
        for i in reversed(range(self.currentTaskElem.count())):
            self.currentTaskElem.itemAt(i).widget().setParent(None)
        item = self.taskListElems.itemAt(0)
        if item is not None:
            form = item.widget()
            self.currentTaskElem.addWidget(form)

    def clear_tasks(self):
        for i in reversed(range(self.currentTaskElem.count())):
            self.currentTaskElem.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.taskListElems.count())):
            self.taskListElems.itemAt(i).widget().setParent(None)

    def update_position(self):
        self.currentPositionImage.setPixmap(QtGui.QPixmap("map.png"))

    def get_task_thread_body(self):
        requests = [
            "Vai a Roma a prendere una birra entro le 14 di dopodomani",
            "Vai a Cosenza entro le 23 a ascoltare una band",
            "Vai a Milano entro le 12 di domani a visitare il duomo"
        ]
        index = -1
        while True:
            index += 1
            if index >= len(requests):
                break
            sentence = self.stt.listen(requests[index])
            task = self.nlp.analyze_task(sentence)
            speech = "Ok, vado a " + task['destination'] + " per il seguente motivo: "
            actions = []
            for k in task['action']:
                actions.append(k + " " + task['action'][k])
                speech += k + " " + task['action'][k] + ", "
            speech += "Entro le " + task['deadline']
            speech += ". Vuoi confermare?"
            self.tts.cached_say(speech)

            confirm = self.stt.listen("ok")
            if confirm.strip().lower() in ["ok", "sì", "si", "va bene", "perfetto", "esatto", "giusto", "affermativo",
                                           "confermo", "confermato", "d'accordo", "certo", "certamente"]:
                self.tts.cached_say("Ok, richiesta inviata")
                response = self.scheduler.schedule_new_task(destination=task['destination'],
                                                            deadline=task['deadline_norm'],
                                                            actions=task['action'])
                if response['status'] == "ERR":
                    self.tts.cached_say(
                        "Non è possibile accettare la richiesta, la scadenza è troppo vicina. " +
                        "Provare nuovamente con una scadenza più lontana.")
                elif response['status'] == "OK":
                    self.tts.cached_say("Richiesta accettata")
                    tasks = self.scheduler.get_current_car_tasks()
                    self.clear_tasks_signal.emit()
                    print(len(tasks))
                    for task in tasks:
                        print(task)
                        actions = []
                        for k in task.get_actions():
                            actions.append(k + " " + task.get_actions()[k])
                        self.add_task_signal.emit(task.get_destination(),
                                                  task.get_arrival_time().strftime("%H:%M, %d/%m/%Y"),
                                                  actions, -1)
            else:
                self.tts.cached_say("Richiesta annullata")

    def update_time(self, time):
        self.timeLabel.setText(time)


app = QApplication(sys.argv)

form = MainApp()
form.show()
app.exec_()
