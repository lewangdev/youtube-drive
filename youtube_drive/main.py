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


def cmd_encode(args):
    if args.encrypt and args.key is not None:
        args.key = str(args.key).encode("ascii")[:16]
    youtube_codec.encode(args.i, args.video_filename, args.video_fps, args.encrypt, args.key)


def cmd_decode(args):
    if args.decrypt and args.key is not None:
        args.key = str(args.key).encode("ascii")[:16]
    youtube_codec.decode(args.i, args.filename, args.decrypt, args.key)


def main(args):
    parser = argparse.ArgumentParser('youtube-drive')
    subparsers = parser.add_subparsers(title="commands")

    encode_parser = subparsers.add_parser('encode', aliases=['en'], help='encode a file to mp4 video')
    encode_parser.add_argument('-i',
                               action='store',
                               metavar="input_filename",
                               help='encode file <input_filename> to a video')
    encode_parser.add_argument('--video-fps',
                               action='store',
                               metavar="video_fps",
                               default=20,
                               type=int,
                               help='set video fps, default value is 20')
    encode_parser.add_argument('video_filename',
                               action='store',
                               help='save the video to this filename')
    encode_parser.add_argument('--encrypt',
                                action='store_true',
                                default=False,
                                help='encrypt the file')
    encode_parser.add_argument('--key',
                                action='store',
                                metavar="encryption_key",
                                default=None,
                                help='encryption key')
    encode_parser.set_defaults(handle=cmd_encode)

    decode_parser = subparsers.add_parser('decode', aliases=['de'], help='decode a video to a file')
    decode_parser.add_argument('-i',
                               action='store',
                               metavar="input_video_filename",
                               help='decode the video <input_video_filename> to a file')
    decode_parser.add_argument('filename',
                               action='store',
                               help='Save the output file to this filename')
    decode_parser.add_argument('--decrypt',
                               action='store_true',
                               default=False,
                               help='decrypt the file')
    encode_parser.add_argument('--key',
                                action='store',
                                metavar="decryption_key",
                                default=None,
                                help='decryption key')
    decode_parser.set_defaults(handle=cmd_decode)

    upload_parser = subparsers.add_parser('upload', aliases=['up'], help='upload a file to YouTube')
    upload_parser.add_argument('filename',
                               action='store',
                               help='encode file <filename> to a video and upload to YouTube')
    upload_parser.set_defaults(handle=cmd_upload)

    retrieve_parser = subparsers.add_parser("retrieve", aliases=['r'],
                                            help="retrieve a video from YouTube save as <filename>")
    retrieve_parser.add_argument('--video-id',
                                 action='store',
                                 metavar="video_id",
                                 help='download YouTube video with <video_id>')
    retrieve_parser.add_argument('-o',
                                 action='store',
                                 metavar="filename",
                                 help='save file to <filename>')
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
