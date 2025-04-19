import pyttsx3

def generate_audio(text, topic):
    engine = pyttsx3.init()

    # Get available voices
    voices = engine.getProperty("voices")

    # Generate Male voice
    engine.setProperty("voice", voices[0].id)  # Male voice
    male_audio_path = f"{topic.replace(' ', '_')}_male.mp3"
    engine.save_to_file(text, male_audio_path)
    
    # Generate Female voice
    engine.setProperty("voice", voices[1].id)  # Female voice
    female_audio_path = f"{topic.replace(' ', '_')}_female.mp3"
    engine.save_to_file(text, female_audio_path)

    engine.runAndWait()
    
    print(f"Audio files generated:\nMale: {male_audio_path}\nFemale: {female_audio_path}")
    return male_audio_path, female_audio_path
