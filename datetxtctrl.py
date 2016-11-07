# -*- coding: utf-8 -*-

import wx
import re
import calendar
import datetime
from widgets.calendardialog import CalendarWindow

WIDTH=115
HEIGHT=25
#pattern='^[0-9]{4}-(([1-9])|(0[1-9])|([12]))-(0[1-9]|[1-2][0-9]|3[0-1])$'
empty_string=re.compile('^\s*$')
pattern='^\s*[0-9]{4}-[0-1]{,1}[0-9]{1}-[0-3]{,1}[0-9]{1}\s*$'
correct_data = re.compile(pattern)
set31={1,3,5,7,8,10,12}
set30={4,6,9,11}

class DateTxtCtrl(wx.TextCtrl):
    def  __init__(self,parent):
        wx.TextCtrl.__init__(self, parent,size=(WIDTH,HEIGHT),style=wx.TE_CENTRE)
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial MS')
        self.SetFont(font)
        self.SetBackgroundColour(wx.Colour(234,255,175))

class DateWidgets(wx.Window):
    def __init__(self,parent):    
        wx.Window.__init__(self,parent)
        self.txt_od=DateTxtCtrl(self)
        self.btn_cal_od=wx.Button(self,2,'Od',size=(30,30))
        self.txt_do=DateTxtCtrl(self)
        self.btn_cal_do=wx.Button(self,3,'Do',size=(30,30))
        self.selfSizer=wx.BoxSizer(wx.HORIZONTAL)
        boxdataOd=wx.BoxSizer(wx.HORIZONTAL)
        boxdataDo=wx.BoxSizer(wx.HORIZONTAL)
        boxdataOd.Add(self.txt_od, 0, wx.EXPAND,2)
        boxdataOd.Add(self.btn_cal_od, 0, wx.RIGHT,30)
        boxdataDo.Add(self.txt_do, 0,wx.EXPAND,2)
        boxdataDo.Add(self.btn_cal_do, 0, wx.EXPAND,2)
        self.selfSizer.Add(boxdataOd)
        self.selfSizer.Add(boxdataDo)
        self.SetSizer(self.selfSizer)
        self.selfSizer.Layout()
        self.Bind(wx.EVT_BUTTON, self.OnCalOd, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnCalDo, id=3)

    def GetDaty(self):
        od=self.txt_od.GetValue()
        do=self.txt_do.GetValue()

        if empty_string.match(do):
            do=datetime.datetime.now().strftime("%Y-%m-%d")
            self.txt_do.SetValue(do)

        if empty_string.match(od):
            od="2010-04-01"

        if correct_data.match(od) and correct_data.match(do):
            data_od=[int(dat) for dat in od.split('-')]
            data_do=[int(dat) for dat in do.split('-')]

            if not self.CheckDataDays(data_od,"OD"):
                return 0
            if not self.CheckDataDays(data_do,"DO"):
                return 0
            if not self.CheckDatyPeriod(data_od,data_do):
                return 0
        else:
            wx.MessageBox(u"Brak wpisanej poprawnej daty")
            return 0

        return od,do

    def CheckDatyPeriod(self,data_from,data_to):
            if data_to[0]<data_from[0]:
                wx.MessageBox(u"Rok w dacie 'DO' wcześniejszy niż w dacie 'OD'")
                return 0
            elif data_to[0]==data_from[0]:
                if data_to[1]<data_from[1]:
                    wx.MessageBox(u"Miesiąc w dacie 'DO' wcześniejszy niż w dacie 'OD'")
                    return 0
                elif data_to[1]==data_from[1]:
                    if data_to[2]<data_from[2]:
                        wx.MessageBox(u"Dzień w dacie 'DO' wcześniejszy niż w dacie 'OD'")
                        return 0
            return 1

    def CheckDataDays(self,data,typ):
        error_type=0
        if data[1] not in range(1,13):
            wx.MessageBox(u"Sprawdź zakres miesięcy w dacie "+typ)
            return 0

        if data[1] in set31:
            if data[2]<1 or data[2]>31:
                error_type=1
        elif data[1] in set30:
            if data[2]<1 or data[2]>30:
                error_type=1
        elif data[1]==2:
            if self.LeapYearDay(data[0],data[2])==False:
                error_type=1

        if error_type==1:
            wx.MessageBox(u"Sprawdź zakres dni w dacie "+typ)
            return 0
        else:
            return 1

    def LeapYearDay(self,year,days):
        if calendar.isleap(year):
            if days not in range(1,30):
                return 0
        else:
            if days not in range(1,29):
                return 0
        return 1

    def OnCalOd(self,event):
        kalendarz=CalendarWindow(self)
        kalendarz.SetOdDo(1)
        kalendarz.Show()
        kalendarz.ShowModal()
        kalendarz.Destroy()

    def OnCalDo(self,event):
        kalendarz=CalendarWindow(self)
        kalendarz.SetOdDo(0)
        kalendarz.Show()
        kalendarz.ShowModal()
        kalendarz.Destroy()