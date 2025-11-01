import cv2
import numpy as np
from ffpyplayer.player import MediaPlayer
import time

def play_video_with_audio(file_path, window_size=(640, 480), target_fps=60):
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print(f"Ошибка: Не удалось открыть видеофайл {file_path}")
        return

    # Устанавливаем размер окна
    cv2.namedWindow(' ', cv2.WINDOW_NORMAL)
    cv2.resizeWindow(' ', 800, 600)

    player = MediaPlayer(file_path)  # Инициализация игрока аудио

    frame_delay = 1 / target_fps  # Вычисляем задержку в секундах

    last_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Уменьшаем размер кадра до размера окна
            resized_frame = cv2.resize(frame, (window_size[0], window_size[1]))

            cv2.imshow(' ', resized_frame)

            audio_frame, val = player.get_frame()  # Получение аудио фрейма

            if val != 'eof' and audio_frame is not None:
                img, t = audio_frame  # Обработка аудио фрейма

            current_time = time.time()
            elapsed_time = current_time - last_time
            sleep_time = max(0, frame_delay - elapsed_time)  # Вычисляем, сколько нужно подождать

            time.sleep(sleep_time)

            last_time = time.time()  # Обновляем время последнего кадра

            if cv2.waitKey(1) & 0xFF == ord("q"):  # Изменено на waitKey(1) для отзывчивости
                break
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        cap.release()
        player.close_player()  # Закрытие аудиоплеера
        cv2.destroyAllWindows()


# Использование
play_video_with_audio('play.mp4', target_fps=27)