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
        os.environ['rpg_path'] = '/home/shigezhuti/geode_ws/test_results/{}/FAST_LIO'.format(sequence_folder)
        os.environ['result_path'] = '{}/{}/'.format(os.environ['rpg_path'], seq_name[idx])
        print(os.environ['result_path'])
        command = 'mkdir -p $result_path'
        os.system(command)
        for trial in range(0, mc_trials):
            print('mc_trial {}'.format(trial))
            # os.environ['data_path'] = '{}/lidar_calibration/mloam_dataset/SR_monte_carlo/group_{}/{}.bag'.format(os.environ['DATA_PATH'], trial, seq_name[idx])
            os.environ['data_path'] = '/media/shigezhuti/SATA2/GEODE/alpha/outdoor/{}.bag'.format(seq_name[idx])
            command = 'bash {}'.format(seq_main_name)
            os.system(command)        
            command = 'mv /home/shigezhuti/geode_ws/src/FAST_LIO/Log/pos_log.txt $result_path/fast_lio_{}.txt'.format(trial)
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

    if  args.sequence == 'alpha':
        sequence_folder = 'alpha'
        # seq_name = ['Offroad1_alpha_rect', 'Offroad2_alpha_rect','Offroad3_alpha_rect','Offroad4_alpha_rect','Offroad5_alpha_rect','Offroad6_alpha_rect','Offroad7_alpha_rect','Tunneling_tunnel2_alpha_rect','Tunneling_tunnel3_alpha_rect','Tunneling_tunnel4_alpha_rect','Tunneling_tunnel5_alpha_rect']
        # seq_name = ['Offroad1_alpha_rect', 'Offroad2_alpha_rect','Offroad3_alpha_rect','Offroad4_alpha_rect','Offroad5_alpha_rect','Offroad6_alpha_rect','Offroad7_alpha_rect']
        seq_name = ['bridge01','bridge02','bridge03','Offroad1_alpha','Offroad2_alpha','Offroad3_alpha','Offroad4_alpha','Offroad5_alpha','Offroad6_alpha','Offroad7_alpha','Urban_Tunnel01','Urban_Tunnel02','Urban_Tunnel03']
        # seq_name = ['bridge01','bridge02','bridge03','Inland_Waterways_Long_Alpha','Inland_Waterways_Medium_Alpha','Inland_Waterways_Short_Alpha','Offroad1_alpha','Offroad2_alpha','Offroad3_alpha','Offroad4_alpha','Offroad5_alpha','Offroad6_alpha','Offroad7_alpha','Urban_Tunnel01','Urban_Tunnel02','Urban_Tunnel03']
        # seq_name = ['stairs_alpha','Tunneling_tunnel3_alpha','Tunneling_tunnel4_alpha','Tunneling_tunnel5_alpha']
        platform = 'real_vehicle/oxford'
        seq_main_name = 'alpha_main.sh'
    elif args.sequence == 'bob':
        sequence_folder = 'bob'
        seq_name = ['stairs_bob']
        platform = 'real_vehicle/oxford'
        seq_main_name = 'bob_main.sh'
        yaml_name = 'config_realvehicle_oxford.yaml'  
    elif args.sequence == 'carol':
        sequence_folder = 'carol'
        seq_name = ['stairs_carol']
        platform = 'real_vehicle/oxford'
        seq_main_name = 'carol_main.sh'
        yaml_name = 'config_realvehicle_oxford.yaml' 
    elif args.sequence == 's3e3':
        sequence_folder = 's3e3'
        seq_name = ['Tunneling_tunnel3_alpha','Tunneling_tunnel4_alpha','Tunneling_tunnel5_alpha']
        platform = 'real_vehicle/oxford'
        seq_main_name = 's3e.sh'
        yaml_name = 'config_realvehicle_oxford.yaml'
    elif args.sequence == 'kitti':
        sequence_folder = 'kitti'
        seq_name = ['kitti_sequence_01','kitti_sequence_04','kitti_sequence_05','kitti_sequence_07','kitti_sequence_09','kitti_sequence_10']
        platform = 'real_vehicle/oxford'
        seq_main_name = 'kitti_main.sh'
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


