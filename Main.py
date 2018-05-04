import logging
import ConfigParser

# get data process time and script run time and week_day
import time
localtime = time.strftime("%Y-%m-%d", time.localtime(time.time()))
logging.info("localtime : %s" % (localtime))

date_time = time.strftime("%Y-%m-%d", time.localtime(time.time() - 24*60*60))
week_day = time.strftime("%w", time.localtime())
logging.info("data time init to : %s , week day is %s" % (date_time, week_day))

import sys
if len(sys.argv) > 1:
    date_time = sys.argv[1]
    logging.info("data time change by argument to : %s"%(localtime))

# change execute directory to the Main.py dir
import os
os.chdir(os.path.split(os.path.realpath('__file__'))[0])
logging.info('current directory：%s'%(os.getcwd()))

if not os.path.isdir('./model'):
    logging.info('check or create model directory')
    os.mkdir('model')

cf = ConfigParser.ConfigParser()

from Hive_Interaction import Hive
hive = Hive()
table = {'fields': cf.get('table','train_set_fields'),'name':cf.get('table','train_set_table')}
logging.info('get %s from %s' % (table['fields'],table['name']))
pandas_df = hive.Get_Pandas_From_Table(table,date_time)

from DeepAndWideModel import model_wide_deep
inputs_wide = {'feature_demo':[0,0,1,1,0,0,0,1,0,1],'length':10,'name':'wide_input','wide_output_dim':32,'l1':1e-4,'l2':1e-4}
inputs_deepX = {'deep_hidden_dim':128,'deep_output_dim':32}
input_deep1={'feature_demo':[0,0,1,3,7,11,2,10,6],'length':9,'name':'shop_id_type','embedding_out_dim':16,'embedding_in_dim':20}
input_deep2={'feature_demo':[3],'length':1,'name':'user_type','embedding_out_dim':8,'embedding_in_dim':10}
model = model_wide_deep(inputs_wide,inputs_deepX,input_deep1,input_deep2)
logging.info(model.summary())