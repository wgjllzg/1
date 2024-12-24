#!/usr/bin/env python3

import sys
import argparse
from jetson_utils import videoSource, videoOutput, Log

# 解析命令行参数
parser = argparse.ArgumentParser(description="Test camera functionality on Jetson platform.",
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 epilog=videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream (default: camera)")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream (default: display window)")
parser.add_argument("--flip", type=str, default="none", choices=["none", "horizontal", "vertical"],
                    help="Flip the video stream (default: none)")

try:
    args = parser.parse_known_args()[0]
except:
    print("\nFailed to parse arguments\n")
    parser.print_help()
    sys.exit(0)

# 创建视频输入和输出
input_stream = videoSource(args.input, argv=sys.argv)
output_stream = videoOutput(args.output, argv=sys.argv)

# 主循环
while True:
    # 捕获当前帧
    frame = input_stream.Capture()

    if frame is None:  # 超时检查
        continue

    # 根据参数选择是否翻转图像
    if args.flip == "horizontal":
        frame = frame.FlippedHorizontal()
    elif args.flip == "vertical":
        frame = frame.FlippedVertical()

    # 在窗口中显示当前帧
    output_stream.Render(frame)

    # 更新状态栏
    output_stream.SetStatus(f"Camera Test | FPS: {input_stream.GetFrameRate():.2f}")

    # 打印性能信息
    Log.Verbose("Captured frame at {:.2f} FPS".format(input_stream.GetFrameRate()))

    # 如果输入或输出流结束，则退出循环
    if not input_stream.IsStreaming() or not output_stream.IsStreaming():
        break

print("Camera test finished.")
