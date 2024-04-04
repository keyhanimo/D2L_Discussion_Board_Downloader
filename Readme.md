# D2L Discussion Board Downloader
This tool helps you download all attachment files from a D2L discussion board and save them to your computer such that each file name begins with the last name of the submitter.
Note: D2L stands for Brightspace Desire2Learn LMS software.

The tool was made by Dr. Mohammad Keyhani at the Haskayne School of Business, University of Calgary to automate the process of downloading attachments submitted by students on D2L discussion boards. The code was written with help from ChatGPT.

The easy-to-use exe file can be downloaded at https://tinyurl.com/D2LDownloader

## Requirements For Executable (exe file)
- Windows OS
- Chrome browser
- Latest version of chromedriver installed from: https://chromedriver.chromium.org/downloads

## Requirements for Python Script (py file)
- Windows OS
- Chrome browser
- Python 3.x
- [Selenium WebDriver for Chrome](https://chromedriver.chromium.org/downloads) (Ensure you have the correct version matching your Chrome browser)
- [Selenium](https://selenium-python.readthedocs.io/installation.html) (`pip install selenium`)


## Installation
D2L_Discussion_Board_Downloader.exe can be downloaded and used without installation. Or python script can be run in your local environment:
1. Ensure you have Python 3.x installed on your system.
2. Download the [Selenium WebDriver for Chrome](https://chromedriver.chromium.org/downloads) and place it in your system PATH or in the same directory as the script.
3. Install the Selenium package using pip: pip install selenium
4. Download the `D2L_Discussion_Board_Downloader1.0.py` script from this repository.

## Usage
The tool is self explanatory and asks you for the information it needs: the URL of the D2L discussion board you want to target, and the folder to download files. After inputs are provided, the tool will ask you to log in to D2L. This tool is completely private, fully runs on your local computer, and does not store or send information anywhere else.

## Contributing
Feel free to do what you want with the code, this is not intended to be a collaborative or constantly maintained project.

## License
This project is open-source and available under the MIT license.
