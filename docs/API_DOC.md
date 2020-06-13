# API documentation

This is a quick documentation of the API.

## Overview

This is a quick documentation for the Speech to text API.
We tried to decribe it as well as possible even though it's actually lightweight.

### Audio data format

The model need a specific type of file as input so to simplify the usage of the API we
decided to do all conversion in the backend. The user just need to add the format of the file
in the config field of the API request. The currently supported format are *{'wav', 'ogg', 'mp3', 'gsm'}*.

**For informational purpose you can use `sox` or other tools or clients library to get audio file's informaions or to convert them in other format.**

**NB:** *For informational purpose this is an example of the characterisics the audio file that has to be passed as input to the model. The lines that are not highlighted (not preceded by #) are the one that we should consider when converting audio file before using it with the API. But the API user don't need to care about this anymore because automatic conversion is already done in backend.*

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

___

> `"config":` Dictionnary of configurations (file format, file extension, fequence rates etc...). For the moment only **{'wav', 'ogg', 'mp3', 'gsm'}** format are supported and we just need to specify the "format" in the config (The other configurations may be implemented later).
> `"format":` The "format" field inside "config" is the format of the audio file. Once the format is given all the required conversion are automatically done in the backend.

___

>`"audio":` Dictionnary which contain either "content "or "uri". Only one of them but not both.
>`"uri":` The "uri" key can be used to get audio file's uri so the server will fetch itself. This parameter is not yet supported for the moment.
>`"content":` The "content" key is when the user pass the audio file directly in the request by encoding it base64. *(You can use the command `$ base64 source_audio_file -w 0 > dest_audio_file` ) to convert data to base64 on linux systems. You can look for other tools or clients libraries to do it, according to your your needs, there are several ones.*

___

**NB :** *Remember, as this is a REST API, we want to pass the audio file to the server via json so we have to encode it base64 first.*

Example of request body.

```javascript
{
    "config": {
        "format": "wav"
    },
    "audio": {
        "content": "UklGRpQeA0AAD4AAAB9AAACA0YXAeAQBC...."
    }
}
```

### Output

On success we can have something like this.

```javascript
{
    "result": {
        "RecognitionResult": "ayihun da nɔ wa"
    }
}
```

On error we can have something like this.

```javascript
{
    "error": {
        "title": "400",
        "message": "Invalid request: Missing audio field."
    }
}
```
