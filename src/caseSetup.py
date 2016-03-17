import sys

sys.path.insert(0, '/Users/jtarver/al-aamp-base/sources/allib/lib')
from allib import db

from allib.api import alrta
from simple_salesforce import Salesforce
from sets import Set
import json, logging

from urlparse import parse_qs
from ConfigParser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')


################################################################
#
# functions for case generation setup
#
# author: Jason Tarver
################################################################


def triggerr():
    return "DONE"

def trigger(cids_to_run=[], cids_exclude=[]):
    for _customer in setup(cids_to_run,cids_exclude):
        for returnd in _customer:
            print("got customer " + returnd[0]['Name'] + " and " + str(len(returnd[1])) + " rules")


def setup(cids_to_run=[], cids_exclude=[]):
    """
    step 2 get active customers

    :param cids_to_run: int[]
    :param cids_exclude: int[]
    :return: a genertor that has a generator for each customer and a generator for each customers rule
    """
    activeLrCustomers = _get_lr_customers()
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

    return _process(customers)


def _process(customers):
    """
    step 3 get rules

    :type customers: object
    """
    global_rules = _get_global_rules()

    for customer in customers.itervalues():
        yield _process_customer(customer, global_rules)


def _process_customer(customer, global_rules):
    """
    step 4 get customer rules

    :param customer:
    :param global_rules:
    """
    customer_rules = _get_customer_rules(customer['cid'])
    # intersect with global rules
    rules = []
    for customer_rule in customer_rules:
        if customer_rule['name'] in global_rules:
            customer_rule['root_rule'] = global_rules[customer_rule['name']]
            rules.append(customer_rule)
    yield (customer, rules)
    # send to aggregation


def _get_customer_rules(cid):
    """
    gets the customer rules from alrta

    :param cid: int
    :return:
    """
    return [json.loads(x) for x in alrta.get_rules(cid)]


def _get_lr_customers():
    """
    gets the customers from salesforce, then the case tables from alpha
    intersects the 2 then returns the results
    :return:
    """
    logging.info("Getting Log Review Customers")
    sf = Salesforce(username=parser.get('config', 'sfUser'), password=parser.get('config', 'sfPass'),
                    security_token=parser.get('config', 'sfKey'))
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
        try:
            cid = int(table['table_name'].replace('_case_tbl', ''));
            if cid in customers:
                customersFiltered[cid] = customers[cid]
        except:
            pass

    logging.info("Got " + str(len(customersFiltered)) + " customers")
    return customersFiltered


def _get_global_rules():
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
