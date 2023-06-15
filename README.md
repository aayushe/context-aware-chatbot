# context-aware-chatbot
chatbot the engages in context related conversation like a youtube video , website link or a pdf or just copy pasted text , It leverages OPENAI API 

# ChatBot

This code represents a ChatBot implemented in Python. The ChatBot utilizes various functionalities to engage in natural language conversations and provide relevant responses.

## Dependencies

The code requires the following dependencies:
- os
- nltk
- typing
- scrap
- gradio
- langchain
- threading
- pdf_helper
- FactCheck
- youtube_utils
- load_chains

## Functionality

The ChatBot includes the following key functionalities:

1. **ChatWrapper**: This class encapsulates the main logic of the ChatBot. It manages conversation history, context, and handles the processing of text or YouTube context to generate appropriate responses.

2. **Process YouTube Context**: This method processes YouTube context by extracting transcripts, chunking the content, and generating responses using the loaded YouTube chains.

3. **Process Text Context**: This method processes text-based context by loading and processing the provided context, and generating responses using the loaded context chains.

5. **gradio**: The code uses Gradio library to create a user interface for the ChatBot. It includes a text input for user questions, a textbox for context input, and an output textbox to display the generated responses.

6. **PDF Upload**: The code allows users to upload PDF files, which are converted to text-based context for processing.

## Usage

To run the ChatBot, make sure to provide your OpenAI API key in the `os.environ['OPENAI_API_KEY']` line. The code can be executed by running the `block.launch()` function, which starts the Gradio interface for the ChatBot.

Note: Additional files and modules, such as `scrap.py`, `youtube_utils.py`, and `load_chains.py`, are required to be present in the same directory for the code to run successfully.

Feel free to customize and extend the code to meet your specific requirements and enhance the ChatBot's functionality!
