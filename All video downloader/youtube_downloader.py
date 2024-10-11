import yt_dlp

def download_video():
    while True:
        link = input("Enter the video link (or type 'exit' to quit): ")
        if link.lower() == 'exit':
            print("Exiting the downloader.")
            break
        try:
            yt_dlp.YoutubeDL().download([link])
            print("Download completed successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_video()
