from openai import OpenAI
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

def trim_bullet_points(text, max_bullets=10):
    bullet_points = re.split(r"\n[-•] ", text)
    trimmed_bullets = "\n- " + "\n- ".join(bullet_points[:max_bullets])
    return trimmed_bullets.strip() if trimmed_bullets != "\n- " else text

def generate_text(topic, section):
    prompt = (
        f"Create exactly **10 bullet points** for a PowerPoint slide on '{topic}', focusing on '{section}'.\n"
        "⚡ **Rules:**\n"
        "- Only list bullet points, NO extra text like 'Here is the response'.\n"
        "- Do NOT add introductions or explanations.\n"
        "- Each bullet point should be **short and impactful** (max 15 words each).\n"
        "- Do NOT exceed 650 characters in total.\n\n"
        "**Bullet Points:**"
    )

    completion = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=4000,
        stream=True
    )

    section_details = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            section_details += chunk.choices[0].delta.content

    section_details = re.sub(r"\*", "", section_details)
    section_details = trim_bullet_points(section_details, max_bullets=10)
    return section_details, section_details  # Tuple: (for slide_text, duplicate if needed)

def generate_all_sections(topic, section_list):
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
                results[i] = ("- Error generating content", "- Error generating content")
                print(f"Error in section {section_list[i]}: {e}")

    return results  # List of tuples (text, text)

