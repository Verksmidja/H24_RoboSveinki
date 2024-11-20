from machine import Pin, SoftI2C, Timer
from time import sleep_ms, ticks_ms, sleep_us, ticks_us, ticks_diff

def skynjari():
    echo = Pin(18, Pin.IN)
    trig = Pin(5, Pin.OUT)
    
    stada = False
    
    def maela_fjarlaegd():
        trig.value(1)
        sleep_us(10)
        trig.value(0)
        
        while not echo.value(): 
            pass
        
        upphafstimi = ticks_us()
        
        while echo.value(): 
            pass
        
        endatimi = ticks_us()
        
        heildartimi = ticks_diff(endatimi, upphafstimi)
        
        heildartimi /= 2
        hljodhradi = 34000 / 1000000
        fjarlaegd = heildartimi * hljodhradi
        
        return int(fjarlaegd)
        
    while True:
        fjarlaegd = maela_fjarlaegd()
        sleep_ms(200)
        if fjarlaegd > 12:
            stada = True
        else:
            stada = False
        return stada
    
    
    
