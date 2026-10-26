# Importing modules and libraries
from maze_visual import maze, agent
import sys
import argparse
import time
from collections import deque 
import math
import heapq # Importing the heapq module to use the priority queue
# Import any other modules you want to use here



# DO NOT CHANGE THESE LINES OF CODE
# ----------------------------------
ROWS = 20 # Number of rows in the maze
COLS = 20 # Number of columns in the maze
m = maze(ROWS, COLS) # Initialize the maze

# Load the maze from the csv file. You may need to change this path depending on where you save the files.
m.LoadMaze(loadMaze='maze_config.csv', theme="dark")
# ----------------------------------


def get_neighbors(maze, cell):
    '''
    Returns a list of valid neighboring cells (positions) from the current cell.
    The neighbors are returned in the order: North, West, South, East.
    '''
    '''
    Function Description:
    This function is used to get the neighbors of a given cell.For example we encounter a cell (1,1) and we want to get the neighbors of this cell.
    So we check if the North, West, South, East of the cell is open or not. If it is open we add it to the list of neighbors.
    So the neighbors of the cell (1,1) are (0,1), (1,0), (2,1), (1,2).
    So the function returns the list of neighbors.
    north means moving up, west means moving left, south means moving down, east means moving right.
    these are in accordance to the maze_map which is nothing but a 2D array containing rows and columns.
    '''

    x, y = cell
    neighbors = [] # List to store the neighbors
    # North
    if maze.maze_map.get((x, y), {}).get('N', 0): # Check if the North is open
        neighbors.append((x - 1, y)) # Add the neighbor to the list
    # West
    if maze.maze_map.get((x, y), {}).get('W', 0): # Check if the West is open
        neighbors.append((x, y - 1)) # Add the neighbor to the list
    # South
    if maze.maze_map.get((x, y), {}).get('S', 0): # Check if the South is open
        neighbors.append((x + 1, y)) # Add the neighbor to the list
    # East
    if maze.maze_map.get((x, y), {}).get('E', 0): # Check if the East is open
        neighbors.append((x, y + 1)) # Add the neighbor to the list
    return neighbors # Return the list of neighbors


def DFS(maze, start, goal):
    '''
    This function should implement the Depth First Search algorithm.
    The inputs to this function are:
        maze: The maze object
        start: The start position of the agent as a tuple (x,y)
        goal: The goal position of the agent as a tuple (x,y)
    The function should return:
        a list containing all the positions visited by the search algorithm
        a list containing the positions in the final path from the start to the goal
    '''
    '''
     DFS Algorithm (Main Idea):
     So the main idea is that we are doing depth by depth traversal of maze using DFS.We initialized a stack to store the positions to be visited and also intialized a set so mark visited positions
     The reason we are using set is that it is more efficient and also it only accpets unique values. We also intialized a dictionary to store the parent of each position so that we can reconstruct 
     the path from the goal to the start after we have reached the goal and the loop stops.We initialized a flag named goal_reached to check if the goal has been reached so that we can stop the loop.
     Once the loop Stops we start another loop in order to reconstruct the path from the goal to the start.we set the initial point as goal and keep on running till we reach the start and finally reverse
     the path to the goal.the reason we are using reversed function is that we want to explore the neighbors in the order of North, West, South, East.
     
    '''    
    
    

    visited_positions = []
    path_to_goal = []

    # TODO: Implement Depth-First Search (DFS) algorithm here
    # NOTE: Think sbout what direction you should explore first in the event of multiple options. For the purpose of this assignment, the start 
    #       position is always bottom right and the goal is always top left. Also think about what gets popped first using either stack or recursion.

    stack = [] # Stack to store the positions to be visited
    stack.append(start) # Add the start position to the stack
    visited_nodes = set() # Set to store the positions that have been visited so that we do not visit them again and it avoid Duplicate entries.
    visited_nodes.add(start) # Add the start position to the set
    parent_nodes = {} # Dictionary to store the parent of each position so that we can reconstruct the path from the goal to the start after we have reached the goal and the loop stops.
    goal_reached = False # Flag to check if the goal has been reached

    while stack:
        current = stack.pop() # Pop the last position from the stack
        if current not in visited_positions: # Check if the current position has not been visited
            visited_positions.append(current) # Add the current position to the list of visited positions
        if current == goal:
            goal_reached = True # Set the flag to True if the goal has been reached
            break
        for neighbor in reversed(get_neighbors(maze, current)): # Get the neighbors of the current position we are reversing the list because we want to explore the neighbors in the order of North, West, South, East.
            if neighbor not in visited_nodes: # Check if the neighbor has not been visited
                visited_nodes.add(neighbor) # Add the neighbor to the set
                parent_nodes[neighbor] = current # Add the neighbor to the dictionary to check how we reached the neighbor from the start.
                stack.append(neighbor) # Add the neighbor to the stack

    # Reconstruct path from goal to start
    if goal_reached:
        node = goal # Set the node to the goal
        while node != start: # Running the loop until the node is the start
            path_to_goal.append(node) # Add the node to the path to the goal
            node = parent_nodes[node] # Get the parent of the node
        path_to_goal.append(start) # Add the start to the path to the goal
        path_to_goal.reverse() # Reverse the path to the goal

    return visited_positions, path_to_goal # Return the list of visited positions and the path to the goal




