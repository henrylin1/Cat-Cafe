import obstacles

class Node:
    def __init__(self, location, cost, heuristic, previous):  #tuple, number, node or None
        self.location = location
        self.cost = cost
        self.heuristic = heuristic
        self.previous = previous
        
    def __repr__(self):
        return "Node"+str(self.location)+"cost:"+str(self.cost)
        
    def __eq__(self, other):
        if isinstance(other,Node) and self.location==other.location:
            return True
        return False
        
def getManhattan(location,target):
    return abs(location[0]-target[0]) + abs(location[1]-target[1])
    
def getNext(board, locationNode, targetNode): #find neighboring nodes
    x,y = locationNode.location
    nextMoves = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    rightMoves = []
    for move in nextMoves:
        if move[0] >= 0 and move[0] < len(board):
            if move[1] >= 0 and move[1] < len(board[0]):
                if board[move[1]][move[0]] == 0 or isinstance(board[move[1]][move[0]],obstacles.Chair):
                    newCost = locationNode.cost + 1 
                    newHeuristic = getManhattan(move,targetNode.location)
                    newNode = Node(move,newCost,newHeuristic,locationNode)
                    rightMoves += [newNode]
    return rightMoves
    
def getPriority(edge):  #find which node to check based on lowest cost
    bestNode = None
    edge.reverse()
    for node in edge:
        priority = node.cost + node.heuristic
        if bestNode == None or priority < bestNode.cost + bestNode.heuristic:
            bestNode = node
    return bestNode
    

def findPath(board, start, target):
    startNode = Node(start, 0, getManhattan(start,target), None)
    targetNode = Node(target,0,0,None)    #cost and previous is unknown, and irrelevant for now
    edge = [startNode]                  #just need for base case
    checked = []
    
    def recursive(board, targetNode, edge, checked):
        if targetNode in edge:
            return edge[edge.index(targetNode)]
        if len(edge) == 0:
            return False

        else:       #expand frontier
            checkingNode = getPriority(edge)
            checked += [checkingNode]
            nextNodes = getNext(board, checkingNode, targetNode)
            
            for next in nextNodes:  #updates checked region with frontier
                if next not in checked:
                    edge += [next]
                else:
                    if next.cost < checked[checked.index(next)].cost:
                        checked[checked.index(next)] = next
                        edge += [next]
            edge.remove(checkingNode)   #do not check again, unless pops up as a neighbor
            return recursive(board,targetNode,edge,checked)
            
    node = recursive(board, targetNode, edge, checked)
    if node == False:
        return []
    path = []
    cont = True
    while cont:
        path += [node.location]
        node = node.previous
        if node == None:
            cont = False
    path.reverse()
    
    movement = []
    for index in range(1, len(path)):
        movement += [(path[index][0]-path[index-1][0],path[index][1]-path[index-1][1])]
    return movement

def findPathClose(board, start, target):
    startNode = Node(start, 0, getManhattan(start,target), None)
    targetNode = Node(target,0,0,None)    #cost and previous is unknown, and irrelevant for now
    edge = [startNode]                  #just need for base case
    checked = []
    
    def recursive(board, targetNode, edge, checked):
        for neighbor in getNext(board, targetNode, targetNode):
            if neighbor in edge:
                return edge[edge.index(neighbor)]

        else:       #expand frontier
            checkingNode = getPriority(edge)
            checked += [checkingNode]
            nextNodes = getNext(board, checkingNode, targetNode)
            
            for next in nextNodes:  #updates checked region with frontier
                if next not in checked:
                    edge += [next]
                else:
                    if next.cost < checked[checked.index(next)].cost:
                        checked[checked.index(next)] = next
                        edge += [next]
            edge.remove(checkingNode)   #do not check again, unless pops up as a neighbor
            return recursive(board,targetNode,edge,checked)
            
    node = recursive(board, targetNode, edge, checked)
    path = []
    cont = True
    while cont:
        path += [node.location]
        node = node.previous
        if node == None:
            cont = False
    path.reverse()
    
    movement = []
    for index in range(1, len(path)):
        movement += [(path[index][0]-path[index-1][0],path[index][1]-path[index-1][1])]
    return movement
    
def testFindPath():
    board = [[0,0,0,0,1,0,0],
             [1,1,1,0,1,0,0],
             [0,0,0,0,1,0,0],
             [0,1,1,1,1,0,0],
             [0,0,0,0,0,0,0],
             [0,0,1,1,1,0,0],
             [0,0,0,0,0,0,0]]
    
    location = (0,0)
    target = (6,0)
    path = findPath(board, location, target)
