import pickle

def print_archive(location):
    with open('Scores/score.txt', 'rb') as data:
        arquivo = pickle.load(data)
    print(arquivo)

print_archive("Scores/score.txt")