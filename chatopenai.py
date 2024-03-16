import json
from openai import OpenAI
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='dawhacksproject',
)
example_json = {
    "name": "Costco",
    "location": "054 rue StGeorge",
    "cardType": "Visa",
    "amount": "27.99"
}


def convert_json(text: str) -> str:
    prompt = text
    response = client.chat.completions.create(
        model="mixtral",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system",
                "content": f"You are a helpful assistant designed to output JSON of a recipe with the format looking like this {json.dumps(example_json)} and only that, do not list the items itself."},
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    json_object = response.choices[0].message.content
    return json_object
