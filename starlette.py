'''
AVATAR-SERVICE

@author: PurePeace
@version: 0.1

'''

from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route
from starlette.types import Send
from os.path import isfile
from os import stat as os_stat
import stat
from hashlib import md5
from datetime import timezone, datetime


# your avatars dir
avatarDir = 'avatars/'


# get GMT time string
def format_timetuple(timetuple):
    return '%s, %02d %s %04d %02d:%02d:%02d %s' % (
        ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][timetuple[6]],
        timetuple[2],
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][timetuple[1] - 1],
        timetuple[0], timetuple[3], timetuple[4], timetuple[5],
        'GMT'
    )


def file_headers(stat_result, conten_type='image/png'):
    return {
        'last-modified': format_timetuple(datetime.fromtimestamp(stat_result.st_mtime, timezone.utc).timetuple()), 
        'etag': md5((str(stat_result.st_mtime) + "-" + str(stat_result.st_size)).encode()).hexdigest(),
        'cache-control': 'public, max-age=7200',
        'content-type': conten_type,
        'content-length': str(stat_result.st_size)
    }


# same as os.path.isfile
def isfile(path):
    try: st = os_stat(path)
    except OSError: return False
    return stat.S_ISREG(st.st_mode)


def full_path(user_id, file_endwith='png'):
    return f'{avatarDir}{user_id}.{file_endwith}'


def get_avatar_path(user_id, default='-1'):
    path = full_path(user_id)
    if not isfile(path): path = full_path(default)
    return path


def file_response(file_path, byte_content):
    async def Response(scope, receive, send):
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [
                (k.lower().encode("latin-1"), v.encode("latin-1"))
                for k, v in file_headers(os_stat(file_path)).items()
            ]
        })
        await send({"type": "http.response.body", "body": byte_content})
    return Response


# interface: avatar
async def get_user_avatar(request):
    user_id = request.path_params['user_id']
    file_path = get_avatar_path(user_id)
    with open(file_path, 'rb') as file: byte_content = file.read()

    # Optimized here: encapsulated a special file_response(faster)
    # return Response(content=byte_content, media_type='image/png', headers=file_headers(os_stat(file_path)))
    return file_response(file_path, byte_content)


# interfaces
routes = [
    Route("/{user_id}", endpoint=get_user_avatar)
]


app = Starlette(routes=routes)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', host='127.0.0.1', port=5000, workers=2, access_log=False)