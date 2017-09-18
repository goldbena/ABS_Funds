import analytics_hero.fundAnalytics as fundAnalytics
from analytics_hero.utils import cumulative_returns
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
ac = fundAnalytics.AnalyticsClass()
plt.style.use('seaborn-deep')
sns.set_color_codes()

# Index_ID   Index Name
# 12211319   Barclays US MBS Index
# 12571      Barclays Global-Aggregate
# 1272018    Barclays Global Agg Treasuries
# 1221120    Barclays US Treasury
# 31219      BofA ML US ABS MBS Index
# 3210       BofA ML AAA US Fixed Rate CMBS
# 3220       BofA ML AA US Fixed Rate CMBS
# 3230       BofA ML A US Fixed Rate CMBS
# 3240       BofA ML BBB US Fixed Rate CMBS

# Load the performance data from the Database
index_returns = ac.get_performance([12211319, 12571, 1272018, 1221120, 31219, 3210, 3220, 3230, 3240],
                                   init='2010-01-01', end='2017-07-01')

# Cumulative returns of Fixed Income Indices
ac.cumulative_return_line(index_returns[[1221120, 12571, 12211319, 31219]])

# Cumulative returns of the MBS Tranches
ac.cumulative_return_line(index_returns[[3210, 3220, 3230, 3240]])

# 1Y Rolling Excess Return of MBS against US Treasuries
MBS_er = index_returns[12211319]-index_returns[1221120]
ABS_er = index_returns[31219]-index_returns[1221120]
excess_return = pd.DataFrame(data=[MBS_er, ABS_er],
                             index=['Barclays US MBS Index Excess Return','BofA ML US ABS MBS Index Excess Return'],
                             columns=MBS_er.index).transpose()
rolling_excess_return = ac.create_rolling_returns(excess_return, window=36)

fig = plt.figure()
ax = plt.axes()
ax.plot(rolling_excess_return)
plt.legend(labels = excess_return.columns)

# Histograms of Returns
ac.funds_histogram_overlap(index_returns[[12211319, 31219, 1221120]], names_from_db=True)

# Monthly Returns Table of Excess Return
MBS_table = ac.monthly_returns_table(excess_return[['Barclays US MBS Index Excess Return']])
ABS_table = ac.monthly_returns_table(excess_return[['BofA ML US ABS MBS Index Excess Return']])
ac.create_monthly_returns_table(MBS_table['Barclays US MBS Index Excess Return'])
ac.create_monthly_returns_table(ABS_table['BofA ML US ABS MBS Index Excess Return'])

# Capture Analysis
MBS_capture = ac.capture_analysis(index_returns[[12211319, 1221120]])
ABS_capture = ac.capture_analysis(index_returns[[31219, 1221120]])

# Sensitivity Analysis
ac.pos_neg_reg(index_returns[[12211319, 1221120]])
ac.pos_neg_reg(index_returns[[31219, 1221120]])

# Risk Adjusted Performance
MBS_risk_return = ac.risk_adjusted_performance(index_returns[12211319],index_returns[1221120])
ABS_risk_return = ac.risk_adjusted_performance(index_returns[31219],index_returns[1221120])