from flask import Flask, request
import base64

from functools import partial
from pathlib import Path
from multiprocessing import Pool
from matplotlib import pyplot as plt
import os
import shutil
import numpy as np
import pandas as pd
import librosa
import soundfile as sf
from scipy.io import wavfile
from tqdm import tqdm_notebook as tqdm
from random import randrange
import torch.nn.functional as F
# from fastai.basic_data import DatasetType
import fastai
from fastai.vision import *

counter = 1
app = Flask(__name__)


def read_file(filename, path='', sample_rate=None, trim=False):
    ''' Reads in a wav file and returns it as an np.float32 array in the range [-1,1] '''
    filename = Path(path) / filename
    file_sr, data = wavfile.read(filename)
    if data.dtype == np.int16:
        data = np.float32(data) / np.iinfo(np.int16).max
    elif data.dtype != np.float32:
        raise OSError('Encounted unexpected dtype: {}'.format(data.dtype))
    if sample_rate is not None and sample_rate != file_sr:
        if len(data) > 0:
            data = librosa.core.resample(
                data, file_sr, sample_rate, res_type='kaiser_fast')
        file_sr = sample_rate
    if trim and len(data) > 1:
        data = librosa.effects.trim(data, top_db=40)[0]
    return data, file_sr


def log_mel_spec_tfm(fname, src_path, dst_path):
    x, sample_rate = read_file(fname, src_path)

    n_fft = 1024
    hop_length = 256
    n_mels = 40
    fmin = 20
    fmax = sample_rate / 2

    mel_spec_power = librosa.feature.melspectrogram(x, sr=sample_rate, n_fft=n_fft,
                                                    hop_length=hop_length,
                                                    n_mels=n_mels, power=2.0,
                                                    fmin=fmin, fmax=fmax)
    mel_spec_db = librosa.power_to_db(mel_spec_power, ref=np.max)
    dst_fname = dst_path + '/' + fname[:-4] + '.png'
    plt.imsave(dst_fname, mel_spec_db)


def get_res():
    '''file: audio file
        returns percentage of COVID certainty [0,1]
    '''

    x, _ = librosa.load('audio.wav', sr=16000)
    sf.write('tmp.wav', x, 16000)

    fn = 'tmp.wav'
    x, sr = read_file(fn, '.')
    log_mel_spec_tfm(fn, '.', '.')

    img = plt.imread(fn[:-4] + '.png')

    learn = load_learner('')
    learn_predict = learn.predict(open_image(fn[:-4] + '.png'))
    print(learn_predict)
    return tuple(learn_predict[2].detach().cpu().numpy())[1]
            
def get_rand(isHigh):
    if isHigh:
        return randrange(5,10) / 10
    else:
        return randrange(3) / 10

@app.route('/post', methods=['GET', 'POST'])
def get_audio():
    '''gets audio file as POST request from frontend'''
    if request.method == 'POST':
        form = request.form
        file = form['file']
        wav_file = open("audio.wav", "wb")  # get audio file as base64
        file = file[35:]
        decode_string = base64.b64decode(file)  # convert base64 to wav
        wav_file.write(decode_string)
        res = get_res()
        print(res)
        return str(res)
    else:
        return "GET"


@app.route('/', methods=['GET'])
def main():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
