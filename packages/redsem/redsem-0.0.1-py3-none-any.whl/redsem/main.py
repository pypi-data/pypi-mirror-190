# TODO: documentar módulo
# TODO: documentar funciones
import networkx as nx


def filtrar_primeras_posiciones(df, ultima=3):
    assert 'posicion' in df.columns, 'El marco de datos debe tener una columna llamada "posicion"'
    rango = range(1, ultima + 1)
    filtro = df['posicion'].isin(rango)
    df_filtrado = df[filtro].reset_index(drop=True)
    return df_filtrado


# TODO: assert, partición solo puede tomar los valores 'estimulo' o 'respuesta'
def extraer_particion(red, particion):
    assert nx.bipartite.is_bipartite(red), 'La red no es bipartita'
    nodos_en_particion = [n for n, d in red.nodes(data=True) if d['bipartita'] == particion]
    if len(nodos_en_particion) == 0:
        raise ValueError(f'No hay nodos en la partición "{particion}"')
    return nodos_en_particion


def obtener_respuestas_asociadas(red, *estimulos):
    estimulos_validos = extraer_particion(red, 'estimulo')
    assert set(estimulos).issubset(estimulos_validos), f'Las palabras estímulo válidas son:\n{estimulos_validos}'
    respuestas_asociadas = []
    for estimulo in estimulos:
        respuestas_asociadas += list(red.neighbors(estimulo))
    return respuestas_asociadas


def filtrar_red_por_estimulos(red, *estimulos):
    respuestas_asociadas = obtener_respuestas_asociadas(red, *estimulos)
    estimulos_y_respuestas = respuestas_asociadas + list(estimulos)
    red_filtrada = red.subgraph(estimulos_y_respuestas).copy()
    return red_filtrada


def proyectar_red_por_estimulos(red, *estimulos):
    respuestas_asociadas = obtener_respuestas_asociadas(red, *estimulos)
    red_filtrada = filtrar_red_por_estimulos(red, *estimulos)
    proyeccion = nx.bipartite.projected_graph(red_filtrada, respuestas_asociadas)
    return proyeccion
