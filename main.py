import argparse
from competition import Competition

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--exercise_type", type=str, help='Type of activity to do', required=True)
ap.add_argument("-d", "--duration", type=int, help='Duration of the competition in seconds', required=True)
ap.add_argument("-m", "--model_path", type=str, default='movenet_v2_large', help='Path to the model file (or model type)')
args = vars(ap.parse_args())

competition = Competition(args["exercise_type"], args["duration"], args["model_path"])
competition.start()
