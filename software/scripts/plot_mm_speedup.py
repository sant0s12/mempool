import re
import matplotlib.pyplot as plt
import numpy as np

# Function to parse the input data


def parse_data(data_str):
    pattern = r"(\w+) MM Duration with size (\d+): (\d+)"
    data = re.findall(pattern, data_str)
    result = {'Sequential': {}, 'Parallel': {}}
    for d in data:
        method, size, duration = d
        result[method][int(size)] = int(duration)
    return result

# Function to calculate speedup


def calculate_speedup(sequential, other):
    return {size: sequential[size] / other[size] for size in sequential.keys()}


# Example input data
gcc_str = """
Sequential MM Duration with size 1: 75
Parallel MM Duration with size 1: 466
Sequential MM Duration with size 2: 174
Parallel MM Duration with size 2: 457
Sequential MM Duration with size 4: 831
Parallel MM Duration with size 4: 644
Sequential MM Duration with size 8: 6057
Parallel MM Duration with size 8: 1195
Sequential MM Duration with size 16: 46001
Parallel MM Duration with size 16: 3368
Sequential MM Duration with size 32: 359745
Parallel MM Duration with size 32: 24273
"""

llvm_str = """
Sequential MM Duration with size 1: 63
Parallel MM Duration with size 1: 1169
Sequential MM Duration with size 2: 179
Parallel MM Duration with size 2: 1096
Sequential MM Duration with size 4: 929
Parallel MM Duration with size 4: 1291
Sequential MM Duration with size 8: 6409
Parallel MM Duration with size 8: 1915
Sequential MM Duration with size 16: 47993
Parallel MM Duration with size 16: 4285
Sequential MM Duration with size 32: 371924
Parallel MM Duration with size 32: 26547
"""

# Parse the data
data_gcc = parse_data(gcc_str)
data_llvm = parse_data(llvm_str)

# Calculate speedup for data1 and data2
speedup_parallel_gcc = calculate_speedup(
    data_gcc['Sequential'], data_gcc['Parallel'])
speedup_parallel_llvm = calculate_speedup(
    data_llvm['Sequential'], data_llvm['Parallel'])

# Function to plot speedup


def plot_speedup_parallel(sizes, speedup_parallel1, speedup_parallel2):
    x = np.arange(len(sizes))  # label locations
    width = 0.35  # width of the bars

    fig, ax = plt.subplots(figsize=(6, 4))
    bars1 = ax.bar(x - width/2, [speedup_parallel1[size] for size in sizes],
                   width, label='GCC')
    bars2 = ax.bar(x + width/2, [speedup_parallel2[size] for size in sizes],
                   width, label='LLVM')

    ax.set_xlabel('Input Size')
    ax.set_ylabel('Speedup')
    ax.set_title('Speedup of Parallel MMM against Sequential')
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.legend()
    ax.set_yticks(np.arange(0, max(max(speedup_parallel1.values()),
                  max(speedup_parallel2.values())) + 1, step=1))

    plt.tight_layout()
    plt.savefig(f'mm_speedup.pdf')


# Sizes to be used for the x-axis
sizes = sorted(data_gcc['Sequential'].keys())

# Plot the speedup for parallel
plot_speedup_parallel(sizes, speedup_parallel_gcc, speedup_parallel_llvm)
