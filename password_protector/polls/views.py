from django.shortcuts import render, redirect
import os
from xlutils import copy
from xlrd import open_workbook
from openpyxl import Workbook
import crypt
import xlrd
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.
class Mainpage:
 def home(self,request):
    return render(request,'home.html',{'name':'To Password Protector'})
 def btn_login(self,request):
    return render(request,"login.html")
 def btn_register(self,request):
    return render(request,"register.html")
 def register(self,request):#Association : Type (Composition)#
     w=Write()
     return w.register(request)
 def login(self,request):#Association : Type (Composition)#
     r=Read()
     return r.login(request)
 def add_passw(self,request):#Association : Type (Composition)#
     a=Add_password()
     return a.add_passw(request)
 def adding_password(self,request):
     return render(request, "Add_passwords.html")
 def viewing_password(self,request):#Association : Type (Composition)#
     v=View_passw()
     return v.viewing_password(request)


class Write:
    ## Class Attributes##
    row=1
    clm=0
    name=None
    email = None
    passw = None
    def register(self,request):#Method Overriding: Overriding method register of class register #
        ## POST is to get the input##
        Write.name=request.POST['username']
        Write.email=request.POST['email_address']
        password=request.POST['password']
        Write.passw = crypt.crypt(password)
        Write.write_in_file()
        return render(request, "Add_passwords.html")
    @classmethod
    def write_in_file(cls):
      try:
        book=open_workbook('/home/ubuntu/PycharmProjects/mysite/mysite/polls/password.xlsx')
        book = copy(book)  # creates a writeable copy
        sheet = book.get_sheet(0)  # get a first sheet
        sheet.write(Write.row,Write.clm,Write.name)
        sheet.write(Write.row,Write.clm+1,Write.email)
        sheet.write(Write.row,Write.clm+2,Write.passw)
        Write.clm+=3
        book.save('password.xlsx')
      except FileNotFoundError:
          w = Write()
          w.initial_write()

    @staticmethod
    def initial_write():## To write initial headings in excel file##
        book=Workbook()
        sheet = book.active
        sheet['A1']='Username'
        sheet['B1']='Email Address'
        sheet['C1']='Password'
        book.save('password.xlsx')

class Read: ## Check if username and password is registered or not##
    u=0
    p=0
    def login(self,request):
        loc = "/home/ubuntu/PycharmProjects/mysite/mysite/polls/password.xlsx"
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                for i in range(sheet.ncols):
                    if sheet.cell_value(1, i-1)== username:
                        if crypt.crypt(password, sheet.cell_value(1, i + 1)) == sheet.cell_value(1, i + 1):
                            Read.u=i-1
                            Read.p=i+1
                            return render(request, "login_options.html")
                else:
                       messages.error(request, 'username or password not correct')
                       return redirect('login')


class Add_password(Read):##Inheritance: Inheriting from Write##
  def add_passw(self,request):
      self.fb= request.POST['fb']
      self.gmail= request.POST['gmail']
      self.yahoo= request.POST['yahoo']
      self.login(request)
      return render(request, "Add_passwords.html")
  def login(self,request):## Method overriding: Overriding login method of class Read ##
      book = open_workbook('/home/ubuntu/PycharmProjects/password_protector/password_protector/polls/password.xlsx')
      book = copy(book)  # creates a writeable copy
      sheet = book.get_sheet(0)  # get a first sheet
      sheet.write(2, Read.u, "Facebook")
      sheet.write(3, Read.u, "Gmail")
      sheet.write(4, Read.u, "Yahoo")
      sheet.write(2, Read.p, self.fb)
      sheet.write(3, Read.p, self.gmail)
      sheet.write(4, Read.p, self.yahoo)
      book.save('password.xlsx')

class View_passw(Read): ## View passwords added by users ##
    def viewing_password(self,request):
        loc = "/home/ubuntu/PycharmProjects/password_protector/password_protector/polls/password.xlsx"
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        fb=sheet.cell_value(2, Read.p)
        gmail=sheet.cell_value(3, Read.p)
        yahoo=sheet.cell_value(4, Read.p)
        return render(request,"view_password.html",{'fb':fb,'gmail':gmail,'yahoo':yahoo})
m=Mainpage()
## Creating file in the same project ##
os.chdir('/home/ubuntu/PycharmProjects/password_protector/password_protector/polls')

## To check whether excel file exist or not , if doesnot exit, creates it##
# if os.path.isfile('/home/ubuntu/PycharmProjects/mysite/mysite/polls/password.xlsx')==True:
#     pass
# else:
#     w=Write()
#     w.initial_write()






 #####
 # import crypt
 # passw = crypt.crypt('abcd')
 # valid_pass = crypt.crypt('abcd', passw) == passw
 # valid_pass
 ####