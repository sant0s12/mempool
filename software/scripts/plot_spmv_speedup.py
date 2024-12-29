import re
import matplotlib.pyplot as plt
import numpy as np

# Function to parse the input data


def parse_data(data_str):
    pattern = r"(\w+) SPMV Duration with size (\d+): (\d+)"
    data = re.findall(pattern, data_str)
    result = {'Sequential': {}, 'Static': {}, 'Dynamic': {}}
    for d in data:
        method, size, duration = d
        result[method][int(size)] = int(duration)
    return result

# Function to calculate speedup


def calculate_speedup(sequential, other):
    return {size: sequential[size] / other[size] for size in sequential.keys()}


# Parse the input data
gcc_str = """
Sequential SPMV Duration with size 1: 100
Static SPMV Duration with size 1: 673
Dynamic SPMV Duration with size 1: 1294
Sequential SPMV Duration with size 2: 116
Static SPMV Duration with size 2: 503
Dynamic SPMV Duration with size 2: 1093
Sequential SPMV Duration with size 4: 139
Static SPMV Duration with size 4: 566
Dynamic SPMV Duration with size 4: 1063
Sequential SPMV Duration with size 8: 213
Static SPMV Duration with size 8: 562
Dynamic SPMV Duration with size 8: 1082
Sequential SPMV Duration with size 16: 365
Static SPMV Duration with size 16: 548
Dynamic SPMV Duration with size 16: 1144
Sequential SPMV Duration with size 32: 669
Static SPMV Duration with size 32: 585
Dynamic SPMV Duration with size 32: 1086
Sequential SPMV Duration with size 64: 2399
Static SPMV Duration with size 64: 903
Dynamic SPMV Duration with size 64: 1214
Sequential SPMV Duration with size 128: 8732
Static SPMV Duration with size 128: 2378
Dynamic SPMV Duration with size 128: 2074
Sequential SPMV Duration with size 256: 32774
Static SPMV Duration with size 256: 8066
Dynamic SPMV Duration with size 256: 5292
Sequential SPMV Duration with size 512: 138608
Static SPMV Duration with size 512: 43642
Dynamic SPMV Duration with size 512: 21219
"""

llvm_str = """
Sequential SPMV Duration with size 1: 51
Static SPMV Duration with size 1: 1429
Dynamic SPMV Duration with size 1: 2653
Sequential SPMV Duration with size 2: 64
Static SPMV Duration with size 2: 1128
Dynamic SPMV Duration with size 2: 2288
Sequential SPMV Duration with size 4: 101
Static SPMV Duration with size 4: 1160
Dynamic SPMV Duration with size 4: 2273
Sequential SPMV Duration with size 8: 190
Static SPMV Duration with size 8: 1127
Dynamic SPMV Duration with size 8: 2282
Sequential SPMV Duration with size 16: 358
Static SPMV Duration with size 16: 1151
Dynamic SPMV Duration with size 16: 2638
Sequential SPMV Duration with size 32: 694
Static SPMV Duration with size 32: 1185
Dynamic SPMV Duration with size 32: 2594
Sequential SPMV Duration with size 64: 2626
Static SPMV Duration with size 64: 2109
Dynamic SPMV Duration with size 64: 3052
Sequential SPMV Duration with size 128: 9436
Static SPMV Duration with size 128: 2537
Dynamic SPMV Duration with size 128: 4639
Sequential SPMV Duration with size 256: 34817
Static SPMV Duration with size 256: 12433
Dynamic SPMV Duration with size 256: 10553
Sequential SPMV Duration with size 512: 145254
Static SPMV Duration with size 512: 54505
Dynamic SPMV Duration with size 512: 12361
"""

# Parse the data
data_llvm = parse_data(llvm_str)
data_gcc = parse_data(gcc_str)

# Calculate speedup for data1 and data2
speedup_static_llvm = calculate_speedup(
    data_llvm['Sequential'], data_llvm['Static'])
speedup_dynamic_llvm = calculate_speedup(
    data_llvm['Sequential'], data_llvm['Dynamic'])
speedup_static_gcc = calculate_speedup(
    data_gcc['Sequential'], data_gcc['Static'])
speedup_dynamic_gcc = calculate_speedup(
    data_gcc['Sequential'], data_gcc['Dynamic'])

# Function to plot speedup


def plot_speedup_static(sizes, speedup_static_gcc, speedup_static_llvm):
    x = np.arange(len(sizes))  # label locations
    width = 0.35  # width of the bars

    plt.figure(figsize=(5, 4))

    fig, ax = plt.subplots(figsize=(5, 4))
    bars1 = ax.bar(x - width/2, [speedup_static_gcc[size] for size in sizes],
                   width, label='GCC')
    bars2 = ax.bar(x + width/2, [speedup_static_llvm[size] for size in sizes],
                   width, label='LLVM')

    ax.set_xlabel('Input Size')
    ax.set_ylabel('Speedup')
    ax.set_title('Speedup of Static SPMV against Sequential')
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.set_yticks(np.arange(0, max(max(speedup_static_llvm.values()),
                                   max(speedup_static_gcc.values())) + 1, step=1))
    ax.legend()

    plt.tight_layout()
    plt.savefig(f'spvm_speedup_static.pdf')


def plot_speedup_dynamic(sizes, speedup_dynamic_gcc, speedup_dynamic_llvm):
    x = np.arange(len(sizes))  # label locations
    width = 0.35  # width of the bars

    plt.figure(figsize=(5, 4))

    fig, ax = plt.subplots(figsize=(5, 4))
    bars1 = ax.bar(x - width/2, [speedup_dynamic_gcc[size]
                   for size in sizes], width, label='GCC')
    bars2 = ax.bar(x + width/2, [speedup_dynamic_llvm[size]
                   for size in sizes], width, label='LLVM')
    ax.set_xlabel('Input Size')
    ax.set_ylabel('Speedup')
    ax.set_title('Speedup of Dynamic SPMV against Sequential')
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.set_yticks(np.arange(0, max(max(speedup_dynamic_gcc.values()),
                                   max(speedup_dynamic_llvm.values())) + 1, step=1))
    ax.legend()

    plt.tight_layout()
    plt.savefig(f'spvm_speedup_dynamic.pdf')


# Sizes to be used for the x-axis
sizes = sorted(data_llvm['Sequential'].keys())

# Plot the speedup for static and dynamic separately
plot_speedup_static(sizes, speedup_static_gcc, speedup_static_llvm)
plot_speedup_dynamic(sizes, speedup_dynamic_gcc, speedup_dynamic_llvm)
