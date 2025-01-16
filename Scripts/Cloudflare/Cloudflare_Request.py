from cloudflare import Cloudflare

def update_dns_record(ip_address, teamname):
    api_email = "awaumans@me.com"
    api_key = "05484766f2d2166862fd86f7589cfff3790e7"
    zone_id = "a20aeda4a3f1e11492799e08a8d88347"
    dns_record_id = "ac478d5a6e872cf2f7893eba1ab72c5a"

    try:
        client = Cloudflare(
            api_email=api_email,
            api_key=api_key,
        )

        response = client.dns.records.edit(
            dns_record_id=dns_record_id,
            zone_id=zone_id,
            type="A",
            name=f"{teamname}.launchingkube.com",
            content=ip_address,
            ttl=1,
            proxied=False
        )

        print(f"DNS record updated successfully for {teamname}: \n{response}")

    except Exception as e:
        print(f"Error updating DNS record for {teamname}: {e}")

if __name__ == "__main__":
    update_dns_record("34.116.176.191", "team10")