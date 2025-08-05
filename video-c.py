import sys
import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

# 解决打包时OpenCV的FFmpeg依赖问题
def fix_opencv_ffmpeg():
    """确保OpenCV能找到FFmpeg DLL"""
    if getattr(sys, 'frozen', False):
        # 在打包环境中
        base_dir = sys._MEIPASS
    else:
        # 在开发环境中
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 尝试查找OpenCV的FFmpeg DLL
    dll_names = [
        "opencv_videoio_ffmpeg420_64.dll",
        "opencv_videoio_ffmpeg430_64.dll",
        "opencv_videoio_ffmpeg440_64.dll",
        "opencv_videoio_ffmpeg453_64.dll",
        "opencv_videoio_ffmpeg454_64.dll"
    ]
    
    for dll_name in dll_names:
        dll_path = os.path.join(base_dir, dll_name)
        if os.path.exists(dll_path):
            # 设置环境变量让OpenCV找到DLL
            os.environ["OPENCV_VIDEOIO_PRIORITY_FFMPEG"] = "1"
            os.environ["PATH"] = os.pathsep.join([base_dir, os.environ["PATH"]])
            cv2.videoio_registry.addBackend(dll_path)
            print(f"找到并加载FFmpeg DLL: {dll_path}")
            return True
    
    print("警告: 未找到OpenCV FFmpeg DLL，视频处理可能受限")
    return False

# 尝试修复FFmpeg依赖
fix_opencv_ffmpeg()

def convert_video_resolution(input_path, output_path, target_width, target_height):
    """转换视频分辨率并保持宽高比（添加黑边填充）"""
    # 打开视频文件
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError(f"无法打开视频文件: {input_path}")
    
    # 获取原始视频属性
    orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 创建视频写入对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (target_width, target_height))
    
    if not out.isOpened():
        raise ValueError(f"无法创建输出文件: {output_path}")
    
    # 计算缩放比例并添加黑边
    scale = min(target_width / orig_width, target_height / orig_height)
    new_width = int(orig_width * scale)
    new_height = int(orig_height * scale)
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2
    
    print(f"开始转换: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
    print(f"原始分辨率: {orig_width}x{orig_height} -> 目标分辨率: {target_width}x{target_height}")
    
    frame_count = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 调整大小并添加黑边
            resized = cv2.resize(frame, (new_width, new_height))
            canvas = cv2.copyMakeBorder(
                resized, 
                y_offset, 
                target_height - new_height - y_offset,
                x_offset,
                target_width - new_width - x_offset,
                cv2.BORDER_CONSTANT, 
                value=[0, 0, 0]
            )
            
            # 写入帧
            out.write(canvas)
            
            # 显示进度
            frame_count += 1
            if frame_count % 30 == 0:
                percent = frame_count / total_frames * 100
                print(f"处理进度: {frame_count}/{total_frames} 帧 ({percent:.1f}%)")
                
        print(f"转换完成! 保存至: {output_path}")
        return True
    except Exception as e:
        print(f"转换过程中出错: {str(e)}")
        return False
    finally:
        # 确保释放资源
        cap.release()
        out.release()

def select_and_convert():
    """选择视频文件并进行分辨率转换"""
    # 创建Tkinter根窗口
    root = tk.Tk()
    root.withdraw()
    root.title("视频分辨率转换工具")
    
    # 选择视频文件
    input_path = filedialog.askopenfilename(
        title="选择视频文件",
        filetypes=[("视频文件", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv")]
    )
    
    if not input_path:
        print("未选择文件")
        return
    
    # 设置输出目录
    output_dir = os.path.join(os.path.dirname(input_path), "converted_videos")
    os.makedirs(output_dir, exist_ok=True)
    
    # 定义目标分辨率
    resolutions = [
        (1920, 1080),  # Full HD
        (1280, 720)    # HD
    ]
    
    # 转换并保存
    output_files = []
    for width, height in resolutions:
        filename = os.path.splitext(os.path.basename(input_path))[0]
        output_filename = f"{filename}_{width}x{height}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            success = convert_video_resolution(input_path, output_path, width, height)
            if success:
                output_files.append(output_path)
        except Exception as e:
            error_msg = f"转换失败: {str(e)}"
            print(error_msg)
            messagebox.showerror("转换错误", error_msg)
    
    if output_files:
        success_msg = "所有转换完成!\n保存的文件:\n" + "\n".join(output_files)
        print(success_msg)
        messagebox.showinfo("转换完成", success_msg)
    else:
        error_msg = "没有成功转换任何文件"
        print(error_msg)
        messagebox.showerror("转换失败", error_msg)

if __name__ == "__main__":
    try:
        select_and_convert()
    except Exception as e:
        error_msg = f"程序发生错误: {str(e)}"
        print(error_msg)
        messagebox.showerror("程序错误", error_msg)
