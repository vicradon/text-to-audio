from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import numpy as np
import torch
import time
import json
import os
import math
import random

synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

def concatenate_audio(file_paths, output_path):
    audio_data_list = [sf.read(file_path)[0] for file_path in file_paths]
    concatenated_audio = np.concatenate(audio_data_list)

    sf.write(output_path, concatenated_audio, samplerate=sf.info(file_paths[0]).samplerate)

def convert_text_to_audio():
    audio_files = []
    base_path = "/tmp/python-text-to-audio/" + str(math.floor(random.randint(1, 100000)))
    os.makedirs(base_path, exist_ok=True)

    with open("input.json", "r") as json_file:
        loaded_data = json.load(json_file)

    for index, section in enumerate(loaded_data):
        speech = synthesiser(section, forward_params={"speaker_embeddings": speaker_embedding})
        filename = f"{base_path}/section-{index}.wav"
        audio_files.append(filename)
        sf.write(filename, speech["audio"], samplerate=speech["sampling_rate"])

    return audio_files


if __name__ == "__main__":
    start_time = time.time()

    audio_files = convert_text_to_audio()
    concatenate_audio(audio_files, "output.wav")

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")