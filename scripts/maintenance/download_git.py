import urllib.request
import os

print("Downloading Git for Windows...")
url = "https://github.com/git-for-windows/git/releases/download/v2.51.2.windows.1/Git-2.51.2-64-bit.exe"
filename = "Git-2.51.2-64-bit.exe"

try:
    urllib.request.urlretrieve(url, filename)
    print(f"✅ Downloaded: {filename}")
    print("🎯 Run the .exe file to install Git")
except Exception as e:
    print(f"❌ Download failed: {e}")
    print("🔧 Try the SourceForge link instead")