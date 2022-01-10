import matplotlib.pyplot as plt

with open('scripts/training.log') as fp:
    i = 0
    loss = []
    line = fp.readline().strip()
    while line or i < 10:
        if line.startswith('Progress:'):
            i += 1
            columns = line.split()
            loss.append(float(columns[7]))
        line = fp.readline().strip()

plt.plot(loss)
plt.show()
