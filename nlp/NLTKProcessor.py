from bs4 import BeautifulSoup
from rake_nltk import Rake
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize


def extract_key_phrases_from_text(TextIn):
    soup = BeautifulSoup(TextIn,"html.parser")
    htmlFreeText = soup.get_text()
    htmlFreeText.replace("-", "")
    htmlFreeText = htmlFreeText.strip()
    r = Rake()
    r.extract_keywords_from_text(htmlFreeText)
    final = []
    for pair in r.rank_list:
        newDic = {}
        newDic["Affinty"] = pair[0]
        newDic["Text"] = pair[1]
        final.append(newDic)

    return final


def read_article(Text):
    text_in = Text.split('. ')
    sentences = []
    for x in text_in:
        sentences.append(x.replace("[^a-zA-Z]", " ").split(" "))
    return sentences


def _create_frequency_table(text_string) -> dict:
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable


def _score_sentences(sentences, freqTable) -> dict:
    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]]  # word_count_in_sentence

    return sentenceValue


def _find_average_score(sentenceValue) -> int:
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue))

    return average


def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence_count > 3:
            break
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary


# https://becominghuman.ai/text-summarization-in-5-steps-using-nltk-65b21e352b65
def generate_summary(textIn):
    soup = BeautifulSoup(textIn,"html.parser")
    textIn = soup.get_text()
    textIn = textIn.replace("-", "")
    textIn = textIn.strip()
    # 1 Create the word frequency table
    freq_table = _create_frequency_table(textIn)
    # print(freq_table)
    # 2 Tokenize the sentences
    sentences = sent_tokenize(textIn)
    # print(sentences)
    # 3 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(sentences, freq_table)
    # print(sentence_scores)
    # 4 Find the threshold
    threshold = _find_average_score(sentence_scores)
    # print(threshold)
    # 5 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, 1.2 * threshold)
    if len(summary) == 0:
        summary = sentences[0]

    return summary

