import matplotlib.pyplot as plt

# mse for first set of epsilon
cdp_mse = [95500.63, 9774.87, 332.49, 281.17]
ldp_mse = [404631.42, 39311.42, 470.14, 309.78]

# first set of epsilon
epsilon_values = [0.5, 1, 5, 10]

# new data for completion
new_epsilon_values = [2, 3, 4, 6, 7, 8, 9]
new_cdp_mse = [1243.0, 585.51, 379.39, 249.39, 295.73, 296.2, 259.31]
new_ldp_mse = [6061.30, 1945.15, 654.79, 404.59, 340.25, 357.22, 328.94]

epsilon_values.extend(new_epsilon_values)
cdp_mse.extend(new_cdp_mse)
ldp_mse.extend(new_ldp_mse)

# sort the data
epsilon_values.sort()

plt.figure(figsize=(8, 6))

plt.plot(epsilon_values, cdp_mse, label='CDP', marker='o', color='b', linestyle='-', linewidth=2)
plt.plot(epsilon_values, ldp_mse, label='LDP', marker='o', color='r', linestyle='-', linewidth=2)

plt.xlabel('ε (Epsilon)', fontsize=12)
plt.ylabel('Mean Squared Error (MSE)', fontsize=12)
plt.title('MSE vs. Epsilon for CDP and LDP', fontsize=14)

plt.legend()

plt.grid(True)

# Save the plot
plt.savefig("../output/mse_vs_epsilon.png")

# Show the plot (optional)
# plt.show()
