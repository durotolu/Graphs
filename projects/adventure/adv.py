from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from util import Stack, Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

map = {}

def traverse(player, moves):
    queue = Queue()
    queue.enqueue([player.current_room.id])
    visited = set()
    #while the queue can go somewhere
    while queue.size() > 0:
        path = queue.dequeue()
        last_visited = path[-1]
        if last_visited not in visited:
            visited.add(last_visited)
        # note the exits
            for exit in map[last_visited]:
                if map[last_visited][exit] == '?':
                    return path
                #otherwise, get rid of the explored path
                else:
                    already_explored = list(path)
                    already_explored.append(map[last_visited][exit])
                    queue.enqueue(already_explored)
    return []

# check for exits that haven't been tried
def untried(player, new_moves):
    exits = map[player.current_room.id]
    untried = []
    for direction in exits:
        if exits[direction] == "?":
            # to be explored
             untried.append(direction)

    if len(untried) == 0:
        # explore until you find a room with unexplored exits
        unexplored = traverse(player, new_moves)
        # set room to the player's current room
        new_room = player.current_room.id

        for room in unexplored:
            # check for unexplored exits in the room and add to new moves
            for direction in map[new_room]:
                if map[new_room][direction] == room:
                    new_moves.enqueue(direction)
                    new_room = room
                    break
    #otherwise, try a random untried exit
    else:
        new_moves.enqueue(untried[random.randint(0, len(untried) -1)])
#create moves that only use untried exits
#create an unexplored room dictionary
unexplored_room = {}

#go through the exits in the current room
for direction in player.current_room.get_exits():
    #add all ? exits to unexplored_room
    unexplored_room[direction] = "?"
    #the starting room should always be an unexplored room
map[world.starting_room.id] = unexplored_room
#turn new_moves into a queue
new_moves = Queue()
#call untried 
untried(player, new_moves)
#set the reverse directions, just like in the adventure game
reverse_dir = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
  }
#while new_moves has items in it
while new_moves.size() > 0:
    #set the starting room
    start = player.current_room.id
    #grab a direction from new_moves
    move = new_moves.dequeue()
    #move that direction
    player.travel(move)
    #add that to traversal_path
    traversal_path.append(move)
    #set the player's new room to a variable
    next_room = player.current_room.id
    #set the map entry for the move to next_room
    map[start][move] = next_room
    #if it isn't in the map
    if next_room not in map:
        map[next_room] = {}
        #for each exit found in the current room
        for exit in player.current_room.get_exits():
            #set each unexplored exit to ?
            map[next_room][exit] = "?"
    #map the reverse compass and set it to the next start
    map[next_room][reverse_dir[move]] = start
    #if there are no moves left in new_moves
    if new_moves.size() == 0:
        #run untried again
        untried(player, new_moves)

# def traverse_unvisited(starting_room = player.current_room):
#     print(starting_room)
#     opposite = {
#         'n': 's',
#         's': 'n',
#         'e': 'w',
#         'w': 'e',
#     }
    
#     s = Stack()
#     s.push([starting_room])
#     visited = {}

#     while s.size() > 0:
#         path = s.pop()
#         # print(43, path)
#         v = path[-1]
#         v_id = v.id
#         v_exits = v.get_exits()

#         print('key', v_id)
#         print(visited[v_id])

#         if not visited[v_id]:
#             print('id', v.id)
#             visited[v] = path
#             # print('47', v, '47')
#             # print('exits', v.get_exits())

#             for next_direction in v_exits:
#                 visited[v_id][next_direction] = '?'
#                 print(visited[v_id])
#                 # for next_room in v.get_room_in_direction(next_direction)
#                 # path_copy = list(path)
#                 # room = v.get_room_in_direction(next_direction)
#                 # v.connect_rooms(next_direction, room)
#                 # print(53, room, next_direction)
#                 # traversal_path.append(next_direction)
#                 # path_copy.append(room)
#                 # s.push(path_copy)

#         for direct in visited[v_id]:
#             if visited[v_id][direct] == '?':
#                 if player.travel(direct):
#                     player_room = player.current_room.id
#                     visited[v_id][direct] = player_room
#                     visited[player_room][opposite[direct]] = v_id
#                     traversal_path.append(direct)

# traverse_unvisited()

# print(traversal_path)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
