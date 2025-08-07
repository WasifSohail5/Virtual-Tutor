from openai import OpenAI
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="Apni_Key_Pao"
)

def generate_text(topic, section):
    prompt = (
        f"Provide a comprehensive, detailed explanation about {topic} focusing on the section: '{section}'. "
        "Include relevant information, examples, and context. "
        "Also provide a detailed lecture script. "
        "Do not start with phrases like 'I have done this' — start directly from the topic. "
        "The content should feel like a lecture breakdown, well arranged as slides: bullet points with light elaboration where necessary. "
        "Do not include headings like 'Slide 1', just logically separated slide content.\n\n"
    )
    completion = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )
    section_details = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            section_details += chunk.choices[0].delta.content

    section_details = re.sub(r"\*", "", section_details)  
    slides_data = section_details[:500]
    lecture_script = section_details[500:]

    return slides_data.strip(), lecture_script.strip()

def generate_all_lectures(topic, section_list):
    results = [None] * len(section_list)
    with ThreadPoolExecutor() as executor:
        future_to_index = {
            executor.submit(generate_text, topic, section): i
            for i, section in enumerate(section_list)
        }

        for future in as_completed(future_to_index):
            i = future_to_index[future]
            try:
                results[i] = future.result()
            except Exception as e:
                print(f"Error generating content for section '{section_list[i]}': {e}")
                results[i] = ("- Error generating slides", "- Error generating lecture")

    return results
if __name__ == "__main__":
    topic = "Deep Learning Applications"
    sections = [
        "Medical Imaging",
        "Natural Language Processing",
        "Autonomous Vehicles",
        "Financial Forecasting",
        "Robotics"
    ]

    print(f"Generating lecture content for topic: {topic}")
    content = generate_all_lectures(topic, sections)

    for i, (slides, lecture) in enumerate(content):
        print(f"\n=== Section: {sections[i]} ===")
        print("\nSlide Content:\n", slides)
        print("\n🎙Lecture Script:\n", lecture)
        print("-"*80)
