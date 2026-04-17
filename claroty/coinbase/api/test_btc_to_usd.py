import time
from datetime import datetime

import requests

from claroty.coinbase.utils.chart_utils import ChartUtils
from claroty.coinbase.utils.mail_utils import MailUtils
from globals import BASE_URL, JSON_PATH, CHART_PATH, CHART_FILE


class TestBtcToUsd():
    def test_btc_to_usd_response_code(self):
        response = requests.get(BASE_URL+"prices/BTC-USD/spot")
        assert response.status_code == 200 , "Response Cose is not 200 as a result of HTTP Get request"

    def test_btc_to_usd_dynamic_data(self,configure_test):

        logger = configure_test
        utils = ChartUtils(logger)
        for i in range (10):
            response = requests.get(BASE_URL + "prices/BTC-USD/spot")
            response_amount = response.json()["data"]["amount"]
            logger.debug(f"response amount value is {response_amount}")
            utils.set_graph_dynamic_data(response_amount)
            time.sleep(1)
        utils.save_graph()



    def test_btc_to_usd_by_json(self,configure_test):

        logger,mail_utils,chart_utils = configure_test
        results = []

        for i in range (12):
            response = requests.get(BASE_URL + "prices/BTC-USD/spot")
            response_amount = response.json()["data"]["amount"]
            current_time  = datetime.now().strftime("%H:%M:%S")
            logger.debug(f"data for results JSON current_time:{current_time}, response amount: {response_amount}")
            new_entry = {
                "time": current_time,
                "price": response_amount
            }
            results.append(new_entry)
            time.sleep(1)
        chart_utils.save_json(results,JSON_PATH)
        chart_utils.create_chart_with_json_data(JSON_PATH)
        chart_utils.save_chart_no_timestemp("btc_price")

    def test_get_max_price_and_send_mail(self,configure_test):
        logger,mail_utils,chart_utils = configure_test
        max_rate = mail_utils.get_max_price()

        mail_as_dict= {
            "to": "kobyd100@gmail.com",
            "subject" : "Max rate for BPI found",
            "attachment" : f'{CHART_PATH}{CHART_FILE}',
            "content" : f"Hi,\nFollowing your request, Max value for BPI found.\nThe value is: {max_rate}"
        }

        mail_utils.send_gmail(mail_as_dict)








