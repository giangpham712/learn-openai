import whisper


class Transcriber:
    def __init__(self):
        self.model = whisper.load_model('base')

    def transcribe(self, file):
        print(file)
        transcription = self.model.transcribe(file)
        return transcription['text']
