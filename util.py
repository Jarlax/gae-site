import re

name_pattern = '[_a-z0-9]+'  # Name pattern
image_pattern = '%s\.(jpe?g|png)' % name_pattern # Image name pattern


def get_img_type(name):
    type = re.match(image_pattern, name).group(1)
    if type == 'jpg':
        type = 'jpeg'
    return type