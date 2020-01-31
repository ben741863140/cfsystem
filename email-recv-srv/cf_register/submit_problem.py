import requests
import time
from robobrowser import RoboBrowser

def cli(handle):
    browser = RoboBrowser(parser= 'html.parser')
    browser.open("http://codeforces.com/enter")
    enter_form = browser.get_form('enterForm')
    enter_form['handleOrEmail'] = handle
    enter_form['password'] = 'scaucf'
    browser.submit_form(enter_form)
    browser.open('http://codeforces.com/problemset/submit')
    submit_form = browser.get_form(class_='submit-form')
    submit_form['submittedProblemCode'] = '791A'
    submit_form['source'] = '#include<bits/stdc++.h>\nusing namespace std;\nint main()\n{ int a,b,count=1;\ncin >> a >> b;' \
                            'while(1){ a=a*3; b=b*2; if(a<=b) count++; else break; } cout << count;}'

    submit_form['programTypeId'] = '54'
    browser.submit_form(submit_form)
    if browser.url[-6:] != 'status':
        print(handle + ' Failed submission')
        return
    print(handle + ' Submit success')


if __name__ == '__main__':
    for i in range(123, 151):
        handle = 'scau_support' + str(i)
        cli(handle)
