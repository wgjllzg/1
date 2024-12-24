from jetson_utils import videoSource, videoOutput

# 初始化输入和输出流
try:
    input_stream = videoSource("csi://0?width=1280&height=720&framerate=30", argv=sys.argv)
    output_stream = videoOutput("", argv=sys.argv)
except Exception as e:
    print(f"Error initializing video streams: {e}")
    sys.exit(1)

while True:
    try:
        frame = input_stream.Capture()
        if frame is None:
            print("Timeout or no frame captured. Retrying...")
            continue

        output_stream.Render(frame)
        output_stream.SetStatus("Camera Test | FPS: {:.2f}".format(input_stream.GetFrameRate()))

    except Exception as e:
        print(f"Error during frame processing: {e}")
        break

    if not input_stream.IsStreaming() or not output_stream.IsStreaming():
        print("Stream ended.")
        break

print("Camera test finished.")
