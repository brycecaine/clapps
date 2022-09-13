from datetime import date, timedelta
import os
from ofxtools.Parser import OFXTree
from io import StringIO
import requests
from ofxparse import OfxParser

CHASE_USERNAME = os.environ['CHASE_USERNAME']
CHASE_PASSWORD = os.environ['CHASE_PASSWORD']
CHASE_CC_NUMBER = os.environ['CHASE_CC_NUMBER']
CHASE_NEWFILEUID = os.environ['CHASE_NEWFILEUID']
CHASE_DTCLIENT = os.environ['CHASE_DTCLIENT']
CHASE_CLIENTUID = os.environ['CHASE_CLIENTUID']
CHASE_TRNUID = os.environ['CHASE_TRNUID']


# Based on https://stackoverflow.com/a/48157581/4062658


def get_ofx_data(response):
    buf = StringIO(response.text)

    ofx_data = ''

    for line in buf.readlines():
        if '<OFX>' in line:
            ofx_data = line

    return ofx_data


def get_bank_txs(start_date):
    url = 'https://ofx.chase.com'

    chase_username = CHASE_USERNAME 
    chase_password = CHASE_PASSWORD
    chase_cc_number = CHASE_CC_NUMBER
    chase_newfileuid = CHASE_NEWFILEUID
    chase_dtclient = CHASE_DTCLIENT
    chase_clientuid = CHASE_CLIENTUID
    chase_trnuid = CHASE_TRNUID
    start_date_str = start_date.strftime('%Y%m%d')

    data = f'''OFXHEADER:100
               DATA:OFXSGML
               VERSION:102
               SECURITY:NONE
               ENCODING:USASCII
               CHARSET:1252
               COMPRESSION:NONE
               OLDFILEUID:NONE
               NEWFILEUID:{chase_newfileuid}

               <OFX>
               <SIGNONMSGSRQV1>
               <SONRQ>
               <DTCLIENT>{chase_dtclient}
               <USERID>{chase_username}
               <USERPASS>{chase_password}
               <LANGUAGE>ENG
               <FI>
               <ORG>B1
               <FID>10898
               </FI>
               <APPID>QWIN
               <APPVER>1800
               <CLIENTUID>{chase_clientuid}
               </SONRQ>
               </SIGNONMSGSRQV1>
               <CREDITCARDMSGSRQV1>
               <CCSTMTTRNRQ>
               <TRNUID>{chase_trnuid}
               <CLTCOOKIE>4
               <CCSTMTRQ>
               <CCACCTFROM>
               <ACCTID>{chase_cc_number}
               </CCACCTFROM>
               <INCTRAN>
               <DTSTART>{start_date_str}
               <INCLUDE>Y
               </INCTRAN>
               </CCSTMTRQ>
               </CCSTMTTRNRQ>
               </CREDITCARDMSGSRQV1>
               </OFX>'''

    headers = {
        "Content-type": "application/x-ofx",
        "Accept": "*/*, application/x-ofx",
    }

    response = requests.post(url, data=data, headers=headers, stream=True)

    ofx_data = get_ofx_data(response)

    stringfile = StringIO()
    stringfile.write(ofx_data)

    ofx = OfxParser.parse(stringfile)

    tx_dicts = []

    for transaction in ofx.account.statement.transactions:
        tx_dicts.append(transaction.__dict__)

    return tx_dicts


def main():
    start_date = date.today() - timedelta(days=1)
    tx_dicts = get_bank_txs(start_date)

    print(tx_dicts)
    print(len(tx_dicts))


if __name__ == '__main__':
    main()

