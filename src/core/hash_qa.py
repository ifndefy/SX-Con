from src.core import hash_password

import utils.logger.logger as log

def hash_security_question_answer(question_answer_pair : dict[str, str]) -> dict[str, str] | int:
    # dictionary is key,value pair. key = question, value = answer
    if not question_answer_pair:
        log.error(f"ERROR: question_answer_pair is empty")
        return -1

    hashed_question_answer_pair = {}
    # Hash all answers (values)
    for key, value in question_answer_pair.items():
        if value is None:
            log.error(f"ERROR: No answer found for question {key}")
            return -1
        hashed_answer = hash_password.hash_password(value)
        hashed_question = hash_password.hash_password(key)
        hashed_question_answer_pair[hashed_question] = hashed_answer

    return hashed_question_answer_pair