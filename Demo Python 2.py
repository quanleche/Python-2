server=app.server
import pandas as pd
gdp = pd.read_csv("D:\Foundation Year\Business IT 1\Datasets R\Group 4 - Dataset.csv")
from matplotlib import pyplot as plt
import seaborn as sb
Top5GDP = pd.DataFrame([['USA', 3.659040, 15.526720, 0.174240],['China', 4.716300, 6.232680, 0.991020],['Japan', 1.450548, 3.384612, 0.048840],
                        ['Germany', 1.099252, 2.530836, 0.021912],['France', 0.517575, 2.005925, 0.051500]],
                        columns=['Country', 'Industry', 'Service', 'Agriculture'])
Top5GDP.plot(x='Country', kind='barh', stacked=True, rot=45)


sb.set_palette('Set1')
plt.title('GDP structure of top 5 nations with the highest GDP', fontsize=15, color='red', y=1.06, loc='left')
plt.title('Unit: million USD', size=10, color='black', loc='right')
plt.ylabel('Country', fontsize=12, color='navy')
plt.xlabel('GDP', fontsize=12, color='navy')
sb.set_context('notebook')
sb.set_style('ticks')
plt.show()
