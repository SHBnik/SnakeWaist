

import time


class pid:
    def __init__(self,Kp,Ki,Kd):
        self.P = 0
        self.I = 0
        self.D = 0
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.last_time = 0
        self.time = 0
        self.last_Error = 0
        self.Error = 0
        self.last_pid = 0 

    def update_pid(self,point,data):
        self.Error = -(point - data)
        self.time = time.time()

        elapsed_time = int((self.time - self.last_time)*1000)
        if elapsed_time >= 10:

            self.P = self.Error * self.Kp
            self.D = ((self.Error - self.last_Error)/(elapsed_time) )* self.Kd
            self.I += (self.Error ) * self.Ki

            if self.I > 100: self.I = 100
            if self.I < -100: self.I = -100

            self.last_time = self.time
            self.last_Error = self.Error
            pid = (self.P + self.I + self.D )

            if pid > 250: pid = 250
            if pid < -250: pid = -250
            self.last_pid = pid
            return pid
        else:
            return self.last_pid

    def get_term_i(self):
        return self.I

    def get_term_p(self):
        return self.P

    def get_term_d(self):
        return self.D

    def get_error(self):
        return self.Error
        
    def resetI(self):
         self.I = 0