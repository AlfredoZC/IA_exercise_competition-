import cv2
import mediapipe as mp
import torch

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        print(f"cuDNN version: {torch.backends.cudnn.version()}")

    def predict_pose(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        keypoints = []
        if results.pose_landmarks:
            for landmark in results.pose_landmarks.landmark:
                keypoints.append((int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]), landmark.visibility))
        return keypoints

    def set_frame_dimensions(self, width, height):
        self.width = width
        self.height = height

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    detector = PoseDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width, _ = frame.shape
        detector.set_frame_dimensions(width, height)
        keypoints = detector.predict_pose(frame)

        if keypoints:
            for i, (x, y, confidence) in enumerate(keypoints):
                if confidence > 0.5:
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                    cv2.putText(frame, str(i), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        cv2.imshow('MediaPipe Pose Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
