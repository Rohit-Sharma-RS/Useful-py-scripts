import libtorrent as lt
import time

def download_torrent(torrent_link):
    ses = lt.session()
    params = {
        'save_path': './downloads/',
        'storage_mode': lt.storage_mode_t(2),
    }
    handle = lt.add_magnet_uri(ses, torrent_link, params)
    ses.start_dht()

    print("Downloading...")
    while not handle.has_metadata():
        time.sleep(1)
    print("Metadata acquired, starting download...")

    while handle.status().state != lt.torrent_status.seeding:
        s = handle.status()
        print(f'Downloading: {s.progress * 100:.2f}% complete (down: {s.download_rate / 1000:.2f} kB/s up: {s.upload_rate / 1000:.2f} kB/s peers: {s.num_peers})')
        time.sleep(5)

    print("Download complete!")


torrent_link = input("Enter the torrent link: ")
download_torrent(torrent_link)
