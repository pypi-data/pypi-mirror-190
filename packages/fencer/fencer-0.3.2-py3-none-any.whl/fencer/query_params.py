import requests

url = "http://localhost:5000/products"


def sql_injection_through_query_param():
    query = "1' OR 1=1 --"
    response = requests.get(url + "?category=" + query)
    print(len(response.json()["products"]))


def check_only_allowed_params():
    response = requests.get(url + "?something=else")
    print(len(response.json()["products"]))


sql_injection_through_query_param()
check_only_allowed_params()
