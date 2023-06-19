from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogGuardarResultados(object):
    def setupUi(self, DialogGuardarResultados):
        DialogGuardarResultados.setObjectName("DialogGuardarResultados")
        DialogGuardarResultados.resize(265, 100)
        DialogGuardarResultados.setMinimumSize(QtCore.QSize(265, 100))
        DialogGuardarResultados.setMaximumSize(QtCore.QSize(265, 100))
        DialogGuardarResultados.setWindowTitle("")
        DialogGuardarResultados.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(DialogGuardarResultados)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(DialogGuardarResultados)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.btnDialogo = QtWidgets.QDialogButtonBox(DialogGuardarResultados)
        self.btnDialogo.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnDialogo.setOrientation(QtCore.Qt.Horizontal)
        self.btnDialogo.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.btnDialogo.setObjectName("btnDialogo")
        self.verticalLayout.addWidget(self.btnDialogo, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(DialogGuardarResultados)
        self.btnDialogo.accepted.connect(DialogGuardarResultados.accept) # type: ignore
        self.btnDialogo.rejected.connect(DialogGuardarResultados.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DialogGuardarResultados)

    def retranslateUi(self, DialogGuardarResultados):
        _translate = QtCore.QCoreApplication.translate
        DialogGuardarResultados.setWindowTitle(_translate("DialogGuardarResultados", "Resultados Guardados"))
        self.label.setText(_translate("DialogGuardarResultados", "<html><head/><body><p>Los Resultados se guardaron correctamente</p></body></html>"))
