from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re
import requests
import google.generativeai as genai
from flask_cors import CORS
import os
from bs4 import BeautifulSoup


genai.configure(api_key= os.getenv('GOOGLE_API_KEY'))

app = Flask(__name__)
CORS(app)

def get_youtube_transcription(video_link):
    # Extract video ID from the YouTube video link
    video_id_match = re.search(r"(?<=v=)[\w-]+", video_link)
    if video_id_match:
        video_id = video_id_match.group(0)
    else:
        return "Invalid YouTube video link. Please provide a valid link."

    try:
        # Fetch the transcript for the YouTube video
        transcription_response = YouTubeTranscriptApi.get_transcript(video_id)

        # Extracting only the text from the transcription response
        extracted_texts = [entry['text'] for entry in transcription_response]

        # Join the extracted texts into a single string
        full_text = ' '.join(extracted_texts)

        return full_text
    except Exception as e:
        return f"Error fetching transcription: {str(e)}"

def get_video_title(video_url):
    try:
        req = requests.get(video_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        title = soup.find('title').text
        return title
    except Exception as e:
        return str(e)

def get_gemini_response(input_text):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input_text)
        return response.text
    except Exception as e:
        return str(e)

input_prompt_template = """
Transcription Text:
{transcription_text}

Based on the provided transcription, create a comprehensive summary of the video content in a paragraph format:

"""

@app.route('/get_summary', methods=['POST'])
def process_youtube_link():
    if request.method == 'POST':
        data = request.get_json()
        youtube_link = data.get('youtube_link')
        if(youtube_link is None):
            return jsonify({'error': 'YouTube link not provided.'}), 400

        if youtube_link:
            transcription_text = get_youtube_transcription(youtube_link)
            input_prompt = input_prompt_template.format(transcription_text=transcription_text)
            summary = get_gemini_response(input_prompt)
            title = get_video_title(youtube_link)
            return jsonify({'title': title.rsplit(' ', 2)[0],'summary': summary})
        else:
            return jsonify({'error': 'YouTube link not provided.'}), 400
    else:
        return jsonify({'error': 'Method not allowed.'}), 405

if __name__ == '__main__':
    app.run(debug=True)
