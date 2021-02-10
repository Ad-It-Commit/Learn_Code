import numbers
import itertools
from datetime import datetime
from datetime import timedelta
import unittest

class TimeZone:
    def __init__(self, name, offset_hours, offset_minutes):
        if name is None or len(str(name).strip())==0:
            raise ValueError("Timezone name cannot be empty")
        self._name = str(name).strip()

        if not isinstance(offset_hours, numbers.Integral):
            raise ValueError("Offset hours must be an integer")

        if not isinstance(offset_minutes, numbers.Integral):
            raise ValueError("Offset minutes must be an integer")

        if not abs(offset_minutes)<=59:
            raise ValueError("Offset minutes must be between -59 and 59.")

        offset = timedelta(hours = offset_hours, minutes = offset_minutes)
        if offset < timedelta(hours = -12, minutes = 0) or offset > timedelta(hours = 14, minutes = 0):
            raise ValueError("Offset must be between -12:00 and +14:00.")

        self._offset_hours = offset_hours
        self._offset_minutes = offset_minutes
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        return (isinstance(other, TimeZone) and self.name == other.name and self._offset_hours == other._offset_hours and self._offset_minutes == other._offset_minutes)

    def __repr__(self):
        return(f'TimeZone Name = {self.name}, offset_hours = {self._offset_hours}, offset_minutes = {self._offset_minutes}')
def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(suite)
class TestAccount(unittest.TestCase):
    def test_create_timezone(self):
        tz = TimeZone("ABC",-1,-30)
        self.assertEqual("ABC",tz.name)
        self.assertEqual(timedelta(hours=-1,minutes=-30),tz.offset)

    def test_timezone_equal(self):
        tz1 = TimeZone("ABC",-1,-30)
        tz2 = TimeZone("ABC",-1,-30)
        self.assertEqual(tz1,tz2)

    def test_timezone_not_equal(self):
        tz1 = TimeZone("ABC",-1,-30)

        test_timezones = (TimeZone("ABC",-1,00),TimeZone("GHY",-4,00),TimeZone("DEF",-1,00))
        for test_tz in test_timezones:
            self.assertNotEqual(tz1,test_tz)

    def test_create_account(self):
        acc_num = "A100"
        f_name = "FIRST"
        l_name = "LAST"
        tz = TimeZone("TZ",1,30)
        init_bal = 100.00

        a = C_Account(acc_num,f_name,l_name,init_bal,tz)

        self.assertEqual(acc_num,a.acc_num)
        self.assertEqual(f_name,a.f_name)
        self.assertEqual(l_name,a.l_name)

    def test_create_account_negativebalance(self):
        acc_num = "A100"
        f_name = "FIRST"
        l_name = "LAST"
        tz = TimeZone("TZ",1,30)
        init_bal = -100.00

        with self.assertRaises(ValueError):
            a = C_Account(acc_num,f_name,l_name,init_bal,tz)


