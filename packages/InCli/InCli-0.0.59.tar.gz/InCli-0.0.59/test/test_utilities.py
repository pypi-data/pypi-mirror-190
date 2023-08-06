import unittest
from InCli.SFAPI import restClient,query,Sobjects


class Test_Utilities(unittest.TestCase):
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
    
    def test_delete_logs(self):
        restClient.init('DTI')

        q = "select Id from ApexLog where Operation='/vlocity_cmt/v3/catalogs/DC_CAT_WOO_MOBILE/basket' "
        res = query.query(q)

        id_list = [record['Id'] for record in res['records']]
        
        Sobjects.deleteMultiple('ApexLog',id_list)
        print()

