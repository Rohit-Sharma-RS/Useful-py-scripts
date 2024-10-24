import tensorflow as tf
import numpy as np
import sounddevice as sd
import tensorflow_datasets as tfds

# Load the trained model
model = tf.keras.models.load_model("speech_commands_model.h5")

# Define parameters
DESIRED_SAMPLING_RATE = 16000  # 16kHz sampling rate
DESIRED_TIME_SAMPLES = 124  # Time samples for spectrogram padding
BLOCK_SIZE = 16000  # Size of audio blocks (1 second of audio for 16kHz sampling rate)

# Preprocess audio data
def preprocess_waveform(waveform):
    waveform = tf.cast(waveform, tf.float32)
    spectrogram = tf.signal.stft(waveform, frame_length=255, frame_step=128)
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.math.log(spectrogram + 1e-6)
    
    padding = [[0, DESIRED_TIME_SAMPLES - tf.shape(spectrogram)[0]], [0, 0]]
    spectrogram = tf.pad(spectrogram, padding)
    
    spectrogram = tf.expand_dims(spectrogram, axis=-1)  # For CNN input shape
    spectrogram = tf.expand_dims(spectrogram, axis=0)  # Add batch dimension
    return spectrogram

# Function to continuously predict the spoken word
def callback(indata, frames, time, status):
    if status:
        print(status)
    
    # Convert microphone input to numpy array
    waveform = np.squeeze(indata)
    
    # Preprocess the waveform to match training data
    spectrogram = preprocess_waveform(waveform)
    
    # Make prediction
    prediction = model.predict(spectrogram)
    predicted_label = np.argmax(prediction)
    
    # Print the predicted label
    print(f"Predicted label: {predicted_label}")

# Start the real-time audio stream
with sd.InputStream(callback=callback, channels=1, samplerate=DESIRED_SAMPLING_RATE, blocksize=BLOCK_SIZE):
    print("Listening... press Ctrl+C to stop.")
    while True:
        pass
