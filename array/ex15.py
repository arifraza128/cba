traffic = [320, 450, 600, 700, 520, 300, 250, 800]

peak = max(traffic)
hour = traffic.index(peak) + 1

minimum = min(traffic)
minhour = traffic.index(minimum) + 1

print("Peak Hour:", hour)
print("Peak Vehicles:", peak)

print("Minimum Hour:", minhour)
print("Minimum Vehicles:", minimum)

print("Total Traffic:", sum(traffic))

print("Hours Above 500 Vehicles:")

for i in range(len(traffic)):
    if traffic[i] > 500:
        print("Hour", i + 1, ":", traffic[i])