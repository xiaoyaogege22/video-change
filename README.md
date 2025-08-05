# video-change(视频格式转换)
由于我们无法在纯Python环境中直接实现图形界面的文件上传，因此这里将使用Tkinter来创建一个简单的GUI用于文件选择。
 另外，视频处理我们将使用OpenCV库。请确保已经安装了opencv-python和tkinter。
 步骤：
 1. 导入必要的库：tkinter用于文件选择，cv2用于视频处理，以及可能需要用到的其他库。
 2. 创建一个函数，用于打开文件选择对话框，让用户选择一个视频文件。
 3. 定义两个目标分辨率：1920x1080和1280x720。
 4. 读取视频文件，然后分别将其转换为两种分辨率，并保存为两个不同的文件。
 注意：视频的重新缩放可能会改变宽高比，我们可以选择保持宽高比并填充黑边，或者直接拉伸。这里我们选择保持宽高比并填充黑边（以避免变形）。
 但注意：1920x1080是16:9，1280x720也是16:9，所以如果原始视频是16:9，则不会变形；如果不是，则我们需要进行填充。
 我们将采用以下方法：
   - 计算目标宽高比
   - 根据原始视频的宽高比，调整到目标分辨率，同时保持宽高比（即保证视频内容不变形），然后在两边或上下添加黑边。
 然而，另一种常见的需求是直接拉伸到目标分辨率（不考虑宽高比），但这样会变形。这里我们按照用户通常的期望，选择保持宽高比并填充黑边。
 具体步骤：
  1. 打开视频文件。
  2. 获取原始视频的分辨率和帧率。
  3. 对于每个目标分辨率，计算缩放后的尺寸，使其在保持原始宽高比的前提下，最大化地适应目标分辨率，并在需要时添加黑边。
  4. 创建视频写入对象，将每一帧调整大小并写入新文件。
 但是，注意：重新编码视频可能会损失质量，并且处理时间可能较长。
 我们将分别生成两个视频文件，文件名在原文件名基础上加上分辨率标识。
 由于视频处理可能比较耗时，我们将使用一个简单的进度条（控制台输出）来显示处理进度。
 另外，我们还需要注意音频的处理。但是，OpenCV本身不支持音频处理。因此，这个简单的脚本将只处理视频流，而忽略音频。
 如果需要保留音频，可以使用其他库（如moviepy）或者之后将原始音频合并到新视频中。但根据要求，我们只使用OpenCV，所以这里不考虑音频。
 如果要求保留音频，那么可能需要更复杂的处理。但题目中没有明确要求，因此我们只处理视频。
 由于时间关系，我们这里只实现视频流的处理。
 实现：
 我们将创建一个函数来处理视频并保存为指定分辨率。
 步骤：
  1. 读取视频文件。
  2. 获取视频的总帧数（用于进度显示）。
  3. 创建VideoWriter对象，使用与原视频相同的帧率（但分辨率改变）。
  4. 逐帧读取视频，调整每一帧（保持宽高比并填充黑边），然后写入新视频。
  5. 释放资源。
 调整帧大小的函数：
   - 计算缩放比例，分别计算宽度和高度的缩放比例，取较小的比例，然后进行缩放。
   - 然后将缩放后的图像放置在目标分辨率的黑色背景的中心。
 注意：OpenCV中图像的高度在前，宽度在后，即(h, w)，而分辨率是(width, height)，即(w, h)。
 例如：1080p是 (1920, 1080) -> (w, h) = (1920, 1080)
 我们将定义一个函数`resize_with_padding`来实现。
 由于视频编码格式，我们使用原视频的编码格式（通过fourcc）。但注意，不同视频的编码格式可能不同，我们可以通过原视频的编码来设置，或者统一使用一种编码（如MP4V）。
 这里我们统一使用MP4V（.mp4）的编码，即fourcc设置为'mp4v'。如果输入不是mp4，我们输出为mp4。
 但注意：输入可能是其他格式，我们根据输入文件的后缀来设置输出格式？但为了简单，我们输出为mp4。
 所以，输出文件名：原文件名+分辨率+.mp4
 代码结构：
 1. 选择文件
 2. 定义两个目标分辨率
 3. 对每个目标分辨率，调用处理函数，生成新视频。
 由于处理时间较长，我们分别处理两个分辨率，并显示进度。
 我们需要将这段代码打包成Windows可执行文件（.exe）。为此，我们可以使用PyInstaller。
 但是，在打包之前，我们需要确保代码中使用的库都已安装，并且我们可能需要做一些调整以便于打包。
 步骤：
 1. 安装PyInstaller: `pip install pyinstaller`
 2. 编写打包命令，注意：由于使用了OpenCV和Tkinter，我们需要确保这些库被正确打包。
 但是，我们注意到代码中使用了OpenCV（cv2）和Tkinter。在打包时，PyInstaller通常能够自动包含这些库。
 然而，OpenCV可能会有一些额外的依赖文件，所以我们需要测试。
 另外，由于我们使用了文件对话框，在打包时可能会遇到Tkinter相关的问题，但通常PyInstaller能够处理。
 打包命令示例：
    pyinstaller --onefile --windowed --add-data "opencv_videoio_ffmpeg420_64.dll;." video_converter.py
 注意：OpenCV可能需要一个额外的DLL（opencv_videoio_ffmpeg420_64.dll）来处理某些视频格式。我们可以从OpenCV的安装目录中找到这个DLL。
 例如，在Python的Lib/site-packages/cv2/目录下。我们需要将这个DLL文件与我们的可执行文件一起分发。
 但是，在代码中，我们也可以尝试设置环境变量来让OpenCV找到这个DLL，或者将其放在同一目录下。
 然而，在代码中，我们并没有显式指定这个DLL，所以OpenCV可能会在它自己的目录中找到。在打包时，我们需要将这个DLL复制到可执行文件所在的目录。
 因此，我们修改代码：在程序开始时，将当前工作目录添加到OpenCV的搜索路径中，并将DLL复制到当前目录（或者我们可以通过PyInstaller的--add-data参数将其打包进去）。
 但是，更简单的方式是：我们使用PyInstaller的--add-data参数将DLL文件打包到可执行文件的同一目录。
 首先，我们需要找到这个DLL文件。在OpenCV的安装目录（例如：`<python_dir>/Lib/site-packages/cv2/`）下，有类似`opencv_videoio_ffmpeg420_64.dll`的文件（版本可能不同，可能是420、430等）。
 我们可以使用以下代码来获取OpenCV的版本，然后动态确定DLL文件名（但为了简单，我们可以先找到并指定它）。
 由于我们不确定用户环境，所以最好在打包时包含这个DLL。
 然而，在代码中，我们也可以不依赖这个DLL？但如果没有它，OpenCV可能无法读取某些格式（如MP4）。
 因此，我们决定在打包时包含这个DLL。
 步骤：
 1. 找到DLL文件（例如：opencv_videoio_ffmpeg420_64.dll）
 2. 在打包命令中，使用--add-data将该DLL文件添加到可执行文件的根目录。
 但是，我们也可以考虑在代码中设置环境变量，让OpenCV能够找到它。我们可以在代码开头添加：
    import os
    from pathlib import Path
    import sys
    # 如果是打包后的可执行文件
    if getattr(sys, 'frozen', False):
        # 我们是在PyInstaller打包的环境中
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).parent
    dll_path = base_dir / "opencv_videoio_ffmpeg420_64.dll"
    if dll_path.exists():
        os.environ["OPENCV_VIDEOIO_FFMPEG_DEBUG"] = "1"  # 可选，调试
        os.environ["PATH"] = os.pathsep.join([str(base_dir), os.environ["PATH"]])
 但是，这样可能还不够，因为OpenCV在加载时可能不会立即从当前目录加载。我们可以尝试在导入cv2之前设置。
 因此，我们需要在代码最前面插入这段代码。
 但是，为了简化，我们可以尝试在打包时将这个DLL复制到可执行文件同一目录，然后通过设置PATH让系统找到它。或者，我们可以让OpenCV直接加载这个DLL。
 然而，OpenCV在运行时应该会自动查找当前目录，所以我们只要确保这个DLL在可执行文件旁边即可。
 所以，我们可以在打包时使用--add-data参数包含这个DLL。
 但是，由于我们无法确定每个OpenCV版本对应的DLL文件名，我们可以先查看自己环境中的DLL文件名。
 假设我们使用的是OpenCV 4.5.x，那么DLL文件名可能是`opencv_videoio_ffmpeg452_64.dll`（具体数字版本可能不同）。
 我们可以写一个函数来检查本地OpenCV安装目录下的DLL文件，然后选择匹配`opencv_videoio_ffmpeg*_64.dll`的文件。
 但是，为了简化打包过程，我们可以在代码中不处理，而是要求打包者找到这个DLL并添加到打包命令中。
 因此，我们修改打包命令为：
    pyinstaller --onefile --windowed --add-data "<path_to_dll>;." video_converter.py
 其中<path_to_dll>是DLL文件的完整路径。
 另外，我们也可以将这段代码改为控制台程序（去掉--windowed），这样在运行时会显示控制台窗口，方便查看进度。
 由于我们在转换过程中需要打印进度，所以建议使用控制台窗口（即去掉--windowed，或者使用--console）。
 所以命令改为：
    pyinstaller --onefile --console --add-data "<dll_path>;." video_converter.py
 但是，我们也可以保留窗口，因为Tkinter的文件对话框需要。但是，控制台窗口可以显示打印信息，所以我们使用控制台模式。
 因此，我们使用--console。
 另外，我们也可以考虑在代码中不打印进度，而是使用GUI进度条？但为了简单，我们保留控制台打印。
 所以，我们不需要修改代码，只需打包。
 但是，为了避免在打包后出现DLL缺失问题，我们在代码中显式添加一个机制：在导入cv2之前，将DLL所在目录（如果是打包环境，则使用临时解压目录）添加到PATH。
 然而，PyInstaller在打包时，通过--add-data添加的文件在运行时会解压到临时目录（sys._MEIPASS），所以我们可以在代码中这样处理：
 修改代码开头：
    import os
    import sys
    from pathlib import Path
    # 判断是否打包运行
    if getattr(sys, 'frozen', False):
        # 打包运行，则临时文件夹在sys._MEIPASS
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).parent
    # 添加DLL目录到系统路径
    os.environ['PATH'] = str(base_dir) + os.pathsep + os.environ['PATH']
 然后，在导入cv2之前执行这段代码。
 因此，我们将代码结构调整为：
    1. 导入必要的模块（sys, os, pathlib）
    2. 设置PATH
    3. 导入cv2和其他模块
 这样，在导入cv2时，系统会从我们的临时目录（打包运行时）或当前目录（直接运行）中查找DLL。
 但是，我们还需要确保这个DLL被正确打包。在打包命令中，我们将DLL添加到数据文件，这样它会被解压到sys._MEIPASS。
 因此，我们修改代码：
 在文件最前面添加：
    import sys
    import os
    from pathlib import Path
    # 设置路径以便OpenCV能够找到FFMPEG DLL
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).parent
    # 将base_dir添加到PATH
    os.environ['PATH'] = str(base_dir) + os.pathsep + os.environ['PATH']
 然后，再导入cv2。
 但是，我们还需要注意：在打包时，我们添加的DLL文件名是什么？我们假设打包者将DLL文件命名为`opencv_videoio_ffmpeg420_64.dll`（或者它本来的名字）并添加到打包数据中。
 然而，OpenCV在加载时可能会自动查找匹配模式`opencv_videoio_ffmpeg*.dll`的文件，所以我们只要保证这个DLL在PATH中即可。
 因此，我们不需要修改代码中关于DLL文件名的部分。
 但是，为了确保安全，我们可以在代码中检查一下OpenCV是否能够读取视频文件。在convert_video_resolution函数中，我们捕获了错误，所以如果因为DLL缺失导致打不开视频，会抛出异常。
 打包步骤总结：
 1. 在开发环境中，找到OpenCV的FFMPEG DLL文件（在cv2安装目录下，如`C:\PythonXX\Lib\site-packages\cv2\`），复制到项目目录，假设命名为`opencv_videoio_ffmpeg420_64.dll`（或者你实际找到的文件名）。
 2. 修改代码，在文件开头添加上述设置PATH的代码，然后再导入cv2。
 3. 使用PyInstaller打包，命令如下：
        pyinstaller --onefile --console --add-data "opencv_videoio_ffmpeg420_64.dll;." video_converter.py
 4. 将生成的exe文件（在dist目录下）和可能需要的其他文件（比如这个DLL）一起分发？但不需要，因为DLL已经被打包进exe，运行时会被解压到临时目录。
 注意：我们使用`--add-data`将DLL文件包含进去，这样在运行时，它会被解压到临时目录（sys._MEIPASS），然后我们将其添加到PATH，所以OpenCV可以找到它。
 现在，我们修改代码：
 我们将代码开头部分修改，添加设置PATH的代码，并调整导入顺序。
 由于原始代码中已经有一些导入，我们将其拆分。
 修改后的代码结构：
    import sys
    import os
    from pathlib import Path
    # 设置路径以便OpenCV能够找到FFMPEG DLL
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).parent
    # 将base_dir添加到PATH
    os.environ['PATH'] = str(base_dir) + os.pathsep + os.environ['PATH']
    import cv2
    import tkinter as tk
    from tkinter import filedialog
    # ... 其他代码不变
 但是，我们还需要注意：在打包时，Tkinter可能会需要一些额外的数据文件，但PyInstaller通常能自动处理。
 现在，我们修改代码，然后打包。
 但是，我们还没有这个DLL文件，所以需要先找到它。假设我们已经在项目目录下放置了`opencv_videoio_ffmpeg420_64.dll`。
 然后，打包命令为：
        pyinstaller --onefile --console --add-data "opencv_videoio_ffmpeg420_64.dll;." video_converter.py
 注意：在Windows上，路径分隔符用分号（;），点号表示目标目录为根目录（在打包后，这个文件会被放在sys._MEIPASS目录下）。
 最后，我们还需要测试打包后的exe文件是否能够正常运行。
 因此，我们修改代码，添加设置PATH的代码，并调整导入顺序。
