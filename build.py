import PyInstaller.__main__
import os
import shutil

# 查找OpenCV的FFmpeg DLL
def find_opencv_dll():
    import cv2
    cv2_dir = os.path.dirname(cv2.__file__)
    for file in os.listdir(cv2_dir):
        if file.startswith("opencv_videoio_ffmpeg") and file.endswith("_64.dll"):
            return os.path.join(cv2_dir, file)
    return None

# 主打包函数
def build_exe():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_name = "video_converter.py"
    
    # 查找OpenCV DLL
    dll_path = find_opencv_dll()
    if not dll_path:
        print("警告: 未找到OpenCV FFmpeg DLL!")
        dll_cmd = []
    else:
        dll_name = os.path.basename(dll_path)
        dll_cmd = [f"--add-data={dll_path};."]
        print(f"找到OpenCV DLL: {dll_path}")
    
    # PyInstaller配置
    pyinstaller_cmd = [
        script_name,
        "--onefile",
        "--console",
        "--name=VideoResolutionConverter",
        "--icon=video_icon.ico",  # 可选：添加图标
        "--add-data=video_icon.ico;."  # 可选：添加图标
    ] + dll_cmd
    
    # 运行PyInstaller
    PyInstaller.__main__.run(pyinstaller_cmd)
    
    # 清理临时文件
    shutil.rmtree("build", ignore_errors=True)
    if os.path.exists("VideoResolutionConverter.spec"):
        os.remove("VideoResolutionConverter.spec")
    
    print("打包完成! 可执行文件在 'dist' 目录中")

if __name__ == "__main__":
    build_exe()
