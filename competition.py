import cv2
import time
import threading
from exercise_detector import ExerciseDetector
from utils import score_table

class Competition:
    def __init__(self, exercise_type, duration, model_path):
        self.exercise_type = exercise_type
        self.duration = duration
        self.cap = cv2.VideoCapture(0)  # Usa la cámara integrada
        self.cap.set(3, 640)  # width
        self.cap.set(4, 480)  # height
        self.counter1 = 0
        self.counter2 = 0
        self.status1 = True
        self.status2 = True
        self.detector1 = ExerciseDetector(self.exercise_type, model_path)
        self.detector2 = ExerciseDetector(self.exercise_type, model_path)
        self.lock = threading.Lock()

    def process_participant(self, detector, frame, counter, status, participant_id):
        with self.lock:
            counter[0], status[0] = detector.detect_exercise(frame)

    def start(self):
        start_time = time.time()
        status1 = [True]
        status2 = [True]
        cv2.namedWindow('Competition', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Competition', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while int(time.time() - start_time) < self.duration:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: No se pudo leer el marco de la cámara.")
                break

            width = frame.shape[1] // 2
            frame1 = frame[:, :width]
            frame2 = frame[:, width:]

            counter1 = [0]
            counter2 = [0]

            thread1 = threading.Thread(target=self.process_participant, args=(self.detector1, frame1, counter1, status1, 1))
            thread2 = threading.Thread(target=self.process_participant, args=(self.detector2, frame2, counter2, status2, 2))

            thread1.start()
            thread2.start()

            thread1.join()
            thread2.join()

            self.counter1 = counter1[0]
            self.counter2 = counter2[0]
            self.status1 = status1[0]
            self.status2 = status2[0]

            time_left = max(0, self.duration - int(time.time() - start_time))
            frame = score_table(self.exercise_type, frame, self.counter1, self.status1, self.counter2, self.status2, time_left)

            cv2.imshow('Competition', frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
        self.declare_winner()

    def declare_winner(self):
        if self.counter1 > self.counter2:
            print("Participante 1 es el ganador!")
        elif self.counter2 > self.counter1:
            print("Participante 2 es el ganador!")
        else:
            print("Es un empate!")
