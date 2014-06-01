
from pylab import *
my_cmap = get_cmap('autumn')
pcolor(rand(10,10),cmap=my_cmap)
colorbar()
print 'foo'

matplotlib.pyplot.show()
