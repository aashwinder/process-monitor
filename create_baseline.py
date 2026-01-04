import psutil
import csv
import os

def create_baseline():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "baseline_processes.csv")

    # Baseline var mı?
    if os.path.exists(output_file):
        choice = input("?? Mevcut baseline bulundu. Üzerine yazılsın mı? (y/n): ").strip().lower()

    if choice != 'y':
        print("X Baseline oluşturma iptal edildi.")
        exit()

    baseline_processes = set()

    for process in psutil.process_iter(['name']):
        try:
            if process.info['name']:
                baseline_processes.add(process.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['process_name'])
        for name in sorted(baseline_processes):
            writer.writerow([name])

    print("Baseline oluşturuldu:", output_file)

# 👉 dosya direkt çalıştırılırsa
if __name__ == "__main__":
    create_baseline()