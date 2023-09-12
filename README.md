# Dolby Vision to HDR10, SDR, and HLG Video Converter

This repository contains a Python script that allows you to convert Dolby Vision (DoVi) video content to the HDR10, SDR (Standard Dynamic Range), or HLG (Hybrid Log-Gamma) formats using the powerful FFmpeg tool.

## What is Dolby Vision?

Dolby Vision is a high dynamic range (HDR) format that provides an exceptional visual experience in terms of color, contrast, and brightness. However, not all devices support Dolby Vision, which can limit its playback capabilities. This script enables you to transform Dolby Vision videos into more widely compatible formats such as HDR10, SDR, and HLG.

## Key Features:

- Convert Dolby Vision videos to HDR10, SDR, or HLG with optimal quality.
- Customize the output bitrate to suit your needs.
- Utilize FFmpeg for fast and efficient processing.
- Provide options to configure specific output parameters.

## Prerequisites:

- Python 3 installed on your system.
- FFmpeg installed on your system.
- Vulkan (Nvidia) installed on your PC for hardware acceleration (required for some conversions).

## Usage:

1. Clone this repository or download it as a ZIP file.
2. Run the script from the command line, providing the following arguments:

   ```
   python dovi_to_hdr_converter.py -i [VIDEO_PATH] -hdr [CONVERSION_FORMAT] --bitrate [BITRATE]
   ```

   - `[VIDEO_PATH]`: The path to the Dolby Vision video file you wish to convert.
   - `[CONVERSION_FORMAT]`: The desired conversion format (choose from "hdr10", "sdr", or "hlg").
   - `[BITRATE]`: The output bitrate in kbps (e.g., 8000k).

3. The script will perform the conversion and generate a new video file in the specified format.

## Example Usage:

To convert a Dolby Vision video to HDR10 with an output bitrate of 8000 kbps:

```
python dovi_to_hdr_converter.py -i my_dolby_vision_video.mp4 -hdr hdr10 --bitrate 8000k
```

Enjoy your Dolby Vision videos on a wide range of devices and screens!

---


**Note**: This script is designed to create HDR10, SDR, and HLG video files. It does not create hybrid Dolby Vision HDR files. If you want to create hybrid Dolby Vision HDR files, you can use the following tool after creating your initial file: [DV-HDR-Hybrid](https://github.com/SASUKE-DUCK/DV-HDR-Hybrid). 

Please note that it's not recommended to use this script with SDR files to create a hybrid file. If you encounter any issues or have questions, feel free to open an issue to seek assistance.

---

