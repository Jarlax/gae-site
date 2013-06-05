import re

name_pattern = '[_a-z0-9]+'  # Name pattern
image_pattern = '%s\.(jpe?g|png)' % name_pattern  # Image name pattern


def get_img_type(img_name):
    img_type = re.match(image_pattern, img_name).group(1)
    if img_type == 'jpg':
        img_type = 'jpeg'
    return img_type