"""Define a custom static storage class."""
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class RyrManifestStaticFilesStorage(ManifestStaticFilesStorage):
    """Define a custom static storage class."""

    manifest_strict = False
