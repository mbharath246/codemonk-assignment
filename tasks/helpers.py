import uuid

stop_words = {"needn't", 'hadn', 'here', 'can', 'shan', 'are', 'm', 'didn', 'our', 'wouldn', 'they', 'o', 'same', 'then', "hasn't", 'doing', 'my', "should've", 'against', 'an', 'when', 'if', "couldn't", 'its', 'any', 'at', 'hasn', "isn't", "wasn't", 'be', 'into', 'you', 'of', 'about', 'do', 'other', 'only', 'whom', 'doesn', 'to', 'as', 'won', "hadn't", 'isn', 'each', 'will', 'for', 'was', 'more', 'yourselves', 'before', 'had', 'than', 'or', 'nor', 'during', 'through', 'aren', 'that', "you're", "you'll", 'how', 'she', "you've", "you'd", 'after', 'been', 'too', "doesn't", "weren't", 'so', 't', "mightn't", 'this', 'needn', 'because', 'over', 'we', 'such', 'does', 'the', 'up', 'off', 'all', 'ma', 'again', "shouldn't", 'your', 'no', 're', 'haven', 's', 'while', 'in', 'themselves', 'his', 'herself', 'mustn', 'should', 'it', 'their', "didn't", 'from', "mustn't", 'him', 'under', 'those', "it's", 'a', 'once', 'll', 'has', 'having', 'ourselves', 'now', 'her', 'very', 'above', "she's", 'on', 'am', 've', 'few', "shan't", 'down', "don't", 'them', 'yours', 'yourself', 'did', 'with', 'until', 'not', 'y', 'himself', 'me', 'have', 'and', 'there', 'why', 'itself', "won't", 'd', 'both', "haven't", 'these', 'between', 'were', 'what', 'just', "wouldn't", 'couldn', 'ours', 'myself', "aren't", 'mightn', 'he', 'own', 'where', 'don', 'who', 'by', 'hers', 'further', 'wasn', 'weren', 'being', 'shouldn', 'theirs', 'ain', 'which', 'some', 'out', 'below', 'is', 'i', 'most', "that'll", 'but'}


def split_paras(text: str):
    paras = []
    for i in text.strip().split('\n\n'):
        paras.append(i.replace('\n',''))
    return paras


def remove_duplicates(array: list):
    return list(set(array))


def tokenized_words(text:str):
    paras = split_paras(text)
    indexed_words = {}
    each_para = {}
    for para in paras:
        para_id = uuid.uuid4()
        each_para[para_id] = para   
        words = remove_duplicates(para.split())
        add_dict = {}
        filtered_words = [word for word in words if word not in stop_words]
        for idx,word in enumerate(filtered_words):
            add_dict[word] = idx
        indexed_words[para_id] = [dict(sorted(add_dict.items(), key=lambda add_dict:add_dict[1]))]

    return each_para, indexed_words

