import os

try:
    os.system("taskkill /f /im chromedriver.exe /t")
    print(f"Kill Chromedriver")
except Exception as e:
    print(f"Failed kill Chromedrvier")
