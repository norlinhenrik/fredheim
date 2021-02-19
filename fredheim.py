import datetime
import xmlrpc.client

url = 'https://fredheim.apps2grow.com'
db = 'ag12'
username = ''
password = ''

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def partner_test():

    ids = models.execute_kw(db, uid, password,
        'res.partner', 'search',
        [[['is_company', '=', True], ['customer', '=', True]]])

    print(ids)

    records = models.execute_kw(db, uid, password,
        'res.partner', 'read', [ids])

    for record in records:
        print(record["name"])

def accounting_test():

    records = models.execute_kw(db, uid, password,
        'account.move.line', 'search_read',
        [[
            ['date', '>=', datetime.datetime(2020, 1, 1)], 
            ['date', '<=', datetime.datetime(2020, 12, 31)], 
            ['account_id', '=', 3983], # 3950 Gift Income
            ['move_id.state', '=', 'posted']
        ]],
        {
            # 'limit': 5,
        },
    )

    for record in records:
        output = "{}, {}, {}, {}, {}, {}, {}".format(record["date"], record["account_id"][1], record["analytic_account_id"], record["partner_id"], record["credit"], record["amount_currency"], record["currency_id"])
        print(output)
    print(len(records))

def fields_test():

    records = models.execute_kw(
        db, uid, password, 'account.move.line', 'fields_get',
        [], {'attributes': ['string', 'help', 'type']})

    for key, value in sorted (records.items()) :  
        print("{} ({})".format(key, value['type'])) 

# useful models:
# account.move.line (all accounting info)
# account.move (every move (transaction) has at least two lines)
# res.partner (contact: customer and/or supplier)
# account.analytic.account (department or project)
# res.currency


accounting_test()
fields_test()
partner_test()
