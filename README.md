Virtual Try-On Studio 👕👗🖥️

A Virtual Try-On Web Application built using Flask and Computer Vision techniques that enables users to upload their photo and a clothing item image to preview how the clothes would look on them.

This project was developed as part of my academic work, where I initially experimented with pose detection, background removal, cloth alignment, and blending techniques. Later, to overcome certain limitations and achieve realistic outputs, I integrated a Try-On Diffusion model via API for generating high-quality try-on results.

🚀 Features

Upload a user image and a clothing image.

Automatic format conversion & validation (supports jpg, png, gif, tiff, webp, etc.).

Preprocessing pipeline: resizing, background cleaning, and image alignment.

Realistic virtual try-on preview.

Download option for saving the try-on result.

Clean, modern UI with drag & drop support.

🛠️ Tech Stack

Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

Image Processing: Pillow (PIL), initial experiments with OpenCV

Try-On Engine: Integrated diffusion-based try-on model

Other Tools: Werkzeug, Requests

📂 Project Structure
virtual-tryon/                 # repo root
├─ version-1/                  
│  ├─ src/
│  ├─ U-2-Net/                
│  ├─ VITON-HD/               
│  ├─ models/                  
│  └─ README.md                
│
├─ version-2/                  # working Flask app (what you'll demo)
│  ├─ app.py                   # Main Flask application
│  ├─ tryon_api.py             # API integration logic (if separated)
│  ├─ requirements.txt         # Python dependencies
│  ├─ templates/
│  │   └─ index.html
│  ├─ static/
│  │   └─ uploads/             
│  └─ .env.example             # Example env file (without real API key)
│
├─ .gitignore
├─ .env.example                # global example (optional)
├─ README.md                   # top-level README summarizing both versions
└─ LICENSE

⚙️ Installation & Setup

Clone the repository

git clone https://github.com/your-username/virtual-tryon.git
cd virtual-tryon


Create & activate a virtual environment

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate


Install dependencies

pip install -r requirements.txt


Set environment variables

Copy .env.example to .env

Add your API key & secret values

RAPIDAPI_KEY=your_api_key_here
RAPIDAPI_HOST=try-on-diffusion.p.rapidapi.com
FLASK_SECRET_KEY=your_secret_here
UPLOAD_FOLDER=static/uploads


Run the application

python app.py


Navigate to: http://127.0.0.1:5000

📸 Screenshots (Add Your Own)

Upload some screenshots of:

Uploading user & clothing images

Try-On result preview

Download functionality

📚 Learning Journey

This project reflects my exploration of computer vision and AI:

🖼️ Attempted pose detection to align body & clothes.

✂️ Worked on background removal & cloth segmentation.

🎨 Experimented with cloth warping & blending using OpenCV & Pillow.

⚡ Finally, integrated a diffusion-based Try-On model for high-quality results.

It represents a balance of research, trial & error, and real-world implementation.

🔮 Future Scope

Improve cloth alignment with advanced pose estimation.

Add support for 3D garments.

Enhance UI with multiple try-on previews & side-by-side comparison.

Deploy the project on cloud platforms (Heroku / AWS / GCP).



👨‍💻 Author

A. Sanjay Goud
3rd Year | Data Science & AI Student
