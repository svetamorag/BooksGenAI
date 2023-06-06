import pdfkit
import generateImage,generateStory
import base64

#options for wkhtmltopdf    
options = {
    "enable-local-file-access":None,
    'page-size': 'A4',
    'margin-top': '0',
    'margin-right': '0',
    'margin-bottom': '0',
    'margin-left': '0',
    'encoding': "UTF-8",
    'orientation':"Landscape",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    'no-outline': None,
}

def split_paragraphs(text):
    paragraphs = []
    for paragraph in text.split("\n\n"):
        paragraphs.append(paragraph)
    return paragraphs

def createBook(text):
    paragraphs = split_paragraphs(text)
    print(len(paragraphs))
    pageNum=0
    pHtml=""
    for paragraph in paragraphs:
        pageNum=pageNum+1
        
        prompt=input("Please enter the prompt for the following paragraph: " + paragraph +":\n")
        generateImage.generateImageFromPrompt(prompt+",colorful,pastele colors,3d animation",pageNum)
       
        pHtml+="<div class='text'>"+paragraph+"</div>"
        pHtml+="<img src='pagen"+str(pageNum)+".jpg'></img>"
        pHtml+="<p style='page-break-before: always;'></p>"
        
    html_code = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>The Book</title>
        <style>
        body
        {
            background-color:#ffffff;
            background-image:url("BookBG.png");
            background-repeat:repeat-y;
            background-size:contain;
        }
        .text {
            width: 35%;
            float: right;
            font-size: 26pt;
            font-family: Google-Sans;
            margin-right:100px;
            margin-top:250px;
            padding:20px;
            color:#246536;
        }
         img{
            width: 40%;
            border: 40px solid #EDD184;
            margin-top:150px;
            margin-left:80px;
        }
        </style>
        </head>
        <body>"""
    html_code+=pHtml
    html_code+=""" </body>
        </html>
        """
    with open("testBook.html", "w") as f:
        f.write(html_code)
    pdfkit.from_file('testBook.html','theBook.pdf',options=options)
     
def createBookFromScratch():
    text=generateStory.generateStory()
    createBook(text)
    
#use this function to recreate PDF from local HTML file
def createPDFfromHTML(): 
     pdfkit.from_file('testBook.html','theBook.pdf',options=options)


createBookFromScratch()
