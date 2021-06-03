# python judge

# import requred packages
import os, sys, time, subprocess, threading

os.system("")

SUCCESS = 0
FAILURE = 1
TLE = 31744

CPP_COMPILE_COMMAND = "g++ -o {} {}.cpp  -std=c++17 -pedantic -Wall -Wshadow -Wformat=2 -Wfloat-equal -Wconversion -Wlogical-op -Wcast-qual -Wcast-align -fmax-errors=1".format
CPP_EXECUTION_COMMAND = "timeout {} ./{} < {} > {} 2> null".format
COMPILE_ERROR_MESSAGE = "Compilation error.\033[0m"
TLE_MESSAGE = "\033[36m\033[01m\033[09m\033[47mTime Limit Exceded.\033[0m"
RTE_MESSAGE = "\033[36m\033[01m\033[09m\033[47mRun Time Error.\033[0m"
SUCCESS_MESSAGE = "\033[32m\033[01m\033[04mSuccessfully executed in {:.2f} seconds.\033[0m".format

# FILE PATHS
TOKEN_CHECKER_PATH = "../../checkers/./token {} {}".format

class Judge(threading.Thread):
  compile_status = SUCCESS
  def __init__(self, file_name, time_limit):
    threading.Thread.__init__(self)
    self.file_name = file_name
    self.time_limit = time_limit
    
  def compile(self, compile_first = True):
    if (compile_first == False):
      return 
    ret = os.system(CPP_COMPILE_COMMAND(self.file_name, self.file_name))
    if (ret != SUCCESS):
      compile_status = FAILURE
      print(COMPILE_ERROR_MESSAGE)
    
  def execute(self, input_file, output_file, expected_output_file):
    st = time.time()
    x = os.system(CPP_EXECUTION_COMMAND(self.time_limit, self.file_name, input_file, output_file))
    en = time.time()
    if (x == SUCCESS):
      # Check output here
      checker = Judge.Checker()
      checker.dis()
      print(SUCCESS_MESSAGE(en - st))
    elif (x == TLE):
      print(TLE_MESSAGE)
    else:
      print(RTE_MESSAGE)
    
  # run is the actuall driver function
  # do compilling and running stuffs
  def run(self):
    self.compile()
    self.execute("in", "out", "exp")
  def run_all_test(self):
    pass
  
  class Checker:
    def __init__(self, checker = TOKEN_CHECKER_PATH, error = 8):
      self.checker = checker
      self.error = error
    
    def dis(self):
      print(self.checker)
    
    
if (__name__ == "__main__"):
  j1 = Judge("sol", 1.0)
  j1.start()
  j1.join()
  
