import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

db_files = 'dataBase'
wd = os.getcwd()
parent_dir = os.path.dirname(os.getcwd())
db_dir = os.path.join(parent_dir, db_files)

m_qx_1000 = pd.read_excel(db_dir + '\\tabelasMortalidadeSexo_20210417.xls', sheet_name='male2019')
f_qx_1000 = pd.read_excel(db_dir + '\\tabelasMortalidadeSexo_20210417.xls', sheet_name='female2019')

fig, axes = plt.subplots()
plt.plot(m_qx_1000.iloc[:, 0], np.log(m_qx_1000.iloc[:, 1] / 1000), label='males')
plt.plot(f_qx_1000.iloc[:, 0], np.log(f_qx_1000.iloc[:, 1] / 1000), label='females')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.xlabel('ages (x)')
plt.ylabel(r'$\ln{(q_x)}$')
plt.title('Mortality Tables for Portugal 2017-2019')
plt.legend()
this_py = os.path.split(sys.argv[0])[-1][:-3]
plt.savefig(this_py + '_qx_mu' + '.eps', format='eps', dpi=3600)
plt.show()
