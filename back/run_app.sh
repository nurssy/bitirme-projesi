#!/bin/bash

# Sanal ortam oluşturma ve etkinleştirme (isteğe bağlı)
# python -m venv venv
# source venv/bin/activate

# Gerekli paketleri yükleme
pip install -r requirements.txt

# Flask uygulamasını çalıştırma
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0
