
from src.core.hash_password import hash_password
from src.core.authenticate import authenticate_password
from src.core.hash_qa import hash_security_question_answer

def test_hash_password():
    """
    purpose: test the accuracy of the hash_password function
    return: 0 on success, else -1
    author: Tyler Slagboom
    """

    password = "string"
    password2 = "string"
    password3 = "a"*72
    password4 = ""
    hashed_password = hash_password(password)
    hashed_password2 = hash_password(password2)
    hashed_password3 = hash_password(password3)
    hashed_password4 = hash_password(password4)

    if hashed_password == hashed_password2:
        assert False, "Hashed Passwords should not be the same output"

    if hashed_password == hashed_password3:
        assert False, "Hashed Passwords should not be the same output"

    if hashed_password == hashed_password4:
        assert False, "Hashed Passwords should not be the same output"

    if hashed_password == "string":
        assert False, "Hash failed, returned unhashed value"

    if hashed_password == "-1":
        assert False, "Password failed to be hashed"

def test_authenticate():
    """
    purpose: test the accuracy of the authenticate_password function
    return: 0 on success, else -1
    author: Tyler Slagboom
    """

    hashed_password = test_hash_password()

    if hashed_password != -1:

        if authenticate_password("a" * 72, hashed_password) != "-1":
            assert False, "Expected Authentication to fail due to length of input"

        if authenticate_password("", hashed_password) != "-1":
            assert False, "Expected authentication to fail for empty string"

        if authenticate_password("string2", hashed_password) != "-1":
            assert False, "Expected authentication to fail for wrong password"

        if not authenticate_password("string", hashed_password):
            assert False, "Expected authentication to succeed"

def test_prompts():
    """
    purpose: test the accuracy of the hash_security_question_answer function
    return: 0 on success, else -1
    author: Tyler Slagboom
    """

    d = {"one": "1", "two": "2", "three": "3"}
    l = list(d.keys())
    v = list(d.values())

    c = {"a"*72: "1"*72, "b"*72: "2"*72, "c"*72: "3"*72}
    l2 = list(c.keys())
    v2 = list(c.values())

    hashed_question_answer_pair = hash_security_question_answer(d)

    if hashed_question_answer_pair != -1:
        i = 0

        for x, y in hashed_question_answer_pair.items():

            if authenticate_password(v[i], y) == "-1":
                assert False, "Expected authentication to succeed on answer match"

            if authenticate_password(l[i], x) == "-1":
                assert False, "Expected authentication to succeed on question match"

            if authenticate_password(v2[i], y) == "1":
                assert False, "Expected authentication to fail due to length of answer input"

            if authenticate_password(l2[i], x) == "1":
                assert False, "Expected authentication to fail due to length of question input"

            i += 1