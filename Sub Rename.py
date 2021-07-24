import os, sys, re
print('Automatic Subtitle File Rename Script by Billy Cao')
print(f'Running on Python {sys.version}')

targetDir = input('Enter target dir: ')
while not os.path.isdir(targetDir):
    if input('Dir does not exist! Would you like to try again? (Y/N)').upper() == 'N':
        sys.exit()
    targetDir = input('Enter target dir: ')
os.chdir(targetDir)
print(f'Dir changed to {os.getcwd()}\nScanning files...')

VidFormats = {'mkv': 'Matroska',
              'mp4': 'MPEG-4 Part 14',
              'mov': 'QuickTime Movie'}
SubFormats = {'srt': 'SubRip',
              'ass': 'Advanced SubStation Alpha',
              'ssa': 'SubStation Alpha',
              'sub': 'DirectVobSub',
              'vtt': 'WebVTT'}

files = os.listdir()
videoFiles = [f for f in files if f.split('.')[-1].lower() in VidFormats]
subFiles = [f for f in files if f.split('.')[-1].lower() in SubFormats]
VideoFileNames = [f.split('.')[0] for f in videoFiles]
SubFileNames = [f.split('.')[0] for f in subFiles]
videoFileFormat = videoFiles[0].split('.')[-1]
subFileFormat = subFiles[0].split('.')[-1]

if not files:
    print('ERROR: no file found!')
elif not videoFiles:
    print('ERROR: no video file found!')
elif not subFiles:
    print('ERROR: no subtitle file found!')
print(f'Found {len(files)} files: {len(videoFiles)} {videoFileFormat} ({VidFormats[videoFileFormat]}) video files and {len(subFiles)} {subFileFormat} ({SubFormats[subFileFormat]}) subtitle files.')

ivid = int(input('Enter the position of episode number in VIDEO file name (E.g. first number in file name is the episode -> 0, 2nd -> 1 etc.): '))
isub = int(input('Enter the position of episode number in SUBTITLE file name (E.g. first number in file name is the episode -> 0, 2nd -> 1 etc.): '))

vid_eps = dict([(re.findall(r"\d+", f)[ivid], f) for f in VideoFileNames])
sub_eps = dict([(f, re.findall(r"\d+", f)[isub]) for f in subFiles])
eps = sorted(sub_eps.values())
print(f'Found {len(eps)} episodes of subtitle files: {", ".join(eps)}')

if len(eps) != len(set(eps)):
    print('Warning: there are duplicated episodes detected!')
if len(eps) == len(subFiles) and len(eps) != len(videoFiles):
    print('Warning: number of subtitle file episodes does not match with number of video file episodes!')
elif len(eps) != len(subFiles):
    print('Warning: number of subtitle episodes found does not match with number of subtitle files!')

if input('Start renaming? (Y/N): ').upper() == 'Y':
    for f in subFiles:
        new_name = vid_eps[sub_eps[f]] + '.' + subFileFormat
        os.rename(f, new_name)
        print(f'Renamed {f} -> {new_name}')
    else:
        print(f'{len(subFiles)} renamed successfully!')
        input("Press enter to exit")  # to keep console window open
else:
    print('Operation cancelled.')
    sys.exit()
