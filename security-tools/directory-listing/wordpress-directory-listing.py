import requests
from bs4 import BeautifulSoup

def check_directory_listing(url):
    """Check if directory listing is enabled and list available images."""
    print("\n[+] Checking Directory Listing...")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        images = [url + a["href"] for a in soup.find_all("a") if a["href"].endswith((".jpg", ".png", ".jpeg", ".gif", ".webp"))]
        if images:
            print("\n✅ Found images via Directory Listing:")
            for img in images:
                print(img)
            return images
    return []

def check_wordpress_api(site_url):
    """Check if WordPress API (wp-json/wp/v2/media) is accessible and list images."""
    print("\n[+] Checking WordPress API...")
    api_url = site_url.rstrip("/") + "/wp-json/wp/v2/media"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        images = [item['source_url'] for item in data if 'source_url' in item]
        if images:
            print("\n✅ Found images via WordPress API:")
            for img in images:
                print(img)
            return images
    return []

def brute_force_images(base_url):
    """Attempt to find images by guessing common filenames."""
    print("\n[+] Trying Brute Force...")
    extensions = ["jpg", "png", "jpeg", "gif", "webp"]
    found_images = []
    for i in range(1, 100):
        for ext in extensions:
            img_url = f"{base_url}image{i}.{ext}"
            response = requests.head(img_url)
            if response.status_code == 200:
                found_images.append(img_url)
                print("✅ Found:", img_url)
    return found_images

def main():
    # Get user input
    site_url = input("Enter the WordPress site URL (e.g., https://ime.ir): ").strip()
    upload_url = site_url.rstrip("/") + "/wp-content/uploads/"

    # Explain each method to the user
    print("\nSelect a method to find images:\n")
    print("1️1 Directory Listing: Checks if the website allows listing all files in the upload folder.")
    print("2️ WordPress API: Uses the built-in API to list uploaded media files.")
    print("3️ Brute Force: Tries to guess image filenames by checking common patterns.")
    print("4️ Run all methods")

    # Get user's choice
    choice = input("\nEnter your choice (1/2/3/4): ").strip()

    found_images = []

    if choice == "1":
        found_images += check_directory_listing(upload_url)
    elif choice == "2":
        found_images += check_wordpress_api(site_url)
    elif choice == "3":
        found_images += brute_force_images(upload_url)
    elif choice == "4":
        found_images += check_directory_listing(upload_url)
        found_images += check_wordpress_api(site_url)
        found_images += brute_force_images(upload_url)
    else:
        print("\n Invalid choice. Please enter 1, 2, 3, or 4.")
        return

    # Display results
    if not found_images:
        print("\n No images found using the selected method(s).")
    else:
        print(f"\n Total {len(found_images)} images found!")

if __name__ == "__main__":
    main()
