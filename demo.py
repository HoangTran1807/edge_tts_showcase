import edge_tts
import asyncio
from edge_tts import VoicesManager
import cusSubMaker

# global variables
OUTPUT_FILE = 'test.mp3'
WEBVTT_FILE = 'test.vtt'
TEXT = 'Hello, this is a test. how are you to day.'
VOICE = 'en-US-GuyNeural'

# simle voice data structure
# voice_data = {
#     'Name': 'Microsoft Server Speech Text to Speech Voice (zu-ZA, ThembaNeural)',
#     'ShortName': 'zu-ZA-ThembaNeural',
#     'Gender': 'Male',
#     'Locale': 'zu-ZA',
#     'SuggestedCodec': 'audio-24khz-48kbitrate-mono-mp3',
#     'FriendlyName': 'Microsoft Themba Online (Natural) - Zulu (South Africa)',
#     'Status': 'GA',
#     'VoiceTag': {
#         'ContentCategories': ['General'],
#         'VoicePersonalities': ['Friendly', 'Positive']
#     },
#     'Language': 'zu'
# }

def print_voice(voice):
    print('ShortName:', voice['ShortName'], '| Gender:', voice['Gender'], '| Locale:', voice['Locale'])

# show all voices available in the service
async def list_voices():
    voices = await edge_tts.VoicesManager.create()
    for voice in voices.voices:
        print_voice(voice)
        

# find voice with specific criteria 
async def find_voice(gender=None, language=None, locale=None):
    voices = await edge_tts.VoicesManager.create()
    search_criteria = {}
    if(gender):
        search_criteria['Gender'] = gender
    if(language):
        search_criteria['Language'] = language
    if(locale):
        search_criteria['Locale'] = locale
    voice = voices.find(**search_criteria)
    if voice:
        for v in voice:
            print_voice(v)
    else:
        print('Voice not found')

# very basic text to speech
async def basic_tts(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(OUTPUT_FILE)

# basic text to speech with streaming audio
async def basic_tts_stream(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                print(f"WordBoundary: {chunk}")

#
async def StreamingWithSubmaker(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    submaker = cusSubMaker.SubMaker()
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

    with open(WEBVTT_FILE, "w", encoding="utf-8") as file:
        file.write(submaker.generate_subs())


def readStory():
    with open('story.txt', 'r') as file:
        return file.read()

def main():
    try:
        # list all voices
        # asyncio.run(list_voices())

        # find voice with specific criteria
        #asyncio.run(find_voice(locale='en-US'))

        # basic tts
        text = readStory()
        asyncio.run(StreamingWithSubmaker(text, VOICE))
    except Exception as e:
        print(e)
    pass


if __name__ == "__main__":
    main()