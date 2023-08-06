import unittest,simplejson
from InCli.SFAPI import restClient,query,Sobjects,utils


class Test_Objects(unittest.TestCase):

    def test_objects(self):
        restClient.init('NOSQSM')
        
        res = Sobjects.get_with_only_id('a3m3O000000KCjCQAW')

        print()     
    def test_limits(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0/limits'
        res = restClient.callAPI(action)

        print()


    def test_id(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0'
        res = restClient.callAPI(action)

        print()

    def test_id(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0'
        res = restClient.callAPI(action)
        for key in res.keys():
            print()
            action = res[key]
            res1 = restClient.callAPI(action)
            print(action)
            print(res1)

        print()

    def getAttributes(self,product):
        attr_str = product['vlocity_cmt__AttributeMetadata__c']
        if attr_str == None: return None
        atributes = simplejson.loads(attr_str)

        atts = []
        for atribute in atributes['records']:
            for productAttribute in atribute['productAttributes']['records']:
                att = {
                    'att':atribute['Code__c'],
                    'pAtt':productAttribute['code'],
                    'type':productAttribute['inputType'],
                    'len':len(productAttribute['values'])
                }
                atts.append(att)
            #    print(f"{atribute['Code__c']}  {productAttribute['code']} {productAttribute['inputType']}  {len(productAttribute['values'])}")
        
        utils.printFormated(atts)

        return atts
    def getChildProducts(self,product):
        children = []
        childItems = query.queryRecords(f"select fields(all) from vlocity_cmt__ProductChildItem__c where vlocity_cmt__ParentProductId__c='{product['Id']}' and vlocity_cmt__IsOverride__c = False limit 200")
        if len(childItems) == 0:
            return None

        for childItem in childItems:
            if childItem['vlocity_cmt__ChildProductId__c'] == None:
                continue
            prd = Sobjects.getF('Product2',f"Id:{childItem['vlocity_cmt__ChildProductId__c']}")['records'][0]
            print(prd['Name'])

            child = {
                'Name':childItem['vlocity_cmt__ChildProductName__c'],
                'virtual':childItem['vlocity_cmt__IsVirtualItem__c'],
                'Id':childItem['vlocity_cmt__ChildProductId__c'],
                'attributes':self.getAttributes(prd),
                'children':self.getChildProducts(prd)
            }
            children.append(child)
            print(childItem['vlocity_cmt__ChildProductName__c'])

        return children

    def test_getF(self):
        restClient.init('NOSDEV')

     #   res = Sobjects.getF('Product2',"ProductCode:CLASS_VOICE_MOBILE_SERVICE")

        promo = Sobjects.getF('vlocity_cmt__Promotion__c',"vlocity_cmt__Code__c:PROMO_WOO_FIXED_INTERNET_MOBILE_12_MONTHS_008")

        promoItems = query.queryRecords(f"select fields(all) from vlocity_cmt__PromotionItem__c where vlocity_cmt__PromotionId__c='{promo['records'][0]['Id']}' limit 200")
        for promoItem in promoItems:
            prods = Sobjects.getF('Product2',f"Id:{promoItem['vlocity_cmt__ProductId__c']}")
            for prod in prods['records']:
                print(prod['Name'])
       #         self.getAttributes(prod)

                self.getChildProducts(prod)

                childItems = query.queryRecords(f"select fields(all) from vlocity_cmt__ProductChildItem__c where vlocity_cmt__ParentProductId__c='{prod['Id']}' limit 200")
                for childItem in childItems:
                    print(childItem['vlocity_cmt__ChildProductName__c'])
            print()
        print()

