#!/usr/bin/env python3
"""
CPU-Bound Execution Performance Visualization

This script generates comprehensive plots comparing different concurrency models
(sync, asyncio, threading) for CPU-bound tasks.

Metrics visualized:
- Execution time
- CPU usage (process and system)
- Memory usage
- Performance comparison across thread counts
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def load_json_data(file_path):
    """Load and return JSON data from file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def extract_metrics(data):
    """Extract key metrics from benchmark data."""
    return {
        'elapsed_seconds': data['elapsed_seconds'],
        'cpu_proc_avg': data['cpu']['proc_average_usage'],
        'cpu_proc_max': data['cpu']['proc_max_usage'],
        'cpu_sys_avg': data['cpu']['sys_average_usage'],
        'cpu_sys_max': data['cpu']['sys_max_usage'],
        'memory_mb': data['memory']['max_usage'] / (1024 * 1024),
        'returned_value': data['returned_value(s)']
    }


def load_all_cpu_bound_data():
    """Load all CPU-bound benchmark results."""
    json_dir = Path(__file__).parent / 'cpu-bound' / 'json'
    
    data = {
        'sync': None,
        'asyncio': None,
        'threads': {}
    }
    
    # Load sync data
    sync_file = json_dir / 'sync_data.json'
    if sync_file.exists():
        data['sync'] = extract_metrics(load_json_data(sync_file))
    
    # Load asyncio data
    asyncio_file = json_dir / 'asyncio_data.json'
    if asyncio_file.exists():
        data['asyncio'] = extract_metrics(load_json_data(asyncio_file))
    
    # Load threading data
    for thread_file in json_dir.glob('*_threads_data.json'):
        thread_count = int(thread_file.stem.split('_')[0])
        data['threads'][thread_count] = extract_metrics(load_json_data(thread_file))
    
    return data


def plot_execution_time(data, ax):
    """Plot execution time comparison."""
    models = []
    times = []
    colors = []
    
    # Sync
    if data['sync']:
        models.append('Sync')
        times.append(data['sync']['elapsed_seconds'])
        colors.append('#2ecc71')
    
    # Asyncio
    if data['asyncio']:
        models.append('Asyncio')
        times.append(data['asyncio']['elapsed_seconds'])
        colors.append('#3498db')
    
    # Threading (sorted by thread count)
    for thread_count in sorted(data['threads'].keys()):
        models.append(f'{thread_count} Threads')
        times.append(data['threads'][thread_count]['elapsed_seconds'])
        colors.append('#e74c3c')
    
    bars = ax.bar(models, times, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Execution Time Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, max(times) * 1.15)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}s',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def plot_cpu_usage(data, ax):
    """Plot CPU usage comparison (process and system)."""
    models = []
    proc_avg = []
    sys_avg = []
    
    # Sync
    if data['sync']:
        models.append('Sync')
        proc_avg.append(data['sync']['cpu_proc_avg'])
        sys_avg.append(data['sync']['cpu_sys_avg'])
    
    # Asyncio
    if data['asyncio']:
        models.append('Asyncio')
        proc_avg.append(data['asyncio']['cpu_proc_avg'])
        sys_avg.append(data['asyncio']['cpu_sys_avg'])
    
    # Threading
    for thread_count in sorted(data['threads'].keys()):
        models.append(f'{thread_count}T')
        proc_avg.append(data['threads'][thread_count]['cpu_proc_avg'])
        sys_avg.append(data['threads'][thread_count]['cpu_sys_avg'])
    
    x = np.arange(len(models))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, proc_avg, width, label='Process CPU', 
                   color='#e74c3c', alpha=0.7, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, sys_avg, width, label='System CPU',
                   color='#3498db', alpha=0.7, edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('CPU Usage (%)', fontsize=12, fontweight='bold')
    ax.set_title('CPU Usage Comparison (Average)', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def plot_memory_usage(data, ax):
    """Plot memory usage comparison."""
    models = []
    memory = []
    colors = []
    
    # Sync
    if data['sync']:
        models.append('Sync')
        memory.append(data['sync']['memory_mb'])
        colors.append('#2ecc71')
    
    # Asyncio
    if data['asyncio']:
        models.append('Asyncio')
        memory.append(data['asyncio']['memory_mb'])
        colors.append('#3498db')
    
    # Threading
    for thread_count in sorted(data['threads'].keys()):
        models.append(f'{thread_count} Threads')
        memory.append(data['threads'][thread_count]['memory_mb'])
        colors.append('#e74c3c')
    
    bars = ax.bar(models, memory, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Memory (MB)', fontsize=12, fontweight='bold')
    ax.set_title('Memory Usage Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, max(memory) * 1.15)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f} MB',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

def create_individual_plots(data, output_dir):
    """Create separate, focused plot for each metric."""
    plots_created = []
    
    # 1. Execution Time Plot
    fig1, ax1 = plt.subplots(figsize=(10, 7))
    plot_execution_time(data, ax1)
    fig1.suptitle('CPU-Bound Execution: Execution Time Comparison\n(Character Encoding - 100,000 URLs)',
                  fontsize=14, fontweight='bold', y=0.98)
    fig1.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_file1 = output_dir / 'cpu_bound_execution_time.png'
    fig1.savefig(output_file1, dpi=300, bbox_inches='tight')
    plots_created.append(output_file1)
    plt.close(fig1)
    
    # 2. CPU Usage Plot
    fig2, ax2 = plt.subplots(figsize=(10, 7))
    plot_cpu_usage(data, ax2)
    fig2.suptitle('CPU-Bound Execution: CPU Usage Comparison\n(Character Encoding - 100,000 URLs)',
                  fontsize=14, fontweight='bold', y=0.98)
    fig2.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_file2 = output_dir / 'cpu_bound_cpu_usage.png'
    fig2.savefig(output_file2, dpi=300, bbox_inches='tight')
    plots_created.append(output_file2)
    plt.close(fig2)
    
    # 3. Memory Usage Plot
    fig3, ax3 = plt.subplots(figsize=(10, 7))
    plot_memory_usage(data, ax3)
    fig3.suptitle('CPU-Bound Execution: Memory Usage Comparison\n(Character Encoding - 100,000 URLs)',
                  fontsize=14, fontweight='bold', y=0.98)
    fig3.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_file3 = output_dir / 'cpu_bound_memory_usage.png'
    fig3.savefig(output_file3, dpi=300, bbox_inches='tight')
    plots_created.append(output_file3)
    plt.close(fig3)
    
    return plots_created


def main():
    """Main execution function."""
    print("Loading CPU-bound benchmark data...")
    data = load_all_cpu_bound_data()
    
    print(f"Found data for:")
    print(f"  - Sync: {'✓' if data['sync'] else '✗'}")
    print(f"  - Asyncio: {'✓' if data['asyncio'] else '✗'}")
    print(f"  - Threading: {len(data['threads'])} configurations")
    
    print("\nGenerating individual plots for each metric...")
    
    # Create output directory
    output_dir = Path(__file__).parent / 'plots'
    output_dir.mkdir(exist_ok=True)
    
    # Generate all plots
    plots_created = create_individual_plots(data, output_dir)
    
    print(f"\n✓ Successfully created {len(plots_created)} plots:")
    for plot_file in plots_created:
        print(f"  • {plot_file.name}")
    
    print(f"\n✓ All plots saved to: {output_dir}/")
    print("\n✓ Done!")


if __name__ == "__main__":
    main()
