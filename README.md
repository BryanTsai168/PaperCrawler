>This program accesses information from the arXiv website, which is owned by Cornell
>University (Educational Corporation; NEW YORK, USA).

>All papers are owned by their respective authors.

>This program is solely for the purpose of web scraping and does not engage in any
>copyright infringement.




## 1. Quick to use

**Install Dependencies**
```bash
pip install -r requirements.txt
```

**Change prompt and Api_key**
```bash
#You must input your API_KEY to use this script. Additionally, the default PROMPT is set to Chinese. If you need another language, please modify it accordingly.
#API_Key (line: 72)
client = OpenAI(api_key = "Your gpt api key")
#Prompt (line: 75)
gpt_input = f'type your prompt' + +str(paper_group)
```

**Execute main.py**
```bash
python main.py
```

## 2. Introduce
- The script mainly serves two purposes: firstly, it swiftly fetches today's computer science papers, and secondly, it feeds each of today's papers into GPT for summarization on a per-article basis. Additionally, option 1 allows setting a different date, with today being the default.

- After the text is processed by GPT, it will first generate a file named gpt_output.txt in the t_output folder in the same directory. Then it will be converted into a DOCX file. You can further convert it to formats like PDF.





