class Util(object):
    def check_user(self,request):
        #从cookie中取出username
        username = (request.session.get('username','')).strip()
        #获得所有cookie
        cookie_list = request.COOKIES
        if ("sessionid" in cookie_list) and (username is not None):
            return username
        else:
            return ""