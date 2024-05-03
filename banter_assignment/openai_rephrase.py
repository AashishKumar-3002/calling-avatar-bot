import openai

def rephrase_question_openai(question):
    # Define the prompt
    prompt = f"Given a question your task is to rephrase the question keeping the meaning same. Question: {question} Rephrased Question:"

    # Define the completion
    completion = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=100
    )

    # Print the completion
    print(completion.choices[0].text)

    return completion.choices[0].text   