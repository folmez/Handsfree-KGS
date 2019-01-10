import matplotlib.pyplot as plt

xy=[]

def onclick(event):
    print(event.xdata, event.ydata)
    xy.append((event.xdata, event.ydata))

fig = plt.figure()
plt.plot(range(10))
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

print(xy)
