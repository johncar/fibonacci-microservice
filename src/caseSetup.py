from allib import db
from allib.api import alrta
from simple_salesforce import Salesforce
from sets import Set
import json
import aggregation
from urlparse import parse_qs


def setup(cids_to_run=[], cids_exclude=[]):
    """
    step 2 get active customers

    :param cids_to_run: int[]
    :param cids_exclude: int[]
    """
    activeLrCustomers = get_lr_customers()
    if not cids_to_run:
        customers = activeLrCustomers
    else:
        customers = {}
        for cid in cids_to_run:
            if cid in activeLrCustomers:
                customers[cid] = activeLrCustomers[cid]

    if cids_exclude:
        for cid in cids_exclude:
            # remove customers that we exclude
            if cid in customers: del customers[cid]

    process(customers)


def process(customers):
    """
    step 3 get rules

    :type customers: object
    """
    global_rules = get_global_rules()

    for customer in customers:
        process_customer(customer, global_rules)


def process_customer(customer, global_rules):
    """
    step 4 get customer rules

    :param customer:
    :param global_rules:
    """
    customer_rules = get_customer_rules(customer['cid'])
    # intersect with global rules
    rules = []
    for customer_rule in customer_rules:
        if customer_rule['name'] in global_rules:
            customer_rule['root_rule'] = global_rules[customer_rule['name']]
            rules.append(customer_rule)
    aggregate(customer, rules)
    # send to aggregation


def get_customer_rules(cid):
    """
    gets the customer rules from alrta

    :param cid: int
    :return:
    """
    return [json.loads(x) for x in alrta.get_rules(cid)]


def get_lr_customers():
    """
    gets the customers from salesforce, then the case tables from alpha
    intersects the 2 then returns the results
    :return:
    """
    sf = Salesforce(username='opsautomation@alertlogic.com', password='',
                    security_token='')
    lrCustomers = sf.query_all(
            "SELECT id, Customer_ID__c, Name FROM Account WHERE Customer_ID__c != '' AND Active_LR_Customer__c = true ")
    customers = {}
    for customer in lrCustomers['records']:
        # i dont want to type Customer_ID__c all the time
        customer['cid'] = int(customer['Customer_ID__c'])
        customers[customer['cid']] = customer

    command = "SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_name LIKE '%_case_tbl' "
    alphaTables = db.run_sql(command)

    # get the case tables from alpha, intersect them with the active lr customers
    # this helps filter customers that dont belong in the datacenter
    customersFiltered = {}
    for table in alphaTables:
        cid = int(table['table_name'].replace('_case_tbl', ''));
        if cid in customers:
            customersFiltered[cid] = customers[cid]

    return customersFiltered


def get_global_rules():
    """
    gets the root rules from alpha
    :return:
    """
    global_rules = db.run_sql("SELECT id, parse_rule, query_rule FROM activequery_rules_list")
    for rule in global_rules:
        rule['parse_rule'] = json.loads(rule['parse_rule'])
        headers = ['Interval']
        split = parse_qs(rule['query_rule'])
        headers.extend(split['dimensions'][0].split(','))
        headers.extend(split['elements'][0].split(','))
        rule['headers'] = headers

        rule['headers_indexed'] = dict([(x, ind) for ind, x in enumerate(headers)])
        rule['headers_simple_indexed'] = dict([(x.split(':')[0], ind) for ind, x in enumerate(headers)])

    return dict([(d['parse_rule']['name'], d) for d in global_rules])


def aggregate(customer, rules):
    """
    sends the customer and rules to the next step
    :param customer:
    :param rules:
    """
    aggregation.aggregation(customer, rules)
