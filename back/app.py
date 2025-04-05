from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import model
import os

app = Flask(__name__)
CORS(app)  # Frontend ile iletişim için CORS'u aktif ediyoruz

# MySQL veritabanı yapılandırması
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:211213058nA@localhost:3310/file_uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

# Fotoğraf tablosu modeli
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    

# Veritabanını oluştur
with app.app_context():
    db.create_all()

# Fotoğraf yükleme klasörünü ayarla
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Dosya adını güvenli hale getirme
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    cnn_model = model.load_selected_model(0)

    try:
        # Dosyayı sunucuda kaydet
        file.save(filepath)

        model.predict_image(cnn_model, filepath)

        # Dosya bilgilerini veritabanına kaydet
        new_photo = Photo(filename=filename, filepath=filepath)
        db.session.add(new_photo)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully', 'filename': filename, 'filepath': filepath}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Tüm fotoğrafları getirme endpoint'i
@app.route('/photos', methods=['GET'])
def get_photos():
    photos = Photo.query.all()
    return jsonify([{'id': photo.id, 'filename': photo.filename, 'filepath': photo.filepath} for photo in photos])

if __name__ == '__main__':
    app.run(debug=True)
