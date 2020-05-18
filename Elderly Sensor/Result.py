import matplotlib.pyplot as plt
import numpy

session = 41
filename = "C:\\Users\\YigitCan\\Desktop\\Tez-Workspace\\Real-Time-Big-Data-Analytics\\Elderly Sensor\\Output"+str(session)+".txt"
results = numpy.genfromtxt(filename, delimiter=',')
timeList = [e[4] for e in results]
mseList = [e[0] for e in results]
accList = [e[1] for e in results]

fig3, (ax3, ax4) = plt.subplots(1,2,sharey=True, sharex=True,figsize=(10,5))

line3, = ax3.plot(timeList, mseList)
line4, = ax4.plot(timeList, accList)

ax3.set_ylabel('MSE')
ax3.set_xlabel("Time")
ax4.set_ylabel("Accuracy Score")
ax4.set_xlabel("Time")

ax3.grid(True)
ax4.grid(True)

plt.subplots_adjust(bottom = 0.2)

plt.title("Session: " + str(session))
plt.show()