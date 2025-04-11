from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from PIL import Image, ImageFilter


def apply_emboss_effect(image_path):
    # Открываем изображение
    image = Image.open(image_path)

    # Применяем эффект тиснения
    embossed_image = image.filter(ImageFilter.EMBOSS)

    # Сохраняем обработанное изображение
    embossed_image_path = "embossed_logo.png"
    embossed_image.save(embossed_image_path)

    return embossed_image_path


def apply_watermark(video_path, logo_path, output_path, opacity=0.5):
    # Применяем эффект тиснения к логотипу
    embossed_logo_path = apply_emboss_effect(logo_path)

    # Открываем видеофайл
    video = VideoFileClip(video_path)

    # Открываем логотип
    logo = ImageClip(embossed_logo_path)

    # Изменяем размер логотипа, чтобы он соответствовал размеру видео
    logo = logo.resized(height=int(video.h * 0.3))  # Изменяем размер логотипа до 30% от высоты видео

    # Устанавливаем прозрачность логотипа для эффекта водяного знака
    logo = logo.with_opacity(opacity)

    # Создаем новое видео с наложенным логотипом
    final_video = CompositeVideoClip([video, logo.with_duration(video.duration)])

    # Сохраняем результат
    final_video.write_videofile(output_path, codec="libx264")


if __name__ == "__main__":
    video_path = "croco.mp4"
    logo_path = "guap.png"
    output_path = "emb_output_video.mp4"
    apply_watermark(video_path, logo_path, output_path)