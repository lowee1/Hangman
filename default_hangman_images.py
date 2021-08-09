from os import listdir

image_paths = listdir("default_hangman_images")


def get_image(lives: int) -> str:
    return image_paths[lives]
