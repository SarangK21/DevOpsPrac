import requests


def check_api(url):

    try:

        response = requests.get(url, timeout=5)

        return {
            "status_code": response.status_code,
            "healthy": response.status_code == 200
        }

    except requests.RequestException:

        return {
            "status_code": None,
            "healthy": False
        }

