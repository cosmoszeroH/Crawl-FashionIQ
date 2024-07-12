import pandas as pd
import json
import os


def extract_captions(error_id, dress_type, cap_dir, save_extracted_dir, save_captions_dir):
    for set_type in ['train', 'test', 'val']:
        file_name = f'cap.{dress_type}.{set_type}.json'
        captions = pd.read_json(f'{cap_dir}\\{file_name}')
        extracted = pd.DataFrame(columns=captions.columns)

        if set_type == 'test':
            for index, cap in captions.iterrows():
                if cap.loc['candidate'] in error_id:
                    extracted = pd.concat([extracted, cap.to_frame().T], ignore_index=True)
                    captions = captions[captions.index != index]
        else:
            for index, cap in captions.iterrows():
                if (cap.loc['candidate'] in error_id) or (cap.loc['target'] in error_id):
                    extracted = pd.concat([extracted, cap.to_frame().T], ignore_index=True)
                    captions = captions[captions.index != index]

        extracted = extracted.to_dict(orient='records')
        with open(f'{save_extracted_dir}\\{file_name}', 'w') as f:
            json.dump(extracted, f, indent=4)

        captions = captions.to_dict(orient='records')
        with open(f'{save_captions_dir}\\{file_name}', 'w') as f:
            json.dump(captions, f, indent=4)


def drop_redundant_caption(dress_type, cap_dir, image_dir):
    for set_type in ['train', 'test', 'val']:
        file_path = f'{cap_dir}\\cap.{dress_type}.{set_type}.json'
        captions = pd.read_json(file_path)

        if set_type == 'test':
            for index, cap in captions.iterrows():
                id = cap['candidate']
                image_path = os.path.join(image_dir, f'{id}.jpg')
                if not os.path.exists(image_path):
                    captions = captions[captions.index != index]
        else:
            for index, cap in captions.iterrows():
                id = cap['candidate']
                image_path = os.path.join(image_dir, f'{id}.jpg')
                if not os.path.exists(image_path):
                    captions = captions[captions.index != index]
                    continue
                image_path = os.path.join(image_dir, f'{id}.jpg')
                if not os.path.exists(image_path):
                    captions = captions[captions.index != index]

        captions = captions.to_dict(orient='records')
        with open(file_path, 'w') as f:
            json.dump(captions, f, indent=4)


def modify_caption_files(error_id_path, cap_dir, save_extracted_dir, save_captions_dir, image_dir):
    for dress_type in ['dress', 'shirt', 'toptee']:
        drop_redundant_caption(dress_type, cap_dir, image_dir)

        error_id_file = f'{dress_type}_error.txt'
        with open(f'{error_id_path}\\{error_id_file}', 'r') as f:
            error_id = f.read().split()
            
        extract_captions(error_id, dress_type, cap_dir, save_extracted_dir, save_captions_dir)


def extract_splits(error_id, dress_type, split_dir, save_extracted_dir, save_splits_dir):
    for set_type in ['train', 'test', 'val']:
        file_name = f'split.{dress_type}.{set_type}.json'
        with open(f'{split_dir}\\{file_name}') as f:
            splits = json.load(f)
        extracted = []

        for s in splits:
            if s in error_id:
                extracted.append(s)
                splits.remove(s)

        with open(f'{save_extracted_dir}\\{file_name}', 'w') as f:
            json.dump(extracted, f)
        with open(f'{save_splits_dir}\\{file_name}', 'w') as f:
            json.dump(splits, f)


def drop_redundant_split(dress_type, split_path, image_dir):
    for set_type in ['train', 'test', 'val']:
        file_path = f'{split_path}\\split.{dress_type}.{set_type}.json'
        with open(f'{file_path}', 'r') as f:
            splits = json.load(f)
        
        for s in splits:
            image_path = os.path.join(image_dir, f'{s}.jpg')
            if not os.path.exists(image_path):
                splits.remove(s)

        with open(file_path, 'w') as f:
            json.dump(splits, f)


def modify_split_files(error_id_path, split_path, save_extracted_dir, save_splits_dir, image_dir):
    for dress_type in ['dress', 'shirt', 'toptee']:
        drop_redundant_split(dress_type, split_path, image_dir)

        error_id_file = f'{dress_type}_error.txt'
        with open(f'{error_id_path}\\{error_id_file}', 'r') as f:
            error_id = f.read().split()

        extract_splits(error_id, dress_type, split_path, save_extracted_dir, save_splits_dir)


error_id_path = r'.\error'
image_dir = r'.\fashionIQ_dataset\images'

cap_dir = r'.\fashionIQ_dataset\previous_captions'
save_extracted_dir = r'.\extracted_cap'
save_captions_dir = r'.\fashionIQ_dataset\captions'
modify_caption_files(error_id_path, cap_dir, save_extracted_dir, save_captions_dir, image_dir)

split_dir = r'.\fashionIQ_dataset\previous_image_splits'
save_extracted_dir = r'.\extracted_split'
save_split_dir = r'.\fashionIQ_dataset\image_splits'
modify_split_files(error_id_path, split_dir, save_extracted_dir, save_split_dir, image_dir)


