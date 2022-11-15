# lyapunov-BESS-control

This repo implements a control algorithm based on Lyapunov optimization [Ref. 1] to reduce the electricity bills of commercial buildings with battery energy storage systems (BESS). The core idea is to seek a balance between the immediate energy/demand charges and the battery energy reservation. The single-step Lyapunov optimization is implemented in “lo_step.py”, while a complete simulation on all time steps is implemented in “simulation.ipynb” by wrapping up other supportive modules. 

We provide a sample data file here for illustration purpose. This data file is from a commercial building but scaled for confidential considerations. It has a time interval of 1 second and covers solar powers and building loads from 05/25/2022 to 06/03/2022.

## Theoretical Background

With Lyapunov optimization, the BESS output at each time step can be determined heuristically by solving the following optimization problem:

![Tux, the Linux mascot](/assets/images/tux.png)

where $d(ta)$ and $c(t_a)$ are the discharging and charging power of the BESS at an arbitrary time step. 

If we replace [d(ta) - c(ta)] with a single variable x, the above optimization problem (e.g. (25), (26a-c), (6), and (7)) will be solely related to x and the optimal value is found at boundary points or any transition points within the range of x. There are two boundary points and three transition points as summarized below:

x = Pmax, right boundary.
x = Pmin, left boundary.
x = 0, a transition point because of the |x| in (26a).
x = PG(ta),  a transition point because of the max(PG(ta), 0) and min(PG(ta), 0) in (26b).
x = PG(ta) - M(ta),  a transition point because of the max(PG(ta) - M(ta), 0) in (26b).

