"""
Asset Discovery Certificate Parser
----------------------------------

Responsible for:

- Parsing X.509 certificates
- Extracting certificate metadata
- Detecting public key algorithm
- Detecting key size
- Calculating SHA256 fingerprint

This module does NOT:
- Open network connections
- Save to database
- Perform risk assessment
"""

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
except ImportError:
    ed25519 = None

try:
    from cryptography.hazmat.primitives.asymmetric import ed448
except ImportError:
    ed448 = None


class CertificateParser:
    """Parse X.509 certificates."""

    @staticmethod
    def parse(certificate_der: bytes) -> dict:
        """
        Parse a DER encoded certificate.
        """

        cert = x509.load_der_x509_certificate(certificate_der)

        public_key = cert.public_key()

        algorithm = "Unknown"
        key_size = None

        if isinstance(public_key, rsa.RSAPublicKey):
            algorithm = "RSA"
            key_size = public_key.key_size

        elif isinstance(public_key, ec.EllipticCurvePublicKey):
            algorithm = "ECDSA"
            key_size = public_key.key_size

        elif ed25519 and isinstance(public_key, ed25519.Ed25519PublicKey):
            algorithm = "Ed25519"

        elif ed448 and isinstance(public_key, ed448.Ed448PublicKey):
            algorithm = "Ed448"

        try:
            san = cert.extensions.get_extension_for_class(
                x509.SubjectAlternativeName
            ).value

            san_list = san.get_values_for_type(x509.DNSName)

        except x509.ExtensionNotFound:
            san_list = []

        return {

            "subject": cert.subject.rfc4514_string(),

            "issuer": cert.issuer.rfc4514_string(),

            "serial_number": hex(cert.serial_number),

            "public_key_algorithm": algorithm,

            "key_size": key_size,

            "signature_algorithm": (
                cert.signature_hash_algorithm.name
                if cert.signature_hash_algorithm
                else None
            ),

            "valid_from": cert.not_valid_before_utc,

            "valid_to": cert.not_valid_after_utc,

            "fingerprint_sha256": cert.fingerprint(
                hashes.SHA256()
            ).hex(),

            "subject_alternative_names": san_list,
        }
