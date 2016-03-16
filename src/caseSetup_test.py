#!/usr/bin/env python

import setup
import unittest
import mock


class SetUpTest(unittest.TestCase):
    @mock.patch.object(setup.Salesforce, '__init__')
    @mock.patch.object(setup.Salesforce, 'query_all')
    @mock.patch('setup.db.run_sql')
    @mock.patch('setup.alrta.get_rules')
    @mock.patch('setup.parser.get')
    def test_setup(self,mock_parser_get, mock_get_rules, mock_run_sql, mock_query_all, mock_sf_init):
        mock_sf_init.return_value = None
        mock_parser_get.return_value = "FakeData"
        fakeCustomer =  {'id': 'qwerty', 'Customer_ID__c': '1', 'Name': 'Test Customer'};
        mock_query_all.return_value = {'records': [fakeCustomer]}

        global_rule = {
            'parse_rule': '{"name":"LR-TestRule","from":[{"parserule":"fakeuuid"}],"intervals":[{"minutes":"5"}],"filter":"true"}'}
        global_rule['query_rule'] = '&dimensions=Column1:*,Column2:*&elements=Column3,Total'
        global_rules = [global_rule]

        mock_run_sql.side_effect = [[{'table_name': '1_case_tbl'}],global_rules]

        mock_get_rules.return_value = ['{"name":"LR-TestRule","from":[{"parserule":"CCF1016C-AFF5-11E1-B6A2-000C29CAA21E"}],"intervals":[{"minutes":"15"}],"filter":"true","dimensions":[{"Appliance":{"message_field":"sid"}},{"website_id":{"token":"AA885221-C163-1004-FEE9-00000A0006E9"}},{"website_name":{"token":"E7869AD0-C055-11E1-B717-0050568AB87A"}},{"violations":{"token":"04A7924A-7A3D-1004-DB80-00007F000001"}}],"collect":[{"TotalMessages":{"count":{"literal":"*"}}}],"id":"7ee927c4-9660-43c4-9b9f-de3f1f10cc18"}']

        gen1 = setup.setup()


        gen2 = gen1.next()
        final = gen2.next()

        customer = final[0]
        rules = final[1]

        self.assertEquals( customer['Customer_ID__c'], fakeCustomer['Customer_ID__c'])
        self.assertEquals(customer['cid'] , int(fakeCustomer['Customer_ID__c']))
        self.assertEquals(customer['Name'] , fakeCustomer['Name'])

        self.assertEquals(len(rules),1)
        self.assertEquals(rules[0]['name'],'LR-TestRule')

        pass





def main():
    unittest.main()


if __name__ == "__main__":
    main()
