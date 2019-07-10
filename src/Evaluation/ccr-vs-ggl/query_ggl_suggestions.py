from requests import get


def get_suggestions(s):
<<<<<<< HEAD
    s = s + " vs"
=======
>>>>>>> 413f56534c7334783889962ccbc655d8cfa42617
    ggl_suggestions = lambda s:get("http://google.com/complete/search?client=gma&q="+s).json()[1]
    return ggl_suggestions(s)

def get_detailed_suggestions(s):
    ggl_suggestions = lambda s:get("http://google.com/complete/search?client=chrome&q="+s).json()[1]
    return ggl_suggestions(s)