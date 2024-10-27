import environ


env = environ.Env()
environ.Env.read_env()

ROOT = environ.Path(__file__) - 1
SCREENS_PATH = ROOT.path("report_screenshots")
