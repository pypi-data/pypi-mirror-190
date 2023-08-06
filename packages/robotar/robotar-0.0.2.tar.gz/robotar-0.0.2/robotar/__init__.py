__author__ = 'reyn_app_igniter' + " zhi wei"
'''
Robot AR module

'''

import time
import socket
#from pynput import keyboard

class RobotAR:

    identity = 0
    ip = socket.gethostbyname(socket.gethostname())
    port = 0

    #listener = None

    def __init__(self, i, p, r):
        self.identity = r
        self.ip = i
        self.port = p
        self.send_message(self.identity, "u0online()")
        '''
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()
        '''

    def send_message(self, id, msg):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, self.port))
            compiled = str(id) + " " + msg
            s.send(compiled.encode())
            response_data = s.recv(1024).decode()
            s.close()
            return response_data
        except:
            print("Instructions cannot be sent. Please check unity address with yours.")
            return(" ")

    '''
    def on_press(self, key):
        if key == keyboard.KeyCode.from_char('w'):
            self.wheels(100,100)
        if key == keyboard.KeyCode.from_char('a'):
            self.wheels(0,100)
        if key == keyboard.KeyCode.from_char('s'):
            self.wheels(-100,-100)
        if key == keyboard.KeyCode.from_char('d'):
            self.wheels(100,0)

    def on_release(self, key):
        if key == keyboard.KeyCode.from_char('w'):
            self.halt()
        if key == keyboard.KeyCode.from_char('a'):
            self.halt()
        if key == keyboard.KeyCode.from_char('s'):
            self.halt()
        if key == keyboard.KeyCode.from_char('d'):
            self.halt()
    '''

    def wheels(self, lv, rv):
        self.send_message(self.identity, "u2wheels(" + str(lv) + "," + str(rv) + ")")
        #unity.u3dwheels(leftv, rightv)

    def get_wheels(self):
        result = self.send_message(self.identity, "u2getwheels()")
        if result == " ":
            return "Error"
        output = result.split(',')
        leftv = float(output[0])
        rightv = float(output[1])
        return leftv, rightv

    def halt(self):
        self.wheels(0,0)
        
    def direction(self):
        results = self.send_message(self.identity, "u3dgetrotation()")
        if results == " ":
            return "Error"
        return results

    def sleep(self, sec):
        time.sleep(sec)

    '''
    def set_other_inputs(self, temp_val, btn_center_val, btn_left_val, btn_right_val, btn_forward_val, btn_backward_val):
        temperature = temp_val
        btn_center = btn_center_val
        btn_left = btn_left_val
        btn_right = btn_right_val
        btn_forward = btn_forward_val
        btn_backward = btn_backward_val
    '''

    def set_other_inputs(self, btn_center_val, btn_left_val, btn_right_val, btn_forward_val, btn_backward_val):
         self.send_message(self.identity, "u5setinputs(" + str(btn_center_val) + "," + str(btn_left_val) + 
                      "," + str(btn_right_val) + "," + str(btn_forward_val) + "," + str(btn_backward_val) + ")")

    def leds_circle(self, led0, led1, led2, led3, led4, led5, led6, led7):
        self.send_message(self.identity, "u3dcircleleds(" + str(led0) 
                   + "," + str(led1) + "," + str(led2) 
                   + "," + str(led3) + "," + str(led4) 
                   + "," + str(led5) + "," + str(led6) 
                   + "," + str(led7) + ")")
        #u3dcircleleds(led0, led1, led2, led3, led4, led5, led6, led7)

    def leds_top(self, r, g, b):
        self.send_message(self.identity, "u3dtopleds(" + str(r) + "," + str(g) + "," + str(b)+ ")")
        #u3dtopleds(r, g, b)

    def use_platform(self):
        self.send_message(self.identity, "u3dengageplatform()")

    def prox_horizontal(self):
        results = self.send_message(self.identity, "u3dgetproxhorizontal()")
        if results == " ":
            return "Error"
        output = results.split(',')
        prox_horizontal = [int(output[0]), int(output[1]), int(output[2]), int(output[3]), int(output[4]), int(output[5]), int(output[6])]
        #prox_horizontal = [u3dgetproxhorizontal0(), u3dgetproxhorizontal1(), u3dgetproxhorizontal2(), u3dgetproxhorizontal3(), u3dgetproxhorizontal4(), u3dgetproxhorizontal5(), u3dgetproxhorizontal6()]
        return prox_horizontal

    def prox_ground(self):
        results = self.send_message(self.identity, "u3dgetproxground()")
        if results == " ":
            return "Error"
        output = results.split(',')
        prox_ground = ProxGround([int(output[0]), int(output[1])], [int(output[2]), int(output[3])], [int(output[4]), int(output[5])])
        #prox_ground = ProxGround([u3dgetproxground0(), u3dgetproxground1()],[u3dgetproxground2(), u3dgetproxground3()],[u3dgetproxground4(), u3dgetproxground5()])
        return prox_ground

    #def temperature(self):
        #return u3dgettemperature()

    def accelerometer(self):
        results = self.send_message(self.identity, "u3dgetaccelerometer()")
        if results == " ":
            return "Error"
        output = results.split(',')
        return [int(output[0]), int(output[1]), int(output[2])]
        #return [u3dgetaccelerometerx(), u3dgetaccelerometery(), u3dgetaccelerometerz()]

    def button_center(self):
        results = self.send_message(self.identity, "u3dgetbuttoncenter()")
        if results == " ":
            return "Error"
        return results == "True"
        #return u3dgetbtncenter()

    def button_left(self):
        results = self.send_message(self.identity, "u3dgetbuttonleft()")
        if results == " ":
            return "Error"
        return results == "True"
        #return u3dgetbtnleft()

    def button_right(self):
        results = self.send_message(self.identity, "u3dgetbuttonright()")
        if results == " ":
            return "Error"
        return results == "True"
        #return u3dgetbtnright()

    def button_forward(self):
        results = self.send_message(self.identity, "u3dgetbuttonforward()")
        if results == " ":
            return "Error"
        return results == "True"
        #return u3dgetbtnforward()

    def button_backward(self):
        results = self.send_message(self.identity, "u3dgetbuttonbackward()")
        if results == " ":
            return "Error"
        return results == "True"
        #return u3dgetbtnbackward()

    '''
    @property
    def init_pos(self):
        return init_pos

    @init_pos.setter
    def init_pos(self, val):
        init_pos = val
    '''


class ProxGround(object):
    def __init__(self,delta=[0,0],reflected=[0,0],ambiant=[0,0]):
        self.delta=delta
        self.reflected=reflected
        self.ambiant=ambiant

    def __str__(self):
        return "This is a ProxGround class."
