import os
import base64
import csv
import requests
import pandas as pd
import numpy as np

# GANTI path ke folder gambar test kamu
DATASET_PATH = r"C:\Users\royanfadli\Downloads\archive\Indonesian License Plate Recognition Dataset\images\test"
GROUND_TRUTH_FILE = os.path.join(DATASET_PATH, "ground_truth_test.csv")
OUTPUT_CSV = os.path.join(DATASET_PATH, "hasil_ocr_lmstudio.csv")

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def cer(s1, s2):
    dp = np.zeros((len(s1)+1, len(s2)+1), dtype=int)
    for i in range(len(s1)+1): dp[i][0] = i
    for j in range(len(s2)+1): dp[0][j] = j
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[len(s1)][len(s2)] / max(len(s1), 1)

# Baca ground truth dari file CSV
df_gt = pd.read_csv(GROUND_TRUTH_FILE)
gt_dict = {row['image']: str(row['ground_truth']).strip().replace(" ", "").upper() for _, row in df_gt.iterrows()}

# Tulis hasil ke file output
with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["image", "ground_truth", "prediction", "CER_score"])

    for fname in sorted(gt_dict.keys()):
        img_path = os.path.join(DATASET_PATH, fname)
        if not os.path.exists(img_path):
            print(f"❌ Gambar tidak ditemukan: {fname}")
            continue

        ground_truth = gt_dict.get(fname, "").upper()
        if ground_truth == "":
            print(f"⚠️  Ground truth kosong untuk {fname}, dilewati.")
            continue

        b64_image = encode_image(img_path)

        payload = {
            "model": "llava-llama-3-8b-v1_1",
            "messages": [
                {"role": "system", "content": "You are an OCR assistant."},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_image}"}},
                    {"type": "text", "text": "What is the license plate number shown in this image? Respond only with the plate number."}
                ]}
            ],
            "temperature": 0,
            "max_tokens": 512
        }

        try:
            response = requests.post("http://localhost:1234/v1/chat/completions", json=payload)
            result = response.json()
            pred = result['choices'][0]['message']['content'].strip().replace(" ", "").upper()
            cer_score = cer(ground_truth, pred)
            writer.writerow([fname, ground_truth, pred, cer_score])
            print(f"✅ {fname} | GT: {ground_truth} | Pred: {pred} | CER: {cer_score:.3f}")
        except Exception as e:
            print(f"❌ ERROR {fname}: {e}")