def BFS(maze, start, goal):
    '''
    This function should implement the Breadth First Search algorithm.
    The inputs to this function are:
        maze: The maze object
        start: The start position of the agent as a tuple (x,y)
        goal: The goal position of the agent as a tuple (x,y)
    The function should return:
        a list containing all the positions visited by the search algorithm
        a list containing the positions in the final path from the start to the goal
    '''

    # BFS Algorithm:
    '''
    BFS Algorithm (Main Idea):
    So the main idea is that we are doing level by level traversal of maze using BFS.We initialized a queue to store the positions to be visited and also intialized a set so mark visited positions
    The reason we are using set is that it is more efficient and also it only accpets unique values. We also intialized a dictionary to store the parent of each position so that we can reconstruct 
    the path from the goal to the start after we have reached the goal and the loop stops.We initialized a flag named goal_reached to check if the goal has been reached so that we can stop the loop.
    Once the loop Stops we start another loop in order to reconstruct the path from the goal to the start.we set the initial point as goal and keep on running till we reach the start and finally reverse
    the path to the goal.
    '''

    visited_positions = [] # List to store all visited positions so that we do not visit them again
    path_to_goal = [] # List to store the path to the goal
    queue = deque() # Queue to store the positions to be visited
    queue.append(start) # Add the start position to the queue 
    visited_nodes = set() # Set to store the positions that have been visited so that we do not visit them again and it avoid Duplicate entries.
    visited_nodes.add(start) # Add the start position to the set
    parent_nodes = {}  # For path reconstruction
    goal_reached = False # Flag to check if the goal has been reached
    while queue:                   # Running the loop until the queue is empty
        current = queue.popleft() # Pop the first position from the queue
        visited_positions.append(current) # Add the current position to the list of visited positions
        if current == goal: # Check if the current position is the goal
            goal_reached = True # Set the flag to True if the goal has been reached
            break               # Break the loop if the goal has been reached
        for neighbor in get_neighbors(maze, current): # Get the neighbors of the current position
            if neighbor not in visited_nodes: # Check if the neighbor has not been visited
                visited_nodes.add(neighbor) # Add the neighbor to the set
                parent_nodes[neighbor] = current # Add the neighbor to the dictionary
                queue.append(neighbor) # Add the neighbor to the queue

    # Reconstruct path from the goal to the start
    if goal_reached:
        node = goal # Set the node to the goal
        while node != start: # Running the loop until the node is the start
            path_to_goal.append(node) # Add the node to the path to the goal
            node = parent_nodes[node] # Get the parent of the node
        path_to_goal.append(start) # Add the start to the path to the goal
        path_to_goal.reverse() # Reverse the path to the goal

    return visited_positions, path_to_goal # Return the list of visited positions and the path to the goal




def heuristic(position, goal):
    '''
    This function should implement Euclidean Distance as the heuristic function used in A* algorithm.
    The inputs to this function are:
        position: The current position of the agent as a tuple (x,y)
        goal: The goal position of the agent as a tuple (x,y)
    The function should return:
        the heuristic value of the given position
    '''
    '''
    Heuristic Function (Main Idea):
    So the main idea is that we are using the Euclidean distance as the heuristic function to find the shortest path between the position and the goal as heuristic value.
    '''
    x1, y1 = position # Getting the x and y coordinates of the position
    x2, y2 = goal # Getting the x and y coordinates of the goal
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)   # Returning the Euclidean distance between the position and the goal

