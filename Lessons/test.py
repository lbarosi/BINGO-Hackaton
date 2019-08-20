import sys
import os
import numpy as np
import inspect
os.getcwd()
os.chdir('../cosmos')

import lessons.lessons1 as lesson1


examples = lesson1.Lesson1
help(examples.example1)
lesson1.countExamples(lesson1.Lesson1)

examples.example1()

print(examples.example1.__doc__)

lesson1.viewCode(examples.example1)
