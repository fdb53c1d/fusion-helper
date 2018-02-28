import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)


from fusionhelper import factory
application = factory.create_app()
