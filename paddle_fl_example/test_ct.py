import paddle.fluid as fluid
import paddle_fl as fl
from paddle_fl.paddle_fl.core.master.job_generator import JobGenerator
from paddle_fl.paddle_fl.core.strategy.fl_distribute_transpiler import FLDistributeTranspiler
from paddle_fl.paddle_fl.core.strategy.fl_strategy_base import FLStrategyFactory, FedAvgStrategy


class Model(object):
    def __init__(self):
        pass

    def mlp(self, inputs, label, hidden_size=128):
        self.concat = fluid.layers.concat(inputs, axis=1)
        self.fc1 = fluid.layers.fc(input=self.concat, size=256, act='relu')
        self.fc2 = fluid.layers.fc(input=self.fc1, size=128, act='relu')
        self.predict = fluid.layers.fc(input=self.fc2, size=2, act='softmax')
        self.sum_cost = fluid.layers.cross_entropy(input=self.predict, label=label)
        self.accuracy = fluid.layers.accuracy(input=self.predict, label=label)
        self.loss = fluid.layers.reduce_mean(self.sum_cost)
        self.startup_program = fluid.default_startup_program()


inputs = [fluid.layers.data( \
    name=str(slot_id), shape=[5],
    dtype="float32")
    for slot_id in range(3)]
label = fluid.layers.data( \
    name="label",
    shape=[1],
    dtype='int64')

model = Model()
model.mlp(inputs, label)

job_generator = JobGenerator()
optimizer = fluid.optimizer.SGD(learning_rate=0.1)
job_generator.set_optimizer(optimizer)
job_generator.set_losses([model.loss])
job_generator.set_startup_program(model.startup_program)
job_generator.set_infer_feed_and_target_names(
    [x.name for x in inputs], [model.predict.name])

build_strategy = FLStrategyFactory()
build_strategy.fed_avg = True
build_strategy.inner_step = 1

'''
def newf(self,
         program=None,
         ps_endpoints=[],
         trainers=0,
         sync_mode=True,
         startup_program=None,
         job=None):
    transpiler = FLDistributeTranspiler()
    trainer_id = 0
    transpiler.transpile(
        trainer_id,
        program=program,
        pservers=",".join(ps_endpoints),
        trainers=trainers,
        sync_mode=sync_mode,
        startup_program=startup_program)
    job.set_server_endpoints(ps_endpoints)
    for endpoint in ps_endpoints:
        transpiler.get_pserver_programs()
        main_prog = transpiler.get_pserver_program(endpoint)
        startup_prog = transpiler.get_startup_program(endpoint, main_prog)
        job._server_startup_programs.append(startup_prog)
        job._server_main_programs.append(main_prog)


FedAvgStrategy._build_server_programs_for_job = newf()
'''
strategy = build_strategy.create_fl_strategy()

endpoints = ["127.0.0.1:8181"]
output = "fl_job_config"
job_generator.generate_fl_job(
    strategy, server_endpoints=endpoints, worker_num=2, output=output)


print('finish!')
