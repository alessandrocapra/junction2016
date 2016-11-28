def get_auth_headers(access_token):
    return {
        'accept': "application/json",
        'authorization': "Bearer " + access_token,
        'content-type': "application/json"
    }
