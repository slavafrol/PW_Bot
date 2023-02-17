questions = {
    "Сколько стоит вход в турнир?" : {"цена", "стоимость", "стоит"},
    "Какие критерии для входа в турнир?" : {"критерии", "требования"},
    "Какие правила участия турнира?" : {"правила"},
    "Сколько будет длиться турнир?" : {"длиться", "длительность"},
    "Призовой фонд" : {"приз", "фонд", "призовой"},
    "Подать жалобу на игрока" : {"жалоба", "пожаловаться"}
}

greet = {
    "привет",
    "прив",
    "ку",
    "здравствуй"
    "здравствуйте",
    "приветствую"
}

def to_alpha(str):
    return ''.join([i for i in str if i.isalpha() or i == " "])

def check_name(name):
    return name[0].isupper() and name[1:].islower() and len(name) < 21

def detect_question(q, questions = questions):
    user_input = set(to_alpha(q).split(" "))

    for question in questions.keys():
        if user_input.intersection(questions[question]):
            return(question)
    return

print(detect_question("a?"))