from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VentanaGuardarResultados(object):
    def setupUi(self, VentanaGuardarResultados):
        VentanaGuardarResultados.setObjectName("VentanaGuardarResultados")
        VentanaGuardarResultados.resize(315, 100)
        VentanaGuardarResultados.setMinimumSize(QtCore.QSize(315, 100))
        VentanaGuardarResultados.setMaximumSize(QtCore.QSize(16777215, 100))
        VentanaGuardarResultados.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(VentanaGuardarResultados)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(VentanaGuardarResultados)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignTop)
        self.txtboxNombreArchivo = QtWidgets.QLineEdit(VentanaGuardarResultados)
        self.txtboxNombreArchivo.setMinimumSize(QtCore.QSize(0, 0))
        self.txtboxNombreArchivo.setAutoFillBackground(False)
        self.txtboxNombreArchivo.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.txtboxNombreArchivo.setObjectName("txtboxNombreArchivo")
        self.verticalLayout.addWidget(self.txtboxNombreArchivo, 0, QtCore.Qt.AlignTop)
        self.btnGuardarResultados = QtWidgets.QPushButton(VentanaGuardarResultados)
        self.btnGuardarResultados.setMinimumSize(QtCore.QSize(100, 0))
        self.btnGuardarResultados.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnGuardarResultados.setObjectName("btnGuardarResultados")
        self.verticalLayout.addWidget(self.btnGuardarResultados, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(VentanaGuardarResultados)
        QtCore.QMetaObject.connectSlotsByName(VentanaGuardarResultados)


    def retranslateUi(self, VentanaGuardarResultados):
        _translate = QtCore.QCoreApplication.translate
        VentanaGuardarResultados.setWindowTitle(_translate("VentanaGuardarResultados", "Guardar los Resultados"))
        self.label.setText(_translate("VentanaGuardarResultados", "Asigna un nombre al archivo:"))
        self.btnGuardarResultados.setText(_translate("VentanaGuardarResultados", "Aceptar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VentanaGuardarResultados = QtWidgets.QWidget()
    ui = Ui_VentanaGuardarResultados()
    ui.setupUi(VentanaGuardarResultados)
    VentanaGuardarResultados.show()
    sys.exit(app.exec_())
