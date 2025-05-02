import cv2
import numpy as np
from utils import calculate_angle
from pose_detector import PoseDetector

class ExerciseDetector:
    def __init__(self, exercise_type, model_path='mediapipe'):
        self.exercise_type = exercise_type
        self.counter = 0
        self.status = True
        self.pose_detector = PoseDetector()

    def detect_exercise(self, frame):
        height, width, _ = frame.shape
        self.pose_detector.set_frame_dimensions(width, height)
        keypoints = self.pose_detector.predict_pose(frame)
        if keypoints:
            print("Keypoints detected:", keypoints)  # Imprimir puntos clave detectados
            if self.exercise_type == "squat":
                return self.count_squats(keypoints)
            elif self.exercise_type == "push-up":
                return self.count_push_ups(keypoints)
        return self.counter, self.status

    def count_squats(self, keypoints):
        left_knee = keypoints[25]
        right_knee = keypoints[26]
        left_hip = keypoints[23]
        right_hip = keypoints[24]
        left_ankle = keypoints[27]
        right_ankle = keypoints[28]

        if all(kp[2] > 0.5 for kp in [left_knee, right_knee, left_hip, right_hip, left_ankle, right_ankle]):
            left_knee_angle = calculate_angle(left_hip[:2], left_knee[:2], left_ankle[:2])
            right_knee_angle = calculate_angle(right_hip[:2], right_knee[:2], right_ankle[:2])
            avg_knee_angle = (left_knee_angle + right_knee_angle) / 2
            print(f"Left knee angle: {left_knee_angle}, Right knee angle: {right_knee_angle}, Avg knee angle: {avg_knee_angle}")

            if self.status:
                if avg_knee_angle < 140:  # Ajusta este umbral según sea necesario para detectar la bajada
                    self.counter += 1
                    self.status = False
                    print("Squat counted!")
            else:
                if avg_knee_angle > 160: # Ajusta este umbral según sea necesario para detectar la subida
                    self.status = True
        return self.counter, self.status

    def count_push_ups(self, keypoints):
        left_elbow = keypoints[13]
        right_elbow = keypoints[14]
        left_shoulder = keypoints[11]
        right_shoulder = keypoints[12]
        left_wrist = keypoints[15]
        right_wrist = keypoints[16]

        if all(kp[2] > 0.5 for kp in [left_elbow, right_elbow, left_shoulder, right_shoulder, left_wrist, right_wrist]):
            left_arm_angle = calculate_angle(left_shoulder[:2], left_elbow[:2], left_wrist[:2])
            right_arm_angle = calculate_angle(right_shoulder[:2], right_elbow[:2], right_wrist[:2])
            avg_arm_angle = (left_arm_angle + right_arm_angle) / 2
            print(f"Left arm angle: {left_arm_angle}, Right arm angle: {right_arm_angle}, Avg arm angle: {avg_arm_angle}")

            if self.status:
                if avg_arm_angle < 90:  # Umbral para "abajo" - ajusta
                    self.counter += 1
                    self.status = False
            else:
                if avg_arm_angle > 160: # Umbral para "arriba" - ajusta
                    self.status = True
        return self.counter, self.status
