from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from transformers import CLIPProcessor, CLIPModel, GPT2LMHeadModel, GPT2Tokenizer
import torch
from PIL import Image
import os
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS
# Set a folder to save uploaded images temporarily
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load Models
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
gpt_model = GPT2LMHeadModel.from_pretrained("gpt2")
gpt_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def generate_image_features(images):
    """Generate image features using CLIP model."""
    image_features = []
    for image in images:
        # Open the image file
        img = Image.open(image).convert("RGB")
        # Preprocess the image and convert to tensor
        inputs = clip_processor(images=img, return_tensors="pt")
        # Generate image features using CLIP
        with torch.no_grad():
            features = clip_model.get_image_features(**inputs)
        image_features.append(features)
    return image_features

def generate_test_instructions(context, image_features):
    """Generate test instructions using GPT model."""
    # Create a prompt with context and image descriptions
    prompt = f"Context: {context}\n\n"
    prompt += "Describe testing instructions for the features depicted in the screenshots:\n"
    # Adding some mock descriptions based on image features as an example
    for idx, feature in enumerate(image_features):
        prompt += f"Image {idx+1}: [description from image features]\n"

    # Generate text using GPT
    inputs = gpt_tokenizer.encode(prompt, return_tensors="pt")
    outputs = gpt_model.generate(inputs, max_length=500)
    response_text = gpt_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response_text

@app.route('/api/describe', methods=['POST'])
def describe():
    """API endpoint to describe testing instructions based on uploaded images and context."""
    if 'images' not in request.files:
        return jsonify({'error': 'No images uploaded'}), 400

    images = request.files.getlist('images')
    if not images:
        return jsonify({'error': 'No images uploaded'}), 400

    image_paths = []
    for image in images:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        image_paths.append(image_path)

    try:
        # Generate image features using CLIP
        image_features = generate_image_features(image_paths)

        # Generate testing instructions using GPT-2
        instructions = generate_test_instructions(context, image_features)

        return jsonify({'instructions': instructions})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        # Clean up uploaded files
        for path in image_paths:
            os.remove(path)

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
