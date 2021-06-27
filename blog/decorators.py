from rest_framework.response import Response
from rest_framework import status

def only_allow_this_fields(validFields):
  def inner(func):
    def wrapper(*args, **kwargs):
      fields = []
      for key in args[1].data.keys():
        if key not in validFields:
          fields.append("{} is not allowed".format(key))
      if fields:
        return Response(fields, status=status.HTTP_400_BAD_REQUEST)
      else:
        return func(*args, **kwargs)
    return wrapper
  return inner