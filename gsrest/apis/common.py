def page_parser(api):
    page_parser = api.parser()
    page_parser.add_argument(
        "page", type="str", location="args",
        help="Resumption token for retrieving the next page")
    return page_parser
