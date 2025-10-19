#!/usr/bin/env python3
"""
IO-Bound Execution Performance Visualization

This script generates comprehensive plots comparing different concurrency models
(sync, asyncio, threading, hybrid) for IO-bound tasks.

Metrics visualized:
- Execution time
- Download speed
- CPU usage (process and system)
- Memory usage
- Failed requests
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def load_json_data(file_path):
    """Load and return JSON data from file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def extract_io_metrics(data):
    """Extract key metrics from IO-bound benchmark data."""
    return {
        'elapsed_seconds': data['elapsed_seconds'],
        'download_speed_kbps': data['total_download'] / data['elapsed_seconds'] / 1024,
        'upload_speed_kbps': data['total_upload'] / data['elapsed_seconds'] / 1024,
        'total_downloaded_mb': data['total_download'] / (1024 * 1024),
        'failed_requests': data['returned_value(s)'][1],
        'cpu_proc_avg': data['cpu']['proc_average_usage'],
        'cpu_proc_max': data['cpu']['proc_max_usage'],
        'cpu_sys_avg': data['cpu']['sys_average_usage'],
        'cpu_sys_max': data['cpu']['sys_max_usage'],
        'memory_avg_mb': data['memory']['average_usage'] / (1024 * 1024),
        'memory_max_mb': data['memory']['max_usage'] / (1024 * 1024),
    }


def load_io_bound_data():
    """Load specific IO-bound benchmark results for comparison."""
    json_dir = Path(__file__).parent / 'io-bound' / 'json'
    
    data = {}
    
    # Sync: 1,000 URLs
    sync_file = json_dir / 'sync_data_with_1000_urls.json'
    if sync_file.exists():
        data['Sync\n(1K URLs)'] = extract_io_metrics(load_json_data(sync_file))
    
    # Asyncio: 10,000 URLs
    asyncio_file = json_dir / 'asyncio_data_with_10000_urls.json'
    if asyncio_file.exists():
        data['Asyncio\n(10K URLs)'] = extract_io_metrics(load_json_data(asyncio_file))
    
    # Threading: 100 threads with 10,000 URLs
    thread_file = json_dir / '100_threads_data_with_10_000_urls.json'
    if thread_file.exists():
        data['Threading\n(100 threads, 10K URLs)'] = extract_io_metrics(load_json_data(thread_file))
    
    # Hybrid: 10 threads + asyncio with 10,000 URLs
    hybrid_file = json_dir / '10_threads_plus_asyncio_with_10_000_urls.json'
    if hybrid_file.exists():
        data['Hybrid\n(10 threads + asyncio, 10K URLs)'] = extract_io_metrics(load_json_data(hybrid_file))
    
    return data


def plot_execution_time(data, ax):
    """Plot execution time comparison."""
    models = list(data.keys())
    times = [data[model]['elapsed_seconds'] for model in models]
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
    
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
    
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')


def plot_download_speed(data, ax):
    """Plot download speed comparison."""
    models = list(data.keys())
    speeds = [data[model]['download_speed_kbps'] for model in models]
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
    
    bars = ax.bar(models, speeds, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Download Speed (KB/s)', fontsize=12, fontweight='bold')
    ax.set_title('Download Speed Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, max(speeds) * 1.15)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f} KB/s',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')


def plot_cpu_usage(data, ax):
    """Plot CPU usage comparison (process and system)."""
    models = list(data.keys())
    proc_avg = [data[model]['cpu_proc_avg'] for model in models]
    sys_avg = [data[model]['cpu_sys_avg'] for model in models]
    
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
    
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')


def plot_memory_usage(data, ax):
    """Plot memory usage comparison."""
    models = list(data.keys())
    memory = [data[model]['memory_avg_mb'] for model in models]
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
    
    bars = ax.bar(models, memory, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Memory (MB)', fontsize=12, fontweight='bold')
    ax.set_title('Memory Usage Comparison (Average)', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, max(memory) * 1.15)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f} MB',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')


def plot_failed_requests(data, ax):
    """Plot failed requests comparison."""
    models = list(data.keys())
    failed = [data[model]['failed_requests'] for model in models]
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
    
    bars = ax.bar(models, failed, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Failed Requests', fontsize=12, fontweight='bold')
    ax.set_title('Failed Requests Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, max(failed) * 1.15 if max(failed) > 0 else 20)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')


def create_individual_plots(data, output_dir):
    """Create separate, focused plot for each metric."""
    plots_created = []
    
    # 1. Execution Time Plot
    fig1, ax1 = plt.subplots(figsize=(12, 7))
    plot_execution_time(data, ax1)
    fig1.suptitle('IO-Bound Execution: Execution Time Comparison\n(HTTP Requests)',
                  fontsize=14, fontweight='bold', y=0.98)
    fig1.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_file1 = output_dir / 'io_bound_execution_time.png'
    fig1.savefig(output_file1, dpi=300, bbox_inches='tight')
    plots_created.append(output_file1)
    plt.close(fig1)
    
    # 2. Download Speed Plot
    fig2, ax2 = plt.subplots(figsize=(12, 7))
    plot_download_speed(data, ax2)
    fig2.suptitle('IO-Bound Execution: Download Speed Comparison\n(HTTP Requests)',
                  fontsize=14, fontweight='bold', y=0.98)
    fig2.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_file2 = output_dir / 'io_bound_download_speed.png'
    fig2.savefig(output_file2, dpi=300, bbox_inches='tight')
    plots_created.append(output_file2)
    plt.close(fig2)
    
    # 3. CPU Usage Plot
    fig3, ax3 = plt.subplots(figsize=(12, 7))
    plot_cpu_usage(data, ax3)
    fig3.suptitle('IO-Bound Execution: CPU Usage Comparison\n(HTTP Requests)',
                  fontsize=14, fontweight='bold', y=0.98)
    fig3.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_file3 = output_dir / 'io_bound_cpu_usage.png'
    fig3.savefig(output_file3, dpi=300, bbox_inches='tight')
    plots_created.append(output_file3)
    plt.close(fig3)
    
    # 4. Memory Usage Plot
    fig4, ax4 = plt.subplots(figsize=(12, 7))
    plot_memory_usage(data, ax4)
    fig4.suptitle('IO-Bound Execution: Memory Usage Comparison\n(HTTP Requests)',
                  fontsize=14, fontweight='bold', y=0.98)
    fig4.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_file4 = output_dir / 'io_bound_memory_usage.png'
    fig4.savefig(output_file4, dpi=300, bbox_inches='tight')
    plots_created.append(output_file4)
    plt.close(fig4)
    
    # 5. Failed Requests Plot
    fig5, ax5 = plt.subplots(figsize=(12, 7))
    plot_failed_requests(data, ax5)
    fig5.suptitle('IO-Bound Execution: Failed Requests Comparison\n(HTTP Requests)',
                  fontsize=14, fontweight='bold', y=0.98)
    fig5.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_file5 = output_dir / 'io_bound_failed_requests.png'
    fig5.savefig(output_file5, dpi=300, bbox_inches='tight')
    plots_created.append(output_file5)
    plt.close(fig5)
    
    return plots_created


def main():
    """Main execution function."""
    print("Loading IO-bound benchmark data...")
    data = load_io_bound_data()
    
    print(f"Found data for {len(data)} configurations:")
    for model in data.keys():
        print(f"  ✓ {model}")
    
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
