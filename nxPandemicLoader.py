import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def getNNposition(alpha, beta, gama, init_dist=0, abDist=20, bgDist=50, vertical_dist=10):
    pos_dict = {}
    bgDist += abDist
    ap = 1
    bp = 1
    gp = 1
    mid_alpha = len(alpha)*vertical_dist/2
    nodeAmplitude = abDist/10
    for i in range(len(alpha)):
        pos_dict[alpha[i]] = (init_dist+1, i*vertical_dist - mid_alpha)#np.random.randint(0,10)*ap
        ap *= -1

    nodeAmplitude = bgDist/3
    mid_beta = len(beta)*vertical_dist/2
    for i in range(len(beta)):
        pos_dict[beta[i]] = (init_dist+abDist+1, i*vertical_dist - mid_beta)#np.random.randint(0,10)*bp
        bp *= -1

    nodeAmplitude = (abDist+bgDist)/6
    mid_gama = len(gama)*vertical_dist/2
    for i in range(len(gama)):
        pos_dict[gama[i]] = (init_dist+bgDist+np.random.randint(0,10)*gp, i*vertical_dist - mid_gama)
        gp *= -1

    return pos_dict

def getNNPositionWithMultipleTimeStamp(timeWiseABG={}):
    combined_pos_dict = {}
    init_dist = 0
    for time in timeWiseABG.keys():
        alpha_nodes, beta_nodes, gama_nodes = timeWiseABG.get(time)
        combined_pos_dict.update(getNNposition(alpha_nodes, beta_nodes, gama_nodes,init_dist))
        init_dist += 200
    return combined_pos_dict


def getRandomCircularPos(alpha, beta, gama, other, abDist=30, bgDist=30, goDist = 30, vertical_dist=10):
    pos_dict = {}
    pos_dict.update(getCircularPos(alpha, 30, 0))
    pos_dict.update(getCircularPos(beta, 50, abDist+50))
    pos_dict.update(getCircularPos(gama, 80, bgDist+80))
    pos_dict.update(getCircularPos(other, 100, goDist+100))
    return pos_dict


def getCircularPos(array, rad, layerDistance):
    temp_pos_dict = {}
    for i in range(len(array)):
        theta = 2*i*np.pi/len(array)
        temp_pos_dict[array[i]] = (layerDistance+rad*np.cos(theta), rad*np.sin(theta))

    return temp_pos_dict

def generatePosDictForNNodes(no_of_nodes):
    #pos = nx.spring_layout(G)  # positions for all nodes
    pos = {(i+1): np.random.random_integers(0,30,(2)) for i in range(no_of_nodes)}
    return pos

def drawAlphaNodes(G, pos, nodeList):
    nx.draw_networkx_nodes(G, pos,nodelist=nodeList,node_color='r',node_size=800,alpha=0.8)

def drawBetaNodes(G, pos, nodeList):
    nx.draw_networkx_nodes(G, pos,nodelist=nodeList,node_color='orange',node_size=500,alpha=0.8)

def drawGamaNodes(G, pos, nodeList):
    nx.draw_networkx_nodes(G, pos,nodelist=nodeList,node_color='y',node_size=300,alpha=0.8)


def addAlphaEdges(G, pos, listOfPair):
    #nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(G, pos,
                           edgelist=listOfPair,
                           width=5, alpha=0.5, edge_color='r')

def addBetaEdges(G, pos, listOfPair):
    # nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(G, pos,
                           edgelist=listOfPair,
                           width=4, alpha=0.5, edge_color='orange')

def addGamaEdges(G, pos, listOfPair):
    # nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(G, pos,
                           edgelist=listOfPair,
                           width=3, alpha=0.5, edge_color='y')

def addOtherEdges(G, pos, listOfPair):
    # nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(G, pos,
                           edgelist=listOfPair,
                           width=2, alpha=0.5, edge_color='g')

def drawNetworkxGraph(ALPHA_NODES, BETA_NODES, GAMA_NODES, OTHER_NODES=[], DB_PATH='files/PandemicSpread.db',TABLE_NAME='UserInfo'):
    G = nx.Graph()
    pos = getNNposition(ALPHA_NODES, BETA_NODES, GAMA_NODES, OTHER_NODES)
    drawAlphaNodes(G, pos, ALPHA_NODES)
    drawBetaNodes(G, pos, BETA_NODES)
    drawGamaNodes(G, pos, GAMA_NODES)

    labels = load_labels(DB_path=DB_PATH, table_name=TABLE_NAME)
    nx.draw_networkx_labels(G, pos=pos, labels=labels)
    plt.axis('off')
    plt.show()

# some math labels
import sqlite3

def load_labels(DB_path, table_name):
    conn = sqlite3.connect(DB_path)
    op = conn.execute('select * from '+str(table_name))
    labels = {}
    for id, name in op:
        labels[id] = name
    return labels


def loadLabelDict(ALPHA_NODES, BETA_NODES, GAMA_NODES):
    labels_DICT = load_labels('files/PandemicSpread.db', 'UserInfo')
    labels = {}
    index = 1
    for node in ALPHA_NODES:
        id_time = node.split('_')
        labels.update({index: labels_DICT.get(id_time[0])+'_'+id_time[1]})
        index += 1

    for node in BETA_NODES:
        id_time = node.split('_')
        labels.update({index: labels_DICT.get(id_time[0])+'_'+id_time[1]})
        index += 1

    for node in GAMA_NODES:
        id_time = node.split('_')
        labels.update({index: labels_DICT.get(id_time[0])+'_'+id_time[1]})
        index += 1

    return labels

def getAlphaBetaGamaNodes(timeWiseABG={}):
    alpha_nodes = []
    beta_nodes = []
    gama_nodes = []
    for time in timeWiseABG.keys():
        alpha, beta, gama = timeWiseABG.get(time)
        for node in alpha:
            if node not in alpha_nodes:
                alpha_nodes.append(node)

        for node in beta:
            if node not in beta_nodes:
                beta_nodes.append(node)

        for node in gama:
            if node not in gama_nodes:
                gama_nodes.append(node)

    beta_nodes = list(set(beta_nodes)-set(alpha_nodes))
    gama_nodes = list(set(gama_nodes)-set(beta_nodes)-set(alpha_nodes))
    return alpha_nodes, beta_nodes, gama_nodes

def RemoveOverlappingEdges(betaEdges, gamaEdges, alpha_nodes, beta_nodes, gama_nodes):
    beta_remove_index = []
    gama_remove_index = []

    '''
    for i in range(len(betaEdges)):
        node1 = betaEdges[i][0]
        node2 = betaEdges[i][1]
        if node1 in alpha_nodes or node2 in alpha_nodes:
            beta_remove_index.append(i)

    new_betaEdges = []
    for i in range(len(betaEdges)):
        if i not in beta_remove_index:
            new_betaEdges.append(betaEdges[i])
    '''

    for i in range(len(gamaEdges)):
        node1 = gamaEdges[i][0]
        node2 = gamaEdges[i][1]
        if node1 in alpha_nodes or node2 in alpha_nodes:
            gama_remove_index.append(i)
    new_gamaEdges = []

    for i in range(len(gamaEdges)):
        if i not in gama_remove_index:
            new_gamaEdges.append(gamaEdges[i])

    return betaEdges, new_gamaEdges
