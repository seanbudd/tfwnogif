from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

from hashlib import md5
import subprocess
from sys import stdout
import urllib.request as curl

fake_useragent = 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'
DATABASE = {}

## REPLACE WITH IMPORT
def gan_compress(image):
    return image

@view_config(route_name='main_page')
def main_page(request):
    with open('main.html') as f:
        html = f.read()
    return Response(html)

@view_config(route_name='main_css')
def main_css(request):
    with open('main.css') as f:
        css = f.read()
    return Response(css)

@view_config(route_name='main_js')
def main_js(request):
    with open('main.js') as f:
        js = f.read()
    return Response(js)

@view_config(renderer='json', route_name='compress')
def compress(request):
    if 'url' not in request.params:
        return {'error': 'no url'}
    #r = curl.Request(request.params['url'], headers={'User-Agent': fake_useragent})
    #f = curl.urlopen(r)

    ##YT TO GIF
    cmd = "youtube-dl -f 'mp4[width<720]' -g {url}".format(url=request.params['url'])
    full_url =  subprocess.check_output(cmd, shell=True).decode(stdout.encoding).strip()
    cmd = 'ffmpeg -i "{url}" -filter:v fps=fps=1/10 tmp/ffmpeg_%03d.bmp'.format(url=full_url)
    subprocess.check_output(cmd, shell=True)
    ## compress bmp files
    cmd = "magick convert -loop 0 -delay 20 tmp/ffmpeg_*.bmp tmp/out.gif"
    subprocess.check_output(cmd, shell=True)
    cmd = "rm tmp/*ffmpeg_*.bmp"
    subprocess.check_output(cmd, shell=True)
    ## END YT
    with open("tmp/out.gif", "rb") as f:
        image_blob = f.read()
    if len(image_blob) == 0:
        return {'error': 'no url'}
    compressed = gan_compress(image_blob)
    guid = md5(compressed).hexdigest()
    savings = len(compressed)/len(image_blob)
    DATABASE[guid] = compressed
    return {'success': True, 'savings': savings, 'guid': guid}


@view_config(route_name='get_gif')
def get_gif(request):
    resp = Response(content_type='application/json')
    if 'guid' not in request.params:
        resp.body = {'error': 'no id'}
        return resp
    guid = request.params['guid']
    if guid not in DATABASE:
        resp.body = {'error': 'bad id'}
        return resp
    resp = Response(content_type='image/gif')
    resp.body = DATABASE[request.params['guid']]
    return resp

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('main_page', '')
        config.add_route('main_css', '/main.css')
        config.add_route('main_js', '/main.js')
        config.add_route('compress', '/compress')
        config.add_route('get_gif', '/get_gif')
        config.scan()
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()