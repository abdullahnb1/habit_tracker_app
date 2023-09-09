import json
from datetime import datetime

# Verileri dosyaya kaydetme
def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

# Şu anki zamanı JSON verilerine ekleme
def add_current_time(data):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["timestamp"] = current_time

# Örnek veri
data = {"title": "Habit 1", "description": "Description 1"}

# Şu anki zamanı veriye ekleme
add_current_time(data)

# Veriyi JSON dosyasına kaydetme
save_data(data, "veri.json")
