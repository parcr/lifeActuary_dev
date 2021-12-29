import numpy as np

period = 10
for m in range(1, 14):
    ts = np.arange(0, period + 1 / m, 1 / m)
    print(ts[:3], '...', ts[-3:])

print("\nWith Linespace")
for m in range(1, 14):
    ts = np.linspace(start=0, stop=period, num=m * period+1, endpoint=True)
    print(ts[:3], '...', ts[-3:])
