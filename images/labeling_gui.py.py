import csv

data = [["test001.jpg", "B1234XYZ"],
        ["test002.jpg", "D5678ABC"]]

output_path = r"C:\Users\royanfadli\Downloads\archive\Indonesian License Plate Recognition Dataset\images\test\ground_truth_test.csv"

with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["image", "ground_truth"])
    writer.writerows(data)

print("✅ CSV berhasil dibuat.")
