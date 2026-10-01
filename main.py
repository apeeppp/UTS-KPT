import os
import time
import argparse
import csv
from pathlib import Path
from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor
)

NAMA = "Muhammad Nazril Putra Rosida"
NIM = 247006111162

DATASET_DIR = Path("dataset")


def read_file(file_path):
    """
    I/O-bound task.
    Membaca satu file teks.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    return content


def analyze_text(text):
    """
    CPU-bound task.
    Menghitung statistik dari isi teks.
    """

    total_char = len(text)
    total_words = len(text.split())

    vowels = sum(
        1 for char in text.lower()
        if char in "aiueo"
    )

    digits = sum(
        1 for char in text
        if char.isdigit()
    )

    symbols = sum(
        1 for char in text
        if not char.isalnum() and not char.isspace()
    )

    uppercase = sum(
        1 for char in text
        if char.isupper()
    )

    lowercase = sum(
        1 for char in text
        if char.islower()
    )

    # Perhitungan tambahan untuk meningkatkan
    # beban CPU pada proses analisis.
    checksum = 0

    for char in text:
        checksum = (checksum * 31 + ord(char)) % 1000000007

    return {
        "characters": total_char,
        "words": total_words,
        "vowels": vowels,
        "digits": digits,
        "symbols": symbols,
        "uppercase": uppercase,
        "lowercase": lowercase,
        "checksum": checksum
    }


def merge_results(results):
    """
    Menggabungkan hasil dari seluruh process.
    """

    total = {
        "characters": 0,
        "words": 0,
        "vowels": 0,
        "digits": 0,
        "symbols": 0,
        "uppercase": 0,
        "lowercase": 0,
        "checksum": 0
    }

    for result in results:
        total["characters"] += result["characters"]
        total["words"] += result["words"]
        total["vowels"] += result["vowels"]
        total["digits"] += result["digits"]
        total["symbols"] += result["symbols"]
        total["uppercase"] += result["uppercase"]
        total["lowercase"] += result["lowercase"]
        total["checksum"] += result["checksum"]

    return total


def sequential_execution(file_paths):
    """
    Baseline tanpa paralelisme.
    """

    contents = []

    for file_path in file_paths:
        contents.append(read_file(file_path))

    results = []

    for content in contents:
        results.append(analyze_text(content))

    return merge_results(results)


def hybrid_execution(file_paths, thread_count, process_count):
    """
    Hybrid computing:
    Thread Pool -> I/O
    Process Pool -> CPU
    """

    # Tahap 1: I/O menggunakan Thread Pool
    with ThreadPoolExecutor(
        max_workers=thread_count
    ) as executor:

        contents = list(
            executor.map(read_file, file_paths)
        )

    # Tahap 2: CPU-bound menggunakan Process Pool
    with ProcessPoolExecutor(
        max_workers=process_count
    ) as executor:

        results = list(
            executor.map(analyze_text, contents)
        )

    return merge_results(results)


def calculate_metrics(total_data, execution_time, baseline_time, process_count):
    """
    Menghitung throughput, speedup dan efisiensi.
    """

    throughput = total_data / execution_time

    speedup = baseline_time / execution_time

    efficiency = (speedup / process_count) * 100

    return throughput, speedup, efficiency


def get_files(total_data):
    files = sorted(DATASET_DIR.glob("*.txt"))

    if len(files) < total_data:
        raise FileNotFoundError(
            f"Dataset hanya memiliki {len(files)} file. "
            f"Dibutuhkan {total_data} file."
        )

    return files[:total_data]

def run_benchmark():
    configurations = [
        (2, 2, 540),
        (4, 2, 540),
        (4, 3, 540),
        (2, 2, 1080),
        (4, 2, 1080),
        (4, 3, 1080),
        (4, 2, 1620),
        (4, 3, 1620),
        (6, 3, 1620),
        (8, 3, 1620),
    ]

    results = []

    print("=" * 80)
    print("BENCHMARK PARALLEL FILE ANALYZER")
    print("=" * 80)

    for i, (threads, processes, data_count) in enumerate(configurations, start=1):

        file_paths = get_files(data_count)

        # Sequential baseline
        start = time.perf_counter()
        sequential_execution(file_paths)
        baseline_time = time.perf_counter() - start

        # Hybrid
        start = time.perf_counter()
        hybrid_execution(
            file_paths,
            threads,
            processes
        )
        hybrid_time = time.perf_counter() - start

        throughput = data_count / hybrid_time
        speedup = baseline_time / hybrid_time
        efficiency = (speedup / processes) * 100

        results.append({
            "No": i,
            "Thread": threads,
            "Process": processes,
            "Data": data_count,
            "Waktu": round(hybrid_time, 4),
            "Speedup": round(speedup, 2),
            "Efisiensi": round(efficiency, 2),
            "Throughput": round(throughput, 2)
        })

        print(
            f"{i:2}. "
            f"Thread={threads} | "
            f"Process={processes} | "
            f"Data={data_count} | "
            f"Waktu={hybrid_time:.4f}s | "
            f"Speedup={speedup:.2f}x | "
            f"Efisiensi={efficiency:.2f}%"
        )

    # Simpan hasil ke CSV
    with open(
        "benchmark_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "No",
                "Thread",
                "Process",
                "Data",
                "Waktu",
                "Speedup",
                "Efisiensi",
                "Throughput"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print()
    print("Hasil tersimpan di: benchmark_results.csv")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Parallel File Analyzer"
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=4
    )

    parser.add_argument(
        "--processes",
        type=int,
        default=3
    )

    parser.add_argument(
        "--data",
        type=int,
        default=1620
    )

    parser.add_argument(
        "--bench",
        action="store_true"
    )

    args = parser.parse_args()

    if args.bench:
        run_benchmark()
        return

    file_paths = get_files(args.data)

    print("=" * 60)
    print("PARALLEL FILE ANALYZER")
    print("=" * 60)

    print(f"Nama           : {NAMA}")
    print(f"NIM            : {NIM}")
    print(f"Jumlah Data    : {args.data}")
    print(f"Jumlah Thread  : {args.threads}")
    print(f"Jumlah Process : {args.processes}")
    print()

    # Baseline sequential
    start = time.perf_counter()

    sequential_result = sequential_execution(file_paths)

    baseline_time = time.perf_counter() - start

    # Hybrid execution
    start = time.perf_counter()

    hybrid_result = hybrid_execution(
        file_paths,
        args.threads,
        args.processes
    )

    execution_time = time.perf_counter() - start

    throughput, speedup, efficiency = calculate_metrics(
        args.data,
        execution_time,
        baseline_time,
        args.processes
    )

    print("HASIL ANALISIS")
    print("-" * 60)

    print(
        f"Total karakter : "
        f"{hybrid_result['characters']:,}"
    )

    print(
        f"Total kata     : "
        f"{hybrid_result['words']:,}"
    )

    print(
        f"Total vokal    : "
        f"{hybrid_result['vowels']:,}"
    )

    print(
        f"Total angka    : "
        f"{hybrid_result['digits']:,}"
    )

    print(
        f"Total simbol   : "
        f"{hybrid_result['symbols']:,}"
    )

    print()

    print("PERFORMA")
    print("-" * 60)

    print(
        f"Waktu Sequential : "
        f"{baseline_time:.4f} detik"
    )

    print(
        f"Waktu Hybrid     : "
        f"{execution_time:.4f} detik"
    )

    print(
        f"Throughput       : "
        f"{throughput:.2f} data/detik"
    )

    print(
        f"Speedup          : "
        f"{speedup:.2f}x"
    )

    print(
        f"Efisiensi        : "
        f"{efficiency:.2f}%"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()