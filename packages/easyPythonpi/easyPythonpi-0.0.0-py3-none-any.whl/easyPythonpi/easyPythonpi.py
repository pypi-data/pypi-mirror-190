"""  A python module that helps you to calculate some of the  most used calculations.....
    usage--
            Just download the file from git and unzip in ur system.
            And while using this module, just write as code-
            'from module import *' and u r good to go...
                            ~Happy programming"""

def add(x:'float', y:'float')->'float': # For addition of 2 numbers
    return  x+y

def sub(x:'float', y:'float')->'float':  # For substraction of 2 numbers
    return  x-y

def multi(x:'float', y:'float')->'float': # For multiplication of 2 numbers
    return  x*y

def div(x:'float', y:'float')->'float':   # For division of 2 numbers
    return  x/y

def mod(x:'float', y:'float')->'float':   # For finding the modulus of 2 numbers
    return  x%y

def factorial(n:'int')->'int': # To find the factorial of 2 numbers
    # single line to find factorial
    return 1 if (n == 1 or n == 0) else n * factorial(n - 1)

# To compute the factord of the argument passed
def factors(n:'int')->'int':
    factors = []
    for i in range(1, n+1):
        if n % i == 0:
            factors.append(i)
    return factors

def Area_circle(r:'double')->'double':  # To find the area of a circle using the radius r
    PI = 3.142
    return PI * (r * r)

def Perimeter_circle(r:'float')->'float': # To find the perimeter of a circle using the radius r
    PI = 3.142
    return 2 * PI * r 

def fibonacci(n:'int')->'int':  #To find the nth fibonacci series
    if n<0:
        print("Incorrect input")
    # First Fibonacci number is 0
    elif n==1:
        return 0
    # Second Fibonacci number is 1
    elif n==2:
        return 1
    else:
        return fibonacci(n-1)+fibonacci(n-2)

def sort(list:'list'):    # To bubble sort and array or list
    for i in range(len(list) - 1, 0, -1):
        for j in range(i):
            if list[j] > list[j + 1]:
                temp = list[j]
                list[j] = list[j + 1]
                list[j + 1] = temp
                
#method to print the 1st prime number between the range
def printprime(start:'int',end:'int')->'list':
    if start<=0:
            start=2
    p=[]        
    for i in range(start,end+1):
                j=0
                for k in range(2,i):
                            if i%k==0:
                                    j=1
                                    break
                if j==0:
                        p.append(i)
                        
    return p                          
#A method to convert Hexadecimal input to binary numbers
def hex2bin(x:'hex')->'bin':
    x=str(x)
    r=''
    for i in x:
        if i=='A':
            r=r+'1010'
        elif i=='B':
            r=r+'1011'
        elif i=='C':
            r=r+'1100'
        elif i=='D':
            r=r+'1101'
        elif i=='E':
            r=r+'1110'
        elif i=='F':
            r=r+'1111'
        else:
            h=bin(int(i))
            n=h[2:]
            for j in range(4):
               if len(n)<4:
                    n='0'+n
                    
            r=r+n
    return r
    

#A method to convert Octal input to binary numbers
def oct2bin(x:'oct')->'bin':       
    r='' 
    x=str(x)
    for i in x:        
        h=bin(int(i))
        n=h[2:]
        for i in range(3):
                if len(n)<3:
                    n='0'+n
        r=r+n            
    return r

#A method to convert binary input to decimal numbers
def bin2dec(x:'bin')->'dec': 
    x=list(str(x))
    l=len(x)
    a=0
    r=0
    for i in range(l-1,-1,-1):
            
            r=r+(int(x[i])*(2**a))
        
            a=a+1
    return r                  
             

def createarray(length:'int',dtype='int')->'array':   # To create an array of entered length and entered data type(interger data type is a default data type)
    import numpy as np 
    a=[]  #empty list
    for i in range(length):
        # if entered dtype is an interger
            if dtype=='int':
                        e=int(input(f"Enter {i+1} element : "))
                        a.append(e)
        # if entered dtype is a string
            elif dtype=='str' or dtype=='string':
                                e=str(input("Enter {i+1} element : "))
                                a.append(e)
        # if entered dtype is a float                         
            elif dtype=='float':
                                e=float(input("Enter {i+1} element : "))
                                a.append(e)
                                
                                    
    b=np.array(a)    
    return b

def arrayrev(array:'array')->'array':        # To reverese the array elements
    import numpy as np
    r=[]
    for i in range(len(array)-1,-1,-1):
                r.append(array[i])
    a=np.array(r)
    return a

