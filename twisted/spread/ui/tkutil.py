
# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from Tkinter import *

from twisted.spread import pb
from twisted.internet import tcp
from twisted import copyright

import string

#normalFont = Font("-adobe-courier-medium-r-normal-*-*-120-*-*-m-*-iso8859-1")
#boldFont = Font("-adobe-courier-bold-r-normal-*-*-120-*-*-m-*-iso8859-1")
#errorFont = Font("-adobe-courier-medium-o-normal-*-*-120-*-*-m-*-iso8859-1")

def grid_setexpand(widget):
    cols,rows=widget.grid_size()
    for i in range(cols):
        widget.columnconfigure(i,weight=1)
    for i in range(rows):
        widget.rowconfigure(i,weight=1)

class CList(Frame):
    def __init__(self,parent,labels,**kw):
        Frame.__init__(self,parent)
        self.labels=labels
        self.lists=[]
        kw["exportselection"]=0
        for i in range(len(labels)):
            Label(self,text=labels[i],anchor=W,relief=RAISED).grid(column=i,row=0,sticky=N+E+W)
            box=apply(Listbox,(self,),kw)
            box.grid(column=i,row=1,sticky=N+E+S+W)
            self.lists.append(box)
        grid_setexpand(self)
        self._callall("bind",'<Button-1>',self.Button1)
        self._callall("bind",'<B1-Motion>',self.Button1)
        self.bind('<Up>',self.UpKey)
        self.bind('<Down>',self.DownKey)

    def _callall(self,funcname,*args,**kw):
        rets=[]
        for l in self.lists:
            func=getattr(l,funcname)
            ret=apply(func,args,kw)
            if ret: rets.append(ret)
        if rets: return rets
        
    def Button1(self,e):
        index=self.nearest(e.y)
        self.select_clear(0,END)
        self.select_set(index)
        return "break"

    def UpKey(self,e):
        index=self.index(ACTIVE)
        if index:
            self.select_clear(0,END)
            self.select_set(index-1)
        return "break"

    def DownKey(self,e):
        index=self.index(ACTIVE)
        if index!=self.size()-1:
            self.select_clear(0,END)
            self.select_set(index+1)
        return "break"

    def activate(self,index):
        self._callall("activate",index)

   # def bbox(self,index):
   #     return self._callall("bbox",index)

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self,*args):
        apply(self._callall,("delete",)+args)

    def get(self,*args):
        return apply(self._callall,("get",)+args)

    def index(self,index):
        return self.lists[0].index(index)

    def insert(self,index,items):
        for i in range(len(items)):
            self.lists[i].insert(index,items[i])

    def nearest(self,y):
        return self.lists[0].nearest(y)

    def see(self,index):
        self._callall("see",index)

    def size(self):
        return self.lists[0].size()

    def selection_anchor(self,index):
        self._callall("selection_anchor",index)
   
    select_anchor=selection_anchor
   
    def selection_clear(self,*args):
        apply(self._callall,("selection_clear",)+args)
        
    select_clear=selection_clear
    
    def selection_includes(self,index):
        return self.lists[0].select_includes(index)
    
    select_includes=selection_includes

    def selection_set(self,*args):
        apply(self._callall,("selection_set",)+args)

    select_set=selection_set
    
    def xview(self,*args):
        if not args: return self.lists[0].xview()
        apply(self._callall,("xview",)+args)
        
    def yview(self,*args):
        if not args: return self.lists[0].yview()
        apply(self._callall,("yview",)+args)

class GenericLogin(Toplevel):
    def __init__(self,callback,buttons):
        Toplevel.__init__(self)
        self.callback=callback
        Label(self,text="Twisted v%s"%copyright.version).grid(column=0,row=0,columnspan=2)
        self.entries={}
        row=1
        for stuff in buttons:
            label,value=stuff[:2]
            if len(stuff)==3:
                dict=stuff[2]
            else: dict={}
            Label(self,text=label+": ").grid(column=0,row=row)
            e=apply(Entry,(self,),dict)
            e.grid(column=1,row=row)
            e.insert(0,value)
            self.entries[label]=e
            row=row+1
        Button(self,text="Login",command=self.doLogin).grid(column=0,row=row)
        Button(self,text="Cancel",command=self.close).grid(column=1,row=row)
        self.protocol('WM_DELETE_WINDOW',self.close)
    
    def close(self):
        self.tk.quit()
        self.destroy()

    def doLogin(self):
        values={}
        for k in self.entries.keys():
            values[string.lower(k)]=self.entries[k].get()
        self.callback(values)
        self.destroy()

class Login(Toplevel):
    def __init__(self, callback,
             referenced = None,
             initialUser = "guest",
                 initialPassword = "guest",
                 initialHostname = "localhost",
                 initialService  = "",
                 initialPortno   = pb.portno):
        Toplevel.__init__(self)
        version_label = Label(self,text="Twisted v%s" % copyright.version)
        self.pbReferenced = referenced
        self.pbCallback = callback
        # version_label.show()
        self.username = Entry(self)
        self.password = Entry(self,show='*')
        self.hostname = Entry(self)
        self.service  = Entry(self)
        self.port     = Entry(self)

        self.username.insert(0,initialUser)
        self.password.insert(0,initialPassword)
        self.service.insert(0,initialService)
        self.hostname.insert(0,initialHostname)
        self.port.insert(0,str(initialPortno))

        userlbl=Label(self,text="Username:")
        passlbl=Label(self,text="Password:")
        servicelbl=Label(self,text="Service:")
        hostlbl=Label(self,text="Hostname:")
        portlbl=Label(self,text="Port #:")
        self.logvar=StringVar()
        self.logvar.set("Protocol PB-%s"%pb.Broker.version)
        self.logstat  = Label(self,textvariable=self.logvar)
        self.okbutton = Button(self,text="Log In", command=self.login)

        version_label.grid(column=0,row=0,columnspan=2)
        z=0
        for i in [[userlbl,self.username],
                  [passlbl,self.password],
                  [hostlbl,self.hostname],
                  [servicelbl,self.service],
                  [portlbl,self.port]]:
            i[0].grid(column=0,row=z+1)
            i[1].grid(column=1,row=z+1)
            z = z+1

        self.logstat.grid(column=0,row=6,columnspan=2)
        self.okbutton.grid(column=0,row=7,columnspan=2) 

        self.protocol('WM_DELETE_WINDOW',self.tk.quit)

    def loginReset(self):
        self.logvar.set("Idle.")
        
    def loginReport(self, txt):
        self.logvar.set(txt)
        self.after(30000, self.loginReset)

    def login(self):
        host = self.hostname.get()
        port = self.port.get()
        service = self.service.get()
        # Maybe we're connecting to a unix socket, so don't make any
        # assumptions
        try:
            port = int(port)
        except:
            pass
        user = self.username.get()
        pswd = self.password.get()
        b = pb.Broker()
        self.broker = b
        b.requestIdentity(user, pswd,
                             callback   = self.gotIdentity,
                             errback    = self.couldNotConnect)
        b.notifyOnDisconnect(self.disconnected)
        tcp.Client(host, port, b)

    def gotIdentity(self,identity):
        identity.attach(self.service.get(),self.pbReferenced,pbcallback=self.pbCallback)

    def couldNotConnect(self,*args):
        self.loginReport("could not connect.")

    def disconnected(self,*args):
        self.loginReport("disconnected from server.")
