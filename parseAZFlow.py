import json
import csv
import datetime
import os

for root, dirs, files in os.walk(os.getcwd(), topdown=False):
    for name in files:
        filepath = os.path.join(root,name)
        flowdata = json.loads(open(filepath).read())

        # flowdata['records'][0]['properties']['flows'] is the array of NSG rules, and their dict of flows

        # Our objective is just to dump a CSV of Timestamp,RULENAME,MACADDR,SRCIP,DSTIP,SRCPRT,DSTPRT,PROTO,DIRECTION,ACTION
        # This will help simple text parsing compared to json for now.
        for flowEvents in flowdata['records']:
            resourceId = flowEvents['resourceId']
            # We can parse NSGName, SubscriptionId, and ResourceGroupName from resourceId
            # /SUBSCRIPTIONS/12345678-abcd-efgh-1234-000000000000/RESOURCEGROUPS/ADTESTINT/PROVIDERS/MICROSOFT.NETWORK/NETWORKSECURITYGROUPS/TESTFLOWLOGS-NSG
            rid = list(csv.reader([resourceId],delimiter="/"))[0]
            SubscriptionID = rid[2]
            RGName = rid[4]
            NSGName = rid[8]
            for NSGs in flowEvents['properties']['flows']:
                NSGRule = NSGs['rule']
                for flows in NSGs['flows']:
                    # yes, it's a recursive flow.. full path:
                    # flowdata['records'][0]['properties']['flows'][0]['flows']
                    MACAddr = flows['mac']
                    for flowTuple in flows['flowTuples']:
                        # now we have CSV data..
                        # 1483286396,10.1.0.4,13.71.200.123,59836,443,T,O,A
                        # TS,SRCIP,DSTIP,SRCPT,DSTPT,PROTO,DIR,ACTION
                        event = list(csv.reader([flowTuple]))[0]
                        TimeStamp = datetime.datetime.fromtimestamp(float(event[0])).strftime('%Y-%m-%d %H:%M:%S')
                        SrcIP = event[1]
                        DstIP = event[2]
                        SrcPort = event[3]
                        DstPort = event[4]
                        Proto = event[5]
                        Direction = event[6]
                        Action = event[7]
                        print("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13}".format(
                            filepath,TimeStamp,SubscriptionID,RGName,NSGName,NSGRule,MACAddr,SrcIP,DstIP,SrcPort,DstPort,Proto,Direction,Action))


