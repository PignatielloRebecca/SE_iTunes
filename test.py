
from model.model import  Model
from database.dao import DAO
import networkx as nx

m=Model()

print(m._build_graph(120))