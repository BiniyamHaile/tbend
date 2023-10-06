import sys
from ttsmms import TTS ,download
import os
import scipy.io.wavfile
import json
# som_dir_path = "./data/som"# lang_code, dir for save model
som_dir_path =  download("orm", os.path.join('data'))
somtts=TTS(som_dir_path )

async def synthesis(text, newsId):
    
    wav=  somtts.synthesis(text)

    wavfile = wav['x']
    wavfile.shape
    scipy.io.wavfile.write( os.path.join(  newsId + ".wav"), 16000, wavfile)
    # somtts.synthesis(text, newsId + ".wav")
    return  newsId + ".wav"

