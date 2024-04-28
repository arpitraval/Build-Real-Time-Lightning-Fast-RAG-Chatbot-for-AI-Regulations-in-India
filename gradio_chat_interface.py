# import necessary libaries
from chat_engine_config import get_chat_engine, question_answer
import gradio as gr

# Initialize the chat engine once
chatEngine = get_chat_engine()

def user_question_answer(question):
    """
    Function to process user questions and return answers using the chat engine.

    Args:
    - question (str): The user's question.

    Returns:
    - str: The response from the chat engine.
    """
    # Get the answer from the chat engine
    answer = question_answer(question, chatEngine)

    # Display the answer in the console for debugging or tracking
    print("Answer:", answer)

    # Return the answer as a string
    return str(answer)

# Set up Gradio interface
gr.Interface(
    fn=user_question_answer,
    inputs="text",
    outputs="text",
    title="Real Time RAG(Retrieval Augmented Generation) for AI regulations in India. 🇮🇳",
    description="Feel free to ask questions about the rules and regulations for AI in India. 🇮🇳",
).launch(debug=True, share=True)