import glob
import os
import time
import shutil

import tensorflow as tf

import matplotlib.pyplot as plt
import matplotlib as mpl

print(tf.__version__)

mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False

style_predict_path = tf.keras.utils.get_file('style_predict.tflite',
                                             'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/prediction/1?lite-format=tflite')
style_transform_path = tf.keras.utils.get_file('style_transform.tflite',
                                               'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/transfer/1?lite-format=tflite')


def imshow(image, title=None):
    if len(image.shape) > 3:
        image = tf.squeeze(image, axis=0)
    plt.imshow(image)
    if title:
        plt.title(title)


def load_img(path_to_img):
    img = tf.io.read_file(path_to_img)
    img = tf.io.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img


def preprocess_image(image, target_dim):
    # Resize the image so that the shorter dimension becomes 256px.
    shape = tf.cast(tf.shape(image)[1:-1], tf.float32)
    short_dim = min(shape)
    scale = target_dim / short_dim
    new_shape = tf.cast(shape * scale, tf.int32)
    image = tf.image.resize(image, new_shape)

    # Central crop the image.
    image = tf.image.resize_with_crop_or_pad(image, target_dim, target_dim)

    return image


def get_images(content_path, style_path):
    content_image = load_img(content_path)
    style_image = load_img(style_path)

    preprocessed_content_image = preprocess_image(content_image, 384)
    preprocessed_style_image = preprocess_image(style_image, 256)

    return preprocessed_content_image, preprocessed_style_image


def run_style_predict(preprocessed_style_image):
    interpreter = tf.lite.Interpreter(model_path=style_predict_path,  num_threads=4)

    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]["index"], preprocessed_style_image)

    interpreter.invoke()
    style_bottleneck = interpreter.tensor(
        interpreter.get_output_details()[0]["index"]
    )()

    return style_bottleneck


def run_style_transform(style_bottleneck, preprocessed_content_image, num_threads=4):
    interpreter = tf.lite.Interpreter(model_path=style_transform_path)

    input_details = interpreter.get_input_details()
    interpreter.allocate_tensors()

    interpreter.set_tensor(input_details[0]["index"], preprocessed_content_image)
    interpreter.set_tensor(input_details[1]["index"], style_bottleneck)
    interpreter.invoke()

    stylized_image = interpreter.tensor(
        interpreter.get_output_details()[0]["index"]
    )()

    return stylized_image


def make_style_transfer(content_image_path, style_image_path, content_blending_ratio=0.1,
                        path_save_final_img="./pics/final_image.jpg"):
    content, style = get_images(content_image_path, style_image_path)
    style_bottleneck_content = run_style_predict(preprocess_image(content, 256))
    style_bottleneck = run_style_predict(style)
    content_blending_ratio = content_blending_ratio
    style_bottleneck_blended = content_blending_ratio * style_bottleneck_content \
                               + (1 - content_blending_ratio) * style_bottleneck
    stylized_image_blended = run_style_transform(style_bottleneck_blended, content)
    # imshow(stylized_image_blended, 'Blended Stylized Image')
    final_image = tf.squeeze(stylized_image_blended, axis=0)
    final_image = tf.image.convert_image_dtype(final_image, tf.uint8)
    final_image_encoded = tf.io.encode_jpeg(final_image)
    tf.io.write_file(tf.constant(path_save_final_img), final_image_encoded)
