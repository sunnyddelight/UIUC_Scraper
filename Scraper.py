import requests
import cookielib
jar=cookielib.CookieJar()
login_url='https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1'
acc_pwd = {'login':'Log In',
            'email':'syduan2',
            'password':'Rwylet314!',
            'disableThirdPartyLogin':'false',
            'loginRedirect':'',
            'includeWorkflow':'',
            'login':'Log In'
         }
