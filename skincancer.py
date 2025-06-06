# -*- coding: utf-8 -*-
"""skincancer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1k4M47C49vBTAzhUANquoUsg7xcscUQt6

#Creating a test folder
"""

from google.colab import drive
drive.mount('/content/drive')

import os
import shutil
import random

def move_random_files(source_folder, target_folder, number_of_files):
    # Kaynak klasördeki tüm dosyaları listelemesi için
    all_files = os.listdir(source_folder)

    # Dosya sayısını kontrol etmek için
    if len(all_files) < number_of_files:
        print(f"Hata: Kaynak klasörde {number_of_files} adetten daha az dosya var.")
        return

    # Hedef klasör yoksa oluştur
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Rastgele dosyaları seçer
    random_files = random.sample(all_files, number_of_files)

    # Seçilen dosyaları taşır
    for file_name in random_files:
        source_path = os.path.join(source_folder, file_name)
        target_path = os.path.join(target_folder, file_name)
        try:
            shutil.move(source_path, target_path)
            print(f"Taşındı: {source_path} -> {target_path}")
        except Exception as e:
            print(f"Hata oluştu: {file_name} -> {e}")

# Kullanım örneği
source_directory = "/content/drive/MyDrive/skincancer/archive/train/malignant"  # Kaynak klasör yolu
target_directory = "/content/drive/MyDrive/skincancer/archive/val/malignant"  # Hedef klasör yolu
move_random_files(source_directory, target_directory, 120)

"""#Code to Install Libraries

"""

# Ultralytics YOLO ve PyTorch kütüphanelerini yükleme kodu
!pip install ultralytics
!pip install torch

"""# Training

"""

import os # Dosya ve dizin işlemleri için gerekli modül
from ultralytics import YOLO  # YOLO modeli için ultralytics kütüphanesi
import torch  # PyTorch kütüphanesi; tensor işlemleri ve GPU kullanımı için

# GPU kullanımı kontrolü: CUDA mevcutsa cuda, değilse cpu kullanması için
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Veri setinin bulunduğu path
DATA_DIR = "/content/drive/MyDrive/skincancer/archive/data"

# YOLO sınıflandırma modeli yüklmesi; 'yolov8x-cls.pt'
model = YOLO("yolov8x-cls.pt")


# Modelin eğitimi başlatılır
results = model.train(data=DATA_DIR,  # Eğitim verilerinin dizini
                      project='/content/drive/MyDrive/skincancer/archive/runs', # Eğitim sonuçlarının kaydedileceği dizin
                      epochs=5, # Eğitim döngüsü sayısı (epoch)
                      auto_augment = False, # Otomatik veri artırma (augmentation) devre dışı
                      mixup = 0,  # Veri karıştırma tekniği (mixup) devre dışı
                      shear= 0, # Görüntü kesme (shear) işlemi devre dışı
                      erasing = 0,  # Rastgele silme (random erasing) devre dışı
                      imgsz=500,  # Eğitim sırasında kullanılacak görüntü boyutu (500x500 piksel)
                      lr0=0.001,  # Başlangıç öğrenme oranı (learning rate)
                      optimizer='Adam', # Kullanılacak optimizasyon algoritması: Adam
                      cache=True) # Veri setinin önbelleğe alınması; eğitim sürecini hızlandırır

"""#Test"""

from ultralytics import YOLO

# Modeli yüklemek için
model = YOLO("/content/drive/MyDrive/skincancer/archive/runs/train3/weights/best.pt")

# Test resmi üzerinde tahmin yaptırmak için
results = model.predict("/content/drive/MyDrive/skincancer/archive/val/benign/1041.jpg",show=True)

# Sonuçları yazdır
print(results)

"""#Class Prediction Visualization"""

from ultralytics import YOLO
import cv2  # Görüntü işleme için gerekli
import matplotlib.pyplot as plt  # Görüntü göstermek için gerekli

# Modeli yüklemek için
model = YOLO("/content/drive/MyDrive/skincancer/archive/runs/train3/weights/best.pt")

# Görüntüyü okuması için
image_path = "/content/drive/MyDrive/skincancer/archive/val/malignant/1040.jpg"
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCV'den okunan görüntüyü RGB'ye dönüştür

# Tahmin yapma kodu
results = model.predict(image, conf=0.7)

# Sınıf tahminini almak için
for result in results:
    class_probs = result.probs  # Sınıf olasılıklarını alması için
    top_class_index = class_probs.top1  # En yüksek güven skoruna sahip sınıfın indeksi
    class_name = result.names[top_class_index]
    confidence = class_probs.data[top_class_index].item()

    # Sınıf adını görüntüye eklemesi için
    cv2.putText(image, f"{class_name} {confidence:.2f}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# Görüntüyü göstermesi için
plt.imshow(image)
plt.axis('off')
plt.show()