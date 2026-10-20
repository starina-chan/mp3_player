import os
from glob import glob

from setuptools import find_packages, setup

package_name = "mp3_player"

setup(
    name=package_name,
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
        (os.path.join("share", package_name, "sounds"), glob("sounds/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="starina-chan",
    maintainer_email="154484150+starina-chan@users.noreply.github.com",
    description="ROS2 node that plays an MP3 file on a topic message.",
    license="Apache-2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "mp3_player_node = mp3_player.mp3_player_node:main",
        ],
    },
)
