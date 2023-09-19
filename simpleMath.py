import sublime
import sublime_plugin
import re
import time
from . import pyperclip as clipboard
import math


class SimpleMathCommand(sublime_plugin.TextCommand):
    def display(self, title, value):
        # copy to clipboard and display operation result
        clipboard.copy(value)
        # if value.is_float():
        if isinstance(value, float):
            if value.is_integer():
                value = int(value)
        sublime.status_message('   ' + title + ': ' + str(value) + "   copied value to clipboard")

    def getText(self):
        # get highlighted text
        sel = self.view.sel()[0]
        if sel.begin() == sel.end():
            return self.view.substr(sublime.Region(0, self.view.size()))
        else:
            return self.view.substr(sel)

    def getNumbers(self):
        text = self.getText()
        result = re.findall(r'(\d+\.\d+|\d+)', text)
        return [float(x) for x in result]

class SummCommand(SimpleMathCommand):

    def run(self, edit):
        # find summ of all numbers in text
        numbers = self.getNumbers()
        summ = sum(numbers)
        self.display("Summ", summ)

class MultiplyCommand(SimpleMathCommand):

    def run(self, edit):
        # multiply all numbers in text
        numbers = self.getNumbers()
        multiplied = 1.0
        for i in numbers:
            multiplied*=i
        self.display("Multiplied", multiplied)

class CalculateCommand(SimpleMathCommand):

    def run(self, edit):
        # calculate math expression
        expression = self.getText()

        # remove non mathematical symbols
        expression = "".join(re.findall(r'(\d+\.\d+|\d+|\*|\/|\+|\-|\(|\))', expression))

        # remove whitespaces
        expression = re.sub(r' ', r'', expression)

        # add multiply characters if needed
        expression = re.sub(r'(\d)(\()', r'\1*\2', expression)
        expression = re.sub(r'(\))(\d)', r'\1*\2', expression)
        try:
            result = eval(expression)
            self.display("Result", result)
        except Exception as e:
            sublime.status_message("   ERROR: " + repr(e))
