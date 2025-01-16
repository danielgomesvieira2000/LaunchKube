from cloudflare import Cloudflare

api_email = "awaumans@me.com"
api_key = "05484766f2d2166862fd86f7589cfff3790e7"
zone_id = "a20aeda4a3f1e11492799e08a8d88347"

client = Cloudflare(
    api_email=api_email,
    api_key=api_key,
)
page = client.dns.records.list(
    zone_id=zone_id
)

page = page.result[0]
print(page)