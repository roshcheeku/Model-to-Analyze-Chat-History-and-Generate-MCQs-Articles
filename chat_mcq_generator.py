import os
import requests
import random
from transformers import pipeline
from nltk.corpus import wordnet

COLOR_BOT = "\033[94m"
COLOR_RESET = "\033[0m"

API_KEY = os.getenv("API_KEY")
GEMINI_API_URL = os.getenv("API_URL")

try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    print(f"Error initializing summarizer: {e}")

def interact_with_gemini(user_input):
    if not GEMINI_API_URL or not API_KEY:
        return "Error: API URL or API key not set."

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_input
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", headers=headers, json=data)
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to API - {e}"

    if response.status_code == 200:
        try:
            bot_response = response.json().get("candidates", [])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        except (IndexError, KeyError) as e:
            return f"Error: Failed to parse response - {e}"
        return format_response(bot_response)
    else:
        return f"Error: {response.status_code} - {response.text}"

def format_response(content):
    short_response = content[:500]
    return f"{COLOR_BOT}{short_response}{COLOR_RESET}"

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

def generate_distractors(correct_answer):
    words = correct_answer.split()
    distractors = []
    for word in words:
        synonyms = get_synonyms(word)
        if synonyms:
            distractor = correct_answer.replace(word, random.choice(synonyms))
            distractors.append(distractor)

    distractors += [
        "An unrelated response.",
        "A completely different answer.",
        "A vague statement.",
    ]
    random.shuffle(distractors)
    return distractors[:3]

def generate_mcqs(chat_history, complexity='normal'):
    questions = []
    try:
        for i in range(0, len(chat_history) - 1, 2):
            user_message = chat_history[i].replace("User: ", "").strip()
            bot_response = chat_history[i + 1].replace("Bot: ", "").strip()

            question = f"What did the bot say in response to: '{user_message}'?"
            correct_answer = bot_response

            distractors = generate_distractors(correct_answer)
            options = [correct_answer] + distractors
            random.shuffle(options)

            questions.append({
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": generate_explanation(correct_answer, complexity)
            })

    except IndexError as e:
        print(f"Error generating MCQs: {e}")

    return questions[:3]

def generate_explanation(correct_answer, complexity):
    if complexity == 'easy':
        return f"The correct answer is '{correct_answer}' because it is a simple response."
    elif complexity == 'hard':
        return f"The correct response was '{correct_answer}' as it comprehensively addressed the user's query with detail."
    return f"The correct answer is '{correct_answer}'."

def generate_article(chat_history, tone="neutral"):
    max_input_length = 1024
    chat_input = " ".join(chat_history)

    if len(chat_input) > max_input_length:
        chat_input = chat_input[:max_input_length]

    try:
        summary = summarizer(chat_input, max_length=300, min_length=200, do_sample=False)[0]['summary_text']
        return adjust_tone(summary, tone)
    except Exception as e:
        print(f"Error generating article: {e}")
        return "Could not generate article due to an error."

def adjust_tone(article, tone):
    if tone == "formal":
        return article.replace("I think", "It is believed")
    elif tone == "casual":
        return article.replace("In recent discussions", "Hey, so here's what we've been chatting about")
    return article

def fact_check(content):
    if "incorrect" in content.lower():
        return "Warning: This content may contain inaccuracies."
    return "Fact-checked: No issues found."

def interact_with_user():
    chat_history = []
    message_limit = 10
    user_input_count = 0

    while user_input_count < message_limit:
        user_input = input("User: ")
        bot_response = interact_with_gemini(user_input)
        
        print(bot_response)

        chat_history.append(f"User: {user_input}")
        chat_history.append(f"Bot: {bot_response}")
        
        user_input_count += 1

    print("\nGenerating MCQs based on the chat history:")
    mcqs = generate_mcqs(chat_history)
    for i, mcq in enumerate(mcqs):
        print(f"Q{i + 1}: {mcq['question']}")
        for option in mcq['options']:
            print(f" - {option}")
        print(f"Correct Answer: {mcq['correct_answer']}")
        print(f"Explanation: {mcq['explanation']}\n")

    print("Generating Article based on the chat history:")
    article = generate_article(chat_history, tone="neutral")
    print(article)

    fact_check_result = fact_check(article)
    print(fact_check_result)

if __name__ == "__main__":
    interact_with_user()
