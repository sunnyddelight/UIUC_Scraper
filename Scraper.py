import cookielib
import mechanize
br=mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Chrome')]

#br.open('https://github.com/login')
#for f in br.forms():
#    print f
subj='CS'


br.open('https://eas.admin.uillinois.edu/eas/servlet/EasLogin?redirect=https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1')
br.select_form(nr=0)
br.form['inputEnterpriseId']='syduan2'
br.form['password']='Rwylet314?'
br.submit()

br.open('https://ui2web1.apps.uillinois.edu/BANPROD1/bwskfcls.p_sel_crse_search')

br.select_form(nr=1)
br.form['p_term']=['120151']
br.open(br.form.click())
#br.open('https://ui2web1.apps.uillinois.edu/BANPROD1/bwckgens.p_proc_term_date')
forms=br.forms()
forms.next()
focus=forms.next()
focus.set_value([subj],  nr=13)

    #.set_value(subj,  nr=0)

#br.form['sel_subj']=[subj]
print br.open(focus.click(name='SUB_BTN')).read()
for f in br.forms():
    print f



