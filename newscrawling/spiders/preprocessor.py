import re
import string

def preprocessing(text, writer=None, press=None):
    '''
    뉴스기사 전처리 함수입니다.
    writer = 기자명
    press = 언론사
    '''
    # 숫자, 소숫점 제거
    text = re.sub('\d+\.\d*', '',text)

    # 이메일, URl 제거
    text = re.sub("([a-zA-Z0-9-]+(\@|\.)[a-zA-Z0-9-.]+)", '', text)
    # 다수의 점 (ex : ...) 점 한개로 대체
    text = re.sub("\.+\.", '.', text)
    # 다수의 공백 축소
    text = re.sub(' +', ' ', text)

    reporter_pattern = re.compile(r"([가-힣]{2,5} 기자)|([가-힣]{2,5}기자)")
    reporter_pattern.sub('', text)

    symbols = string.punctuation.replace(".", "").replace("?", "").replace("!", "") + "·ㆍ■◆△▷▶▼�""''…※↑↓▲☞ⓒ⅔"
    text = text.translate(str.maketrans("", "", symbols))

    # 불용어
    if writer:
        text = text.replace(writer, '')
    if press:
        text = text.replace(press, '')

    text = text.replace('Copyrights', '').replace('무단 전재 및 재배포 금지', '')

    return text

