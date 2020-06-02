import matplotlib.pyplot as plt
import numpy

session = 49
filename = "C:\\Users\\YigitCan\\Desktop\\Tez-Workspace\\Real-Time-Big-Data-Analytics\\Elderly Sensor\\Output"+str(session)+".txt"
results = numpy.genfromtxt(filename, delimiter=',')



timeList = [e[4] for e in results]
mseList = [e[0] for e in results]
accList = [e[1] for e in results]





fig3, (ax3, ax4) = plt.subplots(1,2,sharey=True, sharex=True,figsize=(10,5))

line3, = ax3.plot(timeList, mseList)
line4, = ax4.plot(timeList, accList)

realColumnList = [e[2] for e in results]
labelColor = ('g', 'y', 'r', 'm')


uniqueList = []
for i in range(0, len(results), 5):
    label = int(results[i][2])
    ax3.plot(timeList[i], mseList[i], labelColor[label-1] + 'o')
    #ax3.text(timeList[i], mseList[i], label)

'''
# This code snippet checks the next 100 element after a point and if any label has domination, it adds point into graph
temp = []
for i in range(len(results)):
    label = results[i][2]
    if label in temp:
        continue
    if len(results) < i+102:
        break
    next_window = [e[2] for e in results[i+1:i+102]]
    
    
    if next_window.count(label) > 80:
        temp.append(label)
        ax3.plot(timeList[i], mseList[i], 'o')
        ax3.text(timeList[i], mseList[i], label)
'''
'''
# This code snippet adds the point where each label first occur into graph
for label in [1,2,3,4]:
    labelIndex = realColumnList.index(label)
    if label != -1:
        ax3.plot(timeList[labelIndex], mseList[labelIndex], 'o')
        ax3.text(timeList[labelIndex], mseList[labelIndex], label)
        ax4.plot(timeList[labelIndex], accList[labelIndex], 'o')
        ax4.text(timeList[labelIndex], accList[labelIndex], label)
'''
ax3.set_ylabel('MSE')
ax3.set_xlabel("Time")
ax4.set_ylabel("Accuracy Score")
ax4.set_xlabel("Time")

ax3.grid(True)
ax4.grid(True)

plt.subplots_adjust(bottom = 0.2)

plt.title("Session: " + str(session))
plt.show()