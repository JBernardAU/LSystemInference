from InferenceTools.LSystemInference import LSystemInference

settings_file = "settings.json"
lsit = LSystemInference(settings_file=settings_file)
lsit.display_settings()
lsit.run()
