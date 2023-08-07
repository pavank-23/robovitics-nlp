import spacy
import requests
import re
from bs4 import BeautifulSoup
import sys
import google.generativeai as palm

palm.configure(api_key='')
nlp = spacy.load("en_core_web_sm")

print("1.Enter link for glossary extraction. (arXiv)\n2.Enter text for glossary extraction")
choice = int(input("Enter choice: "))

if choice == 1:
    link = input("Enter link: ")
    response = requests.get(link)
    doc = nlp(response.text)
    soup = BeautifulSoup(response.content, "html.parser")
    ab_list = str(soup.find("blockquote", class_="abstract mathjax").prettify()).split("\n")
    abstract = " ".join(ab_list[ab_list.index(" </span>"):ab_list.index("</blockquote>")])
    doc = nlp(abstract)
elif choice == 2:
    doc = nlp(input())
else:
	sys.exit()

abbr_expr = r"\b[A-Z]+\b"
term_expr = r"\b(?:[A-Z][A-Za-z0-9_]*\s+)+[A-Z][A-Za-z0-9_]*\b"

entities = set()

for match in re.finditer(abbr_expr, doc.text):
    start, end = match.span()
    span = doc.char_span(start, end)
    if span is not None and len(span.text)>1:
        entities.add(span.text)

for match in re.finditer(term_expr, doc.text):
    start, end = match.span()
    span = doc.char_span(start, end)
    if span is not None and len(span.text)>1:
        entities.add(span.text)

ent = list(entities)

while (True):
	print("1.Summary\n2.Exit")
	ch = int(input("Enter choice: "))
	counter = 0
	if ch == 1:
		for i in ent:
			print(counter,".",i)
			counter += 1
		choice = int(input("Enter term to search: "))
		response = palm.generate_text(prompt="Summarize {enx} in 500 words.".format(enx=ent[choice]))
		print(response.result)
	else:
		break