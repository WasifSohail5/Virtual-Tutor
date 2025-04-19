import re
from openai import OpenAI

def correct_grammar(section):
    """Generates grammatically corrected text for a given section and returns it as a comma-separated string."""
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key="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"
    )

    prompt = f"Correct the grammar of the following text and return only the corrected version:\n\n{section}"

    completion = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=300
    )

    corrected_text = completion.choices[0].message.content.strip()  # Directly get the response

    # Clean response
    corrected_text = re.sub(r"[*]", "", corrected_text)  # Remove unwanted symbols

    return ", ".join(corrected_text.split())  # Return comma-separated corrected words

# Example usage
#section = input('Enter the section: ')
#print(correct_grammar(section))
