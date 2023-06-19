#Clase con las variables necesarias para realizar el proceso de análisis de resultados
class MainInfo:

    def __init__(self):
        self.directory = "" # Directorio principal
        self.dir_files = [] # Directorios de los documentos alojados en el directorio principal
        self.files = [] # Nombres de los documentos
        self.text = [] # Textos planos de los documentos
        self.corrupted_files = [] # Posibles documentos corruptos
        self.sim_results = [] # Resultados de similitud de todas las comparaciones
        self.vectors = ("", []) # Vectores obtenidos a partir de los documentos

    def get_directory(self):
        return self.directory
    def set_directory(self, directory):
        self.directory = directory

    def get_dir_files(self):
        return self.dir_files
    def set_dir_files(self, dir_file):
        self.dir_files.append(dir_file)

    def get_files(self):
        return self.files
    def set_files(self, file):
        self.files.append(file)

    def get_text(self):
        return self.text
    def set_text(self, text):
        self.text.append(text)

    def get_corrupted_files(self):
        return self.corrupted_files
    def set_corrupted_files(self, corrupted_files):
        self.corrupted_files.append(corrupted_files)

    def get_sim_results(self):
        return self.sim_results
    def set_sim_results(self, sim_results):
        self.sim_results.append(sim_results)
