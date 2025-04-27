import gradio as gr
import openai
import os
import json
import random
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Sample vector database for RAG
anime_knowledge_base = [
    {"title": "Naruto", "info": "A manga/anime series about a young ninja named Naruto Uzumaki who seeks recognition and dreams of becoming the Hokage. Created by Masashi Kishimoto."},
    {"title": "One Piece", "info": "A manga/anime series about Monkey D. Luffy and his crew searching for the world's ultimate treasure, the 'One Piece'. Created by Eiichiro Oda."},
    {"title": "Attack on Titan", "info": "A manga/anime series set in a world where humanity lives within cities surrounded by enormous walls due to the Titans. Created by Hajime Isayama."},
    {"title": "Violet Evergarden", "info": "An anime series about Violet Evergarden, a former soldier who becomes a letter writer to understand the last words of her mentor. Produced by Kyoto Animation."},
    {"title": "Clannad", "info": "A visual novel and anime series following Tomoya Okazaki as he forms relationships with various girls in his school. Famous for its emotional storytelling."},
]

def simple_vector_search(query, knowledge_base):
    """Simple keyword-based search to simulate vector search"""
    results = []
    query_words = query.lower().split()
    
    for entry in knowledge_base:
        relevance = 0
        text = entry["title"].lower() + " " + entry["info"].lower()
        for word in query_words:
            if word in text:
                relevance += 1
        
        if relevance > 0:
            results.append({"entry": entry, "relevance": relevance})
    
    results.sort(key=lambda x: x["relevance"], reverse=True)
    return [r["entry"] for r in results[:2]]  # Return top 2 relevant entries

