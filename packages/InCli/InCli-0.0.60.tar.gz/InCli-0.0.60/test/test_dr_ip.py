import unittest,simplejson
from InCli import InCli
from InCli.SFAPI import file,DR_IP,restClient,query,utils,thread

class Test_DR_IP(unittest.TestCase):
    options = {
        "isDebug": True,
        "chainable": True,
        "resetCache": False,
        "ignoreCache": True,
        "queueableChainable": False,
        "useQueueableApexRemoting": False
    }     
    def test_IP(self):
        #restClient.init('DTI')
        restClient.init('NOSDEV')

        
        call = DR_IP.ip("custom_GetTrialPromos",input={},options=self.options)
        lc = restClient.lastCall()

        print()

    def test_IP_test(self):
        restClient.init('DTI')

        input = {
            "cartId": "8010Q0000035ec1QAA"
        }
        
        call = DR_IP.ip("unai_chainableIpsTest",input=input,options=self.options)


        print()

    key ='0c900b76-3947-b62a-1927-805a44bd1677'
    def test_attachment(self):
        restClient.init('DTI')

        q = f"select fields(all) from vlocity_cmt__DRBulkData__c where vlocity_cmt__GlobalKey__c = '{self.key}' limit 20"
        call0 = query.query(q)
        print(call0)
        
        q2 = f"select fields(all) from Attachment where ParentId ='{call0['records'][0]['Id']}' limit 10"
        call2 = query.query(q2)
        print(call2['records'][0]['Id'])
        attachmentId = call2['records'][0]['Id']
     #   attachmentId = '00P0Q00000JWEzGUAX'
        action = call2['records'][0]['Body']
        call = restClient.requestWithConnection(action=action)

        filepath = restClient.callSave("AttachementX123")

        print()

    def test_finish_call(self):
        restClient.init('DTI')
        input = "{}"

        options1 = self.options.copy()
        options1['vlcIPData'] = self.key

        call = DR_IP.ip("unai_chainableIpsTest",input=input,options=options1)

        print()

    def test_dr_bundle(self):
        restClient.init('DTI')

        q = "SELECT Name, Id, LastModifiedDate, LastModifiedBy.Name, CreatedDate, CreatedBy.Name, vlocity_cmt__Type__c, vlocity_cmt__InputType__c, vlocity_cmt__OutputType__c, vlocity_cmt__Description__c, LastModifiedById FROM vlocity_cmt__DRBundle__c USING SCOPE Everything WHERE vlocity_cmt__Type__c != 'Migration' AND  vlocity_cmt__Type__c != 'Export (Component)' ORDER BY Name"

        q = "SELECT Name, Id, LastModifiedDate, LastModifiedBy.Name, CreatedDate, CreatedBy.Name, vlocity_cmt__Type__c, vlocity_cmt__InputType__c, vlocity_cmt__OutputType__c, vlocity_cmt__Description__c, LastModifiedById FROM vlocity_cmt__DRBundle__c ORDER BY Name"

        res = query.query(q)
        
        out = []
        for record in res['records']:
            o = {
                "Name":record['Name'],
                "type":record['vlocity_cmt__Type__c']

            }
            out.append(o)
        utils.printFormated(out)
        print()

    def bestMach(self,sequence,ip_definitions):
        possible_ips = []

        for ip_definition in ip_definitions:
            score = 0

       #     print(ip_definition['steps'])
            for index in range(0,len(sequence)):
        #        print(sequence[index])
                if sequence[index] in ip_definition['steps']:
                    score = score + 1

            if score>0:
                ip = {
                    'name':ip_definition['vlocity_cmt__ProcedureKey__c'],
                    'score':score,
                    'ip_steps':len(ip_definition['steps']),
                    'size':len(sequence)
                }
                possible_ips.append(ip)
        return possible_ips
    def findMatch(self,sequence,ip_definitions):
        possible_ips = []

        for ip_definition in ip_definitions:
            if len(sequence) > len(ip_definition['steps']):  continue

            found = True
            for step in sequence:
                if step not in ip_definition['steps']: found = False
                if found== False:break
            if found: possible_ips.append( ip_definition['vlocity_cmt__ProcedureKey__c'])

        return possible_ips

    def test_find_stooped_VIPs_threaded(self):
        restClient.init('NOSQSM')

        q0 = f"select Id,vlocity_cmt__GlobalKey__c from  vlocity_cmt__DRBulkData__c where vlocity_cmt__DRBundleName__c = 'None Specified' and vlocity_cmt__AsyncApexJobId__c = null and vlocity_cmt__GlobalKey__c != null"
        bulk_data_records = query.query(q0)

        q = f"select ID,Body,ParentId,LastModifiedDate from Attachment where ParentId in (select Id from  vlocity_cmt__DRBulkData__c where vlocity_cmt__DRBundleName__c = 'None Specified' and vlocity_cmt__AsyncApexJobId__c = null and vlocity_cmt__GlobalKey__c != null)"

        attachments = query.query_base64(q)

      #  attachments['records'] = attachments['records'][:50]
        for attachment in attachments['records']:
            attachment['vlocity_cmt__GlobalKey__c'] = [bdr['vlocity_cmt__GlobalKey__c'] for bdr in bulk_data_records['records'] if bdr['Id']==attachment['ParentId']][0]

        ip_definitions = self.get_IP_definitions()

        ip_definitions_woo = [ip_definition for ip_definition in ip_definitions if ip_definition['vlocity_cmt__ProcedureKey__c'].startswith('woo_')]

        for ip_definition_woo in ip_definitions_woo:
            ip_definition_woo['steps'] = set(ip_definition_woo['steps'])

        result = []

        def do_work(attachment):
            attachment['log'] = restClient.requestWithConnection(action=attachment['Body'])
            return attachment

        def on_done(attachment,result):
            log = attachment['log']
            if 'vlcDebug' in log:
                sequence = log['vlcDebug']['executionSequence']
                possible_ips =self.findMatch(sequence,ip_definitions_woo)
                if len(possible_ips) >0:  attachment['possible'] = possible_ips
                else: attachment['best_match'] = self.bestMach(sequence,ip_definitions)
                result.append(attachment)

        thread.execute_threaded(attachments['records'],result,do_work,on_done,threads=15)

        found = [attachment for attachment in attachments['records'] if 'possible' in attachment]

        newlist = sorted(found, key=lambda d: d['LastModifiedDate']) 

        utils.printFormated(newlist,"LastModifiedDate:Id:ParentId:vlocity_cmt__GlobalKey__c:possible",rename='ParentId%DRBulkData_Id:Id%Attachment_Id')


    def test_find_stooped_VIPs(self):
        restClient.init('NOSQSM')

        q0 = f"select Id,vlocity_cmt__GlobalKey__c from  vlocity_cmt__DRBulkData__c where vlocity_cmt__DRBundleName__c = 'None Specified' and vlocity_cmt__AsyncApexJobId__c = null and vlocity_cmt__GlobalKey__c != null"
        bulk_data_records = query.query(q0)
        bdrs={}
        for bdr in bulk_data_records['records']: bdrs[bdr['Id']] = bdr['vlocity_cmt__GlobalKey__c']
        print(len(bdrs))

        q = f"select ID,Body,ParentId from Attachment where ParentId in (select Id from  vlocity_cmt__DRBulkData__c where vlocity_cmt__DRBundleName__c = 'None Specified' and vlocity_cmt__AsyncApexJobId__c = null and vlocity_cmt__GlobalKey__c != null)"

        attachments = query.query_base64(q)

        for attachment in attachments['records']:
            attachment['vlocity_cmt__GlobalKey__c'] = bdrs[attachment['ParentId']]

        ip_definitions = self.get_IP_definitions()

        ip_definitions_woo = [ip_definition for ip_definition in ip_definitions if ip_definition['vlocity_cmt__ProcedureKey__c'].startswith('woo_')]

        for ip_definition_woo in ip_definitions_woo:
            ip_definition_woo['steps'] = set(ip_definition_woo['steps'])
        for attachment in attachments['records']:
            log = restClient.requestWithConnection(action=attachment['Body'])
            possible_ips = []

            if 'vlcDebug' in log:
                sequence = log['vlcDebug']['executionSequence']
                possible_ips =self.findMatch(sequence,ip_definitions_woo)
                if len(possible_ips) >0:
                    bulk_data_record = [record for record in bulk_data_records['records'] if record['Id']==attachment['ParentId']][0].copy()
                    bulk_data_record['possible'] = possible_ips
                    utils.printFormated(bulk_data_record)
            #    else:
            #        posibles = self.bestMach(sequence,ip_definitions)
           #         utils.printFormated(posibles)

    def get_IP_definitions(self):
        restClient.init('NOSQSM')
        q = f"""select 
                    Id,
                    vlocity_cmt__Content__c,
                    vlocity_cmt__OmniScriptId__r.name,
                    vlocity_cmt__OmniScriptId__r.vlocity_cmt__ProcedureKey__c 
                    from vlocity_cmt__OmniScriptDefinition__c 
                    where vlocity_cmt__OmniScriptId__c in (select Id from vlocity_cmt__OmniScript__c where vlocity_cmt__OmniProcessType__c = 'Integration Procedure' and vlocity_cmt__IsActive__c = TRUE) """

        res = query.query(q)

        ip_definitions = []

        for record in res['records']:
            ip_definition = {
                'vlocity_cmt__ProcedureKey__c': record['vlocity_cmt__OmniScriptId__r']['vlocity_cmt__ProcedureKey__c'],
                'Name':                         record['vlocity_cmt__OmniScriptId__r']['Name'],
                'steps':                        []
            }
            ip_definitions.append(ip_definition)
            content = simplejson.loads(record['vlocity_cmt__Content__c'])
            for child in content['children']:
                ip_definition['steps'].append(child['name'])

        return ip_definitions
