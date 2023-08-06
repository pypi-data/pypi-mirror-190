# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fcaBayesian']

package_data = \
{'': ['*']}

install_requires = \
['pgmpy>=0.1.15,<0.2.0']

entry_points = \
{'console_scripts': ['fcaBayesian = fcaBayesian:main']}

setup_kwargs = {
    'name': 'fcabayesian',
    'version': '0.0.4',
    'description': '',
    'long_description': "# Laboratorio 2 - Inteligencia Artificial\n\nEste laboratorio es una implementacion de las redes bayesianas en python. La librerí, con nombre fcaBayesian utiliza \nla libería de pgmpy para poder hacer todos los análisis de las redes bayesianas.\n\n\nLos métodos que se encuentran en esta librería son:\n\n- `build_model()`: utiliza los valores obtenidos en los parametros del constructor y crea el modelo de la red bayesiana.\n\n- `enumeracion(variables, evidence)`:  obtiene la variable de forma ['variable'] y la evidencia de la forma {'variable_de_evidencia': evidencia}.\n\n    Un ejemplo de esta llamada es: `bayes.enumeracion(['R'], {'M': 1,})` siendo bayes una instancia de la red bayesiana.\n\n    El valor de retorno es un array con los valores resultantes del metodo de pgmpy `self.inference.query(variables=variables, evidence=evidence)`\n           \n```python\n+------+----------+\n| R    |   phi(R) |\n+======+==========+\n| R(0) |   0.2131 | -> El primer valor en el arreglo del return\n+------+----------+\n| R(1) |   0.7869 | -> El segundo valor en el arreglo del return\n+------+----------+\n```\n\n- `obtener_factores`: obtine las dependencias independientes del modelo bayesiano utiliza la funcion get_independecies del objeto model\n\n\n```python\n(U ⟂ M, B)\n(U ⟂ B | M)\n(U ⟂ M | B)\n(U ⟂ S | B, R)\n(U ⟂ S | M, B, R)\n(M ⟂ U, B)\n(M ⟂ B | U)\n(M ⟂ U | B)\n(M ⟂ S | B, R)\n(M ⟂ S | U, B, R)\n(S ⟂ U, M | B, R)\n(S ⟂ M | U, B, R)\n(S ⟂ U | M, B, R)\n(B ⟂ U, M)\n(B ⟂ M | U)\n(B ⟂ U | M) \n```\n    \n\n- `representacion_compacta`: utiliza la funcion de la libreria pgmpy `get_cpds()` para obtener todos los cpds y los escribe en un string que lo regresa de la siguiente manera: \n\n```python\n+------+------+\n| M(0) | 0.95 |\n+------+------+\n| M(1) | 0.05 |\n+------+------++------+------+\n| U(0) | 0.85 |\n+------+------+\n| U(1) | 0.15 |\n+------+------++------+-----+\n| B(0) | 0.9 |\n+------+-----+\n| B(1) | 0.1 |\n+------+-----++------+------+------+------+------+\n| R    | R(0) | R(0) | R(1) | R(1) |\n+------+------+------+------+------+\n| B    | B(0) | B(1) | B(0) | B(1) |\n+------+------+------+------+------+\n| S(0) | 0.98 | 0.88 | 0.95 | 0.6  |\n+------+------+------+------+------+\n| S(1) | 0.02 | 0.12 | 0.05 | 0.4  |\n+------+------+------+------+------++------+------+------+------+------+------+------+------+------+\n| M    | M(0) | M(0) | M(0) | M(0) | M(1) | M(1) | M(1) | M(1) |\n+------+------+------+------+------+------+------+------+------+\n| B    | B(0) | B(0) | B(1) | B(1) | B(0) | B(0) | B(1) | B(1) |\n+------+------+------+------+------+------+------+------+------+\n| U    | U(0) | U(1) | U(0) | U(1) | U(0) | U(1) | U(0) | U(1) |\n+------+------+------+------+------+------+------+------+------+\n| R(0) | 0.96 | 0.86 | 0.94 | 0.82 | 0.24 | 0.15 | 0.1  | 0.05 |\n+------+------+------+------+------+------+------+------+------+\n| R(1) | 0.04 | 0.14 | 0.06 | 0.18 | 0.76 | 0.85 | 0.9  | 0.95 |\n+------+------+------+------+------+------+------+------+------+\n```\n\n- `completamente_descrita`: Esta funcion devuelve el resultado booleano (true/false) de la comprobacion de si el modelo esta correctamente definido. Utiliza la funcion de pgmpy `check_model()`.\n\n\n\nPara crear una instancia del modelo bayesiano se debe de crear un diccionario de la siguiente forma: \n\n```python\n{\n    'nodos' : ...\n    'edge' : ...\n    'probabilidad' : [[nodo, [probabilidades], [evidencia], [evidence_card]]]\n}\n```\n\nUn ejemplo de esta implementación es lo siguiente:\n```python\nparametros = {\n    'nodos': ['M', 'U', 'R', 'B', 'S'],\n    'edge': [['M','R'], ['U','R'], ['B','R'], ['B','S'], ['R','S']],\n    'probabilidad':     [['M', [[0.95], [0.05]],[], []], ['U', [[0.85], [0.15]],[], []], ['B', [[0.90], [0.10]],[], []], ['S', [[0.98, .88, .95, .6], [.02, .12, .05, .40]],['R','B'], [2,2]],\n        ['R', [[0.96, .86, .94, .82, .24, .15, .10, .05], [.04, .14, .06, .18, .76, .85, .90, .95]],['M','B', 'U'], [2,2,2]]],\n\n}\n\n```\n\nLuego ese diccionario se envia como parametro a la funcion `BayesModel` de la siguiente manera: ```bayes = fca.BayesModel(parametros)```. Luego de esto se puede hacer uso de las funciones explicadas anteriormente.\n",
    'author': 'JuanDiegoAvila',
    'author_email': 'avi20090@uvg.edu.gt',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
