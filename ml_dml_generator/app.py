
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
from docx import Document
from transformers import T5Tokenizer, T5ForConditionalGeneration

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
tokenizer = T5Tokenizer.from_pretrained("./model")
model = T5ForConditionalGeneration.from_pretrained("./model")

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

@app.route('/', methods=['GET', 'POST'])
def index():
    sql_output = ""
    if request.method == 'POST':
        f = request.files['docx_file']
        filename = secure_filename(f.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        f.save(filepath)
        text = extract_text_from_docx(filepath)
        input_ids = tokenizer("Generate SQL: " + text, return_tensors="pt").input_ids
        output = model.generate(input_ids, max_length=512)
        sql_output = tokenizer.decode(output[0], skip_special_tokens=True)
        with open("data.sql", "w", encoding='utf-8') as f:
            f.write(sql_output)
        return render_template("index.html", sql=sql_output)
    return render_template("index.html", sql=None)
