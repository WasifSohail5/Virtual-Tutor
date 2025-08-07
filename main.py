import concurrent.futures
from slide_generator import generate_text as generate_slides
from script_generator import generate_text as generate_script
from image_scraper import search_and_download_images
from ppt_generator import create_presentation
from audio_generator import generate_audio
from section import correct_grammar
import re

def clean_filename(filename):
    """Removes invalid characters from a filename."""
    return re.sub(r'[\\/*?:"<>|,]', '_', filename)

def process_section(topic, section):
    corrected_section = correct_grammar(section)  
    corrected_section = clean_filename(corrected_section) 
    slide_text = ", ".join(generate_slides(topic, corrected_section))  
    lecture_text = ", ".join(generate_script(topic, corrected_section))  
    images = search_and_download_images(f"{topic} {corrected_section}", num_images=5)

    return corrected_section, slide_text, lecture_text, images

def main():
    topic = input("Enter a topic: ")
    sections_input = input("Enter sections separated by commas (e.g., Introduction, History, Applications): ")
    sections = [section.strip() for section in sections_input.split(',')]
    print("\nStarting parallel processing for lecture script, slide text, and image downloading...\n")
    slides_data = {}
    lecture_script = f"Lecture Script for Topic: {topic}"
    images_data = {}
    corrected_sections = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_section = {executor.submit(process_section, topic, section): section for section in sections}
        for future in concurrent.futures.as_completed(future_to_section):
            corrected_section, slide_text, lecture_text, images = future.result()
            slides_data[corrected_section] = slide_text
            lecture_script += f"### {corrected_section}\n{lecture_text}\n\n"
            images_data[corrected_section] = images
            corrected_sections.append(corrected_section)

    print("Creating PowerPoint Presentation...")
    ppt_path = create_presentation(topic, corrected_sections, [slides_data[sec] for sec in corrected_sections],
                                   [images_data[sec] for sec in corrected_sections])
    print(f"Presentation saved as {ppt_path}")
    script_path = f"{topic.replace(' ', '_')}_lecture_script.txt"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(lecture_script)
    print(f"Lecture script saved as {script_path}")

    print("Generating lecture audio.....")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        audio_future = executor.submit(generate_audio, lecture_script, topic)
        audio_path = audio_future.result()
    print(f"Lecture audio saved as {audio_path}")
    print("Slides Data:", slides_data)
    from video_generator import generate_lecture_video

    print("Generating lecture video....")
    generate_lecture_video(ppt_path, audio_path)
    print("Lecture video successfully generated!")
if __name__ == "__main__":
    main()
