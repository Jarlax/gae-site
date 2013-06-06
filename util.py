import re

name_pattern = '[_a-z0-9]+'  # Name pattern


def get_img_type(img_id):
    img_type = re.match('.*\.(jpe?g|png)', str(img_id)).group(1)
    if img_type == 'jpg':
        img_type = 'jpeg'
    return img_type


def get_id_by_name(page_name):
    return str(page_name).strip().replace(' ', '_').lower()