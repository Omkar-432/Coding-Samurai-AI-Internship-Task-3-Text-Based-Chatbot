import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.metrics import edit_distance

# Download NLTK resources (if not already downloaded)
nltk.download('punkt')

# Load the CSV data into a DataFrame
df = pd.read_csv('chatbot_responses.csv')

# Function to calculate word similarity (you can use different similarity measures)
def word_similarity(word1, word2):
    return 1 - edit_distance(word1, word2) / max(len(word1), len(word2))

# Function to get chatbot response based on tokenized user input
def get_chatbot_response(user_input):
    user_tokens = word_tokenize(user_input.lower())
    best_similarity = 0
    best_response = "I'm sorry, I don't understand that."

    for index, row in df.iterrows():
        response_tokens = word_tokenize(row['user_message'].lower())
        similarity = sum(word_similarity(user_token, response_token) for user_token in user_tokens for response_token in response_tokens)
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_response = row['chatbot_response']

    # Set a threshold for similarity score below which the default response is used
    threshold = 0.2  # Adjust this threshold as needed
    if best_similarity < threshold:
        return "I'm sorry, I don't understand that."
    
    return best_response

# Function to handle user input and display chatbot response
def send_message():
    user_input = user_entry.get()
    user_entry.delete(0, tk.END)
    chatbot_response = get_chatbot_response(user_input)
    conversation_area.config(state=tk.NORMAL)
    conversation_area.insert(tk.END, f"You: {user_input}\n")
    conversation_area.insert(tk.END, f"Chatbot: {chatbot_response}\n")
    conversation_area.config(state=tk.DISABLED)
    conversation_area.see(tk.END)

# Create a tkinter window
window = tk.Tk()
window.title("Chatbot")

# Create and configure a scrolled text widget for conversation display
conversation_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=15, state=tk.DISABLED)
conversation_area.pack()

# Create an entry widget for user input
user_entry = tk.Entry(window, width=40)
user_entry.pack()

# Create a send button to trigger user input processing
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# Start the tkinter main loop
window.mainloop()
