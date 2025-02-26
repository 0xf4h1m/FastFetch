
# FastFetch Download Manager

FastFetch Downloader is a high-speed, multi-threaded file downloader for Linux and Windows, designed to maximize download speed using up to 16 threads. It supports resumable downloads, progress tracking, and automatic output folder handling.

## 🚀 Features
- Multi-threaded downloading (default: 16 threads)
- Resumable downloads
- Real-time speed tracking with `tqdm`
- Automatic output directory (`~/Downloads/FastFetch_Downloader/`)
- Custom output filename/location
- User-friendly CLI interface
- Developed and maintained by **Yousuf Abdullah Fahim** (0xf4h1m)


## 📥 Installation

### Prerequisites
Make sure you have Python installed. You can check by running:
```bash
python --version
```

### Install dependencies
```bash
pip install requests tqdm
```

## 🔧 Usage

### Basic Download
```bash
python fastfetch_downloader.py <URL>
```
Example:
```bash
python fastfetch_downloader.py "https://example.com/file.zip"
```
This will download `file.zip` to `~/Downloads/FastFetch_Downloader/`.

### Custom Output Location
```bash
python fastfetch_downloader.py <URL> -o /path/to/save/file.zip
```

### Specify Number of Threads
```bash
python fastfetch_downloader.py <URL> -t 8
```
(Default is 16 threads)

### Resume Download
```bash
python fastfetch_downloader.py <URL> -r
```

## 📌 Use Cases
- **Fast file downloads** (alternative to IDM, Wget, Curl)
- **Resuming large downloads** after interruption
- **Automating downloads** in scripts

## 🔗 How to Collect Download URLs
- **Right-click on a download link** in a browser and select `Copy Link Address`
- Use browser developer tools (`F12` > Network tab > Find request URL)
- Check source websites for direct file links

## ⚡ Contributing
Feel free to submit issues or improvements via GitHub!

## 📜 License
MIT License.
