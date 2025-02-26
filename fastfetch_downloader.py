import os
import requests
import threading
import argparse
import time
from tqdm import tqdm
from urllib.parse import urlparse

def print_banner():
    banner = r"""

    ______           __     ______     __       __  
   / ____/___ ______/ /_   / ____/__  / /______/ /_ 
  / /_  / __ `/ ___/ __/  / /_  / _ \/ __/ ___/ __ \
 / __/ / /_/ (__  ) /_   / __/ /  __/ /_/ /__/ / / /
/_/    \__,_/____/\__/  /_/    \___/\__/\___/_/ /_/ 
                                                    

    FastFetch Download Manager 🚀 v1.0  
    High-Speed Multi-Threaded Downloader 
    Author: Yousuf Abdullah Fahim (0xf4h1m) 
    """
    print(banner)

class FastFetchDownloader:
    def __init__(self, url, output_dir=None, filename=None, num_threads=16, resume=False):
        self.url = url
        self.num_threads = num_threads
        self.resume = resume
        self.lock = threading.Lock()
        self.downloaded = [0] * num_threads  # Track downloaded bytes per thread

        # Default download directory
        self.default_download_dir = os.path.expanduser("~/Downloads/FastFetch_Downloader")
        if output_dir:
            self.download_dir = os.path.abspath(output_dir)
        else:
            self.download_dir = self.default_download_dir

        # Ensure directory exists
        os.makedirs(self.download_dir, exist_ok=True)

        # Determine filename
        if filename:
            self.filename = filename
        else:
            self.filename = os.path.basename(urlparse(url).path) or "downloaded_file"

        self.filepath = os.path.join(self.download_dir, self.filename)
        self.chunk_size = None
        self.file_size = None

    def get_file_size(self):
        """Fetch file size from server."""
        response = requests.head(self.url)
        if response.status_code == 200 and "Content-Length" in response.headers:
            self.file_size = int(response.headers["Content-Length"])
            self.chunk_size = self.file_size // self.num_threads
        else:
            raise Exception("Unable to retrieve file size")

    def download_chunk(self, thread_id, start, end, progress_bar):
        """Download a chunk of the file."""
        headers = {"Range": f"bytes={start}-{end}"}
        part_file = f"{self.filepath}.part{thread_id}"

        # Check for resumption
        downloaded_size = os.path.getsize(part_file) if self.resume and os.path.exists(part_file) else 0
        headers["Range"] = f"bytes={start + downloaded_size}-{end}"

        response = requests.get(self.url, headers=headers, stream=True)
        with open(part_file, "ab" if self.resume else "wb") as f:
            for chunk in response.iter_content(1024):
                if chunk:
                    f.write(chunk)
                    with self.lock:
                        self.downloaded[thread_id] += len(chunk)
                        progress_bar.update(len(chunk))

    def merge_chunks(self):
        """Merge all downloaded chunks into the final file."""
        with open(self.filepath, "wb") as final_file:
            for i in range(self.num_threads):
                part_file = f"{self.filepath}.part{i}"
                with open(part_file, "rb") as pf:
                    final_file.write(pf.read())
                os.remove(part_file)

    def show_speed(self, progress_bar):
        """Show download speed in real-time."""
        prev_downloaded = 0
        while progress_bar.n < self.file_size:
            time.sleep(1)
            downloaded_now = sum(self.downloaded)
            speed = (downloaded_now - prev_downloaded) / 1024 / 1024  # MB/s
            prev_downloaded = downloaded_now
            progress_bar.set_description(f"Speed: {speed:.2f} MB/s")

    def start_download(self):
        """Main download process."""
        print(f"\n📂 Downloading to: {self.filepath}\n")
        self.get_file_size()

        # Initialize progress bar
        progress_bar = tqdm(total=self.file_size, unit="B", unit_scale=True, desc="Downloading")

        # Start speed tracker thread
        speed_thread = threading.Thread(target=self.show_speed, args=(progress_bar,))
        speed_thread.daemon = True
        speed_thread.start()

        # Start downloading in multiple threads
        threads = []
        for i in range(self.num_threads):
            start = i * self.chunk_size
            end = (start + self.chunk_size - 1) if i < self.num_threads - 1 else self.file_size
            thread = threading.Thread(target=self.download_chunk, args=(i, start, end, progress_bar))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        progress_bar.close()
        self.merge_chunks()
        print("✅ Download completed successfully!")

if __name__ == "__main__":
    print_banner()
    parser = argparse.ArgumentParser(description="FastFetch Download Manager 🚀")
    parser.add_argument("url", help="File URL to download")
    parser.add_argument("-o", "--output", help="Output directory (default: ~/Downloads/FastFetch_Downloader)")
    parser.add_argument("-f", "--filename", help="Output file name (default: Original file name from URL)")
    parser.add_argument("-t", "--threads", type=int, default=16, help="Number of threads (default: 16)")
    parser.add_argument("-r", "--resume", action="store_true", help="Enable resumable downloads")

    args = parser.parse_args()

    downloader = FastFetchDownloader(args.url, args.output, args.filename, args.threads, args.resume)
    downloader.start_download()
