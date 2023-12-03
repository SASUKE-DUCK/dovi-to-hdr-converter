import argparse
import subprocess

def encode_video(input_file, output_file, output_bitrate, encoding_type):
    common_params = [
        'ffmpeg.exe',
        '-nostdin',
        '-loglevel', 'error',
        '-stats',
        '-y',
        '-init_hw_device', 'vulkan=vulkan',
        '-filter_hw_device', 'vulkan'
    ]

    video_filters = {
        "hdr10": "hwupload,libplacebo=peak_detect=false:colorspace=9:color_primaries=9:color_trc=16:range=tv:format=yuv420p10le,hwdownload,format=yuv420p10le",
        "sdr": "hwupload,libplacebo=peak_detect=false:colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv:format=yuv420p10le,hwdownload,format=yuv420p10le",
        "hlg": "hwupload,libplacebo=iw:ih:format=yuv420p10le:format=rgb48le"
    }

    x265_params = {
        "hdr10": "repeat-headers=1:sar=1:hrd=1:aud=1:open-gop=0:hdr10=1:sao=0:rect=0:cutree=0:deblock=-3-3:strong-intra-smoothing=0:chromaloc=2:aq-mode=1:vbv-maxrate=160000:vbv-bufsize=160000:max-luma=1023:max-cll=0,0:master-display=G(8500,39850)B(6550,23000)R(35400,15650)WP(15635,16450)L(10000000,1)WP(15635,16450)L(1000000,100%):preset=slow",
        "sdr": "deblock=-3-3:vbv-bufsize=62500:vbv-maxrate=50000:fast-pskip=0:dct-decimate=0:level=5.1:ref=5:psy-rd=1.05,0.15:subme=11:me=umh:me_range=48:preset=slow",
        "hlg": "open-gop=0:atc-sei=18:pic_struct=0:preset=slow"
    }

    if encoding_type not in video_filters or encoding_type not in x265_params:
        print(f"Invalid encoding type: {encoding_type}")
        return

    ffmpeg_cmd = common_params + [
        '-i', input_file,
        '-vf', video_filters[encoding_type],
        '-c:v', 'libx265',
        '-map_chapters', '-1',
        '-an', '-sn',
        '-b:v', f'{output_bitrate}k',
        '-x265-params', x265_params[encoding_type],
        f'{output_file}_{encoding_type}_slow.mp4'
    ]

    subprocess.run(ffmpeg_cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode video using FFmpeg")
    parser.add_argument("-i", "--input", required=True, help="Input file path")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    parser.add_argument("--bitrate", type=int, required=True, help="Output bitrate in kbps")
    parser.add_argument("--type", required=True, choices=["hdr10", "sdr", "hlg"], help="Encoding type")

    args = parser.parse_args()
    encode_video(args.input, args.output, args.bitrate, args.type)
