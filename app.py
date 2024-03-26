from flask import Flask, render_template, request, redirect, url_for
import os
from StudySync import extract_info_from_file, create_audio_file, ask_questions_about_theme

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file_type = request.form['file_type']
        file_path = request.form['file_path']
        
        text = extract_info_from_file(file_path)

        if text:
            create_audio = request.form.get('create_audio', False)
            if create_audio:
                audio_output_path = f'static/audio/audio_output.mp3'
                create_audio_file(text, audio_output_path)
                audio_url = url_for('static', filename=f'audio/audio_output.mp3')
            else:
                audio_url = None

            if file_type == 'topic':
                theme = request.form['theme']
                para = request.form['paragraph']
                ask_questions_about_theme(theme, para)
            else:
                theme = None
                para = None

            return render_template('result.html', text=text, theme=theme, para=para, audio_url=audio_url)
        else:
            return render_template('index.html', error_message="Failed to extract text. Please check the file path.")
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)