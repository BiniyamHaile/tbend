import torch
from transformers import VitsTokenizer, VitsModel, set_seed
import os
import subprocess
import scipy


tokenizer = VitsTokenizer.from_pretrained(os.path.join("facebook/mms-tts-tir"))
model = VitsModel.from_pretrained(os.path.join("facebook/mms-tts-tir"))

def uromanize(input_string, uroman_path):
    """Convert non-Roman strings to Roman using the `uroman` perl package."""
    # script_path = os.path.join(uroman_path, "bin", "uroman.pl")
    # script_path = "./uroman/bin/uroman.pl"
    script_path =  os.path.join(os.path.join("base" , "tts" , "uroman", "bin", "uroman.pl"))

    print(script_path)
    command = ["perl", script_path]

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Execute the perl command
    stdout, stderr = process.communicate(input=input_string.encode())

    if process.returncode != 0:
        print("Process is not 0 Error {process.returncode}: {stderr.decode()}")
        return "Process is not 0 Error {process.returncode}: {stderr.decode()}"
        # raise ValueError(f"Error {process.returncode}: {stderr.decode()}")

    # Return the output as a string and skip the new-line character at the end
    return stdout.decode()[:-1]

async def synthesis(text  , newsId):
    
    try:
        print("here-   - - - - - -")
        uromaized_text = uromanize(text, "./uroman")
        print("here2 ------ uromanizing finished")
        inputs = tokenizer(text=uromaized_text, return_tensors="pt")
        print('tokenized value passed')
        set_seed(555)  # make deterministic
        print("seeded")
        with torch.no_grad():
            
            outputs = model(inputs["input_ids"])

        waveform = outputs.waveform[0]
        
        # Convert waveform to 16-bit PCM values
        waveform = (waveform * 32767.0).numpy().astype('int16')
        # model.config.sampling_rate
        scipy.io.wavfile.write(os.path.join(newsId + ".wav"), rate=16000, data=waveform)
        print("it has returned true!")
        return newsId + ".wav"
    except Exception as e:
        print(e)
        return e
        


