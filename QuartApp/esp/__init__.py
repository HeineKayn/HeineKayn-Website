from .mail import getMails
    
def getESPDic():
    dic = {}

    nbMails,nbMailsPrio = getMails()
    dic["nbMails"] = nbMails
    dic["nbMailsPrio"] = nbMailsPrio

    # dic = {
    #     "info1" : 2,
    #     "info2" : 3,
    #     "info3" : {"aaa":"bbb","ccc":2}
    # }
    return dic 