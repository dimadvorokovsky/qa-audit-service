import requests


def get_performance_status(response_time):
    if response_time < 1:
        return "PASS"

    if response_time <= 3:
        return "WARN"

    return "FAIL"


def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        response_time = round(response.elapsed.total_seconds(), 3)

        return {
            "url": url,
            "status_code": response.status_code,
            "response_time": response_time,
            "is_available": response.ok,
            "performance_status": get_performance_status(response_time)
        }

    except requests.RequestException as error:
        return {
            "url": url,
            "status_code": None,
            "response_time": None,
            "is_available": False,
            "performance_status": "FAIL",
            "error": str(error)
        }