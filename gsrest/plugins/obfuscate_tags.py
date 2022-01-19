def post_processing(request, response_item):
    print(f'requets {request}')
    if not response_item['is_public']:
        response_item['label'] = ''
