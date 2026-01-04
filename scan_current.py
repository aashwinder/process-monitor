import psutil
import csv
import os

def scan_current():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    baseline_file = os.path.join(BASE_DIR, "baseline_processes.csv")

    # Baseline process isimlerini getir
    baseline_processes = set()

    reported = set()

    # Baseline'ı oku
    with open(baseline_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Başlık satırını atla
        for row in reader:
            baseline_processes.add(row[0])

    # Güvenli kabul edilen dizinler
    SAFE_PATHS = ["C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)", "C:\\ProgramData\\Microsoft"]
    WINDOWS_CORE_PROCESSES = [
        "smss.exe", "csrss.exe", "wininit.exe", "services.exe", 
        "lsass.exe", "svchost.exe", "explorer.exe", "winlogon.exe", 
        "dwm.exe", "taskhostw.exe", "sihost.exe"
    ]

    print("\n!!! Baseline'da olmayan veya şüpheli PATH'e sahip process'ler:")

    alert_found = False

    for proc in psutil.process_iter(['name', 'exe']):
        try:
            name = proc.info['name']
            exe_path = proc.info['exe'] or ""
            
            if ":" not in exe_path:
                continue  # Geçersiz exe yolu

            if name in WINDOWS_CORE_PROCESSES:
                continue  # Windows çekirdek process'lerini yoksay

            # Aynı process’i 10 kere yazmasını engelleyelim
            key = (name, exe_path)
            if key in reported:
                continue  # Zaten raporlandı
            reported.add(key)

            # Baseline'da yoksa
            if name not in baseline_processes:
                print(f"\n! Yeni process: {name} | Path: {exe_path}")
                alert_found = True
                continue
            # Baseline'da var ama PATH şüpheli ise
            if not any(exe_path.startswith(safe) for safe in SAFE_PATHS):
                print(f"\n? Şüpheli PATH: {name} | Path: {exe_path}")
                alert_found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if not alert_found:
        print("✓ Tespit edilen şüpheli process yok.")

# 👉 Dosya direkt çalıştırılırsa
if __name__ == "__main__":
    scan_current()