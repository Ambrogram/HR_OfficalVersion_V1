import matplotlib.pyplot as plt

def plot_results(data):
    plt.plot(data)
    plt.xlabel('Event')
    plt.ylabel('Reaction Time')
    plt.title('Reaction Time Analysis')
    plt.show()

def analyze_words(data):
    confirming_words = [word for word in data if word['correct']]
    confusing_words = [word for word in data if not word['correct']]
    return confirming_words, confusing_words
