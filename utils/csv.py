import csv

from django.http import StreamingHttpResponse


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def stream_csv_list_of_list_view(
        rows: list,
        file_name: str,
        headers: list = None) -> StreamingHttpResponse:
    """
    A view that streams a large CSV file from a list of lists plus a list of headers
    :param rows: List of list of rows of the form [[v1,v2,v3],[v1,v2,v3]]
    :param file_name: the name of the output file
    :param headers: List of values of the form [[h1, h1, h3]]
    :return: StreamingHttpResponse with the CSV
    """
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.

    pseudo_buffer = Echo()
    if headers:
        final_rows = headers + rows
    else:
        final_rows = rows
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse(
        (writer.writerow(row) for row in final_rows),
        content_type="text/csv; charset=utf-8")
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(
        file_name)
    return response


def iter_items(items, headers, pseudo_buffer):
    writer = csv.DictWriter(pseudo_buffer, fieldnames=headers)
    for h in headers:
        yield pseudo_buffer.write(h)
        yield pseudo_buffer.write(',')
    yield writer.writerow({})

    for item in items:
        yield writer.writerow(item)


def stream_csv_list_of_dicts_view(rows: list, file_name: str,
                                  headers: list) -> StreamingHttpResponse:
    """
    A view that streams a large CSV file from a list of dictionaries plus a list of headers
    :param rows: List of dicts of rows of the form [{h1:v1,h2:2,h3:v3},{h1:v1,h2:2,h3:v3}]
    :param file_name: the name of the output file
    :param headers: List of values of the form [[h1, h1, h3]]
    :return: StreamingHttpResponse with the CSV
    """
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.

    pseudo_buffer = Echo()
    response = StreamingHttpResponse(
        streaming_content=(iter_items(rows, headers, pseudo_buffer)),
        content_type='text/csv; charset=utf-8',
    )
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(
        file_name)
    return response
