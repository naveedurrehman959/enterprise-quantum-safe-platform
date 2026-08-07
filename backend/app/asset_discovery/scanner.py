"""
Asset Discovery TLS Scanner
---------------------------

Responsible for:

- Establishing a TLS connection
- Negotiating TLS version
- Retrieving peer certificate
- Getting negotiated cipher suite

This module does NOT:
- Parse certificates
- Save to database
- Calculate risk
"""

import socket
import ssl
from typing import Dict


class TLSScannerError(Exception):
    """Raised when TLS scanning fails."""


class TLSScanner:
    """TLS scanner for remote hosts."""

    DEFAULT_TIMEOUT = 10

    @classmethod
    def scan(
        cls,
        hostname: str,
        ip_address: str,
        port: int = 443
    ) -> Dict:
        """
        Perform TLS scan.

        Returns:
            {
                "tls_version": "...",
                "cipher_suite": "...",
                "certificate": {...}
            }
        """

        context = ssl.create_default_context()

        # Require certificate validation
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        try:
            with socket.create_connection(
                (ip_address, port),
                timeout=cls.DEFAULT_TIMEOUT
            ) as sock:

                with context.wrap_socket(
                    sock,
                    server_hostname=hostname
                ) as tls_socket:

                    certificate = tls_socket.getpeercert()

                    cipher = tls_socket.cipher()

                    return {
                        "tls_version": tls_socket.version(),
                        "cipher_suite": cipher[0] if cipher else None,
                        "cipher_protocol": cipher[1] if cipher else None,
                        "cipher_bits": cipher[2] if cipher else None,
                        "certificate": certificate,
                        "certificate_der": tls_socket.getpeercert(binary_form=True),
                    }

        except ssl.SSLError as exc:
            raise TLSScannerError(
                f"TLS error: {exc}"
            ) from exc

        except socket.timeout as exc:
            raise TLSScannerError(
                "Connection timed out."
            ) from exc

        except OSError as exc:
            raise TLSScannerError(
                f"Connection failed: {exc}"
            ) from exc
