import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps

# Load model
model = tf.keras.models.load_model("flood_model.h5")

TARGET_SIZE = (128, 128)


def prepare_image(image):
    """
    Smart resize:
    - Keeps aspect ratio
    - Shrinks large images
    - Enlarges small images
    - Pads to final 128x128
    """

    image = image.convert("RGB")

    # Fit image inside 128x128 while keeping ratio
    image.thumbnail(TARGET_SIZE, Image.Resampling.LANCZOS)

    # Create new canvas
    canvas = Image.new("RGB", TARGET_SIZE, (0, 0, 0))

    # Center image
    x = (TARGET_SIZE[0] - image.width) // 2
    y = (TARGET_SIZE[1] - image.height) // 2

    canvas.paste(image, (x, y))

    return canvas


def predict_flood(image):

    img = prepare_image(image)

    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img, verbose=0)[0][0]

    # label logic
    if pred < 0.5:
        result = 1
        confidence = round((1 - pred) * 100, 2)
    else:
        result = 0
        confidence = round(pred * 100, 2)

    return result, confidence