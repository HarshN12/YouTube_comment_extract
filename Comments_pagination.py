import os
import csv
import googleapiclient.discovery


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAhiEaB9GNcqxsaedeS-NCL5na2FkFrFSM"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId="yeyYVmsywWI",
        maxResults=2000,  # Adjust the maxResults according to your requirement
    )
    all_comments = []

    while request:
        response = request.execute()
        all_comments.extend(response['items'])
        request = youtube.commentThreads().list_next(request, response)

    # Writing the response to a CSV file
    with open('output3.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        # Writing the headers
        writer.writerow(['Comment', 'Author', 'Published At'])
        # Writing each comment data
        for item in all_comments:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            published_at = item['snippet']['topLevelComment']['snippet']['publishedAt']
            writer.writerow([comment, author, published_at])


if __name__ == "__main__":
    main()