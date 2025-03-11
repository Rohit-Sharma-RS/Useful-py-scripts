import subprocess
import os

def download_torrent(torrent_source):
    # Check if the input is a file path or a magnet link
    if os.path.exists(torrent_source) and torrent_source.endswith('.torrent'):
        # If it's a torrent file
        cmd = ['webtorrent', 'download', torrent_source, '--out', './downloads']
    else:
        # Assume it's a magnet link
        cmd = ['webtorrent', 'download', torrent_source, '--out', './downloads']
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in process.stdout:
        print(line.decode(), end='')

# Ask user for input
torrent_source = input('Enter magnet link or path to .torrent file: ')
download_torrent(torrent_source)
