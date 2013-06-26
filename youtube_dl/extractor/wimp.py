import re
import base64
from .common import InfoExtractor


class WimpIE(InfoExtractor):
    _VALID_URL = r'(?:http://)?(?:www\.)?wimp\.com/([^/]+)/'

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group(1)
        webpage = self._download_webpage(url, video_id)
        title = self._search_regex('\<meta name\="description" content="(.+?)" \/\>',webpage, 'video title')
        thumbnail_url = self._search_regex('\<meta property\=\"og\:image" content\=\"(.+?)\" />',webpage,'video thumbnail')
        googleString = self._search_regex("googleCode = '(.*?)'", webpage,'file url')
        googleString = base64.b64decode(googleString)
        final_url = self._search_regex('","(.*?)"', googleString,'final video url')
        ext = final_url.split('.')[-1]
        return [{
            'id':        video_id,
            'url':       final_url,
            'ext':       ext,
            'title':     title,
            'thumbnail': thumbnail_url,
        }]

