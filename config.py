import os

# creating variables
pipeline_root = ''

astrometry = pipeline_root + 'astrometry'
stacking = pipeline_root + 'stacking'
sex = pipeline_root + 'sex'
finished_catalogs = pipeline_root + 'finished_catalogs'
finished_stacked = pipeline_root + 'finished_stacked'
target_data = pipeline_root + 'target_data'
dirlists = [astrometry, stacking, sex, finished_catalogs, finished_stacked, target_data]


def makedirs():
    # making directories
    pipeline_root = input('Provide pipeline root directory:')
    for i in dirlists:
        try:
            os.mkdir(i)
        except FileExistsError:
            print(i, 'already exists.')
        except:
            raise
