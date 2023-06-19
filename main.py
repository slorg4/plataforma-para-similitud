import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import QSortFilterProxyModel, QAbstractTableModel, Qt, QObject, pyqtSignal, QThread, QSettings

import os
import json
import re
import numpy as np

from Interfaces.menu_principal import Ui_VentanaPrincipal
from Interfaces.ventana_filtros import Ui_VentanaFiltros
from Interfaces.tabla_similitudes import Ui_VentanaSimilitudes
from Interfaces.dialogo_abrir_archivos_error import Ui_DialogAbrirArchivosError
from Interfaces.ventana_guardar_resultados import Ui_VentanaGuardarResultados
from Interfaces.dialogo_guardar_resultados import Ui_DialogGuardarResultados
from Interfaces.dialogo_guardar_resultados_error import Ui_DialogGuardarResultadosError
from Interfaces.dialogo_cargar_resultados import Ui_DialogCargarResultados
from Interfaces.ventana_analizando_resultados import Ui_VentanaAnalizandoResultados

from Controladores.doc_similarity import MainInfo
from Controladores.documents_functions import get_docs, format_data, get_filters_list, get_filt_docs, get_texts, start_files
from Controladores.simFuncs_v4 import similarities
from Controladores.format_functions import format_sim_results_v2, format_top_results, format_paths


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.getSettingValues()
        self.menu = Ui_VentanaPrincipal()
        self.menu.setupUi(self)

        #Creacion de la Ventana de filtros del directorio
        self.filters_window = Ui_VentanaFiltros()
        self.newWindow_filters = QtWidgets.QWidget()
        self.filters_window.setupUi(self.newWindow_filters)

        #Creacion de la Ventana de similitudes analizadas
        self.similarity_window = Ui_VentanaSimilitudes()
        self.newWindow_similarity = QtWidgets.QWidget()
        self.similarity_window.setupUi(self.newWindow_similarity)

        #Cracion del dialogo en caso de error al abrir archivos
        self.open_files_dialog_error = Ui_DialogAbrirArchivosError()
        self.newDialog_open_files = QtWidgets.QDialog()
        self.open_files_dialog_error.setupUi(self.newDialog_open_files)

        #Creacion de la Ventana para guardar los resultados
        self.save_results_window = Ui_VentanaGuardarResultados()
        self.newWindow_results = QtWidgets.QWidget()
        self.save_results_window.setupUi(self.newWindow_results)

        #Creacion de los dialogos para la Ventana para guardar los resultados
        self.save_dialog = Ui_DialogGuardarResultados()
        self.newDialog_save = QtWidgets.QDialog()
        self.save_dialog.setupUi(self.newDialog_save)

        self.save_dialog_error = Ui_DialogGuardarResultadosError()
        self.newDialog_save_error = QtWidgets.QDialog()
        self.save_dialog_error.setupUi(self.newDialog_save_error)

        # Creacion del dialogo en caso de que los filtros sean modificados
        # Se encarga de indicar que los resultados cargados serán afectados
        self.load_dialog = Ui_DialogCargarResultados()
        self.newDialog_load = QtWidgets.QDialog()
        self.load_dialog.setupUi(self.newDialog_load)

        # Creacion de la ventana que analiza los resultados
        # Se encarga de mostrar una barra de espera mientras genera los resultados
        self.analizing_window = Ui_VentanaAnalizandoResultados()
        self.newWindow_analizing = QtWidgets.QWidget()
        self.analizing_window.setupUi(self.newWindow_analizing)

        # Variables principales necesarias para el contenido de las ventanas y tablas
        self.main_info = MainInfo()
        self.top_info = ([], [], [])
        self.main_directories = []
        self.filters = []
        self.load_variables_settings()
        self.loaded_results_state = False
        self.similarity_function = similarities()

        ## MUESTRA EL MENÚ PRINCIPAL
        self.menu.menuOpciones.setEnabled(False)
        self.load_window_settings()
        self.show()

        #### ASIGNACION DE FUNCIONES DE LA VENTANA DEL MENU PRINCIPAL ####
        #Asigna la funcion para seleccionar Directorio
        self.menu.actionCargar.triggered.connect(self.browse_directory)
        #Asigna la funciona para cargar un archivo de Resultados
        self.menu.actionCargarResultadosPrevios.triggered.connect(self.load_results)
        #Asigna la funcion para configurar Filtros
        self.menu.actionFiltrar.triggered.connect(self.open_filters)
        #Asigna la funcion para analizar las similitudes
        self.menu.btnAnalizar.clicked.connect(self.get_similarity)

        #### ASIGNACION DE FUNCIONES DE LA VENTANA DE FILTROS #####
        #Asigna la funcion para agregar el filtro
        self.filters_window.btnAgregar.clicked.connect(self.add_filter)
        #Asigna la funcion para eliminar el filtro
        self.filters_window.btnEliminar.clicked.connect(self.delete_filter)
        #Asigna la funciona para el boton de Aceptar en los filtros
        self.filters_window.btnAceptar.clicked.connect(self.save_filters)
        #Asigna la funcion para el boton de Cancelar en los filtros
        self.filters_window.btnCancelar.clicked.connect(self.newWindow_filters.hide)
        #Asigna la medida de similitud que ejecutará al analizar los documentos
        self.filters_window.comboBoxMedida.currentIndexChanged.connect(self.update_similarity_description)
        #Asigna el sub-tipo de similitud que ejecutará al analizar los documentos
        self.filters_window.comboBoxTipo.currentIndexChanged.connect(self.update_type_combobox)

        #### ASIGNACION DE FUNCIONES DE LA VENTANA DE LAS TABLAS DE SIMILITUDES ####
        #Asigna la funcion para abrir los archivos generales
        self.similarity_window.btnAbrir1.clicked.connect(self.open_files)
        #Asigna la funcion para abrir los archivos con similitudes altas
        self.similarity_window.btnAbrir2.clicked.connect(self.open_top_files)
        #Asigna la funcion para guardar los resultados obtenidos
        self.similarity_window.btnGuardarResultados.clicked.connect(self.assign_filename)

        #### ASIGNACION DE FUNCIONES DE LA VENTANA PARA GUARDAR RESULTADOS ####
        #Asigna la funcion para el boton de Aceptar para el nombre ingresado
        self.save_results_window.btnGuardarResultados.clicked.connect(self.save_similarity_results)

        #### ASIGNACION DE FUNCIONES DE LOS BOTONES DEL DIALOGO CARGAR REESULTADOS ####
        #Sustituye las opciones de los resultados cargados por las nuevas opciones
        self.load_dialog.btnAceptar.clicked.connect(self.change_loaded_results)
        #Mantiene los resultados cargados
        self.load_dialog.btnCancelar.clicked.connect(self.newDialog_load.close)

    ######################FUNCIONES PARA GUARDAR LA CONFIGURACIÓN###################################
    #Carga a las configuraciones hechas la ultima vez que se usó la plataforma
    def getSettingValues(self):
        self.setting_window = QSettings("Sim App", "Window Size")
        self.setting_variables = QSettings("Sim App", "Variables")

    #Guarda las últimas configuraciones al cerrar la plataforma
    #Solo aplica si no se cargaron resultados guardados
    def closeEvent(self, event):
        if self.loaded_results_state is False:
            self.save_settings()

    #Función hecha para ejecutar las tareas que guardan las configuraciones de la plataforma
    def save_settings(self):
        # Guarda las configuraciones de las ventanas
        self.setting_window.setValue("menu_height", self.rect().height())
        self.setting_window.setValue("menu_width", self.rect().width())
        self.setting_window.setValue("similarity_height", self.newWindow_similarity.rect().height())
        self.setting_window.setValue("similarity_width", self.newWindow_similarity.rect().width())

        # Guarda las configuraciones de las variables principales
        self.setting_variables.setValue("current_similarity_function", self.current_similarity_function)
        self.setting_variables.setValue("current_similarity_type", self.current_similarity_type)
        self.setting_variables.setValue("folder_checkbox_state", self.folder_checkbox_state)
        self.setting_variables.setValue("measure_checkbox_state", self.measure_checkbox_state)

    #Carga las configuraciones de las variables principales utilizadas en las interfaces y despliegue de resultados
    def load_variables_settings(self):
        sim_func = self.setting_variables.value("current_similarity_function")
        sim_type = self.setting_variables.value("current_similarity_type")
        folder_check = self.setting_variables.value("folder_checkbox_state")
        measure_check = self.setting_variables.value("measure_checkbox_state")
        if folder_check == "true":
            folder_check = True
        else:
            folder_check = False
        if measure_check == "true":
            measure_check = True
        else:
            measure_check = False

        if sim_func == None and sim_type == None and folder_check == None and measure_check == None:
            self.current_similarity_function = "Similitud de Cosenos"
            self.current_similarity_type = "Bolsa de palabras"
            self.folder_checkbox_state = True
            self.measure_checkbox_state = True
            return

        self.current_similarity_function = sim_func
        self.current_similarity_type = sim_type
        self.folder_checkbox_state = folder_check
        self.measure_checkbox_state = measure_check

    #Carga las configuraciones de los tamaños de las interfaces
    def load_window_settings(self):
        menu_height = self.setting_window.value("menu_height")
        menu_width = self.setting_window.value("menu_width")
        sim_height = self.setting_window.value("similarity_height")
        sim_width = self.setting_window.value("similarity_width")

        if menu_height == None and menu_width == None and sim_height == None and sim_width == None:
            return
        self.resize(menu_width, menu_height)
        self.newWindow_similarity.resize(sim_width, sim_height)

    ######################FUNCIONES DE LA VENTANA DEL MENU PRINCIPAL###################################
    # Abre el explorador de archivos y obtiene el directorio seleccionado
    def browse_directory(self):
        self.main_info.set_directory(QtWidgets.QFileDialog.getExistingDirectory())
        # Comprueba si está cargado un archivo de resultados
        if self.loaded_results_state is True:
            self.load_variables_settings()
            self.loaded_results_state = False
        if self.main_info.get_directory() != "":
            self.show_docs_table()

    # Muestra la tabla de los documentos del directorio
    def show_docs_table(self):
        if self.loaded_results_state is False:
            self.main_info = get_docs(self.main_info)
            self.main_directories = self.main_info.dir_files

        data = format_data(self.main_info.get_files())

        self.model = TableModel_Menu(data)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)
        self.proxy_model.setSourceModel(self.model)

        self.menu.tableDocs.clearSpans()
        self.menu.tableDocs.setModel(self.proxy_model)
        self.menu.tableDocs.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.menu.tableDocs.resizeColumnToContents(1)

        self.menu.stackedWidget.setCurrentWidget(self.menu.pageDocs)
        self.menu.menuOpciones.setEnabled(True)

    #Despliega las tablas de resultados, realizando todos los procesos de analisis necesarios
    #En caso de que haya resultados cargados, no necesita realizar los procesos de analis
    def get_similarity(self):
        if self.loaded_results_state is True:
            self.build_table_results()
            self.build_top_table()

            self.newWindow_similarity.show()
            return

        self.show_analizer()

    #Construye la tabla de resultados generales en base a los resultados obtenidos
    def build_table_results(self):
        data = format_sim_results_v2(len(self.main_info.dir_files), self.main_info.sim_results)

        self.model = TableModel_Similarities(data)
        self.model.rows = self.main_info.get_files()
        self.model.columns = self.main_info.get_files()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)
        self.proxy_model.setSourceModel(self.model)

        self.similarity_window.tableResultados.setModel(self.proxy_model)
        self.similarity_window.tableResultados.resizeColumnsToContents()
        self.similarity_window.tableResultados.resizeRowsToContents()
    #Construye la tabla de los mejores resultados en base a los resultados obtenidos
    def build_top_table(self):
        self.top_info = format_top_results(self.main_info.sim_results)
        (rows, columns, data) = self.top_info

        self.model = TableModel_Similarities(data)
        self.model.rows = format_paths(rows)
        self.model.columns = format_paths(columns)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)
        self.proxy_model.setSourceModel(self.model)

        self.similarity_window.tableAltas.setModel(self.proxy_model)
        self.similarity_window.tableAltas.resizeColumnsToContents()
        self.similarity_window.tableAltas.resizeRowsToContents()

    #Abre la ventana de configuración de filtros con las configuraciones previamente cargadas
    def open_filters(self):
        filters_list = get_filters_list(self.main_info.get_directory())

        if self.folder_checkbox_state:
            self.filters_window.checkboxCarpetas.setChecked(True)
        else:
            self.filters_window.checkboxCarpetas.setChecked(False)
        if self.filters_window.checkboxCarpetas.isChecked():
            self.filters_window.frameFiltros.setEnabled(False)
        else:
            self.filters_window.frameFiltros.setEnabled(True)

        if self.measure_checkbox_state:
            self.filters_window.checkboxSimilitudR.setChecked(True)
        else:
            self.filters_window.checkboxSimilitudR.setChecked(False)
        self.show_current_parameters()
        if self.filters_window.checkboxSimilitudR.isChecked():
            self.filters_window.frameParametros.setEnabled(False)
        else:
            self.filters_window.frameParametros.setEnabled(True)

        self.filters_window.listDisponibles.clear()
        self.filters_window.listDisponibles.addItems(filters_list)
        self.filters_window.checkboxCarpetas.stateChanged.connect(self.state_changed)

        self.filters_window.listFiltradas.clear()
        self.filters_window.listFiltradas.addItems(self.filters)

        self.filters_window.checkboxSimilitudR.stateChanged.connect(self.state_changed_similitudes)
        self.update_similarity_description()
        self.update_type_description()

        self.newWindow_filters.show()
    #Habilita o deshabilita los filtros de las carpetas almacenadas en el directorio principal
    def state_changed(self):
        if self.filters_window.checkboxCarpetas.isChecked():
            self.filters_window.frameFiltros.setEnabled(False)
        else:
            self.filters_window.frameFiltros.setEnabled(True)
    #Habilita o deshabilita los filtros de los distintos modelos y medidas de similitud
    #En caso de estar deshabilitados, se usa el modelo y medida recomendados
    def state_changed_similitudes(self):
        if self.filters_window.checkboxSimilitudR.isChecked():
            self.filters_window.frameParametros.setEnabled(False)
            self.filters_window.comboBoxMedida.setCurrentIndex(0)
            self.filters_window.comboBoxTipo.setCurrentIndex(1)
        else:
            self.filters_window.frameParametros.setEnabled(True)
    # Muestra los parametros correctos guardados en la configuración
    def show_current_parameters(self):
        measure = self.current_similarity_function
        type = self.current_similarity_type
        bag_words = ["Similitud de Cosenos",
                     "Coeficiente de Jaccard",
                     "Coeficiente de Dice",
                     "Distancia Euclidiana",
                     "Distancia Manhattan"]
        regular_items = ["Similitud de Cosenos",
                         "Distancia Euclidiana",
                         "Distancia Manhattan"]

        # Pone el parametro de tipo correcto en la configuración
        if type == "Bolsa de palabras":
            self.filters_window.comboBoxTipo.setCurrentIndex(0)
        elif type == "Sentence-Transformers 1":
            self.filters_window.comboBoxTipo.setCurrentIndex(1)
        elif type == "Sentence-Transformers 2":
            self.filters_window.comboBoxTipo.setCurrentIndex(2)
        elif type == "Sentence-Transformers 3":
            self.filters_window.comboBoxTipo.setCurrentIndex(3)
        elif type == "Doc2Vec":
            self.filters_window.comboBoxTipo.setCurrentIndex(4)
        else:
            self.filters_window.comboBoxTipo.setCurrentIndex(1)

        self.filters_window.comboBoxMedida.clear()
        if type == "Bolsa de palabras":
            self.filters_window.comboBoxMedida.addItems(bag_words)
        else:
            self.filters_window.comboBoxMedida.addItems(regular_items)

        #Pone el parametro de medida correcto en la configuración
        if measure == "Similitud de Cosenos":
            self.filters_window.comboBoxMedida.setCurrentIndex(0)
        elif measure == "Coeficiente de Jaccard":
            self.filters_window.comboBoxMedida.setCurrentIndex(1)
        elif measure == "Coeficiente de Dice":
            self.filters_window.comboBoxMedida.setCurrentIndex(2)
        elif measure == "Distancia Euclidiana":
            if type == "Bolsa de palabras":
                self.filters_window.comboBoxMedida.setCurrentIndex(3)
            else:
                self.filters_window.comboBoxMedida.setCurrentIndex(1)
        elif measure == "Distancia Manhattan":
            if type == "Bolsa de palabras":
                self.filters_window.comboBoxMedida.setCurrentIndex(4)
            else:
                self.filters_window.comboBoxMedida.setCurrentIndex(2)
        else:
            self.filters_window.comboBoxMedida.setCurrentIndex(0)

    # Abre la ventana para cargar el archivo de Resultados
    def load_results(self):
        results_directory = QtWidgets.QFileDialog.getOpenFileName(None, "Selecciona un Archivo de Resultados",
                                                                  "Resultados Guardados", "json Files (*.json)")

        if results_directory[0] == "":
            return

        self.loaded_results_state = True
        # Esta funcion guarda previamente las configuraciones antes de cargar las del archivo
        self.save_settings()
        loaded_data = {}
        with open(results_directory[0], "r") as read_file:
            loaded_data = json.load(read_file)

        # Asigna los datos cargados en las variables de la app
        self.main_info.directory = loaded_data["main_info"]["directory"]
        self.main_info.dir_files = loaded_data["main_info"]["dir_files"]
        self.main_info.files = loaded_data["main_info"]["files"]
        self.main_info.text = loaded_data["main_info"]["text"]
        self.main_info.corrupted_files = loaded_data["main_info"]["corrupted_files"]
        self.main_info.sim_results = loaded_data["main_info"]["sim_results"]
        self.top_info = loaded_data["top_info"]
        self.main_directories = loaded_data["main_directories"]
        self.filters = loaded_data["filters"]
        self.current_similarity_function = loaded_data["current_similarity_function"]
        self.current_similarity_type = loaded_data["current_similarity_type"]
        self.folder_checkbox_state = loaded_data["folder_checkbox_state"]
        self.measure_checkbox_state = loaded_data["measure_checkbox_state"]

        self.load_parameters()

    # Asigna los parametros en las ventanas en base al archivo de Resultados
    def load_parameters(self):
        # Carga los parametros para la ventana de filtros
        filters_list = get_filters_list(self.main_info.get_directory())

        if self.folder_checkbox_state:
            self.filters_window.checkboxCarpetas.setChecked(True)
        else:
            self.filters_window.checkboxCarpetas.setChecked(False)
        if self.filters_window.checkboxCarpetas.isChecked():
            self.filters_window.frameFiltros.setEnabled(False)
        else:
            self.filters_window.frameFiltros.setEnabled(True)

        if self.measure_checkbox_state:
            self.filters_window.checkboxSimilitudR.setChecked(True)
        else:
            self.filters_window.checkboxSimilitudR.setChecked(False)
        self.show_current_parameters()
        if self.filters_window.checkboxSimilitudR.isChecked():
            self.filters_window.frameParametros.setEnabled(False)
        else:
            self.filters_window.frameParametros.setEnabled(True)

        self.filters_window.listDisponibles.clear()
        self.filters_window.listDisponibles.addItems(filters_list)
        self.filters_window.checkboxCarpetas.stateChanged.connect(self.state_changed)

        self.filters_window.listFiltradas.clear()
        self.filters_window.listFiltradas.addItems(self.filters)

        self.filters_window.checkboxSimilitudR.stateChanged.connect(self.state_changed_similitudes)
        self.update_similarity_description()
        self.update_type_description()

        #Carga la tabla del menú principal
        self.show_filt_table()

    #########################FUNCIONES DE LA VENTANA DE FILTROS#######################################
    #Añade el filtro de la carpeta seleccionada en la casilla de carpetas disponibles
    def add_filter(self):
        items = [str(self.filters_window.listFiltradas.item(i).text()) for i in range(self.filters_window.listFiltradas.count())]

        for selectedItem in self.filters_window.listDisponibles.selectedItems():
            if not selectedItem.text() in items:
                self.filters_window.listFiltradas.addItem(selectedItem.text())
    #Elimina el filtro de la carpeta seleccionada en la casilla de carpetas filtradas
    def delete_filter(self):
        items = [str(self.filters_window.listFiltradas.item(i).text()) for i in range(self.filters_window.listFiltradas.count())]

        for selectedItem in self.filters_window.listFiltradas.selectedItems():
            items.remove(selectedItem.text())
        self.filters_window.listFiltradas.clear()
        self.filters_window.listFiltradas.addItems(items)
    #Funcion para guardar todas las configuraciones realizadas en la ventana de filtros
    def save_filters(self):
        items = [str(self.filters_window.listFiltradas.item(i).text()) for i in range(self.filters_window.listFiltradas.count())]
        if self.loaded_results_state is True:
            if items != self.filters \
                or self.filters_window.checkboxCarpetas.isChecked() != self.folder_checkbox_state \
                or self.filters_window.checkboxSimilitudR.isChecked() != self.measure_checkbox_state \
                or self.translate_similarity() != self.current_similarity_function \
                    or self.translate_type() != self.current_similarity_type:
                self.newDialog_load.show()
                return
        self.filters = items
        self.show_filt_table()
        self.newWindow_filters.hide()

    #Muestra la tabla con los filtros cambiados
    def show_filt_table(self):
        if self.filters_window.checkboxCarpetas.isChecked() or self.filters_window.listFiltradas.count() == 0:
            self.folder_checkbox_state = True
            self.show_docs_table()
        else:
            self.folder_checkbox_state = False
            if self.loaded_results_state is False:
                self.main_info = get_filt_docs(self.main_info, self.main_directories, self.filters)

            data = format_data(self.main_info.get_files())

            self.model = TableModel_Menu(data)
            self.proxy_model = QSortFilterProxyModel()
            self.proxy_model.setFilterKeyColumn(-1)
            self.proxy_model.setSourceModel(self.model)

            self.menu.tableDocs.clearSpans()
            self.menu.tableDocs.setModel(self.proxy_model)
            self.menu.tableDocs.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            self.menu.tableDocs.resizeColumnToContents(1)

            self.menu.stackedWidget.setCurrentWidget(self.menu.pageDocs)
            self.menu.menuOpciones.setEnabled(True)

        if self.filters_window.checkboxSimilitudR.isChecked():
            self.measure_checkbox_state = True
            self.current_similarity_function = "Similitud de Cosenos"
            self.current_similarity_type = "Sentence-Transformers 1"
            self.filters_window.comboBoxMedida.setCurrentIndex(0)
            self.filters_window.comboBoxTipo.setCurrentIndex(1)
        else:
            self.measure_checkbox_state = False
            self.change_similarity_function()
            self.change_similarity_type()

    #Cambia la medida de similitud que se utilizará
    def change_similarity_function(self):
        value = self.filters_window.comboBoxMedida.currentText()
        if value == "Similitud de Cosenos":
            self.current_similarity_function = "Similitud de Cosenos"
        elif value == "Coeficiente de Jaccard":
            self.current_similarity_function = "Coeficiente de Jaccard"
        elif value == "Coeficiente de Dice":
            self.current_similarity_function = "Coeficiente de Dice"
        elif value == "Distancia Euclidiana":
            self.current_similarity_function = "Distancia Euclidiana"
        elif value == "Distancia Manhattan":
            self.current_similarity_function = "Distancia Manhattan"
        else:
            self.current_similarity_function = "Similitud de Cosenos"

    # Cambia el modelo para la medida de similitud que se utilizará
    def change_similarity_type(self):
        value = self.filters_window.comboBoxTipo.currentText()
        if value == "Bolsa de palabras":
            self.current_similarity_type = "Bolsa de palabras"
        elif value == "Sentence-Transformers 1":
            self.current_similarity_type = "Sentence-Transformers 1"
        elif value == "Sentence-Transformers 2":
            self.current_similarity_type = "Sentence-Transformers 2"
        elif value == "Sentence-Transformers 3":
            self.current_similarity_type = "Sentence-Transformers 3"
        elif value == "Doc2Vec":
            self.current_similarity_type = "Doc2Vec"
        else:
            self.current_similarity_type = "Sentence-Transformers 1"

    # Actualiza la descripcion de la medida de similitud seleccionada en el combo box
    def update_similarity_description(self):
        value = self.filters_window.comboBoxMedida.currentText()
        descriptions = [
            "Descripción:\nMide la correlación entre dos documentos vectorizados \nal cuantificar el coseno del ángulo entre ellos.\n\nVelocidad: MEDIA, complejidad logarítmica ligeramente \nmayor a las demás medidas.\n\nPrecisión: ALTA, relaciona mejor los documentos \nen la mayoría de los casos.",
            "Descripción:\nMide la correlación entre dos documentos vectorizados \nal cuantificar la intersección que existe entre ellos.\n\nVelocidad: ALTA, poca complejidad logarítmica.\n\nPrecisión: MEDIA, no considera el nivel de relevancia \ndel contenido de los documentos.",
            "Descripción:\nMide la correlación entre dos documentos vectorizados \nal cuantificar la intersección que existe entre ellos.\n\nVelocidad: ALTA, poca complejidad logarítmica.\n\nPrecisión: MEDIA, no considera el nivel de relevancia \ndel contenido de los documentos, \nle da mayor relevancia a los valores \ncomunes de los documentos.",
            "Descripción:\nMide la correlación entre dos documentos vectorizados \nal cuantificar las distancia que existe entre ellos.\n\nVelocidad: ALTA, poca complejidad logarítmica.\n\nPrecisión: MEDIA, pierde precisión entre menos \nrelación tenga el contenido de los documentos.",
            "Descripción:\nMide la correlación entre dos documentos vectorizados \nal cuantificar las distancia que existe entre ellos.\n\nVelocidad: ALTA, poca complejidad logarítmica.\n\nPrecisión: BAJA, pierde precisión entre menos \nrelación tenga el contenido de los documentos, \nmenor precisión que la Distancia Euclidiana."
        ]

        if value == "Similitud de Cosenos":
            self.filters_window.lblDescMedida.setText(descriptions[0])
        elif value == "Coeficiente de Jaccard":
            self.filters_window.lblDescMedida.setText(descriptions[1])
        elif value == "Coeficiente de Dice":
            self.filters_window.lblDescMedida.setText(descriptions[2])
        elif value == "Distancia Euclidiana":
            self.filters_window.lblDescMedida.setText(descriptions[3])
        elif value == "Distancia Manhattan":
            self.filters_window.lblDescMedida.setText(descriptions[4])
        else:
            self.filters_window.lblDescMedida.setText(descriptions[0])

    # Actualiza la descripcion del modelo para la medida de similitud seleccionada en el combo box
    def update_type_description(self):
        value = self.filters_window.comboBoxTipo.currentText()
        descriptions = [
            "Descripción:\nPondera los documentos en base a la aparicion de terminos \nen los documentos utilizando medidas binarias \no de TF-IDF.\n\nVelocidad: ALTA, se reduce en base al contenido \ny cantidad de los documentos.\n\nPrecisión: MEDIA, no considera el contexto o la semántica \ndel contenido.",
            "Descripción:\nUtiliza un modelo pre-entrenado con un conjunto de datos \nprevio para ponderar los documentos en base \na su relación semántica con este conjunto.\n\nVelocidad: MEDIA, se reduce en base a la cantidad \nde documentos.\n\nPrecisión: ALTA, considera el contexto y la semántica \ndel contenido.",
            "Descripción:\nUtiliza un modelo pre-entrenado con un conjunto de datos \nprevio para ponderar los documentos en base \na su relación semántica con este conjunto.\n\nVelocidad: MEDIA, se reduce en base a la cantidad \nde documentos.\n\nPrecisión: ALTA, considera el contexto y la semántica \ndel contenido.",
            "Descripción:\nUtiliza un modelo pre-entrenado con un conjunto de datos \nprevio para ponderar los documentos en base \na su relación semántica con este conjunto.\n\nVelocidad: MEDIA, se reduce en base a la cantidad \nde documentos.\n\nPrecisión: ALTA, considera el contexto y la semántica \ndel contenido.",
            "Descripción:\nPondera los documentos al entrenar un modelo con el \ncontenido de los mismos, estableciendo la relación semántica \nque existe entre ellos.\n\nVelocidad: BAJA, se reduce en base al contenido \ny cantidad de los documentos.\n\nPrecisión: MEDIA, considera el contexto y la semántica, \nsu precisión varía en base al contenido con que se \nentrenó."
        ]

        if value == "Bolsa de palabras":
            self.filters_window.lblDescTipo.setText(descriptions[0])
        elif value == "Sentence-Transformers 1":
            self.filters_window.lblDescTipo.setText(descriptions[1])
        elif value == "Sentence-Transformers 2":
            self.filters_window.lblDescTipo.setText(descriptions[2])
        elif value == "Sentence-Transformers 3":
            self.filters_window.lblDescTipo.setText(descriptions[3])
        elif value == "Doc2Vec":
            self.filters_window.lblDescTipo.setText(descriptions[4])
        else:
            self.filters_window.lblDescTipo.setText(descriptions[1])

    #Actualiza las opciones del combo box en base al modelo que se utiliza
    def update_type_combobox(self):
        value = self.filters_window.comboBoxTipo.currentText()
        bag_words = ["Similitud de Cosenos",
                     "Coeficiente de Jaccard",
                     "Coeficiente de Dice",
                     "Distancia Euclidiana",
                     "Distancia Manhattan"]
        regular_items = ["Similitud de Cosenos",
                         "Distancia Euclidiana",
                         "Distancia Manhattan"]

        self.filters_window.comboBoxMedida.clear()
        if value == "Bolsa de palabras":
            self.filters_window.comboBoxMedida.addItems(bag_words)
        else:
            self.filters_window.comboBoxMedida.addItems(regular_items)
        self.update_type_description()

    # Determina el tipo de medida de similitud que se trata y la asocia con su termino en cuestion
    # Esta funcion es utilizada para establecer una relacion entre las opciones del combobox
    #   y el termino que se utiliza para guardarlo en la configuracion
    def translate_similarity(self):
        value = self.filters_window.comboBoxMedida.currentText()
        if value == "Similitud de Cosenos":
            return "Similitud de Cosenos"
        elif value == "Coeficiente de Jaccard":
            return "Coeficiente de Jaccard"
        elif value == "Coeficiente de Dice":
            return "Coeficiente de Dice"
        elif value == "Distancia Euclidiana":
            return "Distancia Euclidiana"
        elif value == "Distancia Manhattan":
            return "Distancia Manhattan"
        return "Similitud de Cosenos"

    # Determina el tipo de sub-tipo de la medida de similitud que se trata y la asocia con su termino en cuestion
    # Esta funcion es utilizada para establecer una relacion entre las opciones del combobox
    #   y el termino que se utiliza para guardarlo en la configuracion
    def translate_type(self):
        value = self.filters_window.comboBoxTipo.currentText()
        if value == "Bolsa de palabras":
            return "Bolsa de palabras"
        elif value == "Sentence-Transformers 1":
            return "Sentence-Transformers 1"
        elif value == "Sentence-Transformers 2":
            return "Sentence-Transformers 2"
        elif value == "Sentence-Transformers 3":
            return "Sentence-Transformers 3"
        elif value == "Doc2Vec":
            return "Doc2Vec"
        return "Bolsa de palabras"

    #####################FUNCIONES DE LA VENTANA DE LAS TABLAS DE SIMILITUDES#########################
    #Abre los archivos seleccionados en las casillas de la tabla de similitudes principal
    def open_files(self):
        rows = sorted(set(index.row() for index in
                          self.similarity_window.tableResultados.selectedIndexes()))
        columns = sorted(set(index.column() for index in
                             self.similarity_window.tableResultados.selectedIndexes()))

        #En caso de no poder ejecutar algun archivo, arroja un diálogo de error
        if not start_files(rows, columns, self.main_info.dir_files):
            self.newDialog_open_files.show()

    #Abre los archivos seleccionados en las casillas de la tabla con mejores resultados
    def open_top_files(self):
        (rows, columns, data) = self.top_info
        files_to_start = set()

        selected_rows = sorted(set(index.row() for index in
                                   self.similarity_window.tableAltas.selectedIndexes()))
        selected_columns = sorted(set(index.column() for index in
                                      self.similarity_window.tableAltas.selectedIndexes()))
        for row in selected_rows:
            files_to_start.add(rows[row])
        for column in selected_columns:
            files_to_start.add(columns[column])
        for file in files_to_start:
            try:
                os.startfile(file)
            # En caso de no poder ejecutar algun archivo, arroja un diálogo de error
            except:
                self.newDialog_open_files.show()
                return

    #Abre la ventana para asignar el nombre del archivo que guarda los resultados obtenidos
    def assign_filename(self):
        self.save_results_window.txtboxNombreArchivo.clear()
        self.newWindow_results.show()

    #####################FUNCIONES DE LA VENTANA PARA GUARDAR RESULTADOS#########################
    #Guarda los datos de los resultados en la carpeta asignada
    #El archivo es .json que utiliza la biblioteca "json" de python
    # para la conversión de las variables principales
    def save_similarity_results(self):
        name = self.save_results_window.txtboxNombreArchivo.text()
        r = re.compile('.*[<>\'\"/?;`%]+.*|\s\s*')

        if name == "" or r.match(name) or self.verify_filename(name):
            self.newDialog_save_error.show()
            self.save_results_window.txtboxNombreArchivo.clear()
            return
        #Crea el diccionario con las variables principales a utilizar
        #En su mayoría se trata de listas o arreglos de n dimensiones
        data_file = {
            "main_info": {
                "directory": self.main_info.directory,
                "dir_files": self.main_info.dir_files,
                "files": self.main_info.files,
                "text": self.main_info.text,
                "corrupted_files": self.main_info.corrupted_files,
                "sim_results": self.main_info.sim_results,
                "vectors": self.main_info.vectors
            },
            "top_info": self.top_info,
            "main_directories": self.main_directories,
            "filters": self.filters,
            "current_similarity_function": self.current_similarity_function,
            "current_similarity_type": self.current_similarity_type,
            "folder_checkbox_state": self.folder_checkbox_state,
            "measure_checkbox_state": self.measure_checkbox_state,
        }
        with open(f"Resultados Guardados/{name}.json", "w") as write_file:
            json.dump(data_file, write_file, cls=NumpyEncoder)

        self.newDialog_save.show()
        self.newWindow_results.close()

    # Comprueba que no exista ningun archivo con el nombre con el que se guardará el archivo
    def verify_filename(self, filename):
        for path, dirs, files in os.walk("Resultados Guardados"):
            for name in files:
                if name.replace(".json", "") == filename:
                    return True
        return False

    #####################FUNCIONES DEL DIALOGO CARGAR RESULTADOS#########################
    #Funcion que cambia las opciones de los resultados cargados por las nuevas que han sido configuradas
    #Se usa tras haber guardado configuraciones a partir de un archivo de resultados
    def change_loaded_results(self):
        self.loaded_results_state = False
        self.newDialog_load.close()
        self.save_filters()

    #####################FUNCIONES PARA LA VENTANA DE ANALISIS DE RESULTADOS#########################
    #Muestra la ventana de carga de análisis de resultados
    def show_analizer(self):
        self.newWindow_analizing.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.newWindow_analizing.show()
        self.execute_analizer()

    #Ejecuta las tareas de análisis de resultados y actualización de la barra de carga de la ventana
    def execute_analizer(self):
        self.update_analizer_progress(0)
        self.thread = QThread()
        self.analyzer = Analyzer()
        self.analyzer.main_info = self.main_info
        self.analyzer.similarity_measure = self.current_similarity_function
        self.analyzer.similarity_type = self.current_similarity_type
        self.analyzer.moveToThread(self.thread)

        self.thread.started.connect(self.analyzer.run)
        self.analyzer.finished.connect(self.thread.quit)
        self.analyzer.finished.connect(self.analyzer.deleteLater)
        # Conecta la función de despligue de resultados una vez se termina el análisis de resultados
        self.thread.finished.connect(self.launch_similarity_tables)
        self.analyzer.progress.connect(self.update_analizer_progress)

        self.thread.start()

    #Actualiza el progreso de la barra de carga cada que se le llama
    def update_analizer_progress(self, progress):
        self.analizing_window.progressAnalisis.setValue(progress)

    #Se encarga de desplegar los resultados obtenidos
    # y cerrar la ventana de análisis de resultados
    def launch_similarity_tables(self):
        self.thread.deleteLater()
        self.main_info = self.analyzer.main_info
        self.newWindow_analizing.close()

        self.build_table_results()
        self.build_top_table()

        self.newWindow_similarity.show()

