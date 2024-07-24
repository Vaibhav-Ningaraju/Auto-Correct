from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def load_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file]
    return words

words = load_words('english_words.txt')

def levenshtein_distance(s, t):
    len_s = len(s)
    len_t = len(t)

    # Initialize the distance matrix
    d = [[0] * (len_t + 1) for _ in range(len_s + 1)]

    for i in range(len_s + 1):
        d[i][0] = i
    for j in range(len_t + 1):
        d[0][j] = j

    for i in range(1, len_s + 1):
        for j in range(1, len_t + 1):
            cost = 0 if s[i - 1].lower() == t[j - 1].lower() else 1
            d[i][j] = min(d[i - 1][j] + 1,      # Deletion
                          d[i][j - 1] + 1,      # Insertion
                          d[i - 1][j - 1] + cost)  # Substitution

    return d[len_s][len_t]

def capitalize_words(words):
    return [word.capitalize() for word in words]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/closest-word', methods=['GET'])
def closest_word():
    user_word = request.args.get('word')
    
    if user_word in words:
        return jsonify({'closest': [f'{user_word.capitalize()}: Correct spelling']})
    
    distances = {word: levenshtein_distance(user_word, word) for word in words}
    min_distance = min(distances.values())

    closest_words = [word for word, distance in distances.items() if distance == min_distance]
    
    # Capitalize the first letter of each closest word
    closest_words = capitalize_words(closest_words)
    
    return jsonify({'closest': closest_words if closest_words else ['No close match found']})

if __name__ == '__main__':
    app.run(debug=True)
