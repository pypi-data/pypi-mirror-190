from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD

class BayesModel:

    '''
    Clase que representa el modelo bayesiano
    Recibe como parámetro un diccionario con los parámetros del modelo
        - ['nodos']
        - ['edge'] donde en la posicion 0 se encuentra el nodo padre y en la posicion 1 el nodo hijo
        - ['probabilidad'] donde en la posicion 0 se encuentra el nodo y en la posicion 1 un array de las probabilidades
    '''
    def __init__(self, parameters):
        self.parameters = parameters
        self.model = BayesianModel()
        self.inference = None
    

    '''
    Construye el modelo bayesiano a partir de los parámetros recibidos en el constructor
    '''
    def build_model(self):
        for nodos in self.parameters['nodos']:
            self.model.add_node(nodos)
        
        for edge in self.parameters['edge']:
            self.model.add_edge(edge[0], edge[1])

        
        for probabilidad in self.parameters['probabilidad']: 

            temp_cpd = TabularCPD(probabilidad[0], 2,  values = probabilidad[1], evidence=probabilidad[2], evidence_card=probabilidad[3])
            self.model.add_cpds(temp_cpd)

        self.inference = VariableElimination(self.model)
        
    def enumeracion(self, variables, evidence):
        en = self.inference.query(variables=variables, evidence=evidence)
        print(en)
        return en.values
    
    def obtener_factores(self):
        return self.model.get_independencies()

    def representacion_compacta(self):
        cpd_string = ""
        for cpd in self.model.get_cpds():
            cpd_string += str(cpd) 

        return cpd_string

    def completamente_descrita(self):
        return self.model.check_model()