# Clase hecha para poder generar la tabla de los documentos del directorio en el menú principal
class TableModel_Menu(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]
        if role == Qt.BackgroundRole:
            return QBrush(QtGui.QColor(78,78,78))
        if role == Qt.ForegroundRole:
            return QBrush(QtGui.QColor(247,247,247))

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        data=['Nombre del Archivo','Extension']

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return f'{data[section]}'
        return super().headerData(section, orientation, role)

# Clase hecha para poder generar las tablas de los resultados de similitud
class TableModel_Similarities(QAbstractTableModel):
    rows=[]
    columns=[]

    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]
        if role == Qt.BackgroundRole:
            if self._data[index.row()][index.column()] == 0.0:
                return QBrush(QtGui.QColor(78, 78, 78))
            elif self._data[index.row()][index.column()] < 60.0:
                return QBrush(QtGui.QColor(70,189,92))
            elif self._data[index.row()][index.column()] < 85.00:
                return QBrush(QtGui.QColor(199,143,64))
            else:
                return QBrush(QtGui.QColor(156,39,39))
        if role == Qt.ForegroundRole:
            return QBrush(QtGui.QColor(247,247,247))

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return f'{self.columns[section]}'
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return f'{self.rows[section]}'
        return super().headerData(section, orientation, role)

