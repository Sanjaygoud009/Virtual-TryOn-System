import requests

# Paths for the images (update with correct paths)
avatar_image_path = "C:/Users/sanjay/Pictures/1.ICFAI/Sem-6/Project/my project/virtual_tryon/data/user.jpg"
clothing_image_path = "C:/Users/sanjay/Pictures/1.ICFAI/Sem-6/Project/my project/virtual_tryon/data/cloth_0.jpg"

# URL of the API endpoint
url = "https://try-on-diffusion.p.rapidapi.com/try-on-file"  # Adjust the endpoint if needed

# Prepare the files to be uploaded
files = {
    "clothing_image": ("cloth_0.jpg", open(clothing_image_path, "rb"), "image/jpeg"),
    "avatar_image": ("user.jpg", open(avatar_image_path, "rb"), "image/jpeg")
}

# Headers with your RapidAPI key
headers = {
    "X-RapidAPI-Key": "b9be7fafbfmsh8c2cbb168e34beep1acc3djsn9337442fc19b",
    "X-RapidAPI-Host": "try-on-diffusion.p.rapidapi.com"
}

# Send the request to the API
print("Sending request to Try-On API...")
response = requests.post(url, files=files, headers=headers)

# Check if the response is successful
print(f"Response status code: {response.status_code}")

# Check if the response is in binary format (image)
if response.status_code == 200:
    print("Received binary data (likely an image). Saving it to file.")
    
    # Save the image to a file (the image is in binary format)
    try:
        with open("C:/Users/sanjay/Pictures/1.ICFAI/Sem-6/Project/my project/virtual_tryon/static/uploads/tryon_result.jpg", "wb") as f:
            f.write(response.content)  # Write the binary data to the file
        print("Image saved successfully as 'tryon_result.jpg'")
    except Exception as e:
        print(f"Failed to save image: {e}")
else:
    print("Failed with status code:", response.status_code)
