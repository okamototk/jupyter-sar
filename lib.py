import subprocess
from subprocess import Popen,PIPE
from datetime import datetime

from highcharts import Highchart

def readSarCPU(f):
    args = ['/bin/bash','-c', "sadf -T --  -C " + f + " |awk '{print $3,$4,$6,$7}'"]
    p = Popen(args,stdout=PIPE,stderr=PIPE)
    out,err = p.communicate()
    cpu = {'%user': [], '%nice': [], '%system': [], '%iowait': [], '%steal': [], '%idle': []}
    timestamp = []
    x = 0
    prev = ""
    for l in out.decode('utf8').split('\n'):
        if l == "":
            break;
        r = l.split(" ")

        if prev != r[1]:
            timestamp.append(datetime.strptime(r[0]+" "+r[1], '%Y-%m-%d %H:%M:%S'))
            prev = r[1]
            x = x+1
        cpu[r[2]].append(float(r[3]))
    return (timestamp, cpu)


def plot(x, data, highchart, title="",xlabel="",ylabel=""): 
    options = {
        'title': {
            'text': 'CPU Usage'
        },
        'subtitle': {
            'text': 'Source: test.sar'
        },
        'xAxis': {
            'type': 'datetime',
            'minRange': 1000*len(x)
        },
        'yAxis': {
            'title': {
                'text': ylabel
            },
            'labels': {
                'formatter': 'function () {\
                                    return this.value ;\
                                }'
            }
#            },
#            'max': 100
        },
        'tooltip': {
            'shared': True,
            'valueSuffix': ylabel
        },
        'plotOptions': {
            'area': {
                'stacking': 'normal',
                'lineColor': '#666666',
                'lineWidth': 1,
                'marker': {
                    'lineWidth': 1,
                    'lineColor': '#666666'
                }
            }
        }
    }
    highchart.set_dict_options(options)
    for k in data.keys():
        highchart.add_data_set(data[k],'area',k,pointInterval=1000, pointStart=x[0])


