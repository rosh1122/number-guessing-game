from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Game state
secret_number = random.randint(1, 100)
attempts = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    global attempts, secret_number
    data = request.get_json()

    try:
        guess = int(data.get('guess'))
    except ValueError:
        return jsonify({
            'message': 'Invalid input! Please enter a number.',
            'attempts': attempts,
            'status': 'ongoing'
        })

    if guess < 1 or guess > 100:
        return jsonify({
            'message': 'Please enter a number between 1 and 100.',
            'attempts': attempts,
            'status': 'ongoing'
        })

    attempts += 1

    if guess < secret_number:
        return jsonify({
            'message': 'Too low! Try again.',
            'attempts': attempts,
            'status': 'ongoing'
        })
    elif guess > secret_number:
        return jsonify({
            'message': 'Too high! Try again.',
            'attempts': attempts,
            'status': 'ongoing'
        })
    else:
        return jsonify({
            'message': f'🎉 Congratulations! You guessed the number in {attempts} attempts.',
            'attempts': attempts,
            'status': 'won'
        })

@app.route('/restart')
def restart():
    global secret_number, attempts
    secret_number = random.randint(1, 100)
    attempts = 0
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
