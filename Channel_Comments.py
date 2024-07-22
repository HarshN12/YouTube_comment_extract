import csv
import os
import googleapiclient.discovery

# Define a function to fetch and process the comment threads
def fetch_comment_threads():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAhiEaB9GNcqxsaedeS-NCL5na2FkFrFSM"  # Replace with your actual developer key

    # Build the YouTube API service
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    # Make a request to fetch comment threads
    request = youtube.commentThreads().list(
        part="snippet,replies",
        channelId="3gJyU7Lvb9CP7SPN"
    )
    response = request.execute()

    # Write the fetched comment threads to a CSV file
    with open('comment_threads.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Author', 'Comment'])

        # Process the fetched comment threads
        if 'items' in response:
            for item in response['items']:
                # Extract and write relevant information from each comment thread
                snippet = item['snippet']['topLevelComment']['snippet']
                author = snippet['authorDisplayName']
                text = snippet['textDisplay']
                writer.writerow([author, text])
        else:
            writer.writerow(['No comments found', ''])

if __name__ == "__main__":
    fetch_comment_threads()
