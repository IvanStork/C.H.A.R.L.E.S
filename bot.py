# bot.py

def chatbot():
    from chatterbot import ChatBot

    from chatterbot.trainers import ListTrainer
    from cleaner import clean_corpus
    CORPUS_FILE = "charlie_training_data.txt"
    chatbot = ChatBot("Charlie")


    trainer = ListTrainer(chatbot)
    cleaned_corpus = clean_corpus(CORPUS_FILE)
    trainer.train(cleaned_corpus)

    exit_conditions = (":q", "quit", "exit")

    while True:

        query = input("> ")

        if query in exit_conditions:
            print(f" Goodbye!")
            break

        else:

            print(f" {chatbot.get_response(query)}")

chatbot()