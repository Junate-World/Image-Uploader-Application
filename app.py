from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'youcandecideyours'  # Needed for flash messages

db = SQLAlchemy(app)

# Model to store image paths
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(150), nullable=False)

# Create the tables within an app context
with app.app_context():
    db.create_all()

# Route to upload image
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            new_image = Image(image_file=filename)
            db.session.add(new_image)
            db.session.commit()
            flash('Image successfully uploaded!', 'success')
            return redirect(url_for('uploaded_images'))
    
    return render_template('upload.html')

# Route to display uploaded images
@app.route('/images')
def uploaded_images():
    images = Image.query.all()
    return render_template('images.html', images=images)

# Route to delete an image
@app.route('/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    
    try:
        # Remove the image from the file system
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.image_file)
        if os.path.exists(image_path):
            os.remove(image_path)
        
        # Delete the image entry from the database
        db.session.delete(image)
        db.session.commit()

        flash('Image successfully deleted!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting image', 'error')
    
    return redirect(url_for('uploaded_images'))

# Helper function to check allowed file extensions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
