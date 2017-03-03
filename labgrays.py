from __future__ import print_function
import numpy as np
import os

if __name__ == '__main__':
    np.random.seed(0)

    L_min = 2
    L_max = 98
    a_min = -2.0
    a_max = 2.0
    b_min = -2.0
    b_max = 2.0
    n_patches = 880
    lab_filename = 'lab.txt'
    icc_profile_filename = 'i1proTarget_good.icc'
    rgb_xyz_filename = 'RGB-XYZ.txt'
    ti1_original_filename = 'i1proTarget.ti1'
    ti1_output_filename = 'i1proTarget_combined.ti1'

    print('Generating %s Lab neutral color points.' % n_patches)
    L = np.linspace(L_min, L_max, n_patches)  # .astype(np.int)
    a = np.random.uniform(low=a_min, high=a_max, size=n_patches)
    b = np.random.uniform(low=b_min, high=b_max, size=n_patches)

    tmp = np.vstack([L, a, b]).T
    print('Saving color points in %s' % lab_filename)
    np.savetxt(open(lab_filename, 'w'), tmp, fmt='%f', delimiter=' ')

    print('Converting Lab values to RGB-XYZ through %s' % icc_profile_filename)
    # See: http://www.russellcottrell.com/photo/ArgyllColorPatches.htm
    command = 'icclu -v0 -fb -ir -pl -s100 %s < %s | icclu -v1 -ff -ia -pX -s100 %s > %s' % (icc_profile_filename,
                                                                                             lab_filename,
                                                                                             icc_profile_filename,
                                                                                             rgb_xyz_filename)
    print('Executing %s' % command)
    os.system(command)

    print('Loading %s' % ti1_original_filename)
    print('Creating %s' % ti1_output_filename)
    f = open(ti1_output_filename, 'w')
    flag = True
    for line in open(ti1_original_filename):
        if line.startswith('NUMBER_OF_SETS') and flag:
            tmp, n_patches_original = line.split()
            n_patches_original = int(n_patches_original)
            flag = False
            print('Found %s patches' % n_patches_original)
            print('Modifying the total number of patches, now %s' % (n_patches_original + n_patches))
            f.write(tmp + ' ' + str(n_patches_original + n_patches) + '\n')
        elif not flag and line.startswith(str(n_patches_original)):
            f.write(line)
            print('Adding new patches')
            for i, line2 in enumerate(open(rgb_xyz_filename)):
                line3 = ' '.join(line2.split()[:3] + line2.split()[7:10]) + '\n'
                f.write(str(n_patches_original + i + 1) + ' ' + line3)

        else:
            f.write(line)

    f.close()
    print('Done.')
