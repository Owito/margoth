import io
import pygame


class AudioPlayer:
    _initialized = False

    def __init__(self):
        if not AudioPlayer._initialized:
            pygame.mixer.init()
            AudioPlayer._initialized = True
        self._current_stream = None

    def play_audio(self, audio_bytes):
        if not audio_bytes:
            return
        try:
            self._current_stream = io.BytesIO(audio_bytes)
            pygame.mixer.music.load(self._current_stream)
            pygame.mixer.music.play()
        except pygame.error as exc:
            print(f"Error reproduciendo audio: {exc}")
