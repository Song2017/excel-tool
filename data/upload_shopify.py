import os
import time

import requests
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

pg_sql_str = os.getenv('NOMAD_PG_DSN')
engine = create_engine(pg_sql_str)
session = scoped_session(sessionmaker(bind=engine))


def get_waybill(order_id: str):
    url = "https://warehouse.samarkand-global.cn/web/dataset/search_read"

    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "sale.order",
            "domain": [
                "|",
                "|",
                [
                    "name",
                    "ilike",
                    order_id
                ],
                [
                    "client_order_ref",
                    "ilike",
                    order_id
                ],
                [
                    "partner_id",
                    "child_of",
                    order_id
                ]
            ],
            "fields": [
                "message_needaction",
                "name",
                "date_order",
                "commitment_date",
                "expected_date",
                "partner_id",
                "user_id",
                "amount_total",
                "currency_id",
                "state", "carrier_tracking_ref", "carrier_id"
            ],
            "limit": 80,
            "sort": "",
            "context": {
                "lang": "en_US",
                "tz": False,
                "uid": 144,
                "search_default_my_quotation": 1
            }
        },
        "id": 87379458
    })
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'cookie': 'session_id=e199174c30ec5102e2cf7f6b4b4bc883b22a3ead; _oauth2_proxy=_dqhJ7eUtBdD4lXW8e_n_Cnz_m_AFI6ADMPWXZw9LcFrTDLK2SnE3Tpw6WizLfeN-UNraLhPHlRYRtBYnOQfZcE6f26Z5TEnwHOCaCPdPGnG-8-KgexZcEEuWzZTTiiXCuoCIvsIc63_E_WCgsPv8x-M1izVxUWz47JgyxURHs-fFfEKNHlyhm7Y0s4FM2zcPHjtLKNerrVoQhMFJoUyCpHlhGnAMeUaSfgwY-akrvKa7lIHkh_G5a8N3Tnql5i4o6Nold2AV70S9arcmZ0lHe8s5AyaUjpXDWcKCQ2uOVCdpMhA9suhxq8nJJICS4cv4qefOMagOYTDfHVtCmsAYZcnKO_VOZ2tpyDXuYWjEhcdiV79uw==|1712660883|x8-1dnTt9MGY5eCqfjSlj9FsT4zChzvtUyFJvPtl5lQ=; session_id=e199174c30ec5102e2cf7f6b4b4bc883b22a3ead',
        'origin': 'https://warehouse.samarkand-global.cn',
        'referer': 'https://warehouse.samarkand-global.cn/web',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    resp = response.json().get('result').get("records", [{}])[0]
    assert resp.get("carrier_tracking_ref"), "waybill id is null"
    return {"waybill_id": resp.get("carrier_tracking_ref"), "express": resp.get('carrier_id')[1]}


def read_order(order_id: str):
    text = 'SELECT delivery_carrier_id,outer_order_id,store_id FROM "order" '
    text += f" where id = '{order_id}' "
    flights = session.execute(text).all()
    assert flights[0][1] in order_id
    return {
        "delivery_carrier_id": flights[0][0],
        "store_id": flights[0][2],
        "outer_order_id": flights[0][1],
    }


def update_order(order_id: str, waybill_id: str):
    text = ('update "order" '
            f"set status = 5, delivery_waybill_id= '{waybill_id}' where id  = '{order_id}';")
    session.execute(text)
    session.commit()


def upload_shopify(express: str, store: str, order_id: str, tracking: str):
    url = f"https://nomad-envoy-shopify-service-int.samarkand-global.cn/v1/int/stores/{store}/orders/{order_id}"
    if "dpd" in express.lower():
        express = "dpd"
    elif "royalmail" in express.lower():
        express = "royalmail"
    else:
        express = "royalmail"

    payload = json.dumps({
        "expressCompany": express,
        "trackingReference": tracking,
        "status": "WAIT_BUYER_CONFIRM_GOODS"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    print(payload, url)
    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    orders = [
        "DJSAMARKANDSHOPIFYPROBIO7#5645642006777",
    ]
    for o in orders:
        waybill = get_waybill(o)
        order = read_order(o)
        upload_shopify(waybill["express"], order["store_id"], order["outer_order_id"], waybill["waybill_id"])
        update_order(o, waybill["waybill_id"])
        time.sleep(1)
