from os import listdir

images_folder_path = "default_hangman_images"
image_paths = listdir(images_folder_path)


def get_image_path(lives: int) -> str:
    return images_folder_path + "/" + image_paths[8 - lives]
