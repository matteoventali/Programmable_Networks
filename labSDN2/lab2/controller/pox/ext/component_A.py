from pox.core import core

class ComponentA (object):
   
    def __init__ (self, hello_message):
      self.hello_message = hello_message
      
    def print_hello_message (self):
      print("Component A says:", self.hello_message)

def launch ():
   component = ComponentA("my_hello_message")
   core.register("componentA", component)