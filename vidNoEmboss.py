from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

def apply_watermark(video_path, logo_path, output_path):
    # Открываем видеофайл
    video = VideoFileClip(video_path)

    # Открываем логотип
    logo = ImageClip(logo_path)

    # Изменяем размер логотипа, чтобы он соответствовал размеру видео
    logo = logo.resized(height=int(video.h * 0.35))  # Изменяем размер логотипа до 35% от высоты видео

    # Устанавливаем прозрачность логотипа для эффекта водяного знака
    logo = logo.with_opacity(0.5)

    # Создаем новое видео с наложенным логотипом
    final_video = CompositeVideoClip([video, logo.with_duration(video.duration)])

    # Сохраняем результат
    final_video.write_videofile(output_path, codec="libx264")

if __name__ == "__main__":
    video_path = "croco.mp4"
    logo_path = "guap.png"
    output_path = "output_video.mp4"
    apply_watermark(video_path, logo_path, output_path)