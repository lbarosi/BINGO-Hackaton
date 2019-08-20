import numpy as np
import inspect
from inspect import ismethod



class Lessons:
    """Parent class with common methods to all Lessons
    **allExamples**
    **viewCode**
    **viewQuestions**
    **callEcamples**
    """
    def __init__(self):
        return

    def all_examples(self):
        """List all examples in the Lesson
        Internal function useful for handling listing

        """
        # Care needed to sort properly.
        methods = sorted(
                        list(
                            filter(
                                lambda x: len(x) >=8 and x[0]=='e',
                                dir(self)
                                )
                            ),
                        key=lambda s: int(s[7:])
                        )
        return methods

    def viewCode(self, *args):
        """Show the actual code of the example in the argument

        :param *args: List of examples.
        :default: ALL
        """
        methodsL = self.all_examples()
        if len(args)!=0:
            methods = list( filter( lambda x: x in args, methodsL))
            for methods in methods:
                attribute = getattr(self,methods)
                print(inspect.getsource(attribute))
        else:
            for methods in methodsL:
                attribute = getattr(self,methods)
                print(inspect.getsource(attribute))
        return

    def viewQuestions(self, **args):
        """Show the questions for the lesson

        :param *args: List of examples.
        :default: ALL
        """
        methodsL = self.all_examples()
        if len(args)!=0:
            methods = list( filter( lambda x: x in args, methodsL))
            for methods in methods:
                attribute = getattr(self,methods)
                print(attribute.__doc__)
        else:
            for methods in methodsL:
                attribute = getattr(self,methods)
                print(attribute.__doc__)
        return

    def callExamples(self, **args):
        """Run the actual code of the example in the argument

        :param *args: List of examples.
        :default: ALL
        """
        methodsL = self.all_examples()
        if len(args)!=0:
            methods = list( filter( lambda x: x in args, methodsL))
            for methods in methods:
                attribute = getattr(self, methods)
                if ismethod(attribute):
                    attribute()
        else:
            for methods in methodsL:
                attribute = getattr(self, methods)
                if ismethod(attribute):
                    attribute()
        return

class Lesson1(Lessons):
    """
    10 exercised in Numpy.
    We must train creating, maniputing and slicing arrays.
    Tricks to format the output are also very handy.
    """
    def __init__(self):
        super().__init__()
        return

    def example1(self, **args):
        """
        Example 1:
        Create a **10x10** array with random values
        find the minimum and maximum values
        print the values with 5 decimals
        print the array with 3 decimals
        :param **args: np.array 2D.
        """
        if len(args)!=0:
            Z = args
        else:
            Z = np.random.random((10,10))
        print("NUMPY Example1 - running\n")
        Zmin, Zmax = Z.max(), Z.min()
        print("Zmin=", "{:2.5f}".format(Zmin)," Zmax=","{:2.5f}".format(Zmax))
        print(Z.round(3))
        return

    def example2(self, **args):
        """
        Example 2:
        How to add a border (filled with 0's) around an existing array?

        :param **args: np.array 2D.
        """
        if len(args)!=0:
            Z = args
        else:
            Z = np.ones((5,5))
        print("NUMPY Example2 - running\n")
        Z = np.pad(Z, pad_width=1, mode='constant', constant_values=0)
        print(Z)
        return

    def example3(self):
        """
        Example 3:
        Create a 8x8 matrix and fill it with a checkerboard pattern
        """
        print("NUMPY Example3 - running\n")
        Z = np.zeros((8,8),dtype=int)
        Z[1::2,::2] = 1
        Z[::2,1::2] = 1
        print(Z)
        return

    def example4(self, **args):
        """
        Example 4:
        Normalization of matrix

        :param **args: np.array 2D.
        """
        if len(args)!=0:
            Z = args
        else:
            Z = np.random.random((5,5))
        print("NUMPY Example4 - running\n")
        Z = (Z - np.mean(Z)) / (np.std(Z))
        print(Z)
        return

    def example5(self, **args):
        """
        Example 5:
        Consider a matrix representing cartesian coordinates,
        convert them to polar coordinates. Data in ROW

        :param **args: np.array 2D.
        """
        if len(args)!=0:
            Z = args
        else:
            Z = np.random.random((10,2))
        print("NUMPY Example5 - running\n")
        X,Y = Z[:,0], Z[:,1]
        R = np.sqrt(X**2+Y**2)
        T = np.arctan2(Y,X)
        print(R)
        print(T)
        return

    def example6(self, **args):
        """
        Example 6:
        Consider a vector with cartesian coordinates in ROWS.
        find point by point distances

        :param **args: np.array 2D.
        """
        if len(args)!=0:
            Z = args
        else:
            Z = np.random.random((10,2))
        print("NUMPY Example6 - running\n")
        X,Y = np.atleast_2d(Z[:,0], Z[:,1])
        D = np.sqrt( (X-X.T)**2 + (Y-Y.T)**2)
        print(D)
        return

    def example7(self, *args):
        """
        Example 7:
        How to compute averages using a sliding window over an array
        # Author: Jaime Fernández del Río

        :param **args: np.array 1D.
        """
        if len(args)!=0:
            Z = args
        else:
            Z = np.arange(20)
        print("NUMPY Example7 - running\n")
        def moving_average(a, n=3) :
            ret = np.cumsum(a, dtype=float)
            ret[n:] = ret[n:] - ret[:-n]
            return ret[n - 1:] / n

        print(moving_average(Z, n=3))
        return

    def example8(self, **args):
        """
        Example 8:
        Compute the eivenvalues of a matrix
        Compute the eigenvector of a matrix
        Show the result is correct

        :param **args: np.array 2D.
        """
        # Compute the Eigenvalues
        print("NUMPY Example8 - running\n")
        if len(args)!=0:
            Z = args
        else:
            Z = np.random.random((20,20))

        return

    def example9(self, **args):
        """
        Example 9:
        Do a least square fit for supernova Data
        and find the Hubble constant.

        :param **args: np.array 2D.
        """
        print("NUMPY Example9 - running\n")

        return

    def example10(self, **args):
        """
        Example 10:
        Implement Matropolis-Hasting algorithm for
        gaussian likelyhood

        :param **args: np.array 2D.
        """
        print("NUMPY Example10 - running\n")
        return



if (__name__ == '__main__'):
    print('Executing as standalone script')
    obj = Lesson1()
    print("Lesson 1: Questions\n")
    obj.viewQuestions()
    print("Lesson 1: Showing results\n")
    obj.callExamples()
    print("Lesson 1: Showing code\n")
    obj.viewCode()
