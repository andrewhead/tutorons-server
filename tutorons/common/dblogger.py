from tutorons.common.models import Block, ServerQuery
from tutorons.common.htmltools import get_css_selector
import datetime

class DBLogger():

    def log(self, request, region=None):
        # extract request fields
        url = request.POST.get('origin')
        path = request.path_info
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        r_type = request.path_info.split('/')[1]
        r_method = request.path_info.split('/')[2]
        if not region:  # log query
            q = ServerQuery(ip_addr=ip, path=path)
            q.save()
        if region:  # log region
            block_hash = hash(region.node)
            block_type = region.node.name
            # find corresponding query
            q = ServerQuery.objects.filter(ip_addr=ip, path=path)[0]
            # find/create block
            b = Block.objects.filter(url=url, block_type=block_type, block_hash=block_hash)
            if not b:
                b = Block(url=url, block_type=block_type, block_text=region.node, block_hash=block_hash)
            else:
                b = b[0]
            b.save()
            q.region_set.create(
                block=b,
                node=get_css_selector(region.node),
                start=region.start_offset,
                end=region.end_offset,
                string=region.string,
                r_type=r_type,
                r_method=r_method)
        return q.id

    def update_server_end_time(self, qid):
        q = ServerQuery.objects.filter(id=qid)[0]
        q.end_time = datetime.datetime.now()
        q.save()

