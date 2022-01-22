import sounddevice as sd
from deepgram import Deepgram
import asyncio, json
import soundfile as sf
directions = []

def check_for_events():
    fs = 44100
    duration = 3
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
    #print("Recording Audio")
    sd.wait()
    sf.write("dummy.wav", myrecording, fs)

    DEEPGRAM_API_KEY = '3616bc1d9c2d4a9306a400801decefbb9d5e984b'

    # Name and extension of the file you downloaded (e.g. sample.wav)
    PATH_TO_FILE = 'E:\Academics\IIT Bombay\Repositories\Cambridge-Hackathon\dummy.wav'

    async def main():
        global directions
        # Initialize the Deepgram SDK
        dg_client = Deepgram(DEEPGRAM_API_KEY)
        # Open the audio file
        with open(PATH_TO_FILE, 'rb') as audio:
            # Replace mimetype as appropriate
            source = {'buffer': audio, 'mimetype': 'audio/wav'}
            response = await dg_client.transcription.prerecorded(source, {'punctuate': False})
            x = json.loads(json.dumps(response, indent=4))
            x = str(x["results"]["channels"][0]["alternatives"][0]["transcript"]).upper().split()
            for i in x:
                if(i in ['LEFT','RIGHT','UP','DOWN']):
                    directions.append(i)

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

while True:
    check_for_events()
    if(len(directions)!=0):
        print(directions.pop(0))
