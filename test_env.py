from pacman import *
from search import *
import matplotlib.pyplot as plt
import seaborn as sns
import time

map = np.flipud(genfromtxt('pacman_map.csv', delimiter=','))
map[15,0] = 0
env = gym.make('MsPacman-v0')
print(map.shape)
sns.set()

for i in range(1):
    x = []
    y = []
    possible_moves = [2,3,4,5]
    a = random.choice(possible_moves)
    observation = env.reset()
    observation, reward, done, info = env.step(random.choice(possible_moves))

    count = 1
    s1_c = 0
    s2_c = 0
    s3_c = 0
    s4_c = 0

    while info['ale.lives'] == 3:
        env.render()

        observation, reward, done, info = env.step(int(a))

        pacman_loc = find_pacman(observation,map)
        g1_loc = find_g1(observation,map)
        g2_loc = find_g2(observation,map)
        g3_loc = find_g3(observation,map)
        g4_loc = find_g4(observation,map)
        possible_moves = get_possible_moves(pacman_loc,map)
        print_status(pacman_loc, g1_loc, g2_loc, g3_loc, g4_loc, possible_moves)



        updated_map = update_map(map,g1_loc,g2_loc,g3_loc,g4_loc,None)
        m = make_graph(updated_map,map)
        print(len(m))
        print(m)
        g = UndirectedGraph(m)
        print(g)
        pac_problem = GraphProblem(str(pacman_loc[0])+","+str(pacman_loc[1]), "1,1",g)

        # test algorithms
        # UCS
        start = time.time()
        s1 = uniform_cost_search(pac_problem)
        end = time.time()
        s1_time = end-start

        # BFS
        start = time.time()
        s2 = breadth_first_graph_search(pac_problem)
        end = time.time()
        s2_time = end-start

        # DFS
        start = time.time()
        s3 = depth_first_graph_search(pac_problem)
        end = time.time()
        s3_time = end-start

        # Bidirectional
        start = time.time()
        s4 = bidirectional_search(pac_problem)
        end = time.time()
        s4_time = end-start

        print("TIME RESULTS:")
        print(s1_time, s2_time, s3_time, s4_time)

        s1_c = s1_c + s1_time
        s2_c = s2_c + s2_time
        s3_c = s3_c + s3_time
        s4_c = s4_c + s4_time

        print("count: " + str(count))
        print("avg ucs score:" + str(s1_c/count))
        print("avg bfs score:" + str(s2_c/count))
        print("avg dfs score:" + str(s3_c/count))
        print("avg bidirec score:" + str(s4_c/count))

        print(s1)
        print(s1.path())
        next_spot = decode_node(str(s1.path()[1].state))
        a = decide_move(pacman_loc, next_spot)
        #t = make_tree(pacman_loc)
        #print(t.get_up())
        #print(np.unique(observation.reshape(-1, observation.shape[2]),axis = 0))
        #output_obs_csv(observation, count)
        # make tree of possible moves
        # give this tree to MCTS
        count = count+1
        #sns.heatmap(map)
        #plt.show()

        # need an undirected graph of the pacman world


        #plot_locations(new_loc(pacman_loc))
    print("done")
    break
env.close()
