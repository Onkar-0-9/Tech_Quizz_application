from pymongo import MongoClient

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017")
db = client.quizapp
questions_collection = db.questions

# List of questions with options and answers
questions = [
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Michelangelo"],
        "answer": "Leonardo da Vinci"
    },
    {
        "question": "What is the capital of Japan?",
        "options": ["Beijing", "Seoul", "Tokyo", "Bangkok"],
        "answer": "Tokyo"
    },
    {
        "question": "Which element has the chemical symbol 'Au'?",
        "options": ["Silver", "Gold", "Copper", "Aluminum"],
        "answer": "Gold"
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
        "answer": "William Shakespeare"
    },
    # Add more questions here following the same format
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"],
        "answer": "Pacific Ocean"
    },
    {
        "question": "Which country is known as the Land of the Rising Sun?",
        "options": ["China", "Korea", "Japan", "Vietnam"],
        "answer": "Japan"
    },
    {
        "question": "What is the chemical formula for water?",
        "options": ["CO2", "H2O", "O2", "N2"],
        "answer": "H2O"
    },
    {
        "question": "Who invented the telephone?",
        "options": ["Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "Albert Einstein"],
        "answer": "Alexander Graham Bell"
    },
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["Mars", "Saturn", "Jupiter", "Neptune"],
        "answer": "Jupiter"
    }
    # Continue adding more questions...
]

# Insert questions into MongoDB
def add_questions_to_db():
    try:
        # Clear existing questions
        questions_collection.delete_many({})
        
        # Insert new questions
        result = questions_collection.insert_many(questions)
        print(f"Successfully added {len(result.inserted_ids)} questions to the database")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    add_questions_to_db()