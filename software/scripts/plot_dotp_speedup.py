import re
import matplotlib.pyplot as plt
import numpy as np

# Function to parse the input data


def parse_data(data_str):
    pattern = r"(\w+) Dot Product duration with (\d+) elements: (\d+)"
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
data_gcc_str = """
Sequential Dot Product duration with 1 elements: 44
Parallel Dot Product duration with 1 elements: 434
Sequential Dot Product duration with 2 elements: 50
Parallel Dot Product duration with 2 elements: 391
Sequential Dot Product duration with 4 elements: 77
Parallel Dot Product duration with 4 elements: 409
Sequential Dot Product duration with 8 elements: 103
Parallel Dot Product duration with 8 elements: 397
Sequential Dot Product duration with 16 elements: 199
Parallel Dot Product duration with 16 elements: 465
Sequential Dot Product duration with 32 elements: 385
Parallel Dot Product duration with 32 elements: 413
Sequential Dot Product duration with 64 elements: 711
Parallel Dot Product duration with 64 elements: 423
Sequential Dot Product duration with 128 elements: 1409
Parallel Dot Product duration with 128 elements: 532
Sequential Dot Product duration with 256 elements: 2775
Parallel Dot Product duration with 256 elements: 601
Sequential Dot Product duration with 512 elements: 5532
Parallel Dot Product duration with 512 elements: 746
Sequential Dot Product duration with 1024 elements: 11041
Parallel Dot Product duration with 1024 elements: 1209
Sequential Dot Product duration with 2048 elements: 22049
Parallel Dot Product duration with 2048 elements: 1833
"""

data_llvm_str = """
Sequential Dot Product duration with 1 elements: 42
Parallel Dot Product duration with 1 elements: 1056
Sequential Dot Product duration with 2 elements: 45
Parallel Dot Product duration with 2 elements: 1048
Sequential Dot Product duration with 4 elements: 71
Parallel Dot Product duration with 4 elements: 1024
Sequential Dot Product duration with 8 elements: 123
Parallel Dot Product duration with 8 elements: 999
Sequential Dot Product duration with 16 elements: 226
Parallel Dot Product duration with 16 elements: 1025
Sequential Dot Product duration with 32 elements: 422
Parallel Dot Product duration with 32 elements: 1029
Sequential Dot Product duration with 64 elements: 835
Parallel Dot Product duration with 64 elements: 1042
Sequential Dot Product duration with 128 elements: 1651
Parallel Dot Product duration with 128 elements: 1054
Sequential Dot Product duration with 256 elements: 3283
Parallel Dot Product duration with 256 elements: 1193
Sequential Dot Product duration with 512 elements: 6547
Parallel Dot Product duration with 512 elements: 1356
Sequential Dot Product duration with 1024 elements: 13075
Parallel Dot Product duration with 1024 elements: 1774
Sequential Dot Product duration with 2048 elements: 26123
Parallel Dot Product duration with 2048 elements: 2627
"""

# Parse the data
data_gcc = parse_data(data_gcc_str)
data_llvm = parse_data(data_llvm_str)

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
    ax.set_title('Speedup of Parallel Dot Product against Sequential')
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.legend()
    ax.set_yticks(np.arange(0, max(max(speedup_parallel1.values()),
                  max(speedup_parallel2.values())) + 1, step=1))

    plt.tight_layout()
    plt.savefig(f'dotp_speedup.pdf')


# Sizes to be used for the x-axis
sizes = sorted(data_gcc['Sequential'].keys())

# Plot the speedup for parallel
plot_speedup_parallel(sizes, speedup_parallel_gcc, speedup_parallel_llvm)
