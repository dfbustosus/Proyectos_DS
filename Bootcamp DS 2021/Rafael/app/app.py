from flask import Flask, request, render_template
import system_recommendation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/', methods=['POST'])
def get_user_id():
    user_id = request.form['user_id']

    if(len(user_id) > 0):
        recommendation =  system_recommendation.knn(int(user_id), 10)
        return render_template('index.html', recommendation=recommendation, user_id=user_id)
    else:
        return render_template('index.html')