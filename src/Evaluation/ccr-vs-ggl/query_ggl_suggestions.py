from requests import get


def get_suggestions(s):
    s = s + " vs"
    ggl_suggestions = lambda s:get("http://google.com/complete/search?client=gma&q="+s).json()[1]
    return ggl_suggestions(s)

def get_detailed_suggestions(s):
    ggl_suggestions = lambda s:get("http://google.com/complete/search?client=chrome&q="+s).json()[1]
    return ggl_suggestions(s)