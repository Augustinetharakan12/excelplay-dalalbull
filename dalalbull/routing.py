from channels.routing import include

from common.routing import channel_routing as common_cr
from dalalbull.routing import channel_routing as dalalbull_cr

channel_routing = [
    include( dalalbull_cr, path=r'^/channel/dalalbull'),
    include( common_cr, path=r'^/channel'),
]