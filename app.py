import streamlit as st
from dotenv import load_dotenv
import os
import openai


def setup():
    st.set_page_config(
        page_title="GPT-3 Playground",
        page_icon="🤖",
        initial_sidebar_state="expanded",
    )
    st.title("ホットドッグ注文受付チャットボット")
    load_dotenv()
    openai.api_key = os.environ.get("OPENAI_API_KEY")


@st.cache_resource
def initialize_chat_log():
    context = [
        {
            "role": "system",
            "content": """\
You are OrderBot, an automated service to collect orders for a hotdog shop. \
You first greet the customer, then collect the order.\
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
You have to communicate in Japanese. \
The menu includes \
normal hotdog small: 5.00, medium: 7.00, large: 9.00 \
cheese hotdog small: 6.50, medium: 8.50, large: 10.50 \
spicy hotdog small: 6.00, medium: 8.00, large: 10.00 \
french fries small: 3.00, medium: 4.00 \
Toppings: \
extra cheese 2.00 \
extra spicy sauce 1.00 \
Drinks: \
coke small: 1.00, medium: 2.00, large: 3.00 \
Dr.Pepper small: 1.00, medium: 2.00, large: 3.00 \
soda small: 1.00, medium: 2.00, large: 3.00 \
bottled water 5.00 \
""",
        }
    ]
    return context


def get_completion_from_messages(
    messages: list[dict[str, str]], model: str = "gpt-3.5-turbo", temperature: int = 0
):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


def display_chat(chat: list[dict[str, str]]) -> None:
    for message in chat:
        role = message["role"]
        if role == "user":
            st.subheader("あなた: ")
        elif role == "assistant":
            st.subheader("ChatGPT: ")

        if role != "system":
            st.write(message["content"])


def main():
    setup()

    chat_log = initialize_chat_log()

    input_text = st.text_input("入力欄", "")

    if st.button("送信"):
        user_message = {"role": "user", "content": f"{input_text}"}
        chat_log.append(user_message)
        response = get_completion_from_messages(chat_log)
        assistant_message = {"role": "assistant", "content": response.strip()}
        chat_log.append(assistant_message)

        display_chat(chat_log)

    else:
        st.write("入力後に「送信」を押してください")


if __name__ == "__main__":
    main()
