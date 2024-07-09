import urllib.request
import pandas as pd
import shutil

timeout = 5


def get_images_by_category(url_path, save_path, error_path):
    error = []
    data = pd.read_csv(url_path, sep='\s+', header=None, names=['id', 'url'])

    for row in data.iterrows():
        id = row[1]['id']
        url = row[1]['url']

        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                with open(f'{save_path}\{id}.jpg', 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)

        except:
            error.append(id)

    with open(error_path, "w") as f:
        for id in error:
            f.write(f"{id}\n")


dress_save_path = r'C:\Users\CPS125\OneDrive\Documents\Dataset\FashionIQ\images'
dress_url_path = r'D:\Specialization\Project\GetFashionIQ\url\asin2url.dress.txt'
dress_error_path = r'D:\Specialization\Project\GetFashionIQ\error\dress_error.txt'
get_images_by_category(dress_url_path, dress_save_path, dress_error_path)


shirt_save_path = r'C:\Users\CPS125\OneDrive\Documents\Dataset\FashionIQ\images'
shirt_url_path = r'D:\Specialization\Project\GetFashionIQ\url\asin2url.shirt.txt'
shirt_error_path = r'D:\Specialization\Project\GetFashionIQ\error\shirt_error.txt'
get_images_by_category(shirt_url_path, shirt_save_path, shirt_error_path)


toptee_save_path = r'C:\Users\CPS125\OneDrive\Documents\Dataset\FashionIQ\images'
toptee_url_path = r'D:\Specialization\Project\GetFashionIQ\url\asin2url.toptee.txt'
toptee_error_path = r'D:\Specialization\Project\GetFashionIQ\error\toptee_error.txt'
get_images_by_category(toptee_url_path, toptee_save_path, toptee_error_path)