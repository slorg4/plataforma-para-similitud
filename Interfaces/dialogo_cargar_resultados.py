from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogCargarResultados(object):
    def setupUi(self, DialogCargarResultados):
        DialogCargarResultados.setObjectName("DialogCargarResultados")
        DialogCargarResultados.resize(274, 115)
        DialogCargarResultados.setMinimumSize(QtCore.QSize(274, 115))
        DialogCargarResultados.setMaximumSize(QtCore.QSize(274, 115))
        DialogCargarResultados.setWindowTitle("")
        DialogCargarResultados.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(DialogCargarResultados)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(DialogCargarResultados)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.label.setLineWidth(1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setIndent(-1)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(45, -1, 45, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAceptar = QtWidgets.QPushButton(DialogCargarResultados)
        self.btnAceptar.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnAceptar.setObjectName("btnAceptar")
        self.horizontalLayout.addWidget(self.btnAceptar)
        self.btnCancelar = QtWidgets.QPushButton(DialogCargarResultados)
        self.btnCancelar.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnCancelar.setObjectName("btnCancelar")
        self.horizontalLayout.addWidget(self.btnCancelar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(DialogCargarResultados)
        QtCore.QMetaObject.connectSlotsByName(DialogCargarResultados)

    def retranslateUi(self, DialogCargarResultados):
        _translate = QtCore.QCoreApplication.translate
        DialogCargarResultados.setWindowTitle(_translate("DialogCargarResultados", "Filtros Modificados"))
        self.label.setText(_translate("DialogCargarResultados", "<html><head/><body><p>Se realizaron cambios en los filtros.</p><p>Los resultados del archivo cargado NO se mostrarán.</p><p>¿Desea guardar los cambios?</p></body></html>"))
        self.btnAceptar.setText(_translate("DialogCargarResultados", "Aceptar"))
        self.btnCancelar.setText(_translate("DialogCargarResultados", "Cancelar"))

