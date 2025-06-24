from flask import Flask, render_template, request, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from io import BytesIO
from config import Config
from models import db, ImageModel
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.cli.command("create-tables")
def create_tables():
    """Команда для создания всех необходимых таблиц."""
    db.create_all()
    print("Tables have been created!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files.get('file')
        
        if not file or not allowed_file(file.filename):
            flash("Invalid file format.")
            return redirect(request.url)
        
        try:
            image_data = file.read()
            file.seek(0)
            
            filename = secure_filename(file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(img_path)
            
            image = Image.open(BytesIO(image_data))
            extracted_text = pytesseract.image_to_string(image)
            
            new_image = ImageModel(filename=filename, text=extracted_text)
            db.session.add(new_image)
            db.session.commit()
            
            return render_template('result.html', text=extracted_text)
        
        except Exception as e:
            flash(f"An error occurred while processing the image: {str(e)}")
            return redirect(request.url)
    
    return render_template('upload.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)