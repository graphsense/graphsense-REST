from werkzeug.datastructures import Headers
import gsrest.apis as Api


def create_download_header(filename):
    headers = Headers()
    headers.add('Content-Disposition', 'attachment', filename=filename)
    return headers


def toCSV(query_function):
    with Api.api.app.app_context():
        fieldnames = []
        flat_dict = {}
        page_state = None
        while True:
            (page_state, rows) = query_function(page_state)
            if rows is None:
                raise ValueError('nothing found')

            def flatten(item, name=""):
                if type(item) is dict:
                    for sub_item in item:
                        flatten(item[sub_item], name + sub_item + "_")
                else:
                    flat_dict[name[:-1]] = item

            for row in rows:
                flatten(row)
                if not fieldnames:
                    fieldnames = ",".join(flat_dict.keys())
                    yield (fieldnames + "\n")
                yield (",".join([str(item) for item in flat_dict.values()]) +
                       "\n")
                flat_dict = {}

            if not page_state:
                break
