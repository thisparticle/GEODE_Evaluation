# ! /usr/bin/python2
# Usage: python run_sr_test.py -sequence=SR -program=mc_test -start_idx=0 -end_idx=4 -trials=10

import os
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

sequence_folder = ''
seq_name = []
platform = ''
seq_main_name = ''
est_type = ''
yaml_name = ''


# python3 test_s3e_de.py -sequence=Inland_Waterways_Carol -program=mc_test -start_idx=0 -end_idx=0 -mc_trials=2
def mc_test(start_idx, end_idx, mc_trials):
    for idx in range(start_idx, end_idx + 1):
        print('testing sequence: {}'.format(seq_name[idx]))
        os.environ['rpg_path'] = '/home/thisparticle/shige/S3E--/evluation/{}/DLIO'.format(sequence_folder)
        os.environ['result_path'] = '{}/{}/'.format(os.environ['rpg_path'], seq_name[idx])
        print(os.environ['result_path'])
        command = 'mkdir -p $result_path'
        os.system(command)
        for trial in range(0, mc_trials):
            print('mc_trial {}'.format(trial))
            # os.environ['data_path'] = '{}/lidar_calibration/mloam_dataset/SR_monte_carlo/group_{}/{}.bag'.format(os.environ['DATA_PATH'], trial, seq_name[idx])
            os.environ['data_path'] = '/media/thisparticle/新加卷/shige/GEODE/Stairs/{}.bag'.format(seq_name[idx])
            command = 'bash {}'.format(seq_main_name)
            os.system(command)        
            # command = 'mv $result_path/traj/stamped_groundtruth.txt $result_path/traj/stamped_groundtruth{}.txt'.format(trial)
            command = 'mv /home/thisparticle/baseline_ws/dlio_ws/path.txt $result_path/dlio_{}.txt'.format(trial)
            os.system(command)                              

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run s3e_de sr test')
    parser.add_argument('-program', help='debug_test, debug_eval, \
        calib_test, single_test, single_eval, mc_test, mc_eval, inject_ext_uct_test')
    parser.add_argument('-sequence', help='Inland_Waterways_Alpha, Inland_Waterways_Bob, Inland_Waterways_Carol, OR')
    parser.add_argument('-start_idx', type=int, help='idx')
    parser.add_argument('-end_idx', type=int, help='idx')
    parser.add_argument('-mc_trials', type=int, help='mc_trials=n')
    parser.add_argument('-ext_level', help='gt, ref, cad, ini, inj')
    parser.add_argument('-est_type', help='xx_xx')
    args = parser.parse_args()

    if args.sequence == 'alpha':
        sequence_folder = 'alpha'
        # seq_name = ['Offroad1_alpha_rect', 'Offroad2_alpha_rect','Offroad3_alpha_rect','Offroad4_alpha_rect','Offroad5_alpha_rect','Offroad6_alpha_rect','Offroad7_alpha_rect','Tunneling_tunnel2_alpha_rect','Tunneling_tunnel3_alpha_rect','Tunneling_tunnel4_alpha_rect','Tunneling_tunnel5_alpha_rect']
        # seq_name = ['Offroad1_alpha_rect', 'Offroad2_alpha_rect','Offroad3_alpha_rect','Offroad4_alpha_rect','Offroad5_alpha_rect','Offroad6_alpha_rect','Offroad7_alpha_rect']
        # seq_name = ['Tunneling_tunnel2_alpha_rect','Tunneling_tunnel3_alpha_rect','Tunneling_tunnel4_alpha_rect','Tunneling_tunnel5_alpha_rect']
        seq_name = ['stairs_alpha']
        platform = 'real_vehicle/oxford'
        seq_main_name = 'alpha_main.sh'
        yaml_name = 'config_realvehicle_oxford.yaml'  
    elif args.sequence == 'bob':
        sequence_folder = 'bob'
        # seq_name = ['Offroad1_bob', 'Offroad2_bob', 'Offroad3_bob', 'Offroad4_bob','Offroad5_bob','Offroad6_bob','Offroad7_bob']
        # seq_name = ['Shield_tunnel7_bob_rect', 'Shield_tunnel8_bob_rect', 'Shield_tunnel9_bob_rect', 'Shield_tunnel10_bob_rect','Tunneling_tunnel2','Tunneling_tunnel3','Tunneling_tunnel4','Tunneling_tunnel5']
        seq_name = ['stairs_bob']
        platform = 'real_vehicle/oxford'
        seq_main_name = 'bob_main.sh'
        yaml_name = 'config_realvehicle_oxford.yaml'  
    elif args.sequence == 'carol':
        sequence_folder = 'carol'
        # seq_name = ['Offroad1_carol', 'Offroad2_carol', 'Offroad3_carol', 'Offroad4_carol','Offroad5_carol','Offroad6_carol','Offroad7_carol']
        # seq_name = ['Tunneling_tunnel1', 'Tunneling_tunnel2', 'Tunneling_tunnel3', 'Tunneling_tunnel4','Tunneling_tunnel5','Shield_tunnel1','Shield_tunnel2','Shield_tunnel3','Shield_tunnel4','Shield_tunnel5','Shield_tunnel6','Offroad1_carol', 'Offroad2_carol', 'Offroad3_carol', 'Offroad4_carol','Offroad5_carol','Offroad6_carol','Offroad7_carol']
        # seq_name = ['Offroad1_carol', 'Offroad2_carol', 'Offroad3_carol', 'Offroad4_carol','Offroad5_carol','Offroad6_carol','Offroad7_carol']
        seq_name = ['stairs_carol']
        platform = 'real_vehicle/oxford'
        seq_main_name = 'carol_main.sh'
        yaml_name = 'config_realvehicle_oxford.yaml' 

    if len(seq_name) < args.end_idx:
        print('exit! end_idx is too large: {} > {}'.format(args.end_idx, len(seq_name)))
        sys.exit(0)

    if args.start_idx > args.end_idx:
        print('exit! start_idx > end_idx: {} > {}'.format(args.start_idx, args.end_idx))
        sys.exit(0)      

    if args.program == 'calib_test':
        calib_test(args.start_idx, args.end_idx)
    elif args.program == 'debug_test':
        debug_test(args.start_idx)
    elif args.program == 'debug_eval':
        if not args.est_type:
            print('exit! no est_type')
            sys.exit(0)
        est_list = args.est_type.split(',')
        for str in est_list:
            est_type += str + ' '
        print('eval method: {}'.format(est_type))
        debug_eval()
    elif args.program == 'single_test':
        single_test(args.start_idx, args.end_idx)
    elif args.program == 'single_eval':
        est_list = args.est_type.split(',')
        for str in est_list:
            est_type += str + ' '
        print('eval method: {}'.format(est_type))
        single_eval(args.start_idx, args.end_idx)        
    elif args.program == 'mc_test':
        mc_test(args.start_idx, args.end_idx, args.mc_trials)
    elif args.program == 'mc_eval':
        est_list = args.est_type.split(',')
        for str in est_list:
            est_type += str + ' '
        print('eval method: {}'.format(est_type))
        mc_eval(args.start_idx, args.end_idx, args.mc_trials)
    elif args.program == 'inject_ext_uct_test':
        inject_ext_uct_test(args.start_idx, args.end_idx, args.ext_level)


