from queue import PriorityQueue
import copy

#Here is the structure of nodes, containing the information of the state of current node,
#its parent node, the action from its parent to itself, its path cost and the f value.
class Node(): 
    def __init__(self,cur_state,par_node,action,path_cost,f_value):
        self.cur_state = cur_state
        self.par_node = par_node
        self.action = action
        self.path_cost = path_cost
        self.f_value = f_value
        
    #Here we define the comparison between two nodes for operations in the frontier.
    def __eq__(self, other):
        return (self.f_value == other.f_value)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self.f_value < other.f_value)

    def __gt__(self, other):
        return (self.f_value > other.f_value)

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)
    
class Project():
    def __init__(self,input_file):
        self.input_file = input_file
        self.input_state, self.goal_state = self.read_file()
        
        #Here we define the actions: 1 left, 2 up-left, 3 up, 4 up-right, 5 right, 6 down-right, 7 down and 8 down-left.
        self.actions = [1,2,3,4,5,6,7,8]
        
        #Here is the frontier (priority queue) for the A* Search.
        self.frontier = PriorityQueue()
        
        #Here is the list to store existing states and avoid repeated states.
        self.states = [self.input_state]
        
        #Here we get all the indices for tiles in the goal state matrix, to calculate the sum of chessboard distances.
        self.goal_index = self.get_goal_index()
        
        #Here we get the goal node from our search algorithm.
        self.result_node = self.search()
    
    #Here we read the input txt file to get the initial state and the goal state.
    def read_file(self):
        data = open(self.input_file,"r")
        input_list = []
        for line in data:
            input_list.append(line.strip())
        data.close()
        index0 = input_list.index("")
        assert index0 == 4
        input_board_raw = input_list[:index0]
        output_board_raw = input_list[index0+1:]
        
        assert len(input_board_raw) == len(output_board_raw)
        
        input_board, output_board = [], []
        for row in range(len(input_board_raw)):
            input_row_raw = input_board_raw[row]
            output_row_raw = output_board_raw[row]
            input_row = input_row_raw.split()
            output_row = output_row_raw.split()
            for e in range(len(input_row)):
                input_row[e] = int(input_row[e])
                output_row[e] = int(output_row[e])
            input_board.append(input_row)
            output_board.append(output_row)
        print("Start State:")
        print(input_board)
        print("Goal State:")
        print(output_board)
        return input_board, output_board
    
    #Given a state, we return its legal actions for its child nodes.
    def get_actions(self,cur_state):
        row_index, col_index = self.get_0_position(cur_state)

        if row_index == 0:
            if col_index == 0:
                return [5,6,7]
            if col_index == len(cur_state[0])-1:
                return [1,7,8]
            return [1,5,6,7,8]
        elif row_index == len(cur_state)-1:
            if col_index == 0:
                return [3,4,5]
            if col_index == len(cur_state[0])-1:
                return [1,2,3]
            return [1,2,3,4,5] 
        else:
            if col_index == 0:
                return [3,4,5,6,7]
            if col_index == len(cur_state[0])-1:
                return [1,2,3,7,8]
            return [1,2,3,4,5,6,7,8]
    
    #Here we get the position index of the 0 tile in the given state.
    def get_0_position(self,cur_state):
        for row_index in range(len(cur_state)):
            for col_index in range(len(cur_state[0])):
                tile = cur_state[row_index][col_index]
                if tile == 0:
                    return row_index, col_index
        raise Exception
    
    #Given a state and an action, we get the new state after the action.
    def result(self,cur_state,action):
        row_index, col_index = self.get_0_position(cur_state)
        next_state = copy.deepcopy(cur_state)
        if action == 1:
            next_state[row_index][col_index], next_state[row_index][col_index-1] = next_state[row_index][col_index-1], next_state[row_index][col_index]
        elif action == 2:
            next_state[row_index][col_index], next_state[row_index-1][col_index-1] = next_state[row_index-1][col_index-1], next_state[row_index][col_index]
        elif action == 3:
            next_state[row_index][col_index], next_state[row_index-1][col_index] = next_state[row_index-1][col_index], next_state[row_index][col_index]
        elif action == 4:
            next_state[row_index][col_index], next_state[row_index-1][col_index+1] = next_state[row_index-1][col_index+1], next_state[row_index][col_index]
        elif action == 5:
            next_state[row_index][col_index], next_state[row_index][col_index+1] = next_state[row_index][col_index+1], next_state[row_index][col_index]
        elif action == 6:
            next_state[row_index][col_index], next_state[row_index+1][col_index+1] = next_state[row_index+1][col_index+1], next_state[row_index][col_index]
        elif action == 7:
            next_state[row_index][col_index], next_state[row_index+1][col_index] = next_state[row_index+1][col_index], next_state[row_index][col_index]
        elif action == 8:
            next_state[row_index][col_index], next_state[row_index+1][col_index-1] = next_state[row_index+1][col_index-1], next_state[row_index][col_index]
        else:
            raise Exception
        return next_state
    
    #Here we get all the indices for tiles in the goal state matrix, to calculate the sum of chessboard distances.
    def get_goal_index(self):
        index_dict = dict()
        for row_index in range(len(self.goal_state)):
            for col_index in range(len(self.goal_state[0])):
                tile = self.goal_state[row_index][col_index]
                index_dict[tile] = (row_index,col_index)
        return index_dict
    
    #Here we compute the sum of chessboard distances between the current state and the goal state.
    def compute_h(self,cur_state):
        chessboard = 0
        for row_index in range(len(cur_state)):
            for col_index in range(len(cur_state[0])):
                tile = cur_state[row_index][col_index]
                if tile != 0:
                    hori = abs(col_index - self.goal_index[tile][1])
                    verti = abs(row_index - self.goal_index[tile][0])
                    chessboard += max(hori,verti)
        return chessboard
    
    #Given a node, we generate its child nodes after its legal actions.
    def expand(self,cur_node):
        cur_state = cur_node.cur_state
        for action in self.get_actions(cur_state):
            next_state = self.result(cur_state,action)
            cost = cur_node.path_cost + 1
            f = cost + self.compute_h(next_state)
            yield Node(next_state,cur_node,action,cost,f)
    
    #Here we check whether the state of current node is the goal state.
    def is_goal(self,cur_node):
        return cur_node.cur_state == self.goal_state
    
    #Here we operate the A* Search. Since the heuristic function is consistent, we can just ignore the repeated states.
    def search(self):
        node = Node(self.input_state,None,None,0,self.compute_h(self.input_state)) #the starting node
        self.frontier.put(node)
        while not self.frontier.empty():
            node = self.frontier.get()
            if self.is_goal(node):
                return node
            for child in self.expand(node):
                s = child.cur_state
                if s not in self.states:
                    self.states.append(s)
                    self.frontier.put(child)
    
    #After getting the goal node, we return its total path cost, the number of nodes generated,
    #the action sequence and the f value sequence from the starting node to the goal node.             
    def result_detail(self):
        a_list = []
        f_list = []
        node = self.result_node
        while not node.action is None:
            a_list.append(str(node.action))
            f_list.append(str(node.f_value))
            node = node.par_node
        f_list.append(str(self.compute_h(project.input_state)))
        a_list.reverse()
        f_list.reverse()
        return self.result_node.path_cost, len(self.states), a_list, f_list
    
    #After getting all information we need, we need to write them into the output file.
    def write_output(self,output_file):
        data_input = open(self.input_file,"r")
        input_list = []
        for line in data_input:
            input_list.append(line)
        data_input.close()
        data_output = open(output_file,"w")
        for line in input_list:
            data_output.write(line)
        result_detail = self.result_detail()
        data_output.write("\n")
        data_output.write(str(result_detail[0])+"\n")
        data_output.write(str(result_detail[1])+"\n")
        data_output.write(" ".join(result_detail[2])+"\n")
        data_output.write(" ".join(result_detail[3])+"\n")
        data_output.close()

if __name__ == "__main__":
    #Just put the input file name and the output file name here, and then we can get the result.
    project = Project("Input3.txt") #Name of input file
    project.write_output("Output3.txt") #Name of output file