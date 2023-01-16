from math import sqrt, inf
from settings import *
### Use just-in-time compilation will speed up the computation
# from numba import njit 

''''''
#@njit
def get_objective(x, Pnet, Q, DT, V, pE, pF, pD, M):
    
    PG = Pnet-x
    QU = Q*(x+(1-sqrt(K))*abs(x))*DT
    Vg = V*(max(PG,0)*pE*DT + min(PG,0)*pF*DT + max(0,PG-M)*pD*WEIGHT_DEMAND_CHARGE)
    obj = QU + Vg
    
    return obj

'''
Perform Lyapunov optimization for a single time step.
Inputs:
    - PS: Solar generation power (kW) at current time step (PS > 0 indicates positive power generation)
    - LB: Building load (kW) at current time step
    - Ppeak: Historical peak load (kW)
    - SoC: BESS SoC at current time step
    - pE: Electricity price ($/kWh) at current time step (buying from the grid)
    - pF: Electricity price ($/kWh) at current time step (selling to the grid)
    - pD: Demand charge price ($/kW) at current time step
    - V: The balance term between immediate costs and energy reservation
    - DT: Control time interval (hour)
    
Outputs:
    - x: BESS discharge power (x>0, BESS discharges to offset the building load, and x<0 BESS get charged)
'''
#@njit
def lo_step(LB, PS, Ppeak, SoC, pE, pF, pD, V, DT):

    Pnet = LB - PS # Calculate net load
    
    if Ppeak > P_PEAK_TARGET: # Determine M based on if the historical peak is above the targeted peak
        M = Ppeak
    else:
        M = P_PEAK_TARGET
            
    # Get current BESS energy queue
    Q = E_MAX - SoC*E_FULL - DT*P_MAX*sqrt(K)

    # Get the objective value at p_BESS = P_MIN
    obj_xmin = get_objective(P_MIN, Pnet, Q, DT, V, pE, pF, pD, M)
    
    # Get the objective value at p_BESS = P_MAX
    obj_xmax = get_objective(P_MAX, Pnet, Q, DT, V, pE, pF, pD, M)
    
    # Get the objective value at p_BESS = 0
    obj_x0 = get_objective(0, Pnet, Q, DT, V, pE, pF, pD, M)
    
    # Get the objective value at p_BESS = Pnet
    if Pnet >= P_MIN and Pnet <= P_MAX:
        obj_xnet = get_objective(Pnet, Pnet, Q, DT, V, pE, pF, pD, M)
    else:
        obj_xnet = inf
    
    # Get the objective value at p_BESS = Pnet-M
    if Pnet-M >= P_MIN and Pnet-M <= P_MAX:
        obj_xnetm = get_objective(Pnet-M, Pnet, Q, DT, V, pE, pF, pD, M)
    else:
        obj_xnetm = inf

    objList = [obj_xmin, obj_xmax, obj_x0, obj_xnet, obj_xnetm]
    xList = [P_MIN, P_MAX, 0, Pnet, Pnet-M]
    objMin = min(objList)
    minIdx = objList.index(objMin)
    x = xList[minIdx]
    
    # clip Q value based on max and min values, and clip x accordingly
    tmpQ = Q + x*DT + abs(x)*DT*(1-sqrt(K))
    if tmpQ > Q_MAX:
        x = (Q_MAX - Q)/((2-sqrt(K))*DT)
    elif tmpQ < Q_MIN:
        x = (Q_MIN - Q)/(sqrt(K)*DT) 
    
    # Charging BESS is only allowed when there is surplus of solar
    if not ALLOW_GRID_CHARGE:
        if x < 0: # If the command is charging, check if charging is allowed
            if PS > 0:
                p_charging_max = PS
            else:
                p_charging_max = 0
            x = -min(p_charging_max, abs(x))
    
    return x