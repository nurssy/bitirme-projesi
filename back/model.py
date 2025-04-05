import tensorflow as tf
import numpy as np
import cv2
from keras.api.models import load_model
from keras.api.preprocessing import image

def load_selected_model(model_type):
    if model_type == 0:
        # CNN modelini yükle
        model = load_model('models/cnn_model_05042025.h5')
        print("CNN modeli yüklendi")
        return model
    elif model_type == 1:
        # U-Net modelini yükle
        model = load_model('models/unet_model_05042025.h5')
        print("U-Net modeli yüklendi")
        return model
    else:
        # Geçersiz model tipi
        raise ValueError("Geçersiz model_type. 0 (CNN) veya 1 (U-Net) değeri giriniz.")

def preprocess_image(image_path):
    img_resized = image.load_img(image_path, target_size=(180, 180))

    img_arr = image.img_to_array(img_resized)

    img_array_expanded = np.expand_dims(img_arr, axis=0)
    img_array_expanded = img_array_expanded / 255.0

    return img_array_expanded, img_resized

def predict_image(model, image_path):
    img_processed, img_original = preprocess_image(image_path)

    prediction = model.predict(img_processed)

    predicted_class_index = int(prediction[0][0] > 0.5)

    print("Cancer" if predicted_class_index == 0 else "Not Cancer")

    return predicted_class_index


