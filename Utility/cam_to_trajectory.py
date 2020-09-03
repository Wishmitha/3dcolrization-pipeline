import argparse
import os
import glob

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", help="path to folder containing cam files to be written")
    parser.add_argument("--output_dir", help="where to put output trajectory file")
    args, unknown = parser.parse_known_args()

    args = parser.parse_args()

    print(args.input_dir)

    if args.input_dir is None or not os.path.exists(args.input_dir):
        raise Exception("input_dir does not exist")
    if os.path.exists(os.path.join(args.output_dir, "key.log")):
        os.remove(os.path.join(args.output_dir, "key.log"))

    cam_files = glob.glob(os.path.join(args.input_dir, "*.txt"),recursive=True)

    count = 0

    for cam_file in cam_files:
        f=open(cam_file)
        lines=f.readlines()

        out = open(os.path.join(args.output_dir, "key.log"), "a")
        out.write(str(count)+" "+str(count)+" "+str(count+1)+'\n')
        out.writelines(lines[1:5])

        count +=1

    out.close()
    print('DONE.')