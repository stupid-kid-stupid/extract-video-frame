"""
Extract the frame at a specified timestamp from a video and save it as an image.
读取视频指定时间点的帧并保存为图片
"""

import cv2


def extract_frame(
    video_path: str,
    time_sec: float,
    output_path: str | None = None,
) -> str:
    """
    读取视频指定时间点的帧并保存为图片。

    参数:
        video_path: 视频文件路径。
        time_sec:   要提取的时间点（单位：秒）。
        output_path: 输出图片路径；为 None 时自动命名为
                     "<视频名>_<时间点>s.png"。

    返回:
        实际保存的图片路径。

    异常:
        RuntimeError: 视频打不开、读取失败或图片保存失败。
    """
    if output_path is None:
        stem = video_path.rsplit(".", 1)[0]
        output_path = f"{stem}_{time_sec:g}s.png"

    cap = cv2.VideoCapture(video_path)
    try:
        if not cap.isOpened():
            raise RuntimeError(f"视频打不开，请检查路径：{video_path}")

        # 定位到指定时间点（毫秒）
        cap.set(cv2.CAP_PROP_POS_MSEC, time_sec * 1000)
        success, frame = cap.read()
        if not success:
            raise RuntimeError(
                f"读取失败，请确认视频长度超过 {time_sec} 秒。"
            )

        # 不进行缩放，直接保存原尺寸画面
        if not cv2.imwrite(output_path, frame):
            raise RuntimeError(f"图片保存失败：{output_path}")

        height, width = frame.shape[:2]
        print(f"已保存：{output_path}，尺寸：{width} × {height}")
        return output_path

    finally:
        cap.release()


if __name__ == "__main__":
    video_path = "test.mp4"
    time_sec = 1.0              # 指定时间点（秒）
    output_path = None

    extract_frame(video_path, time_sec, output_path)