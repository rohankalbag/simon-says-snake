import speech_recognition as sr
from ctypes import *
from contextlib import contextmanager
import sys
import os

# remove unnessecary warning logs
# reference: https://stackoverflow.com/questions/7088672/pyaudio-working-but-spits-out-error-messages-each-time

ERROR_HANDLER_FUNC = CFUNCTYPE(
    None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass


c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)


class LISTENER():
    # reference: https://stackoverflow.com/questions/8391411/how-to-block-calls-to-print
    # disable printing of the dict while recognize_google()
    def blockPrint(self):
        sys.stdout = open(os.devnull, 'w')

    # restore printing
    def enablePrint(self):
        sys.stdout = sys.__stdout__

    # main function to listen to speech from microphone
    def listen(self, cond=False):
        with noalsaerr():
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.2)
                    audio = r.listen(source)
                    self.blockPrint()
                    if (cond):
                        MyText, confidence = r.recognize_google(
                            audio, with_confidence=cond)
                        self.enablePrint()
                        return (MyText, confidence)
                    else:
                        MyText = r.recognize_google(audio)
                        self.enablePrint()
                        return MyText
            except sr.UnknownValueError:
                return ""


if __name__ == "__main__":
    print("program started")
    sample = LISTENER()
    with_confidence = True
    print(sample.listen(with_confidence))
    print(sample.listen(with_confidence))