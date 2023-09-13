import os
import argparse
import subprocess
import logging
import coloredlogs

LOG_FORMAT = "{asctime} [{levelname[0]}] {name} : {message}"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_STYLE = "{"

# Configure the custom logger
class Logger():
    def __init__(self, service, log_level):
        self.service = service
        self.log_level = log_level

    def set_logger(self):
        logger1 = logging.getLogger(self.service)
        coloredlogs.install(level=self.log_level, fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, style=LOG_STYLE)
        return logger1

logger = Logger("DoVi", "INFO").set_logger()
logger.info("by -∞WKS∞-#3982")
# File paths
current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)

ffmpegexe = os.path.join(dir_path, 'ffmpeg.exe')

# Argument parser
parser = argparse.ArgumentParser(description="Convert a video file to HDR10, HLG, or SDR")
parser.add_argument("-i", "--input", required=True, help="Input file path")
parser.add_argument("-hdr", choices=["hdr10", "hlg", "sdr"], required=True, help="Conversion type (hdr10, hlg, or sdr)")
parser.add_argument("--bitrate", type=int, required=True, help="Output bitrate in kbps")
args = parser.parse_args()

input_file = args.input
output_path = input_file + "_" + args.hdr
bitrate = args.bitrate

# FFmpeg command templates
preset = "slow"
dv_to_hdr10 = [
    ffmpegexe,
    '-nostdin',
    '-loglevel', 'error',
    '-stats',
    "-y",
    "-preset", preset,
    "-init_hw_device", "vulkan=vulkan",
    "-filter_hw_device", "vulkan",
    "-i", input_file,
    "-vf",
    "hwupload,libplacebo=peak_detect=false:colorspace=9:color_primaries=9:color_trc=16:range=tv:format=yuv420p10le,hwdownload,format=yuv420p10le",
    "-c:v", "libx265",
    "-c:a", "copy",
    '-map_chapters', '-1',
    '-an',
    '-sn',
    "-y",
    '-b:v', f'{bitrate}k',
    "-x265-params",
    f"repeat-headers=1:sar=1:hrd=1:aud=1:open-gop=0:hdr10=1:sao=0:rect=0:cutree=0:deblock=-3-3:strong-intra-smoothing=0:chromaloc=2:aq-mode=1:vbv-maxrate=160000:vbv-bufsize=160000:max-luma=1023:max-cll=0,0:master-display=G(8500,39850)B(6550,23000)R(35400,15650)WP(15635,16450)L(10000000,1)WP(15635,16450)L(1000000,100%)",
    output_path + ".mp4"
]


dv_to_sdr = [
    ffmpegexe,
    '-nostdin',
    '-loglevel', 'error',
    '-stats',
    "-y",
    "-init_hw_device", "vulkan=vulkan",
    "-vf",
    "hwupload,libplacebo=peak_detect=false:colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv:format=yuv420p10le,hwdownload,format=yuv420p10le",
    "-c:v", "libx265",
    "-preset", preset,
    '-map_chapters', '-1',
    '-an',
    '-sn',
    "-y",
    '-b:v', f'{bitrate}k',
    "-x265-params",
    "deblock=-3-3:vbv-bufsize=62500:vbv-maxrate=50000:fast-pskip=0:dct-decimate=0:level=5.1:ref=5:psy-rd=1.05,0.15:subme=11:me=umh:me_range=48",
    output_path + ".mp4"
]

dv_to_hlg = [
    ffmpegexe,
    '-nostdin',
    '-loglevel', 'error',
    '-stats',
    "-y",
    "-preset", preset,
    "-init_hw_device", "vulkan=vulkan",
    "-filter_hw_device", "vulkan",
    "-i", input_file,
    "-vf",
    "hwupload,libplacebo=iw:ih:format=yuv420p10le:colorspace=bt2020nc:color_primaries=bt2020:color_trc=arib-std-b67,hwdownload,format=yuv420p10le",
    "-c:v", "libx265",
    '-map_chapters', '-1',
    '-an',
    '-sn',
    "-y",
    '-b:v', f'{bitrate}k',
    output_path + ".mp4"
]

# Select the appropriate command
command = []

if args.hdr == "hdr10":
    command = dv_to_hdr10
elif args.hdr == "sdr":
    command = dv_to_sdr
elif args.hdr == "hlg":
    command = dv_to_hlg

# Execute FFmpeg command
try:
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    logger.info("FFmpeg process completed.")
except subprocess.CalledProcessError as e:
    logger.error("Error executing FFmpeg:", e)
    logger.error("Error output:", e.stderr.decode())
