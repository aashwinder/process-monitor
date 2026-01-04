from create_baseline import create_baseline
from scan_current import scan_current

while True:
    print("\n=== Process Monitor v1.0 by Ashwinder ===")
    print("1- Baseline oluştur")
    print("2- Mevcut process'leri tara")
    print("0- Çıkış")

    choice = input("\nSeçimin: ").strip()

    if choice == "1":
        create_baseline()
    elif choice == "2":
        scan_current()
    elif choice == "0":
        print("Görüşürüz :)")
        break
    else:
        print("X Geçersiz seçim, tekrar dene.")