def generate_text(prompt, mode):
    if mode == "Zero-Shot":
        # For Zero-Shot, use system prompt and user's question only
        messages = [
            {"role": "system", "content": "You are a knowledgeable anime assistant. Answer the user's questions accurately and concisely."},
            {"role": "user", "content": prompt}
        ]
    
    elif mode == "Few-Shot":
        # For Few-Shot, include examples in the system message
        system_content = """You are a knowledgeable anime assistant. Answer the user's questions accurately and concisely.
Here are some examples of how to answer questions:
User: Who is the main character in Naruto?
Assistant: Naruto Uzumaki is the main character in Naruto. This series is about a young ninja who seeks recognition from his peers and dreams of becoming the Hokage, the leader of his village. It was created by Masashi Kishimoto and has been adapted into various media, including anime and movies.
User: What is the most popular OST in Violet Evergarden?
Assistant: The most popular OST in Violet Evergarden is "Sincerely" by TRUE. This song is known for its emotional depth and connection to the series' themes of love and loss. It was created by Kyoto Animation and is based on the light novel series written by Kana Akatsuki and illustrated by Akiko Takase.
User: Who is the singer of 'Dango Daikazoku' in Clannad?
Assistant: Chata is the singer of 'Dango Daikazoku' in Clannad. This song is a recurring theme in the series and is associated with the characters' emotional journeys. It was created by Key and has been adapted into various media, including anime and movies."""
       
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]
    
    elif mode == "Chain-of-Thought":
        # Chain-of-Thought: Encourage step-by-step reasoning
        messages = [
            {"role": "system", "content": "You are a knowledgeable anime assistant. Think step-by-step to answer the question accurately."},
            {"role": "user", "content": f"Question: {prompt}\n\nLet's think through this step-by-step:"}
        ]
    
    elif mode == "Meta Prompting":
        # Meta Prompting: The model creates its own prompt first
        messages = [
            {"role": "system", "content": "You are a helpful assistant that creates effective prompts for anime questions."},
            {"role": "user", "content": f"The user wants to know about: '{prompt}'. First, create an effective prompt for an anime assistant to answer this question. Then, answer the question using that prompt."}
        ]
    
    elif mode == "Self Consistency":
        # Self Consistency: Generate multiple approaches and find consensus
        # In a real implementation, we'd make multiple API calls and compare answers
        messages = [
            {"role": "system", "content": "You are a knowledgeable anime assistant. Generate three different approaches to answering this question, then provide a final consensus answer."},
            {"role": "user", "content": f"Question: {prompt}\n\nPlease provide three different approaches to answer this question, then give your final consensus answer."}
        ]
    
    elif mode == "Generate Knowledge":
        # Generate Knowledge: First generate relevant knowledge, then answer
        messages = [
            {"role": "system", "content": "You are a knowledgeable anime assistant."},
            {"role": "user", "content": f"Question: {prompt}\n\nBefore answering, please list all relevant facts and knowledge about this topic. Then use that knowledge to provide a comprehensive answer."}
        ]
    
    elif mode == "Prompt Chaining":
        # Simulate a chain of prompts - in production, this would be multiple API calls
        messages = [
            {"role": "system", "content": "You are a knowledgeable anime assistant that uses a multi-step process to answer questions."},
            {"role": "user", "content": f"""
Question: {prompt}

Follow these steps:
1. Identify the key terms and concepts in the question
2. Retrieve relevant background information about those terms
3. Formulate a complete answer using the background information
4. Present your final answer

Please show your work for each step.
"""}
        ]
    
    elif mode == "RAG":
        # Retrieval-Augmented Generation: Retrieve information first, then generate answer
        # In a real app, this would use vector similarity search instead of keyword search
        results = simple_vector_search(prompt, anime_knowledge_base)
        retrieved_context = "\n\n".join([f"{item['title']}: {item['info']}" for item in results])
        
        messages = [
            {"role": "system", "content": "You are a knowledgeable anime assistant. Use the retrieved information to answer the question accurately."},
            {"role": "user", "content": f"""
Question: {prompt}

Here is some relevant information that might help:
{retrieved_context}

Please answer the question based on this information and your knowledge.
"""}
        ]
    
    else:
        # Default to Zero-Shot if something goes wrong
        messages = [
            {"role": "system", "content": "You are a knowledgeable anime assistant. Answer the user's questions accurately and concisely."},
            {"role": "user", "content": prompt}
        ]
   
    # Chat Completion call to OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
        max_tokens=500
    )
   
    answer = response["choices"][0]["message"]["content"].strip()
    return answer

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🎭 Advanced Prompting Techniques Demo (OpenAI GPT-3.5)")
    
    with gr.Row():
        with gr.Column():
            mode = gr.Radio(
                ["Zero-Shot", "Few-Shot", "Chain-of-Thought", "Meta Prompting", 
                "Self Consistency", "Generate Knowledge", "Prompt Chaining", "RAG"], 
                label="Select Prompting Technique", 
                value="Zero-Shot"
            )
            
            with gr.Accordion("Technique Descriptions", open=False):
                gr.Markdown("""
                - **Zero-Shot**: Direct question-answer with no examples
                - **Few-Shot**: Includes examples in the prompt to guide the model
                - **Chain-of-Thought**: Encourages step-by-step reasoning
                - **Meta Prompting**: The model creates its own prompt first
                - **Self Consistency**: Generates multiple approaches to find consensus
                - **Generate Knowledge**: Generates relevant facts before answering
                - **Prompt Chaining**: Uses a sequence of prompts for complex questions
                - **RAG (Retrieval-Augmented Generation)**: Retrieves information from a knowledge base before generating an answer
                """)
            
            prompt = gr.Textbox(
                lines=3, 
                label="Your Anime Question", 
                placeholder="Ask me anything about anime..."
            )
            
            run_button = gr.Button("Get Answer")
        
        with gr.Column():
            output = gr.Textbox(lines=20, label="Answer")
            
    run_button.click(fn=generate_text, inputs=[prompt, mode], outputs=output)

    gr.Markdown("""
    ## Sample Questions to Try
    - Who is the main character in Naruto?
    - What is the plot of Attack on Titan?
    - Compare the animation styles of Studio Ghibli and Kyoto Animation
    - Explain why One Piece has been so successful
    - What are the major themes in Violet Evergarden?
    """)

# Launch the app
demo.launch()