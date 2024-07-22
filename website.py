from flask import Flask, request, send_file, render_template_string
import os
import csv
import googleapiclient.discovery


#The line of code app = Flask(__name__, static_url_path='/static') is creating an instance of the Flask application with a specified path for serving static files.
app = Flask(__name__, static_url_path='/static')

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

DEVELOPER_KEY = "AIzaSyAhiEaB9GNcqxsaedeS-NCL5na2FkFrFSM"


#it defines the route for the root location for the web application
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YouTube Comments Downloader</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    </head>
    <body>
        <div class="container">
            <h1>YouTube Comments Downloader</h1>
            <form action="/download" method="get">
                <label for="videoId">Enter YouTube Video ID:</label>
                <input type="text" id="videoId" name="videoId" required>
                <button type="submit">Download Comments</button>
            </form>
        </div>
    </body>
    </html>
    ''')


#this code defines the route for /download for the web application
@app.route('/download')
def download_comments():
    video_id = request.args.get('videoId')   #this part of code access the video_id that was entered in the input box
    if not video_id:
        return "Error: No videoId provided. Please specify a videoId."

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=DEVELOPER_KEY)
    request_youtube = youtube.commentThreads().list(part="snippet,replies", videoId=video_id, maxResults=100)
    all_comments = []

    while request_youtube:
        response = request_youtube.execute()     #we are executing the request and we are getting the response
        all_comments.extend(response['items'])    #we are dding repsonse items in all_comments array
        request_youtube = youtube.commentThreads().list_next(request_youtube, response)  #this we are doing for accessing the next pa=ge of comments

    filename = f"{video_id}_comments.csv"
    filepath = os.path.join(os.getcwd(), filename)   #generate a file name and determine the full file path for saving comments as a CSV file in the current working directory.

    with open(filepath, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)      #Creates a CSV writer object that will be used to write data to the file.
        writer.writerow(['Comment', 'Author', 'Published At'])   #writer.writerow([...]): Writes a single row to the CSV file. These are the column headers written
        for item in all_comments:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            published_at = item['snippet']['topLevelComment']['snippet']['publishedAt']
            writer.writerow([comment, author, published_at])      #Writes a row to the CSV file with the comment text, author name, and published date for each comment.

    return send_file(filepath, as_attachment=True, download_name=filename)

if __name__ == "__main__":
    app.run(debug=True)
