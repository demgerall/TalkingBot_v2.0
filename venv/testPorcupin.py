import pvporcupine
from pvrecorder import PvRecorder

porcupine = pvporcupine.create(
        access_key="rGmjFzlpPYfcYnKSjE6cUZhQaW38gssHbfAMBUhYcS5NFAHBzT3GXA==",
        keywords=["grapefruit"])
recoder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

try:
    recoder.start()

    while True:
        keyword_index = porcupine.process(recoder.read())
        if keyword_index >= 0:
            print(f"Detected 'Игорь'")

except KeyboardInterrupt:
    recoder.stop()
finally:
    porcupine.delete()
    recoder.delete()