import requests

def download_pdf(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print("PDF saved successfully.")
    else:
        print("Failed to download PDF.")

# Example usage
pdf_url = 'http://127.0.0.1:5000/downloads/generated_pdf.pdf'  # Adjust to your actual Flask URL and endpoint
save_path = '/Downloads/generated_pdf.pdf'  # Change to your desired local path
download_pdf(pdf_url, save_path)
