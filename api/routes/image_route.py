# image_route

from db import get_session
import io

def fetch_images(sid:str, num_imgs:int = 1):

    query = _build_image_query(sid, num_imgs)
    with get_session() as session:
        res = session.execute(query)
    return _build_response(res)



def _build_image_query(sid, num_imgs):
    return f"""
            SELECT
                time, attachment
            FROM 
                data.sdata 
            WHERE 
                sid='{sid}'
                AND 
                attachment is NOT NULL
            ORDER BY 
                time desc 
            LIMIT {num_imgs};
            """

def _build_response(result):
    resp = {}
    for row in result:
        resp[str(row.time)] = row.attachment.tobytes()
    return io.BytesIO(row.attachment.tobytes())
"""
29	"c_contiguous"
30	"cast"
31	"contiguous"
32	"f_contiguous"
33	"format"
34	"hex"
35	"itemsize"
36	"nbytes"
37	"ndim"
38	"obj"
39	"readonly"
40	"release"
41	"shape"
42	"strides"
43	"suboffsets"
44	"tobytes"
45	"tolist"
46	"toreadonly"
"""