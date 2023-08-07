import networkx as nx
import pandas as pd
import pytest

from redsem import api


@pytest.fixture(scope='module')
def df_prueba():
    datos = {'palabras': ['prueba', 'para', 'redes', 'semánticas'],
             'posicion': [1, 2, 3, 4]}
    return pd.DataFrame(datos)


@pytest.fixture(scope='module')
def red_prueba():
    palabras_estimulo = ['covid_semilla', 'obesidad_semilla']
    palabras_respuesta = ['salud', 'ansiedad', 'higiene', 'comida']
    aristas = [
        ('covid_semilla', 'salud'),
        ('covid_semilla', 'ansiedad'),
        ('covid_semilla', 'higiene'),
        ('obesidad_semilla', 'salud'),
        ('obesidad_semilla', 'ansiedad'),
        ('obesidad_semilla', 'comida')
    ]
    red = nx.Graph()
    red.add_edges_from(aristas)
    particion_bipartita = {palabra: 'estimulo' for palabra in palabras_estimulo}
    particion_bipartita |= {palabra: 'respuesta' for palabra in palabras_respuesta}
    nx.set_node_attributes(red, 'bipartita', particion_bipartita)
    return red


class TestFiltrado:
    @pytest.mark.parametrize("ultima", [1, 2, 3, 4])
    def test_filtrado_correcto(self, df_prueba, ultima):
        df_filtrado = main.filtrar_primeras_posiciones(df_prueba, ultima_posicion=ultima)
        assert df_filtrado['posicion'].max() <= ultima

    @pytest.mark.parametrize('df_falso', ['df_prueba', 5, 5.0, True])
    def test_sin_df(self, df_falso):
        with pytest.raises(TypeError):
            main.filtrar_primeras_posiciones(df_falso)

    def test_sin_columna_posicion(self, df_prueba):
        with pytest.raises(ValueError):
            main.filtrar_primeras_posiciones(df_prueba.drop('posicion', axis=1))
