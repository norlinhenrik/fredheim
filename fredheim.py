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

def print_line(line):
    output = "{}, {}, {}, {}, {}, {}, {}".format(line["date"], line["account_id"], line["analytic_account_id"], line["partner_id"], line["credit"], line["amount_currency"], line["currency_id"])
    print(output)

def get_donations(print_output):

    lines = models.execute_kw(db, uid, password,
        'account.move.line', 'search_read',
        [[
            ['date', '>=', datetime.datetime(2020, 1, 1)], 
            ['date', '<=', datetime.datetime(2020, 12, 31)], 
            ['account_id', '=', 3983], # 3950 Gift Income
            ['move_id.state', '=', 'posted']
        ]],
        {
            'limit': 2,
        },
    )
    if print_output:
        for line in lines:
            print_line(line)
        print(len(lines))
    return lines

def get_donation_payments(donations):
    payment_account_ids = models.execute_kw(db, uid, password,
        'account.account', 'search',
        [[
            ['user_type_id', '=', 20], # bank & cash
        ]])
    # print(payment_account_ids)

    move_ids = [d['move_id'][0] for d in donations]
    print(len(move_ids))
    move_ids = list(set(move_ids)) # remove duplicates
    print(len(move_ids))
    moves = models.execute_kw(db, uid, password, 'account.move', 'read', [move_ids])
    for move in moves:
        output = "account.move: \n{}, {}, {}, lines: {}".format(move["date"], move["id"], move["name"], move["line_ids"])
        print(output)
        lines = models.execute_kw(db, uid, password, 'account.move.line', 'read', [move["line_ids"]])
        for line in lines:
            if line['account_id'][0] in payment_account_ids: # bank & cash etc.
                print('payment')
                print_line(line)
            if line['account_id'][0] == 3983: # 3950 Gift Income
                print('donation')
                print_line(line)

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


donations = get_donations(print_output=False)
get_donation_payments(donations)
# fields_test()
# partner_test()