def AStar(maze, start, goal):
    '''
    This function should implement the A* algorithm.
    The inputs to this function are:
        maze: The maze object
        start: The start position of the agent as a tuple (x,y)
        goal: The goal position of the agent as a tuple (x,y)
    The function should return:
        a list containing all the positions visited by the search algorithm
        a list containing the positions in the final path from the start to the goal
    '''
    '''
    AStar Algorithm (Main Idea):
    So the main idea is that we are using the A* algorithm to find the shortest path between the start and the goal.We initialized a priority queue to store the positions to be visited and also intialized a set so mark 
    visited positions.The reason we are using set is that it is more efficient and also it only accpets unique values. We also intialized a dictionary to store the parent of each position so that we can reconstruct 
    the path from the goal to the start after we have reached the goal and the loop stops.We initialized a flag named goal_reached to check if the goal has been reached so that we can stop the loop.
    Once the loop Stops we start another loop in order to reconstruct the path from the goal to the start.we set the initial point as goal and keep on running till we reach the start and finally reverse
    the path to the goal.
    '''
    visited_positions = [] # List to store all visited positions so that we do not visit them again
    path_to_goal = [] # List to store the path to the goal
    open_set = [] # Priority queue to store the positions to be visited
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))  # (f, g, position) so f is the heuristic value, g is the cost from the start to the current position and position is the current position.
    came_from = {} # Dictionary to store the parent of each position so that we can reconstruct the path from the goal to the start after we have reached the goal and the loop stops.
    g_score = {start: 0} # Dictionary to store the cost from the start to the current position
    visited_nodes = set() # Set to store the positions that have been visited so that we do not visit them again and it avoid Duplicate entries.
    while open_set: # Running the loop until the open set is empty
        f, g, current = heapq.heappop(open_set) # Pop the position with the lowest heuristic value from the open set.
        if current not in visited_positions:
            visited_positions.append(current) # Add the current position to the list of visited positions
        if current == goal: # Check if the current position is the goal
            # Reconstruct path
            node = goal # Set the node to the goal
            while node != start:
                path_to_goal.append(node) # Add the node to the path to the goal
                node = came_from[node] # Get the parent of the node
            path_to_goal.append(start) # Add the start to the path to the goal
            path_to_goal.reverse() # Reverse the path to the goal
            break
        visited_nodes.add(current) # Add the current position to the set
        for neighbor in get_neighbors(maze, current): # Get the neighbors of the current position
            tentative_g_score = g_score[current] + 1  # step cost is 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]: # Check if the neighbor has not been visited or the tentative cost is less than the cost from the start to the neighbor
                came_from[neighbor] = current # Add the neighbor to the dictionary to check how we reached the neighbor from the start.
                g_score[neighbor] = tentative_g_score # Add the tentative cost to the dictionary
                f_score = tentative_g_score + heuristic(neighbor, goal) # Add the heuristic value to the tentative cost
                heapq.heappush(open_set, (f_score, tentative_g_score, neighbor)) # Add the neighbor to the open set.
    return visited_positions, path_to_goal # Return the list of visited positions and the path to the goal





# DO NOT CHANGE THE LINES OF CODE BELOW
# -------------------------------------
# This part of the code calls the search algorithms implemented above and displays the results on the maze
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bfs", help="Run BFS", action="store_true")
    parser.add_argument("-d", "--dfs", help="Run DFS", action="store_true")
    parser.add_argument("-a", "--astar", help="Run A* Search", action="store_true")

    args = parser.parse_args()

    start = (ROWS, COLS)
    goal = (1,1)

    explored, path_to_goal = [], []
    algorithm_name = ""
    start_time = 0

    if args.bfs:
        algorithm_name = "Breadth-First Search (BFS)"
        print(f"Running {algorithm_name}...")
        start_time = time.time()
        explored, path_to_goal = BFS(m, start, goal)
    elif args.dfs:
        algorithm_name = "Depth-First Search (DFS)"
        print(f"Running {algorithm_name}...")
        start_time = time.time()
        explored, path_to_goal = DFS(m, start, goal)
    elif args.astar:
        algorithm_name = "A* Search"
        print(f"Running {algorithm_name}...")
        start_time = time.time()
        explored, path_to_goal = AStar(m, start, goal)
    else:
        print("No search algorithm specified. See help below.")
        parser.print_help()
        sys.exit()
    
    # --- Statistics Calculation and Printing ---
    if start_time > 0:
        end_time = time.time()
        execution_time = end_time - start_time
        path_length = len(path_to_goal)
        nodes_explored = len(explored)

        print("\n--- Search Algorithm Statistics ---")
        print(f"Algorithm: {algorithm_name}")
        print(f"Execution Time: {execution_time:.4f} seconds")
        print(f"Path Length: {path_length} steps")
        print(f"Nodes Explored: {nodes_explored} nodes")
        print("-------------------------------------\n")
    # -------------------------------------------

    # If a path was found, start visualization
    if path_to_goal:
        print("Starting visualization...")
        a = agent(m, ROWS, COLS, filled=True)
        b = agent(m, ROWS, COLS, color="red")

        m.tracePath({a: explored}, delay=20)
        m.tracePath({b: path_to_goal}, delay=50)

        m.run()
    else:
        print("No path to the goal was found!")


if __name__ == "__main__":
    main()






 