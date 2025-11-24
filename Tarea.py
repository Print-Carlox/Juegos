import streamlit as st
import io

st.title("Juegos Panamericanos")

lista_txt = []

archivo = st.file_uploader("Sube un archivo.txt", type=["txt"])
if archivo is not None:
    contenido = archivo.getvalue().decode("utf-8")
    for cadena in contenido.splitlines():
        lista = cadena.strip().split(" ")
        lista_txt.append(lista)
    st.success("Archivo cargado y procesado correctamente")
else:
    st.info("Por favor sube el archivo para continuar")

columna1, columna2 = st.columns(2)

def sumar_medallas(valor):
    if valor == "ORO":
        indice = 0
    elif valor == "PLATA":
        indice = 1
    else:
        indice = 2
    return indice

def sin_paises_repetidos(lista):
    diccionario = {}
    for elemento in lista:
        if elemento[1] not in diccionario:
            diccionario[elemento[1]] = [0,0,0]
        diccionario[elemento[1]][sumar_medallas(elemento[2])] += 1
    return diccionario       

paises_medallas = sin_paises_repetidos(lista_txt)
paises_ordenados = sorted(paises_medallas.items(), key=lambda x: sum(x[1]), reverse=True )

contenido = "{:<7}{:<7}{:<7}{:<7}{:<7}\n".format("País","Oro","Plata","Bronce","Total")
for tupla in paises_ordenados:
    contenido += "{:<7}{:<7}{:<7}{:<7}{:<7}\n".format(tupla[0],tupla[1][0],tupla[1][1],tupla[1][2],sum(tupla[1]))
cont = io.BytesIO(contenido.encode("utf-8"))
if archivo is not None:
    with columna1:
        st.write("Archivo con la cantidad de medallas que obtuvo cada país y su total")
        st.download_button(label = "Descargar medallero.txt",
                   data = cont,
                   file_name = "medallero.txt",
                   mime = "text/plain")

def medallas_por_deporte(lista):
    deportes = {}
    for sublista in lista:
        if sublista[0] not in deportes:
            deportes[sublista[0]] = 1
        else:
            deportes[sublista[0]] += 1
    return deportes
            
deportes = medallas_por_deporte(lista_txt)
deportes_ordenados = sorted(deportes.items(), key=lambda x: x[1], reverse=True)

contenido_2 = "{:<25}{:<5}\n".format("Deporte","Medalla")
for tupla in deportes_ordenados:
    contenido_2 += "{:<25}{:<5}\n".format(tupla[0],tupla[1])
cont_2 = io.BytesIO(contenido_2.encode("utf-8"))
if archivo is not None:
    with columna2:
        st.write("Archivo con la cantidad de medallas que se entregaron en cada deporte")
        st.download_button(label = "Descargar deportes.txt",
                   data = cont_2,
                   file_name = "deportes.txt",
                   mime = "text/plain")
    
def indice_deporte(lista,elemento):
    for i,sublista in enumerate(lista):
        if elemento in sublista:
            return i

def sin_atletas_repetidos(indice):
    lista = []
    for sublista in lista_txt:
        if sublista[indice] not in lista:
            lista.append(sublista[indice])
    return lista
            
atletas_lista = sin_atletas_repetidos(3)

def datos_por_deporte(lista,diccionario,deporte):
    inicio = indice_deporte(lista,deporte)
    matriz = [["Nombre","País","Medallas"]]
    for x in lista[inicio:diccionario.get(deporte)+inicio]:
        matriz.append([' '.join(x[3].split("_")),x[1],x[2]])
    st.dataframe(matriz)
    
def indice_atleta(lista,elemento):
    ind_list = []
    for i,sublista in enumerate(lista):
        if elemento in sublista:
            ind_list.append(i)
    return ind_list
    
def datos_por_atleta(lista,atleta):
    posiciones = indice_atleta(lista,atleta)
    matriz = [["País","Deporte","Medalla"]]
    for x in posiciones:
        matriz.append([lista[x][1],lista[x][0],lista[x][2]])
    st.dataframe(matriz)

def datos_por_pais(lista,diccinario,elemento):
    st.success("Las medallas que obtuvo fueron Oro: {} | Plata: {} | Bronce: {} | Haciendo un total de {} medallas".format(
        diccinario.get(elemento)[0],diccinario.get(elemento)[1],diccinario.get(elemento)[2],sum(diccinario.get(elemento))))
    matriz = [["Atleta","Medalla","Deporte"]]
    for x in lista:
        if x[1] == elemento:
            matriz.append([' '.join(x[3].split("_")),x[2],x[0]])
    st.dataframe(matriz)
    
def datos_por_medalla(lista,medalla):
    matriz = [["Atleta","Deporte"]]
    for j in lista:
        if j[2] == medalla:
            matriz.append([' '.join(j[3].split("_")),j[0]])
    st.dataframe(matriz)

opcion = st.selectbox("¿Qué deseas consultar?",
                      ["Seleccione una opción",
                       "1. Datos por deporte: Nombre de los atletas, país y medallas que obtuvieron",
                       "2. Datos por Atleta: País de procedencia, deporte que practica y resultado que obtuvo",
                       "3. Datos por país: Medallas que obtuvo en total y sus atletas con su resultado",
                       "4. Datos por medalla: Atletas que la obtuvieron y en que deporte"])

if opcion == "1. Datos por deporte: Nombre de los atletas, país y medallas que obtuvieron":
    deporte = st.selectbox("Seleccione un deporte", list(deportes.keys()))
    if st.button("Ver resultados"):
        datos_por_deporte(lista_txt,deportes,deporte)
        
elif opcion == "2. Datos por Atleta: País de procedencia, deporte que practica y resultado que obtuvo":
    atleta = st.selectbox("Seleccione un atleta", atletas_lista)
    if st.button("Ver resultados"):
        datos_por_atleta(lista_txt,atleta)
    
elif opcion == "3. Datos por país: Medallas que obtuvo en total y sus atletas con su resultado":
    pais = st.selectbox("Seleccione un país", list(paises_medallas.keys()))
    if st.button("Ver resultados"):
        datos_por_pais(lista_txt,paises_medallas,pais)
elif opcion == "4. Datos por medalla: Atletas que la obtuvieron y en que deporte":
    medalla = st.selectbox("Seleccione una medalla", ["ORO","PLATA","BRONCE"])
    if st.button("Ver resultados"):
        datos_por_medalla(lista_txt,medalla)
