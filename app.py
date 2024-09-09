# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from werkzeug.utils import secure_filename
# from transformers import CLIPProcessor, CLIPModel, GPT2LMHeadModel, GPT2Tokenizer
# import torch
# from PIL import Image
# import os
# import traceback

# app = Flask(__name__)
# CORS(app)  

# @app.route('/')
# def home():
#     return "Flask server is running!"

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
# clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
# gpt_model = GPT2LMHeadModel.from_pretrained("gpt2")
# gpt_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# if gpt_tokenizer.pad_token_id is None:
#     gpt_tokenizer.pad_token_id = gpt_tokenizer.eos_token_id

# def generate_image_features(images):
#     """Generate image features using CLIP model."""
#     image_features = []
#     for image_path in images:
#         try:
#             img = Image.open(image_path).convert("RGB")
#             inputs = clip_processor(images=img, return_tensors="pt")
#             with torch.no_grad():
#                 features = clip_model.get_image_features(**inputs)
#             image_features.append(features)
#         except Exception as e:
#             print(f"Error processing image {image_path}: {e}")
#             continue
#     return image_features

# def generate_test_instructions(context, image_features):
#     """Generate test instructions using GPT model."""
#     prompt = f"Context: {context}\n\nDescribe testing instructions for the features depicted in the screenshots:\n"
#     for idx, _ in enumerate(image_features):
#         prompt += f"Image {idx+1}: [description from image features]\n"

#     try:
#         inputs = gpt_tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=1024)
#         attention_mask = torch.ones(inputs['input_ids'].shape, dtype=torch.long)
#         outputs = gpt_model.generate(inputs['input_ids'], attention_mask=attention_mask, max_length=500)
#         response_text = gpt_tokenizer.decode(outputs[0], skip_special_tokens=True)
#     except Exception as e:
#         print(f"Error generating instructions: {e}")
#         response_text = "Error generating instructions."

#     return response_text

# @app.route('/api/describe', methods=['POST'])
# def describe():
#     """API endpoint to describe testing instructions based on uploaded images and context."""
#     if 'images' not in request.files:
#         return jsonify({'error': 'No images uploaded'}), 400

#     images = request.files.getlist('images')
#     if not images:
#         return jsonify({'error': 'No images uploaded'}), 400

#     context = request.form.get('context', 'Default context for generating instructions')

#     image_paths = []
#     for image in images:
#         filename = secure_filename(image.filename)
#         image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         image.save(image_path)
#         image_paths.append(image_path)

#     try:
#         image_features = generate_image_features(image_paths)
#         instructions = generate_test_instructions(context, image_features)
#         return jsonify({'instructions': instructions})
#     except Exception as e:
#         error_message = str(e)
#         print(f"Error in /api/describe: {error_message}")
#         print(traceback.format_exc())
#         return jsonify({'error': error_message}), 500
#     finally:
#         for path in image_paths:
#             if os.path.exists(path):
#                 os.remove(path)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from transformers import CLIPProcessor, CLIPModel, GPT2LMHeadModel, GPT2Tokenizer
import torch
from PIL import Image
import os
import traceback

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Flask server is running!"

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
gpt_model = GPT2LMHeadModel.from_pretrained("gpt2")
gpt_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

if gpt_tokenizer.pad_token_id is None:
    gpt_tokenizer.pad_token_id = gpt_tokenizer.eos_token_id

def generate_image_features(images):
    image_features = []
    for image_path in images:
        try:
            img = Image.open(image_path).convert("RGB")
            inputs = clip_processor(images=img, return_tensors="pt")
            with torch.no_grad():
                features = clip_model.get_image_features(**inputs)
            image_features.append(features)
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            continue
    return image_features

def generate_test_instructions(context, image_features):
    prompt = f"Context: {context}\n\n"
    prompt += "Generate detailed test cases for each functionality based on the provided images:\n"
    for idx, _ in enumerate(image_features):
        prompt += f"Test Case {idx+1}:\n"
        prompt += "Description: Describe the functionality that this test case is for.\n"
        prompt += "Pre-conditions: List any setup or conditions required before executing the test.\n"
        prompt += "Testing Steps:\n"
        prompt += "1. Step-by-step instructions on how to perform the test.\n"
        prompt += "2. Further steps if needed.\n"
        prompt += "Expected Result: What should be observed if the functionality works as intended.\n\n"

    try:
        inputs = gpt_tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=1024)
        attention_mask = torch.ones(inputs['input_ids'].shape, dtype=torch.long)
        outputs = gpt_model.generate(inputs['input_ids'], attention_mask=attention_mask, max_length=500)
        response_text = gpt_tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Error generating instructions: {e}")
        response_text = "Error generating instructions."

    return response_text

@app.route('/api/describe', methods=['POST'])
def describe():
    if 'images' not in request.files:
        return jsonify({'error': 'No images uploaded'}), 400

    images = request.files.getlist('images')
    if not images:
        return jsonify({'error': 'No images uploaded'}), 400

    context = request.form.get('context', 'Default context for generating instructions')

    image_paths = []
    for image in images:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        image_paths.append(image_path)

    try:
        image_features = generate_image_features(image_paths)
        instructions = generate_test_instructions(context, image_features)
        return jsonify({'instructions': instructions})
    except Exception as e:
        error_message = str(e)
        print(f"Error in /api/describe: {error_message}")
        print(traceback.format_exc())
        return jsonify({'error': error_message}), 500
    finally:
        for path in image_paths:
            if os.path.exists(path):
                os.remove(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
