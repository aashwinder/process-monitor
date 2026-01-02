import psutil

process_names = set()

for process in psutil.process_iter(['name']):
    try:
        if process.info['name']:
            process_names.add(process.info['name'])
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

print("Çalışan benzersiz process isimleri:")

for name in sorted(process_names):
    print(name)