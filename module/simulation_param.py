import numpy as np


class SimParam:

    def __init__(self, option):

        # consistent random seed
        np.random.seed(0)

        # option 1 (no quarantine)
        if option == 1:
            self.walls = np.array([[0, 0, 2, 0],  # bottom wall
                                   [2, 0, 2, 2],  # right wall
                                   [0, 0, 0, 2],  # left wall
                                   [0, 2, 2, 2]])  # top wall

            self.N = 100     # number of humans
            self.R = 1000    # recovery rate
            self.S = 0.02    # size of marker in plot

            # initial state
            self.init_state = np.zeros((self.N, 7))
            self.init_state[:, :2] = 1.8 * np.random.rand(self.N, 2) + 0.1
            self.init_state[:, 2:4] = 0.5 * np.random.rand(self.N, 2) - 0.25
            self.init_state[0:5, 4] = 2

            # plotting
            self.graph_xlim = (-0.1, 2.1)
            self.graph_ylim = (-0.1, 2.3)
            self.framecount = 4000

        # option 2 (quaratine)
        if option == 2:
            self.walls = np.array([[0, 0, 1, 0],    # bottom wall
                                   [1, 0, 1, .75],   # right wall 1
                                   [1, 1.25, 1, 2],  # right wall 1
                                   [0, 0, 0, 2],    # left wall
                                   [0, 2, 1, 2],    # top wall
                                   [1, 0, 2, 0],    # bottom wall
                                   [2, 0, 2, 2],    # right wall
                                   [1, 2, 2, 2]])   # top wall
            self.N = 100     # number of humans
            self.R = 1000    # recovery rate
            self.S = 0.02   # size of marker in plot

            # initial state
            self.init_state = np.zeros((self.N, 7))
            self.init_state[:, :2] = 1.8 * np.random.rand(self.N, 2) + 0.1
            self.init_state[:, 2:4] = 0.5 * np.random.rand(self.N, 2) - 0.25
            self.init_state[0:5, 4] = 2

            # plotting
            self.graph_xlim = (-0.1, 2.1)
            self.graph_ylim = (-0.1, 2.3)
            self.framecount = 4000

        # option 3 (low social distancing)
        if option == 3:
            self.walls = np.array([[0, 0, 2, 0],  # bottom wall
                                   [2, 0, 2, 2],  # right wall
                                   [0, 0, 0, 2],  # left wall
                                   [0, 2, 2, 2]])  # top wall

            self.N = 100     # number of humans
            self.R = 1000    # recovery rate
            self.S = 0.02   # size of marker in plot

            # low social distance of 25% obeying
            social_distancing = round(0.25 * self.N)
            not_distancing = self.N - social_distancing

            # initial state
            self.init_state = np.zeros((self.N, 7))
            self.init_state[:, :2] = 1.8 * np.random.rand(self.N, 2) + 0.1
            self.init_state[:not_distancing, 2:4] = \
                0.5 * np.random.rand(not_distancing, 2) - 0.25
            self.init_state[0:5, 4] = 2
            self.init_state[not_distancing:, 6] = 1

            # plotting
            self.graph_xlim = (-0.1, 2.1)
            self.graph_ylim = (-0.1, 2.3)
            self.framecount = 4000

        # option 4 (effective social distancing)
        if option == 4:
            self.walls = np.array([[0, 0, 2, 0],  # bottom wall
                                   [2, 0, 2, 2],  # right wall
                                   [0, 0, 0, 2],  # left wall
                                   [0, 2, 2, 2]])  # top wall

            self.N = 100     # number of humans
            self.R = 1000    # recovery rate
            self.S = 0.02   # size of marker in plot

            # low social distance of 75% obeying
            social_distancing = round(0.75 * self.N)
            not_distancing = self.N - social_distancing

            # initial state
            self.init_state = np.zeros((self.N, 7))
            self.init_state[:, :2] = 1.8 * np.random.rand(self.N, 2) + 0.1
            self.init_state[:not_distancing, 2:4] = \
                0.5 * np.random.rand(not_distancing, 2) - 0.25
            self.init_state[0:5, 4] = 2
            self.init_state[not_distancing:, 6] = 1

            # plotting
            self.graph_xlim = (-0.1, 2.1)
            self.graph_ylim = (-0.1, 2.3)
            self.framecount = 4000