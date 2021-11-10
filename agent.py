from mesa import Agent

class Piso(Agent):
    def __init__(self, pos, model, estado_inicial="Sucio"):

        super().__init__(pos, model)
        self.pos = pos
        self.condition = estado_inicial

class Aspiradora(Agent):

    def __init__(self, model, id):

        super().__init__(model, id)
        self.direction = 4

    def move(self):
        """determina si la aspiradora se puede mover
        se mueve si no hay otra aspiradora"""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,  # se pueden diagonales
            include_center=True)  # se puede quedar en el centro (saltar en su mismo lugar)

        if(len(possible_steps) <= self.direction):
            pass
        else:
            self.model.grid.move_agent(self, possible_steps[self.direction])

    def step(self):
        """ 
        determina la nueva direccion
        """
        #regresa lista de cntenidos en esa posicion
        #primer elemento == piso? si es piso revisa su edo y de ahi cambia o mueve
        if(isinstance(self.model.grid[self.pos][0], Piso)):
            if (self.model.grid[self.pos][0].condition=="Sucio"):
                self.model.grid[self.pos][0].condition = " Limpio"
            else:
                self.direction = self.random.randint(0, 8)
                self.move()
                
        else:
            self.direction = self.random.randint(0, 8)
            self.move()

    #checar celda en la que esta, buscar estado de piso y en base a eso limpiar o no. una vez limpio espera una vuelta para ver a donde se mueve. 
    """
    def limpiar(self):
        if(Piso.condition == "Sucio"):
            Piso.condition = " Limpio"
            """




