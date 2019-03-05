import glob
import errno
path = 'awaiting_documents/*.txt'
files = glob.glob(path)
file = []
for name in files:
    try:
        file.append(open(name))
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
print(file[0].read())