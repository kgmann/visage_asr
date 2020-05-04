FROM pykaldi/pykaldi:latest

LABEL   maintainer="Germann ATAKPA <lucatakpa@gmail.com>" \
        version="1.0" \
        description="Speech recogntion API for Fon"

WORKDIR /visage_asr

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "gunicorn", "-b", ":8080", "--access-logfile", "-", "visage_asr:app" ]
