from PyQt5 import QtCore, QtGui, QtWidgets, Qt


class Ui_VentanaAnalizandoResultados(object):
    def setupUi(self, VentanaAnalizandoResultados):
        VentanaAnalizandoResultados.setObjectName("VentanaAnalizandoResultados")
        VentanaAnalizandoResultados.resize(355, 88)
        VentanaAnalizandoResultados.setMinimumSize(QtCore.QSize(355, 88))
        VentanaAnalizandoResultados.setMaximumSize(QtCore.QSize(355, 88))
        VentanaAnalizandoResultados.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(VentanaAnalizandoResultados)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(VentanaAnalizandoResultados)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignTop)
        self.progressAnalisis = QtWidgets.QProgressBar(VentanaAnalizandoResultados)
        self.progressAnalisis.setStyleSheet("")
        self.progressAnalisis.setProperty("value", 24)
        self.progressAnalisis.setAlignment(QtCore.Qt.AlignCenter)
        self.progressAnalisis.setObjectName("progressAnalisis")
        self.verticalLayout.addWidget(self.progressAnalisis)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(VentanaAnalizandoResultados)
        QtCore.QMetaObject.connectSlotsByName(VentanaAnalizandoResultados)

    def retranslateUi(self, VentanaAnalizandoResultados):
        _translate = QtCore.QCoreApplication.translate
        VentanaAnalizandoResultados.setWindowTitle(_translate("VentanaAnalizandoResultados", "Análisis de Resultados"))
        self.label.setText(_translate("VentanaAnalizandoResultados", "<html><head/><body><p>Analizando resultados. </p><p>Dependiendo del número de archivos esto podría tomar un tiempo...</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VentanaAnalizandoResultados = QtWidgets.QWidget()
    ui = Ui_VentanaAnalizandoResultados()
    ui.setupUi(VentanaAnalizandoResultados)
    VentanaAnalizandoResultados.show()
    sys.exit(app.exec_())
