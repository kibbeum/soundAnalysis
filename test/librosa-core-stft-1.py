import librosa, librosa.display
import numpy as np

#y, sr = librosa.load(librosa.util.example_audio_file())
y, sr = librosa.load("../resources/bat.wav")
D = librosa.stft(y)

D_left = librosa.stft(y, center=False)

# Use a shorter hop length

D_short = librosa.stft(y, hop_length=64)

# Display a spectrogram

import matplotlib.pyplot as plt
librosa.display.specshow(librosa.amplitude_to_db(np.abs(D),
                                                 ref=np.max),
                         y_axis='log', x_axis='time')
plt.title('Power spectrogram')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()