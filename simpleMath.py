import sublime
import sublime_plugin
import re
import time

class SimpleMathCommand(sublime_plugin.TextCommand):
    def countSumm(self):
        # get selected text
        sel = self.view.sel()[0]
        if sel.begin() == sel.end():
            text = self.view.substr(sublime.Region(0, self.view.size()))
        else:
            text = self.view.substr(sel)

        # find summ of all numbers in text
        numbers = re.findall(r'(\d+\.\d+|\d+)', text)
        summ = sum([float(i) for i in numbers])
        if summ.is_integer():
            summ = int(summ)

        # display result
        now = time.strftime("%H:%M:%S")
        print(now + "  " + str(summ))
        sublime.status_message('   Summ: ' + str(summ) + "   see [ctrl ~] for copying")

class SummCommand(SimpleMathCommand):

    def run(self, edit):
        self.countSumm()