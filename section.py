import re
from openai import OpenAI

def correct_grammar(section):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key="ithay_v_key_pao"
    )

    prompt = f"Correct the grammar of the following text and return only the corrected version:{section}"
    completion = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=300
    )
    corrected_text = completion.choices[0].message.content.strip()  
    corrected_text = re.sub(r"[*]", "", corrected_text)  
    return ", ".join(corrected_text.split())  

