Image Uploader Application
==========================

Overview
This is a simple image uploader application built using Flask, a micro web framework for Python. The application allows users to upload images, view uploaded images, and delete images.

Features
Image upload: Users can upload images in PNG, JPG, JPEG, and GIF formats.
Image display: Uploaded images are displayed on a separate page.
Image deletion: Users can delete uploaded images.
Requirements
Python 3.x
Flask
Flask-SQLAlchemy
Werkzeug
Configuration
The application uses the following configuration:

Database: SQLite (images.db)
Upload folder: static/uploads
Maximum upload size: 16 MB
Secret key: youcandecideyours (needed for flash messages)
Models
The application uses a single model, Image, to store image paths in the database.

Routes
The application has the following routes:

/: Upload image (GET, POST)
/images: Display uploaded images (GET)
/delete/<int:image_id>: Delete an image (POST)
Helper Functions
The application uses a helper function, allowed_file, to check if a file has an allowed extension.

Running the Application
To run the application, execute the following command:

python app.py
The application will start in debug mode. Open a web browser and navigate to http://localhost:5000 to access the application.#   I m a g e - U p l o a d e r - A p p l i c a t i o n  
 