from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np
import matplotlib.pyplot as plt
import librosa


def fourier_filter(data, lowcut, highcut, fs, suppression_factor=30):
    N = data.shape[0]
    Spectr_input = np.fft.rfft(data, axis=0)
    freqs = np.fft.rfftfreq(N, d=1 / fs)

    # Определение диапазона частот для подавления
    band = (freqs >= lowcut) & (freqs <= highcut)

    # Подавление частот в указанном диапазоне
    Spectr_input[band] /= suppression_factor

    # Обратное преобразование Фурье
    filtered_data = np.fft.irfft(Spectr_input, axis=0)

    return filtered_data


def process_audio(audio, lowcut, highcut, fs, suppression_factor=30):
    return fourier_filter(audio, lowcut, highcut, fs, suppression_factor)


def plot_spectrogram(signal, sr, title):
    D = np.abs(librosa.stft(signal, n_fft=2048, hop_length=512))
    D_db = librosa.amplitude_to_db(D, ref=np.max)
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(D_db, sr=sr, hop_length=512, x_axis="time", y_axis="log")
    plt.colorbar(label="Amplitude (dB)")
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.show()


def apply_audio_filter(video_path, output_path, lowcut=1000, highcut=3000, suppression_factor=30):
    # Открываем видеофайл
    video = VideoFileClip(video_path)

    # Извлекаем аудиодорожку
    audio = video.audio

    # Получаем частоту дискретизации и данные аудио
    audio_fps = audio.fps
    audio_data = audio.to_soundarray()

    # Применяем фильтр к аудиодорожке
    filtered_audio_data = process_audio(audio_data, lowcut, highcut, audio_fps, suppression_factor)

    # Создаем новую аудиодорожку с подавленным сигналом
    filtered_audio = AudioArrayClip(filtered_audio_data, fps=audio_fps)

    # Создаем новое видео с обработанной аудиодорожкой
    final_video = video.with_audio(filtered_audio)

    # Сохраняем результат
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Построение спектрограммы
    plot_spectrogram(np.mean(audio_data, axis=1), audio_fps, "Исходная спектрограмма ")
    plot_spectrogram(np.mean(filtered_audio_data, axis=1), audio_fps, "Спектрограмма после фильтрации")


if __name__ == "__main__":
    video_path = "croco.mp4"
    output_path = "filtered_output_video.mp4"
    apply_audio_filter(video_path, output_path)