questions = [
    {
        "question": "Which AWS service provides serverless computing?",
        "options": ["EC2", "Lambda", "S3", "DynamoDB"],
        "answer": "Lambda"
    },
    {
        "question": "What protocol was developed as part of ARPANET for client-server communication?",
        "options": ["FTP", "HTTP", "TCP/IP", "SMTP"],
        "answer": "TCP/IP"
    }
]


def start_interview():
    print("Welcome to the Department of Technology interview!")
    for q in questions:
        print(f"\n{q['question']}")
        for i, option in enumerate(q["options"], start=1):
            print(f"{i}. {option}")
        user_answer = input("Choose the correct option (1-4): ")
        if q["options"][int(user_answer) - 1] == q["answer"]:
            print("Correct!")
        else:
            print("Incorrect! Try again.")
            return False
    print("Congratulations! You're hired.")
    return True
