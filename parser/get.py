import os, sys, threading, requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

#colorer starts
os.system("")
class colorer:
  reset = '\033[0m'
  bold = '\033[01m'
  disable = '\033[02m'
  underline = '\033[04m'
  reverse = '\033[07m'
  strikethrough = '\033[09m'
  invisible = '\033[08m'
  class foreground:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'
  class background:
    black = '\033[40m'
    red = '\033[41m'
    green = '\033[42m'
    orange = '\033[43m'
    blue = '\033[44m'
    purple = '\033[45m'
    cyan = '\033[46m'
    lightgrey = '\033[47m'

  def write(token, color = None):
    if (color == None):
      print(colorer.reset, end = '')
    else:
      print(color, end = '')
    print(token, end = '')
    print(colorer.reset, end = '')

# MESSAGE
def warning(token):
  colorer.write(token, colorer.foreground.yellow)
def error(token):
  colorer.write(token, colorer.foreground.lightred)
def greeting(token):
  colorer.write(token, colorer.foreground.lightgreen)
def system(token):
  colorer.write(token, colorer.foreground.lightcyan)
def task(token):
  colorer.write(token, colorer.foreground.lightblue)
def general(token):
  colorer.write(token)

class parser:
  #instance
  root = "https://codeforces.com"
  contest_url = None
  def __init__(self, contest_id):
    self.contest_id = contest_id
    self.contest_url = self.root + "/contest/" + self.contest_id + "/"
          
  #methods
  def get_problem_names(self):
    try:
      html_req = requests.get(self.contest_url)
    except:
      return None
    soup = BeautifulSoup(html_req.text, "html.parser")
    body = soup.find('table', attrs = {'class':'problems'})
    problem_title = soup.title 
    if (body == None):
      #link broken or contest is not started
      return None
    
    #display the title
    greeting("\t\t\t\t\t\t\t *** Bismillahir Rahmanir Rahim *** \n")
    greeting("\t\t\t  \t\t\t" + str(soup.title.string) + "\n")
    problems = []
    for tr in body.findAll('tr'):
      td = tr.find('td', attrs = {'class':'id'})
      if (td == None):
        continue
      info = td.find('a')
      problem_link = info.get('href')
      problem_name = info.string
      problem_name = self.clean_name(problem_name)
      problems.append((problem_name, problem_link))
    return problems
  
  def get_samples(self, problem_url, dir_name):                               
    try:
      req = requests.get(problem_url)
    except:
      error("\tFailed parsing problem " + dir_name + ". Please Parse again.\n")
      return 
          
    soup = BeautifulSoup(req.text, "html.parser")
    problem_title = soup.find('div', attrs = {'class':'title'}).string
    task("    Getting problem - " + str(problem_title) + "\n")

    sample = soup.find('div', attrs = {'class':'sample-tests'})
    cnt = 1
    for inp in sample.findAll('div', attrs = {'class':'input'}):
      txt = inp.find('pre')
      sample_list = txt.contents
      val = self.gather_string(sample_list)    
      val = val.lstrip('\n')  
      f_name = dir_name
      f_name += "/input/in"
      f_name += str(cnt)
      cnt += 1
      fp = open(f_name, "w")
      fp.write(val)
      fp.close()

    #ouput part
    cnt = 1
    for inp in sample.findAll('div', attrs = {'class':'output'}):
      txt = inp.find('pre')
      sample_list = txt.contents
      val = self.gather_string(sample_list)
      val = val.lstrip('\n')  
      f_name = dir_name
      f_name += "/output/exp"
      f_name += str(cnt)
      cnt += 1
      fp = open(f_name, "w")
      fp.write(val)
      fp.close() 

  def gather_string(self, ar):
    ret = ""
    for s in ar:
      if (str(s).startswith("<") and str(s).endswith(">")):
        continue
      else :
        ret += str(s)
        ret += "\n"
    return str(ret)

  def driver(self):
    problem_info = self.get_problem_names()
    if (problem_info == None):
      error("\tConnection failed or contest link is broken. Please try again.\n")
      return 
    for info in problem_info:
      self.make_folder(info[0])
    general("\n")
    threads = []
    for info in problem_info:
      sample = threading.Thread(target = self.get_io, args = [info[0], self.root + info[1]])
      threads.append(sample)
    for thread in threads:
      thread.start()
    for thread in threads:
      thread.join()
        
  def get_io(self, name, link):
    self.get_samples(link, name)
    self.copy_files(name)
  
  def copy_files(self, dir_name):
    f_bat = open("run.bat", "r")
    bat = f_bat.read()
    f_bat.close()
    path = dir_name
    path += "/"
    path += "run.bat"
    f_bat = open(path, "w")
    f_bat.write(bat)
    f_bat.close()
        
  def make_folder(self, name):
    try:
      os.mkdir(name)
      system("\tWarning!!! Creating directory " + name + "...\n")
    except:
      warning("\tWarning!!! Updating directory " + name + "...\n")
    try:
      os.mkdir(name + "/input")
      system("\t  -> Warning!!! Creating directory " + "input" + "...\n")
    except:
      warning("\t  -> Warning!!! Updating directory " + "input" + "...\n")
    try:
      os.mkdir(name + "/output")
      system("\t  -> Warning!!! Creating directory " + "output" + "...\n")
    except:
      warning("\t  -> Warning!!! Updating directory " + "output" + "...\n")
  
  def make_problem_link(self, href):
    return self.root + href + "/"

  def clean_name(self, name):
    name = name.replace(' ', '')
    name = name.replace('\t', '')
    name = name.lstrip('\r\n')
    name = name.rstrip('\r\n')      
    return name
  
#main
if (__name__ == "__main__"):
  if (len(sys.argv) < 2):
    error("\tPlease provide a contest id.\n")
    exit()
  contest_id = str(sys.argv[1])
  p = parser(contest_id)
  p.driver()
    
  