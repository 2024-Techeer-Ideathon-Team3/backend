import requests

def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f'Image successfully downloaded: {save_path}')
    else:
        print('Failed to download image')

# 사용 예시
image_url = 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-CJsxlIahLVeHaYSR8r5AAn28/user-vWagej4QSFatB9vaiVjV4GUA/img-7WWFBe3c7C6MSNY2NLKXDHk8.png?st=2024-05-31T16%3A12%3A48Z&se=2024-05-31T18%3A12%3A48Z&sp=r&sv=2023-11-03&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-05-30T23%3A28%3A33Z&ske=2024-05-31T23%3A28%3A33Z&sks=b&skv=2023-11-03&sig=cad3HS9/h6Z1cmmS54x1PoEmbGCEsQMyTLmPebV2EG0%3D'
save_path = 'images/test.png'  # 예: 'downloaded_image.jpg'
download_image(image_url, save_path)
