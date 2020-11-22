from paddle import fluid
from paddle_fl.paddle_fl.core.trainer.fl_trainer import FLTrainerFactory
from paddle_fl.paddle_fl.core.master.fl_job import FLRunTimeJob
import numpy as np
import sys

import logging


def reader():
    for i in range(10):
        data_dict = {}
        for i in range(3):
            data_dict[str(i)] = np.random.rand(1, 5).astype('float32')
        data_dict["label"] = np.random.randint(2, size=(1, 1)).astype('int64')
        yield data_dict


trainer_id = int(sys.argv[1])  # trainer id for each guest
job_path = "fl_job_config"
job = FLRunTimeJob()
job.load_trainer_job(job_path, trainer_id)
job._scheduler_ep = "127.0.0.1:9091"  # Inform the scheduler IP to trainer
# print(job._trainer_send_program)

trainer = FLTrainerFactory().create_fl_trainer(job)
use_cuda = False
place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()
trainer._current_ep = "127.0.0.1:8192"
trainer.start(place=place)
trainer._logger.setLevel(logging.DEBUG)

g = reader()
if trainer_id > 0:
    for i in range(trainer_id):
        next(g)
data = next(g)
print(data)

output_folder = "fl_model"
step_i = 0
while not trainer.stop():
    step_i += 1
    print("batch %d start train" % step_i)
    trainer.run(feed=data, fetch=[])
    if trainer_id == 0:
        print("start saving model")
        trainer.save_inference_program(output_folder)
    if step_i >= 10:
        break
