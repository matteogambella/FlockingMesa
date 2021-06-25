from model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import config


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.8}
    return portrayal

grid = CanvasGrid(agent_portrayal, config.map_size, config.map_size, 500, 500)
server = ModularServer(FlockingModel,
                       [grid],
                       "Flocking Model",
                       {"N":config.birds, "width":config.map_size, "height":config.map_size})
server.port = 8521 # The default
server.launch()