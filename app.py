import os
import sys
import traceback

import requests
import json

from flask import Flask
from flask import request
from flask import Response
from flask import json
from flask import make_response


app = Flask(__name__)

headers = {
  "X-API-KEY": "51ca260f-1d95-438a-a6ea-c77d5a3d8019"
}

# clientes = {
#     "afi_hash1":{
#         "nombre":"Camilo Valencia",
#         "correo":"cvalen20@gmail.com",
#         "ciudad":"Medellin"
#     },
#     "afi_hash2":{
#         "nombre":"Didier Correa",
#         "correo":"correalondon@gmail.com",
#         "ciudad":"Medellin"
#     },
#     "afi_hash3":{
#         "nombre":"Juan Esteban Betancur",
#         "correo":"juaneciyo0908@gmail.com",
#         "ciudad":"Medellin"
#     }
# }


def conslutar_info(clientes,headers):

    for hash,info in clientes.items():
        correo = info["correo"]

        r = requests.get(f"https://api.seon.io/SeonRestService/email-api/v2.2/{correo}?include=history,flags,id&flags_timeframe_days=10&timeout=5000", headers=headers)

        data = json.loads(r.text)
        active_accounts = []
        for account, values in data["data"]["account_details"].items():
            if values["registered"]:
                active_accounts.append(account)
        # print(json.dumps(data, indent=4))
        clientes[hash]["active_acounts"] = active_accounts

    return clientes


@app.route("/", methods=['POST'])
def api_data():
    data = request.get_json(force=True)
    clientes = make_response( conslutar_info(data,headers) )
    return clientes


if __name__ == '__main__':

    app.run( host = os.environ.get('FLASK_IP'))

