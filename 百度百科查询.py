import urllib.request
import urllib.parse
import re 
from bs4 import BeautifulSoup

def test_url(soup):
    result = soup.find(text=re.compile("百度百科尚未收录词条"))
    if result:
        print(result[0:-1]) # 百度这个在最后加了个“符号，给它去掉
        return False
    else:
        return True

def summary(soup):
    word = soup.h1.text
    # 如果存在副标题，一起打印
    if soup.h2:
        word += soup.h2.text
    # 打印标题
    print(word)
    # 打印简介
    if soup.find(class_="lemma-summary"):
        print(soup.find(class_="lemma-summary").text)   

def get_urls(soup):
    for each in soup.find_all(href=re.compile("view")):
        content = ''.join([each.text])
        url2 = ''.join(["http://baike.baidu.com", each["href"]])
        response2 = urllib.request.urlopen(url2)
        html2 = response2.read()
        soup2 = BeautifulSoup(html2, "html.parser")
        if soup2.h2:
            content = ''.join([content, soup2.h2.text])
        content = ''.join([content, " -> ", url2])
        yield content
        

def main():
    word = input("请输入关键词：")
    keyword = urllib.parse.urlencode({"word":word})
    response = urllib.request.urlopen("http://baike.baidu.com/search/word?%s" % keyword)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    if test_url(soup):
        summary(soup)
        
        print("下边打印相关链接：")
        each = get_urls(soup)
        while True:
            try:
                for i in range(10):
                    print(next(each))
            except StopIteration:
                break
            
            command = input("输入任意字符将继续打印，q退出程序：")
            if command == 'q':
                break
            else:
                continue
    
if __name__ == "__main__":
    main()
