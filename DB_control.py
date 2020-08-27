import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('files/Pandamic_Spreadold.db')

def getTableNameFromId(conn, id):
    querry = 'select NAME from UserInfo where ID = '+str(id)+';'
    #print('Table Name querry:',querry, end='\t')
    for name in conn.execute(querry):
        #print('Name: ',name[0])
        return str(name[0])

def getGamaNodesEdges(conn, alphaNodes, betaNodes, timeStamp):
    gamaNodes = []
    gamaEdges = []
    for betaNode in betaNodes:
        betaTable = getTableNameFromId(conn, betaNode)
        querry = 'select deviceID, timestamp from ' + betaTable +' where timestamp = ' + str(timeStamp) + ';'
        
        for gamaNode, time in conn.execute(querry):
            gamaNode = int(gamaNode)
            if gamaNode not in betaNodes or gamaNode not in alphaNodes:
                gamaNodes.append(gamaNode)
                gamaEdges.append((betaNode, gamaNode))
    return gamaNodes, gamaEdges

def getBetaGamaNodes(conn, alphanodes, timeStamp):
    betaNodes = []
    betaEdges = []
    alphaTable = getTableNameFromId(conn, alphanodes[0])
    querry = 'select deviceID from '+alphaTable+' where timestamp = '+timeStamp+';'
    #print('beta querry:',querry)
    for betaNode in conn.execute(querry):
        #print('Node:',betaNode[0])
        betaNodes.append(int(betaNode[0]))
    for node in betaNodes:
        betaEdges.append((alphanodes[0], int(node)))
    gamaNodes, gamaEdges = getGamaNodesEdges(conn, alphanodes, betaNodes, timeStamp)
    return betaNodes, betaEdges, gamaNodes, gamaEdges

def getTimeToString(timeStamp):
    timeObj = datetime.strptime(timeStamp, '%d%m%Y%H%M')
    return str(timeObj.strftime('%d/%m/%Y - %H:%M'))

def getIndex(node, alphaNode=[], betaNode=[], gamaNode=[]):
    if node in alphaNode:
        return alphaNode.index(node)
    elif node in betaNode:
        return len(alphaNode)+betaNode.index(node)
    else:
        return len(alphaNode)+len(betaNode)+gamaNode.index(node)

def getConvertedNodesOfTimeT(conn,alphaNodes, betaNodes, gamaNodes, betaEdges, gamaEdges, timestamp):
    if betaNodes == [] and gamaNodes == []:
        return [], [], [], [], []
    LIST = []
    new_alpha_nodes = []
    new_beta_nodes = []
    new_gama_nodes = []
    time = getTimeToString(timestamp)
    for node in alphaNodes:
        name = getTableNameFromId(conn, node)
        new_alpha_nodes.append(str(name) + '_' + time)
        LIST.append(str(name) + '_' + time)
    for node in betaNodes:
        name = getTableNameFromId(conn, node)
        new_beta_nodes.append(str(name) + '_' + time)
        LIST.append(str(name) + '_' + time)
    for node in gamaNodes:
        name = getTableNameFromId(conn, node)
        new_gama_nodes.append(str(name) + '_' + time)
        LIST.append(str(name) + '_' + time)
    newBetaEdges = []
    newGamaEdges = []



    for node1, node2 in betaEdges:
        newBetaEdges.append((LIST[0], LIST[getIndex(node2, alphaNodes, betaNodes)]))
    for node1, node2 in gamaEdges:
        newGamaEdges.append((LIST[getIndex(node1, alphaNodes, betaNodes)], LIST[getIndex(node2, alphaNodes, betaNodes, gamaNodes)]))
    return new_alpha_nodes, new_beta_nodes, new_gama_nodes, newBetaEdges, newGamaEdges

def getAllNodesOfT(conn, node_id, timeStamp):
    alphaNodes = [node_id]
    betaNodes, betaEdges, gamaNodes, gamaEdges = getBetaGamaNodes(conn,alphaNodes, timeStamp)
    #print('InBetween-Final:\nalphaNodes:', alphaNodes, '\nbetaNodes:', betaNodes, '\ngamaNodes:', gamaNodes,
    #            '\nbetaEdges:', betaEdges,'\ngamaEdges:', gamaEdges)
    alphaNodes, betaNodes, gamaNodes, betaEdges, gamaEdges = getConvertedNodesOfTimeT(conn,
                                                                                      alphaNodes,
                                                                                      betaNodes,
                                                                                      gamaNodes,
                                                                                      betaEdges,
                                                                                      gamaEdges,
                                                                                      timeStamp)
    #print('time:',timeStamp,'node list:',node_list)
    #print('InBetween-Final:\nalphaNodes:',alphaNodes,'\nbetaNodes:', betaNodes,'\ngamaNodes:', gamaNodes,
    #      '\nbetaEdges:', betaEdges,'\ngamaEdges:', gamaEdges)
    return alphaNodes, betaNodes, gamaNodes, betaEdges, gamaEdges

def getPrevTimeStamp(timeStamp, prev):
    timeObj = datetime.strptime(timeStamp,'%d%m%Y%H%M') - timedelta(minutes=prev*5)
    return timeObj.strftime('%d%m%Y%H%M')

def getNodeDict(alphaNodes, betaNodes, gamaNodes):
    DICT = {}
    for node in alphaNodes:
        DICT.update({node: node})
    for node in betaNodes:
        DICT.update({node: node})
    for node in gamaNodes:
        DICT.update({node: node})
    return DICT

def getAllNodes(conn, node_id, timeStamp, period):
    timeList = [getPrevTimeStamp(timeStamp, period - (i+1)) for i in range(period)]
    Alpha = []
    Beta = []
    Gama = []
    BetaEdges = []
    GamaEdges = []
    for time in timeList:
        #print('Timestamp: ',time,'node:',node_id,'period:',period)
        alphaNodes, betaNodes, gamaNodes, betaEdges, gamaEdges = getAllNodesOfT(conn, node_id, time)
        Alpha += alphaNodes
        Beta += betaNodes
        Gama += gamaNodes
        BetaEdges += betaEdges
        GamaEdges += gamaEdges
    AlphaEdges = [(Alpha[i-1], Alpha[i]) for i in range(1,len(Alpha))]
    NodeDict = getNodeDict(Alpha, Beta, Gama)
    return Alpha, Beta, Gama, AlphaEdges, BetaEdges, GamaEdges, NodeDict

Alpha, Beta, Gama, AlphaEdges, BetaEdges, GamaEdges, NodeDict = getAllNodes(conn, 1, '020120200910',5000)

print('Alpha:',Alpha)
print('Beta:',Beta)
print('Gama:',Gama)
print('alphaEdges:',AlphaEdges)
print('betaEdges:',BetaEdges)
print('gamaEdges:',GamaEdges)

import networkx as nx
from nxPandemicLoader import *

G = nx.Graph()
pos = getNNposition(Alpha,Beta,Gama)
drawAlphaNodes(G, pos, Alpha)
drawBetaNodes(G, pos, Beta)
drawGamaNodes(G, pos, Gama)

addAlphaEdges(G, pos, AlphaEdges)
addBetaEdges(G, pos, BetaEdges)
addGamaEdges(G, pos, GamaEdges)


nx.draw_networkx_labels(G, pos, NodeDict)
plt.axis('off')
plt.xlim((-30,100))
plt.show()
