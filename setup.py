#!/usr/bin/python
"""Store files as YouTube videos."""
from distutils.core import setup

setup_kwargs = {
    "name": "youtube-drive",
    "version": "0.0.1",
    "description": "Store files as YouTube videos",
    "author": "Le Wang",
    "author_email": "lewang.dev@gmail.com",
    "url": "https://github.com/lewangdev/youtube-drive",
    "packages": ["youtube_drive/"],
    "scripts": ["bin/youtube-drive"],
    "license": "Apache-2.0 license",
    "long_description": " ".join(__doc__.strip().splitlines()),
    "classifiers": [
        'Topic :: Internet :: WWW/HTTP',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: Apache-2.0 license',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
    ],
    "entry_points": {
        'console_scripts': [
            'youtube-drive = youtube_drive.main:main'
        ],
    },
    "install_requires": [
        'numpy',
        'opencv-python',
        'youtube-dl',
        'pillow',
        'git+https://github.com/tokland/youtube-upload.git'
    ]
}

setup(**setup_kwargs)
