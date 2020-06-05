import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
client_secrets_file = "client secret.json"
api_service_name = "youtube"
api_version = "v3"

def main(url):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    youtube = get_authenticated_service()
    request = youtube.search().list(
        part="snippet",
        maxResults=2,
        q= url
    )
    response = request.execute()
    a = response
    return a['items'][0]['id']['videoId']

def get_authenticated_service():
    if os.path.exists("CREDENTIALS_PICKLE_FILE"):
        with open("CREDENTIALS_PICKLE_FILE", 'rb') as f:
            credentials = pickle.load(f)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()
        with open("CREDENTIALS_PICKLE_FILE", 'wb') as f:
            pickle.dump(credentials, f)
    return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

if __name__ == '__main__':
    print('You only have to do this once so please follow the instructions')
    print('-'*120)
    video_title = input('Enter a random video title: ')
    print('-'*120)
    print('''Now follow the link displayed below and sign in with your google account. Now, agree to \neverything and copy and paste the authorization code you get below''')
    print('-'*120)
    main(video_title)
    
