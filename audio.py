from IPython.display import Audio, display, Javascript
from google.colab import output
from base64 import b64decode

#javascript para gravar audio

RECORD = """  

const sleep = time => new Promise(resolve => setTimeout(resolve, time))

const b2text = blob => new Promise(resolve => {

    const reader = new FileReader()

    reader.onloadend = e => resolve(e.target.result)

    reader.readAsDataURL(blob)
})

var record = time => new Promise(async resolve => {

    const stream = await navigator.mediaDevices.getUserMedia({ audio:true })

    const recorder = new MediaRecorder(stream)

    const chunks = []

    recorder.ondataavailable = e => chunks.push(e.data)

    recorder.start()

    await sleep(time)

    recorder.onstop = async ()=>{

        const blob = new Blob(chunks)

        const text = await b2text(blob)

        stream.getTracks().forEach(track => track.stop())

        resolve(text)

    }

    recorder.stop()

})

"""


def record(sec=5): #função gravar audio

    display(Javascript(RECORD))

    js_result = output.eval_js('record(%s)' % (sec * 1000))

    audio = b64decode(js_result.split(',')[1])

    file_name = 'request_audio.wav'

    with open(file_name, 'wb') as f:

        f.write(audio)

    return f'/content/{file_name}' 


print('Ouvindo...')

record_file = record()

display(Audio(record_file, autoplay=True)) #toca áudio gravado automaticamente