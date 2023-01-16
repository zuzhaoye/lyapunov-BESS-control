from math import sqrt

'''Settings'''

K = 0.88 # BESS energy efficiency (or round-trip efficiency)
E_FULL = 336  # BESS full capacity (kWh)
E_MAX = 0.9*E_FULL # BESS maximum allowable capacity (90% of full)
E_MIN = 0.15*E_FULL # BESS maximum allowable capacity (90% of full)
P_MAX = 57 # BESS maximum allowable power flow (being discharging)
P_MIN = -57 # BESS minimum allowable power flow (being charging)
DT = 1/3600 # Control time interval, in hour
Q_MAX = E_MAX - E_MIN - DT*P_MAX*sqrt(K) # The maximum value of the BESS energy queue 
Q_MIN = -DT*P_MAX*sqrt(K) # The miminum value of the BESS energy queue 
P_PEAK_TARGET = 25 # Target peak load (kW)
WEIGHT_DEMAND_CHARGE = 1 # The weight of demand charge in Eq.(26b)
SELL_BACK_ENABLED = True # If allowing sending electricity back to the grid
if SELL_BACK_ENABLED:
    P_MIN_SELL_BACK = float('-inf')
else:
    P_MIN_SELL_BACK = 0
SELL_BACK_DISCOUNT = 1 # The price discount of sell-back electricity. Examples: For net-metering, use 1. If the sell-back price is 90% of the original price, use 0.9
ALLOW_GRID_CHARGE = False # Whether to allow charging the BESS with power from the grid

month_days = {1: 31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
peakNames = {0: "Super Off-Peak", 1: "Off-Peak", 2: "On-Peak"}
peakHourTable_weekday = {0: 0,
             1: 0,
             2: 0,
             3: 0,
             4: 0,
             5: 0,
             6: 1,
             7: 1,
             8: 1,
             9: 1,
             10: 1,
             11: 1,
             12: 1,
             13: 1,
             14: 1,
             15: 1,
             16: 2,
             17: 2,
             18: 2,
             19: 2,
             20: 2,
             21: 1,
             22: 1,
             23: 1}
peakHourTable_weekdayMarApr = {0: 0,
             1: 0,
             2: 0,
             3: 0,
             4: 0,
             5: 0,
             6: 1,
             7: 1,
             8: 1,
             9: 1,
             10: 0,
             11: 0,
             12: 0,
             13: 0,
             14: 1,
             15: 1,
             16: 2,
             17: 2,
             18: 2,
             19: 2,
             20: 2,
             21: 1,
             22: 1,
             23: 1}
peakHourTable_weekend = {0: 0,
             1: 0,
             2: 0,
             3: 0,
             4: 0,
             5: 0,
             6: 0,
             7: 0,
             8: 0,
             9: 0,
             10: 0,
             11: 0,
             12: 0,
             13: 0,
             14: 1,
             15: 1,
             16: 2,
             17: 2,
             18: 2,
             19: 2,
             20: 2,
             21: 1,
             22: 1,
             23: 1}
summerMonths = [6, 7, 8, 9, 10]
winterMonths = [1, 2, 3, 4, 5, 11, 12]

# Energy charge
energyChargeRef_Winter = {0: 0.09432,
                          1: 0.12207,
                          2: 0.21780}
energyChargeRef_Summer = {0: 0.09960,
                          1: 0.10423,
                          2: 0.17868}

# Demand charge
cd_OnPeak_Winter = 25.56
cd_OnPeak_Summer = 27.80
cd_NonCoincident_Winter = 29.89
cd_NonCoincident_Summer = 31.32
cd_Generation_Winter = 0.0
cd_Generation_Summer = 12.18
demandChargeRef_Winter = {0: cd_NonCoincident_Winter + cd_Generation_Winter,
                          1: cd_NonCoincident_Winter + cd_Generation_Winter,
                          2: cd_NonCoincident_Winter + cd_Generation_Winter + cd_OnPeak_Winter}
demandChargeRef_Summer = {0: cd_NonCoincident_Summer + cd_Generation_Summer,\
                          1: cd_NonCoincident_Summer + cd_Generation_Summer,\
                          2: cd_NonCoincident_Summer + cd_Generation_Summer + cd_OnPeak_Summer}

# V values
V_NONPEAK = 1
V_PEAK = 1
VsTable = {0: V_NONPEAK,
           1: V_NONPEAK,
           2: V_PEAK}

