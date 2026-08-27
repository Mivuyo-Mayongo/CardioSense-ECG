# CardioSense ECG

**An AI-powered ECG monitoring prototype for real-time heart abnormality detection using TinyML.**

CardioSense combines an AD8232 ECG sensor, an ESP32 microcontroller, and a one-dimensional Convolutional Neural Network (1D CNN) to capture ECG signals and classify heartbeats as normal or abnormal.

> **Project status:** In development. Live ECG acquisition and visualization are working. Real-time TinyML classification on the ESP32 is the current phase.
## Project Overview

Cardiovascular abnormalities may not always be detected early, particularly where continuous monitoring equipment is unavailable or expensive. CardioSense explores a portable and low-cost approach to ECG monitoring and on-device heart abnormality detection.

The project is designed to:

- Capture ECG signals using the AD8232 sensor
- Sample ECG data using the ESP32
- Process 200-sample heartbeat windows
- Run a TensorFlow Lite model on the ESP32
- Classify heartbeats as normal or abnormal
- Display or transmit the classification results

### ECG Dataset Exploration

The model is being developed using ECG records from the MIT-BIH Arrhythmia Database. Record 100 was initially explored as an example containing predominantly normal heartbeats.
<img width="795" height="379" alt="mit-bih-record-100-normal-ecg" src="https://github.com/user-attachments/assets/024be67d-7e8b-49e3-ab6c-c667628bdc33" />

*Example ECG signal from MIT-BIH record 100.*

### Abnormal ECG Example

Record 119 was explored as an example containing ventricular premature beats (VPBs), a type of cardiac arrhythmia.

In the graph:

- **N** represents a normal heartbeat.
- **V** represents a ventricular premature beat.
- The ventricular premature beats have a wider and more distorted waveform than the normal beats.
<img width="766" height="408" alt="image" src="https://github.com/user-attachments/assets/7c977c92-3700-4c80-9a7e-ea5e59258181" />

*Example ECG signal from MIT-BIH record 119 showing ventricular premature beats.*

## ECG Signal Preprocessing

The continuous ECG recordings cannot be passed directly to the CNN. Each recording must first be converted into consistently sized heartbeat samples.

The preprocessing pipeline:

1. Loads an ECG signal and its heartbeat annotations.
2. Locates the centre of each annotated heartbeat.
3. Extracts a window containing 200 ECG data points.
4. Assigns the heartbeat a normal or abnormal label.
5. Stores the heartbeat window for model training and evaluation.

Each resulting 200-value array represents one heartbeat and matches the input shape expected by the CNN.

### Example Heartbeat Window
<img width="776" height="415" alt="image" src="https://github.com/user-attachments/assets/58804171-7645-4585-8082-d400086ef993" />

*Example of a normal heartbeat segmented into a 200-sample input window.*

## CNN Model Architecture

A one-dimensional Convolutional Neural Network (1D CNN) was developed using TensorFlow and Keras. The network learns patterns directly from the shape of each 200-sample ECG heartbeat window.

The architecture contains:

1. **Conv1D layer with 16 filters** to detect basic ECG waveform features.
2. **MaxPooling1D layer** to reduce the feature-map size.
3. **Conv1D layer with 32 filters** to learn more detailed waveform patterns.
4. **MaxPooling1D layer** for further dimensionality reduction.
5. **Flatten layer** to convert the extracted features into a single vector.
6. **Dense layer with 32 neurons** to combine the learned features.
7. **Sigmoid output layer** to produce a binary classification probability.

The output represents:

- `0` — Normal heartbeat
- `1` — Abnormal heartbeat
<img width="1745" height="528" alt="image" src="https://github.com/user-attachments/assets/638f93f3-37dd-4d4c-b021-b8915392694a" />

*TensorFlow/Keras summary of the CardioSense 1D CNN architecture.*

## Model Training

The CNN was trained in Google Colab using TensorFlow and Keras. The prepared ECG heartbeat samples were divided into:

- **80% training data**
- **20% testing data**

The model was trained for 10 epochs using binary classification.

### Preliminary Training Results

| Metric | Reported value |
|---|---:|
| Training accuracy | 99.91% |
| Training loss | 0.0019 |

These values describe performance on the training data. They do not, by themselves, confirm how well the model performs on unseen ECG data.

Test accuracy, precision, recall, F1-score, and a confusion matrix will be added after the evaluation results have been verified from the training notebook.
<img width="778" height="485" alt="image" src="https://github.com/user-attachments/assets/f979cca6-a429-4987-84b6-a14317ebcc9b" />

*CNN training output recorded in Google Colab.*

## TensorFlow Lite and TinyML Deployment

After training, the Keras model was converted to TensorFlow Lite so that it could be deployed on the resource-constrained ESP32.

The conversion was performed using:

```python
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
```
<img width="747" height="612" alt="image" src="https://github.com/user-attachments/assets/f5fb5341-9b97-4916-9628-a7ccf2c1a3ad" />

*Arduino test program used to verify that the TensorFlow Lite model was accessible on the ESP32.*

## ESP32 Model Verification

The ESP32 was configured and tested using:

- **Board:** ESP32 Dev Module
- **Port:** COM4
- **Baud rate:** 115200
- **Arduino IDE:** 2.3.8
- **ESP32 board package:** 2.0.17

After compiling and uploading the model-loading program, the Serial Monitor reported:

- `ECG TinyML Model Loaded`
- Model size: **58,400 bytes**
- `Model Stored Successfully`

This confirmed that the generated model byte array was compiled into the firmware and could be accessed by the ESP32.

> This test verifies that the model data is available on the ESP32. It does not yet perform classification inference.
<img width="1602" height="331" alt="image" src="https://github.com/user-attachments/assets/6ae05d53-e6cc-4476-9110-6047a67cf884" />

*Serial Monitor output confirming that the 58,400-byte model array was accessible on the ESP32.*

