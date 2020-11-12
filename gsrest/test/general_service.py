def get_statistics(test_case):
        """Test case for get_statistics

        Get statistics of supported currencies
        """
        headers = {
            'Accept': 'application/json',
        }
        response = test_case.client.open(
            '/stats',
            method='GET',
            headers=headers)
        test_case.assert200(
                response,
                'Response body is : ' + response.data.decode('utf-8'))


def search(test_case):
    return True
