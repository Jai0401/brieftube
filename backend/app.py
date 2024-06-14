from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re
import requests
import google.generativeai as genai
from flask_cors import CORS
import youtube_dl


genai.configure(api_key="AIzaSyBdcA82rIdIhyfvb9yxN1qz1-6xtC5TfH4")

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
        ydl_opts = {
            'verbose': True,  # Enable verbose output
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get('title')
            return video_title
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

Based on the provided transcription, create a comprehensive summary of the video content. The summary should follow the structure below and capture all the essential information without omitting any critical points:

1. **Title**: Provide a brief title for the summary.
2. **Introduction**: Summarize the main introduction points made by the speaker.
3. **Key Points**:
    - **Point 1**: Describe the first key point or section of the video.
    - **Point 2**: Describe the second key point or section of the video.
    - **Point 3**: Describe the third key point or section of the video.
    - (Add more points as necessary)
4. **Examples**: Provide any examples the speaker used to illustrate their points.
5. **Benefits and Impact**: Summarize the benefits and impact discussed in the video.
6. **Conclusion**: Provide the concluding remarks and the main takeaway from the video.

Ensure each section is detailed and clearly written.

Response format:
**Title**: [Title]
**Introduction**: [Introduction]
**Key Points**:
    - **Point 1**: [Details of Point 1]
    - **Point 2**: [Details of Point 2]
    - **Point 3**: [Details of Point 3]
    - (Add more points as necessary)
**Examples**: [Examples]
**Benefits and Impact**: [Benefits and Impact]
**Conclusion**: [Conclusion]

"""

@app.route('/get_summary', methods=['POST'])
def process_youtube_link():
    if request.method == 'POST':
        data = request.get_json()
        youtube_link = data.get('youtube_link')

        if youtube_link:
            transcription_text = get_youtube_transcription(youtube_link)
            input_prompt = input_prompt_template.format(transcription_text=transcription_text)
            summary = get_gemini_response(input_prompt)
            # title = get_video_title(youtube_link)
            return jsonify({'video_summary': summary})
        else:
            return jsonify({'error': 'YouTube link not provided.'}), 400
    else:
        return jsonify({'error': 'Method not allowed.'}), 405

if __name__ == '__main__':
    app.run(debug=True)
