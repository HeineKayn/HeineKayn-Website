import random

class Chart():

    def __init__(self,colorKey):

        self.colorList = {
            "dureeVue" : ['rgba(253, 216, 190,{})', 'rgba(227, 175, 177,{})', 'rgba(153, 119, 135,{})'],
            "expoRes"  : ['rgba(225, 221, 191,{})','rgba(4, 37, 58,{})', 'rgba(76, 131, 122,{})'],
            "other"    : ['rgba(191, 174, 156,{})', 'rgba(193, 221, 224,{})', 'rgba(179, 138, 123,{})'],
            "expoTime" : [  'rgba(255, 239, 66,{})', # jaune 
                            'rgba(228, 164, 60,{})', # orange 
                            'rgba(211, 110, 52,{})', # rouge 
                            'rgba(201, 35, 47,{})', # pourpre 
                            'rgba(198, 13, 135,{})', # magenta 
                            'rgba(122, 47, 137,{})', # violet  
                            'rgba(51, 55, 140,{})', # bleu 
                            'rgba(47, 81, 156,{})', # outremer 
                            'rgba(33, 172, 233,{})', # cyan 
                            'rgba(47, 167, 155,{})', # turquoise 
                            'rgba(61, 162, 89,{})', # vert 
                            'rgba(160, 196, 85, {})', # chartreuse
                        ]
        }
        self.colors = self.colorList[colorKey]

        # self.colorList = [
        #     'rgba(255, 239, 66,{})', # jaune 
        #     'rgba(228, 164, 60,{})', # orange 
        #     'rgba(211, 110, 52,{})', # rouge 
        #     'rgba(201, 35, 47,{})', # pourpre 
        #     'rgba(198, 13, 135,{})', # magenta 
        #     'rgba(122, 47, 137,{})', # violet  
        #     'rgba(51, 55, 140,{})', # bleu 
        #     'rgba(47, 81, 156,{})', # outremer 
        #     'rgba(33, 172, 233,{})', # cyan 
        #     'rgba(47, 167, 155,{})', # turquoise 
        #     'rgba(61, 162, 89,{})', # vert 
        #     'rgba(160, 196, 85, {})', # chartreuse
        # ]
        # self.colorList.reverse()

    def pickColor(self):
        return self.colors.pop()