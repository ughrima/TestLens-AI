# import os
# import requests
# from flask import Flask, request, jsonify
# from werkzeug.utils import secure_filename
# from transformers import BlipProcessor, BlipForConditionalGeneration
# from PIL import Image
# from flask_cors import CORS
# import torch

# app = Flask(__name__)
# CORS(app)
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Initialize models
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# # Ensure the upload directory exists
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route('/')
# def home():
#     return "Welcome to the Testing Instruction Generator!"

# @app.route('/api/describe', methods=['POST'])
# def describe_testing_instructions():
#     context = request.form.get('context', '')
#     images = request.files.getlist('images')

#     if not images:
#         return jsonify({"error": "No images provided"}), 400

#     # Process images with BLIP for captions
#     image_captions = []
#     for image in images:
#         filename = secure_filename(image.filename)
#         image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         image.save(image_path)

#         # Process each image to get a description
#         img = Image.open(image_path).convert("RGB")
#         inputs = processor(images=img, return_tensors="pt").to(device)
#         caption = caption_model.generate(**inputs)
#         decoded_caption = processor.decode(caption[0], skip_special_tokens=True)
#         image_captions.append(f"{decoded_caption}")

#     # Use a local model or service (replace with a free model)
#     # For example, you can use Hugging Face's models (which have some free tier)
#     # or any GPT model available

#     prompt_text = f"Generate detailed test instructions based on these captions: {image_captions} and context: {context}. Mention a Description, Pre-conditions, Testing Steps, and Expected Results."
    
#     instructions = generate_instructions(prompt_text)  # Replace with your AI model logic

#     return jsonify({"instructions": instructions})

# def generate_instructions(prompt):
#     # Placeholder for AI model interaction (free Hugging Face models, for example)
#     return [
#         {
#             "Description": prompt,
#             "Pre-conditions": "Ensure the feature is loaded and accessible.",
#             "Testing Steps": [
#                 "Step 1: Open the app and navigate to the described feature.",
#                 "Step 2: Verify the feature's behavior based on the provided context and screenshot description.",
#                 "Step 3: Check for discrepancies or unexpected behaviors."
#             ],
#             "Expected Result": "The feature should work as described without any errors."
#         }
#     ]

# if __name__ == '__main__':
#     app.run(debug=True)

import torch
from transformers import BitsAndBytesConfig, pipeline
from PIL import Image
import gradio as gr
import re

# Initialize the model for image-to-text
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

model_id = "llava-hf/llava-1.5-7b-hf"
pipe = pipeline("image-to-text",
                model=model_id,
                model_kwargs={"quantization_config": quantization_config})

# Function to generate test instructions based on image and optional text input
def generate_instructions(image_path, input_text):
    # Load the image
    image = Image.open(image_path)

    # Prepare the prompt with both image and text (optional context)
    prompt_instructions = f"""
    Act as an expert in testing. Generate detailed test instructions based on the following image and additional context if any: {input_text}.
    Each test case should include:
    1. Description
    2. Pre-conditions
    3. Testing Steps
    4. Expected Results
    """

    prompt = f"USER: <image>\n{prompt_instructions}\nASSISTANT:"

    # Use the image-to-text pipeline
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # Extract response
    match = re.search(r'ASSISTANT:\s*(.*)', outputs[0]["generated_text"])
    if match:
        # Extract the text after "ASSISTANT:"
        extracted_text = match.group(1)
        return extracted_text
    else:
        return "No response generated."

# Gradio interface
iface = gr.Interface(
    fn=generate_instructions,
    inputs=[
        gr.Image(type="filepath", label="Upload Image"),
        gr.Textbox(label="Optional Context for Testing")
    ],
    outputs=gr.Textbox(label="Generated Test Instructions"),
    title="Image-Based Test Instruction Generator",
    description="Upload an image and optionally provide context to generate detailed test instructions."
)

# Launch the Gradio app
iface.launch(debug=True)

