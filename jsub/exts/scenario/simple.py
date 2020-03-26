class Simple(object):
    def __init__(self):
        pass

    def before_submit_dirac(self):
        create_dfc_dir()
        create_dataset()

    def after_submit_pbs(self):
        pass
