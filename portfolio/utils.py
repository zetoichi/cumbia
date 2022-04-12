import requests


def get_user_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_user_country(request):
    ip_address = get_user_ip(request)
    response = requests.get(f"http://www.geoplugin.net/json.gp?ip={ip_address}")
    country = response.json().get("geoplugin_countryCode")

    if not country:
        country = "AR"

    return country
