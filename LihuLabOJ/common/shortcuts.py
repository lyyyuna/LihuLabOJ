from rest_framework.response import Response


def success_response(result,*args, **kwargs):
    return Response(data={"code": 0, "data": result},*args, **kwargs)


def error_response(reason,*args, **kwargs):
    return Response(data={'code': 1, 'data': reason},*args, **kwargs)