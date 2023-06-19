import os

#Formatea los resultados de similitudes al formato adecuado para el despligue en la tabla
def format_sim_results_v2(n_documents,sim_results):
    similarities=[]
    results = []

    #Obtiene solo los valores de las similitudes
    for doc1, doc2, sim in sim_results:
        similarities.append(float("{:.2f}".format(sim*100)))

    #Obtiene la lista con el formato correcto para los resultados de similitud
    for n in range(n_documents):
        lista = []
        for i in range(n_documents):
            lista.append(similarities.pop(0))
        results.append(lista)
    return results

#Formatea los mejores resultados de similitudes al formato adecuado para el despligue en la tabla
def format_top_results(sim_results):
    top = get_top(sim_results)
    rows = get_ver_head(top)
    columns = get_hor_head(top)
    data = get_table_data(rows, columns, sorted(top))

    return (rows,columns,data)

#Obtiene los mejores resultados (0.6/60% de similitud) en base a todos los resultados
def get_top(sim_results):
    top = []
    data = sorted(sim_results, key=lambda i: i[-1], reverse=True)

    for n in data:
        (doc1,doc2,sim) = n
        if sim >= 0.6:
            top.append(n)
        else:
            break
    return top

#Obtiene los nombres de los documentos que deben ubicarse en las filas de la tabla
def get_ver_head(top):
    headers = set()

    for doc1, doc2, sim in top:
        headers.add(doc1)
    headers = sorted(headers)
    return headers

#Obtiene los nombres de los documentos que deben ubicarse en las columnas de la tabla
def get_hor_head(top):
    headers = set()

    for doc1, doc2, sim in top:
        headers.add(doc2)
    headers = sorted(headers)
    return headers

#Formatea los resultados en el orden correcto de cada resultado para su despliegue en la tabla
def get_table_data(ver_head,hor_head,top):
    results=[]
    for row in ver_head:
        lista=[]
        for column in hor_head:
            control=False
            for doc1,doc2,sim in top:
                if(row==doc1 and column==doc2):
                    control=True
                    lista.append(float("{:.2f}".format(sim*100)))
            if control is False:
                lista.append(0.0)
        results.append(lista)
    return results

#Formatea los directorios de los documentos a únicamente su nombre
def format_paths(paths):
    lista=[]
    for path in paths:
        lista.append(os.path.basename(path))
    return lista