class JustOnSave(object):
    def on_source_saved(self, file):
        file.generate()
