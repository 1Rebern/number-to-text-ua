import sys
import os

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal

def number_to_text_ua(number):
    units = ['нуль', 'один', 'два', 'три', 'чотири', 'п\'ять', 'шість', 'сім', 'вісім', 'дев\'ять']
    teens = ['десять', 'одинадцять', 'дванадцять', 'тринадцять', 'чотирнадцять', 'п\'ятнадцять', 'шістнадцять', 'сімнадцять', 'вісімнадцять', 'дев\'ятнадцять']
    tens = ['', '', 'двадцять', 'тридцять', 'сорок', 'п\'ятдесят', 'шістдесят', 'сімдесят', 'вісімдесят', 'дев\'яносто']
    hundreds = ['', 'сто', 'двісті', 'триста', 'чотириста', 'п\'ятсот', 'шістсот', 'сімсот', 'вісімсот', 'дев\'ятсот']
    scales = ['тисяча', 'мільйон', 'мільярд']
    fraction_scales = {1: 'десятих', 2: 'сотих', 3: 'тисячних'}

    def get_hundreds_text(n, is_thousands=False):
        if n == 1 and is_thousands:
            return 'одна'
        if n < 10:
            return units[n]
        elif 10 <= n < 20:
            return teens[n - 10]
        elif 20 <= n < 100:
            return tens[n // 10] + ('' if n % 10 == 0 else ' ' + units[n % 10])
        else:
            return hundreds[n // 100] + ('' if n % 100 == 0 else ' ' + get_hundreds_text(n % 100))

    def get_scale_name(scale_idx, number):
        if scale_idx == 1:
            return "тисяча" if number == 1 else "тисячі" if number < 5 else "тисяч"
        if scale_idx == 2:
            return "мільйон" if number == 1 else "мільйони" if number < 5 else "мільйонів"
        if scale_idx == 3:
            return "мільярд" if number == 1 else "мільярди" if number < 5 else "мільярдів"
        return ''

    def split_number(n):
        parts = []
        while n > 0:
            parts.append(n % 1000)
            n //= 1000
        return parts[::-1]

    if number == 0:
        return "нуль"

    integer_part = int(number)
    fraction_part = round(number - integer_part, 3)

    integer_parts = split_number(integer_part)
    result = []

    if integer_part == 0:
        result.append("нуль")
    else:
        for i, part in enumerate(integer_parts):
            if part > 0:
                scale_idx = len(integer_parts) - i - 1
                result.append(get_hundreds_text(part, is_thousands=(scale_idx == 1)))
                if scale_idx > 0:
                    result.append(get_scale_name(scale_idx, part))

    if fraction_part > 0:
        result.append("цілих")
        fraction_str = str(fraction_part).split('.')[1]
        fraction_value = int(fraction_str)
        result.append(get_hundreds_text(fraction_value))
        
        if len(fraction_str) <= 3:
            result.append(fraction_scales[len(fraction_str)])

    return ' '.join(result)


class MainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

    def number_is_true(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
        
    def check_decimal_places(self, number):        
        if '.' in number:
            decimal_part = number.split('.')[1]
        
            if len(decimal_part) > 3:
                return False
        return True

    signalNumber = Signal(str)
    signalNum = Signal(bool)
    signalNumMax = Signal(bool)
    signalNumDec = Signal(bool)
    signalText = Signal(str)

    @Slot(str)
    def checkNumber(self, getNumber):
        if self.number_is_true(getNumber):
           number = float(getNumber)
           
           if self.check_decimal_places(getNumber):
            self.signalText.emit(number_to_text_ua(number))
            self.signalNum.emit(True)
            
            if number < 1000000000000:
                self.signalText.emit(number_to_text_ua(number))
                self.signalNum.emit(True)         
                
            else:
                self.signalNumMax.emit(True)
                
           else:
               self.signalNumDec.emit(True)
    
        else:
            self.signalNum.emit(False) 

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    main = MainWindow()
    engine.rootContext().setContextProperty("backend", main)

    engine.load(os.path.join(os.path.dirname(__file__), "qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())