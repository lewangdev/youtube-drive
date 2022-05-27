# youtube-drive

youtube-drive is totally inspired by [YouTubeDrive](https://github.com/dzhang314/YouTubeDrive), a Wolfram Language (aka Mathematica) package. I read the source code of **YouTubeDrive** and write a Python version with a little change for fun.

**youtube-drive** is a Python library encodes/decodes arbitrary data to/from simple RGB videos which are automatically uploaded to/downloaded from YouTube. Since YouTube imposes no limits on the total number or length of videos users can upload, this provides an effectively infinite but extremely slow form of file storage.

youtube-drive is a silly proof-of-concept, and I do not endorse its high-volume use either.

## Usage Example

**Upload**: Encode a file to video and upload to YouTube:

```sh
python -m youtube_drive upload examples/BesselJ.png
YouTube Video ID: EzqstWlMXyk
YouTube: https://youtu.be/EzqstWlMXyk

```

**Retrieve**: Download the video from YouTube and decode to a file:

```sh
python -m youtube_drive retrieve --video-id=EzqstWlMXyk -o BesselJ-retrieved.png
/var/folders/md/dnr_ryfs2_x128p26xx2pnnc0000gn/T/tmp6qfm_msc.mp4
[youtube] EzqstWlMXyk: Downloading webpage
[youtube] EzqstWlMXyk: Downloading MPD manifest
[download] Destination: /var/folders/md/dnr_ryfs2_x128p26xx2pnnc0000gn/T/tmp6qfm_msc.f136.mp4
[download] 100% of 1.74MiB in 00:25
[download] Destination: /var/folders/md/dnr_ryfs2_x128p26xx2pnnc0000gn/T/tmp6qfm_msc.mp4.f140
[download] 100% of 58.70KiB in 00:03
[ffmpeg] Merging formats into "/var/folders/md/dnr_ryfs2_x128p26xx2pnnc0000gn/T/tmp6qfm_msc.mp4"
Deleting original file /var/folders/md/dnr_ryfs2_x128p26xx2pnnc0000gn/T/tmp6qfm_msc.f136.mp4 (pass -k to keep)
Deleting original file /var/folders/md/dnr_ryfs2_x128p26xx2pnnc0000gn/T/tmp6qfm_msc.mp4.f140 (pass -k to keep)
```

The video, video ID is **EzqstWlMXyk**, youtube-drive produces in this example can be viewed at https://youtu.be/EzqstWlMXyk. The video is encoded from the image [BesselJ.png](https://github.com/lewangdev/youtube-drive/blob/main/examples/BesselJ.png). A 62KB image file will produce a video of size 10+MB.

Another file I uploaded to YouTube is [painting.jpg](https://github.com/lewangdev/youtube-drive/blob/main/examples/painting.jpg), it produces a video of size 127.5MB, and the original size is 476KB. The video can be viewed at https://youtu.be/gKhXk3IGW2s.

I use opencv to produce mp4 video, if use ffmpeg with optimizing directly, the video maybe compress to a more smaller size.

**AGAIN:** It is a silly idea, just for fun.

## Installation

**Notice**:

- I only test with **Python 3.8 & 3.9** on **MacOS** with ffmpeg installed.
- If it works on your system, please feel free to let me know. Thanks.

For development:

```sh
git clone https://github.com/lewangdev/youtube-drive.git
cd youtube-drive
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Or run directly from sources:

```sh
git clone https://github.com/lewangdev/youtube-drive.git
cd youtube-drive
python -m venv .venv
. .venv/bin/activate
python setup.py install
```

## Setup

The first time you try to upload a video to YouTube, you will be asked to follow a URL in your browser to get an authentication token. If you have multiple channels for the logged in user, you will also be asked to pick which one you want to upload the videos to

You now must create and use your own OAuth 2.0 file, it's a free service. Steps:

Go to the [Google Cloud Console](https://console.cloud.google.com/).

- Create project.
- Side menu: APIs & Services -> OAuth consent screen: Create app and add the test user you will updoad videos to.
- Side menu: APIs & Services -> Enabled API & services -> ENABLED API AND SERVICES -> Search `youtube` -> Choose `YouTube Data API v3` and enable it.
- Side menu: APIs & Services -> Credentials -> Create Credentials -> OAuth client ID: Application type choose `Desktop app`.
- Download JSON: Under the section "OAuth 2.0 client IDs". Save the file to your local system.
  Use this JSON as your credentials file: copy it to ~/.client_secrets.json.
  Note: client_secrets.json is a file you can download from the developer console, the credentials file is something auto generated after the first time the script is run and the google account sign in is followed, the file is stored at ~/.youtube-upload-credentials.json.

## Usage

**Commands:**

```sh
python -m youtube_drive -h
usage: youtube-drive [-h] {upload,up,retrieve,r} ...

optional arguments:
  -h, --help            show this help message and exit

Commands:
  {upload,up,retrieve,r}
    upload (up)         Upload a file to YouTube
    retrieve (r)        Retrieve a video from YouTube save as <filename>

```

If you install from source, you can run the script directly:

```sh
youtube-drive -h
usage: youtube-drive [-h] {upload,up,retrieve,r} ...

optional arguments:
  -h, --help            show this help message and exit

Commands:
  {upload,up,retrieve,r}
    upload (up)         Upload a file to YouTube
    retrieve (r)        Retrieve a video from YouTube save as <filename>

```

**Upload:**

```sh
python -m youtube_drive upload -h
usage: youtube-drive upload [-h] filename

positional arguments:
  filename    Encode file <filename> to a video and upload to YouTube

optional arguments:
  -h, --help  show this help message and exit

```

**Retrieve:**

```sh
python -m youtube_drive r -h
usage: youtube-drive retrieve [-h] [--video-id video_id] [-o filename]

optional arguments:
  -h, --help           show this help message and exit
  --video-id video_id  Download YouTube video with <video_id>
  -o filename          Save file to <filename>

```

## The difference between **youtube-drive** and **YouTubeDrive**

I add 4 bytes for representing data length at the beginning for the file for easily padding to video frames