# Esta clase permite analizar los textos y generar los resultados evitando el freeze de las ventanas
class Analyzer(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    main_info = MainInfo()
    similarity_measure = ""
    similarity_type = ""
    similarity_function = similarities()

    def run(self):
        # Se pasa la funcion para actualizar el progreso de analisis
        # a la funcion que realiza los procesos de analisis de resultados
        self.get_results_by_parameters(self.update_progress)
        self.finished.emit()

    #Emite la señal con el valor del progreso del analisis
    def update_progress(self, percent):
        self.progress.emit(percent)

    #Funcion principal del analisis de resultados
    #Se encarga de llamar las funciones que realizan el preprocesamiento
    # y obtencion de los resultados de similitud
    #Todas las funciones emiten la señal de las distintas fases de su progreso
    def get_results_by_parameters(self, update_ui):
        self.main_info = get_texts(self.main_info)

        if self.similarity_measure == "Similitud de Cosenos" and self.similarity_type == "Bolsa de palabras":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_cossim_by_tfidf(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)
        elif self.similarity_measure == "Similitud de Cosenos" and self.similarity_type == "Sentence-Transformers 1":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_cossim_by_model1(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)
        elif self.similarity_measure == "Similitud de Cosenos" and self.similarity_type == "Sentence-Transformers 2":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_cossim_by_model2(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)
        elif self.similarity_measure == "Similitud de Cosenos" and self.similarity_type == "Sentence-Transformers 3":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_cossim_by_model3(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)
        elif self.similarity_measure == "Similitud de Cosenos" and self.similarity_type == "Doc2Vec":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_cossim_by_doc2vec(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)

        elif self.similarity_measure == "Distancia Euclidiana" and self.similarity_type == "Bolsa de palabras":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_euclidean_by_tfidf(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)
        elif self.similarity_measure == "Distancia Euclidiana" and self.similarity_type == "Sentence-Transformers 1":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_euclidean_by_model1(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)
        elif self.similarity_measure == "Distancia Euclidiana" and self.similarity_type == "Sentence-Transformers 2":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_euclidean_by_model2(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)
        elif self.similarity_measure == "Distancia Euclidiana" and self.similarity_type == "Sentence-Transformers 3":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_euclidean_by_model3(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)
        elif self.similarity_measure == "Distancia Euclidiana" and self.similarity_type == "Doc2Vec":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_euclidean_by_doc2vec(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)

        elif self.similarity_measure == "Distancia Manhattan" and self.similarity_type == "Bolsa de palabras":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_manhattan_by_tfidf(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)
        elif self.similarity_measure == "Distancia Manhattan" and self.similarity_type == "Sentence-Transformers 1":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_manhattan_by_model1(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)
        elif self.similarity_measure == "Distancia Manhattan" and self.similarity_type == "Sentence-Transformers 2":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_manhattan_by_model2(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)
        elif self.similarity_measure == "Distancia Manhattan" and self.similarity_type == "Sentence-Transformers 3":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_manhattan_by_model3(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)
        elif self.similarity_measure == "Distancia Manhattan" and self.similarity_type == "Doc2Vec":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_manhattan_by_doc2vec(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)

        elif self.similarity_measure == "Coeficiente de Jaccard" and self.similarity_type == "Bolsa de palabras":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_jaccard_by_tfidf(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)

        elif self.similarity_measure == "Coeficiente de Dice" and self.similarity_type == "Bolsa de palabras":
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_dice_by_tfidf(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)

        else:
            self.main_info.vectors, self.main_info.sim_results = self.similarity_function.get_cossim_by_tfidf(self.main_info.dir_files, self.main_info.text, self.main_info.vectors, update_ui)

# Esta clase soluciona el error de compatibilidad de la librería "json" con la librería "numpy/np"
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())