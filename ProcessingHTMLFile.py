import urllib.request 
import requests
# Importing BeautifulSoup and 
# it is in the bs4 module
from bs4 import BeautifulSoup

from azure.ai.textanalytics import ExtractSummaryAction
import math

from re import split
from nltk.tokenize import sent_tokenize, word_tokenize

#Azure text analyticscomm
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


# Opening the html file. If the file
# is present in different location, 
# exact location need to be mentioned
HTMLFileToBeOpened = open("EX-10.7.html", "r")
  
# Reading the file and storing in a variable
contents = HTMLFileToBeOpened.read()
  
# Creating a BeautifulSoup object and
# specifying the parser 
beautifulSoupText = BeautifulSoup(contents, 'html.parser')

# To find data in the html file 
# for i in body:
#     paragraphContainer = i.find("p")
#     if paragraphContainer:
#         print(paragraphContainer)
#     else:
#         print("none")

tables = beautifulSoupText.find_all("table")

finaltables = []

for table in tables:
    table_str = str(table)
    if "<tr>" in table_str:
        row_count = table_str.count("<tr>")
        if row_count > 1:
            finaltables.append(table)

Html_file= open("testfinaltables.html","w")
Html_file.write(str(finaltables))
Html_file.close()

finaltextlist = []
beautifulSoupString = str(beautifulSoupText)
for t in finaltables:
    if str(t) in beautifulSoupString:
        beautifulSoupString  = beautifulSoupString .replace(str(t),"")
finaltextlist.append(beautifulSoupString)

#Conversion back to BS4
beautifulSoupString = BeautifulSoup(finaltextlist[0], 'html.parser')


#print(finaltables)
#get text from the BeautifulSoup page
dirtydocument = beautifulSoupString.get_text()
document = dirtydocument.replace(u"\xa0", u" ")
document = document.replace(u"\n", u" ")

Tokenised_Document = sent_tokenize(document)
NoOfSentences = len(Tokenised_Document)

#find the total number of characters in the document
lengthDoc = len(document)

#define count for loop
count = 0 

#find the number of chunks by dividing number of characters by our character 'soft cap'
NoOfChunks = math.ceil(lengthDoc/4000)

#find the number of sentences that can fit in a single chunk
x = math.ceil(NoOfSentences/NoOfChunks)


ChunkyList = []
#while loop to extract individual sentences
while count < NoOfSentences:
    Chunk = ""
    #extract paragraphs into list with full sentences
    try:
        paralist = Tokenised_Document[count:count + x]
    except:
        paralist = Tokenised_Document[count:-1]
    
    #loop through paragraph list and merge sentences into paragraph in string for instead of in list form
    for i in range(0,len(paralist),2):
        try:
            mergedString = paralist[i] + paralist[i+1]
        except:
            try:
                mergedString = paralist[i]
            except:
                mergedString = paralist[i-1]
            
        count = count + 2
        Chunk += mergedString
    ChunkyList.append(Chunk)



#API key & Endpoint

key =  "402c49b73698483bba747edd53909e9f"
endpoint = "https://txtanalytics12345.cognitiveservices.azure.com/"

# Authenticating Client
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Key Phrase Extraction
def key_phrase_extraction_example(client,sentence):
    try:
        documents = []
        documents.append(sentence)
        response = client.extract_key_phrases(documents = documents)[0] # must be only one string; must iterate through list of strings

        if not response.is_error:
            print("\n")
            print("\tKey Phrases:")
            for phrase in response.key_phrases:
                print("\t\t", phrase)
        else:
            print(response.id, response.error)

    except Exception as err:
        print("Encountered exception. {}".format(err))

def sample_extractive_summarization(client,paragraph):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient
    from azure.ai.textanalytics import ExtractSummaryAction
    

    document = []
    document.append(paragraph)

    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractSummaryAction(MaxSentenceCount=4)
        ],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            print("...Is an error with code '{}' and message '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
            
        else:
            print("Summary extracted: \n{}".format(
                " ".join([sentence.text for sentence in extract_summary_result.sentences]))
            )
            print("/n")

for paragraphs in ChunkyList:
    sample_extractive_summarization(client,paragraphs)


# for paragraphs in ChunkyList:
#     key_phrase_extraction_example(client,paragraphs)



