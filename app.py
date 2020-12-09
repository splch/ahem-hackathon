from flask import Flask
app = Flask(__name__)

def get_res(file):
    return True

@app.route('/post/audio', methods=['GET','POST'])
def get_audio():
    if request.method == 'POST':
        file = request.files['cough_file']
        return get_res(file)

@app.route('/', methods=['GET'])
def main():
    return "Hello World!"

if __name__ == '__main__':
    app.run()