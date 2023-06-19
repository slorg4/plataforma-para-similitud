from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VentanaFiltros(object):
    def setupUi(self, VentanaFiltros):
        VentanaFiltros.setObjectName("VentanaFiltros")
        VentanaFiltros.resize(570, 374)
        VentanaFiltros.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(VentanaFiltros)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(VentanaFiltros)
        self.tabWidget.setStyleSheet("background-color: rgb(54, 54, 54);")
        self.tabWidget.setObjectName("tabWidget")
        self.tabFiltros = QtWidgets.QWidget()
        self.tabFiltros.setStyleSheet("")
        self.tabFiltros.setObjectName("tabFiltros")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tabFiltros)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkboxCarpetas = QtWidgets.QCheckBox(self.tabFiltros)
        self.checkboxCarpetas.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.checkboxCarpetas.setChecked(True)
        self.checkboxCarpetas.setObjectName("checkboxCarpetas")
        self.verticalLayout_3.addWidget(self.checkboxCarpetas)
        self.frameFiltros = QtWidgets.QFrame(self.tabFiltros)
        self.frameFiltros.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameFiltros.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameFiltros.setObjectName("frameFiltros")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frameFiltros)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lblDisponibles = QtWidgets.QLabel(self.frameFiltros)
        self.lblDisponibles.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.lblDisponibles.setObjectName("lblDisponibles")
        self.verticalLayout_6.addWidget(self.lblDisponibles)
        self.listDisponibles = QtWidgets.QListWidget(self.frameFiltros)
        self.listDisponibles.setStyleSheet("background-color: rgb(221, 221, 221);")
        self.listDisponibles.setObjectName("listDisponibles")
        self.verticalLayout_6.addWidget(self.listDisponibles)
        self.btnAgregar = QtWidgets.QPushButton(self.frameFiltros)
        self.btnAgregar.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnAgregar.setObjectName("btnAgregar")
        self.verticalLayout_6.addWidget(self.btnAgregar, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lblFiltradas = QtWidgets.QLabel(self.frameFiltros)
        self.lblFiltradas.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.lblFiltradas.setObjectName("lblFiltradas")
        self.verticalLayout_7.addWidget(self.lblFiltradas)
        self.listFiltradas = QtWidgets.QListWidget(self.frameFiltros)
        self.listFiltradas.setStyleSheet("background-color: rgb(221, 221, 221);")
        self.listFiltradas.setObjectName("listFiltradas")
        self.verticalLayout_7.addWidget(self.listFiltradas)
        self.btnEliminar = QtWidgets.QPushButton(self.frameFiltros)
        self.btnEliminar.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnEliminar.setObjectName("btnEliminar")
        self.verticalLayout_7.addWidget(self.btnEliminar, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addWidget(self.frameFiltros)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tabFiltros, "")
        self.tabSimilitudes = QtWidgets.QWidget()
        self.tabSimilitudes.setObjectName("tabSimilitudes")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tabSimilitudes)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.checkboxSimilitudR = QtWidgets.QCheckBox(self.tabSimilitudes)
        self.checkboxSimilitudR.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.checkboxSimilitudR.setChecked(True)
        self.checkboxSimilitudR.setObjectName("checkboxSimilitudR")
        self.verticalLayout_5.addWidget(self.checkboxSimilitudR)
        self.frameParametros = QtWidgets.QFrame(self.tabSimilitudes)
        self.frameParametros.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameParametros.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameParametros.setObjectName("frameParametros")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frameParametros)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label = QtWidgets.QLabel(self.frameParametros)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.label.setObjectName("label")
        self.verticalLayout_9.addWidget(self.label)
        self.comboBoxMedida = QtWidgets.QComboBox(self.frameParametros)
        self.comboBoxMedida.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(54, 54, 54);")
        self.comboBoxMedida.setObjectName("comboBoxMedida")
        self.comboBoxMedida.addItem("")
        self.comboBoxMedida.addItem("")
        self.comboBoxMedida.addItem("")
        self.comboBoxMedida.addItem("")
        self.comboBoxMedida.addItem("")
        self.comboBoxMedida.addItem("")
        self.verticalLayout_9.addWidget(self.comboBoxMedida)
        self.lblDescMedida = QtWidgets.QLabel(self.frameParametros)
        self.lblDescMedida.setStyleSheet("color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(255, 255, 255);\n"
"")
        self.lblDescMedida.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblDescMedida.setObjectName("lblDescMedida")
        self.verticalLayout_9.addWidget(self.lblDescMedida)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem)
        self.verticalLayout_9.setStretch(0, 1)
        self.verticalLayout_9.setStretch(1, 1)
        self.verticalLayout_9.setStretch(2, 8)
        self.verticalLayout_9.setStretch(3, 5)
        self.horizontalLayout.addLayout(self.verticalLayout_9)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_2 = QtWidgets.QLabel(self.frameParametros)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_10.addWidget(self.label_2)
        self.comboBoxTipo = QtWidgets.QComboBox(self.frameParametros)
        self.comboBoxTipo.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(54, 54, 54);")
        self.comboBoxTipo.setObjectName("comboBoxTipo")
        self.comboBoxTipo.addItem("")
        self.comboBoxTipo.addItem("")
        self.comboBoxTipo.addItem("")
        self.comboBoxTipo.addItem("")
        self.comboBoxTipo.addItem("")
        self.verticalLayout_10.addWidget(self.comboBoxTipo)
        self.lblDescTipo = QtWidgets.QLabel(self.frameParametros)
        self.lblDescTipo.setStyleSheet("color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(255, 255, 255);")
        self.lblDescTipo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblDescTipo.setObjectName("lblDescTipo")
        self.verticalLayout_10.addWidget(self.lblDescTipo)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem1)
        self.verticalLayout_10.setStretch(0, 1)
        self.verticalLayout_10.setStretch(1, 1)
        self.verticalLayout_10.setStretch(2, 8)
        self.verticalLayout_10.setStretch(3, 5)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.horizontalLayout_5.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addWidget(self.frameParametros)
        self.verticalLayout_8.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.tabSimilitudes, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.btnAceptar = QtWidgets.QPushButton(VentanaFiltros)
        self.btnAceptar.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnAceptar.setObjectName("btnAceptar")
        self.horizontalLayout_2.addWidget(self.btnAceptar)
        self.btnCancelar = QtWidgets.QPushButton(VentanaFiltros)
        self.btnCancelar.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 110, 110);")
        self.btnCancelar.setObjectName("btnCancelar")
        self.horizontalLayout_2.addWidget(self.btnCancelar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(VentanaFiltros)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(VentanaFiltros)


    def retranslateUi(self, VentanaFiltros):
        _translate = QtCore.QCoreApplication.translate
        VentanaFiltros.setWindowTitle(_translate("VentanaFiltros", "Configuración de Filtros"))
        self.checkboxCarpetas.setText(_translate("VentanaFiltros", "Todas las Carpetas"))
        self.lblDisponibles.setText(_translate("VentanaFiltros", "Carpetas disponibles"))
        self.btnAgregar.setText(_translate("VentanaFiltros", "Agregar"))
        self.lblFiltradas.setText(_translate("VentanaFiltros", "Carpetas filtradas"))
        self.btnEliminar.setText(_translate("VentanaFiltros", "Eliminar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFiltros), _translate("VentanaFiltros", "Carpetas"))
        self.checkboxSimilitudR.setText(_translate("VentanaFiltros", "Configuración Recomendada"))
        self.label.setText(_translate("VentanaFiltros", "Medida de Similitud"))
        self.comboBoxMedida.setItemText(0, _translate("VentanaFiltros", "Similitud de Cosenos"))
        self.comboBoxMedida.setItemText(1, _translate("VentanaFiltros", "Coeficiente de Jaccard"))
        self.comboBoxMedida.setItemText(2, _translate("VentanaFiltros", "Coeficiente de Dice"))
        self.comboBoxMedida.setItemText(3, _translate("VentanaFiltros", "Distancia Euclidiana"))
        self.comboBoxMedida.setItemText(4, _translate("VentanaFiltros", "Distancia Manhattan"))
        self.lblDescMedida.setText(_translate("VentanaFiltros", "Descripción:"))
        self.label_2.setText(_translate("VentanaFiltros", "Tipo de Modelo"))
        self.comboBoxTipo.setItemText(0, _translate("VentanaFiltros", "Bolsa de palabras"))
        self.comboBoxTipo.setItemText(1, _translate("VentanaFiltros", "Sentence-Transformers 1"))
        self.comboBoxTipo.setItemText(2, _translate("VentanaFiltros", "Sentence-Transformers 2"))
        self.comboBoxTipo.setItemText(3, _translate("VentanaFiltros", "Sentence-Transformers 3"))
        self.comboBoxTipo.setItemText(4, _translate("VentanaFiltros", "Doc2Vec"))
        self.lblDescTipo.setText(_translate("VentanaFiltros", "Descripción:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSimilitudes), _translate("VentanaFiltros", "Medida de Similitud"))
        self.btnAceptar.setText(_translate("VentanaFiltros", "Aceptar"))
        self.btnCancelar.setText(_translate("VentanaFiltros", "Cancelar"))

