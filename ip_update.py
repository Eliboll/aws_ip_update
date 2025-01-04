import boto3 
from requests import get
import dns.resolver

client = boto3.client('route53')

def update_zone(ip:str, domains:list[str], zoneID: str) -> None:
    records = []
    for domain in domains:
        records.append(
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': domain,
                    'Type': 'A',
                    'TTL' : 300,
                    'ResourceRecords': [
                        {
                            'Value': ip
                        },
                    ],
                },
            }
        )

    response = client.change_resource_record_sets(
        HostedZoneId=zoneID,
        ChangeBatch={
            'Comment': 'auto update ip',
            'Changes': records
        }
    )
    return response

if __name__ == "__main__":
    domains = [""]
    zoneID = ""
    ip = get('https://api.ipify.org').content.decode('utf8')
    dns_val = str(dns.resolver.resolve('mc.elibollinger.com', 'A')[0])
    if (ip != dns_val):
        print("Sending update command")
        response = update_zone(ip, domains,)
        code = response["ResponseMetadata"]['HTTPStatusCode']
        print("Returned with status code %d" % code)
    else:
        print("Value up to date")