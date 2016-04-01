import decimal
import Target_Data
import subprocess
import psutil as ps


def kill_old():
    """
    Checks to see if there are old astrometry-engine processes still running.  If there are, they are terminated.
    :return:
    """
    try:
        astrometry_engine_dict = {}
        # key: cpu create time; value: proc ID
        for p in ps.pids():
            if ps.Process(p).name() == 'astrometry-engine':
                astrometry_engine_dict[ps.Process(p).create_time()] = p
            else:
                pass
        if len(astrometry_engine_dict) > 1:
            old_engine_time = max(astrometry_engine_dict.keys())
            old_engine = ps.Process(astrometry_engine_dict.get(key=old_engine_time))
            old_engine.terminate()
            return True
    except ps.ZombieProcess:
        return False
        pass
    except ps.NoSuchProcess:
        pass
        return False
    except:
        raise


def astro_pipe(files, dict1, dict2):
    """
    Runs astrometry.net on input file.  ra and dec are modified to be used in check_call method that
    runs astrometry.net with the following arguments:

        solve-field --use-sextractor --overwrite --downsample <int> --ra <degrees>
        --dec <degrees> --radius <arcminutes> 'filename'

    :param file: input file in which to run astrometry.net on
    :param dict1: used as a dictionary to determine ra from some file
    :param dict2: used as a dictionary to determine dec from some file
    """
    # set precision for decimal objects to 2 decimal points.
    decimal.getcontext().prec = 2

    # Script used in check_call to run astrometry.net as a process.
    script1 = 'solve-field --use-sextractor --overwrite --no-plots --no-fits2fits --ra %s --dec %s --radius 5 "%s"'

    # instantiate TargetData class
    td = Target_Data.TargetData()

    script_len = len(script1)
    timeoutlist_file = open(files[0].split('.', 1)[0] + '_timeout.txt', 'a')
    timeout_time = 10
    for i in files:
        kill_old()
        try:
            # note that ra is returned in hour angles.
            ra = td.coord_lookup(i, dict1)
            dec = td.coord_lookup(i, dict2)
            if ra == False or dec == False:
                print('Coordinate lookup error.  Check to see if target exists in target_data.txt.')
            # Convert ra from str to Decimal and multiply by 15 to give angles in degrees as opposed to hour angles.
            # ra_angles is cast back to str during assignment for consistency with dec_int.
            ra_decimal = decimal.Decimal(ra)
            ra_angle = str(ra_decimal * 15)

            subprocess.run(script1 % (ra_angle, dec, i), shell=True, timeout=timeout_time)

        except KeyboardInterrupt:
            print('Halted')
        except subprocess.TimeoutExpired:
            # populate timeout list with file names of files that timed out during astrometrization
            timeoutlist_file.write(i + ' terminated after ' + str(timeout_time) + ' seconds.')
            timeoutlist_file.write('\n')
        except:
            print('File name: ' + i + '  ra: ' + ra_angle + '  dec: ' + dec)
            timeoutlist_file.close()
            raise
    timeoutlist_file.close()
