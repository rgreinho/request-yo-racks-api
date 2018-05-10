from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class RyrManifestStaticFilesStorage(ManifestStaticFilesStorage):
    manifest_strict = False
