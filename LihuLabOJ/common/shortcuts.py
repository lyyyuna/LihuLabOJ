from rest_framework.response import Response


def success_response(result):
    return Response(data={"code": 0, "data": result})


def error_response(reason):
    return Response(data={'code': 1, 'data': reason})