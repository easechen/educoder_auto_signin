import requests
import time
import json

# 账户和密码
# userid = "1522****"
# passwd = "abc***"

def login(userid, passwd, login_api):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    form = {"login":userid,"password":passwd,"autologin":'true'}
    r = requests.post(login_api, headers=header, data=form)
    return r

def getBaseInfo(r):
    _educoder_session = r.cookies['_educoder_session']
    autologin_trustie = r.cookies['autologin_trustie']
    userDict = json.loads(r.text)
    name = userDict['name']
    school = userDict['school']
    login = userDict['login']
    user_id = userDict['user_id']
    baseInfoDict = {'name':name, 'school':school, '_educoder_session': _educoder_session, 'autologin_trustie':autologin_trustie, 'login':login, 'user_id':user_id}
    return baseInfoDict

def isLoginSuccess(r):
    # print(r.text)
    if '错误的账号或密码' in r.text:
        return False
    else:
        return True

def getCourse(login, cookies):
    getCourseApi = 'https://data.educoder.net/api/users/%s/courses.json' % login
    payload = {'category':'undefined', 'status':'undefined', 'page':'1', 'per_page':'16', 'sort_by':'updated_at', 'sort_direction':'desc', 'username':login}
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    r = requests.get(getCourseApi, params=payload, cookies=cookies, headers=header)
    courseJson = json.loads(r.text)
    # 遍历课程
    i = 1
    for c in courseJson['courses']:
        print("序号   ID           课程名称         老师            学校")
        print(f'{i}、    {c["id"]}       {c["name"]}        {c["teacher"]["real_name"]}        {c["school"]}')
        i += 1
    try:
        select = int(input("请输入要进入的课程："))
        courseID = courseJson['courses'][select-1]["id"]
    except:
        input("非法输入，已退出")
        exit(0)
    # print(courseID)
    return courseID

def welcome(infoDict):
    print(f'你好，来自 {infoDict["school"]} 的 {infoDict["name"]} 。')

# 签到post
def signInPost(attendance_id, attendance_mode, code, cookies):
    signInApi = "https://data.educoder.net/api/weapps/course_member_attendances.json"
    form = {'attendance_id':attendance_id, 'attendance_mode':attendance_mode, 'code':code}
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    sr = requests.post(signInApi, data=form, cookies = cookies, headers=header)
    if 'success' in sr.text:
        return True
    return False
    
# 打印签到信息
def printSignMsg(ser):
    srJson = json.loads(ser.text)
    i = 1
    print("序号  日期        签到码")
    for ser in srJson["attendances"]:
        print(f"{i}、 {ser['attendance_date']}     {ser['attendance_code']}")
        i += 1

# 签到
def signIn(selectCourse, status, cookies):
    # 查询历史记录
    if status == 'history':
        searchApi = "https://data.educoder.net/api/courses/{0}/attendances.json?coursesId={0}&id={0}&status={1}&page=1".format(selectCourse, status)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
        ser = requests.get(searchApi, cookies=cookies, headers = header)
        printSignMsg(ser)
    if status == 'ongoing':
        searchApi = "https://data.educoder.net/api/courses/{0}/attendances.json?coursesId={0}&id={0}&status={1}&page=1".format(selectCourse, status)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
        ser = requests.get(searchApi, cookies=cookies, headers=header)
        srJson = json.loads(ser.text)
        # 如果没有正在签到
        if srJson['normal_count'] == 0:
            return 0
        # 如果有一个在签到，则直接签到
        if srJson['normal_count'] == 1:
            attendance_mode = srJson["attendances"][0]['mode']
            code = srJson["attendances"][0]['attendance_code']
            attendance_id = srJson["attendances"][0]['id']
            print("当前签到码 %s" % code)
            # 如果没有登录成功
            if not signInPost(attendance_id, attendance_mode, code, cookies):
                return -1
            # 签到成功
            else:
                return True

        print("签到数量大于1，没有实现")
        return False
if __name__=='__main__':
    print("******头歌平台自动签到脚本******")
    print("本脚本开源 https://github.com/easechen/educoder_auto_signin 如果觉得还可以，点个star吧~")
    print("----------------------------------------------------------------")
    # ---------------------------------
    # 如果手动写入，则注释这段代码
    try:
        userid = input("enter your userid:")
        passwd = input("enter your password:")
    except:
        input("非法！已退出")
    # ----------------------------------
    login_api = "https://data.educoder.net/api/accounts/login.json"

    r = login(userid, passwd, login_api)
    # 如果登录成功
    if isLoginSuccess(r):
        # 获取用户信息
        infoDict = getBaseInfo(r)
        # 打印欢迎语
        welcome(infoDict)

        # 打印课程信息，返回要签到的课程ID
        selectCourse = getCourse(infoDict['login'], r.cookies)
        selectStatus = int(input("1、签到  2、查询历史签到 3、退出:"))
        while(selectStatus != 3):
            # 签到
            if selectStatus == 1:
                i = signIn(selectCourse, "ongoing", r.cookies)
                # 如果没有签到
                if i == 0:
                    isCon = input("当前没有签到，是否持续等待并自动签到？(y or n):")
                    if isCon in ['y', 'yes']:
                        print("-----------------------------------")
                        print("正在等待签到开始······")
                        j = 0
                        tuxing = ['|','\\','-','/']
                        while(i == 0):
                            j = (j+1) % 3
                            print(f'{tuxing[j]}\b', end='')
                            i = signIn(selectCourse, "ongoing", r.cookies)        
                            time.sleep(0.5)
                    else:
                        input("已取消，任意键退出")
                        exit(0)
                if i == True:
                    print("签到成功!!!")
                    input("任意键退出")
                else:
                    print("签到出错，请提出issue！")
            # 历史记录查询 
            elif selectStatus == 2:
                signIn(selectCourse, "history", r.cookies)
            else:
                print("没有这个选项")
            selectStatus = int(input("1、签到  2、查询历史签到 3、退出:"))
        input("任意键退出！") 
    else:
        print("用户名或密码错误！！")
        input("任意键退出")