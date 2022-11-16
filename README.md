# lyapunov-BESS-control

This repo implements a control algorithm based on Lyapunov optimization [[Ref. 1]](https://ieeexplore.ieee.org/document/9853637) to reduce the electricity bills of commercial buildings with battery energy storage systems (BESS). The core idea is to seek a balance between the immediate energy/demand charges and the battery energy reservation. The single-step Lyapunov optimization is implemented in ```lo_step.py```, while a complete simulation on all time steps is implemented in ```simulation.ipynb``` by wrapping up other supportive modules. 

We provide a sample data file here for illustration purpose. This data file is from a commercial building but scaled for confidential considerations. It has a time interval of 1 second and covers solar powers and building loads from 05/31/2022 to 06/01/2022.

To run:
- Run ```simulation.ipynb``` to obtain optimized loads with BESS (the default data is in 1-second intervals)
- Run ```post1-get-15min-loads.ipynb``` to obtain aggregated 15-min loads w/ and w/o BESS.
- Run ```post2-cost-audit.ipynb``` to get energy/demand charges and total costs w/ and w/o BESS.

## Theoretical Background

With Lyapunov optimization, the BESS output at each time step can be determined heuristically by solving the following optimization problem:

<figure>
    <img src="/assets/la_equations.png"
         width="450"
         alt="Lyapunov optimization">
</figure>

where $d(t_a)$ and $c(t_a)$ are the discharging and charging power of the BESS at an arbitrary time step. 

If we replace $[d(t_a) - c(t_a)]$ with a single variable $x$, the above optimization problem (e.g. (25), (26a-c), (6), and (7)) will be solely related to $x$ and the optimal value is found at boundary points or any transition points within the range of $x$. There are two boundary points and three transition points as summarized below:

- $x = P_{max}$, right boundary.
- $x = P_{min}$, left boundary.
- $x = 0$, a transition point due to the term $|x|$ in (26a).
- $x = P_G(t_a)$,  a transition point due to the terms $max(P_G(t_a), 0)$ and $min(P_G(t_a), 0)$ in (26b).
- $x = P_G(t_a) - M(t_a)$,  a transition point due to the term $max(P_G(t_a) - M(t_a), 0)$ in (26b).

## Implementation
The algorithm is implemented in ```lo_step.py```. It compares the objective values evaluated at the 5 points stated above and selects the best one as the output of the BESS. ```lo_step.py``` has the following inputs and outputs:

Inputs:
- LB: Building load (kW) at current time step
- PS: Solar generation power (kW) at current time step (PS > 0 indicates positive power generation)
- Ppeak: Historical peak load (kW)
- SoC: BESS SoC at current time step
- pE: Electricity price ($/kWh) at current time step (buying from the grid)
- pF: Electricity price ($/kWh) at current time step (selling to the grid)
- pD: Demand charge price ($/kW) at current time step
- V: The balance term between immediate costs and energy reservation
- DT: Control time interval (hour)

Outputs:
- x: BESS discharging power (kW, x>0, BESS discharges to offset the building load, and x<0 BESS get charged)

## Pricing Scheme
### Time-of-use Schedules
Another important aspect of the simulation is the determination of the prices at each time step. Here we adopt the commercial time-of-use schedules of SDGE [[Ref. 2]](https://www.sdge.com/total-electric-rates).

<figure>
    <img src="/assets/time_of_use.png"
         width="650"
         alt="Time_of_use table">
</figure>

### Energy charge
The energy charge varies by season and hour of the day. See ```settings.py``` and [[Ref. 3]](https://www.sdge.com/sites/default/files/regulatory/Summary%20Table%20for%20Large%20Comm%206-1-22%20w%20PCIA.pdf) for detailed information on energy charges.

### Demand charge
According to SDGE, there are three types of demand charges: Non-coincident, On-peak, and Generation [[Ref. 4]](https://www.sdge.com/businesses/pricing-plans/understanding-demand). Each type of demand charge compensates for different aspects of the operation costs. During off-peak hours, the total effective demand charge is the sum of Non-coincident and Generation demand charges, while during on-peak hours, the total effective demand charge is the sum of all three types of demand charges.

## Load Aggregation

```post1-get-15min-loads.ipynb```

Since utility companies usually calculate the bills based on 15-minute intervals, it is necessary to aggregate the original data in 1-second intervals (or whatever other intervals) into 15-min intervals before we calculate the bills w/o or w/ BESS.

The function module creates contiguous 15-min time intervals starting from the Day 0 of billing. For each 15-min time interval, the function module collects all load data points that fall within this interval and then calculates their mean values.

## Cost Audit

```post2-cost-audit.ipynb```

The cost audit process is very similar to the simulation process. The only difference is the time interval of data. The energy charge, demand charge, and total costs will be reported through this module.

## References
1. Shi, Jie, Zuzhao Ye, H. Oliver Gao, and Nanpeng Yu. "Lyapunov Optimization in Online Battery Energy Storage System Control for Commercial Buildings." IEEE Transactions on Smart Grid (2022).
2. SDGE, Summary of electric rates and time-of-use schedules, https://www.sdge.com/total-electric-rates
3. SDGE, Medium Large Commercial & Industrial Rates, https://www.sdge.com/sites/default/files/regulatory/Summary%20Table%20for%20Large%20Comm%206-1-22%20w%20PCIA.pdf
4. SDGE, Understanding demand, https://www.sdge.com/businesses/pricing-plans/understanding-demand

