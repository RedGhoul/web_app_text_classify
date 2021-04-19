from bs4 import BeautifulSoup
from rake_nltk import Rake
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from summarizer import Summarizer
import gc



'''
https://github.com/cjhutto/vaderSentiment
The compound score is computed by summing the valence scores of each word in the lexicon, adjusted according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive). This is the most useful metric if you want a single unidimensional measure of sentiment for a given sentence. Calling it a 'normalized, weighted composite score' is accurate.

It is also useful for researchers who would like to set standardized thresholds for classifying sentences as either positive, neutral, or negative. Typical threshold values (used in the literature cited on this page) are:

positive sentiment: compound score >= 0.05
neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
negative sentiment: compound score <= -0.05
NOTE: The compound score is the one most commonly used for sentiment analysis by most researchers, including the authors.

The pos, neu, and neg scores are ratios for proportions of text that fall in each category 
(so these should all add up to be 1... or close to it with float operation). These are the most useful metrics if you want to analyze the context & presentation of how sentiment is conveyed or embedded in rhetoric for a given sentence. For example, different writing styles may embed strongly positive or negative sentiment within varying proportions of neutral text -- i.e., some writing styles may reflect a penchant for strongly flavored rhetoric, whereas other styles may use a great deal of neutral text while still conveying a similar overall (compound) sentiment. As another example: researchers analyzing information presentation in journalistic or editorical news might desire to establish whether the proportions of text (associated with a topic or named entity, for example) are balanced with similar amounts of positively and negatively framed text versus being "biased" towards one polarity or the other for the topic/entity.
IMPORTANTLY: these proportions represent the "raw categorization" of each lexical item 
(e.g., words, emoticons/emojis, or initialisms) into positve, negative, or neutral classes; they do not account for the VADER rule-based enhancements such as word-order sensitivity for sentiment-laden multi-word phrases, degree modifiers, word-shape amplifiers, punctuation amplifiers, negation polarity switches, or contrastive conjunction sensitivity.

'''
def extract_sentiment(TextIn):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(TextIn)
    gc.collect()
    return vs



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

# https://pypi.org/project/bert-extractive-summarizer/
def extract_summary_from_text(TextIn, min_length=20):
    soup = BeautifulSoup(TextIn, "html.parser")
    html_free_text = soup.get_text()
    html_free_text.replace("-", "")
    html_free_text = html_free_text.strip()
    summary_model = Summarizer()
    result = summary_model(html_free_text, min_length=min_length)
    gc.collect()
    return result



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
    try:
        soup = BeautifulSoup(textIn, "html.parser")
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
    except:
        return "Error Occurred Could Not Parse"



