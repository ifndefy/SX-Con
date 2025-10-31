from core import hash_password

def hash_security_question_answer(question_answer_pair : dict[str, str]) -> dict[str, str]:
    # dictionary is key,value pair. key = question, value = answer
    if not question_answer_pair:
        return -1

    hashed_question_answer_pair = {}
    # Hash all answers (values)
    for key, value in question_answer_pair.items():
        if value == None:
            return -1
        hashed_answer = hash_password.hash_password(value)
        hashed_question = hash_password.hash_password(key)
        hashed_question_answer_pair[hashed_question] = hashed_answer

    return hashed_question_answer_pair

if __name__ == '__main__':
    # Example usage for testing
    question = "What color was your first car?"
    print(question)
    answer = input("Please give an answer to the security question:")

    """
    q_a_pair = {"What was the name of your first pet?": "Buddy",
    "What city were you born in?": "Seattle",
    "What is your favorite teacher's name?": "Mr. Johnson"}"""
    q_a_pair = {question: answer}
    hashed_q_a_pair = hash_security_question_answer(q_a_pair)

    print("q_a_pair: ", q_a_pair)
    print("hashed_q_a_pair: ",hashed_q_a_pair)