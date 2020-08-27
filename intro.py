from DB_control import *
from nxPandemicLoader import *
import sqlite3

DB = 'Pandamic_Spreadnew.db'
conn = sqlite3.connect(DB)

timeWiseABG, betaEdges, gamaEdges, node_dict = getAllNodes(conn,node_id=3,timeStamp=4,period=4)

print('-----------------OUTPUT---------------')
print('Time Wise ABG:',timeWiseABG)
print('BETA_EDGES:',betaEdges)
print('GAMA_EDGES:',gamaEdges)
print('Node dict:', node_dict)
print('------------------------------------------')


G = nx.Graph()
pos = getNNPositionWithMultipleTimeStamp(timeWiseABG)
print(pos)
alpha_nodes, beta_nodes, gama_nodes = getAlphaBetaGamaNodes(timeWiseABG)
print(alpha_nodes)
print(beta_nodes)
print(gama_nodes)
drawAlphaNodes(G, pos, alpha_nodes)
drawBetaNodes(G, pos, beta_nodes)
drawGamaNodes(G, pos, gama_nodes)

alphaEdges = [(alpha_nodes[i-1], alpha_nodes[i]) for i in range(1,len(alpha_nodes))]
betaEdges, gamaEdges = RemoveOverlappingEdges(betaEdges, gamaEdges, alpha_nodes, beta_nodes, gama_nodes)
addAlphaEdges(G, pos, alphaEdges)
addBetaEdges(G, pos, betaEdges)
addGamaEdges(G, pos, gamaEdges)

print(betaEdges)



nx.draw_networkx_labels(G, pos, node_dict)
plt.axis('off')
plt.show()




