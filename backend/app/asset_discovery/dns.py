"""
Asset Discovery DNS Utilities
-----------------------------

Responsible for:

- Hostname validation
- IP validation
- DNS resolution
- Reverse DNS lookup

This module should NOT perform TLS scanning.
"""

import ipaddress
import socket
from typing import Dict


class DNSResolverError(Exception):
    """Raised when DNS resolution fails."""


class DNSResolver:
    """DNS resolution utility."""

    @staticmethod
    def is_ip_address(target: str) -> bool:
        """
        Check if the target is a valid IPv4 or IPv6 address.
        """
        try:
            ipaddress.ip_address(target)
            return True
        except ValueError:
            return False

    @staticmethod
    def resolve_hostname(hostname: str) -> str:
        """
        Resolve a hostname to an IP address.
        """
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror as exc:
            raise DNSResolverError(
                f"Unable to resolve hostname: {hostname}"
            ) from exc

    @staticmethod
    def reverse_lookup(ip_address: str) -> str:
        """
        Resolve an IP address back to a hostname.
        """
        try:
            hostname, _, _ = socket.gethostbyaddr(ip_address)
            return hostname
        except socket.herror:
            return ""

    @classmethod
    def resolve(cls, target: str) -> Dict:
        """
        Resolve a hostname or IP address.

        Returns
        -------
        {
            "hostname": "...",
            "ip_address": "...",
            "is_ip": True/False
        }
        """

        if cls.is_ip_address(target):

            hostname = cls.reverse_lookup(target)

            return {
                "hostname": hostname or target,
                "ip_address": target,
                "is_ip": True,
            }

        ip_address = cls.resolve_hostname(target)

        return {
            "hostname": target,
            "ip_address": ip_address,
            "is_ip": False,
        }
