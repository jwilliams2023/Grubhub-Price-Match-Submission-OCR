This is a Grubhub price match guarantee website automation. It decreases the time needed to submit your proof of a lower-price cart found elsewhere.

When you run this script it will look this this:

![](https://github.com/jwilliams2023/Grubhub-Price-Match-Submission-OCR/blob/master/Resources/DemoVideo.gif)

*A note for this gif is that at the end I manually submitted the image proof but there is a line of code that just has to be uncommented to auto-submit. I personally keep it commented out since I want to be 100% sure everything is accurate.*

There are a couple of modules/libraries needed. Mainly selenium and the chromewebdriver (since I use chrome) and the Python modules tesseract OCR and pyautogui.

selenium documentation - https://www.selenium.dev/documentation/overview/ 

chrome webdriver - https://chromedriver.chromium.org/downloads 

tesseract - https://github.com/UB-Mannheim/tesseract/wiki

SETUP:

The path for the download directory where the image of your cart will be stored needs to be setup. Then set up the path for the tesseract.exe.as show here:

![image](https://github.com/jwilliams2023/Grubhub-Price-Match-Submission-OCR/assets/130696072/cbff4012-b5f9-4e9b-87e3-4701d7b24886)

Next, the Chromewebdriver download needs to be specified in its location. I have also personalized this script to specifically open my signed-in Chrome and not a default instance by specifiy my chrome user data so i can be auto signed in for grubhub as show here: 

![image](https://github.com/jwilliams2023/Grubhub-Price-Match-Submission-OCR/assets/130696072/76592c96-b188-4037-b798-77fd646ec622)
