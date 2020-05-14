# API documentation

This is a quick documentation of the API.

## Overview

This is a quick documentation for the Speech to text API.
We tried to decribe it as well as possible even though it's actually lightweight.

### Audio data format

For the moment we are still using the same audio data format as used by the model.
So we need to convert our audio files if they don't have the required format.
The required characteriscs of the audio files are shown in the following audio
file information sample (we used the `sox` utility to dump audio data informations)

**You can use `sox` or other tools or clients library to convert the audio file before making the request. By the time, automatic conversion will be implemented on the server in the upcoming versions soon and support will be added to other formats too (mp3, ogg etc...).**

**NB:** *The lines that are not highlighted (not preceded by #) are the one that we should consider when converting audio file before using it with the API.*

    # Input File     : 'audio_file.wav'
    # Duration       : 00:00:02.06 = 33034 samples ~ 154.847 CDDA sectors
    # File Size      : 66.1k
    Channels       : 1
    Sample Rate    : 16000
    Precision      : 16-bit
    Bit Rate       : 256k
    Sample Encoding: 16-bit Signed Integer PCM

### Request Parameters

`base url: http://domain_name:8080/api/v1/tts`

`method: POST`

`header: content-type: application/json`

`body:`
`"config":` Dictionnary of configurations (file extension, fequence rates etc...). For the moment only wav files are supported and the frequence is fixed so we didn't implement config yet.

`"audio":` Dictionnary which contain either "content "or "uri". Only one of them but not both.

`"uri":` The "uri" key can be used to get audio file's uri so the server will fetch itself. This parameter is not yet supported for the moment.

`"content":` The "content" key is when the user pass the audio file directly in the request by encoding it base64. *(You can use the command `$ base64 source_audio_file -w 0 > dest_audio_file` ) to convert data to base64 on linux systems. You can look for other tools or clients libraries to do it, according to your your needs, there are several ones.*

**NB :** *Remember, as this is a REST API, we want to pass the audio file to the server via json so we have to encode it base64 first.*

Example of request body.

```javascript
{
    "config": "",
    "audio": {
        "content": "UklGRpQeA0AAD4AAAB9AAACA0YXAeAQBC...."
    }
}

```

### Output

On success we have something like this.

```javascript
{
    "result": {
        "RecognitionResult": "ayihun da nɔ wa"
    }
}

```

On error we have something like this.

```javascript
{
    "error": {
        "title": "400",
        "message": "Invalid request: Missing audio field."
    }
}

```
