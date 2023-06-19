from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogAbrirArchivosError(object):
    def setupUi(self, DialogGuardarResultadosError):
        DialogGuardarResultadosError.setObjectName("DialogGuardarResultadosError")
        DialogGuardarResultadosError.resize(355, 120)
        DialogGuardarResultadosError.setMinimumSize(QtCore.QSize(355, 120))
        DialogGuardarResultadosError.setMaximumSize(QtCore.QSize(355, 120))
        DialogGuardarResultadosError.setWindowTitle("")
        DialogGuardarResultadosError.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(DialogGuardarResultadosError)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(DialogGuardarResultadosError)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.btnDialogoError = QtWidgets.QDialogButtonBox(DialogGuardarResultadosError)
        self.btnDialogoError.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnDialogoError.setOrientation(QtCore.Qt.Horizontal)
        self.btnDialogoError.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.btnDialogoError.setObjectName("btnDialogoError")
        self.verticalLayout.addWidget(self.btnDialogoError, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(DialogGuardarResultadosError)
        self.btnDialogoError.accepted.connect(DialogGuardarResultadosError.accept) # type: ignore
        self.btnDialogoError.rejected.connect(DialogGuardarResultadosError.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DialogGuardarResultadosError)

    def retranslateUi(self, DialogGuardarResultadosError):
        _translate = QtCore.QCoreApplication.translate
        DialogGuardarResultadosError.setWindowTitle(_translate("DialogGuardarResultadosError", "ERROR"))
        self.label.setText(_translate("DialogGuardarResultadosError", "<html><head/><body><p>ERROR:</p><p>Es posible que uno o más archivos no se abrieran correctamente.</p><p>Compruebe que el directorio o el archivo existen.</p></body></html>"))
