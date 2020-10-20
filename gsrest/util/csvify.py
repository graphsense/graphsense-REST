from werkzeug.datastructures import Headers
import operator


def create_download_header(filename):
    headers = Headers()
    headers.add('Content-Disposition', 'attachment', filename=filename)
    return headers


def to_csv(query_function):
    fieldnames = []
    flat_dict = {}
    page_state = None
    while True:
        (page_state, rows) = query_function(page_state)
        if rows is None:
            raise ValueError('nothing found')

        def flatten(item, name=""):
            if 'to_dict' in dir(item):
                item = item.to_dict()
            if isinstance(item, dict):
                for sub_item in item:
                    flatten(item[sub_item], name + sub_item + "_")
            else:
                flat_dict[name[:-1]] = item

        for row in rows:
            flatten(row)
            if not fieldnames:
                fieldnames = sorted(flat_dict.keys())
                yield ','.join(fieldnames) + "\n"
            yield (",".join([str(flat_dict[key]) for key in fieldnames]) +
                   "\n")
            flat_dict = {}

        if not page_state:
            break
