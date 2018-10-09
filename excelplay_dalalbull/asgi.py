import os
import channels.layers #Not required for channels>=2.0.0

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "excelplay_dalalbull.settings")

channel_layer = channels.layers.get_channel_layer()