def ispalindrome(x:'str')->'str':        # To check if the given parameter is palindrome or not
    x=str(x)  #explicitly convert into string data type so as to iterate through each character
    r=''
    for i in range(len(x)-1,-1,-1):
                r=r+x[i]
    if x==r:    # if the parameter get matched with its reverse then returns true othewise false
            return True
    else:
            return False
                   
                   

def even_or_odd(data:'int'):
    try : 
        if data%2==0:
                    return 'even'
        else:
                    return 'odd'
        
    except:
        print("\nError occured, parameter passed should be purely numeric") 


#Linked list                   
                  
def create_node(data:'int')->'Linked list':
    class node:
        def __init__(self,data):
            self.data=data
            self.next=None
    
    a=node(data)
    return a
# to link a node with another node

def node_link(a:'int',b:'int'):
    a.next=b
    b.next=None
    #a=node(data1)
          
         
# to count number of nodes
                                           
def count_node(head:'node')->'int':
    if head is None:
        return 0
    else:
        temp=head
        count=0
        while(temp!=None):
                count=count+1
                temp=temp.next
        return count   

# to diplay a linked list whose header node is passed as an argument                  

def display_nodes(head:'node')->'int':
    t=head
    while t is not None:
        print(t.data,"->",end="")
        t=t.next
    print("NULL")
                        

# Matrix problems

def matrix_add(array1:'array',array2:'array')->'array':
    import numpy as np
    
    result=np.array(array1)+np.array(array2)
    return result


def matrix_sub(array1:'array',array2:'array')->'array':
    import numpy as np
    
    result=np.array(array1)-np.array(array2)
    return result

 # Multiplication of two                   
def matrix_mul(matrix1:'array',matrix2:'array')->'array':
    import numpy as np
    matrix1=np.array(matrix1)  # converting list into array
    matrix2=np.array(matrix2)  
    a=list(matrix1.shape)      # getting the shape of the array
    b=list(matrix2.shape)
    if len(a)==1:
        k=a[0]              # suppose if row is one , for eg [1,2,3] ,then shape returns (3,) instead of [1,3].. 
        a[1]=k    
        a[0]=1              # here first element becomes last element and in place of first element , 1 is appended..
    if a[1]==b[0]:       # from matrix multiplication convention, number of columns of first matrix needs to be equal to number of rows of second matrix
        tt=[]
        for i in range(b[0]):
            u=[]
            for j in range(b[0]):
                u.append(matrix2[j][i])
            tt.append(u)
        t=np.array(tt)   # arrays of coloumn of second matrix
        pp=[]
        
        for k in range(b[0]):
            ar=[]
            for l in range(b[0]):
                y=matrix1[k]*t[l]  # multiplication of rows and columns
                ar.append(list(y)) # appending the result into a list
            pp.append(ar)
        l=[]        
        for i in pp:
            zz=[]
            for j in i:
                sum1=0
                for c in j:
                  sum1=sum1+c  # sum all the element of each row each column
                zz.append(sum1) 
            l.append(zz)    # appending the sum of each row and column of result matrix into a list
        l=np.array(l)  # convert the list of result matrix into array
        return l         
            
            

def matrix_shape(matrix1:'array')->'list':
    import numpy as np
    matrix1=np.array(matrix1)  
    a=list(matrix1.shape)      
    if len(a)==1:
            k=a[0]             
            a[1]=k    
            a[0]=1                                                                                                            
    return a                 #returns shape of a matrix              
                      
                          
                      

def matrix_transpose(matrix1:'array')->'array':
    import numpy as np
    matrix1=np.array(matrix1)  # converting list into array
    a=list(matrix1.shape)      # getting the shape of the array
    tt=[]
    for i in range(a[0]):
                u=[]
                for j in range(len(a)):
                        u.append(matrix1[j][i])
                tt.append(u)
    t=np.array(tt)   # get a transpose of matrix1
    return t       
                                            
def remove_punctuation(my_str:'str')->'str':
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    # remove punctuations from the string
    no_punct = ""
    #run a for loop and traverse every element in a string and check ,if char is not match with punctuations char then it will add in no_punct
    for char in my_str:
        if char not in punctuations:
            no_punct = no_punct + char
    #return no_punct
    return no_punct

def count_vowels(ip_str:'str')->'int':
    # string of vowels
    vowels = 'aeiou'
    # make it suitable for comparisions
    ip_str = ip_str.casefold()

    # make a dictionary with each vowel a key and value 0
    count = {}.fromkeys(vowels,0)

    # count the vowels
    for char in ip_str:
        if char in count:
            count[char] += 1
            
    #return the count dictionary
    return count

