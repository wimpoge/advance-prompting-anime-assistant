# Advanced Prompting Anime Assistant

An interactive Gradio application demonstrating various AI prompting techniques using OpenAI's GPT-3.5 model to answer anime-related questions.

## Overview

This application showcases eight different prompting techniques that can be used to extract different types of responses from large language models. The demo focuses on anime knowledge as the subject domain.

## Features

- Multiple prompting techniques:
  - **Zero-Shot**: Direct question-answer with no examples
  - **Few-Shot**: Includes examples in the prompt to guide the model
  - **Chain-of-Thought**: Encourages step-by-step reasoning
  - **Meta Prompting**: The model creates its own prompt first
  - **Self Consistency**: Generates multiple approaches to find consensus
  - **Generate Knowledge**: Generates relevant facts before answering
  - **Prompt Chaining**: Uses a sequence of prompts for complex questions
  - **RAG (Retrieval-Augmented Generation)**: Retrieves information from a knowledge base before generating an answer

- Simple vector database simulation for RAG implementation
- Interactive UI with technique descriptions
- Sample questions to try out

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install gradio openai python-dotenv
   ```
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run the application:
```
python app.py
```

Then open your web browser and go to the URL displayed in the terminal (typically http://127.0.0.1:7860).

## How It Works

1. Select a prompting technique from the radio button options
2. Enter your anime-related question in the text box
3. Click "Get Answer" to receive a response
4. The answer will be displayed in the output area

## Sample Vector Database

The application includes a small sample knowledge base of anime series information that is used for the RAG demonstration:
- Naruto
- One Piece
- Attack on Titan
- Violet Evergarden
- Clannad

## Example Questions

- Who is the main character in Naruto?
- What is the plot of Attack on Titan?
- Compare the animation styles of Studio Ghibli and Kyoto Animation
- Explain why One Piece has been so successful
- What are the major themes in Violet Evergarden?

## Technical Notes

- The RAG implementation uses a simple keyword-based search to simulate vector search functionality
- For production use, consider implementing proper vector embeddings and similarity search
- Self Consistency and Prompt Chaining would typically involve multiple API calls in a production environment

## Acknowledgements

- OpenAI for the GPT-3.5 API
- Gradio for the interactive UI framework
