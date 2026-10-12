from setuptools import setup, find_packages

setup(
    name="ytdlp-pot-provider",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "yt-dlp",
    ],
    entry_points={
        "yt_dlp.plugins": [
            "yawstar = yt_dlp_plugins",
        ],
    },
)