import numpy as np
import matplotlib.pyplot as plt

# data to plot
n_groups = 3

#all
# groups3 = (47, 255, 508)
# groups4 = (166, 760, 1556)
# groups8 = (10628, 59162, 105132)

#dynamic
# groups3 = (43, 227, 492)
# groups4 = (136, 737, 1535)
# groups8 = (8614, 52378, 102443)

# fixed
# groups3 = (1, 8, 15)
# groups4 = (3, 21, 38)
# groups8 = (187, 1010, 2002)

# hot groups
groups3 = (42, 213, 403)
groups4 = (106, 520, 1110)
groups8 = (4198, 20581, 42912)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.2
opacity = 0.8

rects1 = plt.bar(index, groups3, bar_width,
alpha=opacity,
color='b',
label='3 groups')

rects2 = plt.bar(index + bar_width, groups4, bar_width,
alpha=opacity,
color='g',
label='4 groups')

rects3 = plt.bar(index + 2 * bar_width, groups8, bar_width,
alpha=opacity,
color='r',
label='8 groups')

plt.xlabel('Items')
plt.ylabel('Time(ms)')
ax.set_yscale('log')

# plt.title('Scores by person')
plt.xticks(index + bar_width, ('100\'000', '500\'000', '1\'000\'000'))
plt.legend()
plt.tight_layout()
plt.show()