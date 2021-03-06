import random
import time

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)


class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            # print("WARNING: You cannot be friends with yourself")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            # print("WARNING: Friendship already exists")
            return False
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments
 
        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        # iterate over 0 to num users...
        for i in range(0, num_users):
            # add user using an f-string
            self.add_user(f"User {i}")

        # Create friendships
        # generate all possible friendship combinations
        possible_friendships = []

        # avoid duplicates by making sure the first number is smaller than the second
        # iterate over user id in users...
        for user_id in self.users:
            # iterate over friend id in a range from user id + 1 to last id + 1...
            for friend_id in range(user_id + 1, self.last_id + 1):
                # append a user id and friend id tuple to the possible friendships
                possible_friendships.append((user_id, friend_id))

        # shuffle friendships random import
        random.shuffle(possible_friendships)

        # create friendships for the first N pairs of the list
        # N is determined by the formula: num users * avg friendships // 2
        # NOTE: need to divide by 2 since each add_friendship() creates 2 friendships
        # iterate over a range using the formula as the end base...
        for i in range(num_users * avg_friendships // 2):
            # set friendship to possible friendships at i
            friendship = possible_friendships[i]
            # add friendship of frienship[0], friendship[1]
            self.add_friendship(friendship[0], friendship[1])

    def populate_graph_linear(self, num_users, avg_friendships):
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        #Add users
        for user in range(num_users):
            self.add_user(user)
        
        target_friendships = num_users * avg_friendships
        friendships_successfully_added = 0
        failures = 0

        # continue this until we have as many friendships as we need:
        while friendships_successfully_added < target_friendships:
        ## choose two random numbers(integers) between 1 and self.last_id
            user_id = random.randint(1, self.last_id)
            friend_id = random.randint(1, self.last_id)
            ## try to make that friendship!
            added_friendship = self.add_friendship(user_id, friend_id)
            ## if it works, increment the friendship counter
            if added_friendship:
                friendships_successfully_added += 2
            else:
                failures += 1


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        q = Queue()
        q.enqueue([user_id])

        while q.size() > 0:
            path_list = q.dequeue()
            last_vertex = path_list[-1]

            if last_vertex not in visited:
                visited[last_vertex] = path_list

                for friend in self.friendships[last_vertex]:
                    path = list(path_list)
                    path.append(friend)
                    q.enqueue(path)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()

    num_users = 100
    avg_friendships = 5

    start_time = time.time()
    sg.populate_graph(num_users, avg_friendships)
    print(f'Quadratic time: {time.time() - start_time}')

    start_time = time.time()
    sg.populate_graph_linear(num_users, avg_friendships)
    print(f'Linear time: {time.time() - start_time}')


    print(sg.friendships)

    connections = sg.get_all_social_paths(1)
    total_paths_length = 0
    for user_id in connections:
        total_paths_length += len(connections[user_id])
    average_degree_of_seperation = total_paths_length / len(connections)

    print('cnnections:', connections)
    print('DOS:', average_degree_of_seperation)
