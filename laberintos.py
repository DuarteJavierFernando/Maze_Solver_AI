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


#def transition_model(node,action):


class Maze:
    def __init__(self,file):
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




class Node:
    def __init__(self,state,parent):
        self.state = state
        self.parent = parent
        self.possible_actions = set()

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


m=Maze("laberinto.txt")
print(m.bool_map())



n= Node((3,4),None)

print(n.possible_actions)