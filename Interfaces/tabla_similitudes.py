from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VentanaSimilitudes(object):
    def setupUi(self, VentanaSimilitudes):
        VentanaSimilitudes.setObjectName("VentanaSimilitudes")
        VentanaSimilitudes.resize(760, 430)
        VentanaSimilitudes.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(VentanaSimilitudes)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(VentanaSimilitudes)
        self.tabWidget.setStyleSheet("background-color: rgb(57, 57, 57);\n"
"")
        self.tabWidget.setObjectName("tabWidget")
        self.tabResultados = QtWidgets.QWidget()
        self.tabResultados.setObjectName("tabResultados")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tabResultados)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableResultados = QtWidgets.QTableView(self.tabResultados)
        self.tableResultados.setObjectName("tableResultados")
        self.verticalLayout_3.addWidget(self.tableResultados)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAbrir1 = QtWidgets.QPushButton(self.tabResultados)
        self.btnAbrir1.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnAbrir1.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnAbrir1.setObjectName("btnAbrir1")
        self.horizontalLayout.addWidget(self.btnAbrir1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.btnGuardarResultados = QtWidgets.QPushButton(self.tabResultados)
        self.btnGuardarResultados.setMinimumSize(QtCore.QSize(115, 0))
        self.btnGuardarResultados.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnGuardarResultados.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnGuardarResultados.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnGuardarResultados.setObjectName("btnGuardarResultados")
        self.verticalLayout_3.addWidget(self.btnGuardarResultados, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tabResultados, "")
        self.tabAltas = QtWidgets.QWidget()
        self.tabAltas.setObjectName("tabAltas")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tabAltas)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tableAltas = QtWidgets.QTableView(self.tabAltas)
        self.tableAltas.setObjectName("tableAltas")
        self.verticalLayout_5.addWidget(self.tableAltas)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnAbrir2 = QtWidgets.QPushButton(self.tabAltas)
        self.btnAbrir2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnAbrir2.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnAbrir2.setObjectName("btnAbrir2")
        self.horizontalLayout_2.addWidget(self.btnAbrir2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.tabAltas, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(VentanaSimilitudes)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(VentanaSimilitudes)

    def retranslateUi(self, VentanaSimilitudes):
        _translate = QtCore.QCoreApplication.translate
        VentanaSimilitudes.setWindowTitle(_translate("VentanaSimilitudes", "Tabla de Similitudes"))
        self.btnAbrir1.setText(_translate("VentanaSimilitudes", "Abrir Archivos"))
        self.btnGuardarResultados.setText(_translate("VentanaSimilitudes", "Guardar Resultados"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabResultados), _translate("VentanaSimilitudes", "Resultados"))
        self.btnAbrir2.setText(_translate("VentanaSimilitudes", "Abrir Archivos"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAltas), _translate("VentanaSimilitudes", "Coincidencias Altas"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VentanaSimilitudes = QtWidgets.QWidget()
    ui = Ui_VentanaSimilitudes()
    ui.setupUi(VentanaSimilitudes)
    VentanaSimilitudes.show()
    sys.exit(app.exec_())
