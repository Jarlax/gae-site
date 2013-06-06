import re

name_pattern = '[_a-z0-9]+'  # Name pattern
image_pattern = '%s\.(jpe?g|png)' % name_pattern  # Image name pattern


def get_img_type(img_id):
    img_type = re.match(image_pattern, str(img_id)).group(1)
    if img_type == 'jpg':
        img_type = 'jpeg'
    return img_type


def get_id_by_name(page_name, img_ext):
    page_id = str(page_name).replace(' ', '_').lower()
    if img_ext:
        page_id += '.%s' % img_ext
    return page_id