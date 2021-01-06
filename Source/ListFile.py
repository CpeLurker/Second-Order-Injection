import os
global script_plugin 

from color import end, red, green,good,que 
script_plugin = []
'''
    Parameter：源码路径
    Function ：构建目录结构

'''
def ListFile(file_path, level=0):
       
    level+=2;
    file_list = os.listdir(file_path)
    for filename in file_list:
        try:
            if os.path.splitext(filename)[1] == '':
                print("%s-%s"%(green,end)*level, end='')
                print("%s|%s"%(green,end), end='')
                print(filename)
            if os.path.splitext(filename)[1] == '.php':
                print("%s-%s"%(green,end)*level, end ='')
                print("%s|%s"%(green,end), end='')
                print(filename)
            name = os.path.join(file_path,filename)
            if os.path.splitext(name)[1] == '.php':
                print("%s-%s"%(green,end)*level, end ='')
                print("%s|%s"%(green,end), end = '')
                print(os.path.basename(filename))
                script_plugin.append(name)
            if os.path.isdir(name):
                ListFile(name,level)
        except:
            pass
    return script_plugin

    
       
    
    
        



if __name__ == '__main__':

    file_path = r'E:\PHPStudy\PHPCMS'  
    info = ListFile(file_path)
    