class C_Account:
    
    iter_num = itertools.count(0)
    dt_code = datetime.utcnow()
    _int_rate = 0.5  # interest rate a private variable

    def __init__(self, acc_num, f_name, l_name, init_bal=0, tz = None): # timezone should be set with the timezone class
        
        self._acc_num = acc_num   # acc num stays a private variable
        self.f_name = f_name    # f_name and l_name should be addressed the same as their property definition if setter is to run for init.
        self.l_name = l_name
        if init_bal != 0:
            self._c_bal = init_bal
        if init_bal < 0:
            raise ValueError("Balance cannot be negative")
        
        
        if tz is None:
            tz = TimeZone("UTC", 0, 0)
        self.tz = tz
        
        
    #@classmethod
    #def txn_log(cls):
    #    cls.txn_num += 1
    #    return cls.txn_num
    @classmethod
    def get_IR(cls):
        return cls._int_rate

    @classmethod
    def set_IR(cls,value):
        if not isinstance(value,numbers.Real):
            raise ValueError("Interest Rate must be a real number")

        if value<0:
            raise ValueError("Interest Rate cannot be negative.")
        cls._int_rate = value
        
    #@classmethod
    def pay_IR(self):
        self._c_bal = self._c_bal + (self._c_bal)*((self._int_rate)/100)
        txn_num = next(C_Account.iter_num)    # itertools function for easy transaction number increment.
        t_code = self.getdt()
        txn_code = "D"+"-"+str(self._acc_num)+"-"+t_code+"-"+str(txn_num)
        return f'Your new balance, including interest is {self._c_bal}. Transaction ID:{txn_code}'

    @classmethod
    def txn_fetch(cls,txn_num):
        raw_list = txn_num.split("-")
        if raw_list[0] == "D":
            fetch_code = "This was a deposit"
        elif raw_list[0] == "W":
            fetch_code = "This was a withdrawal"
        elif raw_list[0] == "X":
            fetch_code = "This was a declined transaction"
        else:
            print("Invalid transaction ID. Please enter the transaction Id in the format Z-ZZZZZZZ-ZZZZZZZZZZZZZZ-Z")
        #fetch_2 = f'Transaction number is f{raw_list[3]'
        # :4 4:6 6:8 8:10 10:12 12:14
        raw_dt = raw_list[2]
        fetch_date = raw_dt[:4]+"-"+raw_dt[4:6]+"-"+raw_dt[6:8]
        fetch_time = raw_dt[8:10]+"-"+raw_dt[10:12]+"-"+raw_dt[12:14]
        fetch_string = f'Details for this transaction shown below:\n{fetch_code} for Account Number:{raw_list[1]}.\nInternal Transaction Number:{raw_list[3]}\nThis transaction was made on {fetch_date} at {fetch_time}.'
        print(fetch_string)


    @classmethod
    def getdt(cls):
        cls.dt_code = datetime.utcnow().strftime("%Y%m%d%H%M%S")  # need to know the datetime package better
        #temp_dt = cls.dt_code
       # hrs = str(temp_dt.hour)
       # if len(hrs)==1:
        #    hrs = "0"+hrs
        #mins = str(temp_dt.minute)
       # if len(mins)==1:
       #     mins = "0"+mins
       # secs = str(temp_dt.second)
        #if len(secs)==1:
        #    secs = "0"+secs
        #dy = str(temp_dt.day)
        #if len(dy)==1:
       #     dy = "0"+dy
        #mnth = str(temp_dt.month)
        #if len(mnth)==1:
        #    mnth = "0"+mnth
        #yr = str(temp_dt.year)
        return cls.dt_code
        
    @property
    def tz(self):
        return self._tz

    @tz.setter
    def tz(self,value):
        if not isinstance(value, TimeZone):
            raise ValueError("Timezone must be a valid timezone object.")
        self._tz = value
    
    @property
    def acc_num(self):
        return self._acc_num
    
    @acc_num.setter
    def acc_num(self,value):
        print("Account number cannot be changed!")
    
    @property
    def f_name(self):
        return self._f_name
    
    @f_name.setter
    def f_name(self,value):
        self._f_name = C_Account.Validate_Name(value,"First Name")
        #print("First Name on account changed successfully!") 
    
    @property
    def l_name(self):
        return self._l_name
    
    @l_name.setter
    def l_name(self,value):
        self._l_name = C_Account.Validate_Name(value,"Last Name")
        #print("Last Name on account changed successfully!")
    
    @property
    def c_bal(self):        
        if self._c_bal<=25:
            print(f'Your current balance is €{self._c_bal}')
            print("Your account balance has fallen below €25. Please deposit cash to avoid account charges!")

        else:
            print(f'Current balance in your account is €{self._c_bal}')

    @c_bal.setter
    def c_bal(self,value):
        print("Balance cannot be changed without making a transaction.")


    @staticmethod
    def Validate_Name(value, field_title):
        if value is None or len(str(value).strip()) == 0:   #extra check added to avoid None value being entered.
            raise ValueError(f'{field_title} cannot be empty.')
        return str(value).strip()               #elegant way to validate data, without repeating it for f_name and l_name.

    
    def m_dep(self,value):
        #txn_num = self.txn_log()
        txn_num = next(C_Account.iter_num)    # itertools function for easy transaction number increment.
        self._c_bal = self._c_bal + value
        t_code = self.getdt()
        txn_code = "D"+"-"+str(self._acc_num)+"-"+t_code+"-"+str(txn_num)
        print(f'Balance is updated! New balance is €{self._c_bal}. Transaction ID:{txn_code}')
        
    def m_wdl(self,value):
        txn_num = next(C_Account.iter_num)
        if (self._c_bal - value)<=0:
            t_code = self.getdt()
            txn_code = "X"+"-"+str(self._acc_num)+"-"+t_code+"-"+str(txn_num)
            print(f'This amount cannot be withdrawn since your balance is too low! Try withdrawing a smaller amount. Transaction ID:{txn_code}')
        elif (self._c_bal - value)<=25 and (self._c_bal - value)>0:
            self._c_bal = self._c_bal - value
            t_code = self.getdt()
            txn_code = "W"+"-"+str(self._acc_num)+"-"+t_code+"-"+str(txn_num)
            print(f'Please collect your cash. New account balance is €{self._c_bal}. Transaction ID:{txn_code}')
            print("Your account balance has fallen below €25. Please deposit cash to avoid account charges!")
        else:
            self._c_bal = self._c_bal - value
            t_code = self.getdt()
            txn_code = "W"+"-"+str(self._acc_num)+"-"+t_code+"-"+str(txn_num)
            print(f'Please collect your cash. New account balance is €{self._c_bal}. Transaction ID:{txn_code}')
        
    def chk_txn(self,txnnum):
        self.txn_fetch(txnnum)
