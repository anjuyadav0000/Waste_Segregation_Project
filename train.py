```python
"""
Smart Waste Management System

Author: Anju Yadav
Course: Artificial Intelligence Programming Assistant
Institute: NSTI Women Jaipur
Organization: Edunet Foundation

Model: MobileNetV2
Dataset: TrashNet Waste Classification Dataset
"""

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.callbacks import EarlyStopping

# -----------------------------
# Dataset Path
# -----------------------------
dataset_path = "dataset/dataset/dataset-resized"

IMG_SIZE = 224
BATCH_SIZE = 32

# -----------------------------
# Data Preprocessing
# -----------------------------
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

train_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# -----------------------------
# MobileNetV2 Base Model
# -----------------------------
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224,224,3)
)

base_model.trainable = False

# -----------------------------
# Build Model
# -----------------------------
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(6, activation='softmax')
])

# -----------------------------
# Compile Model
# -----------------------------
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# -----------------------------
# Training
# -----------------------------
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=10,
    callbacks=[early_stop]
)

# -----------------------------
# Save Model
# -----------------------------
import pickle

with open("model/waste_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model Saved Successfully!")
```
