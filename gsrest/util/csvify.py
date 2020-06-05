from werkzeug.datastructures import Headers
import gsrest.apis as Api

def create_download_header(filename):
    headers = Headers()
    headers.add('Content-Disposition', 'attachment', filename=filename)
    return headers

def toCSV(query_function):
    with Api.api.app.app_context():
        fieldnames = []
        flatDict = {}
        page_state = None
        while True:
            (page_state, rows) = query_function(page_state)
            print('row {}'.format(rows), flush=True)
            if rows is None:
                raise ValueError('nothing found')

            def flatten(item, name=""):
                if type(item) is dict:
                    for sub_item in item:
                        flatten(item[sub_item], name + sub_item + "_")
                else:
                    flatDict[name[:-1]] = item

            for row in rows:
                #for item in row.toJson():
                flatten(row)
                if not fieldnames:
                    fieldnames = ",".join(flatDict.keys())
                    yield (fieldnames + "\n")
                yield (",".join([str(item) for item in flatDict.values()]) + "\n")
                flatDict = {}

            if not page_state:
                break

