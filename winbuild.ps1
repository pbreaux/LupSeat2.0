choco install -y python3
py -m pip install pyinstaller

C:/Python39/Scripts/pyinstaller.exe --onefile --noconsole lupseat
Move-Item dist/lupseat.exe exec
