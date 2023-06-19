from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VentanaPrincipal(object):
    def setupUi(self, VentanaPrincipal):
        VentanaPrincipal.setObjectName("VentanaPrincipal")
        VentanaPrincipal.resize(482, 487)
        VentanaPrincipal.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.centralwidget = QtWidgets.QWidget(VentanaPrincipal)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.pageMenu = QtWidgets.QWidget()
        self.pageMenu.setObjectName("pageMenu")
        self.stackedWidget.addWidget(self.pageMenu)
        self.pageDocs = QtWidgets.QWidget()
        self.pageDocs.setObjectName("pageDocs")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.pageDocs)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableDocs = QtWidgets.QTableView(self.pageDocs)
        self.tableDocs.setObjectName("tableDocs")
        self.verticalLayout_3.addWidget(self.tableDocs)
        self.btnAnalizar = QtWidgets.QPushButton(self.pageDocs)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAnalizar.sizePolicy().hasHeightForWidth())
        self.btnAnalizar.setSizePolicy(sizePolicy)
        self.btnAnalizar.setMaximumSize(QtCore.QSize(125, 16777215))
        self.btnAnalizar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnAnalizar.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnAnalizar.setObjectName("btnAnalizar")
        self.verticalLayout_3.addWidget(self.btnAnalizar, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.stackedWidget.addWidget(self.pageDocs)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        VentanaPrincipal.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(VentanaPrincipal)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 482, 21))
        self.menubar.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(54, 54, 54);")
        self.menubar.setObjectName("menubar")
        self.menuDirectorio = QtWidgets.QMenu(self.menubar)
        self.menuDirectorio.setObjectName("menuDirectorio")
        self.menuOpciones = QtWidgets.QMenu(self.menubar)
        self.menuOpciones.setObjectName("menuOpciones")
        VentanaPrincipal.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(VentanaPrincipal)
        self.statusbar.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(54, 54, 54);")
        self.statusbar.setObjectName("statusbar")
        VentanaPrincipal.setStatusBar(self.statusbar)
        self.actionCargar = QtWidgets.QAction(VentanaPrincipal)
        self.actionCargar.setObjectName("actionCargar")
        self.actionFiltrar = QtWidgets.QAction(VentanaPrincipal)
        self.actionFiltrar.setObjectName("actionFiltrar")
        self.actionCargarResultadosPrevios = QtWidgets.QAction(VentanaPrincipal)
        self.actionCargarResultadosPrevios.setObjectName("actionCargarResultadosPrevios")
        self.menuDirectorio.addAction(self.actionCargar)
        self.menuDirectorio.addAction(self.actionCargarResultadosPrevios)
        self.menuOpciones.addAction(self.actionFiltrar)
        self.menubar.addAction(self.menuDirectorio.menuAction())
        self.menubar.addAction(self.menuOpciones.menuAction())

        self.retranslateUi(VentanaPrincipal)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(VentanaPrincipal)

    def retranslateUi(self, VentanaPrincipal):
        _translate = QtCore.QCoreApplication.translate
        VentanaPrincipal.setWindowTitle(_translate("VentanaPrincipal", "Menú Principal"))
        self.btnAnalizar.setText(_translate("VentanaPrincipal", "Analizar"))
        self.menuDirectorio.setTitle(_translate("VentanaPrincipal", "Directorio"))
        self.menuOpciones.setTitle(_translate("VentanaPrincipal", "Opciones"))
        self.actionCargar.setText(_translate("VentanaPrincipal", "Cargar Directorio..."))
        self.actionCargar.setStatusTip(_translate("VentanaPrincipal", "Selecciona un Directorio para Analizar"))
        self.actionCargar.setShortcut(_translate("VentanaPrincipal", "Ctrl+O"))
        self.actionFiltrar.setText(_translate("VentanaPrincipal", "Administrar Filtros..."))
        self.actionFiltrar.setStatusTip(_translate("VentanaPrincipal", "Configura los filtros de las Carpetas y la Medida de  Similitud"))
        self.actionFiltrar.setShortcut(_translate("VentanaPrincipal", "Ctrl+P"))
        self.actionCargarResultadosPrevios.setText(_translate("VentanaPrincipal", "Cargar Resultados Previos..."))
        self.actionCargarResultadosPrevios.setStatusTip(_translate("VentanaPrincipal", "Carga Resultados guardados previamente en un archivo"))
        self.actionCargarResultadosPrevios.setShortcut(_translate("VentanaPrincipal", "Ctrl+I"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VentanaPrincipal = QtWidgets.QMainWindow()
    ui = Ui_VentanaPrincipal()
    ui.setupUi(VentanaPrincipal)
    VentanaPrincipal.show()
    sys.exit(app.exec_())
