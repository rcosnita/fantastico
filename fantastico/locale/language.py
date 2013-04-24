'''
Copyright 2013 Cosnita Radu Viorel

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. codeauthor:: Radu Viorel Cosnita <radu.cosnita@gmail.com>

.. py:module:: fantastico.locale.language
'''

class Language(object):
    '''Class used to define how does language object looks like. There are various use cases for using language but
    the simplest one is in request context object: 
    
    .. code-block:: python
    
       language = request.context.language
       
       if language.code = "en_us":
          print("English (US) language").
       else:
          raise Exception("Language %s is not supported." % language.code) 
    '''
    
    def __init__(self, code):
        self._code = code
    
    @property
    def code(self):
        '''Property that holds the language code. This is readonly because once instantiated we mustn't be able to change it.'''
        
        return self._code
    
    def __str__(self):
        '''Method used to convert the current instance into a string object.'''
        
        return self._code