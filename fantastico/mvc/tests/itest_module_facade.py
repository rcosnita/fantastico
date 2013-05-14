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
.. py:module:: fantastico.mvc.tests.itest_model_facade
'''
from fantastico import mvc
from fantastico.mvc import BASEMODEL
from fantastico.mvc.model_facade import ModelFacade
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.mvc.models.model_filter_compound import ModelFilterAnd
from fantastico.settings import SettingsFacade
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text

class ModelFacadeMessage(BASEMODEL):
    '''This class is a simple mapping over mvc_model_facade_messages table.'''
    
    __tablename__ = "mvc_model_facade_messages"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    message = Column("message", Text)
    
    def __init__(self, message):
        self.message = message

class ModelFacadeIntegration(FantasticoIntegrationTestCase):
    '''This class provides test cases required to guarantee model facade is working as expected.'''
    
    MESSAGES = ["Hello world 1", "Hello world 2", "Hello world 3", "Hello world 4"]
    
    settings_facade = None
    model_facade = None
    last_generated_pk = None
    entities_created = []
    
    @classmethod
    def setup_once(cls):
        '''This method is invoked once before executing any test case. For model facade we create a series of messages.'''
        
        cls.settings_facade = SettingsFacade()
        mvc.init_dm_db_engine(cls.settings_facade.get("database_config"), echo=True)
        
        cls.model_facade = ModelFacade(ModelFacadeMessage, mvc.SESSION())
        
        for message in ModelFacadeIntegration.MESSAGES:
            message_entity = cls.model_facade.new_model(message=message)
            message_id = cls.model_facade.create(message_entity)
            
            assert message_id[0] == message_entity.id
            assert message_id[0] > 0
            
            cls.last_generated_pk = message_id[0]
            cls.entities_created.append(message_entity)
        
        records_count = cls.model_facade.count_records(ModelFilter(ModelFacadeMessage.id, 0, ModelFilter.GT))
        assert records_count == len(cls.MESSAGES)
    
    @classmethod
    def cleanup_once(cls):
        '''This method is invoked only once after all test cases have been executed in order to delete all messages.'''
        
        for entity in cls.entities_created:
            cls.model_facade.delete(entity)
            
        assert cls.model_facade.count_records() == 0
    
    def test_retrieve_message_bypk(self):
        '''This test case ensures filtering message by primary key works.'''
        
        message = self.model_facade.find_by_pk({ModelFacadeMessage.id: self.last_generated_pk})
        
        self.assertIsNotNone(message)
        self.assertEqual(self.MESSAGES[-1], message.message)
    
    def test_retrieve_message_byfilter_and(self):
        '''This test case ensures filtering message using compound filter works as expected.'''
        
        model_filter_gt = ModelFilter(ModelFacadeMessage.id, 1, ModelFilter.GE)
        model_filter_like = ModelFilter(ModelFacadeMessage.message, "%%world 4%%", ModelFilter.LIKE)
        model_filter_and = ModelFilterAnd(model_filter_gt, model_filter_like)
        
        records = self.model_facade.get_records_paged(0, 100, filter_expr=model_filter_and)
        
        self.assertEqual(1, len(records))
        self.assertEqual(self.last_generated_pk, records[0].id)
        self.assertEqual(self.MESSAGES[-1], records[0].message)