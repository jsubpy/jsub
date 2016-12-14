class Submit(object):
    def __init__(self, task_id, repo):
        pass

    def handle(self):
#        task_pool.find(task_id)
#        backend.before_submit()
#        backend.submit()
#        backend.after_submit()

        generate_work_main()
        generate_bootstrap()
        generate_runtime()
        generate_module()
        generate_input()
        for job in jobs:
            generate_config()
