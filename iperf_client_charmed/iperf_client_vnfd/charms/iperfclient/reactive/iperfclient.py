from charmhelpers.core.hookenv import (
    action_get,
    action_fail,
    action_set,
    status_set,
)
from charms.reactive import (
    clear_flag,
    set_flag,
    when,
    when_not,
)
import charms.sshproxy

@when('sshproxy.configured')
@when_not('iperfclient.installed')
def install_iperfclient():
    set_flag('iperfclient.installed')
    status_set('active', 'Ready!')

#####################################################
#by papajohn and dimit
#####################################################

def check_params(gw, serverip, mode, bw, duration, direction):
    if len(gw) == 0:
        gw = "172.101.101.201"

    if mode.upper() == "UDP":
        mode = "-u"

    if len(bw) != 0:
        bw = "-b " + bw + "M"

    if len(duration) != 0:
        duration = "-t " + duration

    if direction.upper() == "DL":
        direction = "-R"

    return [gw, serverip, mode, bw, duration, direction]


@when('actions.goclient')
def goclient():
    cmd = []
    gw_cmd = []
    gw = action_get('gateway')
    serverip = action_get('server_ip')
    mode = action_get('mode')
    bw = action_get('bandwidth')
    duration = action_get('duration')
    direction = action_get('direction')
    err = ''
    try:
        [gw, serverip, mode, bw, duration, direction] = check_params(gw, serverip, mode, bw, duration, direction)
        gw_cmd = ['sudo route delete default gw 0.0.0.0; sudo route add default gw {}'.format(gw)]
        cmd = ['iperf3 -c {} {} {} {} {} >> /home/ubuntu/iperf.log'.format(serverip, mode, bw, duration, direction)]
    except:
        cmd = ['echo "Something is wrong with the input parameters!" >>/home/ubuntu/DOOMSDAY.log']
    try:
        result, err = charms.sshproxy._run(gw_cmd)
    except:
        action_fail('command failed:' + err)
    try:
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed:' + err)
    else:
        action_set({'outout': result})
    finally:
        clear_flag('actions.goclient')
