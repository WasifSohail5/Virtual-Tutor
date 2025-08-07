import pyttsx3

def generate_audio(text, topic):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    engine.setProperty("voice", voices[0].id)  # Male voice
    male_audio_path = f"{topic.replace(' ', '_')}_male.mp3"
    engine.save_to_file(text, male_audio_path)
    
    engine.setProperty("voice", voices[1].id)  # Female voice
    female_audio_path = f"{topic.replace(' ', '_')}_female.mp3"
    engine.save_to_file(text, female_audio_path)

    engine.runAndWait()
    print(f"Audio files generated:Male: {male_audio_path}Female: {female_audio_path}")
    return male_audio_path, female_audio_path
