import matplotlib.pyplot as plt
import matplotlib.animation as animation

from module.population import Population
from module.simulation_param import SimParam

# ------------------------------------------------------------
# set simulation parameters
# 1: no measures 2:quaratine 3: low social distancing 4: effective distancing
s = SimParam(3)

# initialise simulation class
p = Population(s.init_state, s.walls, size=s.S, recovery_step=s.R)

# ------------------------------------------------------------
# set up figure and animation

# new figure and axis properties
fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
ax.set_xlim(s.graph_xlim)
ax.set_ylim(s.graph_ylim)
ax.set_axis_off()

ax2 = fig.add_subplot(2, 1, 2)
ax2.set_ylim(0, s.N)
ax2.set_xlim(0, 50)
ax2.set_ylabel(f"Infected (N={s.N})")
ax2.set_xticks([])
ax2.set_xlabel(f"Time")

# plot walls
for row in s.walls:
    ax.plot(row[0::2], row[1::2], 'k')

# blue for not infected, black for recovered, red for infected
particles0, = ax.plot([], [], 'bo', ms=5)
particles1, = ax.plot([], [], 'ko', ms=5)
particles2, = ax.plot([], [], 'ro', ms=5)

s1 = ax.text(0.2 * max(s.graph_xlim), 0.9 * max(s.graph_ylim), '')
s2 = ax.text(0.6 * max(s.graph_xlim), 0.9 * max(s.graph_ylim), '')

stats, = ax2.plot([], [], 'b')


def init():
    """initialize animation"""
    global p

    particles0.set_data([], [])
    particles1.set_data([], [])
    particles2.set_data([], [])
    s1.set_text(f'Infected = ')
    s2.set_text(f'Recovered = ')
    stats.set_data([], [])

    return particles0, particles1, particles2, s1, s2, stats


def animate(i):
    """perform animation step"""
    global p
    p.step()

    # update pieces of the animation
    particles0.set_data(p.state[p.state[:, 4] == 0, 0],
                        p.state[p.state[:, 4] == 0, 1])
    particles1.set_data(p.state[p.state[:, 4] == 1, 0],
                        p.state[p.state[:, 4] == 1, 1])
    particles2.set_data(p.state[p.state[:, 4] == 2, 0],
                        p.state[p.state[:, 4] == 2, 1])

    s1.set_text(f"Infected = {p.infected_count}")
    s2.set_text(f"Recovered = {p.recovered_count}")

    # print(p.time_history[:, 1])

    stats.set_data(p.time_history[:, 0], p.time_history[:, 1])

    return particles0, particles1, particles2, s1, s2, stats


ani = animation.FuncAnimation(fig, animate, frames=s.framecount, repeat=False,
                              interval=1, blit=True, init_func=init)

plt.show()