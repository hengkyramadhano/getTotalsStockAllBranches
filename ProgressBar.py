import sys
import time

def update_progress(progress):
    bar_length = 50
    filled_length = int(bar_length * progress)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: [{bar}] {int(progress * 100)}%')
    sys.stdout.flush()

def progress_bar(percent):
    for i in range(percent + 1):
        update_progress(i / 100.0)
        print(i / 100.0)
        time.sleep(0.1)
    print("\nSelesai!")

# Input persentase progress
percentage = int(input("Masukkan persentase progress (0-100): "))
progress_bar(percentage)
