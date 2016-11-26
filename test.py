import http.client

conn = http.client.HTTPSConnection("test-restgw.transferwise.com")

headers = {
    'accept': "application/json",
    'authorization': "Bearer 3d4b1072-152c-4df5-9d83-629c427b442d"
    }

conn.request("GET", "/v1/transfers?limit=256&offset=256", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))