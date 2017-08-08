import base64


def lambda_handler(event, context):
    net_profit = 0
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        print("Decoded Payload: {}".format(payload))
        row = payload.split(',')
        net_profit += (float(row[2]) - float(row[3]))
    print("Net Profits: ${}".format(net_profit))
    return net_profit
