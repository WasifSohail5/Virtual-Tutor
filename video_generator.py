import os
import cv2
import moviepy.editor as mp
from pptx import Presentation
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import concatenate_videoclips, AudioFileClip


def extract_slide_images(ppt_path, output_folder="slides"):
    """ Converts PowerPoint slides into images. """
    from pdf2image import convert_from_path
    import comtypes.client

    # Convert PPTX to PDF first
    pdf_path = ppt_path.replace(".pptx", ".pdf")
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1
    presentation = powerpoint.Presentations.Open(ppt_path)
    presentation.SaveAs(pdf_path, 32)  # 32 is for PDF format
    presentation.Close()
    powerpoint.Quit()

    # Convert PDF pages to images
    images = convert_from_path(pdf_path)
    os.makedirs(output_folder, exist_ok=True)
    slide_images = []

    for i, img in enumerate(images):
        img_path = os.path.join(output_folder, f"slide_{i + 1}.jpg")
        img.save(img_path, "JPEG")
        slide_images.append(img_path)

    return slide_images


def create_video_from_slides(slide_images, audio_path, output_video="lecture_video.mp4"):
    """ Generates a video by combining slides and audio. """
    slides = [ImageClip(img).set_duration(5) for img in slide_images]  # 5 sec per slide
    video = concatenate_videoclips(slides, method="compose")

    # Add voiceover
    if os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        video = video.set_audio(audio)

    video.write_videofile(output_video, codec="libx264", fps=24)
    print(f"Lecture video saved as {output_video}")


def generate_lecture_video(ppt_path, audio_path):
    """ Main function to generate AI-powered video lecture """
    slide_images = extract_slide_images(ppt_path)
    create_video_from_slides(slide_images, audio_path)


if __name__ == "__main__":
    ppt_path = "your_presentation.pptx"  # Replace with generated PPT
    audio_path = "your_audio.mp3"  # Replace with generated audio file
    generate_lecture_video(ppt_path, audio_path)
