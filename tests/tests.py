import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    testSuite = loader.discover('tests', pattern='*test*.py')
    testRunner = unittest.TextTestRunner(verbosity=2)
    testRunner.run(testSuite)
