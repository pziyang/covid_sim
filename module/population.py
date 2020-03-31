import numpy as np
import math
from scipy.spatial.distance import pdist, squareform


class Population:
    """ Population class.

        Population is modeled using [Nx7] array where N is the number of
        humans in the population.
        Each human is modeled using [1x7] state vector with x,y location
        and u,v velocity, covid status, time_infected and behaviour mode.

        [[x1, y1, u1, v1, covid, t0, mode],
         [x2, y2, u2, v2, covid, t0, mode],
         ...                             ]

       where:
       covid = 0: not_infected, 1: recovered, 2: infected
       t0 = time stamp when first infected
       mode = 0: not distancing, 1: obeying social distancing

       Tranmission is modeled using elastic collision with infected person.
       The probability of transmission is assumed to be 100%.

       The recovery rate is controlled by recovery_step input argument. It is
       assumed that once recovered, the subject will be immune to further
       infection.

       When obeying social distancing, the subject will remain in the
       current location (zero velocity).

        Parameters
        ----------
        init_state : array
        Nx7 array with each row describing [x,y,u,v,covid,t0,mode]

        wall : array
        Mx4 array, where M is number of wall faces in [x1,y1,x2,y2] format

        size : float
        The size of each human for collision computation. This should be small
        relative to the size of the simulation area (default = 0.005)

        recovery_step : int
        Number of simulation steps required to recover from covid-19
        (default = 200)
    """

    def __init__(self, init_state, wall, size=0.005, recovery_step=200):

        # user input
        self.init_state = np.asarray(init_state, dtype=float)
        self.wall = np.asarray(wall, dtype=float)
        self.size = size
        self.recovery_step = recovery_step

        # compute appropriate time step size for wall collision
        max_dt = size / np.linalg.norm(self.init_state[2:4], axis=0)
        self.dt = max(0.01, np.linalg.norm(max_dt, ord=-np.inf))

        # simulation states
        self.t = 0.0
        self.state = self.init_state.copy()

        # simulation statistics
        self.infected_count = np.count_nonzero(self.init_state[:, 4])
        self.recovered_count = 0

        # time history for plotting [time, infected, recovered]
        self.time_history = np.zeros((1, 3))

    def step(self):

        # increment time
        self.t += self.dt

        # update position (x,y) = (x,y) + (u,v) * dt
        self.state[:, 0:2] += self.state[:, 2:4] * self.dt

        # solve for human to human collision
        self.human_collision()

        # solve for wall coliision
        self.wall_collision()

        # update infection stats
        self.update_infection()

    def human_collision(self):

        # find collisions between particles by looking at square-form
        # distance matrix
        D = squareform(pdist(self.state[:, 0:2], 'euclidean'))

        # look only for upper triangular terms for collision defined to be
        # distance < 2* raduus
        idx1, idx2 = np.where(D <= 2 * self.size)
        unique = (idx1 < idx2)
        idx1 = idx1[unique]
        idx2 = idx2[unique]

        # update velocities of colliding pairs
        for i1, i2 in zip(idx1, idx2):

            # location vector
            r1 = self.state[i1, 0:2]
            r2 = self.state[i2, 0:2]

            # velocity vector
            v1 = self.state[i1, 2:4]
            v2 = self.state[i2, 2:4]

            # relative location & velocity vectors
            r_rel = r1 - r2
            v_rel = v1 - v2

            # collisions of spheres reflect v_rel over r_rel
            rr = np.dot(r_rel, r_rel)
            vr = np.dot(v_rel, r_rel)
            vc = vr / rr * r_rel

            # assign new velocities if not distancing
            if self.state[i1, 6] == 0 and self.state[i2, 6] == 0:
                self.state[i1, 2:4] = v1 - vc

            if self.state[i2, 6] == 0 and self.state[i1, 6] == 0:
                self.state[i2, 2:4] = v2 + vc

            # assign new velocities if distancing
            if self.state[i1, 6] == 0 and self.state[i2, 6] == 1:
                self.state[i1, 2:4] = v1 - 2 * vc

            if self.state[i2, 6] == 0 and self.state[i1, 6] == 1:
                self.state[i2, 2:4] = v2 + 2 * vc

            # check infection status
            s1 = self.state[i1, 4]
            s2 = self.state[i2, 4]

            # s1 infected and s2 not infected, propgate to s2
            if s1 == 2 and s2 == 0:
                self.state[i2, 4] = 2
                self.state[i2, 5] = self.t
                self.infected_count += 1

            # s2 infected and s1 not infected, propogate to s1
            if s2 == 2 and s1 == 0:
                self.state[i1, 4] = 2
                self.state[i1, 5] = self.t
                self.infected_count += 1

    def wall_collision(self):

        for face in self.wall:

            # find length of wall line segment
            a = face[0:2]
            b = face[2:4]
            p = b - a
            l2 = np.dot(p, p)

            # compute the distance of the point from wall face
            for row in self.state:
                c = row[0:2]
                v = row[2:4]

                # find projection of point c onto line segment
                # alpha = (c-a).(b-a)/|b-a|^2
                alpha = np.dot(p, c-a) / l2

                # disregard if not on line segment (not colliding)
                if 0 <= alpha <= 1:
                    # compute the projection, also the point of collision
                    q = a + alpha * p

                    # collision point
                    r = q - c

                    # find distance between point c from collision point
                    m2 = np.dot(r, r)

                    if math.sqrt(m2) <= self.size:
                        # collisions of spheres reflect v_rel over r_rel
                        rr = np.dot(r, r)
                        vr = np.dot(v, r)
                        v_rel = vr / rr * r

                        # update velocity
                        v -= 2.0 * v_rel

    def update_infection(self):
        # selected infected
        idx_infected, = np.where(self.state[:, 4] == 2)

        # update status to recovered if sufficient time has lapsed
        for i in idx_infected:
            time_infected = self.t - self.state[i, 5]

            if time_infected > self.recovery_step * self.dt:
                self.state[i, 4] = 1
                self.infected_count -= 1
                self.recovered_count += 1

        # update to time history
        self.time_history = np.append(self.time_history, [[self.t,
                                  self.infected_count,
                                  self.recovered_count]], axis=0)

