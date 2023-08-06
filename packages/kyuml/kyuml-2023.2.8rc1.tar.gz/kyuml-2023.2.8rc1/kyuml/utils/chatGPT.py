import openai

def chatGPT(prompt, API_KEY=${{ secrets.openai_key }}):
    
    # set api key
    openai.api_key = API_KEY

    # Call the chat GPT API
    completion = openai.Completion.create(
        engine = 'text-davinci-003'     # 'text-curie-001'  # 'text-babbage-001' #'text-ada-001'
        , prompt = prompt
        , temperature = 0.5 
        , max_tokens = 1024
        , top_p = 1
        , frequency_penalty = 0
        , presence_penalty = 0
    )

    return completion['choices'][0]['text'].strip()