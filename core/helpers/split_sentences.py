import re 

def split_sentences(text):
    sent = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)',text)
    sent = [x for x in sent if len(x.strip()) > 0]
    return sent
