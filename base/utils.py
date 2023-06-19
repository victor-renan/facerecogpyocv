import re


def test_code(test_params, code):
    tests_passed = []
    for param in test_params:
        if re.search(param, code):
            tests_passed.append(param)

    if len(tests_passed) == len(test_params):
        return True
    else:
        return False


def teste_desafio1(code):
    return test_code(
        test_params=[
            "import cv2",
            "while True:",
            "VideoCapture",
            "webdriver",
            "selenium"],
        code=code)


def teste_desafio2(code):
    return test_code(
        test_params=[
            "import cv2",
            "while True:",
            "VideoCapture",
            "autentica"],
        code=code)
