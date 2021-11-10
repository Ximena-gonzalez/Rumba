from mesa.space import Grid
from agent import Aspiradora, Piso
from model import Rumba
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

def portrayalRumba(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent, Piso)):
        if(agent.condition=="Sucio"):
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 1
            portrayal["r"] = 0.2
        else:
            portrayal["Color"] = "purple"
            portrayal["Layer"] = 1
            portrayal["r"] = 0.2 
        
    return portrayal

model_params = {"N":UserSettableParameter("slider", "Rumba: ",1 ,1 ,5 ,1), "width":10, "height":10, "porcentaje":UserSettableParameter("slider", "Porcentaje: ", 0.1, 0.1, 1, 0.1), "tiempo_max":UserSettableParameter("slider", "Tiempo max: ", 30, 10, 50, 5)} #slider, checkbox, num? slider funciona para todo
#hacer canvas element (entre corchetes edpues de rumba)= objeto que aparece en la pag y deja ver la simulacion
canvas_element = CanvasGrid(portrayalRumba, 10, 10, 500, 500) #cuando crear server pasas canvas element, pudes tener mas de uno
server = ModularServer(Rumba, [canvas_element], "Rumba", model_params)

server.launch()