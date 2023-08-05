# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spotdl_romanized_lyrics',
 'spotdl_romanized_lyrics.console',
 'spotdl_romanized_lyrics.download',
 'spotdl_romanized_lyrics.providers',
 'spotdl_romanized_lyrics.providers.audio',
 'spotdl_romanized_lyrics.providers.lyrics',
 'spotdl_romanized_lyrics.types',
 'spotdl_romanized_lyrics.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'fastapi!=0.89.0',
 'mutagen>=1.46.0,<2.0.0',
 'platformdirs>=2.6.2,<3.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pykakasi>=2.2.1,<3.0.0',
 'python-slugify>=7.0.0,<8.0.0',
 'pytube>=12.1.2,<13.0.0',
 'rapidfuzz>=2.13.7,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=13.0.1,<14.0.0',
 'spotipy>=2.22.0,<3.0.0',
 'syncedlyrics>=0.2.1,<0.3.0',
 'uvicorn>=0.20.0,<0.21.0',
 'yt-dlp>=2023.1.6,<2024.0.0']

extras_require = \
{':python_version < "3.8"': ['ytmusicapi>=0.22.0,<0.23.0'],
 ':python_version >= "3.8"': ['ytmusicapi>=0.24.0,<0.25.0']}

entry_points = \
{'console_scripts': ['spotdl_romanized_lyrics = spotdl_romanized_lyrics:console_entry_point']}

setup_kwargs = {
    'name': 'spotdl_romanized_lyrics',
    'version': '0.0.1',
    'description': 'Download your Spotify playlists and songs along with album art and metadata',
    'long_description': '<!--- mdformat-toc start --slug=github --->\n\n<!---\n!!! IF EDITING THE README, ENSURE TO COPY THE WHOLE FILE TO index.md in `/docs/`\n--->\n\n<div align="center">\n\n# spotdl_romanized_lyrics v4\n\nDownload your Spotify playlists and songs along with album art and metadata\n\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?style=flat-square&color=44CC11)](https://github.com/spotdl_romanized_lyrics/spotify-downloader/blob/master/LICENSE)\n[![PyPI version](https://img.shields.io/pypi/pyversions/spotdl_romanized_lyrics?color=%2344CC11&style=flat-square)](https://pypi.org/project/spotdl_romanized_lyrics/)\n![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/spotdl_romanized_lyrics/spotify-downloader/latest?color=44CC11&style=flat-square)\n[![PyPi downloads](https://img.shields.io/pypi/dw/spotdl_romanized_lyrics?label=downloads@pypi&color=344CC11&style=flat-square)](https://pypi.org/project/spotdl_romanized_lyrics/)\n![Contributors](https://img.shields.io/github/contributors/spotdl_romanized_lyrics/spotify-downloader?style=flat-square)\n[![Discord](https://img.shields.io/discord/771628785447337985?label=discord&logo=discord&style=flat-square)](https://discord.gg/xCa23pwJWY)\n\n</div>\n\n> A new and improved version of spotdl_romanized_lyrics: still the fastest, easiest and most accurate\n> command-line music downloader\n\n______________________________________________________________________\n\n**[Read the documentation on ReadTheDocs!](http://spotdl_romanized_lyrics.rtfd.io/)**\n\n______________________________________________________________________\n\n## Prerequisites\n\n- [Visual C++ 2019 redistributable](https://docs.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022)\n  **(on Windows)**\n- Python 3.7 or above (added to PATH)\n\n> **_YouTube Music must be available in your country for spotdl_romanized_lyrics to work. This is because we use\n> YouTube Music to filter search results. You can check if YouTube Music is available in your\n> country, by visiting [YouTube Music](https://music.youtube.com)._**\n\n## Installation\n\nRefer to our [Installation Guide](https://spotdl_romanized_lyrics.rtfd.io/en/latest/installation/) for more\ndetails\n\n- Python (**Recommended**)\n  - _spotdl_romanized_lyrics_ can be installed by running `pip install spotdl_romanized_lyrics`.\n  > On some systems you might have to change `pip` to `pip3`.\n\n### Other options\n\n- Prebuilt Executable\n  - You can download the latest version from the\n    [Releases Tab](https://github.com/spotdl_romanized_lyrics/spotify-downloader/releases)\n- On Termux\n  - `curl -L https://raw.githubusercontent.com/spotdl_romanized_lyrics/spotify-downloader/master/scripts/termux.sh | sh`\n- Arch\n  - There is an Arch User Repository (AUR) package for\n    [spotdl_romanized_lyrics](https://aur.archlinux.org/packages/python-spotdl_romanized_lyrics/).\n- Docker\n  - Build image:\n\n    ```bash\n    docker build -t spotdl_romanized_lyrics .\n    ```\n\n  - Launch container with spotdl_romanized_lyrics parameters (see section below). You need to create mapped\n    volume to access song files\n\n    ```bash\n    docker run --rm -v $(pwd):/music spotdl_romanized_lyrics download [trackUrl]\n    ```\n\n### Installing FFmpeg\n\nIf using FFmpeg only for spotdl_romanized_lyrics, you can install FFmpeg to your local directory.\n`spotdl_romanized_lyrics --download-ffmpeg` will download FFmpeg to your spotdl_romanized_lyrics installation directory.\n\nWe recommend the above option, but if you want to install FFmpeg system-wide,\n\n- [Windows Tutorial](https://windowsloop.com/install-ffmpeg-windows-10/)\n- OSX - `brew install ffmpeg`\n- Linux - `sudo apt install ffmpeg` or use your distro\'s package manager\n\n## Usage\n\nTo get started right away:\n\n```sh\nspotdl_romanized_lyrics download [urls]\n```\n\nTo start the Web UI:\n\n```sh\nspotdl_romanized_lyrics web\n```\n\nYou can run _spotdl_romanized_lyrics_ as a package if running it as a script doesn\'t work:\n\n```sh\npython -m spotdl_romanized_lyrics [urls]\n```\n\n______________________________________________________________________\n\n### Further information can be found in our documentation\n\n**[Read the documentation on ReadTheDocs!](http://spotdl_romanized_lyrics.rtfd.io/)**\n\n______________________________________________________________________\n\n## Contributing\n\nInterested in contributing? Check out our [CONTRIBUTING.md](docs/CONTRIBUTING.md) to find\nresources around contributing along with a guide on how to set up a development environment.\n\n## License\n\nThis project is Licensed under the [MIT](/LICENSE) License.\n',
    'author': 'aeska444',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<3.12',
}


setup(**setup_kwargs)
