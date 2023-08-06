import os
import platform
import argparse
import subprocess
import random
import re
import time

EMPTY_MAC = "00-00-00-00-00-00"
INTEL_BYTES = "B0-7D-64"
MAC_REGEX = '([0-9a-fA-F][0-9a-fA-F]-){5}[0-9a-fA-F][0-9a-fA-F]'
ARP_MAC_REGEX = '([0-9a-fA-F][0-9a-fA-F]:){5}[0-9a-fA-F][0-9a-fA-F]'

PING_TIMEOUT = 60
PING_INTERVAL = 1

EXIT_FAILURE = 1
EXIT_SUCCESS = 0


def main():
    args = parse_args()
    if args.json_target_names is None:
        names = [os.path.basename(path) for path in args.json_src_files]
    else:
        names = args.json_target_names
    for path, name in zip(args.json_src_files, names):
        temp_path = path[:-5] + '_TEMP.json'
        with open(path, 'r+') as original_json_file:
            print(f"Opening JSON file at {path}")
            text = original_json_file.read()
            if EMPTY_MAC in text:
                flash_mac = generate_mac()
                print(f"MAC is empty, generated new MAC: {flash_mac}")
                text = text.replace(EMPTY_MAC, flash_mac)
                with open(temp_path, 'w') as new_json_file:
                    print(f"Writing new file at {temp_path}")
                    new_json_file.write(text)
            else:
                results = re.search(MAC_REGEX, text)
                if results:
                    flash_mac = results.group(0)
                    print(f" found MAC: {flash_mac}")
                temp_path = path
        if not flash_json(args, temp_path, name):
            print('Failure: File transfer failed.')
            exit(EXIT_FAILURE)
        print('File transfer successful.')

    # If flashing several files with mac address in them, we expect to see the last one in the test.
    if args.r:
        if not test_mac(args, flash_mac):
            print('Failure.')
            exit(EXIT_FAILURE)
        print('SUCCESS: MAC was changed, flash successful.')
        exit(EXIT_SUCCESS)
    else:
        exit(EXIT_SUCCESS)


def generate_mac():
    """
    Makes a new intel mac address
    """
    new_mac = INTEL_BYTES
    for i in range(3):
        new_mac += '-{:02x}'.format(random.randint(0, 255)).upper()
    return new_mac


def flash_json(args, temp_path, new_name):
    """
    Flashes the json file given in args
    :param args: The args passed to the script
    :param temp_path: The path to the JSON file with the new MAC
    :return: True on flashing success and false on failure
    """
    transfer_cmd = f"test fs -t {new_name}"
    shell_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cli_shell.py")
    ip_port = args.udp_socket if args.udp_socket else args.tcp_socket
    cmd_args = ['-U', ip_port, '-c', transfer_cmd, '-f', temp_path]
    proc = subprocess.run(['python3', shell_path] + cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if platform.system() == "Windows":
        # cli_shell.py doesn't support return code in windows:
        if "Transmission successful" in proc.stderr.decode():
            return True
    else:
        if "Transmission successful" in proc.stderr.decode() and proc.returncode == 0:
            return True
    print(f'stdout is {proc.stdout.decode()}')
    print(f'stderr is {proc.stderr.decode()}')
    return False


def test_mac(args, expected_mac):
    """
    Test if the mac address was changed
    :param args: The args passed to the script
    :param new_mac: The new MAC we generated
    :return: True on flashing success and false on failure
    """
    # Reboot the board so the mac will change:
    shell_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cli_shell.py")
    ip_port = args.udp_socket if args.udp_socket else args.tcp_socket
    cmd_args = ['-U', ip_port, '-c', 'reboot']
    proc = subprocess.run(['python3', shell_path] + cmd_args, stdout=subprocess.PIPE)

    # Wait for the board to boot, then check the info
    if not wait_for_ping(ip_port[:-5]):
        return False
    cmd_args = ['-U', ip_port, '-c', 'info']
    proc = subprocess.run(['python3', shell_path] + cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    matches = re.search(MAC_REGEX, proc.stdout.decode())
    if not matches:
        print("Could not find MAC address on the board.")
        print(f'stdout is {proc.stdout.decode()}')
        print(f'stderr is {proc.stderr.decode()}')
        return False
    print(f"Flashed MAC:{expected_mac}\nMAC on board:{matches.group(0)}")
    if not matches.group(0) == expected_mac:
        print("MACs not identical, failure.")

    # Check the arp table:
    cmd_args = ['arp', '-a', ip_port[:-5]]
    proc = subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    matches = re.search(ARP_MAC_REGEX, proc.stdout.decode())
    if not matches:
        print(f"ARP didn't contain mac address for IP {ip_port[:-5]}")
        return False
    arp_mac = matches.group(0).replace(':', '-').upper()
    print(f"MAC in ARP:{arp_mac}")
    if not arp_mac == expected_mac:
        print("MACs not identical, failure.")
        return False
    return True


def wait_for_ping(ip):
    """
    Pings the given IP until response or until PING_TIMEOUT seconds pass.
    """
    start_time = time.time()
    # Waits until we get a ping from the machine
    print(f"looking for machine on address {ip}...")

    if platform.system() == "Windows":
        flag = '-n'
        success_string = "Received = 1"
    else:
        flag = '-c'
        success_string = "1 received"
    # Ping once
    command = ["ping", flag, "1", ip]
    x = 0
    while (time.time() - start_time < PING_TIMEOUT):
        proc = subprocess.run(command, stdout=subprocess.PIPE)
        x += 1
        # we send one, so 1 received is success
        if success_string in proc.stdout.decode():
            return True
        time.sleep(PING_INTERVAL)
    # Debug Messages in case of failures
    print("Started Pinging in ", start_time)
    print("Gave Up Pinging in ", time.time(), f"Pinged {x} times.")
    # proc = subprocess.run(['sudo', 'arp-Wscan', '-l'], stdout=subprocess.PIPE)
    print(proc.stdout.decode())
    return False


def parse_args():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-U', '--udp-socket',
        metavar='<ip:port>',
        default=None,
        help='Socket address in the form <ip:port>')
    group.add_argument(
        '-T', '--tcp-socket',
        metavar='<ip:port>',
        default=None,
        help='Socket address in the form <ip:port>')
    required.add_argument(
        '-p', '--json-src-files',
        metavar='json_src_files',
        required=True,
        nargs='+',
        help='The path to the JSON file to flash')
    required.add_argument(
        '-n', '--json-target-names',
        metavar='json_target_names',
        default=None,
        nargs='+',
        help="""The target name to give the file inside the MCU. Default is the same name as the src file.
            If flashing several files the names have to be in same order as the json src files.""")
    parser.add_argument(
        '-r',
        action="store_true",
        help='Test the new MAC by rebooting the system and checking the MAC was updated.')
    return parser.parse_args()


if __name__ == "__main__":
    main()
