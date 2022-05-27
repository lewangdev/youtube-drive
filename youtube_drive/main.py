from ast import alias, arguments
import tempfile
import os
import sys
import uuid
import argparse
import youtube_dl
from youtube_upload import auth, lib, upload_video
from . import youtube_codec


def get_youtube_upload_handler():
    """Return the API Youtube object."""
    home = os.path.expanduser("~")
    client_secrets = os.path.join(home, ".client_secrets.json")
    credentials = os.path.join(home, ".youtube-upload-credentials.json")
    get_code_callback = (auth.console.get_code)
    return auth.get_resource(client_secrets, credentials,
                             get_code_callback=get_code_callback)


def upload_youtube_video(youtube, title, video_path):
    """Upload video with index (for split videos)."""
    u = lib.to_utf8
    title = u(title)

    request_body = {
        "snippet": {
            "title": title,
            "description": "",
            "categoryId": None,
            "tags": u(""),
            "defaultLanguage": None,
            "defaultAudioLanguage": None

        },
        "status": {
            "embeddable": True,
            "privacyStatus": "unlisted",
            "publishAt": None,
            "license": "youtube",
        },
        "recordingDetails": {
            "location": None,
            "recordingDate": None,
        },
    }

    return upload_video.upload(youtube, video_path, request_body)


def download_youtube_video(video_id, output_file_path):
    ydl_opts = {'outtmpl': output_file_path}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={video_id}"])


def youtube_upload(upload_file_path):
    video_path = tempfile.mktemp(".mp4")
    youtube_codec.encode(upload_file_path, video_path)
    youtube = get_youtube_upload_handler()
    video_id = upload_youtube_video(youtube, f"DATA-{str(uuid.uuid4()).upper()}", video_path)
    os.remove(video_path)
    return video_id


def youtube_retrieve(video_id, output_file_path):
    video_path = tempfile.mktemp(".mp4")
    print(video_path)
    download_youtube_video(video_id, video_path)
    youtube_codec.decode(video_path, output_file_path)


def cmd_upload(args):
    video_id = youtube_upload(args.filename)
    print(f"YouTube Video ID: {video_id}", f"YouTube: https://youtu.be/{video_id}", sep="\n")


def cmd_retrieve(args):
    youtube_retrieve(args.video_id, args.o)


def main(args):
    parser = argparse.ArgumentParser('youtube-drive')
    subparsers = parser.add_subparsers(title="Commands")

    upload_parser = subparsers.add_parser('upload', aliases=['up'], help='Upload a file to YouTube')
    upload_parser.add_argument('filename',
                               action='store',
                               help='Encode file <filename> to a video and upload to YouTube')
    upload_parser.set_defaults(handle=cmd_upload)

    retrieve_parser = subparsers.add_parser(
        "retrieve", aliases=['r'],
        help="Retrieve a video from YouTube save as <filename>")
    retrieve_parser.add_argument('--video-id',
                                 action='store',
                                 metavar="video_id",
                                 help='Download YouTube video with <video_id>')
    retrieve_parser.add_argument('-o',
                                 action='store',
                                 metavar="filename",
                                 help='Save file to <filename>')
    retrieve_parser.set_defaults(handle=cmd_retrieve)
    arguments = parser.parse_args(args)
    if not hasattr(arguments, 'handle'):
        parser.print_help()
        sys.exit(1)

    arguments.handle(arguments)


def run():
    main(sys.argv[1:])


if __name__ == '__main__':
    # video_id = youtebe_upload("./examples/upload.mp4")
    # print(f"video_id: {video_id}")
    # youtube_codec.encode("./examples/painting.jpg", "./examples/upload.mp4")
    # youtube_codec.decode("./examples/upload.mp4", "./examples/painting-retrieved.jpg")
    # youtube_retrieve("gKhXk3IGW2s", "./examples/painting-retrieved-3.jpg")
    main(sys.argv[1:])
