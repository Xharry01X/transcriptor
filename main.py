import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?P<id>[^\s?&]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group('id')
    
    parsed_url = urlparse(url)
    if parsed_url.netloc in ('youtube.com', 'www.youtube.com'):
        return parse_qs(parsed_url.query).get('v', [None])[0]
    elif parsed_url.netloc == 'youtu.be':
        return parsed_url.path.lstrip('/')
    
    return None

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def format_transcript(transcript):
    formatted_transcript = ""
    for entry in transcript:
        text = entry['text']
        formatted_transcript += f"{text} "
    return formatted_transcript.strip()

def main():
    while True:
        video_url = input("Please enter the YouTube video URL (or 'q' to quit): ")
        
        if video_url.lower() == 'q':
            print("Exiting the program.")
            break

        video_id = extract_video_id(video_url)
        
        if not video_id:
            print("Invalid YouTube URL. Could not extract video ID. Please try again.")
            continue
        
        transcript = get_youtube_transcript(video_id)
        
        if transcript:
            formatted_transcript = format_transcript(transcript)
            print("\nTranscript:")
            print(formatted_transcript)
            
            # Save to a file
            filename = f"{video_id}_transcript.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(formatted_transcript)
            print(f"\nTranscript saved to {filename}")
        
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()