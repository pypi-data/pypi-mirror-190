import logging
import os
import time


logger = logging.getLogger(__name__)

RESOURCES_ROOT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "resources")
)
logger.info(f'RESOURCES_ROOT_PATH = "{RESOURCES_ROOT_PATH}"')


def get_resource_path(sub_path):
    return os.path.join(
        RESOURCES_ROOT_PATH, sub_path.replace("{ts}", time.strftime("(%y%m%d.%H%M%S)"))
    )


def display_bulldog():
    import matplotlib.pyplot as plt

    filename = get_resource_path("woof-DALL-E.01.png")

    ax = plt.imshow(plt.imread(filename))
    ax.figure.set_facecolor("black")
    plt.axis("off")
