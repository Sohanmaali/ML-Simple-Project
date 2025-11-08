# portfolio_chatbot.py

def load_portfolio(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().lower()  # lowercase for easier matching

def find_answer(user_question, portfolio_text):
    words = user_question.lower().split()
    sentences = portfolio_text.split("\n")
    
    best_match = ""
    max_matches = 0
    
    for sentence in sentences:
        match_count = sum(1 for word in words if word in sentence)
        if match_count > max_matches:
            max_matches = match_count
            best_match = sentence
    
    if best_match:
        return best_match
    else:
        return "Sorry, I don't have information on that."

def chat():
    portfolio_text = load_portfolio("portfolio.txt")
    print("Hi! Ask me anything about my portfolio. Type 'exit' to quit.")
    
    while True:
        user_question = input("You: ")
        if user_question.lower() == "exit":
            print("Goodbye!")
            break
        answer = find_answer(user_question, portfolio_text)
        print(f"Bot: {answer}")

if __name__ == "__main__":
    chat()
