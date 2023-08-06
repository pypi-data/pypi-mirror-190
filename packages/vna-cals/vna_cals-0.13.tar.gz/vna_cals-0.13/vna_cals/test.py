# from Mixer import mixing
# import pandas as pd
#
# import pathlib
#
#
# path = pathlib.Path(__file__).parent.resolve()
#
# ri = 10.92799187653-1.0411162607556j
# Ym = (ri, 0, ri)
#
# V_bias = {'open': 0.0017, 'short': 0.00266, 'load': 0.0041}
# mixer = mixing(
#     meas_table=pd.read_csv(f'{path}/test_data/refl.csv'),
#     cal_table=pd.read_csv(f'{path}/test_data/cal.csv'),
#     V_bias=V_bias,
#     offset=(0,0),
#     Ym=Ym,
#     LO_rate=250e9,
#     point_num=300
# )
from utils import calc_offset
import pandas as pd


exppath ='/Users/yarvod/Labs_and_other/ИРЭ/IF-Refl-Experiments/06_09_2022/'
data_offset = pd.read_csv(exppath + 'data/offset.csv')
data_offset['V'] = data_offset['V'][1:]
data_offset['I'] = data_offset['I'][1:]

v, i = calc_offset(data_offset['V'], data_offset['I'])
print(v, i)

