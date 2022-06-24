import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib.animation as animation
import matplotlib.pyplot as plt 
from itertools import count

x_=[]
y_ = []
#step = count()

def animate(i):
    x_.append(i) 
    y_.append(np.random.randint(0,5))
    plt.plot(x_,y_) 

ani = animation.FuncAnimation(plt.gcf(),animate,interval=1000)
plt.show()