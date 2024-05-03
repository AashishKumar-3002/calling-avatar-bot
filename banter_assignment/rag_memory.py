from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import re

load_dotenv()

personName = "Steve Jobs"
llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.2, max_tokens=1024)
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            f"""You are {personName}. Do not write any explanations and only answer like  {personName} would. 
                You must know all of the knowledge of {personName}. Respond as {personName} would, with wit and personality.
                keep your responses within 1-2 sentences only."""
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
)

def chat_with_memory(question):
    input_data = {
        "question": question
    }

    response = conversation(input_data)

    print(conversation.memory)

    # Remove text within asterisks
    cleaned_text = re.sub(r'\*.*?\*', '', response["text"])

    return cleaned_text

if __name__ == '__main__':
    # Example usage:
    question1 = "hi steve, Do you mind asking you some question?"
    question2 = "what do you feel about ai race in the world?"

    reply = chat_with_memory(question1)
    print(reply)

    reply = chat_with_memory(question2)
    print(reply)
