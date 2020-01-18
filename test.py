#%%
# import a module Logger
import mllogger

# prepare and make directory for recording log files.
## must always start by this function; Logger
logger_name = "testlogger"
logger = mllogger.Logger(logger_name=logger_name, allow_duplicate=True, save_inside=True)
## allow_duplicate use for make output log has no version, i.e., ฟfter running it again, it will save the previous.
## save_inside make log and model directories within the current one.

## save_inside 
#%%
# prepare logfiles as an object.
## naming must be string or list of strings
log_name_str = "test_log" # String form.
log_name_list = ["test_log"] # Althernative form.
log = logger.make(log_name_str) # Called method to make an object log sheet. 
print(type(log))# This object is a dict-type object.

for v in [1,2,3,4,5]:
    # Since object's type is dict, we must called object as object["log name"], e.g., log["test_log"] 
    # for calling their method.
    log["test_log"].record(value=int(v)) # Use record for recording value for a log sheet (Object).

log["test_log"].save() # Save object to a .csv file.

# the following method can be used only after saving log file.
final_value = log["test_log"].get() # get final value in log["test_log"]
print(final_value)
all_values = log["test_log"].get(all=True) # get all values in log["test_log"]
print(all_values)

# plot graph for log files. 
log["test_log"].plot(x_label="Epoches", y_label="Y", line_label="a line", title="None title")

#%%
# load data in a log file.
# First, we must make a Log_sheet object with specific file path.
log_load = mllogger.Log_sheet(sheet_name="test_log", sheet_root="./log/testlogger", sheet_path="./log/testlogger/test_log.csv")
# Or althernative mllogger.Log_sheet(sheet_path="./log/testlogger/test_log.csv") 
# to detail Object and allow to use .save and .record method.
## Now, we are able to use .get and .plot
print(log_load.get())
print(log_load.get(all=True))
log_load.plot()

#%%
# save machine learning 
amodel = object()
print(type(amodel))
logger.model_log(root=logger_name, model=amodel) # save model method.

#%%
# make many log files.
log_name = ["test_log_a", "test_log_b"] # must be a list of log's name
log_many = logger.make(log_name)

for v in [1,2,3,4,5]:
    # Since object's type is dict, we must called object as object["log name"], e.g., log["test_log"] 
    # for calling their method.
    log_many["test_log_a"].record(value=int(-v)) # Use record for recording value for a log sheet (Object).
    log_many["test_log_b"].record(value=int(v))

log_many["test_log_a"].save() # Save object to a .csv file.
log_many["test_log_b"].save() # Save object to a .csv file.

#%%
# Plot compare between two log files.
a_log = log_many["test_log_a"] # or althernative a_log = mlogger.Log_sheet(sheet_path="./log/testlogger/test_log_a.csv")
b_log = log_many["test_log_b"] # or althernative b_log = mlogger.Log_sheet(sheet_path="./log/testlogger/test_log_b.csv")

## One can simply use .plot_compare method in Logger
logger.plot_compare(a_log, b_log, x_label="Epoches", y_label="Y ni", line_label_a="a line", line_label_b="b line", title="None")