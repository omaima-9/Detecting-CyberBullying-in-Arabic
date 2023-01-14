import re
from arabert.preprocess import ArabertPreprocessor
model_name = "aubmindlab/bert-base-arabertv2"

arabert_prep = ArabertPreprocessor(model_name=model_name,
                                   remove_html_markup=False,
                                   replace_urls_emails_mentions=False,
                                   strip_tashkeel=True,
                                   strip_tatweel=True,
                                   insert_white_spaces=False,
                                   remove_non_digit_repetition=False,
                                   replace_slash_with_dash=None,
                                   map_hindi_numbers_to_arabic=True,
                                   apply_farasa_segmentation=None
                                   )


def remove_prefix(text):
    prefix_list = [
        'ال',
        'و',
        'ف',
        'ب',
        'ك',
        'ل',
        'لل',
        'ه',
        'ها',
        'ك',
        'ي',
        'هما',
        'كما',
        'نا',
        'كم',
        'هم',
        'هن',
        'كن',
        'ا',
        'ان',
        'ين',
        'ون',
        'وا',
        'ات',
        'ت',
        'ن',
        'ة',
        'س']

    words = text.split()
    needed_words = []
    for w in words:
        if w not in (prefix_list):
            needed_words.append(w)
    filtered_sentence = ' '.join(needed_words)
    return filtered_sentence


def remove_emoji(text):
    emoji_pattern = re.compile('['
                               u'\U0001F600-\U0001F64F'  # emoticons
                               u'\U0001F300-\U0001F5FF'  # symbols & pictographs
                               u'\U0001F680-\U0001F6FF'  # transport & map symbols
                               u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
                               u'\U00002702-\U000027B0'
                               u'\U000024C2-\U0010FFFF'  # wider range
                               ']+', flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def Pre_processing(comment):
    pat1 = '@[^ ]+'  # Remove mentions
    pat2 = '#'      #
    pat3 = '[0-9]'  # remove Number
    pat4 = '[A-Za-z]'  # remove english charctares
    combined_pat = '|'.join((pat1, pat2, pat3, pat4))
    comment = re.sub(combined_pat, '', comment)
    comment = re.sub('[ى]', 'ي', comment)
    comment = re.sub('[إأٱآا]', 'ا', comment)
    comment = re.sub('[ؤئ]', 'ء', comment)
    comment = re.sub('[ة]', 'ه', comment)
    comment = re.sub('[\n]', ' ', comment)
    comment = re.sub('[%s]' % re.escape(
        """!"#$%&'()*+,،-./:;<=>؟?@[\]^_`{|}~"""), '', comment)  # remove punctuation
    comment = re.sub(r'(.)\1+', r'\1\1',
                     comment)  # remove repeated char like هههه
    comment = remove_emoji(comment)

    comment = arabert_prep.preprocess(comment)
    comment = re.sub('[+]', '', comment)
    comment = remove_prefix(comment)

    return comment


Pre_processing(
    " 😂😂😆😆 🐄🐄😛😛 استغفر الله لا مـــــــــغنيه ولا ممثلة البقرة مفيدة اكثر منها هههههههههههههههه ")
