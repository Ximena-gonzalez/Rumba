from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid, MultiGrid
from mesa.datacollection import DataCollector
import time    #libreria para extraer tiempo 
from agent import Aspiradora, Piso

class Rumba(Model):
    def __init__(self, height, width, porcentaje, N, tiempo_max):
        self.tiempo_max= tiempo_max
        self.start_time= time.time()
        self.num_agents = N
        self.grid = MultiGrid(width,height,torus = False) #torus= es tipo circulo (conectado derecha con izquierda)
        self.schedule = RandomActivation(self) #activa los agentes de forma aleatoria dentro del modelo
        self.running = True 

        for i in range(self.num_agents): #depende en num de agentes
            a = Aspiradora(i+1000, self) 
            self.schedule.add(a) #i+1000 para que no se repita el unique id. objeto aspiradora a con u_id i+1000. Crea objeto aspiradora y lo agrega al schedule del modelo
            pos = (1,1)
            self.grid.place_agent(a, pos)

        self.datacollector = DataCollector({
            "Celdas_limpias": lambda m: self.count_type(m, "Limpio")

        }
        )

        area_sucio= int(height * width * porcentaje)
        for i in range(area_sucio): 
            #crea objetos de tipo piso
            a = Piso(i+2000, self) 
            self.schedule.add(a)
            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            #pos dentro de alto y ancho (puede que sea repetido: piso sucio con sucio)
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                #genera posicion valida
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(a, pos)


        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)

        self.final_time= time.time() - self.start_time
        if(self.count_type(self, "Sucio") == 0 or self.final_time >= self.tiempo_max):
            self.running = False

    @staticmethod
    def count_type(model, piso_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for agente in model.schedule.agents:
            if(isinstance(agente, Piso)):
                if agente.condition == piso_condition:
                    count += 1
        return count

#recolectar datos