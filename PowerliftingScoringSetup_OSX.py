from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('pl_gui.py', base=base, targetName = 'PowerliftingScoring.dmg')
]

setup(name='PowerliftingScoring',
      version = '1.0',
      description = 'Program for powerlifting meets',
      options = dict(build_exe = buildOptions),
      executables = executables)
