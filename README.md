# wallwapper
## auto change wallwapper

### exe打包命令
```shell
pyinstaller --onefile --noconsole  --name wallwapper --icon ./resource/icon/umbrella-outline.png --add-data "resource/icon/umbrella-outline.png;resource/icon" ./wallwapper/Main.py
```
该命令用于创建 Python 程序“Main.py”的单个可执行文件。 
 
“--onefile”选项告诉 pyinstaller 创建一个包含程序运行所需的所有必要文件的单个文件，包括 Python 解释器本身。 
 
“--noconsole”选项告诉 pyinstaller 在程序运行时不创建控制台窗口。 
 
“--name”选项指定将创建的可执行文件的名称。 
 
“--icon”选项指定用于可执行文件的图标文件的路径。 
 
“--add-data”选项指定将包含在可执行文件中的文件或目录列表。 
 
在这种情况下，“resource/icon/umbrella-outline.png”文件被包含在可执行文件中，以便于可执行文件运行时在临时文件中生成必要文件