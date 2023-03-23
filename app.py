from flask import Flask
from celery import Celery, chain, Signature, subtask

app = Flask(__name__)
simple_app = Celery('tasks',
                    broker='amqp://admin:mypass@rabbit:5672',
                    result_backend ='rpc://')


@app.route('/simple_start_task_1')
def call_method():
    app.logger.info("Invoking Method ")
    r = simple_app.send_task('tasks.longtime_add', kwargs={'x':1,'y':2}, queue="embedding")
    r = simple_app.send_task('tasks.longtime_add', kwargs={'x':2,'y':2}, queue="embedding")
    
    # r = simple_app.send_task(
            # 'tasks.longtime_add', [1,2], queue="embedding",
            # chain=[
                # Signature('tasks.task_temp', kwargs={}, queue="saveDB")
            # ]
        # )

    # r = simple_app.send_task(
    # 'tasks.longtime_add', [1,2], queue="embedding",
        # link=subtask(
            # 'tasks.task_exception'
        # )
    # )
    

    app.logger.info(r.backend)
    return r.id
    
@app.route('/simple_start_task_2')
def call_method_2():
    app.logger.info("Invoking Method ")
    r = simple_app.send_task('tasks2.longtime_add_2', kwargs={'x': 1, 'y': 2})
    app.logger.info(r.backend)
    return r.id   


@app.route('/simple_task_status/<task_id>')
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)


@app.route('/simple_task_result/<task_id>')
def task_result(task_id):
    result = simple_app.AsyncResult(task_id).result
    return "Result of the Task " + str(result)

