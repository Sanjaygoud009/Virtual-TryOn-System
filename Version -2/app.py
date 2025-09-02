from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from PIL import Image
import os
import requests
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploads")
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'}
MIN_SIZE = (256, 256)  # Minimum image size (adjust based on API docs if available)
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "try-on-diffusion.p.rapidapi.com")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "dev_secret")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper Functions
def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_jpg(image_path):
    """Convert unsupported formats to JPG."""
    img = Image.open(image_path)
    if img.format.lower() not in ['jpeg', 'jpg', 'png']:
        new_path = os.path.splitext(image_path)[0] + '.jpg'
        img.convert('RGB').save(new_path, 'JPEG')
        return new_path
    return image_path

@app.route('/', methods=['GET', 'POST'])
def home():
    avatar_preview = None
    clothing_preview = None
    tryon_image = None
    error = None

    if request.method == 'POST':
        # Check if files are present in the request
        if 'avatar_image' not in request.files or 'clothing_image' not in request.files:
            flash("Please upload both images", "error")
            return redirect(url_for('home'))

        avatar_file = request.files['avatar_image']
        clothing_file = request.files['clothing_image']

        # Validate filenames
        if avatar_file.filename == '' or clothing_file.filename == '':
            flash("Please select both images", "error")
            return redirect(url_for('home'))

        if not allowed_file(avatar_file.filename):
            flash("Avatar image must be a supported format (.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp)", "error")
            return redirect(url_for('home'))

        if not allowed_file(clothing_file.filename):
            flash("Clothing image must be a supported format (.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp)", "error")
            return redirect(url_for('home'))

        # Save files securely
        avatar_filename = secure_filename(avatar_file.filename)
        clothing_filename = secure_filename(clothing_file.filename)
        avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename)
        clothing_path = os.path.join(app.config['UPLOAD_FOLDER'], clothing_filename)
        avatar_file.save(avatar_path)
        clothing_file.save(clothing_path)

        # Convert unsupported formats to JPG
        avatar_path = convert_to_jpg(avatar_path)
        clothing_path = convert_to_jpg(clothing_path)

        # Validate image sizes
        try:
            avatar_img = Image.open(avatar_path)
            clothing_img = Image.open(clothing_path)
            avatar_size = avatar_img.size
            clothing_size = clothing_img.size

            if avatar_size[0] < MIN_SIZE[0] or avatar_size[1] < MIN_SIZE[1]:
                flash(f"Avatar image too small. Minimum size is {MIN_SIZE[0]}x{MIN_SIZE[1]} pixels. Current size: {avatar_size[0]}x{avatar_size[1]}", "error")
                return redirect(url_for('home'))

            if clothing_size[0] < MIN_SIZE[0] or clothing_size[1] < MIN_SIZE[1]:
                flash(f"Clothing image too small. Minimum size is {MIN_SIZE[0]}x{MIN_SIZE[1]} pixels. Current size: {clothing_size[0]}x{clothing_size[1]}", "error")
                return redirect(url_for('home'))
        except Exception as e:
            flash(f"Error processing images: {str(e)}", "error")
            return redirect(url_for('home'))

        # Call the external API
        url = f"https://{RAPIDAPI_HOST}/try-on-file"
        try:
            files = {
                "clothing_image": ("cloth_temp.png", open(clothing_path, "rb"), "image/png"),
                "avatar_image": ("user_temp.jpg", open(avatar_path, "rb"), "image/jpeg")
            }
            headers = {
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": RAPIDAPI_HOST
            }

            response = requests.post(url, files=files, headers=headers)
            if response.status_code == 200:
                result_image_path = os.path.join(app.config['UPLOAD_FOLDER'], "tryon_result.jpg")
                with open(result_image_path, "wb") as f:
                    f.write(response.content)
                tryon_image = os.path.basename(result_image_path)  # ensures only filename
                flash("Try-On successful!", "success")
            else:
                flash(f"API Error: {response.status_code} - {response.text}", "error")
        except Exception as e:
            flash(f"API request failed: {str(e)}", "error")

        # Pass previews to the template
        avatar_preview = avatar_filename
        clothing_preview = clothing_filename

    return render_template('index.html', avatar_preview=avatar_preview, clothing_preview=clothing_preview, tryon_image=tryon_image)

@app.route('/download')
def download():
    try:
        result_image_path = os.path.join(app.config['UPLOAD_FOLDER'], "tryon_result.jpg")
        if os.path.exists(result_image_path):
            return send_file(result_image_path, as_attachment=True)
        else:
            flash("Result image not found", "error")
            return redirect(url_for('home'))
    except Exception as e:
        flash(f"Download failed: {str(e)}", "error")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)