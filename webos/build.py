import os
import shutil

APP_DIR = 'tmp'
DIST_DIR = 'dist'

shutil.rmtree(APP_DIR, ignore_errors=True)
shutil.rmtree(DIST_DIR, ignore_errors=True)
os.makedirs(DIST_DIR, exist_ok=True)
shutil.copytree('src', APP_DIR)

print('Arquivos preparados em webos/tmp')
print('Para gerar IPK: ares-package -n -o dist tmp')
