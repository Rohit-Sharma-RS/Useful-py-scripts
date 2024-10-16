import subprocess

def download_torrent(magnet_link):
    process = subprocess.Popen(['webtorrent', 'download', magnet_link, '--out', './downloads'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in process.stdout:
        print(line.decode(), end='')

magnet_link = input('Enter magnet link: ')
download_torrent(magnet_link)
