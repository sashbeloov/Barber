res = [{'id': 14, 'user': 'sashabelov - +998993150542 - 921347523', 'service': {'id': 1, 'name': 'Soch olish', 'description': 'Soch olish', 'duration': 30, 'price': '30000.00', 'contact': 'Shohruh'}, 'start_time': '2025-07-15 09:30', 'end_time': '2025-07-15 10:00', 'status': 'CONFIRMED', 'notes': None}, {'id': 13, 'user': 'sashabelov - +998993150542 - 921347523', 'service': {'id': 1, 'name': 'Soch olish', 'description': 'Soch olish', 'duration': 30, 'price': '30000.00', 'contact': 'Shohruh'}, 'start_time': '2025-07-15 09:00', 'end_time': '2025-07-15 09:30', 'status': 'CONFIRMED', 'notes': None}, {'id': 12, 'user': 'sashabelov - +998993150542 - 921347523', 'service': {'id': 1, 'name': 'Soch olish', 'description': 'Soch olish', 'duration': 30, 'price': '30000.00', 'contact': 'Shohruh'}, 'start_time': '2025-07-14 18:00', 'end_time': '2025-07-14 18:30', 'status': 'CONFIRMED', 'notes': None}, {'id': 4, 'user': 'sashabelov - +998993150542 - 921347523', 'service': {'id': 1, 'name': 'Soch olish', 'description': 'Soch olish', 'duration': 30, 'price': '30000.00', 'contact': 'Shohruh'}, 'start_time': '2025-07-13 18:00', 'end_time': '2025-07-13 18:30', 'status': 'CONFIRMED', 'notes': None}]
total = []

for i in res:
    for k,v in i.items():
        if k == 'start_time':
            total.append(v)

print(total)