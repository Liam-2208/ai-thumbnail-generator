from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import io
from flask import Flask, request, send_file, render_template
from diffusers import StableDiffusionPipeline
import torch

# Load Stable Diffusion model
sd_model = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
sd_model = sd_model.to("cuda" if torch.cuda.is_available() else "cpu")

# (make sure render_template is imported)
print("🔥 Flask app is starting...")

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-thumbnail', methods=['POST'])
def generate_thumbnail():
    data = request.get_json()
    title = data.get('title', 'Untitled')
    style = data.get('style', 'bold')

    # Create a blank image
    img = Image.new('RGB', (1280, 720), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Load font (use a system font or include one in your project)
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    # Draw text
    draw.text((50, 300), title, font=font, fill=(255, 255, 255))

    # Save to memory
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

@app.route('/upload-thumbnail', methods=['POST'])
def upload_thumbnail():
    title = request.form.get('title', 'Untitled')
    style = request.form.get('style', 'bold')
    image_file = request.files.get('image')
    print("🧠 AI branch activated:", not image_file)

    # 🧠 Generate image with AI if no upload provided
    if image_file:
        img = Image.open(image_file).convert('RGB').resize((1280, 720))
    else:
        prompt = f"{style} YouTube thumbnail background for: {title}"
        print(f"🧠 Generating thumbnail using prompt: {prompt}")
        generated_image = sd_model(prompt).images[0]
        img = generated_image.convert('RGB').resize((1280, 720))

    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    draw.text((50, 300), title, font=font, fill=(255, 255, 255))
    if image_file and image_file.filename != '':
        img = Image.open(image_file).convert('RGB').resize((1280, 720))

    img_io = io.BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    if image_file and image_file.filename != '':
        print("📸 Image uploaded successfully:", image_file.filename)
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True, port=8000)