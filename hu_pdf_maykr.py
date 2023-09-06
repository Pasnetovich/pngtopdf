import requests
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def input_url_and_num_images():
    full_url = input("Enter the URL of the first image: ")
    base_url = full_url.rsplit("-", 1)[0] + "-"
    num_images = int(input("Enter the number of pages to download: "))
    return base_url, num_images

def create_pdf_from_images(image_dir, output_pdf):
    image_paths = [os.path.join(image_dir, filename) for filename in os.listdir(image_dir) if filename.endswith(".png")]
    image_paths.sort()

    c = canvas.Canvas(output_pdf, pagesize=letter)
    for image_path in image_paths:
        img = Image.open(image_path)
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height
        max_width = letter[0] - 36
        max_height = letter[1] - 36
        if img_width > max_width or img_height > max_height:
            if img_width / max_width > img_height / max_height:
                img_width = max_width
                img_height = max_width / aspect_ratio
            else:
                img_height = max_height
                img_width = max_height * aspect_ratio
        x_offset = (letter[0] - img_width) / 2
        y_offset = (letter[1] - img_height) / 2
        c.drawImage(image_path, x_offset, y_offset, width=img_width, height=img_height)
        c.showPage()
    c.save()
    print(f"PDF file '{output_pdf}' created successfully.")

def download_images(base_url, num_images, download_dir):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Directory '{download_dir}' created.")

    for i in range(1, num_images + 1):
        image_url = f"{base_url}{i:06d}.png"
        response = requests.get(image_url)

        if response.status_code == 200:
            with open(os.path.join(download_dir, f"{i:06d}.png"), "wb") as file:
                file.write(response.content)
            print(f"Downloaded {i}/{num_images} - {image_url}")
        else:
            print(f"Failed to download {i}/{num_images} - {image_url}")

    print("All images downloaded successfully.")

def main():
    base_url, num_images = input_url_and_num_images()
    download_dir = input("Enter the directory path to store downloaded images: ")

    if os.path.exists(download_dir):
        create_pdf_option = input(f"The directory '{download_dir}' already exists. Do you want to create a PDF from the images in this directory? (yes/no): ").strip().lower()

        if create_pdf_option == "yes":
            pdf_file_name = input("Enter the PDF file name (e.g., output.pdf): ")
            output_pdf = os.path.join(download_dir, pdf_file_name)
            create_pdf_from_images(download_dir, output_pdf)
            print(f"PDF '{pdf_file_name}' created successfully in '{download_dir}'.")
        else:
            print("No PDF created.")
    else:
        download_images(base_url, num_images, download_dir)
        create_pdf_option = input("Do you want to create a PDF from the downloaded images? (yes/no): ").strip().lower()

        if create_pdf_option == "yes":
            pdf_file_name = input("Enter the PDF file name (e.g., output.pdf): ")
            output_pdf = os.path.join(download_dir, pdf_file_name)
            create_pdf_from_images(download_dir, output_pdf)
            print(f"PDF '{pdf_file_name}' created successfully in '{download_dir}'.")
        else:
            print("No PDF created.")

if __name__ == "__main__":
    main()
