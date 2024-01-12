def maze_builder_func(filename):
    # MAZE BUILDER
    maze_file = open(file=filename, mode="r")
    cont = maze_file.read()
    lines = cont.splitlines()

    mapped_lab = []
    for i, line in enumerate(lines):
        mapped_lab_row = []
        for j, charact in enumerate(line):
            dic = dict()
            if charact == " ":
                dic[(i, j)] = True
                mapped_lab_row.append(dic)

            elif charact == "A":
                dic[(i, j)] = True
                mapped_lab_row.append(dic)
                coord_init_state = (i, j)
            elif charact == "B":
                dic[(i, j)] = True
                mapped_lab_row.append(dic)
                coord_fin_state = (i, j)
            else:
                dic[(i, j)] = False
                mapped_lab_row.append(dic)
        mapped_lab.append(mapped_lab_row)
    maze_file.close()
    return mapped_lab, coord_init_state, coord_fin_state



def expand_node(node,explorados):

    node_state = node.state
    new_nodes = []
    for action in node.possible_actions:
        if action == "UP" :
            new_state = (node.state[0]-1,node.state[1])
            new_node = Node(new_state,node,action)
            if not explorados.is_in_explored(new_node):
                new_nodes.append(new_node)
        if action == "DOWN":
            new_state = (node.state[0]+1,node.state[1])
            new_node = Node(new_state,node,action)
            if not explorados.is_in_explored(new_node):
                new_nodes.append(new_node)
        if action == "LEFT":
            new_state = (node.state[0],node.state[1]-1)
            new_node = Node(new_state,node,action)
            if not explorados.is_in_explored(new_node):
                new_nodes.append(new_node)
        if action == "RIGHT":
            new_state = (node.state[0],node.state[1]+1)
            new_node = Node(new_state,node,action)
            if not explorados.is_in_explored(new_node):
                new_nodes.append(new_node)
    return new_nodes

#def transition_model(node,action):


class Maze:
    def __init__(self,file):
        self.solution = None
        self.mapped_maze,self.initial_coord,self.end_coord=maze_builder_func(file)
        self.dimensions=(len(self.mapped_maze), len(self.mapped_maze[0]))

    def bool_map(self):
        map=[]
        for row in self.mapped_maze:
            map_r=[]
            for col in row:
                map_r.append(int(list(col.values())[0]))
            map.append(map_r)
        return map
    def is_a_wall(self,coord_x,coord_y):
        try:
            valor = not bool(self.bool_map()[coord_x][coord_y])
            return valor
        except IndexError:
            return True
    def is_solution(self,node):
        if node.state == self.end_coord:
            return True
        else:
            return False
    def maze_solver(self,node):
        n_list = []
        n_list.append(node)
        frontier = Frontier()
        frontier.add_node(n_list)
        explored = Explored_set()
        while frontier.frontier:
            if frontier.is_empty():
                raise Exception("no solution")

            new_node = frontier.pick_node()

            #check if node is solution
            if self.is_solution(new_node):
                actions = []
                cells = []
                while new_node.parent is not None:
                    actions.append(new_node.prev_action)
                    cells.append(new_node.state)
                    new_node = new_node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                print("The problem has a solution!")
                return

            explored.add_to_explored(new_node)

            new_nodes= expand_node(new_node,explored)
            frontier.add_node(new_nodes)

         # Check the value of x and act accordingly
        if self.solution is None:
            raise ValueError("No solution found.")




class Node:
    def __init__(self,state,parent,prev_action):
        self.state = state
        self.parent = parent
        self.possible_actions = set()
        self.prev_action = prev_action

        #Append "UP" action
        if not ((self.state[0]==0) or m.is_a_wall(self.state[0]-1,self.state[1]) ):
            self.possible_actions.add("UP")
        # Append "DOWN" action
        if not ((self.state[0]==m.dimensions[0]) or m.is_a_wall(self.state[0]+1,self.state[1]) ):
            self.possible_actions.add("DOWN")
        # Append "LEFT" action
        if not ((self.state[1]==0) or m.is_a_wall(self.state[0],self.state[1]-1) ):
            self.possible_actions.add("LEFT")
        # Append "RIGHT" action
        if not ((self.state[1]==m.dimensions[1]) or m.is_a_wall(self.state[0],self.state[1]+1) ):
            self.possible_actions.add("RIGHT")


class Frontier:
    def __init__(self):
        self.frontier = []

    def is_empty(self):
        return self.frontier == 0
    def add_node(self,nodes):
        self.frontier.extend(nodes)

    def pick_node(self):
        # this is for dept-first search
        try:
            node= self.frontier.pop()
            return node
        except IndexError:
            raise Exception("Frontier is empty. No more nodes to explore.")


class Explored_set:
    def __init__(self):
        self.explored = set()

    def add_to_explored(self,node):
        self.explored.add(node.state)

    def is_in_explored(self,node):
        return node.state in self.explored



# Main Program
m=Maze("laberinto2.txt")
initial_state = m.initial_coord

#initial node
n= Node((initial_state[0],initial_state[1]),None,None)


m.maze_solver(n)

sol_path =[m.initial_coord]+ m.solution[1]



import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def plot_maze(maze, path,start,end):
    # Create a 2D array to represent the maze
    maze_array = np.zeros((len(maze), len(maze[0])))
    cmap = LinearSegmentedColormap.from_list('custom_gray', ['#f0f0f0', '#404040'], N=256)

    # Set values for walls, path, and empty cells
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if not maze[i][j][(i,j)]:
                maze_array[i, j] = 0.5  # Wall (gray)
            else:
                maze_array[i, j] = 0.2  # Empty cell (white)

#    for i in range(len(maze)):
#        for j in range(len(maze[i])):
#            if (i, j) in path:
#                maze_array[i, j] = 2  # Path (yellow)
    # Plot the maze
    plt.imshow(maze_array, cmap=cmap, interpolation='nearest')
    path_x, path_y = zip(*path)
    plt.plot(path_y, path_x, color='red', linewidth=2)

    # Customize the plot
    plt.xticks(np.arange(len(maze[0]))-0.5, range(len(maze[0])))
    plt.yticks(np.arange(len(maze)-0.5), range(len(maze)))
    plt.grid(color='yellow', linestyle='--', linewidth=2)
    plt.axis('off')  # Turn off the axis

    # Add labels "A" and "B" at initial and end positions
    plt.text(start[1] ,  start[0]-0.2, 'A', color='green', ha='center', va='center', fontsize=15,
             fontweight='bold')
    plt.text(end[1] ,  end[0]-0.2 , 'B', color='green', ha='center', va='center', fontsize=15,
             fontweight='bold')

    plt.show()




plot_maze(m.mapped_maze,sol_path,m.initial_coord,m.end_coord )




