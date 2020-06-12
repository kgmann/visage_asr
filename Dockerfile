FROM pykaldi/pykaldi:latest

LABEL   maintainer="Germann ATAKPA <lucatakpa@gmail.com>" \
        version="1.0" \
        description="Speech recognition API for Fon"

WORKDIR /visage_asr

COPY . .

RUN apt update && apt install -y libsox-fmt-all \
    && pip install -r requirements.txt

EXPOSE 8080

CMD [ "gunicorn", "-b", ":8080", "--access-logfile", "-", "visage_asr:app" ]
