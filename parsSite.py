
import json
def ctlpars(HTML):
    #f = open("message1.txt","r",encoding="utf-8")
    text = HTML
    fl = {"answer":[]}
    res = [i for i in range(len(text)) if text.startswith("data-meta-product-id", i)]
    for i in res[0:10]:
        j = text.find("/product", i)
        strt = j
        end = text.find('"', strt+1)
        link = "https://www.citilink.ru/"+text[strt:end-1]
        strt = text.find('title=', end)+7
        end = text.find('"', strt+1)
        name = text[strt:end]
        strt = text.find("data-meta-price",end)+17
        end = text.find('"', strt+1)
        price = text[strt:end]
        fl["answer"].append({"name":name, "link":link, "price":price})

    return(fl)

def ozonpars(HTML):
    return(0)
def pritserupars(HTML):
    return (0)