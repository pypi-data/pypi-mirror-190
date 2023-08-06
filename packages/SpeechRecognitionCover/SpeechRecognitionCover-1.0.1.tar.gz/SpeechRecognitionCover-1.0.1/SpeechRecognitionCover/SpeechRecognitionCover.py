from speech_recognition import Microphone, Recognizer, AudioFile, UnknownValueError, RequestError

class Cover:
    def __init__(self, lang='en'):
        self.lang = lang

    def recognize(self, time=None, noises=False, noises_time=None, message=None):
        if time:
            if noises == True:
                if noises_time:
                    r = Recognizer()
                    mic = Microphone()

                    with mic:
                        r.adjust_for_ambient_noise(mic, duration=int(noises_time))
                        if message:
                            print(message)
                        audio = r.record(mic, int(time))

                    try:
                        try:
                            output = r.recognize_google(audio, language=str(self.lang))
                            return output

                        except UnknownValueError:
                            return ''
                    except RequestError:
                        raise RequestError("can't connect to internet")
                else:
                    r = Recognizer()
                    mic = Microphone()

                    with mic:
                        r.adjust_for_ambient_noise(mic, duration=3)
                        if message:
                            print(message)
                        audio = r.record(mic, int(time))

                    try:
                        try:
                            output = r.recognize_google(audio, language=str(self.lang))
                            return output

                        except UnknownValueError:
                            return ''
                    except RequestError:
                        raise RequestError("can't connect to internet")
            else:
                r = Recognizer()
                mic = Microphone()

                with mic:
                    audio = r.record(mic, int(time))

                try:
                    try:
                        output = r.recognize_google(audio, language=str(self.lang))
                        return output

                    except UnknownValueError:
                        return ''
                except RequestError:
                    raise RequestError("can't connect to internet")
        else:
            if noises == True:
                if noises_time:
                    r = Recognizer()
                    mic = Microphone()

                    with mic:
                        r.adjust_for_ambient_noise(mic, duration=int(noises_time))
                        if message:
                            print(message)
                        audio = r.record(mic, 5)

                    try:
                        try:
                            output = r.recognize_google(audio, language=str(self.lang))
                            return output

                        except UnknownValueError:
                            return ''
                    except RequestError:
                        raise RequestError("can't connect to internet")
                else:
                    r = Recognizer()
                    mic = Microphone()

                    with mic:
                        r.adjust_for_ambient_noise(mic, duration=5)
                        if message:
                            print(message)
                        audio = r.record(mic, 5)

                    try:
                        try:
                            output = r.recognize_google(audio, language=str(self.lang))
                            return output

                        except UnknownValueError:
                            return ''
                    except RequestError:
                        raise RequestError("can't connect to internet")
            else:
                r = Recognizer()
                mic = Microphone()

                with mic:
                    audio = r.record(mic, 5)

                try:
                    try:
                        output = r.recognize_google(audio, language=str(self.lang))
                        return output

                    except UnknownValueError:
                        return ''
                except RequestError:
                    raise RequestError("can't connect to internet")