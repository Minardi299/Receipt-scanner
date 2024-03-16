# imgToText
An OCR tool using Tesseract 4.1.1 with the pytesseract librabry to read an image and OpenCV to pre process and prepare the image for better OCR results. Currently implementing a local host LLm model mixtral through langchain to further cross check and enhance the accuracy of the OCR result

The program will check the TODO folder to check if there's any image to convert, if there is, it will use tesseract to read words from an image of a receipt and will return a JSON object with the help of a LLM model.

To download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki

To process and improve read quality: https://github.com/tesseract-ocr/tessdoc/blob/main/ImproveQuality.md

# EXAMPLE
From ![alt text](TestingImgs/test1.jpeg) To ![alt text](temp/NANORemoveNoise.jpg)
The digitized result:

{
"name": "Main Street Restaurant",
"location": "6332 Business Drive Suite 528, Palo Alto California 94301",
"cardType": "Discover",
"amount": "29.01"
}
From ![alt text](temp/image.png) To ![alt text](temp/image.jpg)
The digitized result:
{
"name": "Marche C&T",
"location": "8200 Boul Taschereau #1300, Brossard QC J4X 256",
"cardType": "MasterCard",
"amount": "39.63"
}
# LLM model
The model being used is a Mixtral-8x7B that's on the local network, bound to port 11434 and can be access via a curl 
![alt text](temp/postman_example.png) 
or in this case through OpenAI api and its library with python.
Example of api being call:
![alt text](temp/image-1.png)