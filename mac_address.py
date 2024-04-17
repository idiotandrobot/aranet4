import argparse

def toint(mac_str, divider = ':'):
    return int(mac_str.replace(divider,''), 16)

def tostr(mac_int, divider = ':'):
    mac_str="{:012X}".format(mac_int)
    return divider.join(a+b for a,b in zip(mac_str[::2], mac_str[1::2]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mac", type=str)
    args = parser.parse_args()
    mac = args.mac
    print('Input:', mac)
    mac_int = toint(args.mac)
    print('toint:', mac_int)
    mac_str = tostr(mac_int)
    print('tostr:', mac_str)
    