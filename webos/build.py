import io
import json
import os
import shutil
import tarfile
import time

SRC_DIR = 'src'
DIST_DIR = 'dist'
APP_ROOT = 'usr/palm/applications'


def add_text_to_tar(tar, name, text):
    data = text.encode('utf-8')
    info = tarfile.TarInfo(name)
    info.size = len(data)
    info.mtime = int(time.time())
    info.mode = 0o644
    tar.addfile(info, io.BytesIO(data))


def make_tar_gz(entries):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w:gz') as tar:
        for kind, arcname, value in entries:
            if kind == 'text':
                add_text_to_tar(tar, arcname, value)
            elif kind == 'file':
                tar.add(value, arcname=arcname, recursive=False)
    return buffer.getvalue()


def ar_header(name, size):
    if len(name) > 15:
        name = name[:15]
    return (
        name.ljust(16)
        + str(int(time.time())).ljust(12)
        + '0'.ljust(6)
        + '0'.ljust(6)
        + '100644'.ljust(8)
        + str(size).ljust(10)
        + '`\n'
    ).encode('ascii')


def write_ar(path, members):
    with open(path, 'wb') as fp:
        fp.write(b'!<arch>\n')
        for name, data in members:
            fp.write(ar_header(name, len(data)))
            fp.write(data)
            if len(data) % 2:
                fp.write(b'\n')


def collect_data_files(app_id):
    entries = []
    base = os.path.join(APP_ROOT, app_id)
    for root, dirs, files in os.walk(SRC_DIR):
        dirs[:] = [d for d in dirs if d not in ('js', 'webOSUserScripts')]
        for filename in files:
            source = os.path.join(root, filename)
            rel = os.path.relpath(source, SRC_DIR).replace(os.sep, '/')
            entries.append(('file', f'{base}/{rel}', source))
    return entries


def main():
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    os.makedirs(DIST_DIR, exist_ok=True)

    with open(os.path.join(SRC_DIR, 'appinfo.json'), 'r', encoding='utf-8') as fp:
        appinfo = json.load(fp)

    app_id = appinfo['id']
    version = appinfo['version']
    title = appinfo.get('title', app_id)
    vendor = appinfo.get('vendor', 'local')

    control = f'''Package: {app_id}\nVersion: {version}\nArchitecture: all\nMaintainer: {vendor}\nDescription: {title}\nSection: misc\nPriority: optional\n'''

    control_tar = make_tar_gz([('text', './control', control)])
    data_tar = make_tar_gz(collect_data_files(app_id))

    ipk_name = f'{app_id}_{version}_all.ipk'
    ipk_path = os.path.join(DIST_DIR, ipk_name)
    write_ar(ipk_path, [
        ('debian-binary', b'2.0\n'),
        ('control.tar.gz', control_tar),
        ('data.tar.gz', data_tar),
    ])

    print(f'IPK gerado: {ipk_path}')


if __name__ == '__main__':
    main()
