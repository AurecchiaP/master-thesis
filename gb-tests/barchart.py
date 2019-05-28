import numpy as np
import matplotlib.pyplot as plt

plt.style.use('bmh')


# data to plot
n_groups = 3

#all
# groups3 = (47, 255, 508)
# groups4 = (166, 760, 1556)
# groups8 = (10628, 59162, 105132)

#dynamic
# groups3 = (.043, .227, .492)
# groups4 = (.136, .737, 1.535)
# groups8 = (8.614, 52.378, 102.443)

# fixed
# groups3 = (.001, .008, .015)
# groups4 = (.003, .021, .038)
# groups8 = (.187, 1.010, 2.002)

# hot groups
groups3 = (0.042, 0.213, 0.403)
groups4 = (0.106, 0.520, 1.110)
groups8 = (4.198, 20.581, 42.912)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.2
opacity = 0.8

rects1 = plt.bar(index, groups3, bar_width,
alpha=opacity,
# color='crimson',
label='3 groups')

rects2 = plt.bar(index + bar_width, groups4, bar_width,
alpha=opacity,
# color='royalblue',
label='4 groups')

rects3 = plt.bar(index + 2 * bar_width, groups8, bar_width,
alpha=opacity,
# color='darkorange',
label='8 groups')

plt.xlabel('Items')
plt.ylabel('Time(s)')
ax.set_yscale('log')

# plt.title('Scores by person')
plt.xticks(index + bar_width, ('100\'000', '500\'000', '1\'000\'000'))
plt.legend()
plt.tight_layout()

import matplotlib.ticker as ticker
import numpy as np
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))

plt.show()