"""Speech workers must not open network connections, even with cached models."""
import sys


def deny_network():
    def audit(event, args):
        if event in ('socket.connect', 'socket.connect_ex', 'socket.getaddrinfo', 'socket.sendto'):
            raise OSError('Network access is disabled in Mack’s speech worker.')
    sys.addaudithook(audit)
