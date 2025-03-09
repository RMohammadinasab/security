🖼️ WordPress Image Finder
🔍 A tool to find images in a WordPress site using different methods
This Python tool helps users find images stored in a WordPress site's upload directory. It supports multiple methods to retrieve images, making it useful for security testing, backup recovery, and web scraping.

📌 Features
✔ Directory Listing Check - Detects if directory listing is enabled and lists available images.
✔ WordPress API Check - Uses the wp-json/wp/v2/media API to fetch uploaded media files.
✔ Brute Force Detection - Attempts to find images by guessing common filenames.
✔ User-Selectable Methods - Allows users to choose a specific method or run all methods together.
✔ Easy-to-Use - Simple command-line interface for quick execution.

🛠️ Installation
This tool requires Python 3 and a few dependencies. Install them using:

```bash
pip install requests beautifulsoup4
```

🚀 How to Use
Run the script and enter a WordPress site URL when prompted:

```bash
python wordpress_image_finder.py
```

Then, choose a method to find images:

```bash
Select a method to find images:

1️: Directory Listing: Checks if the website allows listing all files in the upload folder.
2️: WordPress API: Uses the built-in API to list uploaded media files.
3️: Brute Force: Tries to guess image filenames by checking common patterns.
4️: Run all methods
```

Enter the desired option (1, 2, 3, or 4) and the tool will attempt to retrieve images.

📖 How It Works
1️: Directory Listing
Some WordPress sites allow directory listing, which exposes all files in /wp-content/uploads/.
This tool checks for this vulnerability and extracts image URLs.

2️: WordPress API
WordPress provides an API endpoint (/wp-json/wp/v2/media) that lists uploaded media files.
If enabled, this method retrieves all stored images from the API.

3️: Brute Force
If directory listing and API access are blocked, brute force is used.
The script tries common filenames like image1.jpg, image2.png, etc., and checks if they exist.

⚠️ Disclaimer
This tool is intended for ethical use only!
Use it only on websites you own or have permission to test. Unauthorized access to data may violate privacy laws.

💡 Example Output

```bash
[+] Checking WordPress API...
✅ Found images via WordPress API:
https://example.com/wp-content/uploads/2022/01/image1.jpg
https://example.com/wp-content/uploads/2022/01/image2.png

 Total 2 images found!
```