import os, zipfile, shutil, subprocess, sys

shutil.rmtree(os.path.join('lambda', 'package'), ignore_errors=True)

subprocess.check_call([sys.executable, "-m", "pip", "install", 'pygame', '--target',  './lambda/package'])

files_to_zip = [os.path.join('./ml', 'match.py')]
files_to_zip.extend([os.path.join('./game', f) for f in os.listdir('./game')])

print(files_to_zip)

package_folder = os.path.join('lambda', 'package')
os.mkdir(os.path.join(package_folder, 'src'))
os.mkdir(os.path.join(package_folder, 'src', 'game'))
os.mkdir(os.path.join(package_folder, 'src', 'ml'))

for f in files_to_zip:
    if os.path.isfile(f) and 'game' in f:
        shutil.copy(f, os.path.join(package_folder, 'src', 'game'))
    elif os.path.isfile(f) and 'ml' in f:
        shutil.copy(f, os.path.join(package_folder, 'src', 'ml'))

shutil.copy(os.path.join('lambda', 'lambda_function.py'), os.path.join(package_folder, 'lambda_function.py'))

z = zipfile.ZipFile(os.path.join('lambda', 'lambda_zip.zip'), 'w')

os.chdir(package_folder)
for root, dirs, files in os.walk(os.curdir):
    for file in files:
        z.write(os.path.join(root, file))
z.close()
