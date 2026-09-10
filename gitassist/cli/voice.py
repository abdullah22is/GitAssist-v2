"""Voice input support for GitAssist using sounddevice.

All optional third-party dependencies (sounddevice, numpy, speech_recognition)
are imported lazily, inside functions, and guarded with try/except. This is
required because these packages are optional (see requirements-optional.txt)
and, on some platforms, sounddevice can raise OSError (missing PortAudio)
rather than ImportError even when the Python package itself is installed.
A module-level `import sounddevice` would crash the whole process the moment
this module is imported, before is_available() ever runs.
"""

from gitassist.cli import output
from gitassist.localization.texts import get_text


def is_available():
    """Check if speech recognition libraries (and their native deps) are usable."""
    try:
        import sounddevice  # noqa: F401
        import speech_recognition  # noqa: F401
        import numpy  # noqa: F401
        return True
    except Exception:
        # Catches ImportError (package missing) AND OSError (e.g. PortAudio
        # native library missing on Linux), both of which mean voice is unusable.
        return False


def listen(lang_code="en-US", duration=5):
    """
    Capture voice input and return transcribed text.
    lang_code examples: "en-US", "ar-SA" (Arabic).
    """
    try:
        import sounddevice as sd
        import speech_recognition as sr
    except Exception as e:
        output.print_error(f"Voice libraries unavailable: {e}")
        return ""

    fs = 16000
    output.print_info(get_text("voice_listening"))

    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        audio_bytes = recording.tobytes()
        audio_data = sr.AudioData(audio_bytes, fs, 2)

        output.print_info(get_text("voice_processing"))
        recognizer = sr.Recognizer()
        try:
            text = recognizer.recognize_google(audio_data, language=lang_code)
            return text
        except sr.UnknownValueError:
            output.print_error(get_text("voice_not_understood"))
            return ""
        except sr.RequestError as e:
            output.print_error(f"Speech service error: {e}")
            return ""
    except Exception as e:
        output.print_error(f"Microphone error: {e}")
        return ""


def start_voice_command():
    """Voice command entry point."""
    if not is_available():
        output.print_error(get_text("voice_unavailable"))
        output.print_info(get_text("voice_install_hint"))
        return

    from gitassist.config import settings
    lang_code = "ar-SA" if settings.LANGUAGE == "ar" else "en-US"
    text = listen(lang_code)
    if text:
        output.print_success(get_text("voice_heard", text=text))
        from gitassist.core.manual_command import execute_text_command
        execute_text_command(text)