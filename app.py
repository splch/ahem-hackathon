from flask import Flask, request
import base64
app = Flask(__name__)


def get_res():
    '''file: audio file
        returns percentage of COVID certainty [0,1]
    '''
    return perc


@app.route('/post', methods=['GET', 'POST'])
def get_audio():
    '''gets audio file as POST request from frontend'''
    if request.method == 'POST':
        try:
            form = request.form
            file = form['file']
            wav_file = open("audio.wav", "wb") # get audio file as base64
            file = file[35:]
            decode_string = base64.b64decode(file) # convert base64 to wav
            wav_file.write(decode_string)
            print("SUCCESS")
            return get_res()
        except Exception as e:
            print("EXCEPTION: " + str(e))
            return "-1"
    else:
        return "GET"


@app.route('/', methods=['GET'])
def main():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
