# NLPbrl Project        [![KingOfOrikid](https://circleci.com/gh/KingOfOrikid/proj_NLPbrl_DATA534.svg?style=shield)](https://app.circleci.com/pipelines/github/KingOfOrikid/proj_NLPbrl_DATA534?branch=main)
**Pypi**: **link**     
**Package demo video**: **link**            
            
## Group information          
- **Group name: Ctrl-Alt-Del**          
- **Group members: Yuxin Chen & Siyue Gao**           
                      
## Introduction              
Natural Language Processing(NLP) is an important direction in Computer Science and Artificial Intelligent domains. It studies theories and methods that enable effective communication between computers and humans using natural language. NLP can be used in many applications like Question&Answer System, Spam Email Program, Voice Assistants and Translate, etc. An advanced and completer NLP application usually can be divided into two parts: Natural Language Understanding(NLU) and Natural Language Generation(NLG), which two aspects can also be divided into many small tasks such as Tokenization, Syntax Parsing, and Text Mining. So when we need to work on some big applications, it is very complicated to begin with the basic tasks. At this time, the Rosette Text Analytics API will be extremely powerful because it can help user to achieve many underlying tasks of NLP which makes completing an application much easier and more efficient.                                         
The NLPbrl wrapper API is a package for wrapping The Rosette Text Analytics API's functions. It can use natural language processing, and machine learning to analyze unstructured and semi-structured text in multilingual. It can provide a large number of powerful text analyses which has largely helped people to learn about natural language processing and to develop various applications for processing text.                        
         
- **Word Frequency Counter (cal_frequency)**         
- **Word Frequency Visualization (word_viz)**          
- **TF-IDF (key_extra_tfidf)**               
- **Entity Similarity (cal_simi)**               
- **Text Rank (cal_textRank)** (to find keywords)         
- **Entity Relationship Visualization (relation_viz)**               
- **Text Classification (cal_classification)**                           

## Application of NLPbrl       
NLP is a branch of Artificial Intelligence. Using this usable NLP Library, NLP can finding variety of applications in a wide range of industries with many languages, such as **Deep Learning research**, **Developing chatbots**, **patient data processing**, **text mining**, **text classification**, **text analysis**, **sentiment analysis**, **word sequencing**, **speech recognition and synthesis**, **machine translation** are only a few of the major NLP tasks this package can help achieve
This Library makes text preprocessing easier, which is able to transform free text phrases into structured characteristics that can be readily fed into Machine Learning or Deep Learning pipelines.             
               
## Package Structure
```
NLPbrlpackage
|
| README.md
| LICENSE.md
| requirements.txt
└─── NLPbrl 
    | Data_.py
    └─── Data (class)
        | get_token: Text tokenization
        | get_lang: Recognition of text language
        | get_vec: Word/Sentence embedding
        | get_posTag: Part-of-Speech tagging
        | get_senTag: Sentence cutting
        | get_relation: Relation extraction
        | get_classification: Text categorization
    | NLP_.py
    └─── NLP (class)
        | cal_frequency: Word frequency counter
        | word_viz: Word frequency visualization
        | key_extra_tfidf: TF-IDF
        | cal_simi: Entity similarity
        | cal_textRank: Text Rank to find keywords
        | relation_viz: Entity Relationship Visualization
        | cal_classification: Text categorization
        | __word_wash: Remove stop-words from the text
        | __check_limit: Check if the text length exceeds the API limit
        | __check_limit_tool: Cut out of length text to text list
        | __cal_TF: Calculate TF
        | __cal_IDF: Calculate IDF
        | __cal_TFIDF: Calculate TF-IDF
        | __simi_cal_euc: Euclidean distance calculation
        | __simi_cal_cos: Cosine distance calculation
        | __simi_cal_jac: Jaccard similarity calculation
```

## How to use
Note that two API keys is required to run the functions in NLPbrl. The key can be acquired at https://developer.rosette.com/ and https://rapidapi.com/hub.

```python
from NLPbrl import NLP_
nlp = NLP_.NLP()
short_text_en = "simple test of calculate frequency."
long_text_en = "The goal of the package is to wrap into a set of R/Python functions a web REST API and offer a package for others to use those functions. The functions offered by the package should also take care of the minimum wrangling necessary to output the data in a viable format (that is, not as a raw binary file, unless a raw binary file is the most appropriate data format). You choose the API and the most appropriate input / output design of your functions. Think carefully of what part of the wrangling is of general interest (i.e., most or all of the users will want to perform it, and thus should be done in the package) and what part is only relevant as an example for the vignette (i.e., is too specific to be of general interest, and thus may just end up in the vignette.)"*20
tf_idf_corpus = ["The cat sat on my bed",
                 "The dog sat on my knees"]
tf_idf_text = "The dog sat on my knees"
simi_text1 = 'I am eating an apple'
simi_text2 = 'She is eating an apple'
rela_text = "FLIR Systems is headquartered in Oregon and produces thermal imaging, night vision, and infrared cameras and sensor systems.  According to the SEC’s order instituting a settled administrative proceeding, FLIR entered into a multi-million dollar contract to provide thermal binoculars to the Saudi government in November 2008.  Timms and Ramahi were the primary sales employees responsible for the contract, and also were involved in negotiations to sell FLIR’s security cameras to the same government officials.  At the time, Timms was the head of FLIR’s Middle East office in Dubai."
cate_text = "Sony Pictures is planning to shoot a good portion of the new \"Ghostbusters\" in Boston as well."
```

A simple example of using the cal_frequency() function in the package to obtain word frequency statistics for each word in the input text. Word frequency statistics can summarize the words that appear frequently in the document and help to understand the text quickly, and they are also the basis for many NLP analyses and processes.
![cal_frequency](imgs/cal_frequency.png)   

A simple example of using the word_viz() function in the package to visualisation of the word frequency statistics of the input text, including the visualisation of word clouds and word frequency line graphs, and the ability to select the number of words to be visualised.
![word_viz_code](imgs/word_viz_code.png)   
![word_viz_cloud](imgs/word_viz_cloud.png)    
![word_viz_chart](imgs/word_viz_chart.png)    

A simple example of using the key_extra_tfidf() function in the package to obtain the tf-idf score of words in the input text in the context of a corpus, the TF-IDF can be used to assess the degree of importance of a word for a document set or one of the documents in a corpus. The more often a word appears in a text, and the less often it appears in all documents, the more representative it is of that text.
![key_extra_tfidf](imgs/key_extra_tfidf.png)    

A simple example of using the cal_simi() function in the package to calculate the similarity between two entities, the function can choose whether to use word embedding or sentence embedding, and also whether to use euclidean distance, cosine distance or jaccard for the calculation.
![cal_simi](imgs/cal_simi.png)    

A simple example of using the cal_textRank() function in the package to get the top k keywords of the text by the textRank function.
![cal_textRank](imgs/cal_textRank.png)    

A simple example of using the relation_viz() function in the package to obtain and visualise the relationships between entities embedded in the text using a graph.
![relation_viz_code](imgs/relation_viz_code.png)    
![relation_viz_graph](imgs/relation_viz_graph.png)    

A simple example of using the c() function in the package to obtain the k classifications to which the text is most likely to belong, where the classifications are Arts & Entertainment, Travel, Business, Automotive, Education, Careers, Food & Drink and so on.
![cal_classification](imgs/cal_classification.png)   

## How to Contribute
Please note that this project is released with a [Contributor Code of
Conduct](https://github.com/KingOfOrikid/proj_NLPbrl_DATA534/blob/main/Code%20of%20Conduct.md).
By participating in this project you agree to abide by its terms.