"""
Todas las funcionalidades para filtar marcos de datos y analizar redes semánticas.

Las redes semánticas son bipartitas y la función principal es proyectar las palabras respuesta respecto a los estímulos.

"""
import networkx as nx
import pandas as pd


def filtrar_primeras_posiciones(df, ultima_posicion=3):
    """Filtra el marco de datos para quedarse con las primeras posiciones.

    Parameters
    ----------
    df : pandas.DataFrame
    ultima_posicion : int, default=3
        Última posición a incluir en el marco de datos.

    Returns
    -------
    pandas.DataFrame
        Un marco de datos con las primeras posiciones.

    Raises
    ------
    TypeError
        Si el argumento "df" no es un marco de datos.
    ValueError
        Si el marco de datos no tiene una columna llamada "posicion".

    Examples
    --------
    >>> df_filtrado = filtrar_primeras_posiciones(df, ultima_posicion=3)
    >>> df_filtrado = filtrar_primeras_posiciones(df, ultima_posicion=5)
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError('El argumento "df" debe ser un marco de datos')
    if 'posicion' not in df.columns:
        raise ValueError('El marco de datos debe tener una columna llamada "posicion"')
    rango = range(1, ultima_posicion + 1)
    filtro = df['posicion'].isin(rango)
    df_filtrado = df[filtro].reset_index(drop=True)
    return df_filtrado


def extraer_particion(red, particion):
    """Devuelve los nodos de una red bipartita que pertenecen a la partición indicada.

    Parameters
    ----------
    red : networkx.Graph
    particion : {'estimulo', 'respuesta'}
        Nombre de la partición deseada.

    Returns
    -------
    list
        Una lista con los nodos de la partición indicada.

    Examples
    --------
    >>> estimulos = extraer_particion(red, 'estimulo')
    >>> respuestas = extraer_particion(red, 'respuesta')
    """
    if not isinstance(red, nx.Graph):
        raise TypeError('El argumento "red" debe ser una red semántica')
    if not nx.bipartite.is_bipartite(red):
        raise TypeError('La red no es bipartita')
    nodos_en_particion = [n for n, d in red.nodes(data=True) if d['bipartita'] == particion]
    if len(nodos_en_particion) == 0:
        raise ValueError(f'No hay nodos en la partición "{particion}"')
    return nodos_en_particion


def obtener_respuestas_asociadas(red, *estimulos):
    """Devuelve las respuestas asociadas (nodos) a los estímulos indicados.

    Parameters
    ----------
    red : networkx.Graph
    *estimulos : tuple
        Estímulos para los que se quiere obtener las respuestas asociadas.

    Returns
    -------
    list
        Una lista con las respuestas asociadas a los estímulos indicados.

    Raises
    ------
    ValueError
        Si alguno de los estímulos indicados no es válido.
    """
    estimulos_validos = extraer_particion(red, 'estimulo')
    if not set(estimulos).issubset(estimulos_validos):
        raise ValueError(f'Las palabras estímulo válidas son:\n{estimulos_validos}')
    respuestas_asociadas = []
    for estimulo in estimulos:
        respuestas_asociadas += list(red.neighbors(estimulo))
    return respuestas_asociadas


def filtrar_red_por_estimulos(red, *estimulos):
    """Filtra la red para quedarse con los estímulos indicados y sus respuestas asociadas

    Parameters
    ----------
    red : networkx.Graph
    *estimulos : tuple
        Estímulos que se quiere incluir en la red.

    Returns
    -------
    networkx.Graph
        Una red con los estímulos y sus respuestas asociadas
    """
    respuestas_asociadas = obtener_respuestas_asociadas(red, *estimulos)
    estimulos_y_respuestas = respuestas_asociadas + list(estimulos)
    red_filtrada = red.subgraph(estimulos_y_respuestas).copy()
    return red_filtrada


def proyectar_red_por_estimulos(red, *estimulos):
    """Proyecta la red para quedarse con las palabras respuesta asociadas a los estímulos indicados

    Parameters
    ----------
    red : networkx.Graph
    *estimulos : tuple
        Estímulos para los que se quiere obtener la proyección.

    Returns
    -------
    networkx.Graph
        Una nueva red con las palabras respuesta asociadas a los estímulos indicados.

    Examples
    --------
    >>> red_individual = proyectar_red_por_estimulos(red, 'covid_semilla')
    >>> red_par = proyectar_red_por_estimulos(red, 'covid_semilla', 'obesidad_semilla')
    >>> red_trio = proyectar_red_por_estimulos(red, 'covid_semilla', 'obesidad_semilla', 'dieta_semilla')
    """
    respuestas_asociadas = obtener_respuestas_asociadas(red, *estimulos)
    red_filtrada = filtrar_red_por_estimulos(red, *estimulos)
    proyeccion = nx.bipartite.projected_graph(red_filtrada, respuestas_asociadas)
    return proyeccion
