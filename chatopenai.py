from openai import OpenAI
client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='mycoolproject', 
)
themessage ="hello how are you"
response = client.chat.completions.create(
    model="mixtral",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system", "content":"You are ...TODO"},
        {"role":"user", "content":f"{themessage}"}
    ]
)

print(response.choices[0].message.content)